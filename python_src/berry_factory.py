# berry_factory.py
from python_src import *
from python_src.berry import Berry

berry_type = {'RGB': rgb_led.RgbLed, 'Button': button.Button,
              'Accel': accelerometer.Accelerometer,
              'Knob': knob.Knob, 'Slider': slider.Slider,
              'Pressure': pressure.Pressure,
              'Vibrerry': vibrerry.Vibrerry, 'Beeper': beeper.Beeper,
              'Servo': servo.Servo, 'Flex': flex.Flex}

berry_classes = {'Button': Berry.BerryClasses.input,
              'Accel': Berry.BerryClasses.input,
              'Knob': Berry.BerryClasses.input,
               'Slider': Berry.BerryClasses.input,
              'Pressure': Berry.BerryClasses.input,
              'Vibrerry': Berry.BerryClasses.input,
               'RGB': Berry.BerryClasses.output,
               'Beeper': Berry.BerryClasses.output,
              'Servo': Berry.BerryClasses.output,
               'Flex': Berry.BerryClasses.output}



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

def berry_class_decider (btype):
    berry_class = None
    if btype in berry_classes:
        berry_class = berry_classes[btype]
    else:
        print ("bad type string to class decider "+ btype)
    return berry_class
