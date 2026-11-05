# Combined PHP handoff implementation — 5 November 2026

Revision 3 continues the public PHP 8.2+ manual. No login, database, framework migration, student tracking or browser hardware connection was added.

## Implemented

- Warm workbench styling, 20 px default / 24 px large text (18 px normal on narrow screens), keyboard focus, 44 px controls, teacher view and no-JavaScript mobile navigation.
- Start page with three mode choices; source-derived guided steps, visible power prerequisites, expected results, sketch downloads, Back/Next, free step selection and optional device-local resume/reset. Remote skips sensor calibration.
- Stable subsection anchors and server-side local search with practical symptom synonyms; works without JavaScript.
- Power-state selector; keyboard-operable provisional signal connection viewer using config/robots.php, mode filtering and enlargement. This is a logical map, not a verified physical wiring diagram.
- Calibration worksheet with mixed/unchanging/unstable-input rejection, optional local save, clear, JSON export and printing.
- Branching troubleshooting with Back and teacher handoff; USB/remote Serial Monitor practice; line/obstacle decision simulation with wheel directions, reset, pause, step, playback speed and firmware time limits. Simulations never connect to hardware.
- Corrected wiring HTML nesting and circular motor-test/Bluetooth prerequisite. Displayed full sketches now come from allowlisted actual .ino files; the USB example's stale code was removed.
- Single H1 and adjusted heading hierarchy in the full manual; contents return links, print-code choice, clipboard announcements and selectable fallback.
- Revision manifest, deterministic ZIP with SHA-256 inventory, repository-correct Markdown links, standalone offline HTML with embedded diagrams/sketch downloads, quick cards and a versioned instructions-only PDF. Offline snapshots require a fresh download to update; no service worker.
- CI added for PHP/integration/export checks, browser checks and all five sketches using the manifest's ESP32 core. A workflow definition is not evidence that remote CI has run.

## Verification performed

- tests/smoke.py: public routes, internal links/anchors, allowlisted downloads, invalid requests and PHP syntax; count in tests/manual-results.txt (many checks are repeated link checks).
- tests/browser.py: 99 structural/browser scenarios using installed Edge 156. Widths 320, 360, 620, 749 and 1280 CSS px; normal/large text; no page overflow; public guided USB flow, history/reload/local reset, no-JS navigation, useful search, power/connection selection, mixed/unstable calibration, troubleshooting, PING/newline timeout/baud/deadman simulation, all 4 line and 8 obstacle states, latched stop and copy failure fallback.
- tests/exports.py: all five displayed sketches equal normalized source; repository/offline links, package checksums and reproducibility; isolated split-root /workshop/ installation; missing download 404 and POST 405.
- Browser-rendered print PDFs inspected as page contact sheets; screen screenshots inspected at 360 and 1280 px. Local review artifacts: output/playwright/ (ignored by Git). A 320 px layout checks narrow reflow; actual browser 200%/400% zoom UI and a screen reader were not exercised. No student/teacher usability session occurred.
- Firmware sources were not changed. Historical compilation evidence remains historical; new CI compiles them when run.

## Pending / deliberately separate

1. Genuine kit/assembly photos, IDE screenshots, actual CAD, fastener dimensions and reviewed physical pin placement require supplied references. Screenshot slots state pending. Generated decorative artwork and the optional 3D viewer were not produced; no fabricated evidence was substituted.
2. Teacher must verify voltage/polarity, board exposure, motor direction/fit, regulator stability, USB isolation and Windows Bluetooth Classic SPP on real hardware.
3. Autonomous arming/STOP changes, per-sensor firmware polarity and a compiling code-settings helper are separate firmware work. Current autonomous startup/reset behavior remains unchanged and documented. Physical browser USB control was not added.
4. Live cPanel deployment, independent-domain HTTPS checks, actual printing, full screen-reader/contrast audit and learner review remain outstanding. Local subfolder validation is not proof of production hosting.
5. Guided steps reuse the source text; some safety-heavy and introductory steps remain longer than the 40–80-word target. Exact kit visuals can replace the pending slots after validation.

## Maintenance

Run `python scripts/export_manual.py` with PHP_BINARY set after source changes. Run the three test scripts. Re-render and visually inspect the PDF after content/style changes, replace content/downloads/manual-print.pdf, then export again. Jameel receives ready files and needs only PHP; development Python/browser dependencies are not required on the host.
