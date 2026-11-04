# 00_Sensor_Check
Open the .ino in its same-named folder. Original ESP32, Arduino-ESP32 core 3.x; no added library.
Use isolated USB power only: motor battery OFF and external ESP32 5 V feed disconnected. Select ESP32 Dev Module and your actual USB COM port. Verify then Upload. Serial Monitor: 115200 baud. Motors must remain off.
Connect verified 3.3 V modules only: left OUT GPIO34, front GPIO35, right GPIO39, VCC 3V3, GND common. Read 0=LOW/1=HIGH and record actual surface/object polarity. Unconnected inputs float. This diagnostic cannot drive motors.
