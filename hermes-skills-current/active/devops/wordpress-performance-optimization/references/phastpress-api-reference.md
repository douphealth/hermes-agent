# PhastPress API / Settings Reference

## AJAX Save Endpoint

**URL:** `/wp-admin/admin-ajax.php?action=phastpress_ajax_dispatch`
**Method:** POST  
**Auth:** Requires valid wp-admin session cookie + `_wpnonce`

The nonce is found in the settings page HTML:
```bash
grep -oP '"nonce":"\K[a-f0-9]+' /tmp/phast_settings.html | head -1
```

### Complete Settings Payload

```bash
curl -s -b /tmp/wp_cookies.txt \
  -X POST "https://site.com/wp-admin/admin-ajax.php?action=phastpress_ajax_dispatch" \
  --data-urlencode "_wpnonce=$NONCE" \
  --data-urlencode "phast-plugins-action=save-settings" \
  --data-urlencode "phastpress-enabled=on" \
  --data-urlencode "phastpress-admin-only=off" \
  --data-urlencode "phastpress-pathinfo-query-format=on" \
  --data-urlencode "phastpress-footer-link=off" \
  --data-urlencode "phastpress-compress-service-response=on" \
  --data-urlencode "phastpress-img-optimization-tags=on" \
  --data-urlencode "phastpress-img-optimization-css=on" \
  --data-urlencode "phastpress-img-optimization-api=on" \
  --data-urlencode "phastpress-img-lazy=on" \
  --data-urlencode "phastpress-css-optimization=on" \
  --data-urlencode "phastpress-scripts-rearrangement=on" \
  --data-urlencode "phastpress-scripts-defer=on" \
  --data-urlencode "phastpress-scripts-proxy=on" \
  --data-urlencode "phastpress-iframe-defer=on" \
  --data-urlencode "phastpress-minify-html=on" \
  --data-urlencode "phastpress-minify-inline-scripts=on"
```

### Response (success)
```json
{"phast-success":true,"phast-data":{"config":{...},"nonce":"new_nonce","nonceName":"_wpnonce"}}
```

### Key Config Keys

| POST Field | Default | Description |
|---|---|---|
| `phastpress-enabled` | off | Master toggle |
| `phastpress-img-lazy` | off | Loading=lazy on all images |
| `phastpress-scripts-defer` | on | Async load scripts |
| `phastpress-css-optimization` | on | Inline critical CSS |
| `phastpress-minify-html` | on | Strip whitespace |
| `phastpress-scripts-rearrangement` | off | Move scripts to optimal position |
| `phastpress-iframe-defer` | on | Lazy-load iframes |
| `phastpress-img-optimization-api` | on | Use Phast CDN for images |

## Plugin Slug Reference (for REST API)

Common plugin slugs for `/wp/v2/plugins/{slug}`:

| Plugin Name | Slug (API) |
|---|---|
| Code Snippets | `code-snippets/code-snippets` |
| WPCode Lite | `insert-headers-and-footers/ihaf` |
| PhastPress | `phastpress/phastpress` |
| ShortPixel | `shortpixel-image-optimiser/wp-shortpixel` |
| Seraphinite | `seraphinite-accelerator-ext/plugin_root` |
| LiteSpeed Cache | `litespeed-cache_old/litespeed-cache` |

## PhastPress Python/Script Extraction

The PhastPress config is embedded in the Vue.js app init data on the settings page:

```python
import re, json
with open('/tmp/phast_settings.html') as f:
    html = f.read()
# Extract the config object from window.PHAST_PLUGINS_SDK_ADMIN_PANEL call
match = re.search(r'"config":(\{[^}]+\})', html)
config = json.loads(match.group(1))
```
