# Backuply Fleet Remote Google Drive Backups

Use this reference when asked to back up multiple WordPress sites with Backuply to an offsite Google Drive remote.

## User preference signal
- Be precise and low-token=[REDACTED] status updates, concrete domain-by-domain evidence, no vague “it should be fine”.
- Enterprise-grade means: offsite target verified, full files+database selected, runtime hardened, sequential execution to avoid overloading shared hosts, and completion proven from Backuply state/log/artifact data.
- Preferred Google Drive remote names for this user: `pasalexios-gdrive` or `gdrive-pasalexios`.

## Procedure
1. Discover sites and credentials from the approved local secret store only; never echo secrets.
2. For each site, inspect Backuply status/runtime via an authenticated helper or WP/CyberPanel access.
3. Verify Backuply and Backuply Pro are active where remote backups are required.
4. Enumerate Backuply remote locations and select the Google Drive remote whose name matches `pasalexios-gdrive` or `gdrive-pasalexios`; record the numeric location ID per site because IDs vary.
5. Before starting, ensure backup settings include both database and files, and exclude cache/backup directories where the helper supports it.
6. Run the fleet sequentially, not concurrently, unless resource isolation is proven. Trigger `wp-cron.php`/Backuply tick loops as needed.
7. Verification hierarchy:
   - Best: fresh Backuply artifact appears with `backup_db=true`, `backup_dir=true`, and `backup_location=<target remote ID>`.
   - Acceptable for older helpers: `last_backup` advances after start and log tail contains `Backup Successfully Completed` plus upload reached 100%.
   - Insufficient alone: “backup started”, local archive exists, or a stale artifact exists.
8. Cleanup: remove temporary emergency cron/helper artifacts only after verification; keep durable helper only if it is intentionally installed and safe.
9. Final report should list each domain with status, remote target name/ID, evidence, and any gaps/blockers.

## Pitfalls
- Backuply location IDs differ per WordPress install; never assume ID `1` is the user’s desired Google Drive remote.
- Backuply may delete local archives due to rotation after successful remote upload; do not treat local deletion as failure if logs/artifact metadata prove remote completion.
- REST/status responses can be cached or stale; use cache-busting query params and re-check `last_backup`, active status, and log tail.
- If artifact metadata is unavailable, label verification as log/state verified rather than artifact verified.
