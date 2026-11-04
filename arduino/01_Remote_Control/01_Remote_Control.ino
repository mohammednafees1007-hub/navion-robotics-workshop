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

#include "BluetoothSerial.h"
#if !defined(CONFIG_BT_SPP_ENABLED)
#error Use an original ESP32 with Bluetooth Classic SPP enabled
#endif
BluetoothSerial BT;
const unsigned long DEADMAN_MS=800;
unsigned long lastCommand=0;
int owner=0; // 0 stopped, 1 USB, 2 Bluetooth; last movement sender owns motion
bool wasConnected=false;
void command(char c,int source) {
  int l=0,r=0;
  switch(c) {
    case 'F': l=SPEED;r=SPEED;break;
    case 'B': l=-SPEED;r=-SPEED;break;
    case 'L': l=-SPEED;r=SPEED;break;
    case 'R': l=SPEED;r=-SPEED;break;
    case 'S': drive(0,0);owner=0;Serial.println("STOP");if(BT.hasClient()) BT.println("STOP");return;
    default:return; // ignore line endings and invalid characters
  }
  drive(l,r); owner=source;lastCommand=millis();
  Serial.println(c);if(BT.hasClient()) BT.println(c);
}
void setup() { initRobot(); if(!BT.begin("NAVION_ROBOT")) Serial.println("BT failed: USB available"); Serial.println("Ready F B L R S; repeat movement within 800 ms"); }
void loop() {
  bool connected=BT.hasClient();
  if(wasConnected && !connected && owner==2) { drive(0,0);owner=0; }
  wasConnected=connected;
  // Limit each pass so a noisy sender cannot starve the failsafe.
  for(int n=0;n<32 && Serial.available();++n) command(Serial.read(),1);
  for(int n=0;n<32 && BT.available();++n) command(BT.read(),2);
  if(owner && millis()-lastCommand>=DEADMAN_MS) { drive(0,0);owner=0;Serial.println("Timeout stop"); }
}
