import serial

# Open the serial port
ser = serial.Serial('COM3', 9600)

# Read the file and send its contents
with open('README.md', 'rb') as file:
    file_content = file.read()
    ser.write(file_content)

try:
    while True:
        # Read a line of data from the Arduino
        data = ser.readline().decode('utf-8').strip()
        
        # Print the received data
        print(str(data))
        
except KeyboardInterrupt:
    # Close the serial port when the script is interrupted
    ser.close()
    print("Serial port closed.")


