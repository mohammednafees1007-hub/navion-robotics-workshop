# 03_Obstacle_Avoidance

Requires the original ESP32-WROOM-32 target, Arduino IDE 2.x and Arduino-ESP32 core 3.x. The three robot mode sketches compiled with core 3.3.11. No additional library installation; BluetoothSerial is bundled with the ESP32 core.

## Provisional wiring
IN1 25, IN2 26, IN3 27, IN4 14; ENA 32, ENB 33. Left IR OUT 34, front 35, right 39. Input-only pins have no internal pull-ups. Use teacher-confirmed 3.3 V modules, VCC 3V3 and common GND. Confirm the actual board exposes these GPIOs. No 5 V signals on GPIO.

## Upload and power
1. Read the Power & wiring chapter in the website/full user manual. A compiled program does not approve the physical circuit.
2. Battery OFF, USB unplugged before changing wires. Isolate the external ESP32 5 V feed before connecting USB.
3. Open the .ino from its same-named folder; choose ESP32 Dev Module and actual USB COM port. Verify then Upload. Serial Monitor 115200.
4. For any motor test with USB attached, use only the teacher-approved isolation arrangement. For battery-only runs, unplug USB and restore the verified external feed while everything is OFF.
5. Lift wheels before the first test; keep the switch reachable. Copy calibrated INVERT_LEFT/RIGHT settings into each robot mode sketch.

## Verification limit
Compilation is a software check. Power regulator stability, USB isolation, module voltage/polarity, actual floor behavior and Windows Classic SPP COM operation remain NOT TESTED on hardware. Genuine mounting/board details must be checked by the teacher. The full manual is docs/USER_MANUAL.md in the repository, or USER_MANUAL.md in the downloaded setup pack.

## Operation
IR modules face left/front/right: OUT34/35/39. DETECTED_LEVEL must match obstacle polarity for all three. Front clear advances. Front blocked stops first, then chooses clear left, otherwise clear right. Both sides clear prefers left. All blocked reverses for REVERSE_MS=350 then turns left for UTURN_MS=800. Ordinary turns use TURN_MS=400. Re-sense after each timed action. Session ends at 60 seconds.

## Test
Calibrate roughly 5–10 cm on the actual test object; range is not guaranteed. Check every decision with wheels lifted, then a supervised floor run. No rear sensor: clear the reverse area. Dark/transparent/shiny objects may be missed. Timed turns are not measured angles. Switch OFF to stop autonomous movement before touching or repositioning.
