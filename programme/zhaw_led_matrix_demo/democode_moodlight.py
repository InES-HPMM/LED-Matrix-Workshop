from utime import sleep_ms
from zhaw_led_matrix import (
    LedMatrix,
    PixelColor,
)

matrix = LedMatrix(8, 8)

while True:
    val = 5  # Decides how fast colors are changed. Use 1 for slower change.
    brightness = 40  # Brightness is 40%. All LEDs on 100% use a lot of current!
    r = 255  # Initial Red value: 255
    g = 0  # Initial Green value: 0
    b = 0  # Initial Blue value:  0
    matrix.set_brightness(brightness)

    # Increment green value from 0 to 255
    while g < 255:
        matrix.fill(PixelColor(r, g, b))
        matrix.apply()
        g += val

    # Decrement red value from 255 to 0
    while r > 0:
        matrix.fill(PixelColor(r, g, b))
        matrix.apply()
        r -= val

    # Increment blue value from 0 to 255
    while b < 255:
        matrix.fill(PixelColor(r, g, b))
        matrix.apply()
        b += val

    # Decrement green value from 255 to 0
    while g > 0:
        matrix.fill(PixelColor(r, g, b))
        matrix.apply()
        g -= val

    # Increment red value from 0 to 255
    while r < 255:
        matrix.fill(PixelColor(r, g, b))
        matrix.apply()
        r += val

    # Decrement blue value from 255 to 0
    while b > 0:
        matrix.fill(PixelColor(r, g, b))
        matrix.apply()
        b -= val
