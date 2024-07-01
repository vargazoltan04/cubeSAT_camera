#import base64 as b64
import serial

class Communication:
    def __init__(self, start, end, port, baud):
        self.start = start
        self.end = end
        self.ser = serial.Serial('COM6', 115200, timeout=3)
        
    def build_packet(self, content):
        #return self.start + str(b64.b64encode(bytes(content, 'ascii')))[2:-1] + self.end + str(0) + '*' + str(12345) + '\r' + '\n'
        return bytes(self.start, 'ascii') + content + bytes(self.end + str(0) + '*' + str(12345) + '\r' + '\n', 'ascii')

    def send_packet(self, packet):
        print("Sent: " + str(packet))
        self.ser.write(packet)

    def wait_for_response(self):
        packet = bytes()
        while True:
            packet += self.ser.read(1)
            if bytes("\r\n", 'ascii') in packet:
                break

        return packet

    def calc_checksum(self):
        return 12345

