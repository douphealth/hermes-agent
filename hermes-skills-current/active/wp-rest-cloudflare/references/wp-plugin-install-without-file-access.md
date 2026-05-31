# Plugin Install/Upgrade Without File/SSH Access

## Problem
You need to install or upgrade a WordPress plugin but have no FTP/SSH/cPanel access — only REST API access (Application Passwords) and the Code Snippets plugin is active.

## Solution: REST Media Upload + Code Snippet Installer

### Step 1: Upload plugin zip as media attachment

```python
import requests
from requests.auth import HTTPBasicAuth

session = requests.Session()
session.verify = False
auth = HTTPBasicAuth("admin", "application_password")

with open("plugin.zip", "rb") as f:
    r = session.post(
        "https://example.com/wp-json/wp/v2/media",
        auth=auth,
        files={"file": ("plugin.zip", f, "application/zip")},
        timeout=60
    )

media_url = r.json().get("source_url", "")
print(f"Uploaded to: {media_url}")
```

**Pitfall:** Some sites (like frenchyfab.com) return JSON with a UTF-8 BOM prefix (`\ufeff`). Always decode with `utf-8-sig`:

```python
import json
media_json = json.loads(r.content.decode('utf-8-sig'))
media_url = media_json.get('source_url', '')
```

### Step 2: Create installer Code Snippet

The snippet downloads the zip from the media URL, extracts it into the plugins directory, and activates it:

```python
install_code = """add_action('wp', function() {
    $target = WP_PLUGIN_DIR . '/plugin-folder-name';
    $zip_url = '<MEDIA_URL>';

    // Remove old plugin directory if it exists
    if (file_exists($target)) {
        array_map('unlink', glob($target . '/*'));
        system("rm -rf " . escapeshellarg($target));
    }

    require_once ABSPATH . 'wp-admin/includes/file.php';
    require_once ABSPATH . 'wp-admin/includes/plugin.php';

    // Download zip
    $tmp = download_url($zip_url);
    if (is_wp_error($tmp)) { wp_die('DL'); }

    // Extract
    WP_Filesystem();
    $uz = unzip_file($tmp, WP_PLUGIN_DIR);
    @unlink($tmp);
    if (is_wp_error($uz)) { wp_die('UZ'); }

    // Activate
    activate_plugin('plugin-folder-name/plugin_main_file.php');
    wp_die('DONE');
}, 1);"""

payload = {
    "name": "Plugin Installer",
    "code": install_code,
    "scope": "global",
    "active": True
}

r = session.post("https://example.com/wp-json/code-snippets/v1/snippets",
                 auth=auth, json=payload, timeout=15)
sid = r.json().get("id")
```

### Step 3: Trigger and clean up

```python
# Trigger a front-end request to execute the snippet
r = session.get("https://example.com/?t=" + str(hash("unique")), timeout=45)

# Check result
if "DONE" in r.text:
    print("✅ Install succeeded!")
elif "DL" in r.text:
    print("❌ Download failed")
elif "UZ" in r.text:
    print("❌ Unzip failed")

# Delete the temporary snippet
session.delete(f"https://example.com/wp-json/code-snippets/v1/snippets/{sid}",
               auth=auth, timeout=15)
```

### Step 4: Verify

```python
r = session.get("https://example.com/wp-json/wp/v2/plugins", auth=auth, timeout=15)
for p in r.json():
    if 'plugin-name' in str(p).lower():
        print(f"v{p.get('version','?')}, status={p.get('status','?')}")
```

## Batch Install Across All Sites

For a fleet of sites, iterate over sites and run the same pattern:

```python
sites = [
    ("site1.com", "user1", "pwd1"),
    ("site2.com", "user2", "pwd2"),
]

for domain, user, pwd in sites:
    auth = HTTPBasicAuth(user, pwd)
    # ... same as above ...
```

**Pitfall — reusing file handles:** When iterating, the zip file object from `open()` can carry state between iterations. Open a fresh file handle for each upload:

```python
with open(zip_path, 'rb') as f:
    r = session.post(f"https://{domain}/wp-json/wp/v2/media", ...)
```

## Known Working Example: Seraphinite Accelerator v2.29.10

This pattern was tested on 8 WordPress sites with Seraphinite Accelerator (Full, premium):

| Step | Result |
|---|---|
| Media upload | ✅ Created attachment ID for zip |
| `download_url()` | ✅ Downloaded from local media URL |
| `unzip_file()` | ✅ Extracted to plugins directory |
| `activate_plugin()` | ⚠️ Worked on 7/8 sites; 1 site had license self-deactivation |

