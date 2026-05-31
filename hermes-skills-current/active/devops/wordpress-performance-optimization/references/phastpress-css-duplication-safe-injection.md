# PhastPress CSS Duplication & Safe Injection Methods

## Problem: PhastPress Duplicates CSS from Post Content `<style>` Blocks

PhastPress v3.9 extracts CSS from `<style>` tags inside post content (`the_content`), minifies it, and inlines it in `<head>`. **However**, it also re-renders the original `<style>` content as visible HTML text — producing CSS property declarations as visible text at the top of blog posts.

### Symptoms
- CSS rules like `.gutf-article { max-width: 100% !important; ... }` appear as plain text between the head's `<style>` blocks or at the top of `<body>`
- The same CSS appears **twice**: once inside a `<style>` tag (correctly hidden) and once as visible text
- `@media` queries may be stripped by WordPress `wp_filter_post_kses` during REST API saves, causing the remaining CSS to apply globally instead of responsively

### Root Cause
1. CSS is injected into post content via REST API (`wp/v2/posts/ID` with `content` field)
2. WordPress applies `wp_filter_post_kses` sanitization which can strip `@media` queries
3. PhastPress processes the post content, extracts CSS from `<style>` blocks for head inlining
4. PhastPress also outputs the remaining CSS text outside the `<style>` wrapper as visible text

## Safe Injection Methods (No Duplication)

### Method 1: Insert Headers and Footers Plugin (Best)
The `jamify_hfs_insert_header` option is injected in `<head>` and NOT processed by PhastPress's content pipeline. No duplication.

```bash
# Get nonce from settings page
NONCE=$(curl -sk --resolve site.com:443:ORIGIN_IP -b cookies.txt \
  "https://site.com/wp-admin/options-general.php?page=header-and-footer-scripts" \
  -H "Host: site.com" | grep -oP '_wpnonce value="\K[a-f0-9]+')

# POST CSS wrapped in <style> tags
CSS='<style>@media (max-width: 768px) { .class { padding: 16px !important; } }</style>'
curl -sk --resolve site.com:443:ORIGIN_IP -b cookies.txt \
  -X POST "https://site.com/wp-admin/options.php" -H "Host: site.com" \
  --data-urlencode "jamify_hfs_insert_header=${CSS}" \
  --data-urlencode "option_page=header-and-footer-scripts" \
  --data-urlencode "action=update" \
  --data-urlencode "_wpnonce=${NONCE}" \
  --data-urlencode "_wp_http_referer=/wp-admin/options-general.php?page=header-and-footer-scripts" \
  -L
```

### Method 2: WordPress Custom CSS (Customizer)
The `wp-custom-css` output in `<head>` is also not processed by PhastPress content pipeline.

Use the `customize_save` AJAX action with the customizer nonce:
```bash
NONCE=$(curl -sk ... "https://site.com/wp-admin/customize.php" | grep -oP 'nonce=\K[a-f0-9]+')
CUSTOMIZED=$(python3 -c "import json; print('customized=' + json.dumps(json.dumps({'custom_css': '@media...'})))")
curl -sk ... -d "action=customize_save&nonce=${NONCE}&${CUSTOMIZED}" "admin-ajax.php"
```

### Method 3: Elementor Snippet with `elementor_head` location
Use `POST /wp-json/wp/v2/elementor_snippet` with `_elementor_location=elementor_head` and `_elementor_code` containing `<style>...</style>`.

⚠️ **Risk:** Elementor may strip `<style>` tags from `_elementor_code`, causing visible text. See wp-rest-cloudflare → references/elementor-snippet-rest-api.md.

### Method 4: Direct Theme style.css
Only if writable and you have FTP/shell access. Not available through REST API alone.

## What Does NOT Work

- **Injecting CSS inside post content `<style>` blocks via REST API** — PhastPress WILL duplicate it as visible text
- **WPCode CSS snippets** — no REST API available (stored in custom DB tables)
- **In-database Elementor post meta** (`_elementor_css`) — requires knowing internal meta keys and may be overwritten on Elementor save

## Cache Clearing After Injection

Even with safe injection, PhastPress caches the full rendered page. To make the CSS visible to end users:

1. **Save PhastPress settings** (even without changes) — triggers cache rebuild
2. **Deactivate/reactivate PhastPress** in plugin list
3. **Delete `wp-content/cache/phastpress/`** via WP File Manager

No AJAX endpoint for PhastPress cache clearing was reliable in v3.9 — the Vue.js SPA uses internal state management that doesn't expose a simple "clear" action to admin-ajax.

## Verification

Always verify across three layers:
```bash
# 1. Raw WordPress output (bypasses PhastPress entirely)
curl -s "https://site.com/?phast=-phast" | grep "your-css-marker"

# 2. Cache-busted processed output (bypasses page cache, keeps optimizations)
curl -s "https://site.com/?cb=$(date +%s)" | grep "your-css-marker"

# 3. Clean URL (what visitors see — MUST match for the fix to be live)
curl -s "https://site.com/" | grep "your-css-marker"
```
If (1) and (2) show the CSS but (3) doesn't, PhastPress page cache is still serving the old version. Flush cache and recheck.
