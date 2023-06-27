from machine import Timer

from .ledmatrix import ColorTable, LedMatrix


class WordClock:
    """
    This class implements a word clock on the LED matrix. It uses the
    RaspberryPi Pico RealTimeClock (RTC) as clock reference. Time is
    displayed in 5 minute steps on the word clock.
    """

    def __init__(self, clock, version=1):
        self._timer = Timer()
        self._matrix = LedMatrix(8, 8)
        self._clock = clock
        self._clocktable = ClockTable(version=version)

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
            modifier = self._clocktable.TO
        else:
            modifier = self._clocktable.PAST

        # round minutes to closest multiple of 5
        minutes = 5 * round(minutes / 5)

        # display only hours from 0 - 11
        hours = hours % 12

        # Display time on wordclock
        self._matrix.clear()
        self._matrix.draw_list(self._clocktable.HOURS_MAPPING[hours], self.hour_color)
        if minutes != 0:
            self._matrix.draw_list(self._clocktable.MINUTES_MAPPING[minutes], self.minute_color)
            self._matrix.draw_list(modifier, self.word_color)
        self._matrix.set_brightness(self.brightness)
        self._matrix.apply()


class ClockTable():
    def __init__(self, version=1):
        self._version = version

        self.ONE = [
            (1, 0),
            (4, 0),
            (7, 0),
        ]
        self.TWO = [
            (0, 1),
            (1, 1),
            (1, 0),
        ]
        self.THREE = [
            (3, 2),
            (4, 2),
            (5, 2),
            (6, 2),
            (7, 2),
        ]
        self.FOUR = [
            (0, 0),
            (1, 0),
            (2, 0),
            (3, 0),
        ]
        self.HOUR_FIVE = [
            (0, 3),
            (1, 3),
            (2, 3),
            (3, 3),
        ]
        self.MIN_FIVE = [
            (4, 5),
            (5, 5),
            (6, 5),
            (7, 5),
        ]
        self.SIX = [
            (0, 2),
            (1, 2),
            (2, 2),
        ]
        self.SEVEN = [
            (0, 2),
            (4, 1),
            (5, 1),
            (6, 1),
            (7, 1),
        ]
        self.EIGHT = [
            (3, 3),
            (4, 3),
            (5, 3),
            (6, 3),
            (7, 3),
        ]
        self.NINE = [
            (4, 0),
            (5, 0),
            (6, 0),
            (7, 0),
        ]
        self.HOUR_TEN = [
            (7, 3),
            (7, 2),
            (7, 1),
        ]
        self.MIN_TEN = [
            (2, 7),
            (4, 7),
            (5, 7),
        ]
        self.ELEVEN = [
            (2, 1),
            (3, 1),
            (4, 1),
            (5, 1),
            (6, 1),
            (7, 1),
        ]
        self.TWELVE = [
            (0, 1),
            (1, 1),
            (2, 1),
            (3, 1),
            (5, 1),
            (6, 1),
        ]
        self.QUARTER = [
            (1, 6),
            (2, 6),
            (3, 6),
            (4, 6),
            (5, 6),
            (6, 6),
            (7, 6),
        ]
        self.TWENTY = [
            (2, 7),
            (3, 7),
            (4, 7),
            (5, 7),
            (6, 7),
            (7, 7),
        ]
        self.TWENTY_FIVE = [
            (2, 7),
            (3, 7),
            (4, 7),
            (5, 7),
            (6, 7),
            (7, 7),
            (4, 5),
            (5, 5),
            (6, 5),
            (7, 5),
        ]
        if version == 1:
            self.HALF = [
                (0, 5),
                (1, 5),
                (2, 5),
                (3, 5),
            ]
            self.PAST = [
                (1, 4),
                (2, 4),
                (3, 4),
                (4, 4),
            ]
            self.TO = [
                (6, 4),
                (7, 4),
            ]
            self.ZHAW = [
                (0, 7),
                (0, 6),
                (1, 5),
                (0, 4),
            ]
        elif version == 2:
            self.HALF = [
                (1, 5),
                (2, 5),
                (3, 5),
                (4, 5),
            ]
            self.PAST = [
                (2, 4),
                (3, 4),
                (4, 4),
                (5, 4),
            ]
            self.TO = [
                (5, 4),
                (6, 4),
            ]
            self.ZHAW = [
                (0, 7),
                (0, 6),
                (0, 5),
                (0, 4),
            ]
        # Lookup dictionary for wordclock hours
        self.HOURS_MAPPING = {
            0: self.TWELVE,
            1: self.ONE,
            2: self.TWO,
            3: self.THREE,
            4: self.FOUR,
            5: self.HOUR_FIVE,
            6: self.SIX,
            7: self.SEVEN,
            8: self.EIGHT,
            9: self.NINE,
            10: self.HOUR_TEN,
            11: self.ELEVEN,
        }
        # Lookup dictionary for wordclock minutes
        self.MINUTES_MAPPING = {
            0: 0,
            5: self.MIN_FIVE,
            10: self.MIN_TEN,
            15: self.QUARTER,
            20: self.TWENTY,
            25: self.TWENTY_FIVE,
            30: self.HALF,
        }
