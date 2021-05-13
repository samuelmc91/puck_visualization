#!/usr/bin/python3
import os
import cv2
import sys
import multiprocessing

from predict_position import predict_image


def crop_image(img, inner_dir, root_dir):
    # base_x and base_y are the x and y of the first position crop
    # if the camera is moved recrop position one and set the base_x and base_y to the new x and y value
    # do not change the width or height
    base_x = 425
    base_y = 442
    w = 143
    h = 141

    fname = img.split('.')[0]

    # Do not change the x and y offsets in the lists
    x = [0, 95, 252, 252, 99, -160, -114, 12,
         179, 333, 429, 429, 337, 186, 18, -112]

    y = [0, -131, -84, 78, 133, 2, -160, -274,
         -299, -231, -90, 80, 227, 295, 276, 165]

    count = 1
    img = inner_dir + '/' + img
    img = cv2.imread(img)
    file_path = inner_dir + '/' + fname + '.txt'
    prediction_file = open(file_path, 'w')
    prediction_file.write(
        '\nImage Directory: {} \nImage Name: {}\n'.format(inner_dir, fname))
    for x, y in zip(x, y):
        new_image = inner_dir + '/' + fname + '_' + str(count) + '.jpg'
        new_x = base_x + x
        new_y = base_y + y
        crop_img = img[new_y:new_y + h, new_x:new_x + w]
        cv2.imwrite(new_image, crop_img)
        prediction_file.write('\nPosition {}\n'.format(str(count)))
        prediction_file.write(predict_image(new_image, inner_dir, root_dir) + '\n')
        count += 1
