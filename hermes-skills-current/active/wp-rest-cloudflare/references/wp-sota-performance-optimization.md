# WordPress SOTA Performance Optimization Pipeline

## Target: Sub-100ms TTFB from Cloudflare edge, sub-500ms fully loaded

## Three-Layer Stack
```
Browser → Cloudflare Edge (Auto Minify, Brotli, Polish, Early Hints)
        → LiteSpeed Server Cache (full-page, 7-day TTL at origin)
        → WordPress/PHP (only on cache MISS)
```

## Phase 1: Cloudflare Edge (via API — needs Zone Settings:Edit permission)

### 1.1 Get Zone ID
```bash
ZONE_ID=$(curl -sS "https://api.cloudflare.com/client/v4/zones?name=domain.com" \
  -H "Authorization=[REDACTED] $TOKEN" | python3 -c "import sys,json;print(json.load(sys.stdin)['result'][0]['id'])")
```

### 1.2 Enable All Speed Settings via PATCH
```bash
# Auto Minify (HTML/CSS/JS)
curl -sS -X PATCH "https://api.cloudflare.com/client/v4/zones/$ZONE_ID/settings/minify" \
  -H "Authorization=[REDACTED] $TOKEN" -H "Content-Type: application/json" \
  --data-binary '{"value":{"html":"on","css":"on","js":"on"}}'

# Brotli
curl -sS -X PATCH "https://api.cloudflare.com/client/v4/zones/$ZONE_ID/settings/brotli" \
  -H "Authorization=[REDACTED] $TOKEN" -H "Content-Type: application/json" \
  --data-binary '{"value":"on"}'

# Early Hints
curl -sS -X PATCH "https://api.cloudflare.com/client/v4/zones/$ZONE_ID/settings/early_hints" \
  -H "Authorization=[REDACTED] $TOKEN" -H "Content-Type: application/json" \
  --data-binary '{"value":"on"}'

# Polish (lossless image compression)
curl -sS -X PATCH "https://api.cloudflare.com/client/v4/zones/$ZONE_ID/settings/polish" \
  -H "Authorization=[REDACTED] $TOKEN" -H "Content-Type: application/json" \
  --data-binary '{"value":"lossless"}'

# Rocket Loader (defer JS — test first, can break sites)
curl -sS -X PATCH "https://api.cloudflare.com/client/v4/zones/$ZONE_ID/settings/rocket_loader" \
  -H "Authorization=[REDACTED] $TOKEN" -H "Content-Type: application/json" \
  --data-binary '{"value":"on"}'  # or "off" if it breaks JS
```

### 1.3 Create Cache Rule (cache HTML at edge, exclude admin)
```bash
# First create the ruleset if none exists
RULESET_ID=$(curl -sS "https://api.cloudflare.com/client/v4/zones/$ZONE_ID/rulesets" \
  -H "Authorization=[REDACTED] $TOKEN" | python3 -c "
import sys,json
d=json.load(sys.stdin.read())
for r in d.get('result',[]):
    if r.get('phase') == 'http_request_cache_settings':
        print(r['id'])
")

if [ -z "$RULESET_ID" ]; then
  RULESET_ID=$(curl -sS -X POST "https://api.cloudflare.com/client/v4/zones/$ZONE_ID/rulesets" \
    -H "Authorization=[REDACTED] $TOKEN" -H "Content-Type: application/json" \
    --data-binary '{
      "name": "Default Cache Rules",
      "kind": "zone",
      "phase": "http_request_cache_settings",
      "rules": []
    }' | python3 -c "import sys,json;print(json.load(sys.stdin)['result']['id'])")
fi

# Add the cache rule (excludes admin/api paths)
curl -sS -X POST "https://api.cloudflare.com/client/v4/zones/$ZONE_ID/rulesets/$RULESET_ID/rules" \
  -H "Authorization=[REDACTED] $TOKEN" -H "Content-Type: application/json" \
  --data-binary '{
    "action": "set_cache_settings",
    "action_parameters": {
      "cache": true,
      "edge_ttl": {"mode": "override_origin", "default": 86400},
      "browser_ttl": {"mode": "override_origin", "default": 14400}
    },
    "expression": "(not starts_with(http.request.uri.path, \"/wp-admin\")) and (not starts_with(http.request.uri.path, \"/wp-json\")) and (not starts_with(http.request.uri.path, \"/wp-login\"))",
    "description": "Cache public pages 24h - exclude admin/api"
  }'
```

