# Robot building blocks


ESP32 and GPIO

The microcontroller runs the program repeatedly. GPIO means general-purpose input/output. A digital signal reads HIGH or LOW; it is not an exact distance measurement.

Motor driver and gearbox

An ESP32 pin cannot supply motor current. The L298N H-bridge switches the separate motor supply to change direction. A gearbox trades shaft speed for turning force. Motors may need a higher PWM duty to start than to keep moving.

PWM and ground

Pulse-width modulation switches power rapidly. A value from 0 to 255 controls duty in our 8-bit program; it is not a speed in RPM. Ground is the shared voltage reference, not an optional wire.

IR and serial

IR modules shine infrared light and compare reflected light to a threshold. Potentiometers adjust sensitivity. USB Serial uses a cable and CP2102. Bluetooth Classic SPP can provide a wireless Windows COM port; it is different from BLE and cannot be used directly by a standard browser controller.

Teacher check · provisional wiring
The assumed power path is 2 × matched 18650 cells in series (7.4 V nominal, 8.4 V full) → switched holder → L298N motor supply → onboard regulated 5 V → ESP32 designated 5V/VIN. It is not electrically verified. The regulator may drop out as batteries discharge. Never connect this supply to 3V3.

Keep the regulator 5V-EN jumper as required by the actual module for its 5 V output. Remove only ENA/ENB motor-enable jumpers for PWM. These are different jumpers. Teacher must inspect the exact board before connecting USB and external 5 V together. Default upload procedure: battery off, disconnect the external 5 V wire from ESP32, use USB, then unplug USB before restoring external power.

Use common ground. Sensors must work at 3.3 V with driven digital outputs; no 5 V on GPIO. GPIO 34/35/39 are input only and have no internal pull-ups. An adult prepares matched cells; avoid shorts and improper charging. Switch off during assembly and use teacher supervision. A switched holder does not establish battery protection.



Check your understanding

Why do motors need a driver instead of a GPIO connection?
