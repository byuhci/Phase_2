# test.py
from python_src import *
from python_src.berry_api import *
from python_src.berry_factory import berry_factory
import sys
from time import sleep
import random


def main(argv):
    init_host(argv)
    berry_list = get_berry_list()
    berries = [berry_factory('yo', berry[0], berry[1]) for berry in berry_list]

    btn = None
    led = None
    for berry in berries:
        print('name: {}, type: {}, guid: {}'.format(berry.name, berry.berry_type, berry.addr))
        if berry.berry_type == 'Button':
            btn = berry
        if berry.berry_type == 'RGB':
            led = berry

    try:
        v = 0
        i = 0
        while True:
            berries[i].set_status_led(v)
            i = (i + 1) % len(berries)
            v = random.randint(0, 1)
            if btn.state == 1:
                led.color = [150,150,150]
            else:
                led.color = [0,0,0]
            sleep(.01)
    except:
        print('End')


if __name__ == "__main__":
    main(sys.argv)
