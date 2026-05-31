# Backuply Full Media Fleet Runs

Use when the user wants **full** WordPress backups across a Backuply fleet: database + code/config + media/uploads, uploaded to Google Drive/offsite, with artifact-size verification.

## Key lesson

A Backuply artifact with `backup_db=true` and `backup_dir=true` can still be **partial** if the current exclusions contain the root `wp-content/uploads` directory. Historical size comparison is mandatory for full-backup claims.

## Correct status labels

- `VERIFIED_FULL` — fresh same-site artifact, DB+files, correct target remote, root uploads not excluded, and size is plausible vs historical/expected full size.
- `PARTIAL_ONLY` — fresh artifact exists but root uploads/media are excluded or size is dramatically smaller than historical full backups.
- `RUNNING_FULL` — full-scope job active and logs are moving.
- `FAILED` — explicit Backuply failure/error tail.
- `BLOCKED` — helper/admin access missing, Cloudflare/admin login blocked, or no safe automation channel.

## Efficient full-scope pattern

1. Read exact current Backuply status and artifacts filtered by same `backup_site_url`.
2. Compute expected full size from historical same-site artifacts when available.
3. Before starting, verify:
   - selected remote is the desired Google Drive target (`gdrive-pasalexios` / `pasalexios-gdrive` when present),
   - DB + files are selected,
   - root `wp-content/uploads` is **not** excluded,
   - generated junk is excluded.
4. If a stale Backuply job is active with wrong scope/exclusions, stop it explicitly server-side before restarting. Killing a local watcher is not enough.
5. Start one site at a time. Trigger Backuply ticks/wp-cron but do not stack starts.
6. Verify by fresh same-site artifact and size sanity check; logs alone are weak evidence.

## Safe exclusions for full backups

For full backups, exclude generated/duplicative paths but not the media root:

- `wp-content/backuply/backups`
- `wp-content/cache`, `wphb-cache`, `et-cache`, `litespeed`, `wp-rocket-config`
- `wp-content/ai1wm-backups`, `updraft`, `wpvividbackups`, `wpvivid_uploads`, `uploads/wpvivid_uploads`
- `wp-content/upgrade`, `debug.log`, `wflogs`
- optimizer/temp folders under uploads such as `uploads/ShortpixelBackups`, `uploads/tenweb_image_optimizer`, `uploads/elementor/css`, `uploads/elementor/tmp`, `uploads/seraphinite-accelerator`

Do **not** exclude root `wp-content/uploads` when the user asked for full backups.

## Helper/controller pattern

When existing Backuply helpers cannot safely express full-scope excludes, install a small controlled WordPress plugin/helper that exposes endpoints to:

- report runtime/status/artifacts/log tail;
- prepare settings for full scope;
- set the target Backuply remote location;
- replace exclusions with safe generated-folder exclusions only;
- start Backuply;
- tick Backuply executor/wp-cron;
- stop stale active jobs.

Expose a versioned route (for example `/wp-json/hermes-backuply-full2/v1/...`) so old helper code can coexist and new runners can prefer the newer route. Verify the exact route/version after installation; WordPress may keep an older plugin active if the destination folder already exists.

## Pitfalls

- String-searching for `wp-content/uploads` in exclusions is too broad because safe generated subfolders under uploads contain that prefix. Detect only exact/root uploads exclusions (path ends with `/wp-content/uploads`).
- `Backup Successfully Completed` plus a 1 GB artifact is not a full success if historical full size is 8 GB.
- If updating an already-installed helper ZIP reports unclear status, verify by route/version, not the install page text.
- Cloudflare/wp-login blocks may require origin-IP + Host-header admin upload or an alternate existing helper route; still verify the public REST route after deployment.
- Do not leave a wrong-scope job running just because it is making progress; stop stale/wrong-scope server-side, then restart with full scope.
