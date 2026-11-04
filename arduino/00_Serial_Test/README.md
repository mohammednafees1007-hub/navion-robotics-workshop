# 00_Serial_Test
Open the .ino in its same-named folder. Original ESP32, Arduino-ESP32 core 3.x; no added library.
Use isolated USB power only: motor battery OFF and external ESP32 5 V feed disconnected. Select ESP32 Dev Module and your actual USB COM port. Verify then Upload. Serial Monitor: 115200 baud. Motors must remain off.
Set line ending Newline and send PING. Expected response PONG. This is a teaching-only serial test, not the remote command parser.
