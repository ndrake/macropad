
"""
Banana game clicker
Sends left-clicks manually (every key sends left click) or automatically
"""
from rainbowio import colorwheel
from adafruit_macropad import MacroPad

import time
import random

macropad = MacroPad()

CHANGE_TIME_SEC = .5
RANDOM_TIME_SEC = 1
BUTTON_FLASH_TIME = .2

last_change = time.time()
last_click = time.time()

DO_CLICKING=False
RANDOMIZE_WAIT=False

text_lines = macropad.display_text(title="Nana Clicker")
text_lines[1].text = "Active? {}".format(DO_CLICKING)
text_lines[2].text = "Random Sleep? {}".format(RANDOMIZE_WAIT)

while True:
    key_event = macropad.keys.events.get()

    now = time.time()
    if now - last_change > (RANDOM_TIME_SEC if RANDOMIZE_WAIT else CHANGE_TIME_SEC):
        last_change = now
        RANDOM_TIME_SEC = random.randint(1,15)
        if DO_CLICKING:
            macropad.mouse.click(macropad.Mouse.LEFT_BUTTON)
            macropad.pixels[1] = colorwheel(
                int(255 / 12) * (1 if not RANDOMIZE_WAIT else 5)
            )
        else:
            macropad.pixels.fill((0, 0, 0))

    if now - last_click > BUTTON_FLASH_TIME:
        macropad.pixels.fill((0, 0, 0))

    if key_event:
        if key_event.pressed:
            macropad.pixels[key_event.key_number] = colorwheel(
                int(255 / 12) * key_event.key_number
            )
            macropad.mouse.click(macropad.Mouse.LEFT_BUTTON)

            # Toggle random wait with key 0
            if key_event.key_number == 0:
                RANDOMIZE_WAIT = not RANDOMIZE_WAIT
                text_lines[2].text = "Random Sleep? {}".format(RANDOMIZE_WAIT)
        else:
            macropad.pixels.fill((0, 0, 0))

    macropad.encoder_switch_debounced.update()

    # Click encoder toggles if we're sending clicks or not
    if macropad.encoder_switch_debounced.pressed:
        DO_CLICKING = not DO_CLICKING
        text_lines[1].text = "Active? {}".format(DO_CLICKING)

    
    text_lines.show()
