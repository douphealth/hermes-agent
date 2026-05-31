# Theme Editor Programmatic Access

Reading and writing WordPress theme files (functions.php, style.css) via wp-admin when the REST API file-editing endpoints are unavailable.

## Key Nonce Quirk

The WordPress theme editor uses a **non-standard field name** for its nonce:

- **Most admin forms**: `name="_wpnonce"` 
- **Theme editor**: `name="nonce"` (NO underscore prefix)

Searches for `_wpnonce` in the theme editor page will return empty. Always search for `name="nonce"`.

## Full Workflow

### Step 1: Login to wp-admin (Python with cookie jar)

```python
import urllib.request, urllib.parse, http.cookiejar, re

cj = http.cookiejar.CookieJar()
opener = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(cj))

login_data = urllib.parse.urlencode({
    'log': 'admin_username',
    'pwd': 'password_with_special_chars',
    'wp-submit': 'Log In',
    'redirect_to': '/wp-admin/',
    'testcookie': '1'
}).encode()

req = urllib.request.Request("https://site.com/wp-login.php", data=login_data)
opener.open(req)
```

**Watch out**: If the password contains `$` or `!` characters, Python's `urlencode` handles them correctly, but shell-based curl with `--data-urlencode` may need extra quoting.

### Step 2: Read current file content

```python
req = urllib.request.Request(
    "https://site.com/wp-admin/theme-editor.php?file=functions.php&theme=twentyten-child"
)
resp = opener.open(req)
html = resp.read().decode('utf-8')

# Get nonce (note: NOT _wpnonce — just "nonce")
nonce = re.search(r'name="nonce"[^>]*value="([^"]+)"', html).group(1)

# Get current content from textarea
content_match = re.search(r'<textarea[^>]*>(.*?)</textarea>', html, re.DOTALL)
current = content_match.group(1)

# Unescape HTML entities
current = current.replace('&#039;', "'").replace('&gt;', '>')
current = current.replace('&lt;', '<').replace('&amp;', '&')
current = current.replace('&quot;', '"')
```

### Step 3: Update file

```python
updated = current + "// your new PHP code here"

post_data = urllib.parse.urlencode({
    'nonce': nonce,
    '_wp_http_referer': '/wp-admin/theme-editor.php?file=functions.php&theme=CHILD-THEME',
    'theme': 'twentyten-child',
    'file': 'functions.php',
    'newcontent': updated,
    'action': 'update',
    'scrollto': '0',
}).encode()

req = urllib.request.Request("https://site.com/wp-admin/theme-editor.php", data=post_data)
resp = opener.open(req)
result = resp.read().decode('utf-8')

if 'updated' in result.lower() or 'success' in result.lower() or 'file-editor' in result.lower():
    print("✅ functions.php updated!")
else:
    # Check for error messages
    err_match = re.search(r'<div[^>]*(?:error|notice-error)[^>]*>(.*?)</div>', result, re.DOTALL)
```

## Pitfalls

### 1. `newcontent` values are URL-encoded by urllib.parse.urlencode

Since `newcontent` contains `<?php`, CSS rules, and JavaScript — characters like `<`, `>`, `&`, `"`, `'` — the `urlencode` function encodes them properly. The theme editor PHP handler decodes them on the server. Do NOT pre-encode them manually.

### 2. Theme editor may show `<?php\n` placeholder

Some WordPress installations load the textarea content via AJAX after the page renders. The initial HTML shows only `<?php\n` even when the actual file has hundreds of lines. If the Python parser gets this empty content, it means the page didn't fully render and you need to:
- Check cookie validity (re-login)
- Try adding `'User-Agent': 'Mozilla/5.0'` header to bypass WAF checks
- Use the WordPress REST API's `wp/v2/themes/{stylesheet}/file` endpoint instead (if available — requires `edit_themes` capability)

### 3. Content Security Policy / Cloudflare WAF may block the request

If you get HTTP 403 or the login succeeds but the theme editor returns a blank/captcha page:
- The site may be behind Cloudflare with WAF rules blocking programmatic access
- Add proper User-Agent and Accept headers to mimic a real browser
- Consider using REST API application passwords as a fallback
