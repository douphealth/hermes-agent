# Backuply Enterprise Runtime Tuning Notes

Use these notes when a WordPress fleet is moved to Backuply and backups fail with PHP memory/execution errors.

## Key symptoms

- Backuply log shows: `Allowed memory size of 536870912 bytes exhausted ... you can solve this issue by increasing PHP memory limit`.
- Backuply is installed and active, but full-site backup generation dies before upload or artifact verification.
- REST app password can authenticate but cannot view/manage plugins: `rest_cannot_view_plugins` / HTTP 401.
- WP-admin automation may be blocked by Cloudflare challenge; CyberPanel may require 2FA even with valid credentials.

## Durable lessons

1. Treat Backuply memory errors as a runtime ceiling problem first, not remote-storage auth.
2. Verify Backuply's *effective* runtime from inside wp-admin/Backuply context after changing it. A PHP/server setting is not proven until the plugin admin request shows the new values.
3. A small MU/normal plugin can harden Backuply runtime without editing core Backuply files:
   - `ini_set('memory_limit', '1024M')`
   - `ini_set('max_execution_time', '900')`
   - `set_time_limit(900)`
   - define `WP_MEMORY_LIMIT` / `WP_MAX_MEMORY_LIMIT` if not already defined
   - filter `backuply_backup_self_timeout` upward so self-calls have enough time
   - ensure `wp-content/backuply/` exists and has basic index/.htaccess protections
4. Install by the least-blocked channel:
   - Direct WP-admin plugin upload when admin session works.
   - MainWP Child `installplugintheme` when Cloudflare blocks wp-admin but MainWP still has child connectivity.
   - CyberPanel/server PHP config only when panel auth including 2FA is available.
5. Do not claim all-sites success until Backuply creates verifiable artifacts/log success per site. Runtime tuning fixes the memory class of failure, but backup completion still requires a one-site-at-a-time backup run and artifact verification.

## MainWP install pitfall

When using MainWP internals from PHP scripts, `MainWP_Connect::fetch_urls_authed()` expects the websites argument by reference. Do not pass a temporary array literal:

```php
// Wrong: can throw "Argument #1 ($websites) could not be passed by reference"
MainWP_Connect::fetch_urls_authed([$website], 'installplugintheme', $post_data, $callback, $output);

// Right
$websites = [$website];
MainWP_Connect::fetch_urls_authed($websites, 'installplugintheme', $post_data, $callback, $output);
```

## Verification evidence to collect

- Backuply plugin version and pro/lite activation state.
- Effective `memory_limit`, `max_execution_time`, and `WP_MAX_MEMORY_LIMIT` from a Backuply/admin request.
- Backuply status/log after starting backup.
- New backup artifact name, timestamp, size/parts, local/remote status.
- Any access blockers separately classified: Cloudflare admin block, REST capability limitation, CyberPanel 2FA, MainWP child failure.
