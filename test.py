import tensorflow as tf
import numpy as np
from matplotlib import pyplot as plt
from tensorflow import keras
import pandas as pd
from data import test
import matplotlib.pyplot as plt
import os


newModel = tf.keras.models.load_model('my_model.keras')

import numpy as np
import matplotlib.pyplot as plt
from sklearn.metrics import confusion_matrix, ConfusionMatrixDisplay

# Assuming `test` is a DataLoader or iterable yielding (images, labels)
true_labels = []
predictions = []
images_list = []

for images, labels in test:
    true_labels.extend(labels.numpy())
    batch_predictions = newModel.predict(images) >= 0.5
    predictions.extend(batch_predictions.astype(int).flatten())
    images_list.extend(images.numpy())

true_labels = np.array(true_labels)
predictions = np.array(predictions)

# Confusion Matrix
cm = confusion_matrix(true_labels, predictions)
disp = ConfusionMatrixDisplay(confusion_matrix=cm)
disp.plot()
plt.show()

# Function to visualize all images and specific mismatches on the same plot
def visualize_combinations(images, true_labels, predictions, num_images=9):
    # Create a subplot grid with 3 rows: all images, true=0 & pred=1, and true=1 & pred=0
    fig, axes = plt.subplots(3, num_images, figsize=(15, 15))
    
    # Plot all images
    indices_to_show = np.random.choice(len(images), min(num_images, len(images)), replace=False)
    for i, idx in enumerate(indices_to_show):
        ax = axes[0, i]
        img = images[idx]
        if img.max() > 1:
            img = img / 255.0  # Normalize to [0, 1] if image values are [0, 255]
        ax.imshow(img)
        ax.axis('off')
        ax.set_title(f'True: {true_labels[idx]}\nPred: {predictions[idx]}')
    
    # Plot true=0 & pred=1 images
    mismatched_indices_0_1 = [
        i for i in range(len(true_labels)) 
        if true_labels[i] == 0 and predictions[i] == 1
    ]
    num_images_mismatches_0_1 = min(num_images, len(mismatched_indices_0_1))
    if num_images_mismatches_0_1 == 0:
        print("No mismatched images where true=0 and pred=1 found.")
    else:
        for i in range(num_images_mismatches_0_1):
            idx = mismatched_indices_0_1[i]
            ax = axes[1, i]
            img = images[idx]
            if img.max() > 1:
                img = img / 255.0  # Normalize to [0, 1] if image values are [0, 255]
            ax.imshow(img)
            ax.axis('off')
            ax.set_title(f'True: {true_labels[idx]}\nPred: {predictions[idx]}')
    
    # Plot true=1 & pred=0 images
    mismatched_indices_1_0 = [
        i for i in range(len(true_labels)) 
        if true_labels[i] == 1 and predictions[i] == 0
    ]
    num_images_mismatches_1_0 = min(num_images, len(mismatched_indices_1_0))
    if num_images_mismatches_1_0 == 0:
        print("No mismatched images where true=1 and pred=0 found.")
    else:
        for i in range(num_images_mismatches_1_0):
            idx = mismatched_indices_1_0[i]
            ax = axes[2, i]
            img = images[idx]
            if img.max() > 1:
                img = img / 255.0  # Normalize to [0, 1] if image values are [0, 255]
            ax.imshow(img)
            ax.axis('off')
            ax.set_title(f'True: {true_labels[idx]}\nPred: {predictions[idx]}')
    
    plt.tight_layout()
    plt.show()

# Visualize combinations of images
visualize_combinations(images_list, true_labels, predictions, num_images=9)
