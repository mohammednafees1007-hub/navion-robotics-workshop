# NAVION ROBOTICS — ESP32 Three-Robot Workshop Website

> **Single-file Codex build specification — editable working draft (v1).**
>
> **INSTRUCTION TO CODEX:** This Markdown file is the source of requirements for creating a complete, locally runnable educational website folder, three Arduino sketches, and supporting documentation. Build the project from this document. Do not ask for details already stated here. Treat every `[ASSUMED — CHANGEABLE]` as an explicit user-approved working assumption that may be edited later; do **not** present it as hardware-tested or independently verified. Treat `[TBD]` as not yet confirmed, and make sensible software-only defaults while keeping them easily configurable. Do not silently invent product specifications, photos, supplier claims, or electronics verification results.

## 0. Outcome and work order

Create a PHP-based, multi-page, student-facing robotics learning portal which can be run on localhost now and later integrated under an existing PHP website. It must be suitable for class 6 through class 10 beginners. Build the **complete website**, **three separate compile-ready Arduino IDE `.ino` sketches**, and detailed, accurate documentation of the build and the code. Include quizzes, progress tracking, student-only access and a printable completion certificate. The website is for learning and downloading code, **not** for controlling the robot from a browser.

Steps for Codex:
1. Inspect the working directory. Create the website in a new folder `navion-robotics-workshop/`. Do not overwrite unrelated files.
2. Implement backend, student UI, navigation, database setup and actual content. Do not leave chapters full of generic placeholder text.
3. Implement the three sketches using a single consistent provisional GPIO map, with central editable constants and wiring tables that agree across all files.
4. Include example visuals as editable SVG diagrams (schematics, pinout overview, workflow and sensor layouts). Put **clearly labelled placeholders** where genuine photos and Arduino IDE screenshots must be supplied later; do not fabricate them or claim they are real.
5. Validate PHP syntax, run tests where possible, check the internal links, and try compiling the `.ino` sketches if Arduino CLI/ESP32 core is installed. Otherwise record compilation as **NOT TESTED** and give exact steps to test; never claim an unperformed hardware test has passed.
6. Run the site locally, provide the local URL and exact setup commands, and produce a `PROJECT_STATUS.md` with completed, pending and unverified items.

## 1. Project, audience and permissions

- Project name (working): **Robotics Workshop**.
- Organiser: **Navion Robotics**. Brand/logo artwork: `[TBD — real logo asset to be supplied]`.
- Website placement: integrate later with an **existing PHP website**; build a standalone folder now. No replacement of the existing site's home page.
- Students: school children, **grades 6–10** (the final eligible grade range is `[TBD]`; keep site configuration editable).
- Language: English only; short sentences, step-by-step explanations, friendly technical accuracy.
- Intended learning: one student can identify parts, assemble the robot, install and configure Arduino IDE 2.x on Windows 10/11, upload sketches, use Serial Monitor, troubleshoot, run all three modes, adjust behavior, and complete quizzes and simple challenges.
- Access: **registered students only** may view the lessons, downloads, quizzes, progress and certificate. Admin can manage student accounts and progress. Protect routes server-side; hiding links is not security.
- Student devices: **Windows 10/11 laptop or lab computer**. Students **cannot bring phones**.
- Enrollment/payment handling: **out of scope**. Do not build live Razorpay or public registrations without further specification. Optional nonfunctional navigation placeholder can be omitted.
- This is **educational content**, not an internal pricing/management proposal. Do not display the management proposal, vendor RFQ, supplier prices, internal procurement discussion or customer personal information to students.

## 2. Three experiments, one physical kit

There is **one reusable 3D-printed chassis**, not three simultaneously operating robots. Students reconfigure the same robot for three experiments, changing sensor positions and uploading separate programs. Each experiment must have its own `.ino` file and dedicated website page.

