# SPDX-FileCopyrightText: 2017 Scott Shawcroft, written for Adafruit Industries
# SPDX-FileCopyrightText: Copyright (c) 2021 Jeff Epler for Adafruit Industries
#
# SPDX-License-Identifier: Unlicense

"""Capture an image from the camera and display it as ASCII art.

The camera is placed in YUV mode, so the top 8 bits of each color
value can be treated as "greyscale".

It's important that you use a terminal program that can interpret
"ANSI" escape sequences.  The demo uses them to "paint" each frame
on top of the prevous one, rather than scrolling.

Remember to take the lens cap off, or un-comment the line setting
the test pattern!
"""

import sys
import time

import digitalio
import busio
import board
import usb_cdc

from adafruit_ov7670 import *
from lib import communication as comm
from lib import interpreter
# Ensure the camera is shut down, so that it releases the SDA/SCL lines,
# then create the configuration I2C bus

with digitalio.DigitalInOut(board.GP14) as shutdown:
    shutdown.switch_to_output(True)
    time.sleep(0.001)
    bus = busio.I2C(board.GP1, board.GP0)

cam = OV7670(
    bus,
    data_pins = [
            board.GP6,
            board.GP7,
            board.GP8,
            board.GP9,
            board.GP10,
            board.GP11,
            board.GP12,
            board.GP13
        ],
    clock=board.GP20,
    vsync=board.GP18,
    href=board.GP19,
    mclk=board.GP21,
    shutdown=board.GP14,
    reset=board.GP15,
)
cam.size = OV7670_SIZE_DIV2
cam.colorspace = OV7670_COLOR_RGB
#print(cam.colorspace)
cam.flip_y = True
#cam.test_pattern = OV7670_TEST_PATTERN_COLOR_BAR_FADE

#buf = bytearray(2 * cam.width * cam.height)
#width = cam.width

com = comm.Communication('$', '#', "COM6", 9600)

while True:
    input = com.wait_for_response()
    
    interp = interpreter.interpreter('CAM', com) #Ez maga az interpreter osztály, paraméternek az eszköz nevét, meg 1 kommunikációs objektumot vár
    interp.execute_command(input) #Átadja neki magát az üzenetet, megnézi hogy érvényes üzenet-e, ha igen lefuttatja amit le kell



        


