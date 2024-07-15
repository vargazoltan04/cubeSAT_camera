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

#cam.test_pattern = OV7670_TEST_PATTERN_COLOR_BAR_FADE

#buf = bytearray(2 * cam.width * cam.height)
#width = cam.width

com = comm.Communication('$', '#', "COM6", 9600)
interp = interpreter.interpreter('CAM', com) #Ez maga az interpreter osztály, paraméternek az eszköz nevét, meg 1 kommunikációs objektumot vár

while True:
    input = com.wait_for_response()
    print("input: " + str(input))
    interp.execute_command(input) #Átadja neki magát az üzenetet, megnézi hogy érvényes üzenet-e, ha igen lefuttatja amit le kell



        


