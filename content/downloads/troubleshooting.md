# Fix it step by step


SymptomFirst checks

No USB COM portData cable, USB socket, Device Manager, CP210x driver

Port busy / access deniedClose other terminals; reconnect and reselect port; follow lab permissions

Compile error around LEDCUse Arduino-ESP32 core 3.x; these sketches use ledcAttach and pin-based ledcWrite

Upload connection failureCorrect board and COM port; check BOOT procedure for exact board

Bluetooth pairs but no COMClassic SPP support and outgoing COM settings; use Windows terminal or USB fallback

Remote stops quickly800 ms deadman requires repeated movement commands

Reset / brownoutStop; teacher checks regulator voltage under motor load and USB supply isolation

Motor reversed / silentINVERT constant; ENA/ENB jumpers, common ground, power, wheel friction

False IR readingActive level, 3.3 V suitability, sunlight, reflectivity and potentiometer

Line search on straightBoth white is ambiguous; conservative timeout can trigger on straights

Robot veersWheel rubbing, caster, mismatched motors, battery and sensor spacing

Turn off power before touching wiring. Record the error text and what changed before asking for help.


Check your understanding

What evidence would help your teacher diagnose a reset?
