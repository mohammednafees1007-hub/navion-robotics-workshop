# 01_Remote_Control
Requires original ESP32-WROOM-32 and Arduino-ESP32 core 3.x. No additional library installation; BluetoothSerial comes with the ESP32 core. Independently uploadable.

## Wiring (provisional)
- IN1: GPIO 25
- IN2: GPIO 26
- IN3: GPIO 27
- IN4: GPIO 14
- ENA: GPIO 32
- ENB: GPIO 33
- LEFT_IR: GPIO 34
- FRONT_IR: GPIO 35
- RIGHT_IR: GPIO 39

Remove ENA/ENB motor jumpers for PWM; regulator 5V-EN is different. Read ../../docs/power-assumptions.md before power is applied. Input pins 34/35/39 have no pull-ups. Confirm driven 3.3 V sensor output.

## Upload
1. Teacher checks power isolation; battery off and external ESP32 5 V disconnected.
2. Connect USB data cable. Open this folder's .ino in Arduino IDE 2.x.
3. Select ESP32 Dev Module, USB COM port, core 3.x. Verify then Upload.
4. Serial Monitor: 115200 baud. Disconnect USB before restoring external power, unless the exact board has been approved for both supplies.
5. Lift wheels, check direction at low speed. Change INVERT_LEFT/INVERT_RIGHT if required. Never rewire while powered.

## Operation and problems
Remote: F/B/L/R/S; repeat movement faster than 800 ms or motion stops. S always stops. Bluetooth disconnect stops only Bluetooth-owned motion. USB may take ownership. Invalid characters do not refresh timeout.
Line: calibrate DETECTED_LEVEL. Both white means centered OR lost: a two-sensor limitation. After 700 ms without a black detection it searches for up to 1500 ms, then latches stopped. Both black stops for inspection. Reset after repositioning; a long straight can trigger search. Improve using a teacher-reviewed algorithm or sensor arrangement, not an unsupported claim of perfect tracking.
Obstacle: front clear advances; front blocked prefers clear left, otherwise right. All blocked reverses briefly and turns left for a timed U-turn. No rear sensor: reverse only in a supervised clear area. After each turn re-sense. Session timeout is 60 s in autonomous modes.
Motors silent: check supply, enable jumpers, ground and starting duty. Reset/brownout: teacher measures assumed regulator supply under motor load. IR unreliable: calibrate for actual surface and light.

## Verification
Hardware NOT TESTED. Arduino compilation status: see PROJECT_STATUS.md. Do not infer validation from source delivery.
