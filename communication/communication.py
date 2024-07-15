import binascii
import usb_cdc

class Communication:
    def __init__(self, start, end, port, baud):
        self.start = start
        self.end = end
        self.ser = usb_cdc.data
        
    def build_packet(self, content):
        #return self.start + str(b64.b64encode(bytes(content, 'ascii')))[2:-1] + self.end + str(0) + '*' + str(12345) + '\r' + '\n'
        return bytes(self.start, 'ascii') + binascii.hexlify(content) + bytes(self.end + str(0) + '*' + str(12345) + '\r' + '\n', 'ascii')

    def send_packet(self, packet):
        self.ser.write(packet)

    def wait_for_response(self):
        packet = bytes()
        while True:
            packet += self.ser.read(1)
            carriage_return = bytes("\r\n", "ascii")
            if carriage_return in packet:
                break
            
        return packet

    def calc_checksum(self):
        return 12345


