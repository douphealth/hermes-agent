# Backuply generated-folder writeHeader failures

## Trigger

Use this when Backuply reaches high progress or `100%` in the wp-admin modal but then prints errors like:

- `Failed to write to the backup file. Please check you have enough disk quota available.`
- `Unable to writeHeader`
- `The backup utility could not back up the files.`

The paths printed immediately before those messages are usually the next folders Backuply tried to add to its local archive before uploading to the remote. The selected destination can still be Google Drive; Backuply still creates/writes a local archive first.

## Correct interpretation

- UI progress is not success.
- A 100% modal with `Backup failed` is `FAILED`, not nearly-success.
- Do not claim fixed from helper deployment, exclusions, log movement, or a modal percentage.
- Only a fresh same-site `backuply_get_backups_info()` artifact is `VERIFIED`.

## Immediate response pattern

1. Stop stale local watcher/direct-executor process so it does not keep ticking a known-bad job.
2. Extract every path shown in the modal/log near `Unable to writeHeader`.
3. Add exact excludes for those paths plus known generated backup/cache folders.
4. Reset Backuply state (`backuply_status`, stopped flag) before restart.
5. Redeploy helper/control plugin if needed and verify child helper version + exclude list live on the child site.
6. Start one clean backup run and watch for fresh same-site artifact only.

## Common exact excludes

Use exact `WP_CONTENT_DIR`-relative paths when present:

- `backuply/backups`
- `cache`
- `wphb-cache`
- `et-cache`
- `litespeed`
- `wp-rocket-config`
- `ai1wm-backups`
- `updraft`
- `upgrade`
- `debug.log`
- `uploads/ShortpixelBackups`
- `uploads/shortpixelBackups`
- `uploads/shortpixel-backups`
- `uploads/tenweb_image_optimizer`
- `wflogs`
- `wpvivid_uploads`
- `uploads/wpvivid_uploads`
- `uploads/backup`
- `uploads/backups`
- `uploads/backup-guard`
- `uploads/ithemes-security`
- `uploads/sucuri`
- `uploads/seraphinite-accelerator`
- `uploads/elementor/tmp`

Also exclude extensions like `log` and `tmp` when supported.

## User-facing state labels

For urgent backup repair sessions, be terse and exact:

- `RUNNING`: backup is active, no fresh artifact yet.
- `FAILED`: UI/log explicitly failed or watcher exits without artifact.
- `VERIFIED`: fresh same-site Backuply artifact exists.
- `BLOCKED`: cannot proceed without credential/storage/server action.

Avoid saying “fixed”, “done”, or “working” until `VERIFIED`.
