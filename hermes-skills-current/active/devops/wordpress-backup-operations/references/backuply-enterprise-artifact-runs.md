# Backuply Enterprise Artifact Runs

Session-derived pattern for Backuply failures on very large WordPress sites.

## Verification rule

Do not mark Backuply green from log text, progress percentage, or `Backup Successfully Completed|success|100` alone. The pass condition is a fresh `backuply_get_backups_info()` record for the exact child site URL (`backup_site_url`) with the expected DB/files flags, size, name/timestamp, and remote/location.

## Huge-site workflow

1. Stop any stale runner before starting a new one; never stack Backuply starts on top of an active job.
2. Validate `backuply_settings.backup_location` against `backuply_remote_backup_locs` before start. Invalid IDs can make Backuply attempt filesystem-root writes.
3. Repair location, reset stale `backuply_status`, and set `backuply_backup_stopped=false`.
4. Apply sane excludes before retrying large monolithic jobs: Backuply backup folder, cache folders, transient backup folders (`ai1wm-backups`, `updraft`), upgrades, debug/log/tmp artifacts. Avoid excluding real uploads/content unless the user approves a split/non-full backup strategy.
5. Use a keyed local helper/direct executor only when normal cron/admin-ajax/self-calls stall; tick Backuply's own executor and poll status/artifacts between ticks.
6. For 8–10GB+ archives that keep looping or fail upload, switch strategy instead of brute-forcing forever: DB-only first, then files with approved exclusions/chunking or alternate remote.

## Reporting discipline for this user

Keep progress terse. Use states only: `VERIFIED`, `RUNNING`, `FAILED`, `BLOCKED`, `STOPPED`. Include process ID/log path only when useful. Avoid verbose apologies and do not claim success until artifact proof exists.