The plugin folder name was `seraphinite-accelerator-ext/plugin_root.php`.

## MainWP LocalWP Bulk ZIP Installs: red X, rejection, or endless 0% spinner

When MainWP Dashboard runs inside LocalWP at `http://localhost:<port>` and the user uploads a plugin `.zip` via `PluginsInstall` for multiple remote child sites, distinguish two failure modes immediately:

- **100% progress then red X/rejection:** the dashboard upload likely succeeded, but the child site could not download the ZIP.
- **Modal stuck at 0% with per-site spinners:** the browser/admin-ajax install pipeline is hanging. Do not repeat the same public-dashboard tunnel advice; inspect the AJAX path and the ZIP-serving path for a LocalWP/PHP deadlock.

### Root causes to check first

1. **Unreachable signed ZIP URL**
   - MainWP converts local uploads into signed URLs like `admin_url('?sig=...&mwpdl=...')`.
   - On a LocalWP dashboard, `admin_url()` is often `http://localhost:<port>/...`.
   - Remote child sites interpret `localhost` as themselves, not the operator's PC, so `download_url()` fails even though the dashboard upload succeeded.
2. **Server-side upload cap mismatch**
   - Some MainWP versions render Dropzone with `maxFilesize: 150`, but `MainWP_Install_Bulk::admin_init()` still sets `$sizeLimit = 2 * 1024 * 1024`.
   - Result: ZIPs over 2MB are rejected despite the UI claiming a 150MB limit.
3. **WordPress/PHP self-deadlock while child downloads the ZIP**
   - If the child download URL is served through the same LocalWP WordPress/PHP process that is currently handling the admin-ajax install request, the request can hang at 0% forever.
   - A public tunnel to `localhost:<wp-port>` is not enough when the signed `mwpdl` endpoint still depends on busy WordPress/PHP. Serve uploaded ZIPs from a separate static process.

### Durable repair pattern

1. Verify PHP upload limits are not the bottleneck (`upload_max_filesize`, `post_max_size`).
2. Align MainWP's server-side upload limit with the UI limit in `pages/page-mainwp-install-bulk.php`:
   ```php
   $sizeLimit = 150 * 1024 * 1024; // 150MB = max allowed.
   ```
3. For red-X download failures, a public dashboard tunnel may be enough:
   - Quick temporary fix: `cloudflared tunnel --url http://localhost:<port> --no-autoupdate`
   - Stable production fix: named Cloudflare Tunnel / stable hostname such as `https://mainwp.example.com` to the LocalWP dashboard.
4. For endless 0% spinners, use a separate static ZIP server instead of WordPress/PHP:
   ```bash
   python3 -m http.server 18080 --bind 0.0.0.0 --directory '/mnt/c/Users/<User>/Local Sites/<site>/app/public/wp-content/uploads/mainwp/0/bulk'
   cloudflared tunnel --url http://127.0.0.1:18080 --no-autoupdate
   ```
   Store that static public URL in a separate option such as:
   ```php
   update_option('mainwp_static_bulk_download_base_url', 'https://static-zip-host.example.com');
   ```
5. Patch uploaded-ZIP URL generation to prefer the static base URL for files under the MainWP `bulk` directory. In `class/class-mainwp-system-utility.php`, after `$fullFile` is known and before building the signed `mwpdl` URL:
   ```php
   $static_bulk_base_url = get_option( 'mainwp_static_bulk_download_base_url', '' );
   if ( ! empty( $static_bulk_base_url ) && false !== strpos( str_replace( '\\', '/', $fullFile ), '/mainwp/0/bulk/' ) ) {
       return trailingslashit( $static_bulk_base_url ) . rawurlencode( basename( $fullFile ) );
   }
   ```
   Keep the older `mainwp_public_download_base_url`/signed-URL override as a fallback for cases where the static server is not used.
6. Add browser-side failure handling so the UI cannot spin forever. Replace the relevant `jQuery.post(..., 'json')` install request in `assets/js/mainwp.js` with `jQuery.ajax({ dataType: 'json', timeout: 120000, ... }).done(...).fail(...)`, decrement the active thread counter in both success and fail paths, and mark that site as done/error before starting the next site.
7. Bust MainWP's JS cache while testing patched local files by enqueueing `assets/js/mainwp.js` with `filemtime()` instead of only `MAINWP_VERSION`.

### Verification contract

