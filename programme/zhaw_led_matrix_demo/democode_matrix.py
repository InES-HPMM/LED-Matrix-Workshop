from utime import sleep_ms
from zhaw_led_matrix import (
    ColorTable,
    LedMatrix,
    PixelColor,
)

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
sleep_ms(1000)

# Listen über Matrix bewegen

# Beispiellisten: Geist
# Koerper und Augen haben verschiedene Farben, darum gibt es dafuer zwei seperate Listen
ghost_body = [
    [0, 0], [2, 0], [4, 0], [6, 0], [0, 1], [1, 1], [2, 1], [3, 1], [4, 1], [5, 1],
    [6, 1], [0, 2], [1, 2], [2, 2], [3, 2], [4, 2], [5, 2], [6, 2], [0, 3], [1, 3],
    [2, 3], [3, 3], [4, 3], [5, 3], [6, 3], [0, 4], [3, 4], [6, 4], [0, 5], [3, 5],
    [6, 5], [1, 6], [2, 6], [3, 6], [4, 6], [5, 6], [2, 7], [3, 7], [4, 7],
]
ghost_eyes_right = [
    [1, 4], [2, 5], [1, 5], [4, 5], [5, 5], [4, 4],
]

# Listen nach oben bewegen
matrix.move_across(
    [ghost_body, ghost_eyes_right],
    8,
    [ColorTable.RED, ColorTable.WHITE],
    50,
    "up",
)

# Listen nach oben unten
matrix.move_across(
    [ghost_body, ghost_eyes_right],
    8,
    [ColorTable.RED, ColorTable.WHITE],
    50,
    "down",
)

# Listen nach oben links
matrix.move_across(
    [ghost_body, ghost_eyes_right],
    8,
    [ColorTable.RED, ColorTable.WHITE],
    50,
    "left",
)

# Listen nach rechts bewegen
matrix.move_across(
    [ghost_body, ghost_eyes_right],
    8,
    [ColorTable.RED, ColorTable.WHITE],
    50,
    "right",
)
