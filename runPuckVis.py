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

global today
# Check to make sure that the folder for runtime exists
if os.path.exists('/home/sclark1/Desktop/puck_visualization/bin'):
    ROOT_DIR = '/home/sclark1/Desktop/puck_visualization/bin'
else:
    raise RuntimeError('ROOT DIRECTORY NOT FOUND')

if os.path.exists('/srv1-ram/puckVis/'):
    IMAGE_DIR = '/srv1-ram/puckVis/'
else:
    raise RuntimeError('IMAGE DIRECTORY NOT FOUND')

sys.path.append(ROOT_DIR)

from pre_checks import pre_check_dewar
from take_pic import take_image, post_image
from make_dir import make_daily_dir, make_user_dir, make_inner_dir
from crop_images import crop_image

class Watcher:
    def __init__(self, value):
        self.variable = value

    def set_value(self, new_value):
        if self.variable != new_value:
            self.pre_change()
            self.variable = new_value
            self.post_change()

    def pre_change(self):

        ##### Comment/Uncomment below to set directory by user and not date #####

        todays_dir = make_daily_dir(IMAGE_DIR)

        if pre_check_dewar():
            while math.isclose(int(epics.PV('XF:17IDB-ES:AMX{Dew:1-Ax:R}Mtr.RBV').get()), int(epics.PV('XF:17IDB-ES:AMX{Dew:1-Ax:R}Mtr.VAL').get()), abs_tol=2) is False:
                print('Dewar is at: {} \nRotating to: {}'.format(int(epics.PV(
                    'XF:17IDB-ES:AMX{Dew:1-Ax:R}Mtr.RBV').get()), int(epics.PV('XF:17IDB-ES:AMX{Dew:1-Ax:R}Mtr.VAL').get())))
                time.sleep(2)
                # current_position = int(epics.PV('XF:17IDB-ES:AMX{Dew:1-Ax:R}Mtr.RBV').get())
                # position_goal = int(epics.PV('XF:17IDB-ES:AMX{Dew:1-Ax:R}Mtr.VAL').get())
                # if not math.isclose(current_position,position_goal, abs_tol = 2):
                #     print('Restarted for New Rotation')
                #     break

            inner_dir = make_inner_dir(todays_dir)
            img = take_image(todays_dir, inner_dir)

            try:
                p1 = multiprocessing.Process(
                    target=crop_image(img, inner_dir, ROOT_DIR))
                p1.start()
            except Exception as e:
                print('Prediction Failed: {}'.format(e))
            # A fifty second wait to allow conditions to change
            time.sleep(0.5)
        self.post_change()

    def post_change(self):
        # Ensure the camera is returned to its normal status
        post_image()
        check_for_change(epics.PV('XF:17IDB-ES:AMX{Dew:1-Ax:R}Mtr.VAL').get())


def check_for_change(goal):
    while True:
        time.sleep(3)
        Watcher(goal).set_value(
            epics.PV('XF:17IDB-ES:AMX{Dew:1-Ax:R}Mtr.VAL').get())
        print('Waiting for rotation')


check_for_change(epics.PV('XF:17IDB-ES:AMX{Dew:1-Ax:R}Mtr.VAL').get())
