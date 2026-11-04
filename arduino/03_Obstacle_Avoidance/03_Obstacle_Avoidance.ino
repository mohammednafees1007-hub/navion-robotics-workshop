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
