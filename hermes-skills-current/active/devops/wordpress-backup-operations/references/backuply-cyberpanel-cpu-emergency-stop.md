# Backuply + CyberPanel CPU Emergency Pattern

## Trigger

Use this when a CyberPanel site shows sustained high CPU during Backuply repair or manual backup attempts, especially on large WordPress sites.

## Durable lesson

Do not interpret high CyberPanel CPU as only a hosting/server problem. During Backuply runs it can be self-inflicted by Backuply archive loops and self-calls:

- `About to call self to prevent timeout`
- rising `backuply_status.loop`
- repeated `Adding to the archive`
- tens of thousands of files added
- multi-GB archive growth
- no fresh `backuply_get_backups_info()` artifact yet

This can keep PHP workers hot even after the external watcher is killed, because Backuply may continue server-side via self-calls/wp-cron-like continuation.

## Required emergency sequence

1. Stop local/background Hermes runner first so no new ticks are sent.
2. Check live Backuply status and log tail, not just local process state.
3. If Backuply is still looping, stop the child-site job server-side:
   - set `backuply_backup_stopped=true`
   - delete `backuply_status`
   - log an explicit stop marker if possible
4. Verify status is empty/stopped and log tail contains stop confirmation such as:
   - `Stopping your backup`
   - `Cleaning the backup folder`
   - `Backup Successfully Stopped`
5. Only then tell the user the load source was stopped.

## Reporting rule for this user

Use terse state labels. Do not defend prior actions. Say exactly:

- `CPU CAUSE CONFIRMED: Backuply archive loop`
- `STOPPED: local runner`
- `STOPPED: server-side Backuply job`
- `NOT VERIFIED: no fresh artifact`

## SOTA remediation after stop

For huge WordPress sites, do not immediately retry a full Backuply monolithic archive. First split strategy:

- Backuply DB + code/config/plugin/theme artifact first.
- Exclude massive media/uploads/cache/optimizer/old-backup folders.
- Handle `wp-content/uploads`/media separately through rsync/object storage/chunked tooling or a host-native backup path.
- Only call a site fully protected when DB/code and media paths are both verified.

## Pitfalls

- Killing the Hermes background process is insufficient if Backuply already scheduled/self-called itself.
- UI progress percentages are weak evidence; they can coexist with high CPU and no artifact.
- A fresh Backuply helper deployment is not a fix; only a fresh same-site artifact proves backup success.
