# WordPress Performance: Frontend Bloat Removal via Code Snippets

## Purpose
Remove non-critical frontend bloat from WordPress sites using Code Snippets, without touching theme files or plugins. All changes are reversible via the Code Snippets admin UI.

## When to Use
- User says the site feels slow or bloated
- Homepage has legacy WordPress meta tags, emoji script, embed scripts
- jQuery migrate is loaded but no jQuery-dependent plugins need it
- External analytics/tracking origins lack preconnect hints
- You have Code Snippets plugin active and REST API access
- LiteSpeed Cache is now active (or Seraphinite has been swapped out)

## Do NOT Use For
- Removing scripts that are critical for conversion paths or revenue
- Sites where LiteSpeed Cache or Seraphinite Accelerator handles optimization already (they conflict)
- Deep theme/plugin audits (do one simple pass, then stop)

## The Single Comprehensive Snippet Pattern
Deploy one active global Code Snippets snippet that combines all bloat removals, resource hints, and script optimizations. This avoids creating 8 separate snippets for 8 small fixes.

### SOTA Snippet Template

```php
<?php
/**
 * SOTA Performance: Frontend Bloat Removal + Resource Hints
 * Deactivate via Code Snippets → toggle off → purges instantly
 */

// ===== 1. REMOVE LEGACY WP BLOAT =====

// Emoji script (safe to remove on any site without emoji-dependent features)
remove_action('wp_head', 'print_emoji_detection_script', 7);
remove_action('wp_print_styles', 'print_emoji_styles');
remove_action('admin_print_scripts', 'print_emoji_detection_script');
remove_action('admin_print_styles', 'print_emoji_styles');

// Embed script (only affects oEmbed — safe if embeds not used)
remove_action('wp_head', 'wp_oembed_add_discovery_links');
remove_action('wp_head', 'wp_oembed_add_host_js');
add_filter('embed_oembed_discover', '__return_false');

// Legacy XML-RPC / manifest tags (safe — no modern use)
remove_action('wp_head', 'wlwmanifest_link');
remove_action('wp_head', 'rsd_link');
remove_action('wp_head', 'wp_shortlink_wp_head');
remove_action('wp_head', 'rest_output_link_wp_head');
remove_action('wp_head', 'wp_generator');

// ===== 2. DISABLE SELF-PINGBACKS =====
add_action('pre_ping', function(&$links) {
    foreach ($links as $l => $link) {
        if (strpos($link, home_url()) !== false) {
            unset($links[$l]);
        }
    }
});

// ===== 3. SAFELY REMOVE JQUERY MIGRATE =====
// Only removes migrate — keeps jQuery intact
// If a plugin breaks, deactivate this section
add_action('wp_default_scripts', function($scripts) {
    if (!is_admin() && isset($scripts->registered['jquery'])) {
        $script = $scripts->registered['jquery'];
        if ($script->deps) {
            $script->deps = array_diff($script->deps, ['jquery-migrate']);
        }
    }
});

// ===== 4. RESOURCE HINTS (preconnect / dns-prefetch) =====
// Add preconnect for every external origin the homepage loads from
add_action('wp_head', function() {
    ?>
<link rel="preconnect" href="https://cdn.jsdelivr.net">
<link rel="preconnect" href="https://www.googletagmanager.com">
<link rel="preconnect" href="https://www.google-analytics.com">
<link rel="dns-prefetch" href="//cdn.jsdelivr.net">
<link rel="dns-prefetch" href="//www.googletagmanager.com">
<link rel="dns-prefetch" href="//plugin.nytsys.com">
<link rel="dns-prefetch" href="//tracker.metricool.com">
<link rel="dns-prefetch" href="//faves.grow.me">
<?php
}, 1);

// ===== 5. DISABLE WOOCOMMERCE CART FRAGMENTS (non-logged-in) =====
add_action('wp_enqueue_scripts', function() {
    if (!is_user_logged_in()) {
        wp_deregister_script('wc-cart-fragments');
        wp_dequeue_script('wc-cart-fragments');
    }
}, 11);

// ===== 6. REMOVE QUERY STRINGS FROM STATIC ASSETS =====
add_filter('script_loader_src', function($src) {
    if (strpos($src, '?ver=') !== false) {
        $src = remove_query_arg('ver', $src);
    }
    return $src;
});
add_filter('style_loader_src', function($src) {
    if (strpos($src, '?ver=') !== false) {
        $src = remove_query_arg('ver', $src);
    }
    return $src;
});

// ===== 7. ADD LAZY LOADING TO IMAGES =====
add_filter('wp_content_img_tag', function($html) {
    if (strpos($html, 'loading=') === false) {
        $html = str_replace('<img ', '<img loading="lazy" ', $html);
    }
    return $html;
});

// ===== 8. ADD SECURITY / CACHING HEADERS =====
add_action('send_headers', function() {
    if (!is_admin()) {
        header('X-Content-Type-Options: nosniff');
    }
});

// ===== 9. REMOVE ADDITIONAL HEAD LINKS (safe extras) =====
remove_action('wp_head', 'index_rel_link');
remove_action('wp_head', 'parent_post_rel_link', 10);
remove_action('wp_head', 'start_post_rel_link', 10);
remove_action('wp_head', 'adjacent_posts_rel_link', 10);
remove_action('wp_head', 'adjacent_posts_rel_link_wp_head', 10);

// Remove recent comments inline style
add_action('widgets_init', function() {
    global $wp_widget_factory;
    if (isset($wp_widget_factory->widgets['WP_Widget_Recent_Comments'])) {
        remove_action('wp_head', [$wp_widget_factory->widgets['WP_Widget_Recent_Comments'], 'recent_comments_style']);
    }
});

// Remove WordPress version from RSS
add_filter('the_generator', '__return_empty_string');
```

## Verification Commands

```bash
# Check which items were actually removed
curl -sL "https://example.com/" | grep -c 'emoji\|wlwmanifest\|rsd\|shortlink\|jquery-migrate'

# Check resource hints appeared
curl -sL "https://example.com/" | grep -c 'preconnect\|dns-prefetch'

# Performance timing
curl -o /dev/null -sS -w 'ttfb=%{time_starttransfer} total=%{time_total}\n' https://example.com/
```

## Pitfalls

- **Cache hides changes**: LiteSpeed or Seraphinite cache may serve pre-snippet HTML. Use a cache-busting query string (`?v=timestamp`) or Cloudflare purge to verify.
- **jQuery migrate may be needed**: If a theme or plugin relies on deprecated jQuery methods, removing migrate can break sliders, tabs, or other JS widgets. Test on staging first, or keep it if uncertain.
- **Preconnect only helps with warm cache**: On repeat visits, preconnect shaves ~100ms of DNS/TLS. First visit still resolves fresh.
- **Query string removal can break CDN cache**: If your CDN uses `ver=` as a cache-busting strategy, removing it may cause stale asset versions. Only remove if your CDN/plugin has an alternative versioning strategy.
- **Some items are added by plugins, not core**: RSD link, shortlink, and generator may be re-inserted by Yoast SEO, Jetpack, or other plugins even after core removal. The `remove_action()` calls may need to target plugin-specific hooks if items persist after cache clear.
- **Seraphinite Accelerator conflict**: If Seraphinite is active, it may lazy-load or defer scripts with its own `type="o/js-lzl"` system, preventing `remove_action()` from working. If switching to LiteSpeed Cache, deactivate Seraphinite first.
