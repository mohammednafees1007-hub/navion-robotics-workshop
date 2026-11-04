# Project status

## Implemented software
PHP portal, server-enforced student/admin access, password hashing, session regeneration, CSRF, login throttling, prepared PDO SQLite queries, account creation/disable/reset, lesson access, score settings, dashboard, 15 lesson routes plus tools/admin pages, quiz feedback/history, lesson progress, certificate eligibility/printing, allowlisted downloads, original SVG diagrams, three standalone sketches and hosting documentation.

## User-defined behavior
One reconfigurable chassis; Windows laptops; F/B/L/R/S; two downward line sensors; three directional obstacle sensors; left preference; reverse/U-turn when blocked. BOM quantities preserved; no buck converter/BMS added.

## Assumed / provisional / TBD
2S → L298N regulator → ESP32 5V/VIN stability and Windows Classic SPP COM operation are unverified assumptions. GPIO availability, 3.3 V IR operation/polarity, actual motor fit and turn timing need teacher validation. Photos, genuine logo, IDE screenshots, fasteners, final grades/support contact TBD. SQLite is implemented for localhost; production DB choice is open.

## Limitations
Two flanking sensors cannot distinguish centered/lost when both see white. The delivered conservative algorithm advances up to 700 ms then searches at most 1500 ms and stops; long straights can trigger search. Both black stops. Autonomous sessions stop after 60 seconds. Timed avoidance is not measured navigation; no rear sensor. Physical/electrical checks and classroom acceptance remain NOT TESTED. No claim of hardware safety or official accreditation.

## Actual verification
Verified 2026-11-05: all five PHP files passed syntax checks using PHP 8.2.35. The PHP site ran locally at http://127.0.0.1:8000 during verification. 440 HTTP/integration/link/GPIO checks passed after final changes (tests/verification-results.txt). All three sketches compiled successfully for esp32:esp32:esp32 with installed Arduino-ESP32 3.3.11: remote 1,071,047 bytes, line 280,883 bytes, obstacle 280,779 bytes (full summary in tests/firmware-results.txt). Physical hardware, power stability and Windows Bluetooth communication remain NOT TESTED. The verification server stops after checks; use README commands to start your own instance.
