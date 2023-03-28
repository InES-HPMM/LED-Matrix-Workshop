from zhaw_led_matrix import Button

# Button initialisieren
btn = Button()

# Verhalten bei einem button Ereignis festlegen
def left(_):
    print(".")
btn.set_left_handler(left)

# Werte vom Joystick & Schiebeschalter einlesen
btn.up.value()
btn.down.value()
btn.left.value()
btn.right.value()
btn.center.value()
btn.switch.value()
