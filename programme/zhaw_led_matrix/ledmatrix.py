from machine import Pin  # GPIO access
from neopixel import NeoPixel  # library that handles LEDs
from collections import namedtuple
import ustruct

# pin to which NeoPixel LEDs are connected to
PIN_NP = 19


class PixelColor:
    """store color for a LED"""

    def __init__(self, r, g, b):
        self.red = r
        self.green = g
        self.blue = b

    def __iter__(self):
        """allows unpacking"""
        return iter((self.red, self.green, self.blue))

    def __str__(self):
        return f"(red: {self.red}, green: {self.green}, blue: {self.blue})"

    def __getitem__(self, i):
        return (self.red, self.green, self.blue)[i]

    def copy(self):
        return PixelColor(*self)

    def set(self, color):
        """:param tuple color: (red, green, blue) color tuple"""
        self.red, self.green, self.blue = color


class ColorTable:
    """list of predefined colors"""

    # read only color type for fixed colors
    Color = namedtuple("Color", ["red", "green", "blue"])

    YELLOW = Color(255, 255, 0)
    ORANGE = Color(255, 165, 0)
    RED = Color(255, 0, 0)
    PURPLE = Color(128, 0, 128)
    PINK = Color(255, 0, 255)
    BLUE = Color(0, 0, 255)
    TEAL = Color(0, 128, 128)
    AQUA = Color(0, 255, 255)
    LIME = Color(0, 255, 0)
    GREEN = Color(0, 128, 0)
    LGREY = Color(119, 136, 153)
    GREY = Color(100, 100, 100)
    BROWN = Color(139, 69, 19)
    LBROWN = Color(205, 133, 63)
    WHITE = Color(255, 255, 255)
    BLACK = Color(0, 0, 0)


class LedMatrix:
    """handle LED operations on the Wordclock"""

    def __init__(self, num_rows, num_cols):
        self.rows = num_rows
        self.cols = num_cols
        self._np = NeoPixel(Pin(PIN_NP, Pin.OUT), self.rows * self.cols)
        self._brightness = 50
        self.buf = [PixelColor(*ColorTable.BLACK) for _ in range(self.rows * self.cols)]

    def __cord_to_idx(self, coord):
        try:
            x, y = coord
            if x >= self.cols or y >= self.rows:
                raise IndexError(f"coordinates out of range: ({x,y})")
        except TypeError:
            x, y = (coord, 0)
        return y * self.cols + x

    def __getitem__(self, coord):
        return self.buf[self.__cord_to_idx(coord)]

    def __setitem__(self, coord, color):
        self.buf[self.__cord_to_idx(coord)] = PixelColor(*color)

    def set_brightness(self, brightness):
        if brightness < 0 or brightness > 100:
            raise Exception(f"invalid brightness argument: {brightness}")
        self._brightness = brightness

    def clear(self):
        """turn off all leds"""
        self.fill(ColorTable.BLACK)

    def apply(self):
        """apply brightness and write buffer to leds"""
        for i in range(len(self._np)):
            c = (round(x * self._brightness / 100) for x in self.buf[i])
            self._np[i] = tuple(c)
        self._np.write()

    def fill(self, color):
        """set all leds to the given color"""
        [x.set(color) for x in self.buf]

    def draw_list(self, coords, color, clip=False):
        """set all leds at the given coordinates to the given color"""
        for coord in coords:
            try:
                self[coord] = color
            except IndexError:
                if clip:
                    continue
                else:
                    raise

    def draw_line(self, start_coord, end_coord, color):
        """
        Draw line using Bresenham's line algorithm

        implementation copied from https://en.wikipedia.org/wiki/Bresenham%27s_line_algorithm
        """
        ((x0, y0), (x1, y1)) = (start_coord, end_coord)
        if abs(y1 - y0) < abs(x1 - x0):
            if x0 > x1:
                self.__draw_line_low(end_coord, start_coord, color)
            else:
                self.__draw_line_low(start_coord, end_coord, color)
        else:
            if y0 > y1:
                self.__draw_line_high(end_coord, start_coord, color)
            else:
                self.__draw_line_high(start_coord, end_coord, color)

    def __draw_line_low(self, start_coord, end_coord, color):
        ((x0, y0), (x1, y1)) = (start_coord, end_coord)
        dx, dy = (x1 - x0, y1 - y0)
        yi = 1
        if dy < 0:
            yi = -1
            dy = -dy
        D = (2 * dy) - dx
        y = y0
        for x in range(x0, x1 + 1):
            self[x, y] = color
            if D > 0:
                y = y + yi
                D = D + (2 * (dy - dx))
            else:
                D = D + 2 * dy

    def __draw_line_high(self, start_coord, end_coord, color):
        ((x0, y0), (x1, y1)) = (start_coord, end_coord)
        dx, dy = (x1 - x0, y1 - y0)
        xi = 1
        if dx < 0:
            xi = -1
            dx = -dx
        D = (2 * dx) - dy
        x = x0
        for y in range(y0, y1 + 1):
            self[x, y] = color
            if D > 0:
                x = x + xi
                D = D + (2 * (dx - dy))
            else:
                D = D + 2 * dx

    def draw_bitmap(self, path):
        """
        Draw a bitmap file with a color depth of 24 bit

        bitmap format: https://en.wikipedia.org/wiki/BMP_file_format

        :param string path: path to bitmap file
        """

        file = open(path, "rb")
        bmp = file.read()

        color_depth = int.from_bytes(bmp[28:30], "little")
        bitmap_size = int.from_bytes(bmp[2:6], "little")
        bitmap_offset = int.from_bytes(bmp[10:14], "little")
        image_size = int.from_bytes(bmp[34:38], "little")
        bitmap_height = ustruct.unpack("<h", bmp[22:26])[0]
        upper_left_origin = bitmap_height < 0
        bitmap_height = abs(bitmap_height)
        pic = bmp[bitmap_offset:]

        if image_size != self.rows * self.cols * 3 or bitmap_height != self.rows:
            raise Exception(
                f"The bitmap has the wrong size. Use bitmaps with a size of {self.cols}x{self.rows}."
            )

        if (color_depth) != 24:
            raise Exception(
                f"Wrong color-depth ({color_depth})) detected. Use bitmaps with a color-depth of 24 bits.",
            )

        if (bitmap_size) != 246:
            print(
                "The bitmap size is different than expected. The image may be defective."
            )

        for i, p in enumerate(self):
            if upper_left_origin:
                x = i % self.cols
                y = i // self.cols
                y = self.rows - 1 - y
                i = y * self.cols + x
            i *= 3
            p.set((pic[i + 2], pic[i + 1], pic[i]))
