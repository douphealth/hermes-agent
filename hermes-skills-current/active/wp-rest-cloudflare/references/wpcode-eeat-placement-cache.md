# WPCode E-E-A-T / Author Box Placement + Cache Verification

Use this when a WPCode PHP snippet is active but the user says the author/E-E-A-T box is not visible on WordPress posts, especially on Elementor/PhastPress sites.

## Key lesson

Do **not** stop at “the HTML exists.” The user cares about visible desktop placement. A snippet can be:

- active in WPCode,
- present in source,
- present with cache-busting query params,
- and still appear “not working” because it is below the Table of Contents, below related posts, hidden by CSS, or stale cached HTML is served on the normal URL.

## Investigation order

1. Open the exact normal post URL in a browser automation session, desktop viewport.
2. Use the accessibility snapshot / vision check to locate the visible block relative to:
   - article title,
   - author/meta line,
   - Table of Contents,
   - article content,
   - related posts.
3. Also fetch raw source for positions:
   ```python
   import requests
   h = requests.get(URL, headers={'User-Agent':'Mozilla/5.0'}, timeout=40).text
   for t in ['guf-eeat','guf-eeat__author-card','TABLE OF CONTENTS','relpost-block-container','aegis-root']:
       i = h.find(t)
       print(t, i, h[:i].count('\n')+1 if i != -1 else -1)
   ```
4. Compare all three forms:
   - normal URL: `https://site.com/post/`
   - cache-busted: `https://site.com/post/?t=TIMESTAMP`
   - PhastPress bypass: `https://site.com/post/?phast=-phast`

If only cache-busted/bypass works, the fix is not done. Flush cache and recheck the normal URL.

## Common fix: prepend instead of append

If the snippet builds `$html` inside a `the_content` filter and currently ends with:

```php
return $content . $html;
```

then it appears after content and often after related posts. Change to:

```php
return $html . $content;
```

Keep `the_content` priority high enough for WordPress conditionals; priorities below 10 can make `is_singular()` / `is_single()` unreliable.

## Common fix: visibly above Table of Contents

If prepending still leaves the box under a Table of Contents plugin, add a footer DOM fallback that moves the existing rendered box above the TOC. This is safer than duplicating the box.

```php
add_action( 'wp_footer', function() {
    if ( ! is_singular( 'post' ) ) { return; }
    ?>
    <style id="gutf-eeat-force-visible">
      aside.guf-eeat{display:block!important;visibility:visible!important;opacity:1!important;clear:both!important;position:relative!important;z-index:5!important;margin:24px auto!important;max-width:1120px!important;height:auto!important;overflow:visible!important;}
      aside.guf-eeat *{visibility:visible!important;opacity:1!important;}
    </style>
    <script id="gutf-eeat-force-above-toc">
    (function(){
      function moveEEAT(){
        var box=document.querySelector('aside.guf-eeat');
        if(!box || box.dataset.gutfMoved==='1') return;
        var headings=[].slice.call(document.querySelectorAll('h1,h2,h3,h4,.lwptoc_title,.ez-toc-title,.toc_title'));
        var toc=null;
        for(var i=0;i<headings.length;i++){
          if(/table\s+of\s+contents/i.test((headings[i].textContent||'').trim())){toc=headings[i];break;}
        }
        var target=toc;
        while(target && target.parentElement && target.parentElement !== document.body){
          var cls=(target.className||'').toString();
          if(/toc|contents|lwptoc|ez-toc/i.test(cls)) break;
          if(target.parentElement.matches && target.parentElement.matches('article,.entry-content,.post,.content')) break;
          target=target.parentElement;
        }
        if(toc){ (target||toc).parentNode.insertBefore(box, target||toc); box.dataset.gutfMoved='1'; }
      }
      if(document.readyState==='loading') document.addEventListener('DOMContentLoaded',moveEEAT); else moveEEAT();
      setTimeout(moveEEAT,500); setTimeout(moveEEAT,1500); setTimeout(moveEEAT,3000);
    })();
    </script>
    <?php
}, 9999 );
```

## Emergency PhastPress cache flush pattern

When normal URLs remain stale after snippet changes, inject a **temporary** one-shot cache flush into a safe PHP snippet or functions.php, trigger a few normal URLs, then remove it immediately.

```php
add_action( 'init', function() {
    if ( get_transient( 'hermes_cache_flush_done' ) ) { return; }
    set_transient( 'hermes_cache_flush_done', 1, HOUR_IN_SECONDS );
    $delete = function( $path ) use ( &$delete ) {
        if ( ! file_exists( $path ) ) { return; }
        if ( is_file( $path ) || is_link( $path ) ) { @unlink( $path ); return; }
        $items = @scandir( $path ); if ( ! is_array( $items ) ) { return; }
        foreach ( $items as $item ) {
            if ( $item !== '.' && $item !== '..' ) { $delete( $path . DIRECTORY_SEPARATOR . $item ); }
        }
        if ( basename( $path ) !== 'cache' ) { @rmdir( $path ); }
    };
    foreach ( array(
        WP_CONTENT_DIR . '/cache/phastpress',
        WP_CONTENT_DIR . '/cache/phast',
        WP_CONTENT_DIR . '/cache/phast-press',
        WP_CONTENT_DIR . '/cache'
    ) as $dir ) {
        if ( is_dir( $dir ) ) { $delete( $dir ); }
    }
    if ( function_exists( 'wp_cache_flush' ) ) { wp_cache_flush(); }
}, 1 );
```

After triggering, remove the temporary block and re-save. Then verify the normal URLs again.

## Verification standard before telling the user it works

Before claiming success, provide evidence from the **normal non-cache-busted URL**:

- browser snapshot shows the box visible near the top,
- source contains the visible heading/marker,
- `guf-eeat` or equivalent appears before `relpost-block-container`,
- if the user complained about desktop, verify desktop viewport visually,
- do not say “it exists in HTML” as the final answer.

## Tone/workflow for angry site-repair sessions

If the user says “BS / not working,” assume your prior verification missed the user-visible issue. Immediately re-check the exact normal URL and browser render. Do not defend the previous result. State what you are checking and fix the visible failure.