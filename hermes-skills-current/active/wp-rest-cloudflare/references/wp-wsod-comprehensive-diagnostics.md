# WordPress WSOD (500) Comprehensive Diagnostics

## When Everything Seems Broken

All PHP endpoints return 500 — including `/wp-admin/`, `/wp-login.php`, and `/wp-json/`. **Don't assume everything is down.** Probe every entry point systematically to narrow the crash location in the WordPress bootstrap chain.

## Probe Sequence

```bash
# 1. Static files — confirm web server itself is running
curl -sk -o /dev/null -w "readme.html: HTTP %{http_code}\n" "https://example.com/readme.html"

# 2. admin-ajax.php with heartbeat — tests whether init hook works
curl -sk -o /dev/null -w "admin-ajax heartbeat: HTTP %{http_code}\n" \
  "https://example.com/wp-admin/admin-ajax.php?action=heartbeat"

# 3. admin-ajax without action — tests WordPress bootstrap without specific action
curl -sk -o /dev/null -w "admin-ajax bare: HTTP %{http_code}\n" \
  "https://example.com/wp-admin/admin-ajax.php"

# 4. admin-post.php — tests POST route without template rendering
curl -sk -o /dev/null -w "admin-post: HTTP %{http_code}\n" \
  -X POST "https://example.com/wp-admin/admin-post.php"

# 5. wp-cron.php — tests lightweight bootstrap
curl -sk -o /dev/null -w "wp-cron: HTTP %{http_code}\n" \
  "https://example.com/wp-cron.php"

# 6. wp-login.php — tests login-specific hooks (login_init, etc.)
curl -sk -o /dev/null -w "wp-login: HTTP %{http_code}\n" \
  "https://example.com/wp-login.php"

# 7. wp-json/wp/v2/posts — tests REST API with valid endpoint
curl -sk -o /dev/null -w "REST: HTTP %{http_code}\n" \
  "https://example.com/wp-json/wp/v2/posts?per_page=1"

# 8. wp-admin/upgrade.php — tests minimal bootstrap with WP_INSTALLING constant
curl -sk -o /dev/null -w "upgrade: HTTP %{http_code}\n" \
  "https://example.com/wp-admin/upgrade.php"

# 9. xmlrpc.php — tests XML-RPC hooks
curl -sk -o /dev/null -w "xmlrpc: HTTP %{http_code}\n" \
  -X POST "https://example.com/xmlrpc.php"
```

## Diagnosis by Response Pattern

| admin-ajax (heartbeat) | wp-login | REST API | Likely Cause |
|---|---|---|---|
| 200/400 | 500 | 500 | Crash on `login_init` or `rest_api_init` hooks — **plugin-specific**, often LiteSpeed Cache corrupt state or premium plugin license check |
| 500 | 500 | 500 | Crash on `init` or earlier — early bootstrap error (mu-plugin, wp-config, PHP memory limit) |
| 200 | 200 | 500 | Crash on `rest_api_init` — REST-specific plugin conflict |
| 200 | 200 | 200 | Everything works, crash is intermittent (memory spike on specific pages) |

## Crash While admin-ajax Heartbeat Works (Pattern A)

**Most common pattern from production.** The PHP crash happens on `login_init` or `rest_api_init` hooks, NOT on `init`. This means:
- WordPress loads normally
- Most plugins load normally
- Only plugins hooking into login/REST hooks crash

**What still works:** admin-ajax, admin-post, wp-cron, static files, upgrade.php
**What crashes:** wp-login, wp-json REST, wp-admin

### Most Common Culprits

1. **LiteSpeed Cache** (plugin) — hooks into `login_init` and `rest_api_init` for cache control. Can corrupt state if a code snippet called `do_action('litespeed_purge_all')` or similar. Fix: rename plugin folder or deactivate via database.
2. **All-in-One WP Migration** — can corrupt during backup/restore operations
3. **Premium plugin license validation** — many premium plugins validate license on `login_init` and self-deactivate or crash if the license key is invalid
4. **Security plugins** (Wordfence, etc.) — check IP/login on `login_init`

