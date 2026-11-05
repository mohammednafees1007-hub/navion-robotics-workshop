# Hosting handoff for Jameel — public manual (revision 3)

The site now contains a public practical robot setup manual. Login, users, quizzes, progress, certificates, admin and database setup have been removed at the user's request. No student data is collected. PHP 8.2+ only; PDO SQLite, npm and Composer are not needed.

## Standalone domain/subdomain
1. Clone/download this repository into a private application directory.
2. Point the domain/subdomain document root at its public/ directory.
3. Enable HTTPS on the host. Visit index.php. There is no setup command, database or account to create.

## Existing PHP website subfolder
Keep app/, config/, content/, arduino/ and docs/ outside public_html. Copy public/ contents to public_html/workshop/. Change its index.php bootstrap require to the absolute private app/bootstrap.php path. Keep assets/ beside index.php. Do not replace the existing website home page.

Serve only public/. Public downloads are intentionally allowlisted by PHP; do not expose .git/, private host files or any old student database. Legacy local demo data is not used by this version and must not be uploaded. GitHub Pages cannot execute PHP.

## Run locally (PowerShell)
```powershell
cd 'PATH\TO\navion-robotics-workshop'
php -S localhost:8000 -t public
```
Open http://localhost:8000. No login or installation is required. Content: content/manual/*.html; chapter metadata: content/manual.json; GPIO reference: config/robots.php. If chapter text changes, regenerate docs/USER_MANUAL.md and the ZIP with scripts/export_manual.py so downloads match the site.

## Before publishing
Check home, all chapter links, full-manual printing and all downloads in a fresh browser. Original electrical/Bluetooth assumptions remain unverified; teacher validates actual hardware before classroom use.

## Revision 3 tools and delivery
Guided setup, search and workbench tools are public. Optional reading bookmarks and worksheet notes stay in the browser on that device; Reset/Clear removes them. No student records reach the PHP server.

The ZIP now contains a standalone offline HTML manual, PDF, quick cards, Markdown, sketches, diagrams, revision metadata and SHA-256 inventory. Download a fresh copy after updates. Offline HTML opens directly without PHP. The PDF contains instructions only; the online full-manual print control can include code.

Local verification reproduced split-root `/workshop/` hosting, but the actual cPanel host and independent-domain HTTPS deployment remain untested. See IMPLEMENTATION_STATUS.md for checks and hardware limitations.
