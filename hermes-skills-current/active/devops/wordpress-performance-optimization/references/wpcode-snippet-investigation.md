# WPCode Snippet Investigation

## Overview

WPCode (formerly "Insert Headers and Footers" / "InsaneWPCode") is a WordPress plugin for managing PHP/JS/HTML snippets. Unlike Elementor Custom Code (which uses `elementor_snippet` custom post type accessible via REST API), WPCode stores snippets in its own database tables with NO REST API exposure.

## Key Differences from Elementor Snippets

| Aspect | Elementor Snippets | WPCode Snippets |
|--------|-------------------|-----------------|
| Storage | `wp_posts` (post type `elementor_snippet`) | Custom DB tables (`wp_wpcode_snippets`) |
| REST API | Full CRUD at `/wp/v2/elementor_snippet` | **None** — no REST endpoints exposed |
| Location | Set via `_elementor_location` meta field | Radio button UI, stored as `location` column |
| Code field | `_elementor_code` meta field (plain text) | `code` column (HTML-encoded on display) |
| Auto-insert | Always auto (location determines where) | `auto_insert` column (0/1) |

## Detecting a WPCode Snippet

If the user says "my author bio/schema/code isn't showing" and `/wp/v2/elementor_snippet` shows nothing relevant, it's a WPCode snippet:

```bash
# Check if WPCode plugin exists
curl -s -u "user:app_password" "https://site.com/wp-json/wp/v2/plugins?search=wpcode" \
  | jq '.[] | {plugin, status, name}'
```

## Reading a WPCode Snippet (via wp-admin)

WPCode snippets are NOT accessible via REST API. You must use a browser session:

```python
import urllib.request, urllib.parse, http.cookiejar, re

cj = http.cookiejar.CookieJar()
opener = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(cj))

# Login
login_data = urllib.parse.urlencode({
    'log': 'username',
    'pwd': 'password',
    'wp-submit': 'Log In',
    'redirect_to': '/wp-admin/',
    'testcookie': '1'
}).encode()
req = urllib.request.Request("https://site.com/wp-login.php", data=login_data)
opener.open(req)

# Visit snippet manager
req = urllib.request.Request(
    "https://site.com/wp-admin/admin.php?page=wpcode-snippet-manager&snippet_id=SNIPPET_ID"
)
resp = opener.open(req)
html = resp.read().decode('utf-8')

# Extract code from textarea
code_match = re.search(r'<textarea[^>]*name="wpcode_snippet_code"[^>]*>', html)
start = code_match.end()
end = html.index('</textarea>', start)
code_html = html[start:end]  # HTML-encoded version as displayed in textarea
```

## Checking Snippet Status

From the snippet edit page HTML:

```python
# Check if active
active_found = 'checked' in re.search(
    r'<input[^>]*name="wpcode_active"[^>]*>', html
).group(0)

# Check location (radio buttons)
location_match = re.search(
    r'name="wpcode_auto_insert_location"[^>]*value="([^"]+)"[^>]*checked',
    html
)
location = location_match.group(1) if location_match else "unknown"

# Check auto-insert toggle
auto_insert = re.search(r'name="wpcode_auto_insert"[^>]*value="([^"]*)"', html)
```

## The Encoding Trap

**NEVER** edit WPCode snippets via direct POST to the admin page. The WPCode plugin stores PHP code with HTML-encoded entities (`&#039;` for `'`). When you decode the textarea content and re-submit, WPCode re-encodes the `&` characters, producing:

- 1st save: `&#039;` (correct)
- 2nd save (via API): `&amp;#039;` (double-encoded)
- 3rd save: `&amp;amp;#039;` (triple-encoded)

The PHP code becomes:
```php
// Before (working):
add_filter('the_content', 'aegis_render_author_bio', 999);

// After double-encoding:
add_filter(&amp;#039;the_content&amp;#039;, &amp;#039;aegis_render_author_bio&amp;#039;, 999);
```

This is invalid PHP that silently fails. The only fix is via the WPCode browser UI.

## Common Issue Check: Filter Hook Not Running

If a WPCode PHP snippet registers a `the_content` filter but the content never gets modified, check:

1. **Priority too low** (`< 10`): `is_single()` and `get_post_type()` may not be set up yet. Use priority `50+`.
2. **Priority too high** (`~999`): Filter runs LAST, after all other plugins. Content is fully processed.
3. **Encoding corruption**: The `add_filter` call has `&amp;#039;` instead of `'` — the PHP parser sees invalid syntax.
4. **Elementor override**: Elementor's `theme-post-content` widget may override `the_content` output. Check if the page uses Elementor template.

## Fixing a Corrupted Snippet

The ONLY reliable fix is via the WPCode browser UI. There is no safe automated workaround via API/curl.

