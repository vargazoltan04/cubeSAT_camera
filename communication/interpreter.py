import communication as comm
class interpreter:
    def __init__(self, this_device, com):
        self.this_device = this_device
        self.com: comm = com

    def execute_command(self, packet: str):
        source_device = packet[1::3]
        packet_body = ""
        for c in packet[3::]:
            if c == '#':
                break
            else:
                packet_body += c
        if packet_body.capitalize() == "STATUS":
            response = self.com.build_packet(source_device + "ACTIVE")
            self.com.send_packet(response)