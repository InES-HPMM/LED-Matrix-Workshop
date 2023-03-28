import random

from zhaw_led_matrix import (
    Clock,
    Button,
    ColorTable,
    PixelColor,
    WordClock
)

button = Button()
clock = Clock()
wordclock = WordClock(clock)

"""
The clock has two modes:
 1. Clock mode: slide switch left, time is displayed
 2. Set time mode: slide switch to right, set time with 5-way switch
"""
set_time_mode = button.switch.value()

default_hour_color = ColorTable.WHITE
default_minute_color = ColorTable.WHITE
default_word_color = ColorTable.WHITE

wordclock.hour_color = default_hour_color
wordclock.minute_color = default_minute_color
wordclock.word_color = default_word_color


def joystick_left_handler(_):
    if set_time_mode:
        now = clock.now()
        # decrease minutes by 5 and round to next 5
        minutes = (now.minutes - 5) % 60
        minutes = round_base(minutes, 5)
        clock.set_time(now.hours, minutes)
    else:
        wordclock.hour_color = default_hour_color
        wordclock.minute_color = default_minute_color
        wordclock.word_color = default_word_color

    wordclock.display_time()


def joystick_right_handler(_):
    if set_time_mode:
        now = clock.now()
        # increase minutes by 5 and round to next 5
        minutes = (now.minutes + 5) % 60
        minutes = round_base(minutes, 5)
        clock.set_time(now.hours, minutes)
    else:
        # change colors to random values
        wordclock.hour_color = PixelColor(
            random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)
        )
        wordclock.minute_color = PixelColor(
            random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)
        )
        wordclock.word_color = PixelColor(
            random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)
        )

    wordclock.display_time()


def joystick_up_handler(_):
    if set_time_mode:
        now = clock.now()
        # increase hours by 1
        hours = (now.hours + 1) % 24
        clock.set_time(hours, now.minutes)
    else:
        # increase brightness by 10%
        wordclock.brightness = min(100, wordclock.brightness + 10)
        if wordclock.brightness == 100:
            print("max brightness reached")

    wordclock.display_time()


def joystick_down_handler(_):
    if set_time_mode:
        now = clock.now()
        # decrease hours by 1
        hours = (now.hours - 1) % 24
        clock.set_time(hours, now.minutes)
    else:
        # decrease brightness by 10%
        wordclock.brightness = max(0, wordclock.brightness - 10)
        if wordclock.brightness == 0:
            print("min brightness reached")

    wordclock.display_time()


def joystick_center_handler(_):
    # currently not unused
    print("joystick center button pressed")


def switch_handler(_):
    """
    change clock mode when switch is moved
    """
    global set_time_mode
    set_time_mode = button.switch.value()
    wordclock.display_time()


def round_base(value, base):
    """round `value` to closest multiple of `base`"""
    return base * round(value / base)


# set handler functions for button events
button.set_center_handler(joystick_center_handler)
button.set_left_handler(joystick_left_handler)
button.set_right_handler(joystick_right_handler)
button.set_up_handler(joystick_up_handler)
button.set_down_handler(joystick_down_handler)
button.set_switch_handler(switch_handler)
