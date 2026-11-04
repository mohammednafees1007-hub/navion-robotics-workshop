# 03 · Avoid obstacles


Aim

Sense three directions and choose a clear path. Explain the input, decision and motor output to a partner.

Equipment

Use the same kit and chassis. Remote needs the Windows laptop; line uses two IR modules; avoidance uses all three. No phone, ultrasonic sensor, servo or Wi-Fi.

Learn the concept

Mount modules facing left, front and right. Set potentiometers for roughly 5–10 cm on your actual test object. This is a calibration goal, not a guaranteed range.

FrontLeft / RightAction

ClearAnyForward

BlockedBoth clearStop, prefer left

BlockedLeft clear / right blockedStop, left

BlockedLeft blocked / right clearStop, right

BlockedBoth blockedStop, reverse briefly, timed left U-turn

Re-sense after turns. Dark, shiny or transparent objects and sunlight may defeat detection. There is no rear sensor: teacher must keep the reverse area clear. Timed turns depend on floor grip, supply and motor differences; they are not measured angles.

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
Download 03_Obstacle_Avoidance.ino
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

const unsigned long REVERSE_MS=350, TURN_MS=400, UTURN_MS=800, SESSION_MS=60000;
unsigned long started=0,phaseStart=0;
int phase=0,turnSign=-1; // 0 sensing, 1 reverse, 2 turn
bool uturn=false;
void setup() { initRobot();started=millis();Serial.println("Avoidance: reset starts 60 s session"); }
void loop() {
  unsigned long now=millis();
  if(now-started>=SESSION_MS) { drive(0,0);return; }
  if(phase==1) {
    if(now-phaseStart<REVERSE_MS) { drive(-SPEED,-SPEED);return; }
    drive(0,0);phase=2;phaseStart=now;
  }
  if(phase==2) {
    if(now-phaseStart<(uturn?UTURN_MS:TURN_MS)) { drive(turnSign<0?-SPEED:SPEED,turnSign<0?SPEED:-SPEED);return; }
    drive(0,0);phase=0;return;
  }
  bool front=detected(FRONT_IR), left=detected(LEFT_IR), right=detected(RIGHT_IR);
  if(!front) { drive(SPEED,SPEED);return; }
  drive(0,0); // stop first, then choose a side
  uturn=left && right; turnSign=!left?-1:!right?1:-1;
  phase=uturn?1:2;phaseStart=now;
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

Set DETECTED_LEVEL after checking all three sensors against the same object. Keep speed low. Test one obstacle, then two sides blocked, then all three blocked while a teacher guards the robot. Tune REVERSE_MS, TURN_MS and UTURN_MS one at a time. The sketch stops after a 60-second session; reset only after inspecting the area.

Troubleshooting

Reversed motor: switch the matching INVERT constant. No movement: check enable jumpers, common ground and starting duty. Unexpected sensor state: check calibration and 3.3 V compatibility. Brownout: teacher checks the assumed power regulator under load.

Student challenge

Change the preferred clear side to right and update your decision table.

Quiz

Use the quiz below and explain each decision before you run the robot.

Completion checklist

Teacher checked wiring and power.

I uploaded the correct sketch and identified its constants.

I tested the stop condition.

I logged an observation and a change.


Check your understanding

Which condition stops this program, and how will you test it safely?
