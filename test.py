import tensorflow as tf
import numpy as np
from matplotlib import pyplot as plt
from tensorflow import keras
import pandas as pd
from data import test
import matplotlib.pyplot as plt
import os


newModel = tf.keras.models.load_model('my_model.keras')

X_test = []
y_true = []

for images, labels in test:
    X_test.append(images.numpy())
    y_true.append(labels.numpy())

X_test = np.concatenate(X_test, axis=0)
y_true = np.concatenate(y_true, axis=0)

y_pred = newModel.predict(X_test)

def visualize_predictions(X, y_true, y_pred, max_images=20):
    correct_indices = np.where(y_true == y_pred)[0]
    incorrect_indices = np.where(y_true != y_pred)[0]
    false_negative_indices = np.where((y_true == 0) & (y_pred == 1))[0]
    
    num_correct = min(len(correct_indices), 10)
    num_incorrect = min(len(incorrect_indices), 10)
    num_false_negatives = min(len(false_negative_indices), 10)
    
    selected_correct_indices = correct_indices[:num_correct]
    selected_incorrect_indices = incorrect_indices[:num_incorrect]
    selected_false_negative_indices = false_negative_indices[:num_false_negatives]
    
    selected_indices = np.concatenate([selected_correct_indices, selected_incorrect_indices]) #selected_false_negative_indices
    
    fig, axes = plt.subplots(2, 10, figsize=(20, 10)) #Change to 3 to show false negatives
    for i, ax in enumerate(axes.ravel()):
        if i < len(selected_indices):
            ax.imshow(X[selected_indices[i]].astype('uint8'))
            ax.set_title(f"True: {y_true[selected_indices[i]]}\nPred: {y_pred[selected_indices[i]]}")
            ax.axis('off')
        else:
            ax.axis('off')
    plt.tight_layout()
    plt.show()

# Example usage
visualize_predictions(X_test, y_true, y_pred.argmax(axis=1))
