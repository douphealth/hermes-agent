# WordPress Crash Recovery: Code Snippets Fatal PHP Error on All Front-End Requests

## The Problem

A Code Snippets snippet causes a PHP fatal error that crashes **some or all** front-end requests. Common crash patterns:

- **Pattern A (full front-end crash):** Snippet fires on `init` hook → crashes ALL WordPress PHP pages: wp-login.php, /wp-json/, admin-ajax.php, xmlrpc.php, and public site all return 500.
- **Pattern B (LiteSpeed plugin corruption after purge snippet):** A snippet calling `do_action('litespeed_purge_post', $post_id)` or similar LiteSpeed purge action corrupts the plugin's internal state. After deleting the snippet, the crash PERSISTS on **login_init** and **rest_api_init** hooks ONLY, while **admin-ajax.php?action=heartbeat**, **wp-cron.php**, **install.php**, and **upgrade.php** still work normally (200). This is because the LiteSpeed plugin itself becomes corrupted, not just the snippet, and the crash fires on hooks specific to login/REST rather than the generic `init`.
- **Pattern C (front-end wp_die from active Code Snippets, REST still works):** Public pages return `HTTP 500` with the WordPress error template and a short body such as `DONE`, but authenticated REST endpoints still work. This commonly happens after a temporary install/purge snippet was left active and runs `wp_die('DONE')` or similar on `init`/`template_redirect`. Fix is fast: list snippets via `/wp-json/code-snippets/v1/snippets`, find active snippets containing `wp_die`, `die(`, `DONE`, `status_header(500)`, or temporary names like `Seraph Install`, then POST `/code-snippets/v1/snippets/{id}/deactivate`. Do not delete first; deactivate and verify.

**Critical diagnostic move: test which entry points work. Do not assume "it's all 500."**

```
# Test heartbeat (checks if init hook works)
curl -sS -o /dev/null -w "HTTP %{http_code}" "https://gearuptofit.com/wp-admin/admin-ajax.php?action=heartbeat" -H "User-Agent: Mozilla/5.0"

# Test upgrade.php (skips most plugins)
curl -sS -o /dev/null -w "HTTP %{http_code}" "https://gearuptofit.com/wp-admin/upgrade.php"

# Test wp-cron
curl -sS -o /dev/null -w "HTTP %{http_code}" "https://gearuptofit.com/wp-cron.php"
```

If heartbeat works but wp-login/REST API crash → **Pattern B** — the crash is on login_init/rest_api_init hooks, NOT init. The solution is to disable the plugin that hooks into those, not to find and delete a snippet.

