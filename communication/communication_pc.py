import binascii
import serial

class Communication:
    def __init__(self, start, end, port, baud):
        self.start = start
        self.end = end
        self.ser = serial.Serial('COM6', 115200, timeout=3)
        self.log_file = open("log/log.txt", "w")
        
    def build_packet(self, content):
        #return self.start + str(b64.b64encode(bytes(content, 'ascii')))[2:-1] + self.end + str(0) + '*' + str(12345) + '\r' + '\n'
        start_bytes = bytes(self.start, 'ascii')
        end_bytes = bytes(self.end, 'ascii')
        checksum = sum(start_bytes + content + end_bytes) % 256
        checksum_bytes = checksum.to_bytes(1, 'big')
        checksum_hex = binascii.hexlify(checksum_bytes)
        carriage_return_bytes = bytes("\r\n", 'ascii')
        
        return start_bytes + content + end_bytes + checksum_hex + carriage_return_bytes

    def send_packet(self, packet):
        print("Sent: " + str(packet))
        self.log_file.write("Sent: " + str(packet) + "\n")
        self.ser.write(packet)

    def wait_for_response(self):
        packet = bytes()
        while True:
            packet += self.ser.read(1)
            carriage_return = bytes("\r\n", "ascii")
            if carriage_return in packet:
                break

        print(str(len(packet)) + ": " + str(packet))
        print("Received: " + str(packet) + "\n\n")
        self.log_file.write("Received: " + str(packet) + "\n\n")
        return packet

    def calc_checksum(self):
        return 12345