1. **Bluetooth + USB Serial remote-controlled robot**
   - ESP32-WROOM-32 with Bluetooth Classic SPP. Students operate from their Windows laptop: first via Arduino IDE Serial Monitor over USB, then wirelessly via a Windows Bluetooth virtual COM port where supported.
   - Use the commands `F` (forward), `B` (backward), `L` (left), `R` (right), `S` (stop). Optional `SPEED:0..255` or similar documented speed control may be included, but the five essential commands must always work.
   - Drive two BO motors through the L298N. Stop motors on an explicit stop command, Bluetooth disconnect, and appropriate loss-of-command failsafe. Do not require any smartphone app.
   - `[ASSUMED — CHANGEABLE]` Windows Bluetooth Classic Serial communication with the actual ESP32 works. This is a **project assumption, not a verified test result**. Explain pairing, COM ports, possible IDE limitations and a Windows serial terminal fallback without claiming it has been tested.
   - Do **not** pretend a standard browser can speak directly to Bluetooth Classic SPP; the learning portal should not include a misleading browser Bluetooth controller.

2. **Two-IR-sensor line-follower robot**
   - Black line on white surface, approximately **1 inch / 25.4 mm** wide.
   - Two downward-facing IR sensors near the front of the robot, with the line nominally between them: `sensor — line — sensor`.
   - Fixed motor speed initially; tune the speed constant if needed.
   - Explain the four combinations of two digital IR readings, including how active-low detection maps to black and white only after calibration. Correct for reverse sensor behavior via a configurable constant rather than asserting universal behavior.
   - If the line is lost, rotate/search to reacquire it; preferably use the last known turn direction. Include a bounded or safe-search behavior and clear explanation for beginners.
   - Include track creation, calibration, algorithm, code, expected results and a small modification challenge.

3. **Three-IR-sensor obstacle-avoiding robot**
   - IR sensor arrangement: front, left, right; intended short-range obstacle detection **roughly 5–10 cm**, adjusted via sensor potentiometers. Emphasize actual detection depends on surface reflectivity and module calibration.
   - Stop when front obstacle detected; choose a clear side. If both sides are clear, **prefer left**. If all directions are blocked, reverse then turn around.
   - Explain decision table and motion flowchart; motor timings and speed adjustable. Include limitations of IR detection, the possibility of missed transparent/dark objects, and safe low-speed testing.
   - No ultrasonic sensor, servo or Wi-Fi needed.

## 3. Hardware BOM (per student kit)

Based on the user's BOM/RFQ v1. Preserve these quantities; do not add a new part silently.

| Item | Required specification | Qty per kit |
|---|---|---:|
| ESP32 | ESP32-WROOM-32-family 30-pin development board, CP2102 USB UART, USB Type-C, fitted headers, Bluetooth Classic + BLE | 1 |
| Motor driver | Red L298N 2 A module with heatsink, factory-fitted screw terminals/headers | 1 |
| IR sensors | Three-pin adjustable digital IR proximity/obstacle modules, intended to operate at ESP32-compatible 3.3 V, adjustable potentiometer | 3 |
| Battery cells | 18650 Li-ion 3.7 V nominal, 2000 mAh, matched cells | 2 |
| Battery holder | Two 18650 cells in **series**, built-in ON/OFF switch, pre-attached leads | 1 |
| BO motors | Prewired 130–280 RPM geared motors, **rated 3–9 V** according to user; confirm product fit / motor starting behavior when physical kit arrives | 2 |
| Drive wheels | 65 mm yellow wheels matching BO motor shafts | 2 |
| Motor mounting clamps | Compatible with motor body and chassis | 2 |
| Caster wheel | Single small caster for two-motor chassis | 1 |
| Breadboard | SYB-170 miniature solderless breadboard | 1 |
| Male–female jumper wires | 20 cm, pack of 20 | 1 pack |
| Female–female jumper wires | 20 cm, pack of 20 | 1 pack |
| Data cable | USB-A to USB-C, 0.5 m, data-capable | 1 |
| Screwdriver | Small 2-in-1 flat + Phillips | 1 |

Additionally: **Navion Robotics supplies the separately manufactured 3D-printed chassis**, with interchangeable mounts for two downward sensors and three directional sensors. Mechanical bolts/nuts/standoffs `[TBD — dimensions and quantities]`. Wheel/caster details and final photos `[TBD]`. No student soldering, stripping, crimping or charger setup.

### Working power assumptions (editable, not hardware-verified)

