# Elementor Template Management via REST API

When Cloudflare blocks wp-admin, manage Elementor templates entirely through REST endpoints.

## Find Elementor templates by type

```bash
# List headers
curl -s "https://site.com/wp-json/wp/v2/elementor_library?elementor_library_type=header" \
  -H "Authorization=[REDACTED] $B64"

# List footers
curl -s "https://site.com/wp-json/wp/v2/elementor_library?elementor_library_type=footer" \
  -H "Authorization=[REDACTED] $B64"

# List all Elementor library posts (omit type filter for all)
curl -s "https://site.com/wp-json/wp/v2/elementor_library?per_page=50" \
  -H "Authorization=[REDACTED] $B64"
```

Filterable template types via `elementor_library_type` taxonomy param: `header`, `footer`, `single-post`, `single-page`, `archive`, `section`, `popup`.

## Read/update template display conditions

Elementor stores display conditions in a separate endpoint from the template content.

```bash
# READ: returns array of condition objects
curl -s "https://site.com/wp-json/elementor/v1/site-editor/templates-conditions/{TEMPLATE_ID}" \
  -H "Authorization=[REDACTED] $B64"

# Example response:
# [{"type":"include","name":"general","sub_name":"","sub_id":""}]

# UPDATE: PUT the full condition array
curl -s -X PUT "https://site.com/wp-json/elementor/v1/site-editor/templates-conditions/{TEMPLATE_ID}" \
  -H "Authorization=[REDACTED] $B64" -H "Content-Type: application/json" \
  -d '[
    {"type":"include","name":"general","sub_name":"","sub_id":""},
    {"type":"exclude","name":"front_page","sub_name":"","sub_id":""}
  ]'
```

Common condition names: `general` (all pages), `front_page`, `single_post`, `single_page`, `archive`, `search`, `by_author`, `category`, `by_role`.

Pattern: include + exclude combinations. To show on all pages EXCEPT front page: include `general` + exclude `front_page`. To show ONLY on single posts: just include `single_post`.

## Inject custom CSS/JS via Elementor code snippets

When you can't write to functions.php (no file access, Cloudflare blocks theme editor), use Elementor's built-in snippet post type as a backdoor.

```bash
# Step 1: Create the snippet post (notes its ID)
ID=$(curl -s -X POST "https://site.com/wp-json/wp/v2/elementor_snippet" \
  -H "Authorization=[REDACTED] $B64" -H "Content-Type: application/json" \
  -d '{"title":"Custom CSS Injection","status":"publish","type":"css"}' \
  | python3 -c "import json,sys; print(json.load(sys.stdin)['id'])")

# Step 2: Set the actual CSS code and output location via meta
curl -s -X POST "https://site.com/wp-json/wp/v2/elementor_snippet/$ID" \
  -H "Authorization=[REDACTED] $B64" -H "Content-Type: application/json" \
  -d '{
    "meta": {
      "_elementor_code": "body.home header { display:none!important }",
      "_elementor_location": "elementor_head",
      "_elementor_priority": 1
    }
  }'
```

Meta schema:
- `_elementor_code` (string) — the CSS or JS code
- `_elementor_location` (string) — `elementor_head` (in `<head>`) or `elementor_body_end` (before `</body>`)
- `_elementor_priority` (int) — output order priority (lower = earlier)

### Pitfalls

- The snippet post type content/rendered is always empty. Code lives ONLY in `_elementor_code` meta.
- CSS snippets may not render if PhastPress or another caching plugin minifies/concat styles. Append `?nocache=1` during testing.
- **Elementor snippets (`elementor_snippet`) do NOT reliably inject JS/CSS via REST alone.** Creating a snippet with `_elementor_code` and `_elementor_location: elementor_head` does NOT guarantee it appears on rendered pages. The Elementor Snippets feature requires additional condition configuration (via the Elementor admin UI) that may not take effect through REST meta updates alone. The `_elementor_conditions` meta key is also silently ignored by the REST API — conditions must be set through the native Elementor admin interface. **Do not rely on elementor_snippet for critical CSS/JS injection when wp-admin is blocked.** Use page content editing (`wp/v2/pages`) or theme file editing instead.
- The `type` field on creation (`css`, `js`, `php`) determines how Elementor renders it. CSS and JS auto-embed; PHP may be blocked by DISALLOW_FILE_EDIT.

