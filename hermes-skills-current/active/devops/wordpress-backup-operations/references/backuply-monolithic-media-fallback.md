# Backuply Monolithic Media Fallback

Use when Backuply repeatedly stalls/fails on very large WordPress media libraries (`wp-content/uploads`) after optimizer/cache/old-backup folders have already been excluded.

## Trigger signals

- Fresh artifact is still missing after a helper/control plugin deploy.
- Backuply repeats the same `Last file of (L...)` / `About to call self to prevent timeout` lines for many ticks.
- UI shows `Running` or progress percentage, but no fresh same-site `backuply_get_backups_info()` artifact exists.
- User provides wp-admin screenshots contradicting agent status claims.

## Required reporting discipline

- Do **not** say fixed because the helper version deployed, exclusions were applied, or the UI shows progress.
- Use only these states until artifact proof exists:
  - `RUNNING` — status/log is moving, no fresh artifact yet.
  - `STALLED` — same file/log phase repeats with no artifact.
  - `FAILED` — explicit Backuply failure/log error.
  - `PARTIAL-VERIFIED` — fresh artifact exists, but scope excludes media/uploads.
  - `VERIFIED` — fresh same-site artifact with intended full scope exists.
- If uploads are excluded, say clearly: `DB + code/config only; media excluded; full media requires separate/chunked backup path.`

## Fallback sequence

1. Kill/stop stale watcher; do not stack new starts on a running job.
2. Read live Backuply status/log tail and artifact list filtered by exact `backup_site_url`.
3. If optimizer/cache/backup exclusions were insufficient and `uploads` traversal still stalls, switch to a scoped safety backup:
   - exclude `wp-content/uploads`
   - keep DB + code/config/theme/plugin files
   - reset stale Backuply status
   - start a fresh run
   - verify fresh same-site artifact
4. Report result as `PARTIAL-VERIFIED`, not `VERIFIED`, unless media is included.
5. Plan media separately: rsync/SFTP/object-storage sync, host-level archive split by year/month, or another chunk-capable backup method.

## Pitfall

A fresh DB+code Backuply artifact is operationally valuable, but it is not a complete site disaster-recovery backup if uploads/media are excluded. Never let the artifact-only rule hide the reduced backup scope.