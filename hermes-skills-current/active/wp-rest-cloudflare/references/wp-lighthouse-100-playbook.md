# Lighthouse 100 Performance Playbook for WordPress + Cloudflare + LiteSpeed

## Overview
Target: Lighthouse Performance score 95+ mobile, 98+ desktop on WordPress sites behind Cloudflare with LiteSpeed server.

## The Complete Snippet (one Code Snippet to rule them all)

```php
<?php
// ═══════════════════════════════════════════════════════
// LIGHTHOUSE PERFORMANCE 100 - Critical Optimizations
// ═══════════════════════════════════════════════════════

// 1. REMOVE WP BLOAT (reduces HTML size, removes render-blocking)
remove_action('wp_head', 'print_emoji_detection_script', 7);
remove_action('wp_print_styles', 'print_emoji_styles');
remove_action('admin_print_scripts', 'print_emoji_detection_script');
remove_action('admin_print_styles', 'print_emoji_styles');
remove_action('wp_head', 'wp_oembed_add_discovery_links');
remove_action('wp_head', 'wp_oembed_add_host_js');
add_filter('embed_oembed_discover', '__return_false');
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

// 2. CRITICAL CSS INLINE + CLS FIX + FONT SWAP
// NOTE: If Seraphinite Accelerator is active, inline <style> in wp_head
// gets stripped. Use wp_footer approach or wp_add_inline_style instead.
add_action('wp_head', function() { ?>
<style id="sota-critical">
@font-face{font-family:LocalFont;font-display:swap}
img{max-width:100%;height:auto;aspect-ratio:auto}
.cky-consent-container,.cky-modal{min-height:300px}
.cky-btn-revisit-wrapper{min-height:45px;min-width:45px}
</style>
<?php }, 0);

// 3. PRECONNECT + DNS PREFETCH (reduces connection time)
add_action('wp_head', function() { ?>
<link rel="preconnect" href="https://cdn.jsdelivr.net">
<link rel="preconnect" href="https://www.googletagmanager.com">
<link rel="dns-prefetch" href="//cdn.jsdelivr.net">
<link rel="dns-prefetch" href="//www.googletagmanager.com">
<?php }, 1);

// 4. REMOVE QUERY STRINGS (improves cache hit rate)
add_filter('script_loader_src', function($s) { return $s ? remove_query_arg('ver', $s) : $s; });
add_filter('style_loader_src', function($s) { return $s ? remove_query_arg('ver', $s) : $s; });

// 5. DEFER NON-CRITICAL JS (reduces TBT)
// CRITICAL: Do NOT defer jquery-core - breaks dependent scripts!
add_filter('script_loader_tag', function($tag, $handle) {
    $defer = ['cookie-law-info', 'wp-embed', 'nytsys.min'];
    foreach ($defer as $d) {
        if (strpos($handle, $d) !== false) return str_replace(' src', ' defer src', $tag);
    }
    return $tag;
}, 10, 2);

// 6. ASYNC third-party tracking scripts
add_filter('script_loader_tag', function($tag, $handle) {
    $async = ['clarity', 'metricool', 'grow'];
    foreach ($async as $d) {
        if (strpos($handle, $d) !== false) return str_replace(' src', ' async src', $tag);
    }
    return $tag;
}, 11, 2);

// 7. REMOVE JQUERY MIGRATE (reduces JS bytes)
add_action('wp_default_scripts', function($s) {
    if (!is_admin() && isset($s->registered['jquery'])) {
        $s->registered['jquery']->deps = array_diff($s->registered['jquery']->deps, ['jquery-migrate']);
    }
});

// 8. DISABLE WC CART FRAGMENTS for logged-out users
add_action('wp_enqueue_scripts', function() {
    if (!is_user_logged_in()) {
        wp_deregister_script('wc-cart-fragments');
        wp_dequeue_script('wc-cart-fragments');
    }
}, 11);

// 9. LAZY LOAD IMAGES (save bandwidth, reduce LCP bottleneck)
add_filter('wp_content_img_tag', function($h) {
    if (strpos($h, 'loading=') === false && strpos($h, 'fetchpriority=') === false) {
        return str_replace('<img ', '<img loading="lazy" ', $h);
    }
    return $h;
});
```

## Deployment via REST API

```python
import json
with open("/tmp/lh_snippet.json", "w") as f:
    f.write(json.dumps({
        "name": "LIGHTHOUSE 100 - Critical Performance",
        "description": "Critical CSS, font swap, CLS fix, defer JS, remove bloat",
        "code": snippet_code,  # the PHP from above
        "tags": ["performance", "lighthouse"],
        "scope": "global",
        "active": True
    }))
# POST to /wp-json/code-snippets/v1/snippets with Basic auth
```

## Cloudflare Settings (via API with Zone Settings:Edit token)

```bash
# Enable all at once per zone:
PATCH /zones/{zone}/settings/minify     {"value":{"html":"on","css":"on","js":"on"}}
PATCH /zones/{zone}/settings/brotli     {"value":"on"}
PATCH /zones/{zone}/settings/polish     {"value":"lossless"}  # or "lossy"
PATCH /zones/{zone}/settings/early_hints {"value":"on"}
```

## Cache Rules via Rulesets API

