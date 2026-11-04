# Power & wiring


Teacher check · provisional wiring
The assumed power path is 2 × matched 18650 cells in series (7.4 V nominal, 8.4 V full) → switched holder → L298N motor supply → onboard regulated 5 V → ESP32 designated 5V/VIN. It is not electrically verified. The regulator may drop out as batteries discharge. Never connect this supply to 3V3.

Keep the regulator 5V-EN jumper as required by the actual module for its 5 V output. Remove only ENA/ENB motor-enable jumpers for PWM. These are different jumpers. Teacher must inspect the exact board before connecting USB and external 5 V together. Default upload procedure: battery off, disconnect the external 5 V wire from ESP32, use USB, then unplug USB before restoring external power.

Use common ground. Sensors must work at 3.3 V with driven digital outputs; no 5 V on GPIO. GPIO 34/35/39 are input only and have no internal pull-ups. An adult prepares matched cells; avoid shorts and improper charging. Switch off during assembly and use teacher supervision. A switched holder does not establish battery protection.


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

Connection order

Keep battery off and USB unplugged.

Connect common GND between driver, ESP32 and sensors.

Connect IN1–IN4, then ENA/ENB after removing only motor enable jumpers.

Connect motors to OUT1/OUT2 and OUT3/OUT4. Teacher verifies left/right assignment.

Connect sensor VCC to 3V3 only if the supplied modules support it; connect their OUT pins using the map.

Teacher checks power path and absence of shorts before energizing.

Chosen GPIOs avoid boot-strapping pins; GPIO14 has a JTAG role and is used here as a normal output. Confirm all pins, especially VN/GPIO39, exist on the actual 30-pin board.


Check your understanding

How is 5V-EN different from ENA and ENB?