### 🚫 HEADER/FOOTER CONDITIONS ARE BRITTLE VIA REST

**PUT/POST to `elementor/v1/site-editor/templates-conditions/{ID}` can silently corrupt conditions.** The endpoint returns `true` even when the write fails, and subsequent GET requests may show an empty array `[]` while the stored meta (`_elementor_conditions`) still shows the old value. This creates a split-brain state where the meta says one thing but Elementor's runtime picks up nothing.

**To avoid this:**
- Always **read conditions BEFORE** modifying. Save the original response as your rollback.
- After PUT, **verify with a second GET** that the conditions are what you set.
- If conditions are empty after a PUT, fall back to setting `_elementor_conditions` directly in the elementor_library meta:
  ```bash
  curl -s -X POST "https://site.com/wp-json/wp/v2/elementor_library/{ID}" \
    -H "Authorization=[REDACTED] $B64" -H "Content-Type: application/json" \
    -d '{"meta":{"_elementor_conditions":["include/general"]}}'
  ```
  (This may also silently fail — the meta endpoint can reject write-unlisted keys.)

**When two published templates of the same type exist** (e.g., two "header" Elementor templates), one with empty conditions and one with `include/general`, Elementor may render NEITHER. The empty-conditions template corrupts the selection logic. **Trash or unpublish the duplicate**:
```bash
curl -s -X POST "https://site.com/wp-json/wp/v2/elementor_library/{DUPLICATE_ID}" \
  -H "Authorization=[REDACTED] $B64" -H "Content-Type: application/json" \
  -d '{"status":"trash"}'
```

## Elementor post content widget — `<style>` tag behavior

When using Elementor's `theme-post-content` widget to render a regular post (not a template), `<style>` tags already present in the post's `content.rendered` field **do render correctly**. The widget calls `the_content()` which outputs the rendered content including any `<style>` blocks that survived initial save.

However, **injecting new `<style>` tags via `wp/v2/posts/{ID}` REST API updates strips them** — WordPress sanitization (`wp_kses_post`) removes them during the save. The POST returns 200 and updates content length, but the style block appears as **visible plain-text CSS** on the front end. This is because `wp_kses_post` filters out `<style>` elements from post content during REST saves, while tags saved through the Block Editor (with `unfiltered_html` capability) or pre-existing tags persist.

### What actually works for this widget

| Injection method | Result |
|---|---|
| Tags saved via Block Editor | ✅ Survive |
| Tags injected via `wp/v2/posts` REST API | ❌ Stripped → visible text |
| Elementor Snippets `elementor_head` | ❌ `<style>` stripped → visible text |
| Theme `style.css` / `functions.php` | ✅ Guaranteed |
| Inline PHP `wp_head` action (functions.php) | ✅ Guaranteed |

### Elementor Snippet `<style>` rendering pitfall

When using `elementor_snippet` with `_elementor_location: elementor_head`:

```bash
# Meta structure that fails:
curl -s -X POST "https://site.com/wp-json/wp/v2/elementor_snippet" \
  -H "Authorization=[REDACTED] $B64" -H "Content-Type: application/json" \
  -d '{
    "title": "CSS Fix",
    "status": "publish",
    "meta": {
      "_elementor_code": "<style>.class{color:red}</style>",
      "_elementor_location": "elementor_head",
      "_elementor_priority": 1
    }
  }'
```

The snippet creates successfully (HTTP 201), and the `_elementor_code` stores the full `<style>` block. But Elementor's `wp_head` output hook passes the code through `the_content` filter, which **strips `<style>` tags** and emits the CSS as visible text at the very top of `<body>` — before the `<header>` element. The CSS rules appear as raw text paragraphs, breaking the page layout.

**Workaround:** Wrap CSS in a JavaScript IIFE that creates a `<style>` element:

```javascript
(function(){
  var s = document.createElement('style');
  s.id = 'my-fix';
  s.textContent = '.class { color:red !important; }';
  document.head.appendChild(s);
})();
```

Even this may fail — the JS string itself can appear as visible text if PhastPress or another processor strips inline scripts. **Do not rely on elementor_snippet for critical CSS.** Use theme file editing or page content editing instead.

### 🚫 CACHING MASKS CONDITION CHANGES

