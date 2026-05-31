# Backuply strict-full GDrive failure and server-runner cutover

## Trigger

Use this pattern when strict Backuply scope is correct (`wp-content/uploads` included; only static `wp-content/backuply/backups` excluded) but Backuply still cannot produce trustworthy all-site full backup proof.

Common evidence:

- Fresh Backuply artifact has `backup_db=1` and `backup_dir=1`, but `size=false` / archive size `n/a`.
- Tail contains `Google Drive : 100 Continue`, `Unable to resume upload as upload session expired`, `Upload failed after trying 3 times`, or `Upload Failed! Because the file is not present on the server`.
- A fresh artifact is much smaller than current uploads inventory or historical same-site full artifacts.
- Backuply UI/log says `Backup Successfully Completed`, but the tail also contains upload errors or missing temp-file errors.

## Decision rule

Do **not** keep brute-forcing strict Backuply full runs when the blocker is monolithic Google Drive upload reliability.

State labels:

- `SCOPE_NEEDS_PROOF`: fresh artifact exists but size is implausibly small vs uploads inventory/historical full.
- `FAILED`: upload/session/file-missing errors appear in the final tail, even if Backuply also logs success.
- `FRESH_ARTIFACT_SIZE_UNKNOWN`: size metadata is false/`n/a`; do not mark hard DR green without independent remote/offsite size proof.
- `VERIFIED_FULL`: only when fresh same-site artifact exists, root uploads is included, no final-tail upload errors exist, and size is plausible or independently proven.

## Cutover path

When several sites fail this way, stop treating Backuply as the DR mechanism and switch to a WordPress-side/server-side chunked runner:

1. Stop server-side Backuply jobs; verify inactive status.
2. Deploy/use locked helper endpoint or server-side access.
3. Create separate artifacts:
   - DB dump via `mysqldump` under `bash -o pipefail`.
   - Code/config tar excluding uploads/cache/backup/log junk.
   - Uploads/media tar or rsync mirror separately.
4. Split large media archives into parts before transfer/offsite upload.
5. Generate SHA256 checksums for every artifact/part.
6. Verify locally/offsite by reassembly and checksum before claiming disaster-recovery green.

## Watcher pitfall

A fleet runner must not mark `VERIFIED_FULL` for a fresh Backuply artifact with `size=false` when an expected/historical full size exists. If size metadata fails to hydrate, require an independent remote/offsite size proof or keep the status as `FRESH_ARTIFACT_SIZE_UNKNOWN` / `SCOPE_NEEDS_PROOF`.

Also sort same-site artifacts by `btime`, not list order, when reporting the freshest artifact. Backuply/remote artifact arrays may not be newest-last.