### 1.4 Purge Cache
```bash
curl -sS -X POST "https://api.cloudflare.com/client/v4/zones/$ZONE_ID/purge_cache" \
  -H "Authorization=[REDACTED] $TOKEN" -H "Content-Type: application/json" \
  --data-binary '{"purge_everything":true}'
```

## Phase 2: WordPress Plugins (via REST API)

### 2.1 Install LiteSpeed Cache plugin
```bash
curl -sS -X POST "https://domain.com/wp-json/wp/v2/plugins" \
  -H "Authorization=[REDACTED] $B64" -H "Content-Type: application/json" \
  -H "User-Agent: Mozilla/5.0 (X11; Linux x86_64)" \
  --data-binary '{"slug": "litespeed-cache", "status": "active"}'
```

**CRITICAL: LiteSpeed Cache plugin vs Seraphinite Accelerator conflict**
- LiteSpeed Cache (plugin) handles full-page caching at WordPress level
- Seraphinite Accelerator handles CSS/JS minification + combine + lazy load
- **They conflict on CSS/JS optimization** — running both causes issues
- **Optimal setup:** Keep LiteSpeed Cache PLUGIN inactive, keep Seraphinite ACTIVE
- The server-level LiteSpeed cache (built into LiteSpeed web server) works WITHOUT the plugin
- Seraphinite handles CSS/JS optimization; server-level LiteSpeed handles full-page caching
- **To verify:** check that `x-litespeed-cache: hit` appears in headers (server cache works)

### 2.2 Deactivate conflicting plugins
```bash
# Deactivate LiteSpeed Cache (keep server-level caching)
curl -sS -X POST "https://domain.com/wp-json/wp/v2/plugins/litespeed-cache/litespeed-cache" \
  -H "Authorization=[REDACTED] $B64" -H "Content-Type: application/json" \
  -H "X-HTTP-Method-Override: PUT" --data-binary '{"status":"inactive"}'

# Reactivate Seraphinite 
curl -sS -X POST "https://domain.com/wp-json/wp/v2/plugins/seraphinite-accelerator-ext/plugin_root" \
  -H "Authorization=[REDACTED] $B64" -H "Content-Type: application/json" \
  -H "X-HTTP-Method-Override: PUT" --data-binary '{"status":"active"}'
```

## Phase 3: Code Snippets Bloat Removal

Create a single global Code Snippets snippet with:

### 3.1 Head Bloat Removal (safe, reversible)
```php
// Remove emoji scripts
remove_action('wp_head', 'print_emoji_detection_script', 7);
remove_action('wp_print_styles', 'print_emoji_styles');
remove_action('admin_print_scripts', 'print_emoji_detection_script');
remove_action('admin_print_styles', 'print_emoji_styles');

// Remove embed script
remove_action('wp_head', 'wp_oembed_add_discovery_links');
remove_action('wp_head', 'wp_oembed_add_host_js');
add_filter('embed_oembed_discover', '__return_false');

// Remove legacy WP tags
remove_action('wp_head', 'wlwmanifest_link');
remove_action('wp_head', 'rsd_link');
remove_action('wp_head', 'wp_shortlink_wp_head');
remove_action('wp_head', 'rest_output_link_wp_head');
remove_action('wp_head', 'wp_generator');
remove_action('wp_head', 'index_rel_link');
remove_action('wp_head', 'parent_post_rel_link', 10);
remove_action('wp_head', 'start_post_rel_link', 10);
remove_action('wp_head', 'adjacent_posts_rel_link', 10);
remove_action('wp_head', 'adjacent_posts_rel_link_wp_head', 10);
add_filter('the_generator', '__return_empty_string');
```

### 3.2 Disable Self-Pingbacks
```php
add_action('pre_ping', function(&$links) {
    foreach ($links as $l => $link) {
        if (strpos($link, home_url()) !== false) unset($links[$l]);
    }
});
```

