"""
Mit dem Joystick soll eine einzelne LED in die gewählte Richtung verschoben werden.
Wenn du am Rand angekommen bist soll die LED auf die LED am anderen Ende derselben Zeile oder Spalte wechseln.
Als Hilfestellung wurde bereits die Variable current_position für dich erstellt.

Zusatzaufgabe:
Wenn du auf den Joystick (mitte) klickst soll sich die LED Farbe verändern.
"""


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

current_position = 0
while True:
    np[current_position] = (color_r, color_g, color_b)
    np.write()
    sleep_ms(150)
    
    if pin_js_r.value() == 0:
        #TODO: 
        pass
    elif pin_js_l.value() == 0:
        #TODO
        pass
    elif pin_js_u.value() == 0:
        #TODO
        pass
    elif pin_js_d.value() == 0:
        #TODO
        pass
    elif pin_js_c.value() == 0:
        #TODO
        pass
