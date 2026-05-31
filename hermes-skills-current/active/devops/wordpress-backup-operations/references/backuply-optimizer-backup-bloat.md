# Backuply optimizer-backup bloat pitfall

Session-derived lesson for large WordPress sites using Backuply, image optimizers, and remote storage.

## Symptom

- Backuply makes progress for hours with repeated `About to call self to prevent timeout`.
- Loop/file count keeps increasing but no fresh `backuply_get_backups_info()` artifact appears.
- Archive size grows into ~8-10GB+ and may time out or fail uploading to Google Drive.
- Log tail shows paths under optimizer backup folders, e.g.:
  - `wp-content/uploads/ShortpixelBackups/wp-content/uploads/...`

## Root cause

Backuply is backing up generated/backup copies of media created by optimizer/cache plugins. These are not primary site content and can double or triple the archive size. Retrying the same monolithic backup is not SOTA; it wastes quota/time and can loop/fail at remote upload.

## Enterprise repair pattern

1. Do not declare success from log-tail text; require a fresh same-site Backuply backup-info artifact.
2. Stop/let expire the bloated run if it is trapped in optimizer backup folders and no artifact appears.
3. Reset stale Backuply status before a clean retry.
4. Add safe exact excludes before retrying:
   - `wp-content/uploads/ShortpixelBackups`
   - `wp-content/cache`
   - `wp-content/wphb-cache`
   - `wp-content/et-cache`
   - `wp-content/litespeed`
   - `wp-content/ai1wm-backups`
   - `wp-content/updraft`
   - `wp-content/backuply/backups`
   - transient logs/tmp files where supported
5. Validate `backuply_settings.backup_location` against configured remote IDs.
6. Rerun one site at a time and track JSONL progress.
7. Mark green only when `backuply_get_backups_info()` contains a new artifact whose `backup_site_url` exactly matches the target domain.

## Reporting discipline

For this user, keep updates terse and stateful:

- `RUNNING`: loop/file count/archive size moving; no artifact yet.
- `VERIFIED`: fresh same-site Backuply artifact exists.
- `FAILED`: explicit Backuply failure or timeout policy hit with no artifact.
- `BLOCKED`: required deployment/control path cannot apply excludes/reset.

Never say “perfectly working” or “successful” unless the fresh same-site artifact exists.