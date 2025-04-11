# Credits. This code has been adapted from:
# https://github.com/adap/flower/tree/main/examples/advanced-tensorflow

from typing import Dict, Optional, Tuple
import flwr as fl

import tensorflow as tf
import os
import cv2
import numpy as np
from sklearn.utils import shuffle
from keras.preprocessing import image
import time

import edgeimpulse as ei

# Server address = {IP_ADDRESS}:{PORT}
server_address = "localhost:8000"

# This variable determines if model profiling and deployment with Edge Impulse will be done
profile_and_deploy_model_with_EI = False

# Change this to your Edge Impulse API key
ei.API_KEY = ""

# Defining a .eim file that will be automatically downloaded on the server computer
deploy_eim = "modelfile.eim"

# List with the classes for the image classification
classes = ["bluetit", "jackdaw", "robin"]  # Update classes
class_labels = {cls: i for i, cls in enumerate(classes)}  # Update class labels
number_of_classes = len(classes)

# Defining image size,
# a larger one means more data goes to the model (good thing) but processing time and model size will increase
IMAGE_SIZE = (160, 160)

federated_learning_counts = 2
local_client_epochs = 20
local_client_batch_size = 8

def main() -> None:
    start_time = time.time()  # Start timing
    # Load and compile model for server-side parameter initialization, server-side parameter evaluation
    
    # Loading and compiling Keras model, choose either MobileNetV2 (faster) or EfficientNetB0. 
    # Feel free to add more Keras applications
    # https://keras.io/api/applications/
 
    
    base_model = tf.keras.applications.MobileNetV2(
        input_shape=(160, 160, 3),
        alpha=1.0,
        include_top=False,
        weights="imagenet",
        input_tensor=None,
        pooling=None,
        classes=3,
        classifier_activation="softmax"
    )
    # Freeze the layers in the base model so they don't get updated
    base_model.trainable = False

    # Define classification head
    x = tf.keras.layers.GlobalAveragePooling2D()(base_model.output)
    x = tf.keras.layers.Dense(128, activation='relu')(x)
    outputs = tf.keras.layers.Dense(3, activation='softmax')(x)

    # Create the final model
    model = tf.keras.Model(inputs=base_model.input, outputs=outputs)

    # Compile the model
    model.compile(optimizer='adam', loss='sparse_categorical_crossentropy', metrics=['accuracy'])

    # Apply post-training quantization to the model
    converter = tf.lite.TFLiteConverter.from_keras_model(model)
    converter.optimizations = [tf.lite.Optimize.DEFAULT]
    quantized_tflite_model = converter.convert()

    # Create strategy
    strategy = fl.server.strategy.FedAvg(
        fraction_fit=0.3,
        fraction_evaluate=0.2,
        min_fit_clients=2,
        min_evaluate_clients=2,
        min_available_clients=2,
        evaluate_fn=get_evaluate_fn(model),
        on_fit_config_fn=fit_config,
        on_evaluate_config_fn=evaluate_config,
        initial_parameters=fl.common.ndarrays_to_parameters(
            model.get_weights()),
    )

    # Start Flower server (SSL-enabled) for X rounds of federated learning
    fl.server.start_server(
        server_address=server_address,
        config=fl.server.ServerConfig(num_rounds=federated_learning_counts),
        strategy=strategy
    )
    end_time = time.time()  # End timing
    total_time = end_time - start_time
    print(f"Total time taken for model compilation and training: {total_time} seconds")
def load_dataset():
    # Defining the directory with the server's test images. We only use the test images!
    directory = "datasets/dataset_server"
    sub_directories = ["test", "train"]

    loaded_dataset = []
    for sub_directory in sub_directories:
        path = os.path.join(directory, sub_directory)
        images = []
        labels = []

        print("Server dataset loading {}".format(sub_directory))

        for folder in os.listdir(path):
            label = class_labels[folder]

            # Iterate through each image in the folder
            for file in os.listdir(os.path.join(path,folder)):
                # Get path name of the image
                img_path = os.path.join(os.path.join(path, folder), file)

                # Open and resize the image
                image = cv2.imread(img_path)
                image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
                image = cv2.resize(image, IMAGE_SIZE)

                # Append the image and its corresponding label to loaded_dataset
                images.append(image)
                labels.append(label)

        images = np.array(images, dtype= 'float32')
        labels = np.array(labels, dtype= 'int32')

        loaded_dataset.append((images, labels))
    
    return loaded_dataset

