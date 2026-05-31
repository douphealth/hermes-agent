# Backuply Full vs Partial Fleet Runs

Use when the user explicitly wants full WordPress backups across a Backuply fleet, especially after a prior DB/code-only artifact was mistaken for full coverage.

## Durable lessons

- A fresh Backuply artifact with `backup_db=true` and `backup_dir=true` is not automatically a full disaster-recovery backup.
- Always size-sanity-check a fresh artifact against historical/expected full artifacts for that same `backup_site_url`.
- If the fresh artifact is dramatically smaller than historical full size, treat it as `PARTIAL_ONLY` until proven otherwise.
- `wp-content/uploads` is the decisive scope line for media-heavy WordPress sites. If uploads/media are excluded, report `PARTIAL-VERIFIED`, never `VERIFIED_FULL`.
- User correction signal: when they say a site’s full backup is about a larger size (for example ~8GB vs a fresh ~1GB artifact), immediately reclassify the run and inspect excludes before doing anything else.

## Full-backup verification criteria

For each site:

1. Query live Backuply status/helper with cache-busting.
2. Filter artifacts by exact same-site `backup_site_url`.
3. Capture before-run artifact names and historical sizes.
4. Select the intended Google Drive remote (`gdrive-pasalexios` / `pasalexios-gdrive` when available; IDs vary per site).
5. Prepare settings for DB + files and remove any `wp-content/uploads` / media exclusion.
6. Start only if no active Backuply job is already running.
7. Poll/tick/wp-cron until inactive and a fresh artifact appears.
8. Mark `VERIFIED_FULL` only when:
   - fresh same-site artifact exists,
   - `backup_db=true`,
   - `backup_dir=true`,
   - backup location matches target remote when available,
   - uploads/media are not excluded,
   - fresh artifact size is plausible versus historical full size (for example not <75% of max historical full artifact unless a reason is documented).

## Reporting states

- `VERIFIED_FULL` — fresh same-site artifact, DB+files, uploads included, plausible size.
- `RUNNING_FULL` — active full run; include target remote, expected size, current phase/tail.
- `PARTIAL_ONLY` — fresh artifact exists but uploads/media excluded or size implausibly small.
- `FAILED` — explicit Backuply failure or error log.
- `BLOCKED` — credentials, Cloudflare, helper installation, or admin access prevents required action.
- `VERIFIED_LOG_ONLY` — legacy helper lacks artifact metadata; last_backup advanced + success log only. Do not present as full unless size/scope proof is available.

## Controller/helper pattern

If existing helper cannot remove media exclusions or expose artifact metadata, deploy a temporary/controlled full-backup helper that:

- raises PHP runtime for backup requests,
- exposes status/prep/start/tick endpoints,
- shows `remote_locations`, `settings_backup_location`, current excludes, log tail, last backup, and same-site artifact metadata,
- recursively removes `wp-content/uploads` from Backuply exclude settings for full runs,
- preserves generated/cache/old-backup exclusions where possible,
- starts Backuply with DB + files and intended remote location,
- can tick Backuply directly when available.

Do not expose secrets in helper output. Redact remote URLs/tokens in logs.

## Pitfalls

- `Backup Successfully Completed` plus a 100% upload bar can be true for a partial-scoped artifact.
- Excluding `wp-content/uploads` may be useful for emergency DB/code safety backups, but must be loudly labeled partial.
- A previous full artifact may live under a different Backuply remote location ID/name; historical size still helps detect partial scope.
- Some sites may only have a legacy helper reachable. In that case, run but label proof weak until artifact and size evidence are available.
- Cloudflare/admin login blocks are `BLOCKED`, not a reason to invent success. Use origin/Host-header or MainWP/CyberPanel channels only when authorized.
