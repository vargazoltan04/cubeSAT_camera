import binascii
import usb_cdc
import utils

class Communication:
    def __init__(self, start, end, port, baud):
        self.start = start
        self.end = end
        self.ser = usb_cdc.data
    
    def build_packet(self, content):
        start_bytes = bytes(self.start, 'ascii')
        end_bytes = bytes(self.end, 'ascii')
        content_hex = binascii.hexlify(content)

        checksum = utils.calc_checksum(self.start, content, self.end)
        carriage_return_bytes = bytes("\r\n", 'ascii')

        return start_bytes + content_hex + end_bytes + checksum + carriage_return_bytes

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


