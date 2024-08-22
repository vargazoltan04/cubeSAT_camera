import communication as comm
import digitalio
import busio
import board
import time
import binascii
import utils
import packet_c as pt

from adafruit_ov7670 import *

class interpreter:
    def __init__(self, this_device, com):
        self.this_device = this_device
        self.com: comm = com
        self.buf = bytearray(2*320*240)
        
        with digitalio.DigitalInOut(board.GP14) as shutdown:
            shutdown.switch_to_output(True)
            time.sleep(0.001)
            self.bus = busio.I2C(board.GP1, board.GP0)

        self.cam = OV7670(
            self.bus,
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
        self.cam.size = OV7670_SIZE_DIV2
        self.cam.colorspace = OV7670_COLOR_RGB
        self.cam.flip_y = True

    def execute_command(self, packet: pt.packet):
        if not packet.checksum_valid():
            return

        params = packet.content.decode('ascii').split(',')
        #print("params: " + str(params) + "\n")

        if params[0] != "CAM":
            return
        
        if params[1] == "STATUS":
            response = self.com.build_packet(bytes("OBC,ACTIVE",'ascii'))
            self.com.send_packet(response)
        if params[1] == "TP":
            self.cam.capture(self.buf)
            response = self.com.build_packet(bytes("OBC,ACK", 'ascii'))
            self.com.send_packet(response)
        elif params[1] == "SP":
            counter = int(params[2])
            lilbuf = self.buf[counter*25 : (counter + 1) * 25]
            response = self.com.build_packet(bytes("OBC,", 'ascii') + lilbuf)
            self.com.send_packet(response)


