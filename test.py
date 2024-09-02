import tensorflow as tf
from tensorflow import keras
#import WebChecker.py
from main.py import test

newModel = tf.keras.models.load_model('modelo_detector_caras.keras')

newModel.predict(test)