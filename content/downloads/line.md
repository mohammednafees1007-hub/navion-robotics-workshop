# 02 · Follow the line


Aim

Two downward sensors, one careful decision at a time. Explain the input, decision and motor output to a partner.

Equipment

Use the same kit and chassis. Remote needs the Windows laptop; line uses two IR modules; avoidance uses all three. No phone, ultrasonic sensor, servo or Wi-Fi.

Learn the concept

Make a black line about 25.4 mm wide on a white matte surface. Place sensors on either side: sensor — line — sensor. Their exact spacing and height need prototype calibration. With the current arrangement both white usually means centered, but can also mean completely lost. Two digital readings cannot distinguish those cases.

Left blackRight blackDecision

NoNoForward 700 ms since last detection, then bounded last-turn search; stop if unrecovered

YesNoTurn left

NoYesTurn right

YesYesStop: crossing or alignment needs inspection

Safe-search tradeoff: even a long straight can trigger a search. This is deliberately conservative; do not describe it as reliable lost-line detection. Autonomous session ends after 60 seconds.

Assembly / mounting

Turn off power before moving modules. Secure mounts and keep wires clear of wheels. Use the assembly lesson and inspect fasteners with your teacher.

Wiring table and diagram

FunctionGPIONote

IN125L298N direction

IN226L298N direction

IN327L298N direction

IN414L298N direction

ENA32Motor PWM, remove enable jumper

ENB33Motor PWM, remove enable jumper

LEFT_IR34Driven 3.3 V digital input

FRONT_IR35Driven 3.3 V digital input

RIGHT_IR39Driven 3.3 V digital input

Map is provisional; read Power & wiring before connecting.

Algorithm and flowchart

Read sensors → apply the decision table above → update movement state → repeat until the bounded stop.

Code download
Download 02_Line_Follower.ino
Understand the code

initRobot() sets motor outputs low before attaching PWM. drive() maps signed speeds to wheel directions. oneMotor() briefly clears PWM before reversing. Top-level constants keep the pin map, inversion and duty editable.

detected() converts the calibrated active level to a meaning. millis() controls a bounded session. State variables remember the previous turn or current reverse/turn phase so the loop stays responsive.
Read the complete sketchCopy code
#include <Arduino.h>
// PROVISIONAL map: verify actual 30-pin WROOM-32 board and 3.3 V sensors.
const int IN1=25, IN2=26, IN3=27, IN4=14, ENA=32, ENB=33;
const int LEFT_IR=34, FRONT_IR=35, RIGHT_IR=39;
const int DETECTED_LEVEL=LOW; // calibrate against real surfaces
const bool INVERT_LEFT=false, INVERT_RIGHT=false;
const int SPEED=145; // 0..255 duty, not RPM
void oneMotor(int a,int b,int en,int value,bool invert) {
  if(invert) value=-value;
  ledcWrite(en,0); // remove drive while changing direction
  digitalWrite(a,value>0); digitalWrite(b,value<0);
  ledcWrite(en,constrain(abs(value),0,255));
}
void drive(int left,int right) {
  oneMotor(IN1,IN2,ENA,left,INVERT_LEFT);
  oneMotor(IN3,IN4,ENB,right,INVERT_RIGHT);
}
void initRobot() {
  Serial.begin(115200);
  for(int p: {IN1,IN2,IN3,IN4,ENA,ENB}) { pinMode(p,OUTPUT); digitalWrite(p,LOW); }
  bool okL=ledcAttach(ENA,1000,8), okR=ledcAttach(ENB,1000,8);
  if(!okL || !okR) { Serial.println("PWM init failed; stopped"); while(true) delay(100); }
  drive(0,0);
  pinMode(LEFT_IR,INPUT); pinMode(FRONT_IR,INPUT); pinMode(RIGHT_IR,INPUT);
}
bool detected(int pin) { return digitalRead(pin)==DETECTED_LEVEL; }

const unsigned long SEARCH_MS=1500;
const unsigned long SESSION_MS=60000; // stop after one minute; reset after teacher check
unsigned long started=0,searchStart=0;
bool searching=false,halted=false;
int lastTurn=-1; // -1 left, +1 right
void setup() { initRobot(); started=millis(); Serial.println("Line mode: reset starts 60 s session"); }
void loop() {
  if(halted || millis()-started>=SESSION_MS) { drive(0,0);halted=true;return; }
  bool left=detected(LEFT_IR), right=detected(RIGHT_IR);
  // Sensor -- 25.4 mm black line -- sensor: both white is normally centered.
  if(left && right) { drive(0,0);halted=true;Serial.println("Both black: stop and inspect crossing");return; }
  if(left || right) {
    searching=false;lastTurn=left?-1:1;
    drive(left?-SPEED:SPEED,left?SPEED:-SPEED);return;
  }
  // Both white is ambiguous: centered or lost. Forward only for a bounded interval.
  if(!searching) { searching=true;searchStart=millis(); }
  unsigned long elapsed=millis()-searchStart;
  if(elapsed<700) drive(SPEED,SPEED);
  else if(elapsed<700+SEARCH_MS) drive(lastTurn<0?-SPEED:SPEED,lastTurn<0?SPEED:-SPEED);
  else { drive(0,0);halted=true;Serial.println("Search expired: reposition and reset"); }
}


Upload steps

Teacher checks power isolation; lift wheels and keep battery off while uploading.

Open the .ino inside its same-named folder in Arduino IDE 2.x.

Select ESP32 Dev Module for the original WROOM-32, the correct USB COM port, then Verify and Upload.

Open Serial Monitor at 115200 baud. Record messages and close other applications using the port.

After upload, remove USB before restoring the assumed external supply. Test at low speed with teacher approval.

Run and observe

Start with wheels lifted. Test stop behavior first, then forward direction. Place on the floor only in a supervised clear area. Record input, expected action and observed action. Stop if a motor stalls, wiring heats or the ESP32 resets.

Calibration

With wheels raised, move each sensor over black and white and observe its indicator; measure its digital level with a teacher if necessary. Set DETECTED_LEVEL to LOW only if LOW means black after calibration. Keep lighting constant. Use just GPIO34 and GPIO39; the third module is not needed. Start with a short curve and a clear test area. Reposition and reset after the search timeout.

Troubleshooting

Reversed motor: switch the matching INVERT constant. No movement: check enable jumpers, common ground and starting duty. Unexpected sensor state: check calibration and 3.3 V compatibility. Brownout: teacher checks the assumed power regulator under load.

Student challenge

Change SEARCH_MS. Explain why an unlimited search would be a poor choice.

Quiz

Use the quiz below and explain each decision before you run the robot.

Completion checklist

Teacher checked wiring and power.

I uploaded the correct sketch and identified its constants.

I tested the stop condition.

I logged an observation and a change.


Check your understanding

Which condition stops this program, and how will you test it safely?
