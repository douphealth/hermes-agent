# CyberPanel Cron and File Manager as Emergency WordPress Repair Channels

Use this reference when repairing WordPress backup/runtime failures where wp-admin, REST, SSH, or FTP are unavailable but CyberPanel is reachable.

## Why it matters

A critical WordPress fatal can block REST, wp-admin, plugin deactivation, and backup plugin control paths. CyberPanel may still provide two useful server-side channels:

- File Manager `/filemanager/controller` for read/write/delete operations.
- Cron management for one-shot shell commands that execute as the website user.

This is useful for backup repair too: disabling a fatal MU-plugin, clearing public debug logs, or restoring a helper file can bring the site back enough for normal backup verification.

## Safe pattern

1. Verify the fatal source with the smallest log read possible; redact secrets.
2. If the file is an MU-plugin fatal, rename it out of `.php` execution first.
3. Add a `* * * * *` CyberPanel cron only for commands that need shell execution.
4. Wait one minute, verify the result, then remove the cron immediately.
5. Confirm cron list is empty before reporting done.
6. Continue cleanup: disable debug display, remove public debug logs, and verify public log URLs are gone/denied.

## Evidence checklist

- Homepage `200`.
- `/wp-login.php` reachable or redirects as expected.
- `/wp-json/wp/v2/posts?per_page=1` returns JSON if WordPress bootstrap is healthy.
- No fresh fatal in tail of logs.
- Temporary cron list empty.
- Public `debug.log` / `error_log` returns `404` or `403`.

## Reporting style

For urgent outage/backups work, use terse status labels and evidence. Avoid long narrative while the site is down.

- `FIXED`: exact status checks passed.
- `CLEANED`: debug/log/cron cleanup complete.
- `BLOCKED`: exact missing access or 2FA requirement.
- `PENDING`: only if verification cannot be completed.