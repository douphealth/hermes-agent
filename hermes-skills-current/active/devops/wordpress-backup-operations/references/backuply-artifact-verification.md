# Backuply Artifact-Based Verification Notes

Use these notes when Backuply logs, MainWP responses, or UI status appear successful but the user needs real backup proof.

## Core lesson

Backuply log lines are not sufficient proof. `Backup Successfully Completed|success|100` can appear in a log tail while the actual visible Backuply backup-info artifact is absent, stale, cross-site, or followed by provider/upload failure. Treat log success as a progress signal only.

## Strong success criteria

A Backuply backup is verified only when all of the following are true:

1. A fresh backup-info record exists via Backuply's own artifact source, e.g. `backuply_get_backups_info()` or the Backuply backup list.
2. The artifact's `backup_site_url` exactly matches the child site being verified.
3. The artifact name/timestamp is newer than the baseline collected before the run.
4. The artifact has expected DB/files flags (`backup_db`, `backup_dir`) and a non-trivial size.
5. The artifact's `backup_location` matches a configured remote/location ID if remote backup is expected.
6. Provider/upload logs do not end in failure after artifact creation.

## Backuply pitfalls observed

- Shared or synced remote folders can make a site list backup-info records from other domains. Always filter by exact `backup_site_url` before counting success.
- A saved `backuply_settings.backup_location` can point to an ID that is not present in `backuply_remote_backup_locs`. In that state Backuply may try to write an archive at filesystem root, e.g. `/.wp_example.com_YYYY-MM-DD_HH-MM-SS.tar.gz`, then fail with `Unable to open in write mode`.
- Upload percentages are not final proof. A Google Drive run can reach high percentages and then fail with messages like `Google Drive : 100 Continue` followed by `Backup failed|error|100`.
- `backuply_active()`/active-status checks may flicker false between self-calls or cron continuations. Use log movement and artifact creation to determine real progress, but still require artifact proof for success.

## Recommended workflow

1. Capture baseline backup-info artifacts for the exact domain before starting a run.
2. Validate the selected location ID exists in configured remotes.
3. Start only one site at a time.
4. Poll status/logs for progress and failures.
5. After completion, re-read backup-info records and compare against the baseline.
6. Report one of:
   - `ARTIFACT_SUCCESS`: fresh same-site artifact exists.
   - `LOG_FAILED_NO_ARTIFACT`: Backuply/provider log failed and no fresh artifact exists.
   - `LOG_SUCCESS_NO_ARTIFACT`: log says success but no fresh same-site artifact exists; do not call this successful.
   - `RUNNING`: still moving, no final artifact/failure yet.

## Reporting rule

For users who demand fleet backup proof, never mark a site green from MainWP plugin-install success, runtime tuning success, upload percentage, or a Backuply success log alone. Green means fresh same-site Backuply artifact and, where possible, remote/provider visibility.
