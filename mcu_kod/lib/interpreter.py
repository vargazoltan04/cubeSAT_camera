import communication as comm
import digitalio
import busio
import board
import time
import binascii
import utils
import packet_c as pt
import espcamera
import sdcardio
#from adafruit_ov7670 import *

class interpreter:
    def __init__(self, this_device, com):
        self.this_device = this_device
        self.com: comm = com
        self.buf = bytearray(2*320*240)
        
        #with digitalio.DigitalInOut(board.GP14) as shutdown:
        #    shutdown.switch_to_output(True)
        #    time.sleep(0.001)
        #    self.bus = busio.I2C(board.GP1, board.GP0)
        
        self.cam = espcamera.Camera(
            data_pins = board.CAMERA_DATA,
            external_clock_pin = board.CAMERA_XCLK,
            pixel_clock_pin=board.CAMERA_PCLK,
            vsync_pin=board.CAMERA_VSYNC,
            href_pin=board.CAMERA_HREF,
            powerdown_pin=board.CAMERA_PWDN,
            reset_pin=None,
            i2c = board.I2C(),
            external_clock_frequency=20_000_000,
            pixel_format=espcamera.PixelFormat.JPEG,
            frame_size=espcamera.FrameSize.SVGA
        )
        
        self.SPI = busio.SPI()
        cs = board.SD_CS
        sdcard = sdcard.SDCard(spi, cs)
        vfs = storage.VfsFat(sdcard)
        storage.mount(vfs, "/sd")
        
    def test():
        buf = cam.take(1)
        with open("/sd/out.jpg", "w") as out:
            out.write(buf)
            
          
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
            buf = self.cam.take(1)
            response = self.com.build_packet(bytes("OBC,ACK", 'ascii'))
            self.com.send_packet(response)
        elif params[1] == "SP":
            counter = int(params[2])
            lilbuf = self.buf[counter*25 : (counter + 1) * 25]
            response = self.com.build_packet(bytes("OBC,", 'ascii') + lilbuf)
            self.com.send_packet(response)