- `[ASSUMED — CHANGEABLE]` Battery is **2 × 18650 in series**: 7.4 V nominal, 8.4 V fully charged, routed via the switched holder to L298N motor-supply input.
- `[ASSUMED — CHANGEABLE]` **ESP32 is powered from the red L298N module's onboard regulated 5 V output**, connected only to the development board's designated 5V/VIN pin (never directly to the ESP32 3V3 pin).
- `[ASSUMED — CHANGEABLE]` The specific L298N regulator supplies sufficiently stable current and voltage for the ESP32 throughout the intended session. **User will verify this later; do not state it has been tested or guaranteed.** Some L298N boards' onboard 5 V regulator may drop out as 2S voltage decreases.
- **No separate buck converter in the BOM.** Do not add one by default.
- **Battery-protection redesign is out of scope at the user's request.** Do not add a standalone BMS to the BOM or require students to assemble one. **Do not claim that an ordinary switched holder is protected, that unprotected lithium-ion cells are safe, or that two days of use removes electrical risks.** Document battery handling only at a high level: adult-prepared matched cells, avoid short circuits and improper charging, turn off while assembling, teacher supervision; no unverified charging directions.
- Use **common ground** between the L298N, ESP32 and digital sensors.
- Explain the difference between L298N **5V-EN / regulator jumper** and **ENA/ENB motor PWM jumpers**. Do not tell students to remove the regulator jumper while also claiming the L298N's 5V output is powering the ESP32.
- Connecting USB and external 5 V at the same time depends on the exact ESP32 development board's power circuit. Include a prominent teacher check/USB-power procedure, rather than asserting all boards isolate the two supplies safely.
- The circuit tutorial must show wiring as **provisional until one assembled prototype is electrically validated**, even while using these assumptions for development.

## 4. Provisional GPIO map to keep code and documentation consistent

`[PROVISIONAL — CHANGEABLE]` Codex may use the table below as a starting implementation **if the 30-pin board exposes these GPIOs**, but must label it provisional, keep it in a shared config/documentation map and check for strapping/power and input-only limitations before final publication. If unsuitable, change it consistently everywhere and document the change.

| Function | Proposed ESP32 GPIO | Wiring note |
|---|---:|---|
| L298N IN1 | 25 | Left motor direction |
| L298N IN2 | 26 | Left motor direction |
| L298N IN3 | 27 | Right motor direction |
| L298N IN4 | 14 | Right motor direction |
| L298N ENA | 32 | Left motor PWM; ENA jumper removed if PWM used |
| L298N ENB | 33 | Right motor PWM; ENB jumper removed if PWM used |
| Left IR digital OUT | 34 | Input only; use actual module's digital output |
| Front IR digital OUT | 35 | Input only |
| Right IR digital OUT | 39 (VN) | Input only; ensure exposed on supplied board |
| Sensor VCC | Board's 3V3 | Sensor must be compatible with 3.3 V |
| Sensor GND | GND | Common ground |

For the line follower use left and right sensors only (GPIO 34 and 39) and position them underneath; for obstacle avoiding use all three (34, 35, 39) facing left/front/right. Note that GPIO 34/35/39 are **input-only with no internal pull-ups**, so a compatible driven digital sensor output is required. If sensor outputs require 5 V, do not directly apply 5 V to ESP32 GPIO. Program motor speed with the Arduino-ESP32 PWM API appropriate to the installed core version. Explain how to reverse a motor through code constants if the physical motor orientation differs.

## 5. Course page hierarchy and content

Build proper sidebar navigation, breadcrumbs, previous/next lesson actions, readable content on laptop and mobile-sized displays (mobile layout responsive though students cannot bring phones). The pages must be separate real routes/pages, not one huge scrolling page.

