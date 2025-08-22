from machine import Pin
from neopixel import NeoPixel
from utime import sleep_ms

# GPIO-Pin für WS2812
pin_num_leds = 19

# GPIO-Pin für Switch
pin_num_switch = 9

# Anzahl der LEDs
anzahl_leds = 64

pin_leds = Pin(pin_num_leds, Pin.OUT)
np = NeoPixel(pin_leds, anzahl_leds)
pin_switch = Pin(pin_num_switch, Pin.IN)

value = pin_switch.value()
while True:
    currentValue = pin_switch.value()
    if currentValue != value:
        value = currentValue
        print(value)
        if value == 1:
            np[0] = (50, 50, 50)
        else:
            np[0] = (0, 0, 0)
        np.write()
    sleep_ms(100)