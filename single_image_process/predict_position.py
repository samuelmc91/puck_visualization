#!/usr/local/bin/python3.8
import os

os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'

import logging
import multiprocessing
import numpy as np
import sys
import cv2
import tensorflow as tf
from tensorflow.keras.models import load_model
from datetime import date

model_dir = '/home/samuel/Desktop/puck_visualization/bin/models/'
model_name = 'puck_visualization_model_Apr_01_2021.h5'

tf.get_logger().setLevel('ERROR')
new_model = load_model(model_dir + model_name)


def prepare_image(img_name):
    IMG_HEIGHT = 50
    IMG_WIDTH = 50
    input_image = cv2.imread(img_name)
    image_resize = cv2.resize(
        input_image, (IMG_HEIGHT, IMG_WIDTH))
    image_resize = image_resize / 255
    image_reshape = image_resize.reshape(
        (1, IMG_HEIGHT, IMG_WIDTH, 3))
    return image_reshape


def predict_image(img):
    category_names = ['Empty', 'Straight', 'Tilted']
    prediction = np.argmax(new_model.predict(
        [prepare_image(img)]), axis=-1)
    print(category_names[prediction[0]])


# for i in range(1, 17):
#     fbase = sys.argv[3].split('.')[0]
#     img = sys.argv[2] + '/' + fbase + '_' + str(i) + '.jpg'
#     print('Postion: ' + str(i))
#     predict_image(img)
#     # p1 = multiprocessing.Process(target=predict_image(img))
#     # p1.start()
# # print(p1)
