import epics
import time
import subprocess
import getpass
import os
from datetime import date
import shutil

acq = epics.PV('XF:17IDB-ES:AMX{Cam:14}cam1:Acquire')
img_mode = epics.PV('XF:17IDB-ES:AMX{Cam:14}cam1:ImageMode')
data_type = epics.PV('XF:17IDB-ES:AMX{Cam:14}cam1:DataType')
save_file = epics.PV('XF:17IDB-ES:AMX{Cam:14}JPEG1:WriteFile')


def take_picture():
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
    epics.PV('XF:17IDB-ES:AMX{Cam:14}JPEG1:FilePath').put(inner_dir)

    user_name = getpass.getuser()
    epics.PV('XF:17IDB-ES:AMX{Cam:14}JPEG1:FileName').put(user_name)

    epics.PV('XF:17IDB-ES:AMX{Cam:14}Proc1:EnableFilter').put(1)

    print('Taking image')

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
    epics.PV('XF:17IDB-ES:AMX{Cam:14}Proc1:EnableFilter').put(1)

    img = epics.caget('XF:17IDB-ES:AMX{Cam:14}JPEG1:FileName', as_string=True) + '_' + \
        str(epics.PV(
            'XF:17IDB-ES:AMX{Cam:14}JPEG1:FileNumber').get() - 1).zfill(3) + '.jpg'

    return img


def transfer_image(img, inner_dir):
    pass


def post_image():
    time.sleep(0.5)
    img_mode.put(2)
    data_type.put(1)
    acq.put(1)
    epics.PV('XF:17IDB-ES:AMX{Cam:14}Proc1:EnableFilter').put(0)


if __name__ == "main":
    take_picture()