### 3.3 Remove jQuery Migrate
```php
add_action('wp_default_scripts', function($scripts) {
    if (!is_admin() && isset($scripts->registered['jquery'])) {
        $scripts->registered['jquery']->deps = array_diff(
            $scripts->registered['jquery']->deps, ['jquery-migrate']
        );
    }
});
```

### 3.4 Force font-display: swap
```php
add_action('wp_head', function() { ?>
<style>@font-face{font-display:swap}img{aspect-ratio:auto}</style>
<link rel="preconnect" href="https://cdn.jsdelivr.net">
<link rel="dns-prefetch" href="//cdn.jsdelivr.net">
<link rel="dns-prefetch" href="//www.googletagmanager.com">
<?php }, 0);
```

### 3.5 Remove query strings from static assets
```php
add_filter('script_loader_src', function($src) {
    return strpos($src, '?ver=') !== false ? remove_query_arg('ver', $src) : $src;
});
add_filter('style_loader_src', function($src) {
    return strpos($src, '?ver=') !== false ? remove_query_arg('ver', $src) : $src;
});
});

### 3.7 Defer non-critical JS -- NEVER defer jquery-core
```php
add_filter('script_loader_tag', function($tag, $handle) {
    // SAFE: only scripts without jQuery dependency
    $safe_to_defer = ['wp-embed', 'cookie-law-info', 'nytsys.min', 'rpt_front_style'];
    foreach ($safe_to_defer as $d) {
        if (strpos($handle, $d) !== false) return str_replace(' src', ' defer src', $tag);
    }
    return $tag;
}, 10, 2);
```
**CRITICAL:** Never add jquery-core, jquery, generate-menu, generate-dropdown, or any theme/plugin script with jQuery dependency to the defer list. Deferring jQuery breaks all jQuery-dependent functionality -- menus, sliders, interactive forms.

### 3.8 Preload LCP image for homepage
```php
add_action('wp_head', function() {
    if (is_front_page()) {
        echo '<link rel="preload" as="image" href="/wp-content/uploads/hero.webp" fetchpriority="high">';
    }
}, 1);
```
```php
add_filter('wp_content_img_tag', function($html) {
    return strpos($html, 'loading=') === false 
        ? str_replace('<img ', '<img loading="lazy" ', $html) : $html;
});
```

## Phase 4: Verification

### 4.1 Performance Metrics
```bash
# First request (may be cache MISS)
curl -sI "https://domain.com/" -w "TTFB: %{time_starttransfer}s\nTotal: %{time_total}s\n" -o /dev/null
# Second request (should be cache HIT)
curl -sI "https://domain.com/" | grep -iE 'x-litespeed-cache:|cf-cache-status:'
```

Expected results after full optimization:
- TTFB first request (origin): 0.2–0.5s
- TTFB repeat (CF edge HIT): 0.05–0.1s  
- `x-litespeed-cache: hit` (origin server cache working)
- `cf-cache-status: HIT` (Cloudflare edge cache working)
- `cache-control` with `max-age=14400` or higher

### 4.2 Bloat Check
```bash
echo "Has emoji: $(curl -sL 'https://domain.com/' | grep -c 'emoji')"  # expect 0
echo "Has wlwmanifest: $(curl -sL 'https://domain.com/' | grep -c 'wlwmanifest')" # expect 0
echo "Has shortlink: $(curl -sL 'https://domain.com/' | grep -c 'shortlink')" # expect 0  
echo "Has preconnect: $(curl -sL 'https://domain.com/' | grep -c 'preconnect')" # expect >0
```

### 4.3 Site Health Check
```bash
for url in "/" "/wp-json/" "/sitemap_index.xml" "/some-post-slug/"; do
  echo "$(curl -sI "https://domain.com$url" | grep -E 'HTTP/' | awk '{print $2}') — $url"
