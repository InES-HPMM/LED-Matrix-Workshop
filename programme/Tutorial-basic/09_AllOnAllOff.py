from machine import Pin
from neopixel import NeoPixel
from time import sleep_ms

pin = Pin(19, Pin.OUT)
np = NeoPixel(pin, 64)

sleepTime = 35
brightness = 35

while True:
    for i in range(len(np)):
        # TODO
        pass
