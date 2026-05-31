# CyberPanel WSOD / Critical Error Recovery via File Manager + Cron

Use when a WordPress site shows `There has been a critical error on this website`, REST/wp-admin also 500s, and normal WP admin/plugin tools are unavailable, but CyberPanel is reachable.

## Fast triage

1. Check public and origin directly with cache-busting query strings:
   - `/`
   - `/wp-login.php`
   - `/wp-json/`
   - `/wp-json/wp/v2/posts?per_page=1`
   - `/wp-content/debug.log` and `/error_log` only to identify the fatal, never to expose secrets.
2. If `debug.log` is publicly readable, tail only enough to identify the fatal and treat the public log exposure as a second incident to clean up.
3. MU-plugin parse errors are priority because they load before normal plugin deactivation paths. Disable the exact MU-plugin first, then repair/re-enable only after syntax is fixed.

## CyberPanel access pattern

When SSH/FTP are unavailable but CyberPanel login works:

- CyberPanel File Manager endpoint can read/write files via `/filemanager/controller` with methods:
  - `list`
  - `readFileContents`
  - `writeFileContents`
  - `deleteFolderOrFile`
- For immediate execution when file edits are awkward, CyberPanel Cron Jobs can run one-shot shell commands. Add a `* * * * *` cron, wait for one minute, verify result, then remove the cron immediately.
- Always remove temporary crons in reverse line order after execution and verify the cron list is empty.

## Emergency disable pattern

For an MU-plugin fatal:

```bash
/bin/mv /home/<domain>/public_html/wp-content/mu-plugins/broken.php /home/<domain>/public_html/wp-content/mu-plugins/broken.php.disabled-hermes
```

Then verify:

- homepage returns `200`
- `/wp-login.php` returns login page or expected auth redirect
- `/wp-json/wp/v2/posts?per_page=1` returns `200` JSON
- debug/log tail no longer shows the fatal

## Full cleanup pattern

After the site is back:

1. Use File Manager to read the disabled plugin.
2. Fix syntax locally mentally or with an available PHP linter if present; common failure: unescaped quotes inside PHP regex/string literals.
3. Write the corrected file back as active `.php`; leave the disabled copy only as short-term rollback if useful.
4. Re-test a URL scoped to the plugin's behavior, not only homepage health.
5. Disable public debugging:
   - `WP_DEBUG false`
   - `WP_DEBUG_DISPLAY false`
6. Delete or move public `wp-content/debug.log` / `error_log`; add a deny rule for future logs where supported.
7. Re-verify those log URLs are `404` or denied.
8. Confirm no temporary crons remain.

## User-facing reporting

For urgent WordPress outages, report tersely with evidence:

- `FIXED`: exact URLs and statuses.
- `ROOT CAUSE`: exact file and fatal class, no secret values.
- `CLEANED`: temp crons/log exposure/debug flags.
- `PENDING`: only if final verification or cleanup truly remains.

Do not over-explain while the site is down; act, verify, then summarize.