done  # All should return 200
```

## Phase 5: Lighthouse Performance Score Boosting (Sub-0.1s TTFB Is Not Enough)

Lighthouse score is driven by **6 key metrics**, not just TTFB:
- **LCP** (Largest Contentful Paint) — hero image/text rendering speed
- **FID / TBT** (First Input Delay / Total Blocking Time) — JavaScript execution
- **CLS** (Cumulative Layout Shift) — visual stability
- **Speed Index** — above-fold content visibility
- **SI** (Speed Index) — how fast content visually populates
- **TBT** (Total Blocking Time) — main thread work from JS

A sub-100ms TTFB can still yield a **60 mobile score** if these factors are poor.

### 5.1 Critical CSS Inline (Eliminate Render-Blocking CSS)
```php
add_action('wp_head', function() { ?>
<style id="critical-fix">
/* Reserve space for cookie consent popup — prevents CLS */
.cky-consent-container,.cky-modal{min-height:300px}
.cky-btn-revisit-wrapper{min-height:45px;min-width:45px}
/* Font-display:swap with local() fallback — prevents invisible text */
@font-face{font-family:Ubuntu;font-style:normal;font-weight:400;font-display:swap;src:local('Ubuntu')}
@font-face{font-family:Ubuntu;font-style:normal;font-weight:700;font-display:swap;src:local('Ubuntu Bold')}
/* Images: prevent CLS from missing dimensions */
img{max-width:100%;height:auto;aspect-ratio:auto}
/* Hero area min-height prevents layout shift */
.home .inside-article{min-height:80vh}
</style>
<?php }, 0);
```

**Why this works for Lighthouse:**
- Cookie consent popup has a reserved `min-height` → no layout shift when it renders
- Font-display:swap with `local()` → uses system font instantly, swaps when web font loads (zero invisible text)
- `aspect-ratio:auto` → browser reserves image space before loading → no CLS
- Hero min-height → above-fold space is stable

### 5.2 Preload Fonts with Local Fallback
```php
add_action('wp_head', function() { ?>
<style>
@font-face{font-family:Ubuntu;font-style:normal;font-weight:400;font-display:swap;src:local('Ubuntu'),url(/cf-fonts/s/ubuntu/5.0.11/latin/400/normal.woff2) format('woff2')}
@font-face{font-family:Ubuntu;font-style:normal;font-weight:700;font-display:swap;src:local('Ubuntu Bold'),url(/cf-fonts/s/ubuntu/5.0.11/latin/700/normal.woff2) format('woff2')}
</style>
<?php }, 0);
```
The `local()` hint tells the browser to check if the font is already installed (saves a network request) before downloading.

### 5.3 Defer Non-Critical JS — NEVER Defer jQuery
```php
add_filter('script_loader_tag', function($tag, $handle) {
    // SAFE: only scripts without jQuery dependency
    $safe_to_defer = ['wp-embed', 'cookie-law-info', 'nytsys.min', 'rpt_front_style'];
    foreach ($safe_to_defer as $d) {
        if (strpos($handle, $d) !== false) return str_replace(' src', ' defer src', $tag);
    }
    return $tag;
}, 10, 2);
```
**CRITICAL PITFALL:** Deferring `jquery-core` or `jquery` breaks ALL jQuery-dependent scripts (menus, sliders, interactive elements, accordions). Only defer scripts that have NO jQuery dependency. This is the most common optimization mistake that breaks production sites.

### 5.4 Make Third-Party Scripts Async (Reduces TBT)
```php
add_filter('script_loader_tag', function($tag, $handle) {
    $async = ['clarity', 'metricool', 'grow'];
    foreach ($async as $d) {
        if (strpos($handle, $d) !== false) return str_replace(' src', ' async src', $tag);
    }
    return $tag;
}, 11, 2);
```

### 5.5 Preload LCP Image
```php
add_action('wp_head', function() {
    if (is_front_page()) {
        echo '<link rel="preload" as="image" href="/wp-content/uploads/hero.webp" fetchpriority="high">';
    }
}, 1);
```

### 5.6 Add Explicit Image Dimensions (Lazy Loading)
```php
add_filter('wp_content_img_tag', function($html) {
    if (strpos($html, 'loading=') === false && strpos($html, 'fetchpriority=') === false) {
        return str_replace('<img ', '<img loading="lazy" ', $html);
    }
    return $html;
});
```

### 5.7 Code Snippets: Batch Deactivation of Non-Essential Snippets
WordPress sites with long optimization histories can accumulate 35+ active Code Snippets, each adding PHP execution overhead. Deactivating batch/one-time snippets improves TBT:

```python
import json
from hermes_tools import terminal

