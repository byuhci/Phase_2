# Python initialization file
import os
import ctypes
import sys

__all__ = ['berry_api', 'berry', 'accelerometer', 'beeper', 'button',
           'flex', 'knob', 'pressure', 'rgb_led', 'servo', 'slider', 'vibrerry']

# Load the DLL
dir_name = os.path.dirname(__file__)
file_dir = os.path.abspath(os.path.join(dir_name, "..\\bin"))
file = os.path.abspath(os.path.join(dir_name, "..\\bin\\lib_berry_host.dll"))
os.environ["PATH"] = file_dir + ';' + os.environ["PATH"]
host_api = ctypes.cdll.LoadLibrary(file)


def eprint(*args, **kwargs):
    kwargs["file"] = sys.stderr
    kwargs["flush"] = True
    print(*args, **kwargs)
