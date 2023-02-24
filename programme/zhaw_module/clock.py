from machine import RTC
from collections import namedtuple

# Thonny automatically syncs RTC time to PC


class Time(
    namedtuple(
        "Time",
        [
            "year",
            "month",
            "day",
            "weekday",
            "hours",
            "minutes",
            "seconds",
            "subseconds",
        ],
    )
):
    DAYS = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]

    def __str__(self):
        return f"""\
{self.DAYS[self.weekday]} {self.year}-{self.month}-{self.day} \
{self.hours:02}:{self.minutes:02}:{self.seconds:02}"""


class Clock:
    def __init__(self):
        self._rtc = RTC()

    def __str__(self):
        return self.now().__str__()

    def now(self):
        return Time(*self._rtc.datetime())

    def set_datetime(self, year, month, day, hours, minutes):
        self._rtc.datetime((year, month, day, None, hours, minutes, 0, 0))

    def set_date(self, year, month, day, hours, minutes):
        now = self.now()
        self._rtc.datetime(
            (year, month, day, None, now.hours, now.minutes, now.seconds, 0)
        )

    def set_time(self, hours, minutes):
        now = self.now()
        self._rtc.datetime((now.year, now.month, now.day, None, hours, minutes, 0, 0))
