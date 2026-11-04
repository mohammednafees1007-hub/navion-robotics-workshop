# Your first serial conversation


A tiny test sketch

void setup() { Serial.begin(115200); Serial.println("Ready"); }
void loop() {
  if (Serial.available()) {
    String s = Serial.readStringUntil('\n');
    s.trim();
    if (s == "PING") Serial.println("PONG");
  }
}

This short teaching test may wait for the serial timeout; it is not the nonblocking remote parser. Select Newline in Serial Monitor, type PING, and press Send. Matching spelling and capitals matter.

Record the result

Write the COM port, baud rate, sent text and received response. If text is scrambled, check 115200 baud. If nothing arrives, verify the port and upload, then reset the board. Do not connect motors for this exercise.

Teacher checks power isolation; lift wheels and keep battery off while uploading.

Open the .ino inside its same-named folder in Arduino IDE 2.x.

Select ESP32 Dev Module for the original WROOM-32, the correct USB COM port, then Verify and Upload.

Open Serial Monitor at 115200 baud. Record messages and close other applications using the port.

After upload, remove USB before restoring the assumed external supply. Test at low speed with teacher approval.


Check your understanding

What is the difference between the message you send and the response you receive?
