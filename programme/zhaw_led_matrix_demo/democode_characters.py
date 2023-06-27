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

# Check which version of the wordclock
# you have and adapt the version parameter
clocktable = ClockTable(version=1)

# Die 10 von der Minutenanzeige in blau
# leuchten lassen
matrix.draw_list(
    clocktable.MIN_TEN, ColorTable.BLUE
)
matrix.apply()
sleep_ms(1000)

# Die 10 von der Stundenanzeige in gruen
# leuchten lassen
matrix.clear()
matrix.draw_list(
    clocktable.HOUR_TEN, ColorTable.GREEN
)
matrix.apply()
sleep_ms(1000)

# Buchstabe A auf LED-Matrix ausgeben in rot
matrix.clear()
matrix.draw_list(
    CharacterTable.A, ColorTable.RED
)
matrix.apply()
sleep_ms(1000)

# Laufschrift
laufschrift = "hello world"
text, length = CharacterTable.convert_str(laufschrift)
matrix.move_across(text, length)
