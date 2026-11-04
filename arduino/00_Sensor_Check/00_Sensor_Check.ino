#include <Arduino.h>
const int LEFT_IR=34, FRONT_IR=35, RIGHT_IR=39;
unsigned long previous=0;
void setup() {
  Serial.begin(115200);
  pinMode(LEFT_IR,INPUT); pinMode(FRONT_IR,INPUT); pinMode(RIGHT_IR,INPUT);
  Serial.println("Raw states: 0=LOW, 1=HIGH. Motors must stay OFF.");
}
void loop() {
  if (millis()-previous>=200) {
    previous=millis();
    Serial.print("Left="); Serial.print(digitalRead(LEFT_IR));
    Serial.print(" Front="); Serial.print(digitalRead(FRONT_IR));
    Serial.print(" Right="); Serial.println(digitalRead(RIGHT_IR));
  }
}
