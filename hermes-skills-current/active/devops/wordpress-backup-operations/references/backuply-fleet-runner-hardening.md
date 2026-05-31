# Backuply fleet runner hardening notes

Use this reference when orchestrating multi-site Backuply runs to Google Drive or another remote target.

## Core lesson

A fleet runner must distinguish **server-side Backuply job state** from **local watcher state**. Killing or crashing a Hermes/background process does not stop a WordPress-side Backuply job. Conversely, a local watcher can stall even after the site backup succeeded if its pass criteria are too strict for that helper version.

## Runner pattern

1. Inventory each site first:
   - `backuply_active`, `backuply_pro_active`
   - current `backuply_settings.backup_location`
   - configured remote location IDs/names/protocols
   - `last_backup`
   - `status` / `status_active`
   - log tail
   - `backup_infos` support and whether records include `backup_site_url`
2. Run sites sequentially unless the user explicitly accepts load/quota risk.
3. Force the intended remote by ID only after confirming that ID exists in `backuply_remote_backup_locs`.
4. Persist progress to JSONL with event labels: `PRE`, `START`, `POLL`, `VERIFIED`, `FAILED`, `RETRY`, `SUMMARY`.
5. Use a fresh baseline per site: previous `last_backup` plus pre-run same-site artifact names.
6. Poll both the helper endpoint and `wp-cron.php`; if a helper exposes a direct executor/tick route, call it between polls.
7. Retry failures only after a short cooldown and after verifying no Backuply job remains active.

## Pass criteria by helper capability

Prefer strongest available evidence:

1. **Strongest:** fresh same-site `backup_infos` record with:
   - `backup_site_url` exactly matching the child domain
   - new backup name/timestamp not present before the run
   - `backup_db=true`
   - `backup_dir=true`
   - expected remote/location ID
   - plausible nonzero size
2. **Medium:** `last_backup` advanced after the baseline, Backuply is inactive, and log tail ends with `Backup Successfully Completed`. Use only when the helper does not expose artifact records or the plugin omits same-site info.
3. **Weak/not enough:** progress bar at 100%, `Uploaded till ... / ...`, or a UI modal without a fresh artifact/advanced `last_backup`.

If a site exposes `backup_infos`, do not ignore it. If a site does **not** expose `backup_infos`, do not leave a verifier stuck forever waiting for artifacts; use `last_backup + completed log + inactive` as the best available proof and label the evidence level.

## Common failure modes

- **Google Drive `100 Continue` then `Backup failed`:** treat as failure unless a fresh artifact exists. Retry the same/alternate valid remote once; if it repeats, report provider-upload failure with the archive size.
- **Memory exhaustion:** increase effective Backuply runtime memory/time from inside the WordPress request context, reduce generated-folder bloat, and avoid repeatedly starting the same failing job.
- **Watcher stuck after visible success:** check live status directly. If `active=false`, `last_backup` advanced, and completed log is present, kill the stuck watcher and continue with corrected criteria.
- **Shared remote folders:** backup info can include records for multiple domains; filter by exact `backup_site_url` before marking green.
- **Stale old failure tails:** compare against fresh baseline. Old log errors are not proof the current run failed unless they occur after the new start time/status.

## Reporting standard

Use terse labels:

- `VERIFIED_FULL` — fresh artifact or accepted medium proof confirms DB + files.
- `RUNNING` — active Backuply status with moving logs/counters.
- `FAILED` — inactive with explicit Backuply error and no fresh evidence.
- `BLOCKED` — no route/auth/remote capability to continue.
- `PARTIAL-VERIFIED` — DB/code/config or media-excluded fallback only.

For each site, include evidence level, remote location name/ID, archive size if available, `last_backup` if used, and the exact next action for failures.