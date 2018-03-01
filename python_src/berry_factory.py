# berry_factory.py
from python_src import *

berry_type = {'RGB': rgb_led.RgbLed, 'Button': button.Button,
              'Accel': accelerometer.Accelerometer,
              'Knob': knob.Knob, 'Slider': slider.Slider,
              'Pressure': pressure.Pressure,
              'Vibrerry': vibrerry.Vibrerry, 'Beeper': beeper.Beeper,
              'Servo': servo.Servo, 'Flex': flex.Flex}


# berry_type = {'RGB':RgbLed,'Button':Button,
#             'Accel':Accelerometer,
#             'Knob':Knob,'Slider':Slider,
#             'Pressure':Pressure,
#             'Vibrerry':Vibrerry,'Beeper':Beeper,
#             'Servo':Servo,'Flex':Flex}

def berry_factory(name, guid, btype):
    berry_inst = None
    if btype in berry_type:
        berry_inst = berry_type[btype](name, guid, btype)
    else:
        print("Bad type string: " + btype)
    return berry_inst
