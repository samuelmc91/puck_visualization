import epics
import time
import subprocess
import getpass
import os
from datetime import date
import shutil

# Getting the handles for CSS 
acq = epics.PV('XF:17IDB-ES:AMX{Cam:14}cam1:Acquire')
img_mode = epics.PV('XF:17IDB-ES:AMX{Cam:14}cam1:ImageMode')
data_type = epics.PV('XF:17IDB-ES:AMX{Cam:14}cam1:DataType')
save_file = epics.PV('XF:17IDB-ES:AMX{Cam:14}JPEG1:WriteFile')

# Method to take an image
def take_picture():

    # Change the settings to take the picture and capture the image
    acq.put(0)
    img_mode.put(0)
    data_type.put(0)
    time.sleep(0.5)
    acq.put(1)
    time.sleep(0.5)
    save_file.put(1)

    # Put the camera back to the original settings
    time.sleep(0.5)
    img_mode.put(2)
    data_type.put(1)
    acq.put(1)

def take_image(todays_dir, inner_dir):
    today = date.today().strftime('%b_%d_%Y')
    inner_dir = os.path.join(todays_dir, inner_dir)

    # Entering the new directory into CSS
    epics.PV('XF:17IDB-ES:AMX{Cam:14}JPEG1:FilePath').put(inner_dir)

    # Entering the new image name into CSS
    user_name = getpass.getuser()
    epics.PV('XF:17IDB-ES:AMX{Cam:14}JPEG1:FileName').put(user_name)

    # Turing the mult-image filter on
    epics.PV('XF:17IDB-ES:AMX{Cam:14}Proc1:EnableFilter').put(1)

    print('Taking image')

    take_picture()

    # Getting the image information to pass to the calling function
    img = epics.caget('XF:17IDB-ES:AMX{Cam:14}JPEG1:FileName', as_string=True) + '_' + \
        str(epics.PV(
            'XF:17IDB-ES:AMX{Cam:14}JPEG1:FileNumber').get() - 1).zfill(3) + '.jpg'

    return img

# Resetting the camera
def post_image():
    time.sleep(0.5)
    img_mode.put(2)
    data_type.put(1)
    acq.put(1)
    epics.PV('XF:17IDB-ES:AMX{Cam:14}Proc1:EnableFilter').put(0)

if __name__ == "main":
    take_picture()
