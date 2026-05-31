# CSS Injection Pitfalls on WordPress Behind Cloudflare

## Fallback Hierarchy for CSS/Style Changes

When you need to inject CSS into a WordPress site behind Cloudflare (e.g., gearuptofit.com):

1. **Theme style.css via Theme File Editor** — fastest if writable. Check `file_not_writable` in response.
2. **Theme functions.php** — add `wp_add_inline_style` hook. Also may not be writable.
3. **WPCode Snippet** — CSS type snippet via admin-ajax.php. Use the proper WPCode admin form to save.
4. **Elementor Snippet** (`elementor_snippet` CPT) — ⚠️ **Strips `<style>` tags from output.** Only use for JavaScript or raw CSS injected into `<head>` without wrapping tags.
5. **Post content `<style>` block** — Read post via REST API GET, append CSS before the first `</style>` tag, POST back. Most reliable for per-post fixes.
6. **admin-ajax.php with customizer nonce** — ⚠️ Risk of CSS leaking into `<meta name="description">` via cache. Verify meta tag content after applying.
7. **Manual via browser** — Last resort when all automated paths fail.

## App Password Read-Only Pitfall

**Application passwords may be created with read-only scope.** Test write access before relying on it:

```bash
# Test read
curl -s "https://site.com/wp-json/wp/v2/posts/1" \
  -H "Authorization=[REDACTED] $(echo -n 'user:app_pass' | base64 -w0)"
# → HTTP 200 = read works

# Test write
curl -s -X POST "https://site.com/wp-json/wp/v2/posts/1" \
  -H "Authorization=[REDACTED] $(echo -n 'user:app_pass' | base64 -w0)" \
  -H "Content-Type: application/json" \
  -d '{"content":"<p>test</p>"}'
# → `rest_cannot_edit` (HTTP 401) = read-only
```

If write fails, you must use cookie-based auth or get a new app password with full scope.

## CSS Leaking Into Meta Description

When CSS injected via admin-ajax.php gets cached by PhastPress/Cloudflare, it can appear inside the `<meta name="description">` tag:

```
<meta name="description" content="/* POST LAYOUT FIX */ .gutf-article { max-width: 100% !important; ..." />
```

**Debug:** Check the meta description tag directly:

```bash
curl -s "https://site.com/post-slug/" \
  | grep -oP 'name="description"[^>]*content="\K[^"]+'
```

**Causes:**
- Caching plugin (PhastPress) combined the style block content with meta description during minification
- The fix was applied via a non-standard mechanism (customizer nonce) that didn't respect proper WordPress hooks
- Cloudflare cached the broken HTML before the cache could be purged

**Fix:** 
- Clear all caches (PhastPress, Cloudflare, plugin cache)
- The CSS text is not actually visible on the page — it's in the meta tag only
- The meta tag content is not rendered to users, but shows in search previews

## Cache Purge Actions That Fail Silently

These admin-ajax actions return "0" without authentication:

- `phast_clear_cache` — needs admin session + nonce
- `cloudflare_purge_cache` — needs plugin-specific nonce
- `rocket_purge_cache` — needs WP Rocket nonce

Do not rely on these from REST-only sessions. They require full cookie-based admin auth.

## CSS Injection via Post Content `<style>` Block (Working Method)

When all other CSS injection paths fail, insert CSS into the existing `<style>` block at the start of the post content:

```bash
# 1. Read current content
curl -s "https://site.com/wp-json/wp/v2/posts/ID?edit=true" \
  -H "Authorization=[REDACTED] ..." > post.json

# 2. Extract and modify
python3 << 'EOF'
import json
with open('post.json') as f:
    d = json.load(f)
rendered = d['content']['rendered']

# Find first </style>
idx = rendered.find('</style>')
if idx < 0:
    print("No style block found")

# Insert CSS before closing </style>
css_block = '''
@media (max-width: 768px) {
  .gutf-article { max-width: 100% !important; }
}
'''
new_content = rendered[:idx] + '\n' + css_block.strip() + '\n' + rendered[idx:]

with open('updated.json', 'w') as f:
    json.dump({'content': new_content}, f)
EOF

# 3. POST back (requires write-capable app password)
curl -s -X POST "https://site.com/wp-json/wp/v2/posts/ID" \
  -H "Authorization=[REDACTED] ..." \
  -H "Content-Type: application/json" \
  -d @updated.json
```

**Important:** The post content starts with `<style>` (no raw field). Always use the `rendered` content from the GET response, modify it, and POST it back as the `content` field.

## Why Theme style.css Is Often Not Writable

On many managed WordPress hosts, the web server user (www-data) does not own the theme files. Even with the Theme File Editor UI, the save function returns a `file_not_writable` template:

```html
<# } else if ( 'file_not_writable' === data.code ) { #>
  You need to make this file writable before you can save your changes.
```

Check for this pattern in the theme editor response. If present, ALL file-based CSS injection paths are blocked.

## Detection: Check Where CSS Actually Ended Up

After any CSS injection attempt on a Cloudflare-hosted WordPress site:

```bash
# 1. Check meta description
curl -s "https://site.com/post/" | grep -oP 'name="description" content="\K[^"]+' | head -1

# 2. Check page body for visible CSS text
curl -s "https://site.com/post/" | grep -oP 'gutf-article \{ max-width: 100%'

# 3. Check <head> style blocks
curl -s "https://site.com/post/" | python3 -c "
import sys, re
html = sys.stdin.read()
head = html[:html.find('</head>')]
styles = re.findall(r'<style[^>]*>(.*?)</style>', head, re.DOTALL)
for i, s in enumerate(styles):
    if 'gutf-article' in s:
        print(f'Style block {i}: {len(s)} bytes, has gutf-article')
"

# 4. Check <body> style blocks
curl -s "https://site.com/post/" | python3 -c "
import sys, re
html = sys.stdin.read()
body = html[html.find('<body>'):]
styles = re.findall(r'<style[^>]*>(.*?)</style>', body, re.DOTALL)
for i, s in enumerate(styles):
    if 'gutf-article' in s:
        print(f'Body style block {i}: {len(s)} bytes')
"
```
