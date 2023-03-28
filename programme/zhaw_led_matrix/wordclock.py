from machine import Timer

from .characters import ClockTable
from .ledmatrix import ColorTable, LedMatrix


class WordClock:
    """
    This class implements a word clock on the LED matrix. It uses the
    RaspberryPi Pico RealTimeClock (RTC) as clock reference. Time is
    displayed in 5 minute steps on the word clock.
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
        now = self._clock.now()
        hours = now.hours
        minutes = now.minutes

        if minutes > 32:
            # after half past, the next hour must be displayed
            hours += 1
            # and minutes are going backwards
            minutes = 60 - minutes
            # and TO is used as modifier
            modifier = ClockTable.TO
        else:
            modifier = ClockTable.PAST

        # round minutes to closest multiple of 5
        minutes = 5 * round(minutes / 5)

        # display only hours from 0 - 11
        hours = hours % 12

        # Display time on wordclock
        self._matrix.clear()
        self._matrix.draw_list(ClockTable.wcl_hours[hours], self.hour_color)
        if minutes != 0:
            self._matrix.draw_list(ClockTable.wcl_minutes[minutes], self.minute_color)
            self._matrix.draw_list(modifier, self.word_color)
        self._matrix.set_brightness(self.brightness)
        self._matrix.apply()
