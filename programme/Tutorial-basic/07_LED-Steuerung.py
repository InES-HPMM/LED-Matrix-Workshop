# Importierte Bibliotheken
from machine import Pin
from neopixel import NeoPixel
from utime import sleep_ms

# Variablen / Objekte initialisieren
led_pin = Pin(19, Pin.OUT)
matrix = NeoPixel(led_pin, 64)

# Im Programmcode wird immer bei 0 gestartet
matrix[0] = [50, 0, 0]

# Informationen zur Matrix / den LEDs schicken
matrix.write()
