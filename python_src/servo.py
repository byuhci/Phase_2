# servo.py
from python_src import berry_api
from python_src import berry

class Servo(berry.Berry):
    # Registers
    REG_POSITION = 2
    
    def __init__(self, name, address, berry_type):
        super().__init__(name, address, berry_type)
        self._position = None
    
    @property
    def position(self):
        return self.get_position()
    
    @position.setter
    def position(self, val):
        return self.set_position(val)
    
    # The position must be from 0 to 255
    def set_position(self, position):
        if position < 0 or position > 255:
            berry_api.eprint("Error in set_position; invalid position of %d. %s" % (position, self.to_string()))
            return
        err = berry_api.set_device_multi_values(self.addr, self.REG_POSITION, [position], 1)
        if err != 0:
            berry_api.eprint("Error %d in set_position. %s" % (err, self.to_string()))
            return
        self._position = position
    
    def get_position(self):
        err, vals = berry_api.get_device_multi_values(self.addr, self.REG_POSITION, 1)
        if err != 0:
            berry_api.eprint("Error %d in get_position for %s" % (err, self.to_string()))
            return None
        else:
            self._position = vals[0]
            return vals[0]

### End class Servo ###
