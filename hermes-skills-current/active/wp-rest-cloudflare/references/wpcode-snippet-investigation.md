# WPCode Snippet Investigation via wp-admin

WPCode (formerly "Insert Headers and Footers" / "WPCode Pro") stores snippets in custom database tables, **not** as WordPress post types. There are **no REST API endpoints** for WPCode snippets — they cannot be listed, read, or modified via `/wp/v2/` routes.

To investigate or check WPCode snippets, you must scrape the wp-admin HTML.

## Finding Snippet Page URL

WPCode uses a custom admin page, not a post type. Snippets are accessed at:

```
/wp-admin/admin.php?page=wpcode-snippet-manager&snippet_id={ID}
```

The snippet list is at:
```
/wp-admin/admin.php?page=wpcode
```

## Checking Snippet Status & Settings

After logging into wp-admin with cookies (see `theme-editor-programmatic-access.md`), access the snippet editor page and scrape form fields:

```python
import urllib.request, urllib.parse, http.cookiejar, re

cj = http.cookiejar.CookieJar()
opener = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(cj))

# Login first (same as theme editor flow)
login_data = urllib.parse.urlencode({
    'log': 'admin',
    'pwd': 'password_with_special_chars',
    'wp-submit': 'Log In',
    'redirect_to': '/wp-admin/',
    'testcookie': '1'
}).encode()
req = urllib.request.Request("https://site.com/wp-login.php", data=login_data)
opener.open(req)

# Access snippet editor
req = urllib.request.Request(
    "https://site.com/wp-admin/admin.php?page=wpcode-snippet-manager&snippet_id=86668"
)
resp = opener.open(req)
html = resp.read().decode('utf-8')
```

## Key Fields to Extract

### Snippet Active Status

WPCode uses a checkbox with `name="wpcode_active"`:

```python
active = '<input type="checkbox"  checked=\'checked\' name="wpcode_active"'
is_active = active in html
```

### Auto-Insert Enabled

Hidden field with `name="wpcode_auto_insert"` — value `1` = enabled, `0` = disabled:

```python
auto_insert = re.search(r'name="wpcode_auto_insert"[^>]*value="(\d+)"', html)
is_auto_insert = auto_insert and auto_insert.group(1) == '1'
```

### Insertion Location (Radio Buttons)

WPCode uses radio buttons (not `<select>`) for location. Check for `checked='checked'`:

```python
location_match = re.search(
    r'<input[^>]*type="radio"[^>]*name="wpcode_auto_insert_location"[^>]*value="([^"]*)"[^>]*checked',
    html
)
location = location_match.group(1) if location_match else 'unknown'
```

Common location values:
- `everywhere` — Both frontend AND admin
- `frontend_only` — Public pages only
- `admin_only` — wp-admin only
- `frontend_cl` — Frontend with conditional logic
- `on_demand` — Manual execution only (via `wpcode()` function)

### Conditional Logic

Check if enabled:

```python
cl_checkbox = re.search(
    r'<input[^>]*name="wpcode_conditional_logic_enable"[^>]*checked',
    html
)
cl_enabled = bool(cl_checkbox)
```

### Code Type (PHP, HTML, JS, etc.)

```python
code_type = re.search(r'name="code_type"[^>]*value="([^"]+)"[^>]*checked', html)
snippet_type = code_type.group(1) if code_type else 'unknown'
# Common: "php", "html", "js", "text", "universal"
```

### Snippet Code Content

```python
code_match = re.search(r'<textarea[^>]*id="[^"]*code[^"]*"[^>]*>', html)
if code_match:
    start = code_match.end()
    end = html.index('</textarea>', start)
    code = html[start:end]
    # Unescape HTML entities
    code = code.replace('&#039;', "'").replace('&gt;', '>')
    code = code.replace('&lt;', '<').replace('&amp;', '&')
    code = code.replace('&quot;', '"')

# Key checks for PHP snippets:
php_open_count = code.count('<?php')
php_close_count = code.count('?>')
# WPCode auto-wraps PHP snippets — 0 open tags is normal for "PHP Snippet" type
```

### Save/Update Nonce

```python
nonce = re.search(r'name="wpcode-save-snippet-nonce"[^>]*value="([^"]+)"', html).group(1)
```

## Common Investigation Scenarios

### "WPCode snippet not showing on page"

If the user reports a WPCode snippet stopped appearing:

1. **Check Active status** — Is `wpcode_active` checked?
2. **Check Auto-Insert** — Is `wpcode_auto_insert` set to `1`?
3. **Check Location** — Is it `everywhere` or `frontend_only`? (NOT `on_demand`)
4. **Check Code** — Scan for `return;` or `if (!condition)` early-exit conditions
5. **Check Output hooks** — PHP snippets typically use `add_action` or `add_filter`. Verify the hooks exist and match WordPress execution flow. Common:
   - `add_filter('the_content', ...)` — Won't fire on Elementor pages (Elementor bypasses `the_content`)
   - `add_action('wp_head', ...)` — Should fire on all pages
   - `add_action('wp_footer', ...)` — Should fire on all pages
6. **Check for PHP errors** — WPCode catches PHP fatal errors silently. Check the WPCode error log at `wp-admin/admin.php?page=wpcode-tools&tab=logs`
7. **Check Page Source for output** — Search for unique strings from the snippet's expected output in the page HTML. Even if visual elements are missing, their HTML/CSS/JS should be in the source. Use `grep -c "unique_snippet_string"` on the curl output.

### "WPCode snippet output is visible but broken"

- Check for CSS `display:none` from other plugins/functions.php
- Check for JavaScript errors in console (PhastPress may defer JS execution)
- Check if Elementor snippet outputs conflicting CSS/js

## Limitations

- **No REST API.** Cannot use application passwords. Must use cookie-based admin login.
- **No bulk operations.** Each snippet must be checked individually by ID.
- **No easy error detection.** WPCode doesn't expose execution errors via page scraping. Visit the WPCode Tools → Logs page separately.
- **Saving snippets requires JavaScript.** The WPCode editor uses CodeMirror (JS-based code editor). The `newcontent` value must be submitted via the form's POST, NOT via API. Use the nonce and form fields extracted from the page.

## Distinguishing WPCode from Elementor Snippets

Users often confuse these two systems since both are called "code snippets":

| Feature | WPCode | Elementor Snippets |
|---------|--------|-------------------|
| **Post type** | Custom DB tables | `elementor_snippet` (WP post type) |
| **REST API** | ❌ None | ✅ `/wp/v2/elementor_snippet` |
| **Storage** | Database + optional file export | WordPress posts with `meta._elementor_code` |
| **Locations** | `everywhere`, `frontend_only`, hooks, CSS selectors | `elementor_head`, `elementor_body_start`, `elementor_body_end` |
| **Code types** | PHP, HTML, JS, Text, Universal | Generic (always output as raw text) |
| **Conditional logic** | ✅ Built-in | ❌ None |
| **Priority** | Numeric `wpcode_priority` | Numeric `_elementor_priority` |

When debugging "missing snippet output":
1. First check if it's a WPCode snippet (no REST API → scrape admin)
2. If it's an Elementor snippet, use REST API (`/wp/v2/elementor_snippet/{id}`)
3. Check PhastPress cache — append `?phast=-phast` to bypass
4. Check Cloudflare cache — `cf-cache-status: HIT` means Cloudflare is serving stale
