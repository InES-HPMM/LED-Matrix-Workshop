from machine import Pin
from neopixel import NeoPixel
from utime import sleep_ms

# GPIO-Pin für WS2812
pin_leds = 19

# Anzahl der LEDs
anzahl_leds = 64

pin = Pin(pin_leds, Pin.OUT)
np = NeoPixel(pin, anzahl_leds)

np[0] = (0, 0, 25) # MAX: 255
np.write()

sleep_ms(2000)
np[0] = (0, 0, 0)
np.write()
