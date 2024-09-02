import tensorflow as tf
import os

path = "/Users/ryanlee/SPIS_Test1/dataset"

def get_from_dir(dir):
    dir_path = os.path.join(path, dir)
    print(f"Loading images from: {dir_path}")  # Print the directory path
    if not os.path.isdir(dir_path):
        raise FileNotFoundError(f"Directory not found: {dir_path}")
    return tf.keras.utils.image_dataset_from_directory(
        dir_path,
        labels='inferred',
        color_mode="rgb",
        seed=42,
        batch_size=32,
        image_size=(64, 64) #Can make smaller to make run faster also need to change ln 61 input shape to same size
    )

# Load the datasets
train = get_from_dir("Train")
test = get_from_dir("Test")
val = get_from_dir("Validation")