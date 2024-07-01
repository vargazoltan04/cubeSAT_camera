#import base64 as b64
import serial

class Communication:
    def __init__(self, start, end, port, baud):
        self.start = start
        self.end = end
        self.ser = serial.Serial(port, baud, timeout=3)

    def build_packet(self, content):
        #return self.start + str(b64.b64encode(bytes(content, 'ascii')))[2:-1] + self.end + str(0) + '*' + str(12345) + '\r' + '\n'
        return self.start + content + self.end + str(0) + '*' + str(12345) + '\r' + '\n'

    def send_packet(self, packet):
        print('Sent: ' + str(bytes(packet, 'ascii')))
        self.ser.write(bytes(packet, 'ascii'))

    def wait_for_response(self):
        packet = bytes()
        while True:
            packet += self.ser.read()
            if bytes("\r\n", 'ascii') in packet:
                break

        print("Received: " + str(packet))
        return packet

    def calc_checksum(self):
        return 12345

