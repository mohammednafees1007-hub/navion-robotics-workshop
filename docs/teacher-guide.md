# Teacher guide — public manual

No student accounts, passwords, scores, analytics, progress or certificates are collected by this version. No database is read/created. Any historical local/host database stays private and is not part of the public manual.

Validate supplied board GPIOs, 3.3 V sensor operation/output polarity, module labels, motor direction/startup, fasteners and mounting before teaching. Validate the assumed L298N regulator output under motor load and as the 2S supply discharges. Isolate the external ESP32 5 V feed during USB work unless the exact arrangement has been approved. The guide gives explicit upload, battery-run and teacher-approved USB motor-test states.

Adult-prepared matched cells and supervised handling remain required. No student charging, soldering or battery redesign is introduced. No buck converter/BMS was added. A switched holder does not establish protection.

Use motor-OFF diagnostics before motion. Two flanking line sensors cannot distinguish centered/lost both-white states, so a long straight may trigger search. Avoidance has no rear sensor. Actual power, floor behavior and Windows Bluetooth COM operation remain unverified.

Read [USER_MANUAL.md](USER_MANUAL.md). Genuine kit/chassis photos, fasteners, final board/module specification and support contact remain pending. Source diagrams remain provisional.
