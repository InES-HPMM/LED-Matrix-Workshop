from utime import sleep_ms
from zhaw_led_matrix import (
    CharacterTable,
    ClockTable,
    ColorTable,
    LedMatrix,
)

# LED-Matrix initialisieren
matrix = LedMatrix(8, 8)
matrix.set_brightness(20)

# Die 10 von der Minutenanzeige in blau
# leuchten lassen
matrix.draw_list(
    ClockTable.MIN_TEN, ColorTable.BLUE
)
matrix.apply()
sleep_ms(1000)

# Die 10 von der Stundenanzeige in gruen
# leuchten lassen
matrix.clear()
matrix.draw_list(
    ClockTable.HOUR_TEN, ColorTable.GREEN
)
matrix.apply()
sleep_ms(1000)

# Buchstabe A auf LED-Matrix ausgeben in rot
matrix.clear()
matrix.draw_list(
    CharacterTable.A, ColorTable.RED
)
matrix.apply()