### Manual Fix (WPCode UI)

1. Log in to wp-admin via browser
2. WPCode → Code Snippets → Find the snippet → Edit
3. In the code editor textarea, find and replace all `&amp;#039;` back to `'`
4. Also check for `&amp;gt;` → `>` and `&amp;lt;` → `<`
5. Click Update

### Browser Console Fix (When Textarea Is Too Large for Manual Scanning)

If the snippet is 50,000+ characters and you can't visually find the corrupt lines:

```javascript
// 1. Fix the code in the textarea
const ta = document.querySelector('textarea[name="wpcode_snippet_code"]');
let code = ta.value;

// Fix encoding corruption
code = code.replace(/&amp;/g, '&');

// Fix broken constant values (common corruption from failed API saves)
code = code.replace(
    "const AUTHOR_IMAGE='...9';",
    "const AUTHOR_IMAGE='https://secure.gravatar.com/avatar/CORRECT_HASH?s=400&d=mm&r=g';"
);

// Fix specific code changes (e.g., change return from append to prepend)
// ⚠️ INDENTATION MUST MATCH EXACTLY — check with console.log(JSON.stringify(line))
code = code.replace('    return $content . $html;', '    return $html . $content;');

ta.value = code;
ta.dispatchEvent(new Event('input', { bubbles: true }));

// 2. Find and click the Update button (NOT form.submit())
const publishBtn = document.querySelector('button[name="button"][value="publish"]');
publishBtn.removeAttribute('disabled');
publishBtn.click();
```

### ⚠️ CRITICAL: `form.submit()` vs `button.click()`

`form.submit()` bypasses JavaScript event handlers that WPCode uses to process the form. The code change appears to take effect (HTTP request is sent), but WPCode's server-side processing:

1. Receives the raw textarea value
2. Applies `sanitize_textarea_field()` (HTML-encodes `'` → `&#039;`, `&` → `&amp;`)
3. Stores in database (already encoded once)
4. On reload, the textarea shows the encoded version

If you use `form.submit()`, WPCode never receives the `button` form field, so it doesn't know the form was submitted for saving. The page reloads with the OLD (un-encoded) data from the database.

**ALWAYS click the Update/Save button in the DOM**, not `form.submit()`. The correct button is:
- `button[name="button"][value="publish"]` — **the Update button**
- NOT `button#wpcode_execute_now` — this EXECUTES the snippet but doesn't save
- NOT `input[type="submit"]` — these don't trigger WPCode's JS handlers

### Pitfall: Exact Indentation in Textarea Replacements

WPCode's textarea preserves exact whitespace. A line like:
```
    return $html . $content;
```
Has **4 spaces** of indentation (not tabs). Replacements must match exactly:

```javascript
// ✅ CORRECT — includes the 4 spaces
code = code.replace('    return $html . $content;', '    return $content . $html;');

// ❌ WRONG — no leading spaces, won't match
code = code.replace('return $html . $content;', 'return $content . $html;');
```

To verify exact whitespace:
```javascript
const line = ta.value.split('\\n')[1150]; // or whatever line number
console.log(JSON.stringify(line)); // Shows every space and tab character
```

### Verification After Fix

1. Navigate away and back to the snippet editor page
2. Check the textarea content for `&amp;` — should be none
3. Check the target line (e.g., return statement) is correct
4. Verify the page output with cache-busting parameter

### Multi-Hook Architecture (Debugging Aid)

WPCode PHP snippets can register hooks at multiple locations. This is useful for debugging because a partial fix may make SOME hooks work while others remain broken:

| Hook | What It Renders | Failure Indicator |
|------|----------------|-------------------|
| `wp_head` (priority 1) | CSS styles (inline `<style>` block) | No AEGIS/author CSS in `<head>` |
| `the_content` (priority 999) | Author bio HTML (appended/prepended to content) | No author bio card in post content |
| `wp_footer` (priority 5) | JSON-LD structured data + resource hints | Missing verification/disclaimer schema |

Any one of these can fail independently:
- A broken PHP constant (e.g., corrupted `AUTHOR_IMAGE`) causes a **fatal parse error** that stops ALL hooks — nothing renders.
- A priority issue (`< 10` for `the_content` filter) breaks only `the_content` while CSS and JSON-LD still render.
- Encoding corruption in a single value (e.g., `define('CONSTANT', 'value&amp;more')`) may produce unexpected output but NOT break execution.

**First thing to check when the user says "my WPCode snippet doesn't show":** is the CSS in `<head>`? If yes, the PHP is executing — the issue is in `the_content` filter timing or encoding. If no CSS either, the PHP has a fatal error — check `&amp;` encoding and broken constants.
