import tensorflow as tf
import numpy as np
from matplotlib import pyplot as plt
from tensorflow import keras
import pandas as pd
from data import test

newModel = tf.keras.models.load_model('my_model.keras')

newModel.evaluate(test)