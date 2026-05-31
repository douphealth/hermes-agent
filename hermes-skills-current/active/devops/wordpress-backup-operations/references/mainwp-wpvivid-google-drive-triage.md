# MainWP + WPvivid + Google Drive Triage: Only One Site Uploads

Session-derived notes for diagnosing a WordPress fleet where MainWP + WPvivid is configured for Google Drive but only one child site's backup appears remotely.

## Symptom

- User configured WPvivid Backup via MainWP with a single Google Drive account.
- Google Drive showed only one site's multipart ZIP files.
- Other child sites appeared connected/installed in MainWP.

## Useful Audit Sequence

1. Query MainWP child-site inventory:
   - site ID, domain/name, URL, HTTP response/sync status
   - MainWP Child plugin version and backup plugin version from cached plugin inventory
2. Query WPvivid/MainWP extension option/cache tables:
   - schedule state
   - remote entries
   - selected remote ID/current destination
   - recent task status/log names
3. Call live child-site WPvivid/MainWP endpoints, not just dashboard cache:
   - remote storage type/default remote
   - backup task list/status
   - schedule last message
4. Start or inspect backups per site, not all at once:
   - use hard process/request timeouts
   - redact raw payloads before printing because task payloads may contain OAuth token fields

## Key Findings Pattern

A recurring misconfiguration can be:

- Google Drive remote object exists and contains token/auth data.
- Historical selected remote includes the Google Drive remote ID.
- Current `remote_selected`/selected destination is empty or stale.

This means Google Drive OAuth may be valid, but backups may not target the remote destination consistently.

## Failure Classes Observed

- **Completed and visible remotely:** task completed, multipart ZIPs visible in Google Drive.
- **Completed locally / needs remote check:** WPvivid task says completed, but remote file listing must be confirmed.
- **MainWP Child unreachable:** backup prepare reports child plugin not detected/reachable even though plugin inventory says active; suspect security/firewall/cache/connectivity.
- **`Unknown function`:** installed plugin inventory is not enough; the specific child-side WPvivid MainWP action endpoint is unavailable/stale/incompatible.
- **Memory exhausted:** PHP fatal like `Allowed memory size ... exhausted` during `wpdb.php`; increase PHP memory and reduce WPvivid DB/file workload chunks.
- **`Too many resumption attempts` / `no_responds`:** stuck task or server-side execution failure; cancel stale tasks, tune workload, retry individually.
- **Dashboard spinner/hang:** backend action may block on one child; isolate per-site with timeouts.

## Reporting Shape the User Needed

Use a blunt status matrix:

- Completed / visible in remote storage
- Completed / remote verification pending
- Running / likely stuck
- Failed: memory
- Failed: child unreachable
- Failed: action endpoint mismatch
- Failed: resumption/no-response loop

For each failed site, provide one next repair action rather than re-explaining Google OAuth.

## Safety Notes

- Do not paste OAuth token payloads or raw serialized WPvivid remote settings.
- If a script accidentally emits token-bearing payloads, kill/stop it and switch to a redacted/status-only script.
- Avoid simultaneous fleet backups; they can amplify CPU, memory, request timeout, Google API quota, and host throttling problems.
