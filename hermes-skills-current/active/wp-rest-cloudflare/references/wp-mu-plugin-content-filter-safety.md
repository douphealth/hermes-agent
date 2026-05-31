# WordPress MU-plugin content filter safety

Use this when adding cleanup, affiliate-link hardening, shortcode removal, schema injection, or other `the_content` filters through an MU-plugin.

## Failure mode observed

A broad `preg_replace_callback()` filter over a very large custom homepage/classic HTML page can fail due to PCRE backtracking/limits and return `null` or empty output. If the filter returns that value directly, the public page can render as a blank content area even though WordPress still returns HTTP 200.

This is especially likely on pages that contain:
- large self-contained HTML/CSS templates in `<!-- wp:html -->` blocks
- many links/attributes
- huge inline `<style>` blocks
- homepage/front-page landing templates

## Emergency symptom: post bodies collapse sitewide

If many WordPress posts suddenly render only header/title/byline metadata while HTTP status remains 200 and the HTML payload is still large, suspect a runtime `the_content` filter before assuming database content loss. Immediate recovery pattern:

1. Disable the broad `the_content` filter block in the MU/plugin file; keep redirect/noindex/sitemap logic if separable.
2. Purge Cloudflare (`purge_everything` if exact-file purge might miss the cache key).
3. Verify at least three representative posts with cache-busted requests: status 200, visible word count restored, expected article sections such as Quick Answer/FAQ/body text present.
4. Browser-spot-check one affected URL to confirm rendered content, not just raw HTML.
5. Do not re-enable sitewide regex affiliate rel hardening. Replace it with offline batch edits or a DOM-safe targeted pass.

## Safer pattern

```php
add_filter('the_content', function ($content) {
    if (is_admin() || empty($content) || is_front_page()) {
        return $content;
    }

    $updated = preg_replace_callback('/.../i', function ($m) {
        // transform narrow matches only
        return $m[0];
    }, $content);

    return is_string($updated) ? $updated : $content;
}, 20);
```

## Rules

1. Do not run broad regex cleanup over the homepage/front page unless the task is explicitly homepage content repair.
2. Always store regex output in `$updated`; never return `preg_replace*()` directly.
3. Always fallback to original content if regex output is not a string.
4. Scope filters by path/post type/ID when possible.
5. After deploying any `the_content` filter, verify real public rendered output, not just HTTP 200:
   - HTML byte length
   - visible word count after stripping scripts/styles/tags
   - expected hero/H1/snippet present
   - cache-busted URL and normal URL after Cloudflare purge

## Verification snippet

```python
import re, requests
url = 'https://example.com/?verify-content-filter=1'
r = requests.get(url, timeout=25, headers={'User-Agent':'Mozilla/5.0'})
body = re.search(r'<body[^>]*>(.*)</body>', r.text, re.S|re.I)
visible = re.sub(r'(?is)<(script|style|noscript)[^>]*>.*?</\\1>', ' ', body.group(1) if body else r.text)
visible = re.sub(r'<[^>]+>', ' ', visible)
visible = re.sub(r'\\s+', ' ', visible).strip()
print(r.status_code, len(r.text), len(visible.split()), visible[:300])
```

If the user reports a blank homepage after an MU-plugin/content-filter deployment, immediately disable or narrow the content filter, purge Cloudflare, and verify visible words/hero text before explaining.