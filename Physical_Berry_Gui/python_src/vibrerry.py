# vibrerry.py
from python_src import berry_api
from python_src import berry

class Vibrerry(berry.Berry):
    # Registers
    REG_ON_OFF = 3
    REG_INTENSITY = 4

    def __init__(self, name, address, berry_type):
        super().__init__(name, address, berry_type)
        self.stop()

    # self.set_intensity(self.DEFAULT_INTENSITY)

    # The programmer inputs an intensity value in the range [0,100]; 0 = off, 100 = max intensity.
    # We map this to the range [0,255], which is the appropriate range on the berry.
    def set_intensity(self, intensity):
        if intensity < 0 or intensity > 100:
            berry_api.eprint("Error, intensity out of range for berr %s" % self.to_string())
        else:
            intensity = round(intensity * 2.55)
            err = berry_api.set_device_multi_values(self.addr, self.REG_INTENSITY, [intensity], 1)
            if err != 0:
                berry_api.eprint("Error %d in set_intensity. %s" % (err, self.to_string()))

    def run(self):
        err = berry_api.set_device_multi_values(self.addr, self.REG_ON_OFF, [1], 1)
        if err != 0:
            berry_api.eprint("Error %d in run. %s" % (err, self.to_string()))

    def stop(self):
        err = berry_api.set_device_multi_values(self.addr, self.REG_ON_OFF, [0], 1)
        if err != 0:
            berry_api.eprint("Error %d in stop. %s" % (err, self.to_string()))

    def run_at_intensity(self, intensity):
        self.set_intensity(intensity)
        self.run()
    
    def is_running(self):
        err, val = berry_api.get_device_multi_values(self.addr, self.REG_ON_OFF, 1)
        if err != 0:
            berry_api.eprint("Error %d in is_on. %s" % (err, self.to_string()))
            return False
        else:
            return val[0]

### End class Vibrerry ###
