import epics
import getpass

def pre_check_dewar():
    position_goal = int(epics.PV('XF:17IDB-ES:AMX{Dew:1-Ax:R}Mtr.VAL').get())
    puck_check = False
    fill_check = False
    fill_level = epics.PV('XF:17IDB-ES:AMX{CS8}Ln2Level-I').get()
    user_name = getpass.getuser()
    
    plates = dict([(1, 180),
                (2, 135),
                (3, 90),
                (4, 45),
                (5, 0),
                (6, 315),
                (7, 270),
                (8, 225)])

    degrees_high_check = position_goal + 135
    degrees_low_check = position_goal - 225

    plate = next(plate for plate, degree in plates.items() if degree == degrees_high_check or degree == degrees_low_check)

    if epics.PV('XF:17IDB-ES:AMX{Wago:1}Puck' + str(plate) + 'C-Sts').get() != 1:
            print('There is no puck on position: {}. No image taken'.format(plate))
    else:
        puck_check = True

    if fill_level >= 85:
            fill_check = True
    else:
        print('Fill Violation, Fill Level Is: ' + str('%.2f' % fill_level))
        print('Please Fill Dewar to Continue')

    if fill_check and puck_check:
        return True
    else:
        return False