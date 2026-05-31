# CSS Injection Methods for Elementor WordPress Sites (Ranked)

When you need to inject CSS but various methods fail, use this priority-ordered table.

## Method Comparison

| Method | Reliability | Requires | Best For |
|--------|-------------|----------|----------|
| Theme `style.css` (child) | ✅ MAX | File writable + SSH/panel | Long-term, site-wide CSS fixes |
| WPCode CSS snippet | ✅ HIGH | WPCode plugin installed | When theme file not writable |
| Elementor → Custom CSS (per page) | ⚠️ MEDIUM | Elementor Pro + page edit access | Single-page CSS overrides |
| Post content raw `<style>` tag | ❌ FAILS | N/A | WordPress sanitization strips `<style>` |
| REST API `wp/v2/settings` with `custom_css` | ❌ FAILS | N/A | `custom_css` not exposed via REST settings endpoint |
| Elementor snippet (`elementor_snippet`) | ⚠️ LOW | Elementor Pro | Conditions often don't stick via REST |

## Key Facts

### 1. `<style>` tags in post content are STRIPPED

When updating `wp/v2/posts/{ID}` via REST API, WordPress applies `wp_kses_post()` which strips `<style>` tags. The POST returns `200 OK` and content length appears to increase, but on the frontend the CSS rules appear as visible plain text paragraphs.

**This applies even when the post is rendered through Elementor's `theme-post-content` widget.** Elementor calls `the_content()` which runs through the same sanitization.

### 2. `custom_css` is NOT in `wp/v2/settings`

Despite being a WordPress core feature, the `custom_css` field (from Customizer → Additional CSS) is NOT exposed through the REST API settings endpoint. A `PUT /wp/v2/settings` with `{"custom_css": "..."}` silently ignores the field.

To check:
```bash
curl -s -u "user:app_password" "https://site.com/wp-json/wp/v2/settings" \
  | python3 -c "import sys,json; d=json.load(sys.stdin); print('\n'.join(sorted(d.keys())))"
# custom_css will NOT be in the output
```

### 3. Theme file editor returns 200 but doesn't save when file isn't writable

The WordPress Theme File Editor form submission returns HTTP 200 even when the file save FAILS. The `file_not_writable` error is hidden in a JavaScript template string (`<# } else if ( 'file_not_writable' === data.code ) { #>`) — NOT in a visible error banner.

**Always verify by re-reading the file after save:**
```bash
curl -s -b /tmp/wp_cookies.txt -H "Host: site.com" \
  "https://ORIGIN_IP/wp-admin/theme-editor.php?file=style.css&theme=CHILD-THEME" \
  | python3 -c "
import re,sys
html = sys.stdin.read()
m = re.search(r'name=\"newcontent\"[^>]*>(.*?)</textarea>', html, re.DOTALL)
if m:
    content = m.group(1).replace('&lt;','<').replace('&gt;','>')
    print(f'Length: {len(content)}')
    print('Has new CSS:', 'POST LAYOUT FIX' in content)
"
```

### 4. WPCode CSS snippets work without file writes

If WPCode (Code Snippets) is installed, create a CSS snippet:

```bash
# This goes through the WPCode admin UI
# WPCode stores snippets in custom DB tables
# CSS snippets are output in <head> via wp_head hook
```

But editing WPCode via REST/cURL is dangerous — see `references/wpcode-safe-editing.md` for encoding corruption issues.

### 5. Elementor page-specific CSS

If Elementor Pro is installed, per-page custom CSS is stored in `_elementor_page_settings` meta. This may work via:

```bash
curl -s -X POST "https://site.com/wp-json/wp/v2/posts/{POST_ID}" \
  -u "user:app_password" \
  -H "Content-Type: application/json" \
  -d '{"meta":{"_elementor_page_settings":{"custom_css":".gutf-article{max-width:100%!important}"}}}'
```

However, this meta key may be silently rejected by the REST API. Verify by re-reading the post after update.

## Fallback Chain

When you need to inject CSS and the primary method fails:

1. **Try WPCode CSS snippet** (database-backed, no file permissions needed)
2. **Try Elementor per-page custom CSS** (if Elementor Pro)
3. **Try editing theme style.css via SSH** (if credentials available)
4. **Try hosting panel file manager** (HestiaCP, cPanel, etc.)
5. **Try uploading a CSS file to wp-content/uploads/ and enqueuing via WPCode PHP snippet**
