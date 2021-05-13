import epics
import os
from datetime import date
import getpass
import random
import subprocess

def make_daily_dir(IMAGE_DIR):
    today = date.today().strftime('%b_%d_%Y')
    todays_dir = IMAGE_DIR + 'puckSnap_' + today
    
    if os.path.exists(IMAGE_DIR + 'puckSnap_' + today):
        pass
        # epics.PV('XF:17IDB-ES:AMX{Cam:14}JPEG1:FilePath').put(todays_dir)
    else:
        epics.PV('XF:17IDB-ES:AMX{Cam:14}JPEG1:FileNumber').put(1)
        # Joining the image path to the temporary directory for a new directory to store images
        os.system("mkdir -p " + todays_dir)
        os.system("chmod 777 " + todays_dir)
        print('Directory Created for today at: {}'.format(todays_dir))
        # Input file path to CSS
        epics.PV('XF:17IDB-ES:AMX{Cam:14}JPEG1:FilePath').put(todays_dir)

    return todays_dir

def make_user_dir(IMAGE_DIR):
    epics.PV('XF:17IDB-ES:AMX{Cam:14}JPEG1:FileNumber').put(1)
            
    # Get the username for the directory and file name
    user_name = getpass.getuser()
    tmp_dir = user_name + '_puckSnap_' + str(random.randint(11111, 99999))

    # Joining the image path to the temporary directory for a new directory to store images
    image_path = os.path.join(IMAGE_DIR, tmp_dir)
    os.system("mkdir -p " + image_path)
    os.system("chmod 777 " + image_path)

    # Input file path to CSS
    epics.PV('XF:17IDB-ES:AMX{Cam:14}JPEG1:FilePath').put(image_path)
    # Input file name to CSS
    epics.PV('XF:17IDB-ES:AMX{Cam:14}JPEG1:FileName').put(user_name)

    return tmp_dir

def make_inner_dir(todays_dir):
    user_name = getpass.getuser()
    inner_dir = user_name + '_puckSnap_' + str(random.randint(11111, 99999))
    inner_dir = os.path.join(todays_dir, inner_dir)
    os.system("mkdir -p " + inner_dir)
    os.system("chmod 777 " + inner_dir)
    print('Images are in: {}'.format(inner_dir))
    return inner_dir