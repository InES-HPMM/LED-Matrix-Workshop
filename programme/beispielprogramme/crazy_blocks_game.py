import random

from machine import Timer
from utime import sleep_ms

from zhaw_led_matrix import Button, CharacterTable, LedMatrix

CHARACTER_NUMBERS = [
    CharacterTable.ZERO,
    CharacterTable.ONE,
    CharacterTable.TWO,
    CharacterTable.THREE,
    CharacterTable.FOUR,
    CharacterTable.FIVE,
    CharacterTable.SIX,
    CharacterTable.SEVEN,
    CharacterTable.EIGHT,
    CharacterTable.NINE,
]


# -------------------------------------------------------------------------
def list_offset_x(coords, offset, cols):
    # find the highest and lowest y coordinate value to determine width of pixel art
    highest_x = 0
    lowest_x = cols

    for coord in coords:
        if highest_x < coord[0]:
            highest_x = coord[0]
        if lowest_x > coord[0]:
            lowest_x = coord[0]

    width = highest_x - lowest_x + 1

    i = -(highest_x + 1) + offset
    new_list = []
    for coord in coords:
        x, y = coord
        x = x + i
        if (x >= 0) and (x < cols):
            new_list.append((x, y))
    return new_list


# -------------------------------------------------------------------------
# CrazyBlocksGame Class
# -------------------------------------------------------------------------


