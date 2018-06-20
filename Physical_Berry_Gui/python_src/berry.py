# berry.py
from python_src.berry_api import *
from python_src import eprint
import threading
from traceback import print_exc
from time import sleep
import ctypes


class Berry:
    REG_STATUS = 1


    # Default stream period is in seconds and is chosen arbitrarily
    # Rate = 1/DEFAULT_STREAM_PERIOD Hz
    DEFAULT_STREAM_PERIOD = 0.05

    # Minimum period is 10 ms; latency for a server call is at least 2 ms, so this seemed like a good number.
    MIN_STREAM_PERIOD = 0.01

    def __init__(self, name, address, berry_type, streamer_callback=None):
        self.addr = address
        self.name = name
        self.berry_type = berry_type
        # lookup the berry class.


        # ID should not be zero.
        if self.addr == 0:
            raise BerryError('Error - invalid id of 0 initializing %s.' % self.to_string())

        # Enable polling/cacheing if a callback for it is given.
        if not streamer_callback is None:
            self.streamer_period = self.DEFAULT_STREAM_PERIOD
            self.lock = threading.Lock()
            self.streamer = threading.Thread(target=self.streamer_func, args=(streamer_callback,))
            self.streamer.start()

        self.callbacks = []
        err = self.set_status_led(0)
        if err != 0:
            raise BerryError('Error %d: failed to set status LED for %s' % (err, self.to_string()))

    def print_info(self):
        eprint("%s" % self.to_string())

    def to_string(self):
        return '%s (Type: %s, guid: %d)' % (self.name, self.berry_type, self.addr)

    # Poll the berry at a rate of (1/streamer_period) Hz.
    # The berry will not be polled by setting streamer_period to zero.
    def streamer_func(self, streamer_callback):
        while (True):
            sleep(self.streamer_period) if self.streamer_period >= self.MIN_STREAM_PERIOD else sleep(
                self.MIN_STREAM_PERIOD)
            if self.streamer_period > 0:
                streamer_callback()

    # register_callback(uint64 addr, void (*callback)(void), int callback_type)
    def register_callback(self, func, cb_type):
        CB_T = ctypes.CFUNCTYPE(None)
        self.callbacks.append(CB_T(func))
        host_api.register_callback.argtypes = (ctypes.c_ulonglong, ctypes.c_void_p, ctypes.c_int)
        err = host_api.register_callback(self.addr, self.callbacks[-1], cb_type)
        if err != 0:
            raise BerryError("Error %d registering a callback for %s\n" % (err, self.to_string()))
        return err

    def set_status_led(self, val):
        return set_device_multi_values(self.addr, self.REG_STATUS, [val], 1)

# End class Berry ###
