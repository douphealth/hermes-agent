# Cloudflare Origin IP Bypass for wp-admin Access

When Cloudflare blocks `/wp-login.php` and `/wp-admin/`, but you know the server's **origin IP**, access the admin panel directly via the IP with the correct `Host` header.

## Prerequisites

- Server origin IP (e.g., `104.168.100.41`)
- WordPress admin credentials (username + password)
- Application Password for REST API — **check the secrets file for the correct user/password pair** (see Pitfalls below)

## Step 1: Login via origin IP

### Method A: Raw IP with `-k`

```bash
urlencode() {
  python3 -c "import urllib.parse,sys; print(urllib.parse.quote(sys.argv[1], safe=''))" "$1"
}
PWD_ENCODED=$(urlencode 'your_password_with_$pec!@ls')

curl -s -k -c /tmp/wp_cookies.txt \
  -H "Host: gearuptofit.com" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  "https://104.168.100.41/wp-login.php" \
  -d "log=admin&pwd=[REDACTED]https://104.168.100.41/wp-admin/')}&testcookie=1" \
  -o /dev/null \
  -w "HTTP_CODE: %{http_code}\n"
```

Expect HTTP 302 (redirect) = success. HTTP 200 with login form = wrong password.

### Method B: `--resolve` (SOTA — preserves SSL hostname matching)

Avoids browser cert errors by mapping the domain to the origin IP at the DNS resolution level:

```bash
curl -sk --resolve gearuptofit.com:443:104.168.100.41 \
  -c /tmp/wp_cookies.txt \
  "https://gearuptofit.com/wp-login.php" \
  -H "Host: gearuptofit.com" \
  --data-urlencode "log=admin" \
  --data-urlencode "pwd=[REDACTED] \
  --data-urlencode "wp-submit=Log In" \
  --data-urlencode "redirect_to=/wp-admin/" \
  --data-urlencode "testcookie=1" \
  -L 2>/dev/null | grep -c Dashboard
```

**Why this works:** The `--resolve` flag overrides DNS resolution for the specific hostname:port:IP triple, so the TLS handshake uses the real domain name. This makes the SSL connection work correctly even though the IP is direct-to-origin. The `-k` flag may still be needed if the origin cert is self-signed or uses Cloudflare Origin CA certs that don't match the domain.

**Note:** `--data-urlencode` properly handles special characters in passwords (`&`, `$`, `#`, etc.) vs the raw `-d` string which would interpret them as shell/syntax characters.

## Step 2: Access wp-admin pages

All standard wp-admin pages work with the cookies + Host header:

```bash
# Dashboard
curl -s -k -b /tmp/wp_cookies.txt \
  -H "Host: gearuptofit.com" \
  "https://104.168.100.41/wp-admin/" | grep -c "wp-admin-bar\|dashboard"

# Theme file editor
curl -s -k -b /tmp/wp_cookies.txt \
  -H "Host: gearuptofit.com" \
  "https://104.168.100.41/wp-admin/theme-editor.php?file=style.css&theme=twentyten-child"

# WP File Manager (if installed)
curl -s -k -b /tmp/wp_cookies.txt \
  -H "Host: gearuptofit.com" \
  "https://104.168.100.41/wp-admin/admin.php?page=wp_file_manager"
```

With `--resolve`, use the real domain in the URL instead:

```bash
curl -sk --resolve gearuptofit.com:443:104.168.100.41 \
  -b /tmp/wp_cookies.txt \
  "https://gearuptofit.com/wp-admin/options-general.php?page=phast-press" \
  -H "Host: gearuptofit.com"
```

## Step 3: Verify successful login

```bash
# Successful login returns the admin dashboard HTML
curl -sk --resolve gearuptofit.com:443:104.168.100.41 \
  -b /tmp/wp_cookies.txt \
  "https://gearuptofit.com/wp-admin/" \
  -H "Host: gearuptofit.com" | grep -o '<title>[^<]*</title>'

# Expected: "Dashboard ‹ Site Name — WordPress"
# Failed login: "Log In ‹ Site Name — WordPress"
```

## Pitfalls

### 🚫 Cloudflare Worker must not treat wp-admin `&s` as public search

WordPress plugin activate/deactivate links often include a bare `&s` query parameter:

```text
/wp-admin/plugins.php?action=activate&plugin=elementor%2Felementor.php&plugin_status=all&paged=1&s&_wpnonce=...
```

If an apex Worker routes any request with `url.searchParams.has("s")` to WordPress search/front-end logic, plugin actions will silently fail or show the wrong page. Always exclude admin/login paths before public search routing:

