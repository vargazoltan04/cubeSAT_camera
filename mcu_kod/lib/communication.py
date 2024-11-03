import binascii
#import usb_cdc
import utils
import packet_c as pt

class Communication:
    def __init__(self, start, end, port, baud):
        self.start = start
        self.end = end
        #self.ser = usb_cdc.data
    
    def build_packet(self, content):
        content_bytes = bytes(self.start, 'ascii') + binascii.hexlify(content) + bytes(self.end, 'ascii')
        return content_bytes + utils.calc_checksum(content_bytes) + bytes("\r\n", 'ascii')

    def send_packet(self, packet):
        self.ser.write(packet)

    def wait_for_response(self):
        packet = bytes()
        while True:
            packet += self.ser.read(1)
            carriage_return = bytes("\r\n", "ascii")
            if carriage_return in packet:
                break
        
        packet = pt.packet(packet)
        return packet
    
    def calc_checksum(self):
        pass


