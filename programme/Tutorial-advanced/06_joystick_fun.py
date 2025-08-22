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

np[0] = (color_r, color_g, color_b)
np.write()

while True:
    sleep_ms(200)
    
    if pin_js_r.value() == 0:
        print("rechts")
        #TODO
        pass # pass ist ein Platzhalter für neuen Code. Sobald du hier einen eigenen Code geschrieben hast kannst du diese Zeile löschen.
    elif pin_js_l.value() == 0:
        print("links")
        #TODO
        pass # pass ist ein Platzhalter für neuen Code. Sobald du hier einen eigenen Code geschrieben hast kannst du diese Zeile löschen.
    elif pin_js_u.value() == 0:
        print("hoch")
        #TODO
        pass # pass ist ein Platzhalter für neuen Code. Sobald du hier einen eigenen Code geschrieben hast kannst du diese Zeile löschen.
    elif pin_js_d.value() == 0:
        print("runter")
        #TODO
        pass # pass ist ein Platzhalter für neuen Code. Sobald du hier einen eigenen Code geschrieben hast kannst du diese Zeile löschen.
    elif pin_js_c.value() == 0:
        print("mitte")
        #TODO
        pass # pass ist ein Platzhalter für neuen Code. Sobald du hier einen eigenen Code geschrieben hast kannst du diese Zeile löschen.
