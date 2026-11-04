#include <Arduino.h>
void setup() {
  Serial.begin(115200);
  Serial.setTimeout(200); // teaching test only; no motors attached
  Serial.println("Ready. Send PING with Newline.");
}
void loop() {
  if (Serial.available()) {
    String message = Serial.readStringUntil(char(10));
    message.trim();
    if (message == "PING") Serial.println("PONG");
    else Serial.println("Type PING in capitals.");
  }
}