1. **Student dashboard** — welcome, objectives, learner progress, three project cards, current lesson, quiz scores, certificate status.
2. **Introduction** — what is a robot, three project outcomes, workshop sequence, learning goals, how to use the documentation.
3. **Kit unboxing & BOM** — exact item list, quantities, what each part does; annotated placeholders for real photos; kit inventory checklist.
4. **Robot basics** — ESP32 microcontroller, GPIO, L298N H-bridge, DC motor/gearbox, PWM, ground, digital IR sensors, Bluetooth vs USB Serial, battery/switch overview, safety notes.
5. **Software installation on Windows 10/11** — Arduino IDE 2.x download, setup, add Espressif board package URL, install ESP32 core, CP210x USB driver when needed, USB data cable, choose board/port, open Serial Monitor, line endings and baud rate, upload errors, sample Hello World/LED exercise without relying on a possibly missing LED pin.
6. **Mini C/C++ lesson** — variables, constants, `setup()`, `loop()`, `pinMode`, `digitalRead`, `digitalWrite`, PWM, `if/else`, functions, serial commands, `millis` vs `delay`, concise examples separate from full robot sketches.
7. **Physical chassis assembly** — motors, motor clamps, 65-mm wheels, caster, ESP32, driver, battery holder and interchangeable sensor mounts; checklists, screw sizes `[TBD]`, teacher-supplied photos placeholders.
8. **Power & wiring** — shared wiring table, 2S battery, L298N module, ESP32 5 V (as an **assumed/teacher-check** setup), common ground, control pins and correct jumper discussion; schematic SVG for base robot, two-sensor variant, three-sensor variant; no false-tested claims.
9. **First serial test** — upload sketch, print status, type and read `PING`/`PONG`, explain Serial Monitor.
10. **Experiment 1: Bluetooth / USB remote robot** — objectives, wiring, control flow diagram, pairing on Windows, finding Bluetooth COM port, testing USB and Bluetooth, commands, separate working sketch, section-level annotated explanations, test checklist, challenges, troubleshooting.
11. **Experiment 2: line follower** — track layout, 1-inch black line, two IR mounts, calibration, decision table, loss-of-line recovery, distinct code and explanation, guided testing, challenges, troubleshooting.
12. **Experiment 3: obstacle avoiding** — three IR sensor angles, front/left/right, 5–10 cm target calibrated with potentiometers, decision table, left preference, reverse/U-turn condition, distinct sketch, tuning and troubleshooting.
13. **Calibration & testing** — motor direction, wheel rotation, PWM speed, sensor sensitivity, sensor inverted output, battery voltage effects, expected outcomes, start with wheels lifted, test log template.
14. **Troubleshooting** — no COM port, permission/driver failures, compile/upload errors, Bluetooth paired but no serial COM connection, reset/brownout, USB/external power caution, motor reversed/not moving, IR false detection, off-track movement, mechanical issues.
15. **Downloads** — all three `.ino` files, wiring/pinout SVGs, downloadable lesson Markdown, printable checklists, code change log, PDF-friendly browser-print pages, placeholders for future real photos.
16. **Mini challenges** — class-appropriate modifications, e.g. change robot speed, print a sensor reading, change line-search direction, adjust the preferred turn; include hints and model answers hidden in a teacher/admin section where appropriate.
17. **Quizzes** — small section quizzes and one final quiz (configurable passing criteria); display answers/explanations after submission, save score and attempts.
18. **Progress & certificate** — per-lesson completion, project completion, quiz progress; printable branded certificate only after configurable requirements are met, including student display name, completion date, completion ID. Do not promise official accreditation.
19. **FAQ & support** — common student questions, workshop help contact `[TBD]`, post-workshop modifications/resources.
20. **Admin portal** — create/disable student accounts, optionally reset passwords, view progress/scores and certificate status, manage lesson access and core configuration. Keep admin permissions server-enforced.

Every **robot experiment** should have the consistent chapter sequence: Aim → Equipment → Learn the concept → Assembly/mounting → Wiring table and diagram → Algorithm/decision table → Flowchart → Code download → Small code-section explanations → Upload steps → Run and observe → Calibration → Troubleshooting → Student challenges → Quiz → Completion checklist.

## 6. Three Arduino firmware deliverables

Create a dedicated folder `arduino/` with at least:

- `01_Remote_Control/01_Remote_Control.ino`: `Serial.begin(115200)`, `BluetoothSerial` with a clear device name such as `NAVION_ROBOT`, dual USB and Bluetooth command parsing, `F/B/L/R/S`, nonblocking processing, PWM motor functions, serial feedback and stop-on-disconnect / deadman behavior that does not wrongly stop an active USB session; no phone requirement.
- `02_Line_Follower/02_Line_Follower.ino`: two GPIO inputs, configurable detection polarity, 4-case decision table, motor functions, fixed initial speed, last-known-turn line search, and safe/sensible bounded searching.
- `03_Obstacle_Avoidance/03_Obstacle_Avoidance.ino`: left/front/right sensor inputs, adjustable motor speed and turn time constants, stop on front detection, prefer left if both sides clear, reverse and U-turn on all directions blocked, commented short main loop.