## Using REST /wp/v2/plugins as Diagnostic Tool

When wp-admin loads but plugin activation fails silently, use the REST API:

```python
from requests.auth import HTTPBasicAuth

auth = HTTPBasicAuth("admin", "app_password")
r = session.get(f"{site}/wp-json/wp/v2/plugins", auth=auth, timeout=15)
for p in r.json():
    name = p.get('name', '?')
    status = p.get('status', '?')
    plugin = p.get('plugin', '?')
    print(f"{status} | {name} | {plugin}")
```

**Key observation:** If a plugin shows "Plugin activated" admin notice but the REST status remains "inactive", this indicates a **license validation self-deactivation** — the premium plugin's `plugins_loaded` or `init` hook checks its license and deactivates itself immediately after activation. Common with premium plugins that require a valid license key.

## Code Snippets REST API as Emergency PHP Execution Backdoor

When standard plugin activation fails (nonce mismatch, capability restriction, or license self-deactivation), use the Code Snippets REST API to execute arbitrary PHP:

### Create a snippet that manipulates the database directly:

```python
payload = {
    "name": "Emergency Plugin Activator",
    "code": """$plugin = 'seraphinite-accelerator-ext/plugin_root.php';
$active_plugins = get_option('active_plugins', array());
if (!in_array($plugin, $active_plugins)) {
    $active_plugins[] = $plugin;
    update_option('active_plugins', $active_plugins);
}
wp_delete_post(<snippet_id>, true);
""",
    "description": "Direct DB activation",
    "tags": [],
    "scope": "global",
    "active": True
}

r = session.post(f"{site}/wp-json/code-snippets/v1/snippets",
                 auth=auth, json=payload, timeout=15)
```

**Pitfalls:**
- `update_option('active_plugins', ...)` may NOT work because WordPress caches the active plugins list in memory before the snippet runs. The DB value changes but WordPress re-reads from memory, so plugin activation via DB write from a Code Snippet may fail silently.
- Use `activate_plugin()` function instead of DB manipulation when possible, but this function is only available in admin context.
- **More reliable pattern:** Create a proper mu-plugin via file write (requires file access) or use `wp-admin/plugins.php` with valid nonce cookies.

### More reliable: wp-admin session + nonce activation

The Code Snippets approach above is unreliable. The most reliable activation path is:

1. Login to wp-admin via form POST (get auth cookies)
2. Visit plugins.php to get a fresh nonce
3. Immediately activate via GET with that nonce

```python
# Step 1: Login
session.get(f"{site}/wp-login.php", timeout=15)
session.post(f"{site}/wp-login.php", data={
    "log": "admin", "pwd": "password",
    "wp-submit": "Log In", "redirect_to": "/wp-admin/", "testcookie": "1"
}, timeout=30, allow_redirects=True)

# Step 2: Get nonce
r = session.get(f"{site}/wp-admin/plugins.php", timeout=30)

# Step 3: Find activate link and nonce
import re
idx = r.text.find('seraphinite-accelerator-ext/plugin_root.php')
row = r.text[idx-2000:idx+2500]
activate_match = re.search(r'href="(plugins\.php\?action=activate&amp;plugin=seraphinite[^"]*)"', row)
activate_url = activate_match.group(1).replace('&amp;', '&')

# Step 4: Activate
r2 = session.get(site + '/wp-admin/' + activate_url, timeout=30, allow_redirects=True)
print(f"Activation response URL: {r2.url}")  # Should have ?activate=true
```

## The "Plugin Activated" But Still Inactive Pattern

If the plugins page shows "Plugin activated." admin notice but the plugin row still has `class="inactive"`, the plugin is **self-deactivating** on the subsequent page load. This is a **license validation failure**.

