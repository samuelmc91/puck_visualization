#!/usr/bin/python3
import time
import epics
import getpass
import os
import random
from datetime import date
import multiprocessing
import sys
import math

# Used only for collecting data and ignores all processing done

if os.path.exists('/home/sclark1/Desktop/puck_visualization/bin'):
    ROOT_DIR = '/home/sclark1/Desktop/puck_visualization/bin'
else:
    raise RuntimeError('ROOT DIRECTORY NOT FOUND')

sys.path.append(ROOT_DIR)

from pre_checks import pre_check_dewar
from take_pic import take_picture, post_image

image_path = os.path.join(os.getcwd(), 'Images')

position_goal = epics.PV('XF:17IDB-ES:AMX{Dew:1-Ax:R}Mtr.VAL').get()


class plate_check:
    def __init__(self, plate, degree):
        self.plate = plate
        self.degree = degree


class Watcher:
    def __init__(self, value):
        self.variable = value

    def set_value(self, new_value):
        if self.variable != new_value:
            self.pre_change()
            self.variable = new_value
            self.post_change()

    def pre_change(self):
        if pre_check_dewar():
            # A one minute buffer to allow the dewar to rotate
            while math.isclose(int(epics.PV('XF:17IDB-ES:AMX{Dew:1-Ax:R}Mtr.RBV').get()), int(epics.PV('XF:17IDB-ES:AMX{Dew:1-Ax:R}Mtr.VAL').get()), abs_tol=2) is False:
                print('Dewar is at: {} \nRotating to: {}'.format(int(epics.PV(
                    'XF:17IDB-ES:AMX{Dew:1-Ax:R}Mtr.RBV').get()), int(epics.PV('XF:17IDB-ES:AMX{Dew:1-Ax:R}Mtr.VAL').get())))
                time.sleep(2)

            epics.PV('XF:17IDB-ES:AMX{Cam:14}JPEG1:FilePath').put(image_path)
            epics.PV('XF:17IDB-ES:AMX{Cam:14}Proc1:EnableFilter').put(1)
            user_name = getpass.getuser()
            epics.PV('XF:17IDB-ES:AMX{Cam:14}JPEG1:FileName').put(user_name)

            take_picture()

            print('Images are in: {}'.format(image_path))
            epics.PV('XF:17IDB-ES:AMX{Cam:14}Proc1:EnableFilter').put(1)
            for i in range(1, 4):
                print('Taking image: ' + str(i) + ' of 3')
                
        self.post_change()

    def post_change(self):
        # Ensure the camera is returned to its normal status
        post_image()
        epics.PV('XF:17IDB-ES:AMX{Cam:14}Proc1:EnableFilter').put(0)
        check_for_change(epics.PV('XF:17IDB-ES:AMX{Dew:1-Ax:R}Mtr.VAL').get())


def check_for_change(goal):
    while True:
        time.sleep(10)
        Watcher(goal).set_value(
            epics.PV('XF:17IDB-ES:AMX{Dew:1-Ax:R}Mtr.VAL').get())
        print('Waiting for rotation')


check_for_change(position_goal)
