from machine import Pin
from neopixel import NeoPixel
from utime import sleep_ms

pin = Pin(19, Pin.OUT)
np = NeoPixel(pin, 64)

pin_js_r = Pin(2, Pin.IN) #rechts
pin_js_l = Pin(7, Pin.IN) #links
pin_js_u = Pin(3, Pin.IN) #hoch
pin_js_d = Pin(6, Pin.IN) #runter
pin_js_c = Pin(8, Pin.IN) #mitte

color_r = 50 # Rot
color_g = 50 # Gruen
color_b = 50 # Blau
color_h = 0  # Puffer

currentPosition = 0
while True:
    np[currentPosition] = (color_r, color_g, color_b)
    np.write()
    sleep_ms(200)
    
    if pin_js_r.value() == 0:
        if (currentPosition + 1) % 8 != 0:
            np[currentPosition] = (0, 0, 0)
            currentPosition += 1
    elif pin_js_l.value() == 0:
        if currentPosition % 8 != 0:
            np[currentPosition] = (0, 0, 0)
            currentPosition -= 1
    elif pin_js_u.value() == 0:
        if currentPosition <= 55:
            np[currentPosition] = (0, 0, 0)
            currentPosition += 8
    elif pin_js_d.value() == 0:
        if currentPosition >= 8:
            np[currentPosition] = (0, 0, 0)
            currentPosition -= 8
    elif pin_js_c.value() == 0:
        print("Joystick pressed - color change")
        color_r = color_g
        color_g = color_b
        color_b = color_h
        color_h = color_r