### Diagnostic confirmation:
```python
# Check via REST after activation
r = session.get(f"{site}/wp-json/wp/v2/plugins/seraphinite-accelerator-ext/plugin_root",
                auth=auth, timeout=15)
print(f"Status: {r.json().get('status', '?')}")  # Will show "inactive"
```

### Root causes:
| Cause | Indicator |
|---|---|
| Missing/exired license key | Plugin console shows activation prompt; settings page has "License" section |
| Domain mismatch | License key was for a different domain |
| API server unreachable | Plugin tries to validate via HTTP call that times out |
| PHP version incompatibility | Plugin checks `PHP_VERSION` and deactivates if below minimum |
| Plugin conflict | Another running plugin interferes during activation hook |

### Fix options:
1. **Enter the license key** via the plugin's settings page (`admin.php?page=seraph_accel_settings` for Seraphinite)
2. **Delete and reinstall** the plugin to reset license state
3. **Use an alternative plugin** that doesn't require a license (e.g., Autoptimize, WP-Optimize, Flying Press)
4. **Implement the plugin's functionality via Code Snippets** if the feature is simple (CSS/JS combine, caching, etc.)

## Reading PHP Source Files via Code Snippets (Base64 through wp_die)

When you need to inspect plugin source code but only have REST API access, use a Code Snippet that reads the file and base64-encodes it through `wp_die()`:

```python
read_code = """add_action('wp', function() {
    $path = WP_PLUGIN_DIR . '/target-plugin-dir/target-file.php';
    $content = file_get_contents($path);
    wp_die(base64_encode($content));
}, 1);
"""
r = session.post(f"https://{site}/wp-json/code-snippets/v1/snippets",
                 auth=auth, json={"name":"Read File","code":read_code,
                                  "scope":"global","active":True}, timeout=15)
sid = r.json().get('id')
r2 = session.get(f"https://{site}/?x=read", timeout=45)

import base64, re
match = re.search(r'<div[^>]*class="[^"]*wp-die-message[^"]*"[^>]*>([^<]+)</div>', r2.text, re.DOTALL)
decoded = base64.b64decode(match.group(1).strip()).decode('utf-8')

session.delete(f"https://{site}/wp-json/code-snippets/v1/snippets/{sid}", auth=auth, timeout=15)
```

**Pitfalls:**
- PHP files are **executed by the server**, not served as text. You cannot read PHP source by requesting the file URL via HTTP — it would execute the PHP. Always use the Code Snippet approach above.
- Class/function redefinition: `require_once` inside a Code Snippet will fail if the class was already defined by WordPress's normal plugin loading. Use a fresh request where the plugin is not active, or use `file_get_contents()` to read without executing.
- The `wp_die()` output appears inside a `<div class="wp-die-message">` in the HTML. Extract it with regex.

## Patching Plugin Files via Code Snippets (Edit Without SSH)

When you need to modify a plugin's PHP code to fix a bug, remove a license check, or add error suppression, use `file_get_contents()` + `file_put_contents()` + `str_replace()`:

```python
patch_code = """add_action('wp', function() {
    $path = WP_PLUGIN_DIR . '/target-plugin-dir/target-file.php';
    $content = file_get_contents($path);
    
    // Find and replace specific code
    $content = str_replace(
        'Plugin::Init();',
        'try { Plugin::Init(); } catch (Throwable $e) { error_log($e->getMessage()); }',
        $content
    );
    
    file_put_contents($path, $content);
    wp_die('PATCHED');
}, 1);
"""
```

**Pitfalls:**
- PHP file permissions must allow the web server user to write to the file
- Always double the `\\` escapes in namespace references inside your search/replace strings
- Backup pattern: read the file content, save it locally, then apply the patch
- **Cannot parse/replace if file is too large** (PHP memory limit may apply to huge files like `main.php` at 140KB+)
- **Cannot fix fatal parse errors** via this method — if the file has a syntax error, `file_get_contents()` still works but the Code Snippet itself may crash before executing

