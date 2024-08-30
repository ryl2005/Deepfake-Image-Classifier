import numpy as np
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers, models
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Input, Conv2D, MaxPooling2D, Flatten
from sklearn.model_selection import train_test_split
from tensorflow.keras.preprocessing.image import ImageDataGenerator
import os
from PIL import Image


# Update the path to your local dataset directory
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
        image_size=(32, 32) #Can make smaller to make run faster also need to change ln 61 input shape to same size
    )

# Load the datasets
train = get_from_dir("Train")
test = get_from_dir("Test")
val = get_from_dir("Validation")


from matplotlib import pyplot as plt

class_names = np.unique(train.class_names)

n_rows = 4
n_cols = 10
plt.figure(figsize=(n_cols * 1.2, n_rows * 1.2))
data = list(train.take(n_rows*n_cols))
for row in range(n_rows):
    for col in range(n_cols):
        index = n_cols * row + col
        # Obtener solo la primera imagen del lote
        single_image = data[index][0][0]  # Tomar la primera imagen del primer lote
        plt.subplot(n_rows, n_cols, index + 1)
        plt.imshow(single_image.numpy().astype("uint8"),cmap="gray")  # Convertir a tipo uint8 para imshow
        plt.axis('off')
        # Convertir a un solo valor antes de usarlo para indexar class_names
        label_index = data[index][1][0]
        plt.title(class_names[label_index], fontsize=12)
plt.subplots_adjust(wspace=0.2, hspace=0.5)
plt.show()


model = models.Sequential()

model.add(layers.Conv2D(32,(3,3),activation="relu", padding='same', input_shape=(32, 32, 3)))
model.add(layers.Conv2D(32,(3,3),activation="relu", padding='same'))
model.add(layers.MaxPooling2D((2,2), strides=(2, 2)))


model.add(layers.Conv2D(64,(3,3),activation="relu", padding='same'))
model.add(layers.Conv2D(64,(3,3),activation="relu", padding='same'))
model.add(layers.MaxPooling2D((2,2), strides=(2, 2)))


model.add(layers.Conv2D(128,(3,3),activation="relu", padding='same'))
model.add(layers.Conv2D(128,(3,3),activation="relu", padding='same'))
model.add(layers.MaxPooling2D((2,2), strides=(2, 2)))

model.add(layers.Flatten())
model.add(layers.Dropout(0.5))
model.add(layers.Dense(128,activation="relu"))
model.add(layers.Dense(256,activation="relu"))
model.add(layers.Dense(1,activation="sigmoid"))

model.summary()

model.compile('adam',loss=tf.keras.losses.BinaryCrossentropy(), metrics=['accuracy'])

early_stopping_cb = keras.callbacks.EarlyStopping(patience=5,restore_best_weights=True)
history = model.fit(train,epochs=20,batch_size=32,validation_data=val,callbacks=[early_stopping_cb])

model.save("modelo_detector_caras.keras")