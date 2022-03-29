import board
import neopixel

from adafruit_led_animation.animation.comet import Comet
from adafruit_led_animation.animation.rainbowcomet import RainbowComet
from adafruit_led_animation.animation.rainbowchase import RainbowChase
from adafruit_led_animation.animation.sparklepulse import SparklePulse
from adafruit_led_animation.animation.sparkle import Sparkle
from adafruit_led_animation.animation.rainbowsparkle import RainbowSparkle
from adafruit_led_animation.animation.chase import Chase
from adafruit_led_animation.animation.pulse import Pulse
from adafruit_led_animation.animation.rainbow import Rainbow
from adafruit_led_animation.animation.solid import Solid
from adafruit_led_animation.animation.colorcycle import ColorCycle
from adafruit_led_animation.animation.customcolorchase import CustomColorChase

from adafruit_led_animation.sequence import AnimationSequence
from adafruit_led_animation import helper
from adafruit_led_animation.color import AQUA, PURPLE, JADE, AMBER, BLUE, CYAN, GOLD, GREEN, MAGENTA, OLD_LACE, ORANGE, PINK, TEAL, WHITE, YELLOW
from adafruit_macropad import MacroPad
from adafruit_hid.consumer_control_code import ConsumerControlCode

from random import randint, choice
import time

macropad = MacroPad()
macropad.pixels.brightness = 0.2

colors = [AQUA, PURPLE, JADE, AMBER, BLUE, CYAN, GOLD, GREEN, MAGENTA, OLD_LACE, ORANGE, PINK, TEAL, WHITE, YELLOW]
def get_rand_color():
    return choice(colors)


def get_random_comet():
    return Comet(macropad.pixels, speed=0.1, color=get_rand_color(), tail_length=4, bounce=True)

def get_random_sparkle():
    return Sparkle(macropad.pixels, speed=0.2, color=get_rand_color(), num_sparkles=7)

def get_random_chase():
    return Chase(macropad.pixels, speed=0.4, color=get_rand_color(), size=2, spacing=5)

def get_random_pulse():
    return Pulse(macropad.pixels, speed=0.1, color=get_rand_color(), period=3)

def get_random_solid():
    return Solid(macropad.pixels, color=get_rand_color())

def get_random_sparkle_pulse():
    return SparklePulse(macropad.pixels, speed=0.1, period=3, color=get_rand_color())

def get_random_color_cycle():
    c = []
    for i in range(0, 4):
        c.append(get_rand_color())
    return ColorCycle(macropad.pixels, speed=0.4, colors=c)

def get_random_custom_color_chase():
    c = []
    for i in range(0, 3):
        c.append(get_rand_color())
    return  CustomColorChase(macropad.pixels, speed=0.1, size=2, spacing=3, colors=c)

rainbow_chase_v = RainbowChase(macropad.pixels, speed=0.1, size=3, spacing=2, step=8)
rainbow_comet_v = RainbowComet(macropad.pixels, speed=0.1, tail_length=7, bounce=True)
rainbow_v = Rainbow(macropad.pixels, speed=0.1, period=2)
sparkle = RainbowSparkle(macropad.pixels, speed=0.5, num_sparkles=5)

animations = AnimationSequence(
    rainbow_v,
    rainbow_comet_v,
    sparkle,
    rainbow_chase_v,
    get_random_comet(),
    get_random_chase(),
    get_random_pulse(),
    get_random_sparkle(),
    #get_random_solid(),
    get_random_sparkle_pulse(),
    get_random_color_cycle(),
    get_random_custom_color_chase(),
    advance_interval=60,
    auto_clear = True,
    auto_reset = True,
    random_order = True
)

curr_img = randint(0,150)
encoder_last_pos = 0

import displayio

def show_image(file_name):
    img = displayio.OnDiskBitmap(file_name.format(curr_img+1))
    macropad.display_image(file_name, (int((64-(img.width/2))),int((32-(img.height/2)))))

show_image("pmon/{}.bmp".format(curr_img+1))

CHANGE_TIME_SEC = 3
last_change = time.time()

SCROLL_AMOUNT = 100
MOUSE_AMOUNT = 50
doScroll = False
mouseVert = False
mouseHor = False

while True:

    animations.animate()
    now = time.time()

    if now - last_change > CHANGE_TIME_SEC:
        last_change = now

    key_event = macropad.keys.events.get()
    if key_event:
        if key_event.pressed:
            if key_event.key_number == 0:
                curr_img = (curr_img - 1) % 150
                show_image("pmon/{}.bmp".format(curr_img+1))
            if key_event.key_number == 1:
                curr_img = randint(1,151)
                show_image("pmon/{}.bmp".format(curr_img+1))
            if key_event.key_number == 2:
                curr_img = (curr_img + 1) % 150
                show_image("pmon/{}.bmp".format(curr_img+1))
            if key_event.key_number == 4:
                animations.random()
            if key_event.key_number == 6:
                mouseVert = True
            if key_event.key_number == 7:
                doScroll = True
            if key_event.key_number == 8:
                mouseHor = True
            if key_event.key_number == 9:
                macropad.consumer_control.send(ConsumerControlCode.SCAN_PREVIOUS_TRACK)
            elif key_event.key_number == 10:
                macropad.consumer_control.send(ConsumerControlCode.PLAY_PAUSE)
            elif key_event.key_number == 11:
                macropad.consumer_control.send(ConsumerControlCode.SCAN_NEXT_TRACK)
        if key_event.released:
            if key_event.key_number == 6:
                mouseVert = False
            if key_event.key_number == 7:
                doScroll = False
            if key_event.key_number == 8:
                mouseHor = False

    ##text_lines[1].text = "Rotary encoder {}".format(macropad.encoder)
    ##text_lines[2].text = "Encoder switch: {}".format(macropad.encoder_switch)

    current_pos = macropad.encoder
    if macropad.encoder > encoder_last_pos:
        if doScroll:
            macropad.mouse.move(wheel=-SCROLL_AMOUNT)
        elif mouseVert:
            macropad.mouse.move(y=MOUSE_AMOUNT)
        elif mouseHor:
            macropad.mouse.move(x=MOUSE_AMOUNT)
        else:
            macropad.consumer_control.send(ConsumerControlCode.VOLUME_INCREMENT)
        encoder_last_pos = current_pos
    elif macropad.encoder < encoder_last_pos:
        if doScroll:
            macropad.mouse.move(wheel=SCROLL_AMOUNT)
        elif mouseVert:
            macropad.mouse.move(y=-MOUSE_AMOUNT)
        elif mouseHor:
            macropad.mouse.move(x=-MOUSE_AMOUNT)
        else:
            macropad.consumer_control.send(ConsumerControlCode.VOLUME_DECREMENT)
        encoder_last_pos = current_pos

    macropad.encoder_switch_debounced.update()  # check the knob switch for press or release
    if macropad.encoder_switch_debounced.pressed:
        macropad.consumer_control.send(ConsumerControlCode.MUTE)
    ##text_lines.show()
