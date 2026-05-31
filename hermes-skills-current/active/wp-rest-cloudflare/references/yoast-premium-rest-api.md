# Yoast SEO Premium REST API Patterns

## Overview
Yoast Premium exposes limited but critical REST endpoints. Standard WP REST API meta fields (`_yoast_wpseo_title`, `_yoast_wpseo_metadesc`) do **NOT** persist via `POST /wp/v2/posts/{id}` — Yoast does not register these meta keys with the REST API. Workarounds documented below.

## Endpoints

### Base: `/wp-json/yoast/v1/`

### Redirects Management

**List all redirects:**
```bash
curl -sS "https://example.com/wp-json/yoast/v1/redirects/list" \
  -H "Authorization=[REDACTED] $B64"
```
Returns `{"success":true,"redirects":[{"origin":"...","target":"...","type":301,"format":"plain"},...]}`

**Delete a redirect:**
```bash
curl -sS -X POST "https://example.com/wp-json/yoast/v1/redirects/delete" \
  -H "Authorization=[REDACTED] $B64" \
  -H "Content-Type: application/json" \
  -d '{"origin":"health/best-supplements-2025"}'
```
Origin must be the raw path (no leading/trailing slash). Returns `{"title":"Redirect deleted.","message":"The redirect was deleted successfully.","success":true}`.

**Identify Yoast redirects via HTTP headers:**
Yoast redirects emit `x-redirect-by: Yoast SEO Premium` — use this to differentiate from server-level (.htaccess/nginx) or Cloudflare redirects.
```bash
curl -sS -I "https://example.com/some-url/" | grep -i 'x-redirect-by'
```

### Get Head (inspect rendered SEO metadata)
```bash
curl -sS "https://example.com/wp-json/yoast/v1/get_head?url=https://example.com/some-page/" \
  -H "Authorization=[REDACTED] $B64"
```
Returns JSON with `title`, `description`, `robots`, `canonical`, `schema` etc. Use the actual public URL as the `url` query parameter, not the REST API URL.

### Working with Redirect Loops

A redirect loop manifests as:
1. URL A → 301 (Yoast) → URL B → 301 (Yoast) → URL A
2. Both hops emit `x-redirect-by: Yoast SEO Premium`
3. List all redirects, search for both origin paths, delete the offending entry

**Complete loop resolution pattern:**
```bash
# 1. Identify the loop via headers
curl -sS -I "https://example.com/path-a/" | grep -i 'location\|x-redirect-by'
curl -sS -I "https://example.com/path-b/" | grep -i 'location\|x-redirect-by'

# 2. List all redirects
curl -sS "https://example.com/wp-json/yoast/v1/redirects/list" \
  -H "Authorization=[REDACTED] $B64" | python3 -c "
import json,sys
d=json.load(sys.stdin)
for r in d.get('redirects',[]):
    if 'best-supplements' in r.get('origin','')+r.get('target',''):
        print(f\"{r['origin']} -> {r['target']}\")
"

# 3. Delete one side of the loop
curl -sS -X POST "https://example.com/wp-json/yoast/v1/redirects/delete" \
  -H "Authorization=[REDACTED] $B64" \
  -H "Content-Type: application/json" \
  -d '{"origin":"health/path-a"}'

# 4. Verify loop is broken
curl -sS -o /dev/null -w "HTTP %{http_code}" "https://example.com/path-a/" -L --max-redirs 3
```

## Updating Yoast SEO Meta (Title, Description)

### Problem
Standard WP REST API doesn't persist `_yoast_wpseo_title` or `_yoast_wpseo_metadesc` meta. The REST object's `meta` field typically only exposes non-Yoast keys (e.g. `footnotes`).

### Solution: Code Snippets PHP Override

Use the Code Snippets REST API (`/wp-json/code-snippets/v1/snippets`) to create a global PHP snippet that overrides Yoast output via filters:

