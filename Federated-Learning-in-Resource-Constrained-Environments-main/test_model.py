import tensorflow as tf
import os
import cv2
import numpy as np
from keras.preprocessing import image

# list with the classes for the image classification
classes = ["bluetit", "jackdaw", "robin"]  # Update classes
class_labels = {cls: i for i, cls in enumerate(classes)}  # Update class labels
number_of_classes = len(classes)
IMAGE_SIZE = (160, 160)

# load a local model from the saved_models directory
# model = tf.keras.models.load_model('saved_models/mobilenetv2.h5')
model = tf.keras.models.load_model('saved_models/final_model.h5')
# model.summary()

# function to load images from a directory
def load_images_from_folder(folder):
    images = []
    for filename in os.listdir(folder):
        img_path = os.path.join(folder, filename)
        img = cv2.imread(img_path)
        if img is not None:
            img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            img = cv2.resize(img, IMAGE_SIZE)
            images.append(img)
    return images

# test the model on images from each folder
total_accuracy = 0.0
total_folders = 0

# iterate over each folder in dataset_test
for folder_name in os.listdir("datasets/dataset_test"):
    folder_path = os.path.join("datasets/dataset_test", folder_name)
    if os.path.isdir(folder_path):
        true_label = folder_name  # true label is the folder name
        print(f"\nTesting the model on images from folder: {true_label}")

        # load images from the folder
        images = load_images_from_folder(folder_path)
        if len(images) == 0:
            print(f"No images found in folder: {folder_name}")
            continue

        # predict labels for the images
        predictions = model.predict(np.array(images))

        # calculate accuracy
        correct_predictions = sum(1 for pred in predictions.argmax(axis=1) if classes[pred] == true_label)
        accuracy = correct_predictions / len(images)
        total_accuracy += accuracy
        total_folders += 1

        print(f"Accuracy for folder {true_label}: {accuracy}")

# calculate average accuracy
average_accuracy = total_accuracy / total_folders if total_folders > 0 else 0.0
print(f"\nAverage accuracy across all folders: {average_accuracy}")