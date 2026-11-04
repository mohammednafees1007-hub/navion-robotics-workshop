# Public manual checks

Run `python tests/smoke.py` with PHP 8.2+ on PATH, or set `PHP_BINARY` to php.exe. It starts a temporary server on an unused port with a deliberately nonexistent database path. Checks: chapter pages, internal links/anchors, public downloads, ZIP contents, legacy redirects, invalid paths, lack of account/session/database dependencies and PHP syntax. Results: manual-results.txt.

Visual review uses current browser screenshots at the current in-app/laptop viewport, including navigation, overflow, code copy and printing. Hardware results are not inferred from these checks.
