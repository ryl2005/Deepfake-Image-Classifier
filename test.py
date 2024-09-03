import tensorflow as tf
import numpy as np
from matplotlib import pyplot as plt
from tensorflow import keras
import pandas as pd
from data import test

newModel = tf.keras.models.load_model('my_model.keras')


import os
import numpy as np

X_test = []
y_true = []

for images, labels in test:
    X_test.append(images.numpy())
    y_true.append(labels.numpy())

X_test = np.concatenate(X_test, axis=0)
y_true = np.concatenate(y_true, axis=0)

y_pred = newModel.predict(X_test)
incorrect_indices = np.where(y_true != y_pred.argmax(axis=1))[0]

X_incorrect = X_test[incorrect_indices]
y_true_incorrect = y_true[incorrect_indices]
y_pred_incorrect = y_pred[incorrect_indices].argmax(axis=1)

import matplotlib.pyplot as plt
import numpy as np

def visualize_predictions(X, y_true, y_pred):
    correct_indices = np.where(y_true == y_pred)[0]
    incorrect_indices = np.where(y_true != y_pred)[0]
    
    num_correct = min(len(correct_indices), 5)  # Show up to 5 correct predictions
    num_incorrect = min(len(incorrect_indices), 5)  # Show up to 5 incorrect predictions
    
    selected_correct_indices = correct_indices[:num_correct]
    selected_incorrect_indices = incorrect_indices[:num_incorrect]
    
    selected_indices = np.concatenate([selected_correct_indices, selected_incorrect_indices])
    
    fig, axes = plt.subplots(2, 5, figsize=(15, 6))
    for i, ax in enumerate(axes.ravel()):
        ax.imshow(X[selected_indices[i]].astype('uint8'))
        ax.set_title(f"True: {y_true[selected_indices[i]]}\nPred: {y_pred[selected_indices[i]]}")
        ax.axis('off')
    plt.tight_layout()
    plt.show()

# Example usage
visualize_predictions(X_test, y_true, y_pred.argmax(axis=1)) # 0 is for fake and 1 is for real

# def visualize_predictions(X, y_true, y_pred):
#     fig, axes = plt.subplots(2, 5, figsize=(15, 6))
#     for i, ax in enumerate(axes.ravel()):
#         ax.imshow(X[i].astype('uint8'))  # No reshaping; handle color images correctly
#         ax.set_title(f"True: {y_true[i]}\nPred: {y_pred[i]}")
#         ax.axis('off')
#     plt.tight_layout()
#     plt.show()


# visualize_predictions(X_incorrect, y_true_incorrect, y_pred_incorrect)

# correct_indicies = np.where(y_true == y_pred.argmax(axis=1))[0]
# X_correct = X_test[correct_indicies]
# y_true_correct = y_true[correct_indicies]
# y_pred_correct = y_pred[correct_indicies].argmax(axis=1)

# visualize_predictions(X_correct, y_true_correct, y_pred_correct)


