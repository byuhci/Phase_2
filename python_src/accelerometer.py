# accelerometer.py
from python_src import berry_api
from python_src.berry import Berry
from struct import pack, unpack
from time import perf_counter
from collections import namedtuple

class Accelerometer(Berry):
    # Registers
    REG_MOVE_THRESHOLD_L = 2
    REG_MOVE_THRESHOLD_H = 3
    REG_SPIKE_THRESHOLD_L = 4
    REG_SPIKE_THRESHOLD_H = 5
    REG_ORIENT_THRESHOLD_L = 6
    REG_ORIENT_THRESHOLD_H = 7
    REG_ACCEL_X_L = 8
    REG_ACCEL_X_H = 9
    REG_ACCEL_Y_L = 10
    REG_ACCEL_Y_H = 11
    REG_ACCEL_Z_L = 12
    REG_ACCEL_Z_H = 13
    REG_GYRO_X_L = 14
    REG_GYRO_X_H = 15
    REG_GYRO_Y_L = 16
    REG_GYRO_Y_H = 17
    REG_GYRO_Z_L = 18
    REG_GYRO_Z_H = 19
    REG_MAG_X_L = 20
    REG_MAG_X_H = 21
    REG_MAG_Y_L = 22
    REG_MAG_Y_H = 23
    REG_MAG_Z_L = 24
    REG_MAG_Z_H = 25
    REG_TEMP_L = 26
    REG_TEMP_H = 27
    REG_INTR_COOLDOWN = 28
    
    # Interrupts
    MOVE_INTERRUPT = 0x01
    SPIKE_INTERRUPT = 0x02
    ORIENT_INTERRUPT = 0x04
    
    # Constants
    MIN_POLL_WAIT = 0.05  # 20 Hz, fairly arbitrary

    # Data types
    Acceleration = namedtuple('Acceleration', ['x', 'y', 'z'])
    Rotational_v = namedtuple('Rotational_v', ['x', 'y', 'z'])
    
    def __init__(self, name, address, berry_type):
        super().__init__(name, address, berry_type)
        
        self._acceleration = None
        self._rotational_v = None
        
        self.events = {
            "on_%s_movement_detected" % self.name : "on_move",
            "on_%s_impulse_detected" % self.name : "on_spike",
            "on_%s_orientation_changed" % self.name : "on_orient"
        }
    
    @property
    def acceleration(self):
        # Don't poll if recently measured
        time = perf_counter()
        if self._acceleration is None or time - self.last_acc_time > self.MIN_POLL_WAIT:

            # Get the data from the berry
            err, buf = berry_api.get_device_multi_values(
                    self.addr, self.REG_ACCEL_X_L, 6)

            # Store the result
            if err == 0:
                self._acceleration = self.Acceleration(
                        *[x/2048 for x in unpack("<hhh",bytearray(buf))])
            else:  # Report errors
                berry_api.eprint(
                        "Error %d in get_value for %s" % (err, self.to_string()))
                self._acceleration = None

            # Save access time
            self.last_acc_time = time

        # Return the new or stored value
        return self._acceleration
        
    @property
    def rotational_v(self):
        # Don't poll if recently measured
        time = perf_counter()
        if self._rotational_v is None or time - self.last_gyro_time > MIN_POLL_WAIT:
        
            # Get the data from the berry
            err, buf = berry_api.get_device_multi_values(
                    self.addr, self.REG_GYRO_X_L, 6)

            # Store the result
            if err == 0:
                self._rotational_v = Rotational_v(
                        *[2000*x/32768 for x in unpack("<hhh",bytearray(buf))])
            else:
                berry_api.eprint(
                        "Error %d in get_value for %s" % (err, self.to_string()))
                self._rotational_v = None
            
            # Save access time
            self.last_gyro_time = time
            
        # Return the new or stored value
        return self._rotational_v
    
    def on_move(self, func):
        return self.register_callback(func, self.MOVE_INTERRUPT)
    
    def on_spike(self, func):
        return self.register_callback(func, self.SPIKE_INTERRUPT)
    
    def on_orient(self, func):
        return self.register_callback(func, self.ORIENT_INTERRUPT)
    
    @property
    def movement_threshold(self):
        err, buf = berry_api.get_device_multi_values(
                self.addr, self.REG_MOVE_THRESHOLD_L, 2)
        if err == 0:
            return unpack("<h", bytearray(buf))[0]
        else:
            berry_api.eprint("Error %d in movement_threshold for %s" %
                             (err, self.to_string()))
            return 0
    
    @movement_threshold.setter
    def movement_threshold(self, threshold):
        err = berry_api.set_device_multi_values(
                self.addr, self.REG_MOVE_THRESHOLD_L, pack("<h", threshold), 2)
        if err != 0:
            berry_api.eprint("Error %d in set_movement_threshold for %s" %
                             (err, self.to_string()))
    
    @property
    def spike_threshold(self):
        err, buf = berry_api.get_device_multi_values(
                self.addr, self.REG_SPIKE_THRESHOLD_L, 2)
        if err == 0:
            return unpack("<h", bytearray(buf))[0]
        else:
            berry_api.eprint("Error %d in spike_threshold for %s" %
                             (err, self.to_string()))
            return 0
    
    @spike_threshold.setter
    def spike_threshold(self, threshold):
        err = berry_api.set_device_multi_values(
                self.addr, self.REG_SPIKE_THRESHOLD_L, pack("<h", threshold), 2)
        if err != 0:
            berry_api.eprint("Error %d in set_spike_threshold for %s" %
                             (err, self.to_string()))
    
    @property
    def orient_threshold(self):
        err, buf = berry_api.get_device_multi_values(
                self.addr, self.REG_ORIENT_THRESHOLD_L, 2)
        if err == 0:
            return unpack("<h", bytearray(buf))[0]
        else:
            berry_api.eprint("Error %d in orient_threshold for %s" %
                             (err, self.to_string()))
            return 0
    
    @orient_threshold.setter
    def orient_threshold(self, threshold):
        err = berry_api.set_device_multi_values(
                self.addr, self.REG_ORIENT_THRESHOLD_L, pack("<h", threshold), 2)
        if err != 0:
            berry_api.eprint("Error %d in set_orient_threshold for %s" %
                             (err, self.to_string()))
                             
    @property
    def orient_div(self):
        err, buf = berry_api.get_device_multi_values(
                self.addr, self.REG_ORIENT_DIV, 1)
        if err == 0:
            return buf[0]
        else:
            berry_api.eprint("Error %d in orient_div for %s" %
                             (err, self.to_string()))
            return 0
    
    @orient_div.setter
    def orient_div(self, div):
        err = berry_api.set_device_multi_values(
                self.addr, self.REG_ORIENT_DIV, [div], 1)
        if err != 0:
            berry_api.eprint("Error %d in set_orient_div for %s" %
                             (err, self.to_string()))

    @property
    def int_cooldown(self):
        err, buf = berry_api.get_device_multi_values(
                self.addr, self.INT_COOLDOWN, 1)
        if err == 0:
            return buf[0]
        else:
            berry_api.eprint("Error %d in int_cooldown for %s" %
                             (err, self.to_string()))
            return 0
    
    @int_cooldown.setter
    def int_cooldown(self, div):
        err = berry_api.set_device_multi_values(
                self.addr, self.INT_COOLDOWN, [div], 1)
        if err != 0:
            berry_api.eprint("Error %d in set_int_cooldown for %s" %
                             (err, self.to_string()))

### End class Accelerometer ###
