# berry_api.py
from python_src import host_api
# from python_src.berry import BerryError
import ctypes


class BerryError(Exception):
    """ Class used for raising exceptions due to errors initializing or communicating with berries."""

    def __init__(self, message):
        self.message = message


### HOST API ###################################################################

# init_host:
# parameters:
#   argv - command line arguments;
def init_host(argv):
    # Cast argv to a char** to pass into init_all
    arr = (ctypes.c_char_p * len(argv))
    args = arr()
    for i in range(len(argv)):
        args[i] = bytes(argv[i], encoding='UTF-8')

    # Initialize berries
    err = host_api.init_host(len(argv), args, 0)
    if err != 0:
        raise BerryError("Error %d initializing berries." % err)


# get_device_multi_values: uint64 addr, int reg, char *buf, int count
# return an error code (0 for success, nonzero for error) and a list of requested values
host_api.get_device_multi_values.argtypes = (ctypes.c_ulonglong, ctypes.c_int, ctypes.c_void_p, ctypes.c_int)


def get_device_multi_values(addr, reg, count):
    buf = (ctypes.c_ubyte * count)()
    buf_p = ctypes.c_void_p(ctypes.addressof(buf))
    err = host_api.get_device_multi_values(addr, reg, buf_p, count)
    buf_list = [buf[i] for i in range(len(buf))]
    return err, buf_list


# set_device_multi_values: uint64 addr, int reg, char *vals, int count
# return an error code (0 for success, nonzero for error)
host_api.set_device_multi_values.argtypes = (ctypes.c_ulonglong, ctypes.c_int, ctypes.c_void_p, ctypes.c_int)


def set_device_multi_values(addr, reg, vals, count):
    buf = (ctypes.c_ubyte * count)(*vals)
    buf_p = ctypes.c_void_p(ctypes.addressof(buf))
    err = host_api.set_device_multi_values(addr, reg, buf_p, count)
    return err


class BerryInfo(ctypes.Structure):
    _fields_ = [("guid", ctypes.c_ulonglong), ("type", ctypes.c_char_p)]


def get_berry_list():
    count = host_api.get_berry_count()
    arr = (BerryInfo * count)()

    host_api.get_berry_list(ctypes.byref(arr), count)
    berry_list = []
    for b in arr:
        btype = b.type.decode()
        print(btype)
        # berry_list.append(berry_factory('yo',b.guid,btype))
        berry_list.append((b.guid, btype))
    return berry_list

### End Host API ###
