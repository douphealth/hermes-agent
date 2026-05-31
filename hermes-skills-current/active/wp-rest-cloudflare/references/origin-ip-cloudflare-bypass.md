# Origin IP Bypass for Cloudflare-Protected WordPress Admin

When Cloudflare blocks wp-admin access (browser shows "Just a moment..." Cloudflare challenge or curl returns 403), use the server's origin IP address to bypass Cloudflare entirely.

## Prerequisites

You need the server's **origin IP address** from hosting credentials. This is typically found in the user's secrets file alongside the site's WordPress admin credentials.

Common hosting panels and their port defaults:
- HestiaCP/VestaCP: port 8090 (web panel), port 22 (SSH)
- cPanel: port 2083 (SSL web panel), port 22 (SSH)
- DirectAdmin: port 2222 (web panel)

## Technique: wp-admin via Origin IP

### Step 1: Direct login via origin IP

```bash
curl -s -k -c /tmp/wp_cookies.txt \
  -H "Host: gearuptofit.com" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  "https://104.168.100.41/wp-login.php" \
  -d "log=admin&pwd=[REDACTED]
```

Key requirements:
- **`-k`** — skip SSL verification (cert is for the domain, not the IP)
- **`Host: gearuptofit.com`** — tells nginx/apache which virtual host to serve
- **`-c /tmp/wp_cookies.txt`** — save auth cookies for subsequent requests
- **DO NOT use `-L` (follow redirects)** — redirects go to the public domain which re-triggers Cloudflare. Handle the 302 manually.
- The `redirect_to` should point to the origin IP, not the domain

### Step 2: URL-encode the password

The password often contains special characters (`@`, `!`, `$`, `%`, `(`, `)`). Use Python for proper encoding:

```python
import urllib.parse
pwd=[REDACTED]
encoded = urllib.parse.quote(pwd, safe='')
print(encoded)
# Output: 99d%28J%40%25aVil%40%24dbkkv%21ke8Fd
```

Alternatively, use curl's `--data-urlencode` flag:
```bash
curl -s -k -c /tmp/wp_cookies.txt \
  -H "Host: gearuptofit.com" \
  --data-urlencode "log=admin" \
  --data-urlencode "pwd=[REDACTED] \
  --data-urlencode "wp-submit=Log In" \
  --data-urlencode "redirect_to=https://104.168.100.41/wp-admin/" \
  --data-urlencode "testcookie=1" \
  "https://104.168.100.41/wp-login.php"
```

### Step 3: Verify login success

Check for 302 (not 200) — a 302 means successful login (redirecting to dashboard):

```bash
curl -s -k -b /tmp/wp_cookies.txt \
  -H "Host: gearuptofit.com" \
  "https://104.168.100.41/wp-admin/" \
  -o /tmp/dashboard.html \
  -w "HTTP_CODE: %{http_code}\n"

# Check for admin content
grep -c "dashboard-widgets\|wp-admin-bar\|wrap\|Welcome to WordPress" /tmp/dashboard.html
# Should return > 0 if authenticated
```

### Step 4: Keep cookies fresh

WordPress auth cookies expire. If you get a 302 redirect when accessing wp-admin, re-login:

```bash
# Login again to refresh cookies, then retry
```

## Cookie Domain Issue

Cookies are stored for `gearuptofit.com` (not the IP). When accessing via the IP, curl may not send them. Fix by forcing the cookie file:

```bash
curl -s -k -b /tmp/wp_cookies.txt  # Force-send all cookies in the file
```

The `-b` flag sends all cookies regardless of domain match.

## Puppeteer/Headless Browser Origin IP Access

When you need a REAL browser session (for Elementor SPA editor, JavaScript-rendered admin pages, or Cloudflare challenge bypass):

