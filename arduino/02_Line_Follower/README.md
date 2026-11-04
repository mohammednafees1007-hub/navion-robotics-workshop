# 02_Line_Follower

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
Two downward sensors flank a 25.4 mm black line on white: left OUT34 and right OUT39. DETECTED_LEVEL must match measured black polarity for both. One black turns toward that sensor; both black latches stopped. Both white can mean centered OR lost. The conservative algorithm moves forward up to 700 ms without a black reading, searches in the last-turn direction for up to 1500 ms, then latches stopped. A long straight can trigger search. Reset only after inspection/repositioning. Autonomous session ends at 60 seconds.

## Test
With wheels raised, present all four black/white combinations. Check both-black stop and search timeout, then supervise a short floor test. Initial lastTurn=-1 searches left; +1 searches right. Tune SPEED and SEARCH_MS one value at a time. Do not claim continuous or unambiguous line tracking from this sensor arrangement.
