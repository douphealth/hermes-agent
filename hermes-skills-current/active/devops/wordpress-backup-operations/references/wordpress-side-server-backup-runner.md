# WordPress-side server backup runner fallback

Use this when CyberPanel/hosting backup, Backuply, and WPvivid all fail or create CPU-heavy monolithic jobs, and SSH/CyberPanel Terminal is unavailable or blocked by 2FA.

## Trigger

- Huge WordPress site stalls in plugin backup at DB dump/archive phases.
- CyberPanel backup is monolithic and fails or spikes CPU.
- CyberPanel login requires 2FA or there is no visible Terminal option.
- MainWP is still able to install/update plugins on the child site.

## Pattern

1. Stabilize first: stop Backuply/plugin-side archive loops if active; do not stack more backup jobs.
2. Deploy a temporary locked helper plugin through MainWP install/update.
3. Expose minimal REST endpoints:
   - `GET /wp-json/<namespace>/status?key=...`
   - `POST /wp-json/<namespace>/start` with `key` and `scope`.
4. Keep the helper key private and hardcoded/generated for the session; do not print it in user-facing output.
5. Store backups outside public `uploads` and preferably outside `public_html`:
   - Good: `/home/<site>/hermes-enterprise-backups/<timestamp>`
   - Avoid: `wp-content/uploads/...` because a full media mirror can recursively copy the backup itself.
6. Use server-native tools from PHP `system()` rather than plugin backup internals:
   - DB: `mysqldump --single-transaction --quick --skip-lock-tables --no-tablespaces --default-character-set=utf8mb4 --hex-blob --routines --events --triggers --max_allowed_packet=512M`
   - Code/config: `tar`, excluding uploads/cache/backup/log folders.
   - Media: `rsync -aH --numeric-ids --delete`, excluding optimizer backups/cache/old backup folders.
7. Poll the REST `status` endpoint for report tail and artifact sizes; report terse `RUNNING`, `VERIFIED_FULL`, `VERIFIED_DB_CODE`, `FAILED`.
8. Verify by artifacts and checksums, not by request success.

## Pitfalls

- PHP request timeout can occur while the server-side process continues. Treat client timeout as `START_DETACHED`, then poll status.
- `mysqldump ... | gzip` can produce a tiny valid gzip (about 20 bytes) if `mysqldump` failed and shell pipeline errors are hidden. Run under `bash -o pipefail`, capture stderr, and reject DB artifacts below a sane minimum (for large sites, `<1024` bytes is definitely invalid).
- WordPress `DB_HOST` can be `localhost:3306`. Split host and port for `mysqldump` (`-h localhost -P 3306`) instead of passing `localhost:3306` as the host.
- Passing MySQL passwords as `-p'<password>'` can be brittle in generated shell commands. Prefer `MYSQL_PWD=[REDACTED] in the command environment plus `-u <user>`.
- `tar` may return `1` when files change during archive creation. If the archive exists and has expected size, treat as warning, but still preserve the return code in the report.
- If a DB dump remains at `DB_START` for a long time with no artifact-size visibility, add status output that reports current file sizes/counts before deciding to stop or continue.
- Do not call a backup `VERIFIED_FULL` until DB dump, code archive, media mirror, and checksum steps complete. If only DB+code are complete, report `VERIFIED_DB_CODE` and say media is not yet covered.

## User-facing style for urgent backup repair

Keep updates short and state-labeled. The user may be stressed by failed backups and CPU spikes; avoid long explanations while active remediation is underway. Preferred format:

- `AFS: VERIFIED_FULL — path ...`
- `Gear: RUNNING — phase DB_START`
- `Next: ...`

Avoid repeating manual instructions after an automated fallback is available; act through MainWP/helper paths first.