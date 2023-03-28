# Load Libraries
from machine import Pin
from neopixel import NeoPixel
from utime import sleep_ms

from ledmatrix import *
from characters import *
from button import *

# Experimental Module: Used to implement moving Text and other advanced functions

"""
Two buffers needed:
    - One with the first letter
    - Second with the next letter which is "pushed in" from left
As soon as the first buffer is pushed away fully, it is reused for the third letter
and so on. 

"""

# class MovingText():

WCL = LedMatrix(8, 8)  # Create a Matrix object called WCL wich 8 rows & cols
CL = ColorTable()  # ColorTable object
CT = CharacterTable()  # CharacterTable object


def moving_letters(text):
    print(text)
    brightness = 40
    sleep = 1000

    WCL.clear()
    WCL.draw_list(CT.h, CL.BLUE)
    WCL.set_brightness(brightness)
    WCL.apply()
    sleep_ms(sleep)

    WCL.clear()
    WCL.draw_list(CT.i, CL.BLUE)
    WCL.set_brightness(brightness)
    WCL.apply()
    sleep_ms(sleep)


moving_letters("hi")