```php
<?php
/**
 * Bulk override Yoast SEO titles and descriptions for specific posts.
 * Runs on every page load. Deactivate or delete after verified.
 */
add_filter('wpseo_title', function($title) {
    // Map of post IDs → new titles
    $overrides = [
        12345 => 'Custom SEO Title for Post 12345 | Site Name',
        67890 => 'Custom SEO Title for Post 67890 | Site Name',
    ];
    if (is_singular() && isset($overrides[get_queried_object_id()])) {
        return $overrides[get_queried_object_id()];
    }
    return $title;
}, 999);

add_filter('wpseo_metadesc', function($desc) {
    $overrides = [
        12345 => 'Custom meta description for post 12345...',
        67890 => 'Custom meta description for post 67890...',
    ];
    if (is_singular() && isset($overrides[get_queried_object_id()])) {
        return $overrides[get_queried_object_id()];
    }
    return $desc;
}, 999);

// Also override Open Graph and Twitter when needed
add_filter('wpseo_opengraph_title', function($title) {
    // same logic
    return $title;
}, 999);
```

**Code Snippets REST create pattern:**
```python
import json, base64, http.client

conn = http.client.HTTPSConnection("example.com")
auth = base64.b64encode(b"username:app_password").decode()
payload = {
    "name": "Yoast Title Override (Bulk)",
    "code": "<?php\n// PHP code as above\n",
    "code_type": null,  # null = php for Code Snippets 3.x
    "scope": "global",  # runs on ALL page loads
    "active": True
}
conn.request("POST", "/wp-json/code-snippets/v1/snippets",
    json.dumps(payload),
    {"Authorization": f"Basic {auth}", "Content-Type": "application/json"})
```

**Key Code Snippets REST details:**
- `code_type`: must be `null` (not `"php"`) for PHP snippets in Code Snippets 3.x
- `scope`: `"global"` runs on every page load; `"admin"` only runs in wp-admin
- Always add ABSPATH guard: `if (!defined('ABSPATH')) { exit; }`
- After creation, trigger a front-end page request to execute the snippet
- Verify by visiting the public page URL and checking `<title>` tag
- Delete the snippet after verification succeeds

### Alternative: `meta_input` (works occasionally, not reliable)
```bash
curl -sS -X POST "https://example.com/wp-json/wp/v2/posts/{id}" \
  -H "Authorization=[REDACTED] $B64" \
  -H "Content-Type: application/json" \
  -d '{"meta_input":{"_yoast_wpseo_title":"New Title","_yoast_wpseo_metadesc":"New desc"}}'
```
This may work on some sites where Yoast has registered meta in REST, but fails silently on most. Verify by re-reading the object and checking public `<title>`.

## Slug Changes via REST API

Changing a post slug:
```bash
curl -sS -X POST "https://example.com/wp-json/wp/v2/posts/{id}" \
  -H "Authorization=[REDACTED] $B64" \
  -H "Content-Type: application/json" \
  -d '{"slug":"new-slug"}'
```

**Caveat:** The `link` field in the response may still show the old canonical URL if Yoast Premium has set a canonical override. The slug _did_ change (confirmed by `slug` field), but the public URL may redirect. Check both:
- New slug URL (may 301 back to old canonical via Yoast)
- Old slug URL (may 301 to new slug)

If Yoast's canonical URL is stale, the only reliable fix is to delete the offending Yoast redirect (see above) or use a Code Snippets filter.

## Canonical URL Override Detection

If a post slug changes via REST but the public `link` in WP REST response still shows the old URL, Yoast has stored a canonical override. Symptoms:
- `GET /wp/v2/posts/{id}` returns `slug: "new-slug"` but `link: "https://example.com/old-slug/"`
- Visiting `/new-slug/` 301s to `/old-slug/` with `x-redirect-by: Yoast SEO Premium`

Fix: Delete the Yoast redirect (see Redirects Management above).
