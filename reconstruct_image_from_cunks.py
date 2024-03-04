from PIL import Image
import sys



try:
    j = 0
    bytesOfImg = bytes()
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