```bash
# Step 1: Create ruleset
POST /zones/{zone}/rulesets
{"name":"Cache Rules","kind":"zone","phase":"http_request_cache_settings","rules":[]}
# Save {ruleset_id}

# Step 2: HTML cache rule (4h edge, 1h browser, exclude admin/json)
POST /zones/{zone}/rulesets/{ruleset_id}/rules
{
  "action": "set_cache_settings",
  "action_parameters": {
    "cache": true,
    "edge_ttl": {"mode": "override_origin", "default": 14400},
    "browser_ttl": {"mode": "override_origin", "default": 3600}
  },
  "expression": "(not starts_with(http.request.uri.path, \"/wp-admin\")) and (not starts_with(http.request.uri.path, \"/wp-json\"))",
  "description": "HTML: cache 4 hours"
}

# Step 3: Static assets rule (1 year)
POST /zones/{zone}/rulesets/{ruleset_id}/rules
{
  "action": "set_cache_settings",
  "action_parameters": {
    "cache": true,
    "edge_ttl": {"mode": "override_origin", "default": 31536000},
    "browser_ttl": {"mode": "override_origin", "default": 31536000}
  },
  "expression": "(ends_with(http.request.uri.path, \".css\") or ends_with(http.request.uri.path, \".js\") or ends_with(http.request.uri.path, \".woff2\") or ends_with(http.request.uri.path, \".webp\") or ends_with(http.request.uri.path, \".png\") or ends_with(http.request.uri.path, \".jpg\"))",
  "description": "Static: cache 1 year"
}
```

## WordPress Plugin Management via REST

**Install and activate LiteSpeed Cache:**
```bash
POST /wp-json/wp/v2/plugins
{"slug": "litespeed-cache", "status": "active"}
```

**Activate Seraphinite Accelerator (for CSS/JS combine):**
```bash
# Find the plugin slug first
GET /wp-json/wp/v2/plugins?search=seraph
# Then activate it
POST /wp-json/wp/v2/plugins/{slug} -H "X-HTTP-Method-Override: PUT" --data-binary '{"status":"active"}'
```

**Deactivate a plugin:**
```bash
POST /wp-json/wp/v2/plugins/{slug} -H "X-HTTP-Method-Override: PUT" --data-binary '{"status":"inactive"}'
```

## Cache Purge Sequence (when plain URLs stay stale)

The most common failure mode: cache-busted URLs show the fix but plain URLs don't.

**Root cause:** The Cloudflare edge cache + LiteSpeed server cache form a two-layer cache hierarchy. Purging only Cloudflare is not enough — LitSpeed origin cache must also be purged.

**Nuclear purge sequence:**
1. Purge Cloudflare: `POST /zones/{zone}/purge_cache {"purge_everything":true}`
2. Purge LiteSpeed: either via the LS Cache plugin or a Code Snippet:
```php
add_action('init', function() {
    if (isset($_GET['purge_now'])) {
        if (class_exists('LiteSpeed_Cache_API')) LiteSpeed_Cache_API::purge_all();
        do_action('litespeed_purge_all');
        do_action('litespeed_purge_url', '/');
        if (function_exists('wp_cache_flush')) wp_cache_flush();
        exit('Purged');
    }
});
```
3. Trigger via: `curl "https://site.com/?purge_now=1"`
4. Wait 2-3 seconds
5. Warm with 3 unique query string requests: `?w=1`, `?w=2`, `?w=3`
6. Wait 2 seconds
7. Verify plain URL now shows the fix

## Seraphinite Accelerator Cache Issues

Seraphinite Accelerator intercepts the rendered HTML and caches optimized versions. If a Code Snippet adds inline `<style>` in `wp_head`, Seraphinite may strip it from its cached output.

**Workaround:** Inject styles via `wp_footer` (priority 1) or use `wp_add_inline_style('handle', 'css')` instead of raw `<style>` tags in `wp_head`.

**Forcing Seraphinite cache rebuild:** Visit `?seraph_accel_force=1` or go to wp-admin → Seraphinite Accelerator → Rebuild Cache.

## The Post-Optimization Verification Checklist

```bash
for site in "site1.com" "site2.com"; do
  echo "=== $site ==="
  curl -sI "https://$site/" -w "Status: %{http_code}\nTTFB: %{time_starttransfer}s\n" -o /dev/null
  curl -sI "https://$site/" | grep -o 'cf-cache-status: [A-Z]*'
  curl -sL "https://$site/" | grep -c 'font-display'   # should be >= 2
  curl -sL "https://$site/" | grep -c 'emoji'           # should be 0
  curl -sL "https://$site/" | grep -c 'wlwmanifest'     # should be 0
  curl -sL "https://$site/" | grep -c 'preconnect'      # should be >= 1
  curl -sL "https://$site/" | grep -c 'defer'           # should be >= 2
done
```

## Pitfalls

- **Deferring jquery-core breaks JavaScript.** jQuery must NOT be deferred. Only defer cookie-consent, analytics snippets, and embed scripts.
- **Seraphinite strips inline `<style>` from `wp_head`.** Use `wp_footer` or `wp_add_inline_style()` instead.
- **Cloudflare cache-busted URLs show fixes but plain URLs don't.** This means the origin LiteSpeed cache still has stale data. Use the nuclear purge sequence.
- **LiteSpeed Cache plugin can conflict with Seraphinite.** The safest combo: use LiteSpeed Cache plugin for page caching, Seraphinite for CSS/JS combine. Deactivate one if issues arise.
- **REST API for plugin install returns 500 if the site has a PHP fatal error.** You can still apply Cloudflare edge settings — those can't cause PHP issues.
- **Multiple active Code Snippets add PHP overhead.** Deactivate batch/one-time snippets via REST after they've done their job. Each active snippet's `code_error` should be `null`.
