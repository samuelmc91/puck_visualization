#!/usr/local/bin/python3.8
import os
import sys
import getpass
import random
import shutil

if os.path.exists('/home/samuel/Desktop/puck_visualization/single_image_process'):
    root_dir = '/home/samuel/Desktop/puck_visualization/single_image_process'
else:
    raise RuntimeError('ROOT DIRECTORY DOES NOT EXIST')

sys.path.insert(0, root_dir)
from crop_images import crop_image
from predict_position import predict_image

user = getpass.getuser()

tmp_dir = os.getcwd() + '/' + user + '_puck_visualization_' + str(random.randint(11111, 99999))
os.mkdir(tmp_dir)

shutil.copy(sys.argv[1], tmp_dir)

img = sys.argv[1]
tmp_fname = os.listdir(tmp_dir)[0]
fname = tmp_fname.split('.')[0]
fbase = fname + '_position'

os.remove(tmp_dir + '/' + tmp_fname)

print('Processing Image: {}'.format(fname))
print('Files in: {}'.format(tmp_dir))


crop_image(img, fbase, tmp_dir)

files = sorted([f for f in os.listdir(tmp_dir)])
position_number = 1
for my_file in files:
    filepath = tmp_dir + '/' + my_file
    print('Predicting Image: {}'.format(my_file))
    predict_image(filepath)