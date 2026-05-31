# Backuply Strict Full Fleet Enforcement

Use this reference when the user explicitly says **all websites** and **only full backups**. This is stricter than a normal Backuply fleet run.

## Required posture

- Treat the complete site manifest as mandatory. Do not silently focus on the currently-running site.
- Keep a per-site state list: `VERIFIED_FULL`, `RUNNING_STRICT_FULL`, `QUEUED_STRICT_FULL`, `FAILED`, or `BLOCKED`.
- A site is not green because a previous partial run completed, because a legacy helper logged success, or because Backuply reached 100% upload. It is green only after fresh same-site artifact proof.
- If one site is blocked (for example Cloudflare/wp-admin/2FA), keep it in the manifest as `BLOCKED`; do not omit it from the fleet summary.

## Strict-full sequence

1. Load the current site manifest from the task/user context.
2. Verify controller/helper availability per site before starting the fleet.
3. Stop wrong-scope active jobs server-side first; killing the local watcher is not enough.
4. Clear broad Backuply exclude/skip/ignore settings.
5. Set only Backuply's own active output folder as excluded to prevent recursive backup of the archive being created.
6. Inventory `wp-content/uploads` before start and preserve `uploads_bytes` + `uploads_files` as scope evidence.
7. Start sequentially, not all at once, unless the user explicitly accepts load/quota risk.
8. Poll via direct executor/wp-cron where available and persist JSONL progress.
9. Verify final result with fresh same-site Backuply artifact: `backup_db=true`, `backup_dir=true`, correct remote/location, root uploads not excluded, and plausible size vs current inventory/historical full backups.

## Deployment/workaround notes

- If normal wp-admin plugin upload is Cloudflare-blocked, try the authenticated WordPress REST plugin endpoint (`POST /wp-json/wp/v2/plugins`) when application passwords have plugin-management capability. This can install a WordPress.org bridge plugin such as File Manager Advanced even when wp-admin UI is blocked.
- Installing a bridge plugin is not the backup fix by itself; it is an access channel to deploy/repair the strict Backuply controller.
- CyberPanel may be reachable but API disabled or login may require 2FA. Report that exact blocker and continue all non-blocked sites; do not mark the blocked site verified.
- If a legacy Backuply helper lacks artifact/scope APIs, its log-only success is insufficient for an `only full backups` request. Use it only as diagnostic evidence or a temporary safety backup, not as `VERIFIED_FULL`.

## Reporting format

Keep updates terse and fleet-shaped:

- `RUNNING_STRICT_FULL`: domain, phase, current loop/tail, uploads included evidence.
- `VERIFIED_FULL`: domain, fresh artifact name/timestamp, size, remote/location, uploads inventory/scope evidence.
- `BLOCKED`: domain, exact missing access/control path, next repair action.
- `FAILED`: domain, exact Backuply error tail and whether a retry/split strategy is needed.

Avoid long explanations while a fleet run is active. The user wants active execution and all-site coverage.