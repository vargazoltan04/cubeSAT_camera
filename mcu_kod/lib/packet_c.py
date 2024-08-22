
import utils
class packet:
    def __init__(self, packet: bytes):
        #Azért így van megvalósítva, hogy kitörölgeti az elejéről, mert könnyebb mint splitelni, mivel bytes tömb, nem string
        #A packet-nak a 0. byteját átalakítja asciivá, és az lesz a start_char (csomag első karaktere)
        self.start_char = packet.decode('ascii')[0]
        packet = packet[1:]

        self.content = packet.split(bytes('%', 'ascii'))[0]
        self.end_char = '%'

        #Kitörli az elejéről a contentet, illetve az end_char-t
        packet = packet[len(self.content):]
        packet = packet[1:]

        self.checksum = packet[:-len(bytes('\r\n', 'ascii'))]

        #print(self.start_char)
        #print(self.content)
        #print(self.end_char)
        #print(self.checksum)

    def checksum_valid(self):
        content_bytes = bytes(self.start_char, 'ascii') + self.content + bytes(self.end_char, 'ascii')
        checksum_hex = utils.calc_checksum(content_bytes)
        
        if checksum_hex.decode('ascii') == self.checksum.decode('ascii'):
            return True
        else:
            return False