```js
const wpAdminPath = url.pathname.startsWith('/wp-admin') || url.pathname === '/wp-login.php';
const searchRequest = !wpAdminPath && url.searchParams.has('s');
```

Also rewrite wp-admin HTML/redirects from `origin.gearuptofit.com` to `gearuptofit.com`; otherwise admin JS canonical/history, REST root URLs, cookies, and nonces can break activation flows.

### 🚫 App Password vs WP-Admin Credentials — Use the Right One

The credentials file (`/home/hermes/.secrets/alexiios-websites-credentials.txt`) has **two separate sections** per site:

```
[WP-Admin Credentials]        ← use for wp-login.php / origin-IP login
site.com|admin|PASSWORD

[REST API Passwords]          ← use for REST API calls
site.com|admin|APP_PASSWORD
```

These may use **different usernames and passwords**. The wp-admin user might be `admin` while the REST API user is the same `admin` but with a different application password string. **Always check both sections** before attempting authentication.

Symptoms of using wrong credentials:
- `rest_cannot_edit` or `rest_not_logged_in` when trying REST API write — you're probably using the wrong app password
- HTTP 200 (login form) instead of 302 (redirect) — wrong wp-admin password
- `curl --resolve` returns login page HTML after POST — password is wrong

### 🚫 REST API: `edit=true` vs Regular Endpoint Returns Different Content

The standard post endpoint **silently returns different content** depending on the query parameter:

| Endpoint | What it returns |
|----------|----------------|
| `/wp/v2/posts/ID` | `post_content` passed through `the_content` filter (includes PhastPress processing, auto-p, shortcodes) |
| `/wp/v2/posts/ID?edit=true` | Raw `post_content` directly from the database |

When debugging content issues:
```bash
# Get the FILTERED content (what PhastPress/Elementor sees)
curl -s -u "user:pass" "https://site.com/wp-json/wp/v2/posts/ID" \
  | python3 -c "import sys,json; d=json.load(sys.stdin); c=d['content']['rendered']; print(f'{len(c)} bytes: {c[:200]}')"

# Get the RAW content (what's in the database)
curl -s -u "user:pass" "https://site.com/wp-json/wp/v2/posts/ID?edit=true" \
  | python3 -c "import sys,json; d=json.load(sys.stdin); c=d['content']['rendered']; print(f'{len(c)} bytes: {c[:200]}')"
```

**If lengths differ significantly**, PhastPress or another filter is transforming the content. The `edit=true` version is what you actually stored — check this first when CSS injections don't appear or CSS shows as visible text.

### 🚫 WordPress Strips `@media` from Inline CSS in Post Content

When saving post content via REST API with `<style>` blocks containing `@media` queries, WordPress's content sanitization (`wp_filter_post_kses`) strips the `@media` keyword and emits the remaining CSS rules as **visible text outside the `<style>` tag**.

**What happens in the database:**
1. You POST: `<style>@media (max-width: 768px) { .foo { color:red } }</style>`
2. WP saves (via `edit=true`): Same — looks clean.
3. WP renders (via public endpoint): `<style></style><p>@media (max-width: 768px) { .foo { color:red } }</p>`

The CSS rules end up as visible text on the page because the `@media` gets stripped but the remaining CSS rules survive as text nodes inside `<p>` tags (WordPress auto-p wraps them).

**Detection:**
```bash
# Check if @media got stripped and CSS is now visible text
curl -s -u "user:pass" "https://site.com/wp-json/wp/v2/posts/ID" \
  | python3 -c "
import sys,json,re
d=json.load(sys.stdin)
c=d['content']['rendered']
# Remove style blocks
text_only = re.sub(r'<style>.*?</style>', '', c, flags=re.DOTALL)
if 'max-width' in text_only or 'gutf-article' in text_only:
    print('❌ CSS is visible text outside <style> tags')
    for m in re.finditer(r'[^.<]{0,40}(?:max-width|gutf-article)[^<]{0,80}', text_only):
        print(f'   Found: {m.group().strip()[:80]}')
else:
    print('✅ No visible CSS outside style blocks')
"
```

**Workarounds (pick one):**
1. **Use `wp_head`/functions.php** instead of post content — no content sanitization applies
2. **Use Elementor Snippets** (`elementor_head` location) — sidesteps post content filter entirely
3. **Use Insert Headers and Footers plugin** — dedicated code injection area, no filter
4. **Write mobile-first CSS without `@media`** — default styles serve mobile, override with `min-width` media queries in theme CSS (not in post content)
5. **Direct theme file edit** via WP File Manager or theme editor — bypasses all content filters

## Cookie lifecycle

Cookies expire after ~15-20 minutes. If you get a 302 redirect from any wp-admin page back to wp-login.php, re-authenticate:

