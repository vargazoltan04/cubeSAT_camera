import sys
import time
import gc

import digitalio
import busio
import board
import usb_cdc

from adafruit_ov7670 import *
from lib import communication as comm
from lib import interpreter

com = comm.Communication('#', '%', "COM6", 9600)
interp = interpreter.interpreter('CAM', com)

gc.enable()
print(gc.mem_free())
print(gc.mem_alloc())
while True:
    input = com.wait_for_response()
    #print("input: " + str(input))
    interp.execute_command(input)




        


