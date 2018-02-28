# button.py
from python_src import berry_api
from python_src import berry

class Button(berry.Berry):
    # Registers
    REG_SWITCH = 2
    
    # Interrupts
    ON_BUTTON_PRESSED = 0x1
    ON_BUTTON_RELEASED = 0x2

    def __init__(self, name, address, berry_type):
        super().__init__(name, address, berry_type) # , self.get_value)
        self._value = self.get_value()
        
        # Create a dictionary of all possible event names with the associated function events
        self.events = {
            "on_%s_pressed" % self.name : "on_pressed",
            "on_%s_released" % self.name : "on_released"
        }
    
    @property
    def state(self):
        return self.get_value()
    
    def get_value(self):
        err, val = berry_api.get_device_multi_values(self.addr, self.REG_SWITCH, 1)
        if err != 0:
            berry_api.eprint("Error %d in get_value. %s" % (err, self.to_string()))
            self._value = None
        else:
            self._value = val[0]
            return val[0]

    def on_pressed(self, func):
        # Register callback function
        return self.register_callback(func, self.ON_BUTTON_PRESSED)

    def on_released(self, func):
        # Register callback function
        return self.register_callback(func, self.ON_BUTTON_RELEASED)

### End class Button ###
