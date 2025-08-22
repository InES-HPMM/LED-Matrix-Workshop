from machine import Timer

from .ledmatrix import ColorTable, LedMatrix


class WordClock:
    """
    This is an abstract class that implements an interface for a word clock on the LED
    matrix. It uses the RaspberryPi Pico RealTimeClock (RTC) as clock reference.
    """

    def __init__(self, clock):
        self._timer = Timer()
        self._matrix = LedMatrix(8, 8)
        self._clock = clock

        self.hour_color = ColorTable.WHITE
        self.minute_color = ColorTable.WHITE
        self.word_color = ColorTable.WHITE
        self.brightness = 50

        self.display_time()
        self.__schedule_refresh()

    def __schedule_refresh(self):
        """
        schedule refresh every minute
        """

        def refresh(_):
            self.display_time()
            self.__schedule_refresh()

        now = self._clock.now()
        period_sec = 60 - now.seconds
        self._timer.init(
            mode=Timer.ONE_SHOT, period=period_sec * 1000, callback=refresh
        )

    def display_time(self):
        pass