The following are typically available during either crash pattern:
- `wp-admin/install.php` (shows "Already Installed" page, bypasses all plugin loading via WP_INSTALLING constant)
- `wp-admin/upgrade.php` (shows "No Update Required", same bypass)
- `readme.html`, static CSS/JS files (served by web server, not PHP)
- `wp-cron.php` (often works because it doesn't trigger login/REST hooks)

## Recovery Priority Ladder

### 1. Code Snippets Safe-Mode (often unreliable)

Code Snippets has a safe-mode mechanism that supposedly skips all snippets:
- Cookie: `code_snippets_safe_mode=true` (or `code-snippets-safe-mode=1`)
- URL param: `?code-snippets-safe-mode&deactivate_all=1`

**⚠️ Production finding: safe-mode often does NOT work.** The snippet may run before the safe-mode check fires. Do not waste time here — proceed to ladder 2 or 3.

### 2. Direct REST API: deactivate/delete the snippet remotely

If the fatal error is in a *specific* snippet (not the plugin itself), the Code Snippets REST API may still work. Prefer **deactivation first** because it is reversible and preserves evidence.

```bash
# List all snippets
curl -s "https://example.com/wp-json/code-snippets/v1/snippets" \
  -H "Authorization=[REDACTED] $(echo -n 'user:app_pass' | base64)" > /tmp/snips.json

# Find suspicious active snippets quickly
python3 - <<'PY'
import json
j=json.load(open('/tmp/snips.json'))
for s in j:
    code=s.get('code','')
    hits=[x for x in ['wp_die','die(','DONE','status_header(500)','set_status_header(500)'] if x in code]
    if s.get('active') and hits:
        print(s['id'], s.get('name'), hits, 'priority=', s.get('priority'), 'scope=', s.get('scope'))
PY

# Reversible fix: deactivate the crashing snippet by ID
curl -s -X POST "https://example.com/wp-json/code-snippets/v1/snippets/42/deactivate" \
  -H "Authorization=[REDACTED] $(base64 -w0 <<< 'user:app_pass')"

# Destructive fallback: delete only after backup/confirmation
curl -s -X DELETE "https://example.com/wp-json/code-snippets/v1/snippets/42?force=true" \
  -H "Authorization=[REDACTED] $(base64 -w0 <<< 'user:app_pass')"
```

**Pattern C field note:** If public pages show the WordPress error template with only `DONE`, search active snippets for `wp_die('DONE')`. A temporary installer snippet such as `Seraph Install` can kill the frontend while REST remains usable; deactivating the snippet restores the site immediately.

**⚠️ BUT:** if the snippet crashes on `init` before REST routing, this also fails. Proceed to ladder 3.

### 3. Create an override snippet via REST API (before the crash runs)

If the crash happens on `init` but *after* REST routing completes, a race condition exists:

1. Create a new snippet that kills the crashing one:
```bash
curl -s -X POST "https://example.com/wp-json/code-snippets/v1/snippets" \
  -H "Authorization=[REDACTED] $(base64 -w0 <<< 'user:app_pass')" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "EMERGENCY KILL crashing snippet 42",
    "code": "add_action(\"init\", function() { remove_action(\"init\", \"crashing_function_name\"); }, 1);",
    "scope": "global",
    "active": true,
    "priority": 1
  }'
```

**⚠️ If the REST endpoint also crashes, this fails.** Proceed to ladder 4.

### 4. Direct file/database access (requires SSH, FTP, cPanel, or WP File Manager)

This is the **reliable** fix. The snippet data is stored in the WordPress `options` table under option name `code_snippets_snippets` (auto-loaded).

#### Via Database (phpMyAdmin / WP-CLI / direct SQL):

```sql
DELETE FROM wp_options WHERE option_name = 'code_snippets_snippets';
```

Or via WP-CLI:
```bash
wp option delete code_snippets_snippets
```

Or disable the entire Code Snippets plugin:
```bash
# Rename plugin directory to disable it
mv wp-content/plugins/code-snippets wp-content/plugins/code-snippets-disabled
```

#### Via SSH:
```bash
# Option A: Disable the plugin
cd /path/to/wordpress
mv wp-content/plugins/code-snippets wp-content/plugins/code-snippets.disabled

# Option B: Clear the snippets option from DB
wp option delete code_snippets_snippets
```

#### Via WP File Manager (if an existing admin session cookie still works)

If the user has WP File Manager installed and their browser still has a valid WordPress admin session cookie (from before the crash), they can access it directly at `/wp-admin/admin.php?page=wp_file_manager` even though wp-login crashes for NEW logins.

Steps:
1. Ask the user to navigate directly to WP File Manager URL
2. Use the file manager to rename `/wp-content/plugins/<crashing-plugin>/` to `<crashing-plugin>-disabled/`
3. The site recovers immediately
4. Then reconnect to wp-admin normally to fix the underlying issue

If the user CAN access WP File Manager, this is the fastest fix because it requires no credentials transfer.

⚠️ This only works if the user has an EXISTING valid WP admin session (cookie not expired). A fresh login attempt will fail because wp-login crashes.

### 5. Recovery Mode Email (WordPress built-in recovery system)

When WordPress detects a fatal error on a login page, it sends a recovery mode email to the site admin email with a special link:

```text
/wp-login.php?action=enter_recovery_mode&rm_key=XXX&rm_token=[REDACTED]
```

This link loads WordPress in recovery mode, which temporarily **disables all plugins** and uses the default theme, allowing the admin to fix the issue.

Steps:
1. The admin checks their inbox (the site admin email)
2. Clicks the recovery link
3. WordPress loads with plugins disabled → admin can access wp-admin and WP File Manager
4. Fix the crashing plugin/snippet from there

⚠️ The recovery mode link is one-time use and expires after a few hours.

### 6. Ask the user for server access (final fallback)

If no remote method works, present a clear, action-oriented request:
- What you need: Hosting cPanel credentials, SSH credentials, or FTP credentials
- Why: The crashing snippet runs on every PHP request before authentication, so no WordPress admin or API path works
- How long: Fix takes ~30 seconds once access is granted
- What the fix is: Delete `code_snippets_snippets` option from the database, or rename the plugin directory

## Post-Recovery Steps

After the site is back:
1. **Restore any temporary debug/config edits.** If you enabled `WP_DEBUG`, `WP_DEBUG_LOG`, or `WP_DEBUG_DISPLAY` in `wp-config.php`, put the original file back before closing the task.
2. **Delete any temporary public debug logs.** `wp-content/debug.log` is often web-readable; remove it and verify it returns 404.
3. **Immediately remove the noindex** on any pages that were set to noindex during the outage
4. **Purge all caches**: Cloudflare, LiteSpeed, plugin caches
5. **Verify the plain (no-query) public URL returns 200 with correct content**
6. **Browser-verify the actual rendered page**, not just curl status: title, H1/homepage content, iframe/app widgets if relevant, and no WordPress error template.
7. **Re-enable Cloudflare proxy** if it was turned off during recovery
8. **Check both cache-busted and plain URLs** — LiteSpeed/Cloudflare can serve stale 500s for the cache TTL even after the origin is fixed

## Key Production Findings

- **Not all crashes are equal.** Test which entry points still work (heartbeat, install.php, upgrade.php, wp-cron) to narrow down which hooks/plugins are crashing.
- **Pattern B (LiteSpeed plugin corruption after purge snippet):** A `do_action('litespeed_purge_post', ...)` or `do_action('litespeed_purge_all')` call from a code snippet can corrupt LiteSpeed's internal state/database tables, causing persistent crashes on `login_init` and `rest_api_init` hooks. The snippet is already deleted — you need to disable the **LiteSpeed plugin itself**, not the snippet. Admin-ajax heartbeat will still work, but wp-login and REST API will crash.
- **LiteSpeed cache serves error pages with ~1 week TTL.** Even after the origin PHP error is fixed, LiteSpeed may keep serving cached 500 pages for 604800 seconds. You need an explicit purge: `do_action('litespeed_purge_all')` or `LiteSpeed_Cache_API::purge_all()` or Cloudflare cache purge. The error page is cached, so users will still see the error until cache expires or is purged.
- **Code Snippets safe-mode is unreliable.** The init hook can fire before the safe-mode check.
- **install.php and upgrade.php survive** because they use the `WP_INSTALLING` constant which bypasses most plugin loading.
- **Cloudflare API tokens** may verify as active but only have DNS permissions — insufficient for WAF/Page Rule/Workers recovery.
- **Origin IP discovery**: use DNS SPF records (`v=spf1 +a +mx ip4:X.X.X.X`) or brute-force known hosting provider ranges when Cloudflare proxies the domain.
- The crash can persist even after all snippets are deleted if the **executed snippet triggered a plugin action** (e.g., `litespeed_purge_post`) that corrupted plugin state or the database.

## Fast Action First Principle

When a WordPress site crashes to 500 errors and the user becomes highly agitated, do NOT investigate extensively. Follow this priority immediately:

1. **Test entry points** (heartbeat, upgrade.php) — 1 curl command
2. **Check if admin-ajax heartbeat works** — if yes, Pattern B; ask user about WP File Manager
3. **Ask the user to check their email for recovery mode link** or to try WP File Manager directly (they may have an existing session)
4. **Or ask for server credentials** (cPanel/SSH) if above fails

The user's expectation is: execute the fix ladder aggressively, report what was done and the result. Do not explain why things broke until after the fix ships.

## Tools You Still Have During the Crash

| Tool | Pattern A (init crash) | Pattern B (login/REST crash) | Notes |
|------|----------------------|-----------------------------|-------|
| `wp-admin/install.php` | ✅ | ✅ | Loads minimal WP, bypasses plugins via WP_INSTALLING constant |
| `wp-admin/upgrade.php` | ✅ | ✅ | Same minimal bootstrap |
| `wp-content/readme.html` | ✅ | ✅ | Static file, no PHP |
| Dynamic CSS/JS files | ✅ | ✅ | Served by web server, not PHP |
| Cloudflare API | ✅ | ✅ | If token has DNS/cache permissions |
| `wp-cron.php` | ✅ | ✅ | Often works — lightweight bootstrap |
| `admin-ajax.php?action=heartbeat` | ❌ | ✅ **Key diagnostic!** | Tests whether init hook is broken separately from login/REST hooks |
| `wp-admin/admin.php?page=wp_file_manager` | ❌ | ✅ (if existing session) | WP File Manager — only works with valid admin cookie |
| Recovery mode email link | ✅ | ✅ | Sent to admin inbox; loads with all plugins disabled |
| `wp-login.php` | ❌ | ❌ | Crashes on login_init or init |
| `/wp-json/` | ❌ | ❌ | Crashes on rest_api_init or init |
| `admin-ajax.php` (no action) | ❌ | ❌ (but heartbeat works) | Crashes on init or returns 400/500 |
| `xmlrpc.php` | ❌ | ❌ | Crashes on init or xmlrpc hooks |
| SSH/FTP | Maybe | Maybe | Depends on hosting provider and credentials |
| cPanel | Maybe | Maybe | Depends on hosting provider |

**Diagnostic protocol:**
1. First test `admin-ajax.php?action=heartbeat` — if 200, you have Pattern B (login/REST hooks crash)
2. Test `wp-admin/upgrade.php` — if 200, WordPress is basically running
3. If heartbeat works: ask user to check inbox for recovery mode email, or try WP File Manager if they have an existing session
4. If everything crashes: need server-level access (SSH/cPanel)
