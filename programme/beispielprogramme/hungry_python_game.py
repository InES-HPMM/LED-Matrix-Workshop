from collections import namedtuple
from random import randint
from machine import Timer

from zhaw_led_matrix import (
    LedMatrix,
    Button,
    ColorTable
)

Pos = namedtuple("Pos", ["x", "y"])


class HungryPythonGame:
    MAX_VELOCITY: int = 48

    def __init__(self, cols: int, rows: int):
        self._hungry_python = RingBuf(cols * rows)
        self._field_size: Pos = Pos(cols, rows)
        self._food_pos: Pos = None
        self._velocity: int = 0
        self._dir = None
        self._next_dir = None
        self._just_ate: bool = False
        self._game_over: bool = False
        self.reset()

    def reset(self):
        self._hungry_python.clear()
        self._hungry_python.push(self.__get_random_pos())
        self._just_ate = False
        self._game_over = False
        self._velocity = 1
        self._dir = Direction.RIGHT
        self.__place_food()

    def __get_random_pos(self):
        return Pos(
            randint(0, self._field_size.x - 1), randint(0, self._field_size.y - 1)
        )

    def __place_food(self):
        # use nth free position for food
        num_free_positions = self.get_max_len() - len(self)
        n = randint(0, num_free_positions - 1)
        i = 0
        for x in range(self._field_size.x):
            for y in range(self._field_size.y):
                pos = Pos(x, y)

                if any(map(lambda p: p == pos, self._hungry_python)):
                    continue

                if i == n:
                    self._food_pos = pos
                    return

                i += 1

        raise Exception("no free position for food found")

    def get_head_pos(self) -> Pos:
        return self._hungry_python.last()

    def get_tail_pos(self) -> Pos:
        return self._hungry_python.first()

    def get_food_pos(self) -> Pos:
        return self._food_pos

    def is_game_over(self) -> bool:
        return self._game_over

    def get_timer_period(self) -> int:
        return 100 + (self.MAX_VELOCITY - self._velocity) * 7

    def get_max_len(self) -> int:
        return self._field_size.x * self._field_size.y

    def __move_pos(self, p: Pos, dir) -> Pos:
        new_x, new_y = p
        if dir == Direction.UP:
            new_y = (p.y + 1) % self._field_size.y
        elif dir == Direction.RIGHT:
            new_x = (p.x + 1) % self._field_size.x
        elif dir == Direction.DOWN:
            if p.y == 0:
                new_y = self._field_size.y - 1
            else:
                new_y = p.y - 1
        elif dir == Direction.LEFT:
            if p.x == 0:
                new_x = self._field_size.x - 1
            else:
                new_x = p.x - 1
        else:
            raise Exception("invalid dir arg")

        return Pos(new_x, new_y)

    def set_direction(self, dir):
        if dir == Direction.reverse(self._dir):
            return
        self._next_dir = dir

    def progress(self):
        if self._game_over:
            return

        if self._next_dir is not None:
            self._dir = self._next_dir
            self._next_dir = None

        next_pos = self.__move_pos(self.get_head_pos(), self._dir)

        # check for collision with itself
        if any(map(lambda p: p == next_pos and p != self.get_tail_pos(), self)):
            self._game_over = True
            self._food_pos = None
            return

        if self._velocity == 0:
            return

        # move head
        self._hungry_python.push(next_pos)

        if not self._just_ate:
            # move tail
            self._hungry_python.pop()
        else:
            self._just_ate = False
            if len(self) == self.get_max_len():
                # you win
                self._velocity = 0
                return

        if self.get_head_pos() == self._food_pos:
            # omnomnom
            self._food_pos = None
            self._just_ate = True
            self.__place_food()
            self._velocity = min(self.MAX_VELOCITY, self._velocity + 1)

    def __iter__(self):
        return self._hungry_python.__iter__()

    def __getitem__(self, i):
        return self._hungry_python.__getitem__(i)

    def __len__(self):
        return len(self._hungry_python)

    def __str__(self):
        return str(self._hungry_python)


class RingBuf:
    def __init__(self, capacity: int):
        self._capacity = capacity
        self.clear()

    def clear(self):
        self._buf = [None for _ in range(self._capacity)]
        self._start = 0
        self._len = 0

    def push(self, x):
        if self.is_full():
            raise Exception("cant push, ringbuf full")
        self._buf[(self._start + self._len) % self._capacity] = x
        self._len += 1

    def pop(self):
        if self.is_empty():
            raise Exception("cant pop, ringbuf empty")
        x = self._buf[self._start]
        self._len -= 1
        self._start = (self._start + 1) % self._capacity
        return x

    def is_full(self):
        return len(self) == self._capacity

    def is_empty(self):
        return self._len == 0

    def first(self):
        return self[0]

    def last(self):
        return self[len(self) - 1]

    def __len__(self):
        return self._len

    def __getitem__(self, i):
        return self._buf[(self._start + i) % self._capacity]

    def __iter__(self):
        for i in range(self._len):
            yield self[i]

    def __str__(self):
        out = "("
        for i, p in enumerate(self):
            out += str(p)
            if i < len(self) - 1:
                out += ", "
        return out + ")"


class Direction:
    UP = 0
    RIGHT = 1
    LEFT = 2
    DOWN = 3

    def reverse(dir):
        if dir == Direction.UP:
            return Direction.DOWN
        if dir == Direction.RIGHT:
            return Direction.LEFT
        if dir == Direction.LEFT:
            return Direction.RIGHT
        if dir == Direction.DOWN:
            return Direction.UP


def joystick_center_handler(_):
    if hungry_python.is_game_over():
        hungry_python.reset()


def joystick_left_handler(_):
    hungry_python.set_direction(Direction.LEFT)


def joystick_right_handler(_):
    hungry_python.set_direction(Direction.RIGHT)


def joystick_up_handler(_):
    hungry_python.set_direction(Direction.UP)


def joystick_down_handler(_):
    hungry_python.set_direction(Direction.DOWN)


def slithering_python(_):
    hungry_python.progress()
    matrix.clear()
    if hungry_python.is_game_over():
        hungry_python_color = ColorTable.RED
    else:
        hungry_python_color = ColorTable.GREEN
    for pos in hungry_python:
        matrix[pos].set(hungry_python_color)
    head_pos = hungry_python.get_head_pos()
    if head_pos is not None:
        matrix[head_pos] = ColorTable.TEAL
    food_pos = hungry_python.get_food_pos()
    if food_pos is not None:
        matrix[food_pos] = ColorTable.ORANGE
    matrix.apply()

    timer.init(
        mode=Timer.ONE_SHOT, period=hungry_python.get_timer_period(), callback=slithering_python
    )


num_rows, num_cols = (8, 8)
matrix = LedMatrix(num_rows, num_cols)
hungry_python = HungryPythonGame(num_rows, num_cols)

button = Button()
timer = Timer()

button.set_center_handler(joystick_center_handler)
button.set_left_handler(joystick_left_handler)
button.set_right_handler(joystick_right_handler)
button.set_up_handler(joystick_up_handler)
button.set_down_handler(joystick_down_handler)

slithering_python(None)
