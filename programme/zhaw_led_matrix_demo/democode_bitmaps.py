from utime import sleep
from zhaw_led_matrix import LedMatrix

lm = LedMatrix(8, 8)

# Der Ordner bitmaps muss auf den RaspberryPi Pico kopiert werden
# um diese Demo laufen lassen zu koennen!
bitmap1 = "/bitmaps/wine.bmp"
bitmap2 = "/bitmaps/bird.bmp"

while True:
    lm.draw_bitmap(bitmap1)
    lm.set_brightness(20)
    lm.apply()

    sleep(1)

    lm.draw_bitmap(bitmap2)
    lm.set_brightness(20)
    lm.apply()

    sleep(1)
