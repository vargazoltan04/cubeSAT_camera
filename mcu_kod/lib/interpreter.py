import communication as comm
import digitalio
import busio
import board
import time
import binascii
import utils

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

    def execute_command(self, packet: bytes):
        #source_device = packet[1::3]
        packet_str = packet.decode('ascii')

        checksum_received = packet_str.split('%')[1][0:2]
        #print("checksum_received: " + checksum_received)

        start_char = ""
        end_char = ""
        packet_body = ""

        for c in packet_str[0::]:
            if c == '$':
                start_char = '$'
                continue
            if c == '%':
                end_char = '%'
                break
            else:
                packet_body += str(c)
        

        content_bytes = bytes(start_char, 'ascii') + bytes(packet_body, 'ascii') + bytes(end_char, 'ascii')
        checksum_hex = utils.calc_checksum(content_bytes)
        print(checksum_hex.decode('ascii') == checksum_received)
        if checksum_hex.decode('ascii') != checksum_received:
            return

        params = packet_body.split(',')
        print("params: " + str(params) + "\n")
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


