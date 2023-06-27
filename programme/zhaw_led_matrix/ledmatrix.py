import gc
from collections import namedtuple

import micropython
import ustruct
from machine import Pin, bitstream  # GPIO access
from utime import sleep_ms, ticks_ms, ticks_us

# pin to which NeoPixel LEDs are connected to
PIN_NP = 19

# LED data timing (high_0, low_0, high_1, low_1)
TIMING = (400, 850, 800, 450)


PixelColor = namedtuple("Color", ["red", "green", "blue"])


class ColorTable:
    """list of predefined colors"""

    YELLOW = PixelColor(255, 255, 0)
    ORANGE = PixelColor(255, 165, 0)
    RED = PixelColor(255, 0, 0)
    PURPLE = PixelColor(128, 0, 128)
    PINK = PixelColor(255, 0, 255)
    BLUE = PixelColor(0, 0, 255)
    TEAL = PixelColor(0, 128, 128)
    AQUA = PixelColor(0, 255, 255)
    LIME = PixelColor(0, 255, 0)
    GREEN = PixelColor(0, 128, 0)
    LGREY = PixelColor(119, 136, 153)
    GREY = PixelColor(100, 100, 100)
    BROWN = PixelColor(139, 69, 19)
    LBROWN = PixelColor(205, 133, 63)
    WHITE = PixelColor(255, 255, 255)
    BLACK = PixelColor(0, 0, 0)


class LedMatrix:
    """
    handle LED operations on the Wordclock

    When using multiple matrices connect them like this:

        [::]-+ [::]-+ [::]
         |   |  |   |  |
        [::] +-[::] +-[::]
    """

    def __init__(self, num_rows, num_cols, num_matrices=(1, 1)):
        """
        :param tuple num_matrices: number of matrices in x and y direction
        """
        # size of one matrix
        self.cols_matrix, self.rows_matrix = num_cols, num_rows
        self.cols = num_cols * num_matrices[0]
        self.rows = num_rows * num_matrices[1]
        self._pin = Pin(PIN_NP, Pin.OUT)
        self._brightness = 50
        self.clear()

    @micropython.native
    def __is_coord_in_range(self, coord):
        if isinstance(coord, int):
            return coord < len(self)
        else:
            x, y = coord
            return x >= 0 and x < self.cols and y >= 0 and y < self.rows

    @micropython.native
    def __coord_to_idx(self, coord):
        # This is commented for performance reasons, uncomment it for debugging
        # if not self.__is_coord_in_range(coord):
        #     raise IndexError(f"coordinates out of range: ({coord})")

        if isinstance(coord, int):
            x = coord % self.cols
            y = coord // self.cols
        else:
            x, y = coord

        return (
            x // self.cols_matrix * self.rows * self.cols_matrix
            + x % self.cols_matrix
            + y * self.rows_matrix
        ) * 3

    @micropython.native
    def __getitem__(self, coord):
        idx = self.__coord_to_idx(coord)
        buf = memoryview(self.buf)
        return PixelColor(buf[idx + 1], buf[idx], buf[idx + 2])

    @micropython.native
    def __setitem__(self, coord, color):
        idx = self.__coord_to_idx(coord)
        buf = self.buf
        buf[idx] = color[1]
        buf[idx + 1] = color[0]
        buf[idx + 2] = color[2]

    @micropython.native
    def __len__(self):
        return self.cols * self.rows

    @micropython.native
    def set_brightness(self, brightness):
        if brightness < 0 or brightness > 100:
            raise Exception(f"invalid brightness argument: {brightness}")
        self._brightness = brightness

    @micropython.native
    def clear(self):
        """turn off all leds"""
        self.buf = bytearray(len(self) * 3)

    @micropython.native
    def apply(self):
        """apply brightness and write buffer to leds"""
        buf = bytearray(self.buf)
        for i in range(len(buf)):
            buf[i] = buf[i] * self._brightness // 100

        # bitbang data to LEDs
        bitstream(self._pin, 0, TIMING, buf)

    @micropython.native
    def fill(self, color):
        """set all leds to the given color"""
        for i in range(len(self)):
            self[i] = color

    @micropython.native
    def draw_list(self, coords, color, crop=False, offset=(0, 0)):
        """
        set all leds at the given coordinates to the given color

        :param bool crop: whether to ignore out of bounds coordinates
        :param tuple offset: offset to apply to each coordinate
        """
        for coord in coords:
            coord = coord[0] + offset[0], coord[1] + offset[1]
            if crop and not self.__is_coord_in_range(coord):
                continue
            self[coord] = color

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
        bitmap_width = (image_size // 3) // bitmap_height

        if bitmap_height > self.rows or bitmap_width > self.cols:
            print(f"bitmap is larger than matrix: {bitmap_width}x{bitmap_height}")

        if (color_depth) != 24:
            raise Exception(
                f"Wrong color-depth ({color_depth})) detected. Use bitmaps with a color-depth of 24 bits.",
            )

        if (bitmap_size) != 246:
            print(
                "The bitmap size is different than expected. The image may be defective."
            )

        for i in range(image_size // 3):
            if upper_left_origin:
                x = i % bitmap_width
                y = i // bitmap_width
                y = bitmap_height - 1 - y
                j = y * bitmap_width + x
            else:
                j = i
            j *= 3
            self[i] = (pic[j + 2], pic[j + 1], pic[j])

    @micropython.native
    def move_across(
        self, bitmaps, length, colors=ColorTable.WHITE, delay_ms=50, direction="left"
    ):
        """
        moves bitmaps across the led matrix

        :param list bitmaps: list of lists with coordinates
        :param int length: length of all bitmaps combined in the specified direction
        :param list colors: color to use for each bitmap
        """

        def is_x_in_bounds(coords, offset):
            x, _ = coords[0]
            x_offset, _ = offset
            if x + x_offset - self.cols > self.cols:
                return -1
            if x + x_offset + self.cols < 0:
                return 1
            return 0

        def is_y_in_bounds(coords, offset):
            _, y = coords[0]
            _, y_offset = offset
            if y + y_offset - self.rows > self.rows:
                return -1
            if y + y_offset + self.rows < 0:
                return 1
            return 0

        # wrap in list if only one bitmap is supplied
        try:
            bitmaps[0][0][0]
        except TypeError:
            bitmaps = [bitmaps]

        # use same color for all bitmaps if only one color is supplied
        if not isinstance(colors, list):
            colors = [colors] * len(bitmaps)

        if direction == "left":
            offset_range = range(self.cols, -(length + 1), -1)
        elif direction == "right":
            offset_range = range(-(length + 1), self.cols + 1)
        elif direction == "up":
            offset_range = range(-self.rows, self.rows + 1)
        elif direction == "down":
            offset_range = range(self.rows, -(self.rows + 1), -1)
        else:
            raise Exception("invalid direction")

        if direction in ["left", "right"]:
            offset_range = (offset_range, [0] * len(offset_range))
            is_in_bounds = is_x_in_bounds
        else:
            offset_range = ([0] * len(offset_range), offset_range)
            is_in_bounds = is_y_in_bounds

        for offset in zip(*offset_range):
            self.clear()

            for bitmap, color in zip(bitmaps, colors):
                if not bitmap:
                    continue

                # only display bitmap if parts of it are in bounds
                res = is_in_bounds(bitmap, offset)
                if res < 0:
                    break
                elif res > 0:
                    continue

                self.draw_list(bitmap, color, crop=True, offset=offset)

            self.apply()
            # regularly calling the garbage collector reduces stutter
            gc.collect()
            sleep_ms(delay_ms)