def get_evaluate_fn(model):
    """Return an evaluation function for server-side evaluation."""

    # Load data and model here to avoid the overhead of doing it in `evaluate` itself
    (training_images, training_labels), (test_images, test_labels) = load_dataset()
    print("[Server] test_images shape:", test_images.shape)
    print("[Server] test_labels shape:", test_labels.shape)

    # The `evaluate` function will be called after every round
    def evaluate(
        server_round: int,
        parameters: fl.common.NDArrays,
        config: Dict[str, fl.common.Scalar],
    ) -> Optional[Tuple[float, Dict[str, fl.common.Scalar]]]:
        print("======= Server Round %s/%s Evaluate() ===== " %(server_round, federated_learning_counts))
        # Update model with the latest parameters
        model.set_weights(parameters)
        loss, accuracy = model.evaluate(test_images, test_labels, verbose=0)
        print("======= Server Round %s/%s Accuracy : %s =======" %(server_round, federated_learning_counts, accuracy))

        if (server_round == federated_learning_counts):
            # Save the decentralized ML model locally on the server computer
            print("Saving updated model locally..")
            model.save('saved_models/final_model.h5')  # Save the model in .h5 format

            # Test the updated model
            test_updated_model(model)

            # Using Edge Impulse Python SDK to profile the updated model and deploy it for various MCUs/MPUs
            if (profile_and_deploy_model_with_EI):
                ei_profile_and_deploy_model(model)
            else:
                print("Skipping profiling and deploying with Edge Impulse BYOM!")
             
        return loss, {"accuracy": accuracy}
    return evaluate

def fit_config(server_round: int):
    # Return training configuration dict for each round
    config = {
        "batch_size": local_client_batch_size,
        "local_epochs": local_client_epochs,
    }
    return config

def evaluate_config(server_round: int):
    """Return evaluation configuration dict for each round."""
    val_steps = 4
    return {"val_steps": val_steps}

def test_updated_model(model):
    # Test the model by giving it an image and get its prediction
    test_image_head_path = "datasets/dataset_test/bluetit/(121).jpg"
    test_image_head = cv2.imread(test_image_head_path)
    test_image_head = cv2.cvtColor(test_image_head, cv2.COLOR_BGR2RGB)
    test_image_head = cv2.resize(test_image_head, IMAGE_SIZE)

    test_image_hardhat_path = "datasets/dataset_test/robin/(121).jpg"
    test_image_hardhat = cv2.imread(test_image_hardhat_path)
    test_image_hardhat = cv2.cvtColor(test_image_hardhat, cv2.COLOR_BGR2RGB)
    test_image_hardhat = cv2.resize(test_image_hardhat, IMAGE_SIZE)

    print("Testing the final model on an image.....")
    # Chose either test_image_head or test_image_hardhat for the prediction
    image_test_result = model.predict(np.expand_dims(test_image_hardhat, axis=0))
    # Print the prediction scores/confidence for each class
    print(image_test_result[0])

    # An easy trick to see the model's prediction scores ("confidence") for each class
    highest_prediction_score = max(image_test_result[0])
    highest_prediction_score_index = 0
    for i in range(len(image_test_result[0])):
        if image_test_result[0][i] == highest_prediction_score:
            highest_prediction_score_index = i

    most_confident_class = classes[highest_prediction_score_index]
    print("The model mostly predicted %s with a score/confidence of %s" %(most_confident_class, highest_prediction_score))

def ei_profile_and_deploy_model(model):
    # List the available profile target devices
    ei.model.list_profile_devices()

    # Estimate the RAM, ROM, and inference time for our model on the target hardware family
    try:
        profile = ei.model.profile(model=model,
                                device='raspberry-pi-4')
        print(profile.summary())
    except Exception as e:
        print(f"Could not profile: {e}")

    # List the available profile target devices
    ei.model.list_deployment_targets()

    # Set model information, such as your list of labels
    model_output_type = ei.model.output_type.Classification(labels=classes)

    # Create eim executable with trained model
    deploy_bytes = None
    try:
        deploy_bytes = ei.model.deploy(model=model,
                                    model_output_type=model_output_type,
                                    deploy_target='runner-linux-aarch64',
                                    output_directory='ei_deployed_model')
    except Exception as e:
        print(f"Could not deploy: {e}")

    # Write the downloaded raw bytes to a file
    if deploy_bytes:
        with open(deploy_eim, 'wb') as f:
            f.write(deploy_bytes)

if __name__ == "__main__":
    main()