Requirements for all sketches:
- Arduino IDE 2.x and original ESP32-WROOM-32 compatibility; match Arduino-ESP32 core API.
- Motor functions shared in design and behavior, but each `.ino` is independently uploadable. Put relevant config in the sketch (students need not install a separate library).
- No missing symbols or pseudocode; actual compilable C++.
- Clearly declare the *provisional* wiring map and sensor active-level constants; student-accessible tuning constants at the top.
- Section-level comments understandable by classes 6–10, without line-by-line prose for every standard line.
- Do not falsely claim that the IR sensor model or power circuit has been tested.
- Basic motor failsafe, no blocking indefinitely, do not leave motors spinning unintentionally on reset.
- `README.md` beside each sketch with dependencies, wiring, operation, common problems, and exact upload steps.

## 7. Website technology and local-development requirements

- PHP 8.2+ preferred; accessible HTML5, CSS and minimal vanilla JavaScript. Match or cleanly embed in the existing PHP site later.
- Use PHP sessions, secure password hashing and server-side authorization. Avoid hard-coded public default student/admin credentials.
- Use PDO; default **SQLite for localhost** to minimize setup and allow a genuine working MVP. Keep configuration modular so MySQL/MariaDB can be added for the production PHP host without rewriting business logic. Do not claim the production database has been chosen.
- Define configuration for branding, grade range, completion criteria, course content, downloads path and database. Keep credentials in `.env` or ignored config, with a safe `.env.example`.
- Create setup script/CLI for initializing the DB and securely creating the first admin account and demo student account; demo account only for localhost and clearly labelled; never publish real student passwords.
- Implement a simple way for admin to add student accounts before the workshop. Minimize information collected about minors, no public roster or unnecessary analytics.
- Student route protection must cover download endpoints and APIs too. Secure CSRF-protected forms, prepared SQL statements, escaped HTML output, session regeneration at login and rate-limited login attempts where feasible.
- Layout: neutral modern educational design, large readable typography, clear diagrams, side nav, breadcrumbs, progress bar, copy-code button, downloadable files, accessible contrast and keyboard navigation.
- Use actual completed content in a Markdown-based content folder **or** structured PHP content templates; however, the public route must render readable formatted lessons (not a raw Markdown code dump).
- Avoid external paid services and avoid network dependencies for core functionality. Do not require npm if straightforward PHP/CSS suffices.
- For quizzes, store questions/answers server-side so client view source does not expose answers before submission.
- Certificate: printable HTML/CSS A4 certificate with completion ID, date and name; PDF creation via the browser print dialog is acceptable in MVP, with future server-side PDF as `[TBD]`.
- Images/screenshots: use original explanatory SVG diagrams and labelled image placeholders. Do not hallucinate wiring photographs or screenshots.
- Site should be able to run with `php -S localhost:8000 -t public` after setup; write cross-platform Windows PowerShell commands where appropriate.

## 8. Suggested output folder structure

This is a suggested structure; Codex may adjust for good PHP architecture while preserving the deliverables.

```text
navion-robotics-workshop/
├── README.md
├── PROJECT_STATUS.md
├── .env.example
├── .gitignore
├── config/
│   ├── app.php
│   └── robots.php
├── app/
│   ├── auth/
│   ├── controllers/
│   ├── database/
│   ├── helpers/
│   └── views/
├── public/
│   ├── index.php
│   ├── assets/
│   │   ├── css/
│   │   ├── js/
│   │   ├── svg/
│   │   └── images/README.md
│   └── .htaccess
├── content/
│   ├── lessons/
│   ├── quizzes/
│   └── downloads/
├── arduino/
│   ├── 01_Remote_Control/
│   │   ├── 01_Remote_Control.ino
│   │   └── README.md
│   ├── 02_Line_Follower/
│   │   ├── 02_Line_Follower.ino
│   │   └── README.md
│   └── 03_Obstacle_Avoidance/
│       ├── 03_Obstacle_Avoidance.ino
│       └── README.md
├── docs/
│   ├── hardware-bom.md
│   ├── power-assumptions.md
│   ├── gpio-pinout.md
│   ├── student-guide.md
│   ├── teacher-guide.md
│   ├── deployment.md
│   └── sources-and-verification.md
├── scripts/
│   └── setup.php
└── tests/
```

