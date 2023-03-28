from machine import Pin


class Button:
    up = Pin(3, Pin.IN, Pin.PULL_UP)
    down = Pin(6, Pin.IN, Pin.PULL_UP)
    left = Pin(7, Pin.IN, Pin.PULL_UP)
    right = Pin(2, Pin.IN, Pin.PULL_UP)
    switch = Pin(9, Pin.IN, Pin.PULL_UP)
    center = Pin(8, Pin.IN, Pin.PULL_UP)

    def set_center_handler(self, handler):
        self.center.irq(trigger=Pin.IRQ_FALLING, handler=handler)

    def set_left_handler(self, handler):
        self.left.irq(trigger=Pin.IRQ_FALLING, handler=handler)

    def set_right_handler(self, handler):
        self.right.irq(trigger=Pin.IRQ_FALLING, handler=handler)

    def set_up_handler(self, handler):
        self.up.irq(trigger=Pin.IRQ_FALLING, handler=handler)

    def set_down_handler(self, handler):
        self.down.irq(trigger=Pin.IRQ_FALLING, handler=handler)

    def set_switch_handler(self, handler):
        self.switch.irq(trigger=Pin.IRQ_FALLING | Pin.IRQ_RISING, handler=handler)