- PHP lint the modified MainWP files and syntax-check the patched JS.
- Discover the actual MainWP bulk directory via `MainWP_System_Utility::get_mainwp_specific_dir('bulk')` instead of guessing.
- Write a tiny health file into the bulk directory and verify both local static server and tunnel return HTTP 200.
- Generate a small valid test plugin ZIP in the bulk directory and verify the static public URL downloads bytes and opens as a ZIP.
- Run a test install to two representative child sites. If using a dummy plugin, delete it afterward through MainWP and verify deletion returns success.
- If failures remain, inspect child-side install response/error details; do not assume upload size after the ZIP URL is publicly reachable.

### Pitfalls

- If the user reports “endless,” “never stops,” or shows 0%, treat it as a hung AJAX/deadlock problem first, not as the same rejected-download problem. Respond with a fix path and evidence, not defensive explanation.
- A Cloudflare quick tunnel URL is temporary. If the tunnel process stops or the PC restarts, update `mainwp_static_bulk_download_base_url` / `mainwp_public_download_base_url` before retrying installs.
- WordPress may redirect public tunnel wp-admin requests back to `localhost` if `home/siteurl` are still local. The signed `mwpdl` endpoint must be tested end-to-end through the public hostname, not only by opening wp-admin locally.
- Prefer a stable named tunnel for recurring MainWP fleet installs; quick tunnels are acceptable only as an emergency workaround.

## Limitations

- Requires Code Snippets plugin to be **active** (can't install it via this method)
- Requires **write permission** on `wp-content/plugins/` (PHP file owner must be the web server user)
- Plugin self-deactivation after activation (license check) is NOT solvable via this method — the plugin's runtime hooks check immediately after activation
- `unzip_file()` may fail if the zip is too large or PHP memory is limited
- The temporary snippet should be **deleted** after use to avoid cluttering the snippets list

## Reading PHP Source Files via Code Snippets

To inspect plugin PHP code without SSH access, read via `file_get_contents()` + base64 `wp_die()`:

```python
read_code = """add_action('wp', function() {
    $path = WP_PLUGIN_DIR . '/plugin-folder/target.php';
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
lines = decoded.split('\n')
for i, line in enumerate(lines[:50]):
    print(f"{i+1}: {line}")

# Clean up
session.delete(f"https://{site}/wp-json/code-snippets/v1/snippets/{sid}", auth=auth, timeout=15)
```

## Patching Plugin Files via Code Snippets

To modify plugin code (e.g., add error suppression, remove license check):

```python
patch_code = """add_action('wp', function() {
    $path = WP_PLUGIN_DIR . '/plugin-folder/target.php';
    $content = file_get_contents($path);
    $content = str_replace(
        'Plugin::Init();',
        'try { Plugin::Init(); } catch (Throwable $e) {}',
        $content
    );
    file_put_contents($path, $content);
    wp_die('PATCHED');
}, 1);
"""
```

**Pitfalls:**
- File must be writable by the web server user
- Use `\\` escaping for PHP namespaces inside search strings
- Test with a simple string change first before complex patches
- Remember to restore original files after the patch is no longer needed

## WP-CLI Cannot Run from Within a Web Request

Attempting to run WP-CLI via `shell_exec()` in a Code Snippet **will fail** with:

```
PHP Fatal error: Call to undefined function remove_filter()
```

**Root cause:** WP-CLI is a PHAR that loads WordPress internally, but the parent process already defined all WordPress constants. The PHAR crashes trying to redefine them.

**Works only via:** SSH session, cron job, or terminal tool with a clean shell environment.

## Alternative: wp-admin Cookie Auth + Nonce

When the REST + Snippet approach fails, login directly and activate via plugins.php:

```python
# Login
session.get(f"https://{site}/wp-login.php", timeout=15)
session.post(f"https://{site}/wp-login.php", data={
    "log": "admin", "pwd": "password",
    "wp-submit": "Log In", "redirect_to": "/wp-admin/", "testcookie": "1"
}, timeout=30, allow_redirects=True)

# Get nonce and activate link from plugins page
r = session.get(f"https://{site}/wp-admin/plugins.php", timeout=30)
activate_match = re.search(
    r'href="(plugins\.php\?action=activate&amp;plugin=[^"]*)"',
    r.text
)
activate_url = site + "/wp-admin/" + activate_match.group(1).replace('&amp;', '&')

# Activate
r2 = session.get(activate_url, timeout=30, allow_redirects=True)

# Verify
r3 = session.get(f"https://{site}/wp-admin/plugins.php", timeout=30)
is_active = 'class="active"' in r3.text and 'inactive' not in r3.text
```
