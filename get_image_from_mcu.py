import serial
from PIL import Image
import sys
import cv2
import numpy as np
import time

# Open the serial port
ser = serial.Serial('COM6', 115200, timeout=3)
image_counter = 0
vsync_counter = 0

buf_send_next_im = bytearray(320*2)
for i in range(0, len(buf_send_next_im)):
    buf_send_next_im[i] == 255
def send_next_im():
    ser.write(buf_send_next_im)

#The camera sends an image if it finds 640 white pixels. 
send_next_im()
while True: 
    while vsync_counter < 640:
        vsync_buf = ser.read(1)
        if int.from_bytes(vsync_buf) == 0:
            vsync_counter += 1
        else:
            vsync_counter = 0

    print(vsync_counter)
    tempData = bytearray(ser.read(320*240*2))
    print(str(image_counter) + ": " + str(len(tempData)))
    for i in range(0, 320*240*2,2):
        tempData[i], tempData[i+1] = tempData[i+1], tempData[i]

    rgb565_array = np.frombuffer(tempData, np.uint16).reshape(240, 320)
    print(len(rgb565_array))
    # Convert RGB565 to RGB888 (standard RGB)
    rgb888_array = np.zeros((rgb565_array.shape[0], rgb565_array.shape[1], 3), dtype=np.uint8)
    rgb888_array[:,:,0] = ((rgb565_array & 0b1111_1000_0000_0000) >> 8)  # Red component
    rgb888_array[:,:,1] = ((rgb565_array & 0b0000_0111_1110_0000) >> 3)  # Green component
    rgb888_array[:,:,2] = ((rgb565_array & 0b0000_0000_0001_1111) << 3)  # Blue component
    
    # Convert numpy array to PIL Image
    pil_image = Image.fromarray(rgb888_array, 'RGB')

    # Save PIL Image as PNG
    pil_image.save(f'kepek3/output{image_counter}.png')
    image_counter += 1
    vsync_counter = 0

    if image_counter == 200:
        break

    if ser.in_waiting == 0:
        send_next_im()

