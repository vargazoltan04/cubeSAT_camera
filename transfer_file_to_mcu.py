# import serial COMMENTED OUT FOR TESTING
from PIL import Image
import sys

'''

# Open the serial port
# ser = serial.Serial('COM3', 115200) COMMENTED OUT FOR TESTING
imageSize = 12
data = Image.open('cubeSAT_camera\earth.bmp')
saved_mode = data.mode
saved_size = data.size
# Read the file and send its contents
bytesOfImg = data.tobytes()
# ser.write(data.tobytes()[0:57600:1]) COMMENTED OUT FOR TESTING
i = 0    
index = 57600
try:
    while i < imageSize:
        tempData = bytesOfImg[index-57600:index]
            
        title = f"{i}.bmp"
        
        
        im = Image.frombytes('RGB', (480, 40), tempData)
        im.save(title, format='BMP')
        
        i = i + 1
        # ser.write(data.tobytes()[index:index+57600:1]) COMMENTED OUT FOR TESTING
        index += 57600


        
except KeyboardInterrupt:
    # Close the serial port when the script is interrupted
   # ser.close() COMMENTED OUT FOR TESTING
    print("Serial port closed.")

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