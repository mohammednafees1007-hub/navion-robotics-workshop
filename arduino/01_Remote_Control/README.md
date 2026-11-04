# 01_Remote_Control

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
Send uppercase F/B/L/R/S from USB Serial Monitor or a working Windows Bluetooth Classic outgoing COM port. F forward, B backward, L left, R right, S stop. One movement lasts at most about 800 ms without a refresh. Invalid characters do not refresh the timeout. Last movement sender owns motion; Bluetooth disconnect stops Bluetooth-owned motion without cancelling an active USB-owned command. S from either source stops.

## Test
Wheels lifted: S first, then one F. Check direction and timeout. Test B/L/R briefly. If pairing works but COM traffic does not, fall back to USB. A browser or phone app is not part of this guide. Starting duty SPEED=145 is not measured RPM; tune only after removing mechanical faults.
