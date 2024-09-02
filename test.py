import tensorflow as tf
from tensorflow import keras
from data import test

newModel = tf.keras.models.load_model('modelo_detector_caras.keras')

loss, acc = newModel.evaluate(test)

newModel.summary()