Even after conditions are corrected, **PhastPress caches the page WITHOUT the header**. The header may exist in raw HTML (`?phast=-phast` shows it) but the cached version doesn't include it. Use a cache-busting query param (`?v=$(date +%s)`) or bypass PhastPress when verifying. Cloudflare also caches — flush if you have API access.

### 🚫 HOMEPAGE-ONLY HEADER HIDE VIA PAGE CONTENT CSS

To hide the Elementor header **only on the homepage** (without modifying Elementor conditions globally), inject CSS into the homepage page's raw HTML content:

```python
# Add to homepage page content's <style> block (inside <!-- wp:html -->)
css_rule = 'header.elementor-location-header{display:none!important}'

# Find the last </style> tag and insert before it
idx = content.rfind('</style>')
content = content[:idx] + css_rule + '\n' + content[idx:]
```

This works because the homepage's page content `<!-- wp:html -->` block is only rendered when viewing that specific page. Other pages (posts, archives, custom post types) do NOT load the homepage CSS, so the header remains visible there. No global conditions need changing.

## ⚠️ Regular post content editing: `<style>` tag stripping

When updating a **regular WordPress post** (not an Elementor template/library item) via `wp/v2/posts/{ID}`, any `<style>` tags in the `content` field are **stripped by WordPress sanitization** (`wp_kses_post()`). The POST returns `200 OK` and updates the content length, but style blocks do NOT render on the frontend — they appear as visible plain-text CSS rules.

**This applies even when the post is rendered through Elementor's `theme-post-content` widget.** Elementor calls `the_content()` which runs through WordPress content filters that strip `<style>`.

### What works instead

| Method | Reliable? | Notes |
|--------|-----------|-------|
| Update `_elementor_data` meta JSON | ✅ | Full Elementor content stored here, not post_content |
| Elementor snippets (`elementor_snippet`) | ⚠️ | Partial — conditions often don't stick (see pitfalls above) |
| Theme `style.css` via SSH/panel | ✅ | Guaranteed to render, best for CSS fixes |
| WPCode snippets via REST | ✅ | If WPCode plugin is installed and snippet type is CSS |
| Post content `<style>` tag | ❌ | Stripped by WordPress sanitization |

### Identify post ID for Elementor-driven regular posts

When you see a page URL like `https://site.com/running/hoka-speedgoat-7/` and need its WordPress post ID:

```bash
# Find by slug — works even when the Elementor template ID differs
curl -s "https://site.com/wp-json/wp/v2/posts?slug=hoka-speedgoat-7" \
  -H "Authorization=[REDACTED] $B64" \
  | python3 -c "import sys,json; d=json.load(sys.stdin); print(f'ID: {d[0][\"id\"]}')"
```

The ID returned here is the **post ID** (e.g., 88020), NOT the Elementor template ID (e.g., 72108). The post holds `_elementor_data` meta; the template defines how it's displayed.

### How to verify a page is Elementor-driven

In the browser console or from page source:

```js
// If these exist, the page content comes from Elementor's _elementor_data
document.querySelector('.elementor-location-single');
document.querySelector('.elementor-widget-theme-post-content');
```

### Fallback: SSH / hosting panel

When REST API methods fail (style tags stripped, snippets don't inject, conditions corrupt), inject CSS directly into the file system:

```bash
# Locate the active child theme directory
# Common paths:
#   /var/www/wp-content/themes/twentyten-child/style.css
#   /home/user/public_html/wp-content/themes/twentyten-child/style.css

# Append CSS to the child theme style.css
echo "/* Fix: post content responsive layout */" >> style.css
```

This bypasses all WordPress sanitization and caching layers. Always append to the **child theme**, never the parent — parent updates overwrite changes.

## Get Elementor template raw JSON widget tree

Each template stores its full Elementor editor content as JSON in `_elementor_data` meta.

```bash
curl -s "https://site.com/wp-json/wp/v2/elementor_library/{ID}?context=edit" \
  -H "Authorization=[REDACTED] $B64" | python3 -c "
import json,sys
d=json.load(sys.stdin)
data = json.loads(d['meta']['_elementor_data'])
print(json.dumps(data, indent=2)[:3000])
"
```

Use this to inspect widget settings (background colors, padding, image URLs) without loading the Elementor editor UI.
