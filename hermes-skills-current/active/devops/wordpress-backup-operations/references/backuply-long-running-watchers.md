# Backuply Long-Running Watchers

Session-derived pattern for very large Backuply sites that produce 8–10GB+ archives and sit behind Cloudflare.

## What went wrong

- A Backuply run can keep progressing while REST/status requests intermittently return Cloudflare `524`, blank/non-JSON responses, or socket timeouts.
- Treating those transient read failures as script-fatal crashes loses the orchestration context even though the child backup may still be running.
- Log lines like `Backup Successfully Completed|success|100` are not sufficient proof. A fresh same-site `backuply_get_backups_info()` artifact is the pass condition.
- User-facing progress must be terse and stateful. Do not spam explanations; report `RUNNING`, `VERIFIED`, `FAILED`, `BLOCKED`, or `STOPPED` with the current evidence.

## Recommended watcher behavior

1. Capture the baseline same-site artifact names before starting/resuming.
2. Start or resume only one backup per site. Never stack a second Backuply start on top of a running `backuply_status` job.
3. Use direct executor ticks only when Backuply's cron/admin-ajax self-call path stalls; call the plugin's own executor rather than reimplementing backup logic.
4. Wrap every tick/status call in retry/tolerant error handling:
   - tolerate Cloudflare `524`
   - tolerate socket/read timeouts
   - tolerate blank/non-JSON bodies from long executor requests
   - keep polling instead of exiting unless Backuply log/artifact evidence says failed
5. Persist JSONL progress to disk with at least:
   - site
   - event
   - Backuply job name
   - loop number
   - file count/archive size from log tail when available
   - last log line
   - artifact name/size/location on success
6. Mark success only when a fresh artifact appears whose `backup_site_url` exactly matches the child domain and whose name was not present in the baseline.
7. If the user says stop, kill the background process and report `STOPPED`; do not continue or restart silently.

## Split strategy trigger

If a 9GB+ monolithic full backup repeatedly loops or upload-fails, stop brute force and switch to an enterprise split plan:

- reset stale Backuply state
- validate saved `backup_location` against configured remotes
- exclude cache/temp/old-backup directories (`wp-content/cache`, `backuply/backups`, `updraft`, `ai1wm-backups`, `upgrade`, large logs/tmp)
- run DB-only first when possible
- then run files backup with approved exclusions/chunking
- verify each part by fresh same-site artifact

## Reporting rule

For urgent user interactions, keep it short:

- `RUNNING: affiliate, loop 99, 87,538 files, 9.86GB, no artifact yet.`
- `VERIFIED: gearuptofit, artifact wp_..., size ..., location ...`
- `FAILED: affiliate, Google Drive upload failed; next: split DB/files with exclusions.`
- `STOPPED: process killed on user request; no artifact verified.`
