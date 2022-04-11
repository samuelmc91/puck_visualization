#!/usr/bin/python3
from tensorflow.keras.models import load_model
import tensorflow as tf
import cv2
import sys
import os
import numpy as np
import multiprocessing
import shutil

os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'

# Prepare Image = formats the input image into the expected format
def prepare_image(img_name):
    IMG_HEIGHT = 150
    IMG_WIDTH = 150
    input_image = cv2.imread(img_name)
    image_resize = cv2.resize(
        input_image, (IMG_HEIGHT, IMG_WIDTH))
    image_resize = image_resize / 255
    image_reshape = image_resize.reshape(
        (1, IMG_HEIGHT, IMG_WIDTH, 3))
    return image_reshape


def predict_image(new_image, inner_dir, root_dir):
    tf.get_logger().setLevel('ERROR')
    category_names = ['Empty', 'Straight', 'Tilted']
    model_dir = os.path.join(root_dir, 'models')
    model_name = 'puck_visualization_model_Apr_26_2021.h5'
    model = os.path.join(model_dir,model_name)
    dir_name = {}
    for category_name in category_names:
        new_dir = os.path.join(inner_dir, category_name)
        os.system('mkdir -p ' + new_dir)
        dir_name[category_name] = new_dir

    print('Model Used: {}'.format(model))
    print('Predicting image: {}'.format(new_image))
    new_model = load_model(model)
    prediction = np.argmax(new_model.predict(
        [prepare_image(new_image)]), axis=-1)
    if category_names[prediction[0]] == 'Straight':
        shutil.move(new_image, dir_name['Straight'])
    elif category_names[prediction[0]] == 'Tilted':
        shutil.move(new_image, dir_name['Tilted'])
    elif category_names[prediction[0]] == 'Empty':
        shutil.move(new_image, dir_name['Empty'])
    else:
        print('Prediction Error')
    return category_names[prediction[0]]


