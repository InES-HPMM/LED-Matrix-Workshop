from ledmatrix import (
    ColorTable,
    LedMatrix,
    PixelColor,
)
from utime import sleep_ms

# Kreiere eigene Farbe
my_color = PixelColor(2, 211, 13)

# LED Matrix Objekt
matrix = LedMatrix(8, 8)

# Setze Helligkeit
matrix.set_brightness(20)

# Setze Pixel x=0,y=1
# ColorTable beinhaltet 16 Farben
matrix[0, 1] = ColorTable.YELLOW

# Sende Farbwerte an LED-Matrix
matrix.apply()
sleep_ms(1000)

# Alle Neopixel auf blau setzen
matrix.fill(ColorTable.BLUE)
matrix.apply()
sleep_ms(1000)

# Alle Farben auf Null setzen
matrix.clear()
matrix.apply()
sleep_ms(1000)

# Liste von Pixel auf einen Farbwert setzen
pixel_list = [(5, 1), (5, 2), (6, 1)]
matrix.draw_list(pixel_list, ColorTable.GREEN)
matrix.apply()
sleep_ms(1000)

# Linien zeichnen:
# Gerade Linie
matrix.draw_line(
    (0, 0), (0, 4), ColorTable.ORANGE
)
# Diagonale Linie
matrix.draw_line(
    (0, 7), (5, 5), ColorTable.PINK
)
matrix.apply()
