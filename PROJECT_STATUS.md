# Current status — revision 3 — 2026-11-05

Implemented the combined PHP handoff software improvements. See [implementation status](docs/IMPLEMENTATION_STATUS.md) for delivered tools, evidence and deferred hardware/media/firmware work. The public manual, guided reader and workbench tools remain PHP + vanilla JavaScript, with no accounts or database. Production deployment has not been performed.

---

## Historical revision 2 record

# Project status — revision 2 — 2026-11-05

## Current scope
User requested a public robot setup user manual. Account/course features have been removed: no authentication, admin, quiz, progress or certificate routes; no database/session dependency. Old account URLs redirect to the manual home and never reveal old account data. The original docs/BUILD_BRIEF.md is retained as historical input and is superseded for access/course requirements.

## Delivered
14 action-oriented chapters, expected results and troubleshooting beside actions, numbered navigation, jump links, public allowlisted downloads, full printable manual, downloadable Markdown manual and complete ZIP pack. Additional serial and sensor diagnostic sketches avoid hand-typing and permit motor-OFF input tests. Existing three robot sketches remain unchanged.

## Important hardware limitations
Assumed 2S → L298N regulator → ESP32 VIN path is NOT physically verified. USB/external 5 V must be isolated with teacher checks. GPIO/module compatibility, actual fasteners, motor fit and Bluetooth Classic Windows serial operation remain unverified. Genuine photos/screenshots pending. Two flanking line sensors cannot uniquely detect loss when both see white: forward/search limits can trigger on a long straight. No rear sensor exists for obstacle reverse. No additional buck converter or BMS was introduced into the BOM.

## Actual verification
Original three robot sketches compiled with Arduino-ESP32 3.3.11 and were unchanged in this revision. Both added diagnostic sketches also compiled successfully against that core/target. Prior 440 checks applied to the superseded course portal only; do not use them as evidence for revision 2. Revision 2 passed 737 software/link/download/anchor/syntax checks, including fresh public access with no existing database or session. Results: tests/manual-results.txt and tests/firmware-results.txt.

Browser review confirmed the current 749-pixel in-app viewport has no horizontal page overflow (document width 732 pixels). Chapter navigation/disclosures, code copy, temporary checkboxes, complete-manual contents and public entry were exercised. The sub-620-pixel mobile breakpoint, full accessibility compliance, actual PDF output/physical printing and hardware testing remain unverified. Local student-perspective screenshot review was saved beside the workspace under tmp/manual-review/student-review.html.
