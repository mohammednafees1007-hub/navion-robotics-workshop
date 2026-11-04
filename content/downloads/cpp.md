# A little C/C++


Variables and constants

const int sensorPin = 34; // pin stays the same
int reading = 0;         // reading may change

A semicolon ends a statement. Braces group statements. A constant is a useful tuning label that prevents accidental changes while running.

Setup and loop

void setup() { pinMode(34, INPUT); Serial.begin(115200); }
void loop() {
  int reading = digitalRead(34);
  if (reading == LOW) { Serial.println("Detected"); }
  else { Serial.println("Clear"); }
}

pinMode selects input/output. digitalRead gets HIGH/LOW. digitalWrite sets an output. Never set an input-only sensor pin to output.

Functions and PWM

void stopRobot() { /* call the sketch motor function with 0, 0 */ }
// Core 3.x: ledcAttach(32, 1000, 8); then ledcWrite(32, 150);

A function groups one job. In the full sketches drive(left,right) takes signed speeds: positive forward, negative reverse, zero stop.

Timing and serial

delay(1000) pauses processing for a second. millis() measures elapsed time so the remote robot can keep checking for commands. Read one character with Serial.read() only after Serial.available(). F/B/L/R/S are characters, not words.


Check your understanding

Why is millis timing useful for a stop-command failsafe?