```bash
curl -sk --resolve gearuptofit.com:443:104.168.100.41 \
  -c /tmp/wp_cookies_fresh.txt \
  "https://gearuptofit.com/wp-login.php" \
  -H "Host: site.com" \
  --data-urlencode "log=admin" \
  --data-urlencode "pwd=[REDACTED] \
  --data-urlencode "wp-submit=Log In" \
  --data-urlencode "redirect_to=/wp-admin/" \
  --data-urlencode "testcookie=1" \
  -L
```

Always use a fresh cookie jar per session. Don't reuse stale cookies.

## Nonce extraction pattern

The nonce in WordPress admin pages is embedded in URLs and forms:

```bash
# From theme editor URL parameter
grep -oP '_wpnonce=\K[a-f0-9]+' /tmp/theme_editor.html

# From JavaScript (customizer)
grep -oP 'nonce"\s*:\s*"[a-f0-9]+' /tmp/customize.html

# From admin-ajax.php URL
grep -oP 'action=rest-nonce[^"]*' /tmp/page.html
```

Nonces are tied to the user session and expire when cookies do. Always extract fresh nonces after login.

## Limitations

- **SSL mismatch:** `curl -k` (or `--insecure`) may still be required; use `--resolve` to minimize cert issues
- **Non-canonical URL blocking:** Some plugins check `$_SERVER['HTTP_HOST']` and refuse non-canonical requests. The `Host` header usually fixes this.
- **Cloudflare origin CA:** If the origin server has Cloudflare's origin certificate installed, Cloudflare may intercept even direct IP traffic. In this case, only REST API + Application Password works.
- **Elementor AJAX:** Elementor's admin-ajax endpoints may reject requests from non-canonical URLs even with correct cookies. Use REST API for Elementor operations.
- **PhastPress cache often can't be cleared via programmatic AJAX** — the Vue.js admin panel renders cache controls via JavaScript that's not easily scriptable. The admin-ajax `phast_clear_cache` action may return 400. Use the browser UI or the toggle-off/on workaround.

## Cloudflare Cache Persistence

Cloudflare edge cache can persist **well past the `max-age` TTL**:

- Even with `cache-control: max-age=3600` (1-hour TTL), Cloudflare may serve cached pages for **2+ hours** (`age: 7425` seconds observed)
- The `cf-cache-status: HIT` header confirms the page was served from Cloudflare's edge cache
- The `age` header (in seconds) tells you how long the page has been cached — check this to know if you're seeing stale content

**Bypassing Cloudflare cache for verification:**
```bash
# Check cache status
curl -sI "https://site.com/page/" | grep -i 'cf-cache-status\|age\|cache-control'

# Hit the origin directly (no Cloudflare edge caching)
curl -sk --resolve site.com:443:ORIGIN_IP "https://site.com/page/" -H "Host: site.com"
```

**Purge methods when API token is invalid:**
1. Cloudflare Dashboard → Caching → Configuration → Purge Everything (manual)
2. Cloudflare Dashboard → Caching → Purge Individual Files (enter URL)
3. Wait for TTL expiry (may take 2-3x the `max-age` value)
4. Change the page URL (update slug) — Cloudflare will cache the NEW URL fresh

## REST API Content Field: `raw` Object vs String

**CRITICAL:** The `wp/v2/posts` REST API `content` field is an **object**, not a string. Sending content as a plain string (`{'content': '<html>'}`) updates the post in the response body but **does not persist to the database**.

**Schema** (from `OPTIONS /wp/v2/posts/{ID}`):
```json
{
  "content": {
    "type": "object",
    "properties": {
      "raw": { "type": "string", "context": ["edit"] },
      "rendered": { "type": "string", "readonly": true },
      "block_version": { "type": "integer", "readonly": true },
      "protected": { "type": "boolean", "readonly": true }
    }
  }
}
```

**Correct usage:**
```python
# ✅ WORKS — content persists to database
requests.post("/wp/v2/posts/ID", json={'content': {'raw': '<div>new content</div>'}})

# ❌ DOES NOT WORK — content appears updated in response but DB unchanged
requests.post("/wp/v2/posts/ID", json={'content': '<div>new content</div>'})
```

**How to tell if the update persisted:**
```python
# After POST, verify with context=edit (NOT edit=true):
resp = requests.get("/wp/v2/posts/ID?context=edit")
raw = resp.json()['content']['raw']  # This shows the ACTUAL database content

# ❌ edit=true returns server-side CACHED content, NOT the DB
resp = requests.get("/wp/v2/posts/ID?edit=true")  # May return stale data for ~30-60s
```

### `context=edit` vs `edit=true` — Critical Difference

