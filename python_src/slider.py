# slider.py
from python_src import berry_api
from python_src import berry

class Slider(berry.Berry):
    # Registers
    REG_VAL8 = 2
    REG_VAL10_LO = 3
    REG_VAL10_HI = 4
    REG_INTR_THRESHOLD = 5
    REG_INTR_DELAY = 6
    
    # Interrupts
    ON_SLIDER_MOVED = 0x1

    def __init__(self, name, address, berry_type):
        super().__init__(name, address, berry_type) # , self.get_value)
        self._value = self.get_value()
        
        # Create a dictionary of all possible event names with the associated function events
        self.events = {
            "on_%s_moved" % self.name : "on_moved"
        }
    
    @property
    def position(self):
        return self.get_value()
        # self.lock.acquire()
        # val = self._value
        # self.lock.release()
        # return val
    
    @position.setter
    def position(self, val):
        self._value = val
        # self.lock.acquire()
        # self._value = val
        # self.lock.release()
    
    @property
    def threshold(self):
        return self.get_threshold()
    
    @threshold.setter
    def threshold(self, new_threshold):
        return self.set_threshold(new_threshold)
    
    @property
    def interrupt_delay(self):
        return self.get_interrupt_delay()
    
    @interrupt_delay.setter
    def interrupt_delay(self, new_intr_delay):
        return self.set_interrupt_delay(new_intr_delay)
    
    def get_value(self):
        err, val = berry_api.get_device_multi_values(self.addr, self.REG_VAL8, 1)
        if err != 0:
            berry_api.eprint("Error %d in get_value for %s" % (err, self.to_string()))
            self.position = None
            return None
        self.position = val[0]
        return val[0]

    def on_moved(self, func):
        return self.register_callback(func, self.ON_SLIDER_MOVED)
    
    # Set the minimum position the slider must change in order to interrupt.
    # The default interrupt threshold is 8.
    # If threshold is zero, the slider will set the threshold to its default.
    def set_threshold(self, threshold):
        err = berry_api.set_device_multi_values(self.addr, self.REG_INTR_THRESHOLD, [threshold], 1)
        if err != 0:
            berry_api.eprint("Error %d in set_threshold for %s" % (err, self.to_string()))
    
    # Get the interrupt threshold
    def get_threshold(self):
        err, vals = berry_api.get_device_multi_values(self.addr, self.REG_INTR_THRESHOLD, 1)
        if err != 0:
            berry_api.eprint("Error %d in get_threshold for %s" % (err, self.to_string()))
            return None
        return vals[0]
    
    # Set the interrupt delay - the time that the slider waits after an interrupt was asserted before
    # it will assert another interrupt. The time is approximately (delay * 5.5) ms. The default delay
    # is 10; thus, approximately 55 ms between interrupts.
    # If delay is zero, the slider will set the delay to its default.
    def set_interrupt_delay(self, delay):
        err = berry_api.set_device_multi_values(self.addr, self.REG_INTR_DELAY, [delay], 1)
        if err != 0:
            berry_api.eprint("Error %d in set_interrupt_delay for %s" % (err, self.to_string()))
    
    # Get the interrupt delay
    def get_interrupt_delay(self):
        err, vals = berry_api.get_device_multi_values(self.addr, self.REG_INTR_DELAY, 1)
        if err != 0:
            berry_api.eprint("Error %d in get_threshold for %s" % (err, self.to_string()))
            return None
        return vals[0]

### End class Slider ###
