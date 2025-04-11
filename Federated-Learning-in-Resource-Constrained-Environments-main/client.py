# Credits. This code has been adapted from :
# https://github.com/adap/flower/tree/main/examples/advanced-tensorflow

import argparse
import flwr as fl

import tensorflow as tf
import os
import cv2
import numpy as np
from sklearn.utils import shuffle
from keras.preprocessing import image

# server address = {IP_ADDRESS}:{PORT}
server_address = "localhost:8000"

classes = ["bluetit", "jackdaw", "robin"]  # Update classes
class_labels = {cls: i for i, cls in enumerate(classes)}  # Update class labels
number_of_classes = len(classes)
IMAGE_SIZE = (160, 160)

# make TensorFlow logs less verbose
os.environ["TF_CPP_MIN_LOG_LEVEL"] = "3"

# define Flower client
class CifarClient(fl.client.NumPyClient):
    def __init__(self, model, training_images, training_labels, test_images, test_labels):
        self.model = model
        self.training_images, self.training_labels = training_images, training_labels
        self.test_images, self.test_labels = test_images, test_labels

    def get_properties(self, config):
        """Get properties of client."""
        raise Exception("Not implemented")

    def get_parameters(self, config):
        print("======= get_parameters() ===== ")
        """Get parameters of the local model."""
        raise Exception("Not implemented (server-side parameter initialization)")

    def fit(self, parameters, config):
        print("======= fit() ===== ")
        """Train parameters on the locally held training set."""

        # update local model parameters
        self.model.set_weights(parameters)

        # get hyperparameters for this round
        batch_size: int = config["batch_size"]
        epochs: int = config["local_epochs"]

        # train the model using hyperparameters from config
        history = self.model.fit(
            self.training_images,
            self.training_labels,
            batch_size,
            epochs,
            validation_split=0.2,
        )

        # return updated model parameters and results
        parameters_prime = self.model.get_weights()
        num_examples_train = len(self.training_images)
        results = {
            "loss": history.history["loss"][0],
            "accuracy": history.history["accuracy"][0],
            "val_loss": history.history["val_loss"][0],
            "val_accuracy": history.history["val_accuracy"][0],
        }
        return parameters_prime, num_examples_train, results

    def evaluate(self, parameters, config):
        print("======= evaluate() ===== ")
        """Evaluate parameters on the locally held test set."""

        # update local model with global parameters
        self.model.set_weights(parameters)

        # get config values
        steps: int = config["val_steps"]

        # evaluate global model parameters on the local test data and return results
        loss, accuracy = self.model.evaluate(self.test_images, self.test_labels)
        num_examples_test = len(self.test_images)
        return loss, num_examples_test, {"accuracy": accuracy}

def main() -> None:
    # argument to define the client's number
    client_argumentparser = argparse.ArgumentParser()
    client_argumentparser.add_argument(
                                    '--client_number', dest='client_number', type=int, 
                                    required=True,
                                    help='Used to load the dataset for the client')
    client_argumentparser = client_argumentparser.parse_args()
    client_number = client_argumentparser.client_number
    print("Client %s has been connected!" %client_number)

    # load and compile Keras model, choose either MobileNetV2 (faster) or EfficientNetB0. Needs to be same as the server!
    
    # # uncomment to load an EfficientNetB0 model
    # model = tf.keras.applications.EfficientNetB0(
    #     input_shape=(160, 160, 3), weights=None, classes=number_of_classes
    # )
    # model.compile("adam", "sparse_categorical_crossentropy", metrics=["accuracy"])
    
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
    # freeze the layers in the base model so they don't get updated
    base_model.trainable = False

    # define classification head
    x = tf.keras.layers.GlobalAveragePooling2D()(base_model.output)
    x = tf.keras.layers.Dense(128, activation='relu')(x)
    outputs = tf.keras.layers.Dense(3, activation='softmax')(x)

    # create the final model
    model = tf.keras.Model(inputs=base_model.input, outputs=outputs)

    # compile the model
    model.compile(optimizer='adam', loss='sparse_categorical_crossentropy', metrics=['accuracy'])

    # Load dataset for each client
    (training_images, training_labels), (test_images, test_labels) = load_dataset(client_number)

    # to train the model better, we can shuffle the data in the dataset
    training_images, training_labels = shuffle(training_images, training_labels, random_state = 25)

    # start Flower client
    client = CifarClient(model, training_images, training_labels, test_images, test_labels)

    fl.client.start_numpy_client(
        server_address=server_address,
        client=client
    )

# this function loads different datasets for the clients using the client's number
def load_dataset(client_number):
    if client_number == 1: 
        directory = "datasets/dataset_client1"
    elif client_number == 2:
        directory = "datasets/dataset_client2"
    
    sub_directories = ["test", "train"]

    loaded_dataset = []

    for sub_directory in sub_directories:
        path = os.path.join(directory, sub_directory)
        images = []
        labels = []

        print("Client dataset loading {}".format(sub_directory))

        for folder in os.listdir(path):
            label = class_labels[folder]

            # iterate through each image in the folder
            for file in os.listdir(os.path.join(path,folder)):
                # get path name of the image
                img_path = os.path.join(os.path.join(path, folder), file)

                # open and resize the image
                image = cv2.imread(img_path)
                image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
                image = cv2.resize(image, IMAGE_SIZE)

                # append the image and its corresponding label to loaded_dataset
                images.append(image)
                labels.append(label)

        images = np.array(images, dtype= 'float32')
        labels = np.array(labels, dtype= 'int32')

        loaded_dataset.append((images, labels))
    
    return loaded_dataset

if __name__ == "__main__":
    main()