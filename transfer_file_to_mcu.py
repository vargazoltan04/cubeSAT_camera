import serial
from PIL import Image
import sys

# Open the serial port
ser = serial.Serial('COM3', 115200)

data = Image.open('earth.bmp')
saved_mode = data.mode
saved_size = data.size
# Read the file and send its contents

ser.write(data.tobytes()[0:57600:1])
i = 0    
index = 57600
try:
    while i < 12:
        tempData = ser.read(57600) 
            
        title = f"{i}.bmp"
        
        
        im = Image.frombytes('RGB', (480, 40), tempData)
        im.save(title, format='BMP')
        
        i = i + 1
        ser.write(data.tobytes()[index:index+57600:1])
        index += 57600


        
except KeyboardInterrupt:
    # Close the serial port when the script is interrupted
    ser.close()
    print("Serial port closed.")


