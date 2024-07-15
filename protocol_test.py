import binascii
from PIL import Image
import numpy as np
from communication import communication_pc as comm

com = comm.Communication('$', '#', "COM6", 9600)


com.send_packet(com.build_packet(bytes("CAM,TP",'ascii')))
print(com.wait_for_response())

buf = bytes()
for i in range(4800):
    print(str(i) + ": ")
    command = com.build_packet(bytes("CAM,SP," + str(i), 'ascii'))
    com.send_packet(command)
    
    packet = com.wait_for_response()
    packet_str = str(packet)[2:-1]
    #source_device = packet[1:4]
    
    packet_body_hex: str = ""
    for c in packet_str[1::]:
        if c == '#':
            break
        else:
            packet_body_hex += str(c)
            

    packet_body = binascii.unhexlify(packet_body_hex)
    buf += packet_body[4:]
buf = bytearray(buf)
print(len(buf))

com.log_file.close()


#innen csak megjelenít

for i in range(0, len(buf),2):
    buf[i], buf[i+1] = buf[i+1], buf[i]

rgb565_array = np.frombuffer(buf, np.uint16).reshape(240, 320)
# Convert RGB565 to RGB888 (standard RGB)
rgb888_array = np.zeros((rgb565_array.shape[0], rgb565_array.shape[1], 3), dtype=np.uint8)
rgb888_array[:,:,0] = ((rgb565_array & 0b1111_1000_0000_0000) >> 8)  # Red component
rgb888_array[:,:,1] = ((rgb565_array & 0b0000_0111_1110_0000) >> 3)  # Green component
rgb888_array[:,:,2] = ((rgb565_array & 0b0000_0000_0001_1111) << 3)  # Blue component

# Convert numpy array to PIL Image
pil_image = Image.fromarray(rgb888_array, 'RGB')

# Save PIL Image as PNG
pil_image.save(f'kepek3/output_test.png')
