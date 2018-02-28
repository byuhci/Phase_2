# pressure.py
from python_src import berry_api
from python_src import berry

class Pressure(berry.Berry):
    # Registers
    REG_VAL8 = 2  # 8-bit ADC value
    REG_LEVEL = 3  # level
    REG_VAL10_LO = 4  # 10-bit ADC value, first 8 bits
    REG_VAL10_HI = 5  # 10-bit ADC value, last 2 bits (high 6 bits are 0)

    # Interrupts
    ON_REACH_LEVEL1 = 0x01
    ON_REACH_LEVEL2 = 0x02
    ON_REACH_LEVEL3 = 0x04
    ON_REACH_LEVEL4 = 0x08
    ON_LEVEL_CHANGE = 0x10
    ON_RELEASED = 0x20

    def __init__(self, name, address, berry_type):
        super().__init__(name, address, berry_type) #, self.get_value_and_level)
        self._value = self.get_value()
        self._level = self.get_pressure_level()
        
        # Create a dictionary of all possible event names with the associated function events
        self.events = {
            "on_%s_light_press" % self.name : "on_light_press",
            "on_%s_medium_press" % self.name : "on_medium_press",
            "on_%s_hard_press" % self.name : "on_hard_press",
            "on_%s_hardest_press" % self.name : "on_hardest_press",
            "on_%s_level_change" % self.name : "on_level_change",
            "on_%s_straight" % self.name : "on_straight"
        }
    
    @property
    def value(self):
        return self.get_value()
        # self.lock.acquire()
        # val = self._value
        # self.lock.release()
        # return val
    
    @value.setter
    def value(self, val):
        # self.lock.acquire()
        self._value = val
        # self.lock.release()
    
    @property
    def level(self):
        return self.get_pressure_level()
        # self.lock.acquire()
        # val = self._level
        # self.lock.release()
        # return val
    
    @level.setter
    def level(self, val):
        # self.lock.acquire()
        self._level= val
        # self.lock.release()
    
    # The current pressure level from ranges from [0,4], where 0 means no press and 4 is the heaviest press
    def get_pressure_level(self):
        err, val = berry_api.get_device_multi_values(self.addr, self.REG_LEVEL, 1)
        if err != 0:
            berry_api.eprint("Error %d in get_value for %s" % (err, self.to_string()))
            self.level = None
            return None
        self.level = val[0]
        return val[0]

    # Use this only if you really want to see the 8-bit ADC value
    def get_value(self):
        err, val = berry_api.get_device_multi_values(self.addr, self.REG_VAL8, 1)
        if err != 0:
            berry_api.eprint("Error %d in get_value for %s" % (err, self.to_string()))
            self.value = None
            return None
        self.value = val[0]
        return val[0]

    # Get the value and the level in a single call - use this if you want them to be in sync.
    def get_value_and_level(self):
        err, vals = berry_api.get_device_multi_values(self.addr, self.REG_VAL8, 2)
        if err != 0:
            berry_api.eprint("Error %d in get_value for %s" % (err, self.to_string()))
            self.value = None
            self.level = None
            return None
        self.value = vals[0]
        self.level = vals[1]
        return (vals[0], vals[1])

    # Enable different callbacks with the following methods:

    def on_light_press(self, func):
        return self.register_callback(func, self.ON_REACH_LEVEL1)

    def on_medium_press(self, func):
        return self.register_callback(func, self.ON_REACH_LEVEL2)

    def on_hard_press(self, func):
        return self.register_callback(func, self.ON_REACH_LEVEL3)

    def on_hardest_press(self, func):
        return self.register_callback(func, self.ON_REACH_LEVEL4)

    def on_level_change(self, func):
        return self.register_callback(func, self.ON_LEVEL_CHANGE)

    def on_released(self, func):
        return self.register_callback(func, self.ON_RELEASED)

### End class Pressure ###