## WP-CLI from Within a Web Request: Does Not Work

Attempting to run `/bin/wp plugin activate` from within a web request (via `shell_exec()` in a Code Snippet) will **fail with fatal error**:

```
PHP Fatal error:  Uncaught Error: Call to undefined function remove_filter()
```

**Root cause:** WP-CLI is a PHAR (PHP Archive) that tries to load WordPress from scratch, but the parent web request process has already defined all WordPress constants (`WP_MAX_MEMORY_LIMIT`, `WP_MEMORY_LIMIT`, `ABSPATH`, etc.). The PHAR's internal WordPress loader tries to redefine these constants and crashes.

**Workarounds that also fail:**
- `env -i` (clearing environment) does NOT clear PHP constant definitions
- `nohup setsid` (new session) does NOT clear PHP constant definitions — they're process-level, not environment-level
- Writing a separate PHP script file and executing it — the PHP CLI process still inherits the parent's constant definitions

**The only ways to run WP-CLI:**
1. True SSH session to the server (separate login shell)
2. Cron job (runs in clean environment)
3. Terminal tool if available (direct shell access)

## WordPress 6.x Auto-Deactivation Between Requests

WordPress 6.x introduced a **plugin error recovery mechanism** that can deactivate plugins BETWEEN requests, even when the plugin loads without errors during the current request. This is managed through:

1. **`recently_activated` option** — WordPress stores plugins that failed to activate here
2. **`recovery_keys` option** — Recovery mode keys stored as a serialized array
3. **`recovery_mode_email_last_sent`** — Timestamp of last recovery email

**Symptoms:**
- "Plugin activated." admin notice appears on plugins.php
- Plugin row has `class="inactive"` or `class="inactive update"`
- REST API shows `{status: "inactive"}` after activation
- On the **next request** after activation, the plugin is already gone from active_plugins

**Diagnostic:**
```python
# Check recovery-related options
options_code = """add_action('wp', function() {
    $recent = get_option('recently_activated', array());
    $recover = get_option('recovery_keys', array());
    $last_sent = get_option('recovery_mode_email_last_sent', 0);
    wp_die('recently_activated=' . serialize($recent) . 
           '|recovery_keys=' . serialize($recover) . 
           '|last_sent=' . $last_sent);
}, 1);
"""
```

**What can cause auto-deactivation:**
| Trigger | How it works |
|---|---|
| PHP fatal error | Any uncatchable `ParseError` or `TypeError` in plugin code |
| PHP warning notice (E_WARNING) | If `WP_DEBUG` is on, some hosts treat warnings as errors |
| Deprecation notice | `strlen(null)`, `${}` variable interpolation, etc. on PHP 8.1+ |
| Plugin dependency missing | WordPress 6.5+ can deactivate plugins with unmet dependencies |
| `register_activation_hook` failure | If the callback throws an exception |

**What does NOT help:**
- `try/catch(Throwable $e)` around `Plugin::Init()` — the error may be outside the init (during file include)
- `@require_once()` — suppression operators don't prevent ParseErrors
- Direct DB manipulation of `active_plugins` — WordPress re-reads from the option on the next request, and the recovery mechanism overwrites it
- `set_error_handler()` — ParseErrors can't be caught by error handlers

**When all else fails:** Use a permanent Code Snippet that:
1. Hooks into `shutdown` (priority 999999)
2. Re-adds the plugin to `active_plugins` on every request
3. The plugin won't load during the request (already processed), but WILL be present for the next request

```php
add_action('shutdown', function() {
    $plugin = 'target-plugin/main-file.php';
    $active = get_option('active_plugins', array());
    if (!in_array($plugin, $active)) {
        $active[] = $plugin;
        update_option('active_plugins', $active);
    }
}, 999999);
```

**Note:** Even this approach fails if the error happens **during** the request's plugin loading phase — the plugin is deactivated before `shutdown` fires. Use it for license self-deactivation (where the plugin runs fine but calls `deactivate_plugins()` on itself).

