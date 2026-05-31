# Backuply strict full media runs

Use this when the user explicitly demands **only full backups** and rejects DB/code or DB+files artifacts that omit media.

## Trigger

- Fresh Backuply artifact is far smaller than historical same-site full artifacts.
- Backuply logs say success but artifact size implies `wp-content/uploads` or large media folders were skipped.
- User corrects the workflow: “fix it” / “only full backups for all websites.”

## Pattern

1. **Stop the wrong-scope job server-side first.** Killing the local watcher is insufficient. Call the Backuply helper/controller stop endpoint and verify `backuply_status`/`status_active` is false before restart.
2. **Deploy/use a strict full controller.** It should force:
   - `backup_db = 1`
   - `backup_dir = 1`
   - selected valid Google Drive location
   - high runtime limits
   - direct executor tick endpoint when available
3. **Clear broad excludes before start.** Remove all Backuply exclude/skip/ignore settings from `backuply_settings`, then set only Backuply’s own output folder to avoid archive self-recursion. Do **not** keep cache/optimizer/WPvivid/old-backup exclusions if the user’s requirement is literally all files.
4. **Inventory media before start.** Capture `wp-content/uploads` bytes/file count. This prevents falsely accepting a 1GB artifact when uploads inventory is 7GB+.
5. **Verify strict scope after prepare.** Check exclude settings after the prepare call. `wp-content/uploads` or any broad media root exclusion means `BLOCKED`/`FAILED_PARTIAL`, not full.
6. **Run sequentially.** Strict full media archives can be very large and CPU-heavy. Do one site at a time, emit terse progress, and keep JSONL evidence.
7. **Artifact gate:** mark `VERIFIED_FULL` only when a fresh same-site artifact exists, has DB+files flags, targets the expected remote, root uploads was not excluded, and size is plausible against historical full size/current media inventory.

## Deployment fallbacks

- If wp-admin upload is blocked by Cloudflare but REST app passwords can list plugins, do not assume plugin upload works via REST: core `/wp/v2/plugins` installs only WordPress.org slugs, not arbitrary ZIPs.
- If wp-admin is blocked but the site has WP File Manager or a known file-manager channel, deploy a MU/plugin file through that channel and verify the REST route.
- If only a legacy helper is available and cannot prove artifact scope, label the site `BLOCKED` or `LEGACY_NOT_FULL_PROOF`; do not turn it green.

## User-facing reporting

For urgent frustrated backup repair, respond with labels and action only:

- `STOPPED_WRONG_SCOPE`
- `RUNNING_STRICT_FULL`
- `VERIFIED_FULL`
- `FAILED_PARTIAL`
- `BLOCKED`

Avoid explaining why partial might be “okay” when the user explicitly demanded full backups. The correct action is strict full or blocked with the exact blocker.
