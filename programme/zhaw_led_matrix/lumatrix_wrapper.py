from zhaw_led_matrix import (
    CharacterTable,
    ColorTable,
    LedMatrix,
)


class Lumatrix:
    def __init__(self):
        self._matrix = LedMatrix(8, 8)


    def writeText(self, my_text, color=ColorTable.WHITE, brightness=20):
        text, length = CharacterTable.convert_str(my_text)
        self._matrix.set_brightness(brightness)
        self._matrix.move_across(text, length, colors=color)


    def drawImage(self, image, brightness=20):
        self._matrix.draw_bitmap(image)
        self._matrix.set_brightness(brightness)
        self._matrix.apply()
        
    
    def moveImage(self, image, brightness=20):
        self._matrix.draw_bitmap(image)
        
        buf = bytearray(self._matrix.buf)
        for i in range(len(buf)):
            buf[i] = buf[i] * brightness
            
        self._matrix.move_across(buf, 8)
