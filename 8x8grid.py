import os, glob

NOHAT =       'No HAT\x00'
SENSEHATFB =  'RPi-Sense FB'
SENSEHAT =    'Sense HAT\x00'
UNICORNHAT =  'Unicorn HAT\x00'
UNICORNPHAT = 'Unicorn pHAT\x00'

# Return Boolean
def answeryes(question = '(y/n): '):
    answer = input(question)
    return (answer == 'y' or answer == 'Y')

# Return a String
def GetNameHAT():
    if os.path.isfile('/proc/device-tree/hat/product'):
        file = open('/proc/device-tree/hat/product','r')
        hat = file.readline()
        file.close()
        return hat
    
    # Try to find Sense HAT Frame Buffer name
    # Fragment extracted from the sense_hat library
    for fb in glob.glob('/sys/class/graphics/fb*'):
        name_file = os.path.join(fb, 'name')
        if os.path.isfile(name_file):
            with open(name_file, 'r') as f:
                name = f.read()
            if name.strip() == SENSEHATFB:
                fb_device = fb.replace(os.path.dirname(fb), '/dev')
                if os.path.exists(fb_device):
                    return SENSEHATFB
                    
    return NOHAT

# **************** main ******************
mypath = "/usr/bin/env python3 " + os.path.dirname(os.path.abspath(__file__))
namehat = GetNameHAT()

if  namehat == SENSEHAT or namehat == SENSEHATFB:
    print('Sense HAT auto detected')
    os.system(mypath + '/8x8grid-sense.py')
elif namehat == UNICORNHAT:
    print('Unicorn pHAT auto detected')
    os.system(mypath + "/8x8grid-unicorn.py")
elif namehat == NOHAT:
    print('No HAT detected.')
    if answeryes('Do you have a Unicorn pHAT (y/n)? '):
        print('Configuring Unicorn pHAT')
        os.system(mypath + "/8x8grid-unicornphat.py")
    elif answeryes('Do you have a Sense HAT (y/n)? '):
        print('Configuring Sense HAT')
        os.system(mypath + "/8x8grid-sense.py")
else:
    print("WARNING !!! Unknown HAT : " + namehat)