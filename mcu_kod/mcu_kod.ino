#include <stdio.h> 

const uint16_t BUFFER_SIZE = 1000;
uint8_t buffer[BUFFER_SIZE];
void setup()
{
  pinMode(25, OUTPUT);
  Serial.begin(9600);
  digitalWrite(25, HIGH);
}

void loop()
{
  if (Serial.available() > 0)
  {
    int bytesRead = Serial.readBytes(buffer, 1000);

    processSerialData(bytesRead);

    Serial.print("I received: ");
    Serial.println(bytesRead);
  }
}

void processSerialData(int length) {
  Serial.println("");
  for (int i = 0; i < length; i++) {
    char temp = buffer[i];
    Serial.print(temp);
  }
  Serial.println("");
  
}
