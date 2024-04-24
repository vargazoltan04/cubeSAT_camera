# import serial COMMENTED OUT FOR TESTING
from PIL import Image
import sys
import cv2
import numpy as np

# Open the serial port
ser = serial.Serial('COM6', 9600, timeout=5)
j=0
vsync_counter = 0
while True: 

    vsync_buf = ser.read(1)
    #print(int.from_bytes(vsync_buf))
    if int.from_bytes(vsync_buf) == 0:
        vsync_counter += 1
    else:
        vsync_counter = 0

    if vsync_counter == 640:
        tempData = bytearray(ser.read(320*240*2))
        for i in range(0, 320*240*2,2):
            tempData[i], tempData[i+1] = tempData[i+1], tempData[i]
        #print(str(tempData))

        rgb565_array = np.frombuffer(tempData, np.uint16).reshape(240, 320)
        print(len(rgb565_array))
        #img_np = cv2.cvtColor(nparr, cv2.COLOR_R)
        # Convert RGB565 to RGB888 (standard RGB)
        rgb888_array = np.zeros((rgb565_array.shape[0], rgb565_array.shape[1], 3), dtype=np.uint8)
        rgb888_array[:,:,0] = ((rgb565_array & 0b1111_1000_0000_0000) >> 8)  # Red component
        rgb888_array[:,:,1] = ((rgb565_array & 0b0000_0111_1110_0000) >> 3)  # Green component
        rgb888_array[:,:,2] = ((rgb565_array & 0b0000_0000_0001_1111) << 3)  # Blue component

        #rgb888_array[:,:,2] = rgb888_array[:,:,2] + 30
        #rgb888_array[:,:,1] = rgb888_array[:,:,1].mean(axis=(0,1))
        #rgb888_array[:,:,2] = rgb888_array[:,:,2].mean(axis=(0,1))
        
        # Convert numpy array to PIL Image
        pil_image = Image.fromarray(rgb888_array, 'RGB')

        # Save PIL Image as PNG
        pil_image.save(f'kepek/output{j}.png')
        j += 1
        
        if j == 20:
            break
        #print(type(img_np))

'''

try:
    j = 0
    bytesOfImg = bytes()
    print("Elindult megint")
    while j < 12:
    
       
        title = f"{j}.bmp"
        print(title)
        data = Image.open(title)
    
        saved_mode = data.mode
        saved_size = data.size
        bytesOfImg += (data.tobytes())
        j+=1
    
    im = Image.frombytes('RGB',(480,480), bytesOfImg)
    name = f"pieced_together.bmp"
    im.save(name, format='BMP')

except Exception as e:
    print(repr(e))
    '''