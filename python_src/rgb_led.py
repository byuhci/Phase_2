# rgb_led.py
from python_src import berry_api
from python_src import berry
from copy import deepcopy


class RgbLed(berry.Berry):
    # Registers
    REG_RED = 2
    REG_GREEN = 3
    REG_BLUE = 4
    
    # Some predefined colors. Use these with the set_color method.
    RED = [255, 0, 0]
    ORANGE = [255, 160, 0]
    YELLOW = [255, 255, 0]
    GREEN = [0, 255, 0]
    BLUE = [0, 0, 255]
    PURPLE = [255, 0, 255]
    WHITE = [255, 255, 255]
    BLACK = [0, 0, 0]
    
    def __init__(self, name, address, berry_type):
        super().__init__(name, address, berry_type)
        self._color = self.read_colors()
    
    @property
    def color(self):
        return self.read_colors()
    
    @color.setter
    def color(self, vals):
        self.set_color(vals)
    
    @property
    def red(self):
        return self._color[0]
    
    @property
    def green(self):
        return self._color[1]
    
    @property
    def blue(self):
        return self._color[2]
    
    # vals = a list of red, green, and blue colors from 0 to 255 (i.e. [red, green, blue])
    def set_color(self, vals):
        err = berry_api.set_device_multi_values(self.addr, self.REG_RED, vals, 3)
        if err != 0:
            berry_api.eprint("Error ", err, "in write_rgb_colors, rgb = ")
            self.print_info()
            self._color = [None,None,None]
        else:
            self._color = deepcopy(vals)

    def read_colors(self):
        err, vals = berry_api.get_device_multi_values(self.addr, self.REG_RED, 3)
        if err != 0:
            berry_api.eprint("Error ", err, " in read_rgb_colors, rgb = ")
            self.print_info()
            self._color = [None,None,None]
            return [None,None,None]
        else:
            self._color = deepcopy(vals)
            return self._color

### End class RgbLed ###