class CrazyBlocksGame:
    MAX_VELOCITY: int = 58

    # Blocks Definition
    # name      list                               center  rotation_allowed?
    BLOCK_Z = [[[0, 0], [0, 1], [1, 1], [1, 2]], [1, 1], True]
    BLOCK_O = [[[0, 0], [0, 1], [1, 1], [1, 0]], [0, 0], False]
    BLOCK_L = [[[0, 0], [0, 1], [0, 2], [1, 0]], [0, 1], True]
    BLOCK_I = [[[0, 0], [0, 1], [0, 2], [0, 3]], [0, 1], True]
    BLOCK_T = [[[0, 0], [0, 1], [0, 2], [1, 1]], [0, 1], True]
    BLOCK_J = [[[0, 0], [0, 1], [0, 2], [1, 2]], [0, 1], True]
    BLOCK_S = [[[0, 1], [0, 2], [1, 0], [1, 1]], [1, 1], True]
    CRAZY_BLOCK_TABLE = [BLOCK_Z, BLOCK_O, BLOCK_L, BLOCK_I, BLOCK_T, BLOCK_J, BLOCK_S]

    def __init__(self, rows, cols):
        self._velocity = 0
        self._crazy_blocksMatrix = LedMatrix(rows, cols)
        self._rows = rows
        self._cols = cols
        self._crazy_blocks_field = []
        self._crazy_blocks_block_batch = []
        self.copy_to_empty_block_table(
            self.CRAZY_BLOCK_TABLE, self._crazy_blocks_block_batch
        )
        self.moving_block = CrazyBlocksGame.__get_empty_block()
        self.get_random_block(self.moving_block)
        self.next_moving_block = CrazyBlocksGame.__get_empty_block()
        self._score = 0
        self._game_over = False

    def __get_empty_block():
        return [[[]] * 4, [], None]

    def get_timer_period(self):
        return 300 + (self.MAX_VELOCITY - self._velocity) * 12

    def get_score(self):
        return self._score

    def is_game_over(self) -> bool:
        return self._game_over

    def is_running(self) -> bool:
        return self._velocity > 0

    def game_over(self):
        self._crazy_blocksMatrix.clear()
        self._crazy_blocksMatrix.draw_list(self._crazy_blocks_field, [50, 0, 0], True)
        self._crazy_blocksMatrix.apply()
        self._game_over = True
        self._velocity = 0
        sleep_ms(1000)
        for offset in reversed(range(-10, 53)):
            text_G = list_offset_x(CharacterTable.G, offset - 40, self._cols)
            text_A = list_offset_x(CharacterTable.A, offset - 34, self._cols)
            text_M = list_offset_x(CharacterTable.M, offset - 28, self._cols)
            text_E = list_offset_x(CharacterTable.E, offset - 22, self._cols)
            text_O = list_offset_x(CharacterTable.O, offset - 14, self._cols)
            text_V = list_offset_x(CharacterTable.V, offset - 8, self._cols)
            text_E2 = list_offset_x(CharacterTable.E, offset - 2, self._cols)
            text_R = list_offset_x(CharacterTable.R, offset + 4, self._cols)
            self._crazy_blocksMatrix.clear()
            self._crazy_blocksMatrix.draw_list(text_G, [50, 0, 0], True)
            self._crazy_blocksMatrix.draw_list(text_A, [50, 0, 0], True)
            self._crazy_blocksMatrix.draw_list(text_M, [50, 0, 0], True)
            self._crazy_blocksMatrix.draw_list(text_E, [50, 0, 0], True)
            self._crazy_blocksMatrix.draw_list(text_O, [50, 0, 0], True)
            self._crazy_blocksMatrix.draw_list(text_V, [50, 0, 0], True)
            self._crazy_blocksMatrix.draw_list(text_E2, [50, 0, 0], True)
            self._crazy_blocksMatrix.draw_list(text_R, [50, 0, 0], True)
            self._crazy_blocksMatrix.apply()
            sleep_ms(100)
        for offset in reversed(range(-10, 53)):
            text_S = list_offset_x(CharacterTable.S, offset - 40, self._cols)
            text_C = list_offset_x(CharacterTable.C, offset - 35, self._cols)
            text_O = list_offset_x(CharacterTable.O, offset - 29, self._cols)
            text_R = list_offset_x(CharacterTable.R, offset - 23, self._cols)
            text_E = list_offset_x(CharacterTable.E, offset - 17, self._cols)
            text_colon = list_offset_x([[0, 1], [0, 4]], offset - 15, self._cols)
            self._crazy_blocksMatrix.clear()
            self._crazy_blocksMatrix.draw_list(text_S, [50, 0, 0], True)
            self._crazy_blocksMatrix.draw_list(text_C, [50, 0, 0], True)
            self._crazy_blocksMatrix.draw_list(text_O, [50, 0, 0], True)
            self._crazy_blocksMatrix.draw_list(text_R, [50, 0, 0], True)
            self._crazy_blocksMatrix.draw_list(text_E, [50, 0, 0], True)
            self._crazy_blocksMatrix.draw_list(text_colon, [50, 0, 0], True)

            score_string = str(self._score)
            for i in range(len(score_string)):
                score_number = list_offset_x(
                    CHARACTER_NUMBERS[int(score_string[i])],
                    offset - (6 - i * 6),
                    self._cols,
                )
                self._crazy_blocksMatrix.draw_list(score_number, [50, 0, 0], True)

            self._crazy_blocksMatrix.apply()
            sleep_ms(100)

        self._crazy_blocksMatrix.clear()
        self._crazy_blocksMatrix.draw_list(self._crazy_blocks_field, [50, 0, 0], True)
        self._crazy_blocksMatrix.apply()

    def check_game_over(self):
        for i in range(len(self._crazy_blocks_field)):
            x, y = self._crazy_blocks_field[i]
            if y >= self._rows:
                return True
        return False

    def reset(self):
        self._velocity = 1
        self._crazy_blocks_field.clear()
        self._score = 0
        self._game_over = False

    def copy_block(self, block1, block2):
        for i in range(len(block1[0])):
            x, y = block1[0][i]
            block2[0][i] = [x, y]
        center_x, center_y = block1[1]
        rotation_allowed = block1[2]
        block2[1] = [center_x, center_y]
        block2[2] = rotation_allowed

    def copy_to_empty_block_table(self, block1, empty_block_table):
        for j in range(len(block1)):
            new_block = []
            new_list = []
            for i in range(len(block1[j][0])):
                x, y = block1[j][0][i]
                new_list.append([x, y])
            new_block.append(new_list)

            center_x, center_y = block1[j][1]
            rotation_allowed = block1[j][2]
            new_block.append([center_x, center_y])
            new_block.append(rotation_allowed)
            empty_block_table.append(new_block)

    # Rotatefunction
    # direction: 0=clockwise, 1=counterclockwise
    def rotate_90degrees(self, block_list, direction):
        coords, center, rotation_allowed = block_list

        if rotation_allowed:
            # rotate coords list around (0,0)
            for i in range(len(coords)):
                x, y = coords[i]
                if direction == 0:
                    coords[i] = [y, -x]
                else:
                    coords[i] = [-y, x]
            # rotate center
            center_x, center_y = center
            if direction == 0:
                center_new_x = center_y
                center_new_y = -center_x
            else:
                center_new_x = -center_y
                center_new_y = center_x
            # move list back to old center
            for i in range(len(coords)):
                [x, y] = coords[i]
                coords[i] = [
                    x - (center_new_x - center_x),
                    y - (center_new_y - center_y),
                ]

    def move_offset(self, block_list, x_offset, y_offset):
        coords, center, rotation_allowed = block_list
        for i in range(len(coords)):
            coords[i][0] += x_offset
            coords[i][1] += y_offset
        center[0] += x_offset
        center[1] += y_offset

    def check_border_collision(self, block_list):
        coords, center, rotation_allowed = block_list
        max_x = 0
        min_x = self._cols
        max_y = 0
        min_y = self._rows
        for coord in coords:
            if max_x < coord[0]:
                max_x = coord[0]
            if min_x > coord[0]:
                min_x = coord[0]
            if max_y < coord[1]:
                max_y = coord[1]
            if min_y > coord[1]:
                min_y = coord[1]
        if min_x < 0:
            for i in range(len(coords)):
                coords[i][0] -= min_x
            center[0] -= min_x
        if max_x >= self._cols:
            for i in range(len(coords)):
                coords[i][0] -= max_x - self._cols + 1
            center[0] -= max_x - self._cols + 1
        if min_y < 0:
            for i in range(len(coords)):
                coords[i][1] -= min_y
            center[1] -= min_y

    def blink_row(self, num_row):
        blink_list = []
        for i in range(self._cols):
            blink_list.append([i, num_row])
        for i in range(5):
            self._crazy_blocksMatrix.draw_list(blink_list, [30, 30, 30])
            self._crazy_blocksMatrix.apply()
            sleep_ms(100)
            self._crazy_blocksMatrix.draw_list(blink_list, [0, 0, 0])
            self._crazy_blocksMatrix.apply()
            sleep_ms(100)
        del blink_list

    def upper_block_fall(self, gone_row):
        for i in range(len(self._crazy_blocks_field)):
            x, y = self._crazy_blocks_field[i]
            if y > gone_row:
                self._crazy_blocks_field[i] = [x, y - 1]
        self._crazy_blocksMatrix.clear()
        self._crazy_blocksMatrix.draw_list(self._crazy_blocks_field, [0, 25, 25], True)
        self._crazy_blocksMatrix.apply()

    def check_full_line(self):
        at_least_one_row_found = False
        for y in range(self._rows):
            full_row_found = True
            for x in range(self._cols):
                # is x,y in self._crazy_blocks_field
                found = False
                for i in range(len(self._crazy_blocks_field)):
                    if self._crazy_blocks_field[i][0] == x and self._crazy_blocks_field[i][1] == y:
                        found = True
                        break
                if not found:
                    full_row_found = False
            if full_row_found:
                # FULL ROW FOUND
                at_least_one_row_found = True
                self.blink_row(y)
                self._score += 1
                print("New Score:")
                print(self._score)
                for x in range(self._cols):
                    self._crazy_blocks_field.remove([x, y])
                self.upper_block_fall(y)
                self._velocity = min(self.MAX_VELOCITY, self._velocity + 1)

        return at_least_one_row_found

    def check_collision_with_field(self, block_list):
        # Check collision with self._crazy_blocks_field
        for i in range(len(block_list[0])):
            x1, y1 = block_list[0][i]
            for j in range(len(self._crazy_blocks_field)):
                x2, y2 = self._crazy_blocks_field[j]
                if x1 == x2 and y1 == y2:
                    return True
        return False

    def get_random_block(self, block_list):
        # if batch of blocks is empty, refill with all blocks
        if len(self._crazy_blocks_block_batch) <= 0:
            self.copy_to_empty_block_table(
                self.CRAZY_BLOCK_TABLE, self._crazy_blocks_block_batch
            )

        # choose a random block from the batch
        x = random.randint(0, len(self._crazy_blocks_block_batch) - 1)
        self.copy_block(self._crazy_blocks_block_batch[x], block_list)
        # remove used block from batch
        del self._crazy_blocks_block_batch[x]

        # move to top of matrix
        self.move_offset(block_list, 0, self._rows)

        # generate random x offset
        x = random.randint(0, 8)
        self.move_offset(block_list, x, 0)
        self.check_border_collision(block_list)

        # generate random rotation
        x = random.randint(0, 4)
        for i in range(x):
            self.rotate_90degrees(block_list, 1)
        self.check_border_collision(block_list)