```js
const puppeteer = require('puppeteer-core');
const browser = await puppeteer.launch({
  executablePath: '/home/hermes/.cache/ms-playwright/chromium-1217/chrome-linux64/chrome',
  headless: true,
  args: [
    '--ignore-certificate-errors',
    '--no-sandbox',
    '--disable-setuid-sandbox',
    '--host-resolver-rules=MAP gearuptofit.com 104.168.100.41, MAP origin.gearuptofit.com 104.168.100.41'
  ]
});
const page = await browser.newPage();
await page.goto('https://gearuptofit.com/wp-login.php');
await page.type('#user_login', 'admin', {delay: 20});
await page.type('#user_pass', 'PASSWORD', {delay: 10});
await Promise.all([
  page.waitForNavigation({ timeout: 15000 }).catch(() => {}),
  page.click('#wp-submit')
]);
```

**How it works:**
- `--host-resolver-rules=MAP gearuptofit.com 104.168.100.41` makes Chrome resolve `gearuptofit.com` to the origin IP
- The browser still sends the correct `Host` header and TLS SNI, so the web server serves the right site
- `--ignore-certificate-errors` bypasses SSL mismatch (cert is for `gearuptofit.com`, not the IP)
- After login, navigate to any wp-admin URL using `https://gearuptofit.com/wp-admin/...`

**Use cases this enables:**
- Theme File Editor (inject/restore PHP code in functions.php)
- Elementor Tools (Regenerate CSS, Clear Files & Data)
- Elementor Kit editor (Custom CSS tab, Advanced settings)
- Options page (view/edit wp_options)
- WP File Manager (if installed)
- Plugin management (activate/deactivate/delete)

**Pitfalls:**
- Chrome binary path: `/home/hermes/.cache/ms-playwright/chromium-1217/chrome-linux64/chrome`
- `page.waitForTimeout()` DOES NOT EXIST in puppeteer-core — use `new Promise(r => setTimeout(r, N))`
- `has-text()` pseudo-selector NOT SUPPORTED in Puppeteer's `page.$()` — use `page.evaluate()` with `querySelectorAll`
- Elementor editor is an SPA: click gear icon → tabs load dynamically → CodeMirror needs `cmInstance.setValue('')`
- Theme Editor textarea selector: `textarea#newcontent` or `textarea[name="newcontent"]`
- ALWAYS restore functions.php after injecting temporary code
- The `_elementor_global_css` option is DISABLED on options.php — cannot edit directly

## Common Pitfalls

### 🚫 Cloudflare Challenges on POST to wp-login.php

Even the origin IP can trigger Cloudflare challenges if:
- The request follows a redirect (`-L` flag redirects to the public domain)
- The `Host` header is incorrect or missing
- The server has Cloudflare's "orange cloud" DNS at the origin level (unusual but possible)

**Fix:** Never use `-L`. Handle the 302 redirect manually. Point `redirect_to` to the origin IP, not the domain.

### 🚫 SSL Certificate Warning

The origin IP will NOT match the SSL certificate (which is issued for the domain name). Always use `-k` (or `--insecure`) with curl, or disable SSL verification in Python/other tools.

### 🚫 Nonce Validation Failure

WordPress nonces are tied to the admin URL. Accessing via origin IP may cause nonce validation to fail on POST requests even with valid cookies:

```html
<!-- Hidden in page HTML: -->
<div id="message" class="notice notice-info">
<p><strong>Did you know?</strong> There is no need to change your CSS here</p>
</div>
```

This means the form submission was processed but the nonce check failed silently — the file was NOT saved even though the page loaded.

**Fix:** Use the `admin-ajax.php` endpoint with the proper nonce instead of form POST, or use the REST API (which works via application passwords, independent of nonce).

## When Origin IP Fails

If the origin IP approach doesn't work (e.g., hosting is behind a load balancer or the IP is a shared reverse proxy), fall back to:

1. **REST API with Application Passwords** — Works independently of Cloudflare for most read/write operations
2. **Hosting Panel Web UI** — HestiaCP/VestaCP on port 8090, cPanel on port 2083
3. **SSH/SFTP** — If the hosting panel offers file manager or SSH access
4. **WordPress CLI (wp-cli)** — If SSH is available on the server