to_disable = [27, 28, 50, 54, 55, 56, 57, 58, 72]  # IDs of one-time/batch snippets
for sid in to_disable:
    payload = json.dumps({"active": False})
    r = terminal(f"""curl -sS -X POST "https://domain.com/wp-json/code-snippets/v1/snippets/{sid}" \
      -H "Authorization=[REDACTED] $B64" -H "Content-Type: application/json" \
      -H "User-Agent: Mozilla/5.0" -H "X-HTTP-Method-Override: PUT" \
      --data-binary '{payload}'""")
```

**Heuristic for which snippets to disable:**
- Snippets with "batch", "one-time", "temp", "purge" in the name
- Snippets that were created as part of a content cleanup campaign that has ended
- Snippets that only run on admin (`is_admin()`) or cron
- Snippets that hook `init` with no conditional check (runs on every request)

## Pitfalls
- **Rocket Loader breaks JS-heavy sites** — disable if you see console errors or blank page sections
- **LiteSpeed Cache plugin ≠ server-level LiteSpeed** — the plugin is optional; server-level caching works independently
- **Seraphinite + LiteSpeed Cache plugin conflict** — don't run both active; Seraphinite for CSS/JS, server LiteSpeed for caching
- **First request after deploy can be slow** — cache must warm. Hit the URL 2-3 times to warm all caches
- **Cloudflare settings need Zone Settings:Edit permission** — `GET` returning 403 doesn't mean `PATCH` will fail; always try the write
- **Cache rule expression escaping** — use double quotes inside single-quoted JSON for string constants
- **Deactivating plugins via REST may return empty/null status** — verify by re-reading the plugin list

### Seraphinite Accelerator: Cache Strips Code Snippets wp_head Output
When Seraphinite Accelerator has cached a page, it strips inline `<style>` and `<link>` tags added via `add_action('wp_head', ...)`. This means:
- `font-display:swap` inline styles **disappear** from cached pages
- `preconnect`/`dns-prefetch` `<link>` tags **disappear** from cached pages
- But bloat removal (`remove_action`) still works because it runs before Seraphinite captures the output

**Detection pattern:** Cache-busted URL (`?nocache=1`) shows the snippet output; plain URL shows 0 matches. Compare:
```bash
# Cache-busted (fresh PHP execution)
curl -sL "https://domain.com/?cb=$(date +%s)" | grep -c 'font-display:swap'  # expect >0
# Plain URL (may be Seraphinite-cached)
curl -sL "https://domain.com/" | grep -c 'font-display:swap'  # expect >0 after fix
```

**Fixes (in order of reliability):**
1. **Use `wp_footer` instead of `wp_head`** — Seraphinite doesn't cache footer output:
   ```php
   add_action('wp_footer', function() {
       echo '<style id="font-fix">@font-face{font-display:swap}</style>';
   }, 1);
   ```
2. **Use `wp_add_inline_style`** — attaches to an enqueued stylesheet, Seraphinite preserves it:
   ```php
   add_action('wp_enqueue_scripts', function() {
       wp_add_inline_style('generate-style', '@font-face{font-family:Ubuntu;font-display:swap}');
   }, 1000);
   ```
3. **Deactivate Seraphinite, rely on LiteSpeed Cache plugin** — LiteSpeed doesn't strip `wp_head` output

### Cloudflare API Token Error Code Diagnosis
When Cloudflare API calls fail, two distinct error codes indicate different problems:
- **Code `9109`**: Token lacks the permission group for this resource. The token exists and is valid, but the user needs to edit the token in Cloudflare Dashboard and add the required permission.
- **Code `10000`**: Authentication error — the token can't authenticate for this scope at all. Usually means the token was created without ANY permission for this resource type.
- **`GET` returning 403 ≠ `PATCH` will fail**: Some tokens have write-only permissions. Always try the write operation directly.

**Minimal permission set for full Cloudflare optimization via API:**
- `Zone → Zone Settings → Edit` (for Auto Minify, Brotli, Polish, Early Hints, Rocket Loader)
- `Zone → Cache Rules → Edit` (for creating edge cache rules)
- `Zone → Page Rules → Edit` (for legacy page rules)
- `Zone → DNS → Edit` (for DNS record management)
- `Zone → Cache Purge → Edit` (for cache invalidation)

### The Two-Cache Problem: Stale Edge Cache After Optimization
WordPress on LiteSpeed + Cloudflare has TWO independent caches that can conspire to serve stale content:
1. **Cloudflare edge cache** (4h–24h TTL via Cache Rule)
2. **LiteSpeed origin server cache** (7-day TTL via server-level caching)

**The stale cycle:** You purge CF → CF asks origin → LiteSpeed returns old cached HTML → CF recaches the stale version.

**Reliable cache-busting protocol:**
1. Deploy all Code Snippets first (they're active immediately, just not visible through cache)
2. Purge **LiteSpeed origin cache** via snippet:
   ```php
   do_action('litespeed_purge_all');
   if (class_exists('LiteSpeed_Cache_API')) { LiteSpeed_Cache_API::purge_all(); }
   ```
3. Hit the site with a unique query string to warm the fresh version:
   ```bash
   curl -sL "https://domain.com/?warm=$(date +%s)" -o /dev/null
   ```
4. Purge Cloudflare edge cache:
   ```bash
   curl -sS -X POST "https://api.cloudflare.com/client/v4/zones/$ZONE_ID/purge_cache" ... --data-binary '{"purge_everything":true}'
   ```
5. Verify with BOTH:
   ```bash
   curl -sL "https://domain.com/" | grep -c 'font-display'  # plain URL
   curl -sL "https://domain.com/?cb=$(date +%s)" | grep -c 'font-display'  # cache-busted
   ```

### Cloudflare Cache Rules: Targeting Static Assets
For optimal caching, create SEPARATE cache rules for static files vs HTML pages. The right expressions:

**Static assets (1 year TTL):**
```
expression: "(ends_with(http.request.uri.path, ".css") or ends_with(http.request.uri.path, ".js") or ends_with(http.request.uri.path, ".woff2") or ends_with(http.request.uri.path, ".webp") or ends_with(http.request.uri.path, ".png") or ends_with(http.request.uri.path, ".jpg"))"
edge_ttl: 31536000
browser_ttl: 31536000
```

**HTML pages (4 hour TTL, exclude admin):**
```
expression: "(not starts_with(http.request.uri.path, "/wp-admin")) and (not starts_with(http.request.uri.path, "/wp-json"))"
edge_ttl: 14400
browser_ttl: 3600
```

**Avoid `"expression": "true"`** — this caches admin pages and API endpoints, causing stale login sessions and broken admin UI.

## Reference: Aggressive Static Cache Rule Creation
```bash
# Create ruleset if none exists
RULESET_ID=$(curl -sS "https://api.cloudflare.com/client/v4/zones/$ZONE_ID/rulesets" \
  -H "Authorization=[REDACTED] $TOKEN" | python3 -c "
import sys,json
for r in json.load(sys.stdin).get('result',[]):
    if r.get('phase') == 'http_request_cache_settings': print(r['id'])
")

# Add static asset rule
curl -sS -X POST "https://api.cloudflare.com/client/v4/zones/$ZONE_ID/rulesets/$RULESET_ID/rules" \
  -H "Authorization=[REDACTED] $TOKEN" -H "Content-Type: application/json" \
  --data-binary '{
    "action": "set_cache_settings",
    "action_parameters": {
      "cache": true,
      "edge_ttl": {"mode": "override_origin", "default": 31536000},
      "browser_ttl": {"mode": "override_origin", "default": 31536000}
    },
    "expression": "(ends_with(http.request.uri.path, \".css\") or ends_with(http.request.uri.path, \".js\") or ends_with(http.request.uri.path, \".woff2\") or ends_with(http.request.uri.path, \".webp\") or ends_with(http.request.uri.path, \".png\") or ends_with(http.request.uri.path, \".jpg\"))",
    "description": "Static assets: cache 1 year"
  }'
```
