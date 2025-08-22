"""
JSPaint: https://jspaint.app/

"""

from time import sleep
from zhaw_led_matrix import Lumatrix

lumatrix = Lumatrix()

bitmap1 = "Blume.bmp"
bitmap2 = "bitmaps/apple.bmp"

while True:
    lumatrix.drawImage(bitmap1, 50)

    sleep(1)

    lumatrix.drawImage(bitmap2, 50)

    sleep(1)

    lumatrix.writeText("Blume schoen")
