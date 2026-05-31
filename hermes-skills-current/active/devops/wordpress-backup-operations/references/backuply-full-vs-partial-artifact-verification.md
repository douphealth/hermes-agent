# Backuply Full vs Partial Artifact Verification

Use this when a user asks for **full** WordPress backups across a Backuply fleet, especially after a smaller DB/code safety artifact was produced.

## Core rule

A fresh same-site Backuply artifact is not automatically a full backup. Treat it as `VERIFIED_FULL` only when all of these are true:

- `backup_db=true` and `backup_dir=true`.
- Artifact `backup_site_url` matches the exact domain.
- Artifact is fresh relative to the run start.
- Target remote/location matches the intended Google Drive remote.
- Scope includes media/uploads; `wp-content/uploads` is not excluded.
- Size is plausible compared with historical full artifacts or a current disk/inventory estimate.

If `wp-content/uploads` is excluded, label the result `PARTIAL-VERIFIED` / `PARTIAL_ONLY` even when Backuply reports success.

## Size sanity pattern

1. Before a full run, record historical same-site artifacts from `backup_infos`:
   - name
   - size
   - backup location
   - DB/files flags
2. Establish an expected full-size band from recent full artifacts or file inventory.
3. After completion, compare the fresh artifact size to that band.
4. If the fresh artifact is dramatically smaller, inspect Backuply settings/excludes before reporting success.

Example: if a site historically has 8.1–8.3 GB full artifacts and the fresh artifact is 1.08 GB, it is almost certainly partial unless a deliberate content cleanup happened and was independently verified.

## Exclusion audit

For full backups, generated/cache/old-backup folders may remain excluded, but media must not be excluded:

Safe to exclude when observed:
- `wp-content/cache`
- `wp-content/wphb-cache`
- `wp-content/et-cache`
- `wp-content/litespeed`
- `wp-content/backuply/backups`
- `wp-content/wpvivid_uploads`
- `wp-content/uploads/wpvivid_uploads`
- optimizer backup/cache folders such as `ShortpixelBackups` or `tenweb_image_optimizer`
- `.log` / temporary files if policy allows

Not acceptable for `VERIFIED_FULL`:
- `wp-content/uploads`
- broad rules that match all uploads/media paths

## Fleet execution/reporting

When the user says “full backup for all websites”:

1. Inventory all known sites and current Backuply state.
2. For each site, validate selected Google Drive remote.
3. Remove only broad media/uploads exclusions; keep generated/cache/backup exclusions.
4. Run sequentially unless the user explicitly accepts load risk.
5. Keep statuses terse:
   - `VERIFIED_FULL`
   - `RUNNING`
   - `FAILED`
   - `BLOCKED`
   - `PARTIAL_ONLY`
6. Never mark a site `VERIFIED_FULL` from log-tail success alone or from a fresh artifact with suspiciously small size.

## User-facing pitfall

If the user corrects that “full backup should be ~8GB,” do not defend the previous status. Immediately reclassify the small artifact as partial, cite the fresh and historical sizes, and proceed to full-scope remediation.