## Seraphinite `_SelfRenameDir` Deactivation Pattern

Some plugins (like Seraphinite Accelerator) have a **self-rename mechanism** that deactivates and renames the plugin directory. This is NOT the same as a license failure:

```php
static private function _IsRenameNeeded()
{
    if( Plugin::GetCurBaseName( false ) != 'seraphinite-accelerator' )
        return( false );
    // ...
}

static private function _SelfRenameDir( $url, $referer )
{
    // 1. Deactivate itself
    deactivate_plugins( $aPlugins, true, $bMultisiteGlobalAmin );
    // 2. Rename directory from seraphinite-accelerator to seraphinite-accelerator-ext
    rename( $dir, $dirNew );
    // 3. Reactivate
    activate_plugins( $aPlugins, '', $bMultisiteGlobalAmin, true );
}
```

**How to distinguish self-rename from license failure:**
- Self-rename: Plugin shows as inactive, but on the NEXT page load it's active again (rename -> reactivate cycle)
- License failure: Plugin shows "activated" notice but immediately shows inactive on the same page load
- Self-rename URL: Contains `?activate=true` followed by a redirect to a page where the plugin is re-activated
- License failure: `?activate=true` but the plugin row stays permanently inactive

## CyberPanel as a Backdoor: Password Character Restrictions

When using CyberPanel API (port 8090) to fix a WordPress crash, be aware of **input character restrictions**:

### Blocked characters in CyberPanel API:
```
$ & ( ) [ ] { } ; : ' < >
```

### Most passwords will contain blocked characters:
Common patterns like `^!%@$#Alex1973(~*^@!` contain `$`, `(`, `)` which are all blocked.

### Solutions if CyberPanel API rejects the password:
1. **Ask user to log in to CyberPanel** and rename the plugins folder via File Manager
2. **Ask user to create a new FTP user** with a simple password
3. **Check for SSH access** on the same server
4. **Check for phpMyAdmin** at `/phpmyadmin` on the CyberPanel server

### Example: Ask user to rename plugins folder
```
Go to CyberPanel → File Manager → navigate to:
example.com/public_html/wp-content/

Rename "plugins" → "plugins_old"
Site comes back immediately.
Then create "plugins" directory and move plugins back one at a time.
```

## Browser-Based Bulk Plugin Activation (Fallback When REST/WP-CLI Fail)

When all plugins are inactive (accidentally or otherwise) and REST API returns 200 but doesn't actually activate plugins, use a browser session with JavaScript to bulk-activate:

### Single-page bulk activation (high-level JavaScript in browser)

```javascript
// Run in browser console on wp-admin/plugins.php
document.querySelectorAll('input[type="checkbox"][name="checked[]"]')
  .forEach(cb => cb.checked = true);

var bulkAction = document.querySelector('select[name="action"]');
if (bulkAction) bulkAction.value = 'activate-selected';

var form = document.querySelector('form#bulk-action-form') || 
           document.querySelector('form[action="plugins.php"]');
if (form) form.submit();
```

**Note:** This navigates away from the plugins page (form submission). After the page reloads, you may land on another plugin's dashboard. Navigate back to `wp-admin/plugins.php` to verify activation state.

### Multi-page/fallback: Check all + submit through form
When the admin form submission redirects unexpectedly (to Grow dashboard, Elementor, etc.), navigate back to `wp-admin/plugins.php` and verify with:

```javascript
document.querySelectorAll('tr.active').length + ' active, ' + 
document.querySelectorAll('tr.inactive').length + ' inactive'
```

### Limitations
- This requires you to be logged into wp-admin (cookie session) in the browser
- Some plugins may fail activation silently (same "Plugin activated" but inactive pattern) — these need individual handling
- Works for restoring dozens of plugins at once; for individual stubborn plugins, use the per-plugin activate link approach

