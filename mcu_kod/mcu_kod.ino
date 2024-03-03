#include <stdio.h> 
#include "Arduino.h"
//#include <opencv2/opencv.hpp>

using namespace std;

const uint16_t BUFFER_SIZE = 57600;
uint8_t buffer[BUFFER_SIZE];
void setup()
{
  Serial.begin(115200);
  digitalWrite(25, HIGH);
}

void loop()
{
  if (Serial.available() > 0)
  {
    int bytesRead = Serial.readBytes(buffer, BUFFER_SIZE);
    
    Serial.write(buffer, bytesRead);
  }
}
