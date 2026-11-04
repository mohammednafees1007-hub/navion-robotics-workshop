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
