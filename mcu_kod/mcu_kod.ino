#include <Wire.h>

#define SDA_PIN 20 // Change this to the desired SDA pin
#define SCL_PIN 21 // Change this to the desired SCL pin

void setup() { 
  Wire.begin();  // Initialize I2C communication with custom pins
  Serial.begin(9600);  // Initialize serial communication
  while (!Serial);  // Wait for serial port to connect
  Serial.println("\nI2C Scanner");
}

void loop() {
  byte error, address;
  int devices = 0;

  Serial.println("Scanning...");

  for (address = 1; address < 127; address++) {
    // The i2c_scanner uses the return value of
    // the Write.endTransmisstion to see if
    // a device did acknowledge to the address.
    Wire.beginTransmission(address);
    error = Wire.endTransmission();

    if (error == 0) {
      Serial.print("I2C device found at address 0x");
      if (address < 16)
        Serial.print("0");
      Serial.print(address, HEX);
      Serial.println(" !");
      devices++;
    } else if (error == 4) {
      Serial.print("Unknown error at address 0x");
      if (address < 16)
        Serial.print("0");
      Serial.println(address, HEX);
    }
  }

  if (devices == 0)
    Serial.println("No I2C devices found\n");
  else
    Serial.println("Done\n");

  delay(5000);  // Wait 5 seconds for the next scan
}