class Game:
    def __init__(self, two_matrices=True, allow_restart=True):
        num_rows, num_cols = (8, 8)
        if two_matrices:
            num_rows *= 2
        self._crazy_blocks = CrazyBlocksGame(num_rows, num_cols)

        button = Button()
        if allow_restart:
            button.set_center_handler(self.joystick_center_handler)
        button.set_left_handler(self.joystick_left_handler)
        button.set_right_handler(self.joystick_right_handler)
        button.set_up_handler(self.joystick_up_handler)
        button.set_down_handler(self.joystick_down_handler)

        self._timer = Timer()

        self._game_over_handler = None

    def get_score(self) -> int:
        return self._crazy_blocks.get_score()

    def is_running(self) -> bool:
        return self._crazy_blocks.is_running()

    def reset(self):
        return self._crazy_blocks.reset()

    def joystick_center_handler(self, _):
        if self._crazy_blocks.is_game_over():
            self._crazy_blocks.reset()
            self.run()

    def joystick_left_handler(self, _):
        if self._crazy_blocks.is_game_over():
            return
        self._crazy_blocks.copy_block(
            self._crazy_blocks.moving_block, self._crazy_blocks.next_moving_block
        )
        self._crazy_blocks.move_offset(self._crazy_blocks.next_moving_block, -1, 0)
        self._crazy_blocks.check_border_collision(self._crazy_blocks.next_moving_block)
        collision = self._crazy_blocks.check_collision_with_field(
            self._crazy_blocks.next_moving_block
        )
        if not collision:
            self._crazy_blocks.copy_block(
                self._crazy_blocks.next_moving_block, self._crazy_blocks.moving_block
            )
        self._crazy_blocks._crazy_blocksMatrix.clear()
        self._crazy_blocks._crazy_blocksMatrix.draw_list(
            self._crazy_blocks.moving_block[0], [30, 30, 0], True
        )
        self._crazy_blocks._crazy_blocksMatrix.draw_list(
            self._crazy_blocks._crazy_blocks_field, [0, 25, 25], True
        )
        self._crazy_blocks._crazy_blocksMatrix.apply()

    def joystick_right_handler(self, _):
        if self._crazy_blocks.is_game_over():
            return
        self._crazy_blocks.copy_block(
            self._crazy_blocks.moving_block, self._crazy_blocks.next_moving_block
        )
        self._crazy_blocks.move_offset(self._crazy_blocks.next_moving_block, 1, 0)
        self._crazy_blocks.check_border_collision(self._crazy_blocks.next_moving_block)
        collision = self._crazy_blocks.check_collision_with_field(
            self._crazy_blocks.next_moving_block
        )
        if not collision:
            self._crazy_blocks.copy_block(
                self._crazy_blocks.next_moving_block, self._crazy_blocks.moving_block
            )
        self._crazy_blocks._crazy_blocksMatrix.clear()
        self._crazy_blocks._crazy_blocksMatrix.draw_list(
            self._crazy_blocks.moving_block[0], [30, 30, 0], True
        )
        self._crazy_blocks._crazy_blocksMatrix.draw_list(
            self._crazy_blocks._crazy_blocks_field, [0, 25, 25], True
        )
        self._crazy_blocks._crazy_blocksMatrix.apply()

    def joystick_up_handler(self, _):
        if self._crazy_blocks.is_game_over():
            return
        self._crazy_blocks.copy_block(
            self._crazy_blocks.moving_block, self._crazy_blocks.next_moving_block
        )
        self._crazy_blocks.rotate_90degrees(self._crazy_blocks.next_moving_block, 1)
        self._crazy_blocks.check_border_collision(self._crazy_blocks.next_moving_block)
        collision = self._crazy_blocks.check_collision_with_field(
            self._crazy_blocks.next_moving_block
        )
        if not collision:
            self._crazy_blocks.copy_block(
                self._crazy_blocks.next_moving_block, self._crazy_blocks.moving_block
            )
        self._crazy_blocks._crazy_blocksMatrix.clear()
        self._crazy_blocks._crazy_blocksMatrix.draw_list(
            self._crazy_blocks.moving_block[0], [30, 30, 0], True
        )
        self._crazy_blocks._crazy_blocksMatrix.draw_list(
            self._crazy_blocks._crazy_blocks_field, [0, 25, 25], True
        )
        self._crazy_blocks._crazy_blocksMatrix.apply()

    def joystick_down_handler(self, pin):
        if pin.value() == 1 or self._crazy_blocks.is_game_over():
            return
        self._timer.deinit()
        while not self.progress():
            pass
        self.run()

    def set_game_over_handler(self, handler):
        self._game_over_handler = handler

    def progress(self) -> bool:
        self._crazy_blocks._crazy_blocksMatrix.clear()

        # copy current moving block
        self._crazy_blocks.copy_block(
            self._crazy_blocks.moving_block, self._crazy_blocks.next_moving_block
        )
        # move next_moving_block down by one pixel
        self._crazy_blocks.move_offset(self._crazy_blocks.next_moving_block, 0, -1)
        # check if block is colliding with left,right,bottom border
        # if it is, it moves the block nack inside the game field
        self._crazy_blocks.check_border_collision(self._crazy_blocks.next_moving_block)

        # Check if the block is no longer moving
        identical = True
        for i in range(len(self._crazy_blocks.moving_block[0])):
            x1, y1 = self._crazy_blocks.moving_block[0][i]
            x2, y2 = self._crazy_blocks.next_moving_block[0][i]
            if (x1 != x2) or (y1 != y2):
                identical = False
                break

        # Check if new block would be in existing field block
        has_collision = self._crazy_blocks.check_collision_with_field(
            self._crazy_blocks.next_moving_block
        )
        # If new moved block is identical to moving block, add to field
        if identical or has_collision:
            for i in range(len(self._crazy_blocks.moving_block[0])):
                x, y = self._crazy_blocks.moving_block[0][i]
                self._crazy_blocks._crazy_blocks_field.append([x, y])
            self._crazy_blocks._crazy_blocksMatrix.draw_list(
                self._crazy_blocks._crazy_blocks_field, [0, 25, 25], True
            )
            self._crazy_blocks.get_random_block(self._crazy_blocks.moving_block)
        else:
            self._crazy_blocks._crazy_blocksMatrix.draw_list(
                self._crazy_blocks._crazy_blocks_field, [0, 25, 25], True
            )
            self._crazy_blocks._crazy_blocksMatrix.draw_list(
                self._crazy_blocks.next_moving_block[0], [30, 30, 0], True
            )
            self._crazy_blocks.copy_block(
                self._crazy_blocks.next_moving_block, self._crazy_blocks.moving_block
            )

        self._crazy_blocks._crazy_blocksMatrix.apply()
        full_row_found = True
        while full_row_found:
            full_row_found = self._crazy_blocks.check_full_line()

        return identical or has_collision

    def run(self, _=None):
        self.progress()

        if self._crazy_blocks.check_game_over():
            if self._game_over_handler:
                self._game_over_handler()
            self._crazy_blocks.game_over()
            return

        self._timer.init(
            mode=Timer.ONE_SHOT,
            period=self._crazy_blocks.get_timer_period(),
            callback=self.run,
        )


if __name__ == "__main__":
    crazy_blocks = Game(two_matrices=False)
    crazy_blocks.run()
