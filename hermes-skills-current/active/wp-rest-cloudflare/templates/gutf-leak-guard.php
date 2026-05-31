<?php
/**
 * Plugin Name: GUTF Elementor Output Guard
 * Description: Output-layer guard for GearUpToFit: removes duplicated plaintext Elementor CSS, normalizes origin hostname, suppresses duplicate Elementor chrome on self-contained imported reviews, and can recover the broken /blog/ route.
 * Version: 1.3.0-template
 */
if (!defined('ABSPATH')) { exit; }

// Exact-path recovery for /blog/ when Elementor archive routing renders the wrong hub + empty archive.
// Keep exact-path only; do not hijack all categories/archives.
add_action('template_redirect', function () {
    if (is_admin() || (function_exists('wp_doing_ajax') && wp_doing_ajax())) { return; }
    $path = trim(parse_url($_SERVER['REQUEST_URI'] ?? '', PHP_URL_PATH), '/');
    if ($path !== 'blog') { return; }

    status_header(200);
    nocache_headers();
    add_filter('document_title_parts', function ($parts) { $parts['title'] = 'Blog'; return $parts; }, 20);
    get_header();

    $q = new WP_Query(array(
        'post_type' => 'post',
        'post_status' => 'publish',
        'posts_per_page' => 18,
        'ignore_sticky_posts' => false,
    ));
    ?>
    <main id="primary" class="gutf-blog-index" role="main">
      <style id="gutf-blog-index-css">
        .gutf-blog-index{max-width:1180px;margin:0 auto;padding:44px 18px 70px;font-family:system-ui,-apple-system,BlinkMacSystemFont,"Segoe UI",sans-serif;color:#111827}.gutf-blog-hero{background:linear-gradient(135deg,#071f1d,#0f766e);color:#fff;border-radius:28px;padding:42px 32px;margin:0 0 34px;box-shadow:0 18px 45px rgba(15,118,110,.22)}.gutf-blog-eyebrow{font-size:13px;font-weight:800;letter-spacing:.14em;text-transform:uppercase;color:#99f6e4;margin-bottom:10px}.gutf-blog-hero h1{font-size:clamp(34px,5vw,62px);line-height:1.02;margin:0 0 14px;color:#fff}.gutf-blog-hero p{font-size:clamp(17px,2vw,21px);line-height:1.65;max-width:820px;margin:0;color:#e6fffb}.gutf-blog-grid{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:24px}.gutf-blog-card{background:#fff;border:1px solid #e5e7eb;border-radius:22px;overflow:hidden;box-shadow:0 10px 28px rgba(17,24,39,.08);transition:transform .18s ease,box-shadow .18s ease}.gutf-blog-card:hover{transform:translateY(-3px);box-shadow:0 18px 38px rgba(17,24,39,.13)}.gutf-blog-thumb{display:block;aspect-ratio:16/9;background:#f3f4f6;overflow:hidden}.gutf-blog-thumb img{width:100%;height:100%;object-fit:cover;display:block}.gutf-blog-body{padding:20px}.gutf-blog-meta{font-size:12px;font-weight:800;letter-spacing:.08em;text-transform:uppercase;color:#0f766e;margin-bottom:9px}.gutf-blog-card h2{font-size:21px;line-height:1.25;margin:0 0 10px}.gutf-blog-card h2 a{color:#111827;text-decoration:none}.gutf-blog-card h2 a:hover{color:#0f766e}.gutf-blog-excerpt{font-size:15px;line-height:1.65;color:#4b5563;margin:0 0 16px}.gutf-blog-read{font-weight:800;color:#0f766e;text-decoration:none}.gutf-blog-empty{padding:40px;background:#fff7ed;border:1px solid #fed7aa;border-radius:20px}@media(max-width:900px){.gutf-blog-grid{grid-template-columns:repeat(2,minmax(0,1fr))}.gutf-blog-hero{padding:34px 24px}}@media(max-width:640px){.gutf-blog-index{padding:28px 14px 54px}.gutf-blog-grid{grid-template-columns:1fr;gap:18px}.gutf-blog-hero{border-radius:22px;padding:28px 20px}.gutf-blog-body{padding:18px}.gutf-blog-card h2{font-size:19px}}
      </style>
      <section class="gutf-blog-hero" aria-labelledby="gutf-blog-title">
        <div class="gutf-blog-eyebrow">Gear Up to Fit Blog</div>
        <h1 id="gutf-blog-title">Latest Fitness, Running, Nutrition & Gear Guides</h1>
        <p>Fresh evidence-based training guides, running shoe reviews, health explainers, nutrition advice, and practical tools from Gear Up to Fit.</p>
      </section>
      <?php if ($q->have_posts()) : ?>
      <section class="gutf-blog-grid" aria-label="Latest posts">
        <?php while ($q->have_posts()) : $q->the_post(); ?>
          <article class="gutf-blog-card">
            <a class="gutf-blog-thumb" href="<?php echo esc_url(get_permalink()); ?>" aria-label="<?php echo esc_attr(get_the_title()); ?>">
              <?php if (has_post_thumbnail()) { the_post_thumbnail('medium_large', array('loading' => 'lazy')); } ?>
            </a>
            <div class="gutf-blog-body">
              <div class="gutf-blog-meta"><?php echo esc_html(get_the_date('M j, Y')); ?><?php $cat = get_the_category(); if (!empty($cat)) { echo ' · ' . esc_html($cat[0]->name); } ?></div>
              <h2><a href="<?php echo esc_url(get_permalink()); ?>"><?php the_title(); ?></a></h2>
              <p class="gutf-blog-excerpt"><?php echo esc_html(wp_trim_words(get_the_excerpt(), 24)); ?></p>
              <a class="gutf-blog-read" href="<?php echo esc_url(get_permalink()); ?>">Read article →</a>
            </div>
          </article>
        <?php endwhile; wp_reset_postdata(); ?>
      </section>
      <?php else : ?>
        <div class="gutf-blog-empty">No posts found.</div>
      <?php endif; ?>
    </main>
    <?php
    get_footer();
    exit;
}, 0);

if (!is_admin() && !(function_exists('wp_doing_ajax') && wp_doing_ajax())) {
    ob_start(function ($html) {
        if (!is_string($html) || $html === '') { return $html; }

        // Public URLs must never send users to the origin hostname. Replace bare hostname so normal,
        // URL-encoded, and JS-escaped references are corrected.
        if (strpos($html, 'origin.gearuptofit.com') !== false) {
            $html = str_replace('origin.gearuptofit.com', 'gearuptofit.com', $html);
        }

        // Remove duplicated plaintext GUTF CSS leaks while preserving valid <style> blocks.
        if (strpos($html, '.gutf-article') !== false) {
            // Case 1: duplicated text node immediately after a style tag.
            $pattern1 = '~(</style>)\s*\.gutf-article\s*\{(?:(?!<).)*?@media\s*\(max-width:\s*480px\)\s*\{(?:(?!<).)*?\}\s*(?=<)~s';
            $cleaned = preg_replace($pattern1, "$1\n", $html, -1, $count1);
            if ($count1 > 0 && is_string($cleaned)) { $html = $cleaned; }

            // Case 2: stale/generated pages where the same CSS became a body text node before the header.
            $pattern2 = '~(<body[^>]*>)\s*\.gutf-article\s*\{(?:(?!<).)*?@media\s*\(max-width:\s*480px\)\s*\{(?:(?!<).)*?\}\s*(?=<)~is';
            $cleaned = preg_replace($pattern2, "$1\n", $html, 1, $count2);
            if ($count2 > 0 && is_string($cleaned)) { $html = $cleaned; }
        }

        // Imported reviews that contain a complete GUTF review document should not also show Elementor chrome.
        if (strpos($html, 'class="gutf-review-page"') !== false || strpos($html, "class='gutf-review-page'") !== false) {
            $css = '<style id="gutf-self-contained-review-guard">body.single-post .elementor-widget-theme-post-title,body.single-post .elementor-widget-post-info,body.single-post .elementor-widget-theme-post-featured-image,body.single-post .elementor-widget-table-of-contents,body.single-post .sota-root{display:none!important}</style>';
            if (strpos($html, 'id="gutf-self-contained-review-guard"') === false) {
                $html = preg_replace('~</head>~i', $css . "\n</head>", $html, 1);
            }
        }

        return $html;
    });
}
