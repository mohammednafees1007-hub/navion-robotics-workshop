# Code change log
## v2 — 2026-11-05
- Public setup manual replaces account/course system; no login/database dependency.
- Added motor-OFF PING/PONG and raw IR diagnostic sketches.
- Three robot mode sketches unchanged; instructions now include power states and expected results.

## v1 — 2026-11-05
- Core 3.x pin-based LEDC; self-contained sketches and consistent provisional map.
- Remote ownership prevents Bluetooth disconnect stopping an active USB session. 800 ms deadman.
- Line layout ambiguity explicitly documented; 700 ms forward, bounded search, latched stop.
- Obstacle nonblocking reverse/turn states; left preference; 60-second autonomous session limit.
