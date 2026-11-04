# Set up Arduino on Windows


Install on Windows 10/11

Download Arduino IDE 2.x from Arduino and run its installer.

In File → Preferences add https://espressif.github.io/arduino-esp32/package_esp32_index.json to Additional Boards Manager URLs.

Open Boards Manager, search esp32, install “esp32 by Espressif Systems”. These sketches target core 3.x and use pin-based LEDC APIs.

Connect a data-capable cable. If no COM port appears, inspect Windows Device Manager and install the official CP210x driver if needed.

Select ESP32 Dev Module and the COM port that appears when you plug in the board.

Hello without an LED

void setup() { Serial.begin(115200); }
void loop() { Serial.println("Hello, engineer!"); delay(1000); }

Upload with battery disconnected. At 115200 baud you should see one message each second. This exercise does not assume an onboard LED exists.
REAL SCREENSHOT PLACEHOLDER: Arduino IDE board, port and Serial Monitor.
If upload fails

Check data cable, port, board, driver, and that no terminal has the port open. If the exact board requires it, hold BOOT during connection and release after upload starts. Ask the teacher if this fails; do not randomly change wiring while powered.


Check your understanding

Which board and baud rate will you select?
