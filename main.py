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
from data import *


from matplotlib import pyplot as plt

class_names = np.unique(train.class_names)

n_rows = 4
n_cols = 10
plt.figure(figsize=(n_cols * 1.2, n_rows * 1.2))
data = list(train.take(n_rows*n_cols))
for row in range(n_rows):
    for col in range(n_cols):
        index = n_cols * row + col
        single_image = data[index][0][0]
        plt.subplot(n_rows, n_cols, index + 1)
        plt.imshow(single_image.numpy().astype("uint8"),cmap="gray")
        plt.axis('off')
        label_index = data[index][1][0]
        plt.title(class_names[label_index], fontsize=12)
plt.subplots_adjust(wspace=0.2, hspace=0.5)
plt.show()


model = models.Sequential()

model.add(layers.Conv2D(64,(3,3),activation="relu", padding='same', input_shape=(64, 64, 3)))
model.add(layers.Conv2D(64,(3,3),activation="relu", padding='same'))
model.add(layers.MaxPooling2D((2,2), strides=(2, 2)))


model.add(layers.Conv2D(128,(3,3),activation="relu", padding='same'))
model.add(layers.Conv2D(128,(3,3),activation="relu", padding='same'))
model.add(layers.MaxPooling2D((2,2), strides=(2, 2)))


model.add(layers.Conv2D(256,(3,3),activation="relu", padding='same'))
model.add(layers.Conv2D(256,(3,3),activation="relu", padding='same'))
model.add(layers.MaxPooling2D((2,2), strides=(2, 2)))

model.add(layers.Flatten())
model.add(layers.Dropout(0.5))  
model.add(layers.Dense(256,activation="relu"))
model.add(layers.Dense(512,activation="relu")) 
model.add(layers.Dense(1,activation="sigmoid"))

model.summary()

optimizer = tf.keras.optimizers.Adam(0.0003)

model.compile(optimizer=optimizer,loss=tf.keras.losses.BinaryCrossentropy(), metrics=['accuracy'])

early_stopping_cb = keras.callbacks.EarlyStopping(patience=5,restore_best_weights=True)
history = model.fit(train,epochs=20,batch_size=32,validation_data=val, callbacks=[early_stopping_cb])

model.evaluate(test)

model.save("my_model.keras")
#model.save('my_model.h5')