## ⚠️ CRITICAL SAFETY RULE: Never Directly Modify `active_plugins` in Diagnostics

**Do NOT ever write this in diagnostic or exploratory code:**

```python
# DANGER: This will DEACTIVATE ALL PLUGINS
$active = get_option('active_plugins', array());
$filtered = array();
# ... some filtering logic ...
update_option('active_plugins', $filtered);  # ← WRONG! Destructive!
```

This was the root cause of a production incident where a diagnostic test accidentally emptied the `active_plugins` option, deactivating all 47+ plugins on a live WordPress site. The code was intended to test plugin isolation but had a logic bug: the target plugin was already inactive, so the "keep" filter matched nothing, producing an empty list.

**Safe alternative for read-only diagnostics:**

```php
# ✅ SAFE — read only, never write
$active_plugins = get_option('active_plugins', array());
error_log('Active plugin count: ' . count($active_plugins));

# If you MUST test isolation, create a backup first:
$backup = get_option('active_plugins', array());
update_option('active_plugins_backup_' . time(), $backup);  // backup
// ... test ...
update_option('active_plugins', $backup);  // restore
```

**Better approach:** Instead of modifying the live `active_plugins` option, use a Code Snippets hook with early priority to conditionally skip plugins at runtime. This doesn't persist across requests and won't break wp-admin:

```php
add_filter('option_active_plugins', function($plugins) {
    // Only filter for front-end requests, not admin
    if (is_admin()) return $plugins;
    
    $exclude = ['problematic-plugin/main.php'];
    return array_values(array_diff($plugins, $exclude));
}, 999);
```

This is safe because it only affects front-end rendering and auto-resets on the next request.

## Watchdog Snippet: Limitations Confirmed

A permanent Code Snippet that re-adds a plugin to `active_plugins` on `shutdown` may NOT work if WordPress's auto-deactivation mechanism fires BETWEEN requests. The sequence:

1. **Request N:** Plugin loads → error occurs → marked for deactivation
2. **Between requests:** WordPress runs cleanup → plugin removed from `active_plugins`
3. **Request N+1:** Plugin NOT loaded → Code Snippets runs (as a separate plugin) → watchdog re-adds plugin at `shutdown`
4. **Request N+2:** Plugin loads again → error occurs → cycle repeats

**Evidence:** Even a `shutdown` priority 999999 watchdog failed to keep Seraphinite Accelerator active on gearuptofit.com, because the deactivation happens during request cleanup (after `shutdown` but before the option is re-read), or WordPress's recovery mechanism runs as a CRON job between requests.

**This confirms that plugins self-deactivating due to runtime PHP errors cannot be kept active via post-hoc DB manipulation.** The only fix is to eliminate the root cause (PHP error, license validation, or plugin bug).

## Production Lessons

- **Not all "500" errors are the same PHP crash.** Static files (readme.html, license.txt) may work while PHP crashes — distinguish between PHP and server-level failures.
- **A single `do_action('litespeed_purge_all')` from a code snippet can corrupt LiteSpeed Cache's internal state**, causing persistent crashes on `login_init` even after the snippet is deleted. Fix: disable LiteSpeed plugin, NOT just the snippet.
- **admin-ajax.php returning "0" (bare 400) is GOOD** — it means WordPress loaded and is waiting for a valid AJAX action. This is NOT a crash.
- **admin-ajax.php returning "-1" means not logged in or invalid nonce** — this is an auth issue, not a crash.
- **Premium plugins that self-deactivate after "Plugin activated"** — check for license validation, domain mismatch, or PHP incompatibility. The activation itself succeeds, but the plugin's runtime check immediately undoes it.
- **wp-admin cookie nonces expire quickly** — get the nonce and use it in the same request session. If you see "The link you followed has expired" with 403, get a fresh nonce and retry immediately.
- **Application Password REST auth does NOT create cookie sessions** for admin-ajax or plugins.php. For those, use form-based login via wp-login.php POST.
