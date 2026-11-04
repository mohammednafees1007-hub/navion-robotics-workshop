# Navion Robotics · Robotics Workshop

A PHP student learning portal for one ESP32 chassis and three experiments. Private student accounts, admin management, 15 substantial lesson routes, quizzes, progress, authenticated downloads, printable completion certificates and three self-contained Arduino sketches. No phones, browser robot control, payment or public registration.

## Run locally
PHP 8.2+, PDO SQLite, sessions. No npm/Composer.
```powershell
php scripts/setup.php
php -S localhost:8000 -t public
```
Open http://localhost:8000. Setup generates the first admin password locally; no public default credentials. Admin creates students. For initial local demo setup only: set NAVION_LOCAL_DEMO=1 and add --demo.

**Jameel: start with [docs/deployment.md](docs/deployment.md).** Serve only public/, keep the database and application outside public_html, enable HTTPS. GitHub Pages cannot run this PHP application.

See [PROJECT_STATUS.md](PROJECT_STATUS.md), [teacher guide](docs/teacher-guide.md), [power assumptions](docs/power-assumptions.md), [pinout](docs/gpio-pinout.md) and [sources](docs/sources-and-verification.md).

Brand/support/grade defaults: config/app.php. GPIO source: config/robots.php and matching standalone firmware constants. Pass criteria and lesson access: Admin. Lesson content: content/lessons/*.html; downloadable text: content/downloads/. Quiz answers remain outside public/. Original SVG diagrams are editable. Real logo/photos/screenshots remain labelled placeholders.
