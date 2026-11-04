# 01 · Laptop remote control


Aim

Drive with USB and Bluetooth Classic. Explain the input, decision and motor output to a partner.

Equipment

Use the same kit and chassis. Remote needs the Windows laptop; line uses two IR modules; avoidance uses all three. No phone, ultrasonic sensor, servo or Wi-Fi.

Learn the concept

A serial command is one letter. F drives forward; B reverses; L spins left; R spins right; S stops. Movement must repeat within 800 ms. One Send produces only a short motion: that is the deadman, not a fault.

InputAction

F / BBoth motors forward / reverse

L / ROpposite wheel directions

S / command timeoutStop

Bluetooth disconnectStop if Bluetooth owns motion; keep an active USB session

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

Read commands → validate letter → drive → check owner/disconnect/timeout → repeat.

Code download
Download 01_Remote_Control.ino
Understand the code

initRobot() sets motor outputs low before attaching PWM. drive() maps signed speeds to wheel directions. oneMotor() briefly clears PWM before reversing. Top-level constants keep the pin map, inversion and duty editable.

command() accepts only F/B/L/R/S. owner records the last movement source. lastCommand and millis implement the deadman without waiting. Limited parser loops keep timeout checks running.
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


Upload steps

Teacher checks power isolation; lift wheels and keep battery off while uploading.

Open the .ino inside its same-named folder in Arduino IDE 2.x.

Select ESP32 Dev Module for the original WROOM-32, the correct USB COM port, then Verify and Upload.

Open Serial Monitor at 115200 baud. Record messages and close other applications using the port.

After upload, remove USB before restoring the assumed external supply. Test at low speed with teacher approval.

Run and observe

Start with wheels lifted. Test stop behavior first, then forward direction. Place on the floor only in a supervised clear area. Record input, expected action and observed action. Stop if a motor stalls, wiring heats or the ESP32 resets.

Calibration

Pair on a Windows laptop

Upload using USB first and test S with wheels lifted.

Open Windows Settings → Bluetooth & devices → Add device → Bluetooth, select NAVION_ROBOT. Teacher should use a unique device name when several kits operate together.

Look in More Bluetooth settings → COM Ports or Device Manager for the outgoing serial COM port.

Try that port in the IDE. If unavailable, use a Windows serial terminal such as PuTTY with the outgoing COM port. Close other programs using it.

Send F briefly, then S. Repeat commands for sustained motion; terminal key repeat can help but must beat the 800 ms timeout.

Bluetooth Classic SPP/Windows COM compatibility is assumed, not tested. Pairing alone does not guarantee a working COM connection. This is not BLE; ESP32-C3/S3 are not substitutes for Classic SPP. Use USB when the laptop cannot expose the required port.

Troubleshooting

Reversed motor: switch the matching INVERT constant. No movement: check enable jumpers, common ground and starting duty. Unexpected sensor state: check calibration and 3.3 V compatibility. Brownout: teacher checks the assumed power regulator under load.

Student challenge

Change SPEED from 145 to 120. Does the motor still start?

Quiz

Use the quiz below and explain each decision before you run the robot.

Completion checklist

Teacher checked wiring and power.

I uploaded the correct sketch and identified its constants.

I tested the stop condition.

I logged an observation and a change.


Check your understanding

Which condition stops this program, and how will you test it safely?
