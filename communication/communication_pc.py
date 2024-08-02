import binascii
import serial
from . import utils

class Communication:
    def __init__(self, start, end, port, baud):
        self.start = start
        self.end = end
        self.ser = serial.Serial('COM6', 115200, timeout=3)
        self.log_file = open("log/log.txt", "w")
        
    def build_packet(self, content):
        content_bytes = bytes(self.start, 'ascii') + content + bytes(self.end, 'ascii')
        return content_bytes + utils.calc_checksum(content_bytes) + bytes("\r\n", 'ascii')

    def send_packet(self, packet:bytes):
        print("------------------------ \r\n Sent: " + packet.decode('ascii'))
        self.log_file.write("------------------------ \r\n Sent: " + packet.decode('ascii'))
        self.ser.write(packet)

    def wait_for_response(self):
        packet = bytes()
        while True:
            packet += self.ser.read(1)
            carriage_return = bytes("\r\n", "ascii")
            if carriage_return in packet:
                break

        print("Received: " + packet.decode('ascii'))
        self.log_file.write("Received: " + packet.decode('ascii'))
        return packet

    def calc_checksum(self):
        return 12345


