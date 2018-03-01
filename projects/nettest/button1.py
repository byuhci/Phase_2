
def on_pressed():
    print('Pressed!')
    led1.color = [100, 100, 100]
    button1.set_status_led(1)
    pass


def on_released():
    led1.color = [0, 0, 0]
    button1.set_status_led(0)
    pass
