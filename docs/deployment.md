# Hosting handoff for Jameel

Requires PHP 8.2+ with PDO SQLite and sessions; HTTPS. No npm, Composer or external service required. SQLite is the implemented database; production choice remains open. PDO access is centralized in app/bootstrap.php, but MySQL requires a tested schema/upsert adapter, not merely a DSN change.

## Safe cPanel layout
1. Clone/download the repository to a private directory outside public_html, for example /home/ACCOUNT/navion-workshop. Never put the entire repository in public_html.
2. Prefer configuring the workshop domain/subdomain document root to that directory's public/ folder. For a subfolder on an existing PHP site, copy public/ contents into public_html/workshop/ and change its index.php require to the absolute private app/bootstrap.php path. Assets remain next to index.php. The bootstrap uses its own private root for content/downloads.
3. Set NAVION_DB_PATH to an absolute writable path outside the web root (or keep private storage/). Set NAVION_SECURE_COOKIE=1 under HTTPS. Grant only host-user write access; do not use world-writable permissions.
4. In cPanel Terminal/SSH run `php scripts/setup.php` from the private project root. Enter an admin username and display name. It generates a random password shown only in that terminal: save privately. No browser installer exists. If terminal access is unavailable, ask the host to run this CLI command.
5. Visit /workshop/index.php (or the selected domain), sign in as admin, create students. Do not enable --demo in production. No published defaults exist.
6. Verify unauthenticated requests cannot read lessons or downloads; disable a test student and confirm immediate loss of access. Check certificate rules, quizzes and printing.
7. Back up the private SQLite database using a consistent SQLite backup method; stop writers before a filesystem copy. Restrict backups; define a student data retention period with the organiser.

Never serve config/, content/, arduino/, app/, scripts/, storage/, or the .git directory directly. Downloads are streamed by authenticated allowlisted routes. Existing PHP website home page remains untouched. GitHub Pages does not execute PHP.

## Local PowerShell
Install PHP 8.2+ and enable pdo_sqlite, then:
```powershell
cd 'PATH\TO\navion-robotics-workshop'
php scripts/setup.php
php -S localhost:8000 -t public
```
Open http://localhost:8000. For a local-only demo add `$env:NAVION_LOCAL_DEMO='1'` and run initial setup with `--demo`; generated credentials are never committed. To override DB path, set `$env:NAVION_DB_PATH='C:\private\workshop.sqlite'` before setup/server commands.
