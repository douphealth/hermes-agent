# MainWP + WPvivid Enterprise Backup Repair Notes

Session-derived notes for future MainWP/WPvivid fleet backup repair. Keep these as patterns, not as fixed site state.

## Durable lessons

- Do not reauthorize Google Drive first just because Drive only shows one site's backup. Separate: OAuth/remote exists, selected remote destination, task prepare, task start, child-site execution, upload, and remote object visibility.
- MainWP's WPvivid cache can have remote entries and token history while `remote_selected` is empty. If `history.remote_selected` contains the intended Google Drive remote ID and live child remote check returns `googledrive`, restore `remote_selected` before rerunning backups.
- WPvivid/MainWP task payloads can contain OAuth token fields; redact anything named token/secret/password/client/auth/credential/key/refresh/access before logging.
- Run fleet repairs one site at a time. Bulk runs hide which child failed and can leave multiple `no_responds` tasks.

## Payload pitfall

For a MainWP/WPvivid manual database + files backup, the working UI-compatible backup selector is:

```text
backup_files = files+db
local = 0
remote = 1
ismerge = 1
lock = 0
```

A value like `backup_files=all` can be accepted by WPvivid and may quickly report `completed`, but it can produce no new backup-list artifact. Treat that as fake success unless a new backup entry appears.

## Verification standard

Weak evidence:

- `result: success` from prepare/start
- task status `completed`

Strong evidence:

- a new backup-list entry whose ID matches the task ID or expected site prefix/timestamp
- `type: Manual`
- `remote: true`
- remote storage files/parts visible with matching site prefix and approximate size

If `start_backup` returns a MainWP Child reachability/error after a long call, do not immediately mark the backup failed. WPvivid may have already launched the child-side async task. Poll `wpvivid_get_status_mainwp` out-of-band for the task ID and verify whether it is progressing.

## Stuck tasks

Symptoms:

- `status: no_responds`
- long-running `running` at a fixed percent such as 13%
- message: `backup_db is not responding`
- cancel says `force cancel?` or `will be canceled after current chunk ends` but the task remains active

Safe sequence:

1. Push conservative settings and ensure selected remote is correct.
2. Attempt normal cancel.
3. Attempt force-cancel variants if supported.
4. Re-audit task state.
5. If still active, do not stack a new backup; perform child-side WPvivid task-state cleanup or plugin repair first.

## Resource failures

A PHP fatal in `wp-includes/class-wpdb.php` during DB dump means the child server cannot dump the database with current WPvivid method/workload. Even `512M` memory may be insufficient for large `wp_posts`/database tables.

Mitigations to try one at a time:

- raise PHP memory beyond 512M where hosting allows
- reduce WPvivid database/file chunk sizes and per-request workload
- switch DB dump/connect method away from WPDB if the installed WPvivid version supports it
- split backup into DB-only and files-only to isolate the failing layer
- avoid concurrent backups on the same hosting account
