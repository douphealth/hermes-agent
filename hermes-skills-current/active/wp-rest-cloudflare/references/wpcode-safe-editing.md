# WPCode safe editing: avoid PHP entity corruption

Use this when editing WPCode PHP snippets on WordPress sites behind Cloudflare/PhastPress, especially when the user reports a snippet is active but not visible.

## What went wrong

Direct/API/admin POST saves can corrupt WPCode PHP snippets by repeatedly HTML-encoding code (`'` -> `&#039;` -> `&amp;#039;` / worse). A corrupted constant/string can cause PHP parse/runtime failure and make the snippet disappear even though WPCode shows it as active.

## Safer workflow

1. Log in to wp-admin with a browser/session or `requests.Session` against `wp-login.php`.
2. Open the normal WPCode editor URL:
   - `/wp-admin/admin.php?page=wpcode-snippet-manager&snippet_id=<ID>`
3. Extract the real form `#wpcode-snippet-manager-form`.
4. Read code from `textarea[name="wpcode_snippet_code"]` and HTML-unescape exactly once before editing.
5. Preserve critical fields on POST:
   - `wpcode-save-snippet-nonce`
   - `_wp_http_referer`
   - `id`
   - `wpcode_snippet_title`
   - `wpcode_snippet_type=php`
   - `wpcode_snippet_code`
   - `wpcode_snippet_text`
   - `wpcode_auto_insert=1`
   - `wpcode_auto_insert_location`
   - `wpcode_priority`
   - `wpcode_active=on`
   - `button=publish`
6. Re-fetch the editor immediately and verify the code text contains the intended PHP, not entity-corrupted code.
7. Verify live output with cache-busting URLs (`?t=<timestamp>`), not cached pages.

## Common visibility / placement bug

If a WPCode author/EEAT box appears to be missing on desktop but exists in source, compare HTML offsets for:

- the snippet root class (example: `guf-eeat`, `aegis-root`)
- table-of-contents root/header/link text
- related-posts container (example: `relpost-block-container`)
- any existing author/AEGIS block

**Do not assume the fix is always “move it to the top.”** Confirm the user's requested placement and the current visual location first. Author/EEAT boxes can be intentionally placed at the end of the post for UX; moving them above the TOC can pollute the TOC and make the article look broken.

Placement choices in a `the_content` filter:

```php
// END of post body / after plugin-inserted related posts if this filter runs late
return $content . $html;

// TOP of post content / before body content and usually before related posts
return $html . $content;
```

If the box must be at the **end**, keep/restore `return $content . $html;` and improve styling/visibility instead of prepending. If headings inside the EEAT box are being indexed by the Table of Contents plugin, change internal `<h2>/<h3>` to semantic non-heading wrappers:

```php
$html .= '<div class="guf-eeat__title" role="heading" aria-level="2">Why trust this guide</div>';
$html .= '<div class="guf-eeat__author-name" role="heading" aria-level="3">...</div>';
```

Keep the filter priority stable unless verified; changing priority too early can break `is_singular()`, `in_the_loop()`, or `is_main_query()` behavior.

## Verification checklist

- Snippet is active in WPCode.
- PHP source is not double-encoded.
- Schema/JSON-LD appears where expected (`wp_head`/footer).
- Root HTML appears in the requested placement (top, before/after TOC, after related posts, before/after existing author box). Do not hard-code “before related posts” as success.
- Browser-rendered desktop/mobile placement is checked, not only curl/source offsets.
- Use browser DOM checks for *visible* state: `getComputedStyle`, `getBoundingClientRect()`, parent containment, and compare DOM order with `compareDocumentPosition()`.
- Scroll to the actual box and inspect a screenshot/vision result; if the user still cannot see it while DOM says visible, check overlays/popups/newsletter modals that can cover the block.
- TOC did not gain unwanted EEAT/author headings.
- Mobile and desktop both show the box with acceptable spacing and responsive stacking.
- No raw JS/PHP text is emitted.
- Final pass includes the exact no-query normal URL after cache flush, plus cache-busted checks on at least 2 posts.

## Last-resort visibility controller

If WPCode/the_content priority and cache behavior keep producing user-visible mismatch, avoid more risky WPCode rewrites. Add a small, marked, reversible controller in the active theme `functions.php` that only affects single posts and only moves the existing snippet DOM node. Use this as a positioning fallback, not as a replacement for the snippet.

Pattern:

```php
/* GUTF_FORCE_91008_FINAL_VISIBLE_YYYYMMDD */
add_action( 'wp_footer', function () {
    if ( ! is_singular( 'post' ) ) { return; }
    ?>
    <style id="gutf-force-eeat-visible-css">
      body.single-post aside.guf-eeat{
        display:block!important;visibility:visible!important;opacity:1!important;
        transform:none!important;clear:both!important;position:relative!important;z-index:9!important;
      }
    </style>
    <script id="gutf-force-eeat-visible-js">
      (function(){
        function placeEEAT(){
          var box=document.querySelector('aside.guf-eeat');
          if(!box) return false;
          var target=document.querySelector('#aegis-root,.aegis-root,[class*="aegis"]');
          if(target && target.parentNode){ target.parentNode.insertBefore(box,target.nextSibling); return true; }
          var article=document.querySelector('article');
          if(article && article.lastElementChild!==box){ article.appendChild(box); return true; }
          var footer=document.querySelector('footer');
          if(footer && footer.parentNode){ footer.parentNode.insertBefore(box,footer); return true; }
        }
        placeEEAT();
        if(document.readyState==='loading'){document.addEventListener('DOMContentLoaded',placeEEAT,{once:true});}
        var n=0,t=setInterval(function(){placeEEAT(); if(++n>20) clearInterval(t);},250);
      })();
    </script>
    <?php
}, 99999 );
```

After adding this fallback, verify with `?phast=nocache` first. If normal URLs do not include the controller, flush PhastPress/cache and then remove any temporary flush code, leaving only the marked controller.

## Style/UX preference from GearUpToFit author boxes

When the user says a WordPress author/EEAT block is ugly or asks for “1000x more beautiful,” treat it as a full visual overhaul, not a tiny CSS tweak: premium card surface, tinted shadows, responsive grid, author avatar treatment, trust badges/pills, readable mobile stacking, and no generic boxed-border look. If the user asks to place it at the end of the post, preserve that UX even if top placement might boost source-order prominence.
