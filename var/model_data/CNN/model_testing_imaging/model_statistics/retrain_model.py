import tensorflow as tf
from tensorflow.keras.models import Sequential
import os
from datetime import date
import sys

sys.path.insert(1, '/home/samuel/Desktop/Classes/CSC_300/puck_visualization_system/puck_visualization_program/bin/')

from puck_visualization_tensorflow import prepare_image

model_dict = '/home/samuel/Desktop/Classes/CSC_300/puck_visualization_system/puck_visualization_program/models/'
model_name = 'puck_visualization_model_' + date.today().strftime('%b_%d_%Y')
my_model = os.path.join(model_dict, 'puck_visualization_model_Apr_01_2021.h5')

model = tf.keras.models.load_model(my_model)