# Navion Robotics · Robot Setup & User Manual

Public, step-by-step instructions for one ESP32 chassis and three robot modes. **No login, admin, quizzes, certificates or database.** The latest user request supersedes those parts of the original build brief.

14 practical chapters: start, kit, assembly, Windows software, first USB upload, base wiring, motor direction/stop test, sensor calibration, laptop remote control, line following, obstacle avoidance, troubleshooting, shutdown and reference. Each chapter gives prerequisites, actions, expected results and recovery advice.

## Run locally
PHP 8.2+; no extra package, database, npm or Composer.
```powershell
php -S localhost:8000 -t public
```
Open http://localhost:8000. Everything is publicly readable. [Jameel's hosting guide](docs/deployment.md).

## User manual & sketches
- [Detailed user manual](docs/USER_MANUAL.md) or open `?page=manual` and Print → Save as PDF.
- [Complete setup pack](content/downloads/robot-setup-pack.zip): manual, all five sketch folders, README files, original provisional diagrams and checklist.
- Three robot mode sketches plus motor-OFF USB and IR diagnostic sketches, each directly uploadable from Arduino IDE.
- Content: content/manual/*.html and content/manual.json. Run `python scripts/export_manual.py` after content edits to regenerate text/ZIP downloads.

[Verification status](PROJECT_STATUS.md). Hardware fit, IR polarity/voltage, assumed regulator power path and Windows Bluetooth COM operation still require prototype checks. No fabricated photos or physical test claims. The conservative two-sensor line algorithm has a documented centered/lost ambiguity.