| Parameter | What it returns | Reliability |
|-----------|----------------|-------------|
| `?context=edit` | Raw `post_content` from database | ✅ Real-time, trusted for verification |
| `?edit=true` | Server-side cached `post_content` | ❌ May be stale for 30-60s after write |
| (no param) | `post_content` through `the_content` filter | ❌ Includes plugin transforms |

```bash
# Verify content was actually saved — use context=edit
curl -s -u "user:pass" "https://site.com/wp-json/wp/v2/posts/ID?context=edit" \
  | python3 -c "import sys,json; d=json.load(sys.stdin); print(d['content'].get('raw','')[:200])"

# Compare with edit=true (may show different/old content)
curl -s -u "user:pass" "https://site.com/wp-json/wp/v2/posts/ID?edit=true" \
  | python3 -c "import sys,json; d=json.load(sys.stdin); print(d['content'].get('rendered','')[:200])"
```

### POST Response vs Database — The Liar Pattern

The REST API `POST` response always includes the updated post object with the `rendered` content:
```python
resp = requests.post("/wp/v2/posts/ID", json={'content': {'raw': '<p>NEW</p>'}})
resp.json()['content']['rendered']  # Shows '<p>NEW</p>' — BUT THIS MAY NOT BE IN DB
```

Always verify with a separate GET request using `context=edit` before concluding the content changed.

## PhastPress `advanced-cache.php` Drop-in Persists After Deactivation

**Deactivating PhastPress does NOT remove `wp-content/advanced-cache.php`.** This drop-in continues serving cached full-page HTML snapshots indefinitely.

The `advanced-cache.php` file is registered as a WordPress "drop-in" (visible in `/wp-admin/plugins.php` under "Drop-ins"). It intercepts all page requests before WordPress loads and serves cached HTML from `wp-content/cache/`.

### Detection
```bash
# Check if advanced-cache.php is still active (in plugins page source)
curl -s -b cookies.txt "https://site.com/wp-admin/plugins.php" \
  | grep -oP '"dropins":\[\K[^\]]*'
# Look for "advanced-cache.php" in the output

# Check if page is served from cache (even without PhastPress active)
curl -s "https://site.com/page/" | grep -c 'phast'  # If >0, cached page still served
```

### Cleaning Up After PhastPress Deactivation

To fully disable PhastPress and serve fresh pages:

1. **Delete `wp-content/advanced-cache.php`** — removes the page-cache drop-in
2. **Delete `wp-content/cache/phastpress/` directory** — removes all cached HTML files
3. **Delete `wp-content/cache/phast/` directory** — alternative cache path
4. **Delete `wp-content/uploads/phastpress/` directory** — image cache
5. **Purge Cloudflare** — edge cache may still have old pages

**If you can't access the file system:**
- Wait for the cache files to expire (PhastPress cache rarely auto-expires without the plugin active)
- Re-activate PhastPress → save settings → deactivate again (may trigger cleanup)
- Use WP File Manager plugin (if installed) from wp-admin to delete the files

### Three-Layer Cache Architecture

WordPress + Cloudflare sites can have THREE independent cache layers:

```
Layer 1: Cloudflare (edge CDN)     → cf-cache-status: HIT/EXPIRED/MISS
Layer 2: advanced-cache.php        → PhastPress full-page cache on disk
Layer 3: WordPress object cache    → db.php drop-in (transients, options)
```

Changes must survive all three layers to be visible to visitors. The only way to confirm a change is live is to check all three:
```bash
# Layer 1: Bypass Cloudflare
curl -sk --resolve site.com:443:ORIGIN_IP "https://site.com/page/" | grep "your-marker"

# Layer 2: Bypass advanced-cache.php (via cache-busting param)
curl -s "https://site.com/page/?cb=$(date +%s)" | grep "your-marker"

# Layer 3: Clean URL — what real visitors see
curl -s "https://site.com/page/" | grep "your-marker"
```

## When to use this vs REST API

| Situation | Best approach |
|---|---|
| Read theme files | REST API for post types; origin IP for theme-editor.php |
| Edit functions.php/style.css | Origin IP + cookies (unless not writable) |
| Edit post/page content | REST API (application password) |
| Edit Elementor templates | REST API (elementor_library endpoint) |
| Create Elementor snippets | REST API (elementor_snippet endpoint) |
| Clear PhastPress cache | Origin IP + browser UI (admin-ajax unreliable) |
| Install/activate plugins | Origin IP + plugins.php page |
| Change settings | Both work; REST API is simpler |
| Inject site-wide CSS | `wp_head` hook or Insert Headers and Footers plugin (NOT in post content — `@media` gets stripped) |
