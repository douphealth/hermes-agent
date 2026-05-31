# SOTA WordPress Post Header Shortcodes

Complete set of shortcodes and CSS for enterprise-grade blog post headers. Designed to be placed via Elementor Shortcode widget or inserted into `the_content`.

## Shortcodes

### `[wpbread]` — Yoast SEO Breadcrumbs
```php
add_shortcode('wpbread', function() {
    if (function_exists('yoast_breadcrumb')) {
        ob_start();
        yoast_breadcrumb('<nav class="wpbread">', '</nav>');
        return ob_get_clean();
    }
    return '<nav class="wpbread"><a href="' . home_url() . '">Home</a></nav>';
});
```

### `[last_modified_date]` — Last Modified Date
```php
add_shortcode('last_modified_date', function() {
    global $post;
    if ($post) {
        return get_the_modified_date('F j, Y');
    }
    return '';
});
```

### `[reading_time]` — Reading Time Estimate
Calculates at ~200 words/min. Returns e.g. "⏱ 12 min read".
```php
add_shortcode('reading_time', function() {
    global $post;
    if (!$post) return '';
    $content = get_post_field('post_content', $post->ID);
    $words = str_word_count(wp_strip_all_tags($content));
    $minutes = max(1, ceil($words / 200));
    $label = $minutes === 1 ? 'minute' : 'minutes';
    return '<span class="sota-reading-time">⏱ ' . $minutes . ' ' . $label . ' read</span>';
});
```

### `[post_categories]` — Category Badge Links
```php
add_shortcode('post_categories', function() {
    global $post;
    if (!$post) return '';
    $categories = get_the_category($post->ID);
    if (empty($categories)) return '';
    $output = '<span class="sota-categories">';
    $links = array();
    foreach ($categories as $cat) {
        $links[] = '<a href="' . esc_url(get_category_link($cat->term_id)) . '" class="sota-cat-badge">' . esc_html($cat->name) . '</a>';
    }
    $output .= implode(' ', $links);
    $output .= '</span>';
    return $output;
});
```

### `[author_avatar]` — Author Avatar + Name
```php
add_shortcode('author_avatar', function() {
    global $post;
    if (!$post) return '';
    $author_id = $post->post_author;
    $avatar = get_avatar($author_id, 40, '', get_the_author_meta('display_name', $author_id), array('class' => 'sota-avatar'));
    $name = get_the_author_meta('display_name', $author_id);
    return '<span class="sota-author-block">' . $avatar . ' <span class="sota-author-name">' . esc_html($name) . '</span></span>';
});
```

### `[affiliate_disclosure]` — FTC Affiliate Disclosure
```php
add_shortcode('affiliate_disclosure', function() {
    $text = 'We independently review everything we recommend. When you buy through our links, we may earn a commission.';
    return '<div class="sota-disclosure">📢 ' . esc_html($text) . '</div>';
});
```

## CSS (inject via `wp_head`)

```php
add_action('wp_head', function() {
    echo '<style id="sota-styles">
    .sota-reading-time { display:inline-block; background:#f0f4f8; color:#2d3748; padding:3px 10px; border-radius:4px; font-size:13px; font-weight:500; margin-right:8px; }
    .sota-categories { display:inline-block; }
    .sota-cat-badge { display:inline-block; background:#ebf8ff; color:#2b6cb0; padding:3px 10px; border-radius:4px; font-size:13px; font-weight:500; text-decoration:none; margin-right:4px; }
    .sota-cat-badge:hover { background:#bee3f8; }
    .sota-author-block { display:inline-flex; align-items:center; gap:6px; }
    .sota-author-block .sota-avatar { border-radius:50%; width:24px; height:24px; }
    .sota-author-block .sota-author-name { font-weight:600; font-size:14px; color:#2d3748; }
    .sota-disclosure { background:#fffff0; border-left:3px solid #d69e2e; padding:8px 14px; margin:16px 0; font-size:13px; color:#744210; border-radius:3px; }
    .wpbread { font-size:13px; color:#718096; margin-bottom:8px; }
    .wpbread a { color:#4a5568; text-decoration:none; }
    .wpbread a:hover { color:#2b6cb0; text-decoration:underline; }
    .wpbread .breadcrumb_last { color:#2d3748; font-weight:500; }
    </style>';
});
```

## Elementor Usage

Elementor-built posts do NOT use WordPress's `the_content` filter. To use these shortcodes:

1. Add all shortcode handlers + CSS to `functions.php` (as shown above)
2. In Elementor editor, add a **Shortcode** widget
3. Paste the shortcodes: `[author_avatar] · January 4, 2026 · 3:15 pm [wpbread] [reading_time] [post_categories] 📅 Updated: [last_modified_date]`
4. Add another Shortcode widget at post bottom: `[affiliate_disclosure]`

## Auto-Injection for Non-Elementor Posts

For classic WordPress posts (not Elementor), use `the_content` filter:

```php
add_filter('the_content', function($content) {
    if (!is_singular('post') || !in_the_loop() || !is_main_query()) {
        return $content;
    }
    // Skip if Elementor is rendering
    if (class_exists('\\Elementor\\Plugin') && \\Elementor\\Plugin::instance()->documents->get_current() && \\Elementor\\Plugin::instance()->documents->get_current()->is_built_with_elementor()) {
        return $content;
    }
    
    $header = '<div class="sota-post-header" style="margin-bottom:20px;padding-bottom:16px;border-bottom:1px solid #e2e8f0;">';
    $header .= '<div style="display:flex;align-items:center;gap:10px;flex-wrap:wrap;margin-bottom:8px;">';
    $header .= do_shortcode('[author_avatar]');
    $header .= '<span style="color:#718096;font-size:13px;">·</span>';
    $header .= '<span style="color:#718096;font-size:13px;">' . get_the_date('F j, Y') . '</span>';
    $header .= '<span style="color:#718096;font-size:13px;">·</span>';
    $header .= '<span style="color:#718096;font-size:13px;">' . get_the_time('g:i a') . '</span>';
    $header .= '</div>';
    $header .= '<div style="margin-bottom:6px;">' . do_shortcode('[wpbread]') . '</div>';
    $header .= '<div style="display:flex;align-items:center;gap:8px;flex-wrap:wrap;">';
    $header .= do_shortcode('[reading_time]');
    $header .= do_shortcode('[post_categories]');
    $header .= '<span style="color:#a0aec0;font-size:12px;">📅 Updated: ' . do_shortcode('[last_modified_date]') . '</span>';
    $header .= '</div>';
    $header .= '</div>';
    
    $content = $header . $content . do_shortcode('[affiliate_disclosure]');
    return $content;
}, 5);
```
