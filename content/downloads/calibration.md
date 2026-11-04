# Calibrate & test


Motor direction

Lift the wheels. Send a short forward command and stop. If one wheel reverses, change that motor's INVERT constant, upload again and repeat. Check mechanical friction before increasing speed.

Sensor polarity and sensitivity

With motors disabled, inspect indicator changes and digital output against black/white or obstacle/no obstacle. Active LOW is a configuration, not a universal IR property. Adjust the potentiometer slowly. Record lighting, surface and the successful threshold.

Battery effects

Motor starting and turn times change with voltage and load. Brownouts may indicate an inadequate assumed 5 V path. A teacher must measure before approving the circuit; do not improvise an added part into this BOM.

Test log

Date / modeSettingExpectedObservedNext change

________________________________________

Print this page. Repeat each supervised test three times. A simulation or successful upload is not a physical pass.


Check your understanding

Why should you change only one tuning constant at a time?
