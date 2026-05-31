# Backuply Direct Executor Recovery Pattern

Session-derived pattern for large WordPress sites where Backuply accepts a start request but stalls at cron/self-call phases or where log success does not produce a backup-info artifact.

## Trigger

Use this pattern when:

- Backuply starts but remains at `Creating cron job`, `About to call self to prevent timeout`, or repeated archive loops.
- `admin-ajax.php?action=backuply_handle_backup` is unreliable because it needs a logged-in capability cookie, is blocked by Cloudflare, or does not run from REST automation.
- Logs show apparent completion or upload progress, but `backuply_get_backups_info()` has no fresh same-site artifact.
- The saved Backuply `backup_location` is invalid or points to a missing remote location ID.

## Key lessons

- Treat Backuply log strings as progress only, not final proof. The green condition is a fresh `backuply_get_backups_info()` entry filtered to the exact `backup_site_url`.
- Before retrying, compare `backuply_settings.backup_location` to configured keys in `backuply_remote_backup_locs`. Repair the setting first if it points to a non-existent ID.
- Backuply may create a very large local archive before upload; huge sites can spend a long time in archive loops. Report the state as `running` with loop/file-count/archive-size evidence, not `success`.
- If a 9GB+ monolithic full backup repeatedly fails at Google Drive upload, switch to split strategy instead of endlessly retrying: DB-only first, then files with exclusions/chunking, then remote/artifact verification.

## Direct executor approach

When normal cron/ajax execution is unreliable, deploy a small site-local helper plugin through MainWP or another trusted child-site channel. The helper should:

1. Harden runtime for Backuply requests: high `memory_limit`, `WP_MAX_MEMORY_LIMIT`, `max_execution_time`, `max_input_time`, `default_socket_timeout`, and `backuply_backup_self_timeout`.
2. Expose a keyed status endpoint returning sanitized Backuply runtime state, `backuply_settings`, remote location IDs, log tail, and `backuply_get_backups_info()`.
3. Expose a keyed location-repair endpoint that updates `backuply_settings.backup_location` to a valid configured remote ID.
4. Expose a keyed direct-tick endpoint that loads Backuply and calls its own executor (`backuply_backup_execute()` where available) without relying on a browser cookie or wp-cron.
5. Run one site at a time. Between ticks, poll status and stop only on fresh same-site artifact or explicit Backuply failure.

## Verification states to report

- `artifact_success`: fresh same-site `backuply_get_backups_info()` record exists, with expected DB/files flags, timestamp/name, size, and remote location.
- `running`: Backuply status/logs show an active job, but no fresh artifact yet. Include backup name, loop number, file count, archive size, and last log.
- `failed`: explicit `Backup failed|error|100`, provider upload error, or process exit with no artifact after Backuply reports failure.
- `blocked`: Backuply Pro inactive for remote backup requirement, no valid remote ID, permissions prevent helper deployment, or storage quota/auth is invalid.

## Reporting pitfall

For this user's WordPress backup work, never phrase a site as successful from log-tail completion alone. Use blunt labels: `VERIFIED`, `RUNNING`, `FAILED`, or `BLOCKED`. If no fresh artifact exists, say so plainly.