## 9. Verification, sources, and content quality

- Prefer official Arduino IDE, Espressif Arduino-ESP32, Espressif hardware, and the chosen module manufacturer's documentation for setup, APIs, voltage and GPIO cautions. Include exact URLs and access dates in `docs/sources-and-verification.md` if online research is available. If offline, mark links/sources as needing review rather than inventing them.
- Distinguish **user-defined behavior**, **user-approved but unverified electrical/BT assumptions**, **provisional decisions**, and **actual test results** in the status report.
- Ensure L298N jumper instructions do not contradict the chosen L298N-powered ESP32 assumption.
- Clearly explain USB Serial Monitor vs Bluetooth COM port; provide Windows Bluetooth pairing steps without requiring phones or a browser Bluetooth app.
- Ensure the final circuits, wiring tables, code GPIO constants, diagrams and parts list agree.
- Add short student comprehension checks at the end of each major lesson.
- No copied vendor/manufacturer photographs without license; SVG diagrams created for this site are fine.
- Do not state that code was compiled or the site was run unless that action was actually carried out.

## 10. Acceptance checklist for Codex

The project is considered ready for a **local software demo** when:

- [ ] Website folder exists, with setup and run instructions.
- [ ] Student login and admin login work; lessons/downloads are access-controlled.
- [ ] Every course page in Section 5 exists with substantial beginner-friendly content.
- [ ] Dedicated lesson routes for all three robots show correct wiring, algorithm, code, tests and challenges.
- [ ] Three self-contained `.ino` files and accompanying README files exist.
- [ ] GPIO tables, firmware constants and diagrams are synchronized.
- [ ] Two-sensor line following and three-sensor obstacle avoidance logic match the requested behaviors.
- [ ] USB and Bluetooth control instructions are written for Windows laptops only.
- [ ] Student lesson completion, quizzes, dashboard and print-ready certificate are functional.
- [ ] Images/screenshots not yet available are honestly labelled placeholders.
- [ ] PHP syntax and primary flows checked; any Arduino compilation or hardware verification limitations recorded.
- [ ] `PROJECT_STATUS.md` distinguishes completed software from `[ASSUMED]`, `[TBD]`, and `NOT TESTED` hardware.
- [ ] No soldering requirement, buck converter or standalone BMS silently introduced into the BOM.

## 11. Editable decision log — change here when new information arrives

| Topic | Current decision |
|---|---|
| Physical platform | One shared 3D-printed robot chassis reconfigured for each of 3 experiments |
| Students' controller | Windows 10/11 laptop; **no smartphones** |
| Bluetooth | `[ASSUMED — CHANGEABLE]` Windows Bluetooth Classic SPP / COM communication works |
| Power | `[ASSUMED — CHANGEABLE]` 2S 18650 → L298N → onboard 5 V output → ESP32 5V input works; teacher will verify |
| Buck converter | Excluded |
| Battery protection project work | Excluded from kit planning by user; no claim that unprotected cells are safe |
| Motor model | Two 130–280 RPM BO motors rated 3–9 V |
| IR module | Three adjustable three-pin modules; active-low and 3.3 V operation **to be confirmed** |
| Line follower | Black line on white, ~1 inch, sensors flanking line, fixed speed, spin/search on loss |
| Obstacle robot | Left/front/right, ~5–10 cm goal, choose left when both sides clear, reverse + turn around if all blocked |
| Control commands | F/B/L/R/S, optional speed control |
| Website framework | PHP, locally runnable, eventually installed under existing PHP site |
| Access | Registered students; admin controls users |
| Study materials | Full course, three sketches, wiring diagrams, quizzes, progress, certificate, downloads |
| Chassis CAD, school branding, lesson photos, actual GPIO confirmation | `[TBD]` |

## 12. Final instruction to Codex

**Build the project now.** Create the complete runnable website folder and Arduino projects using the decisions above, with reasonable configurable software defaults for unspecified details. Do not block on `[TBD]` photos, chassis dimensions or production hosting. Do **not** replace user-approved assumptions with unsupported claims of hardware verification. Report exactly what works, what was not tested and what the teacher must check on the prototype. Include the exact Windows/PowerShell commands to start the local PHP server and access the demo.
