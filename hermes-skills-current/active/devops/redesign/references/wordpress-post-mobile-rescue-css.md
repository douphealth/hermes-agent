# WordPress post mobile rescue CSS

Use this when a single WordPress article/post renders correctly in source but is visually crushed on mobile, especially after AI/imported HTML modules are embedded inside Elementor/theme wrappers.

## Failure signature

- Screenshot shows hero text in a very narrow column, with badges/pills floating beside it.
- DOM may show no horizontal overflow, but the visible composition is broken.
- The broken block is often a semantic `<header>` inside post content, e.g. `.gu-ms-hero` or `.sota-root`.
- Elementor/theme global CSS can apply layout to generic selectors like `header`, causing article-internal hero headers to inherit `display:flex`, `flex-direction`, fixed widths, or child alignment.

## Fast diagnosis

Run a mobile iframe check from the browser console so the page is tested through the live CDN/theme stack:

```js
new Promise(resolve => {
  const old = document.querySelector('iframe'); if (old) old.remove();
  const f = document.createElement('iframe');
  f.style.cssText = 'position:fixed;left:0;top:0;width:390px;height:900px;z-index:999999;background:white;border:4px solid blue';
  f.src = location.href.split('?')[0] + '?mobilecheck=' + Date.now();
  document.body.appendChild(f);
  f.onload = () => setTimeout(() => {
    const d = f.contentDocument, w = f.contentWindow;
    const hero = d.querySelector('.gu-ms-hero,.sota-root,[class*=hero]');
    resolve({
      vw: w.innerWidth,
      docScroll: d.documentElement.scrollWidth,
      bodyScroll: d.body.scrollWidth,
      heroDisplay: hero && w.getComputedStyle(hero).display,
      heroW: hero && Math.round(hero.getBoundingClientRect().width),
      title: d.title
    });
  }, 2500);
});
```

Also inspect obvious crushed children:

```js
[...d.querySelectorAll('.gu-ms-lede,.gu-ms-meta,.gu-ms-pill,.sota-card,.sota-star-rating')].map(el => ({
  cls: el.className,
  display: w.getComputedStyle(el).display,
  w: Math.round(el.getBoundingClientRect().width),
  x: Math.round(el.getBoundingClientRect().x)
}))
```

## Scoped rescue pattern

Inject a post-scoped `<style id="gutf-mobile-visual-hardfix">` or similarly unique ID at the top of the affected post content. Scope to the article's custom class when possible; use `!important` to override theme/Elementor globals.

```html
<style id="gutf-mobile-visual-hardfix">
@media (max-width: 767px){
  html, body { overflow-x: clip !important; }
  .entry-content, .post-content, .elementor-widget-theme-post-content, article {
    max-width: 100% !important;
  }
  .gu-ms-hero,
  .sota-root,
  .article-hero {
    display: block !important;
    width: auto !important;
    max-width: 100% !important;
    margin-inline: 0 !important;
    box-sizing: border-box !important;
  }
  .gu-ms-hero > *,
  .sota-root > *,
  .article-hero > * {
    position: static !important;
    float: none !important;
    transform: none !important;
    width: 100% !important;
    max-width: 100% !important;
    min-width: 0 !important;
    margin-inline: 0 !important;
    box-sizing: border-box !important;
  }
  .gu-ms-lede, .gu-ms-meta, .sota-card, .sota-author-row, .sota-badges {
    display: block !important;
    line-height: 1.55 !important;
    text-align: left !important;
  }
  .gu-ms-pill, .sota-badges > * {
    display: block !important;
    width: 100% !important;
    margin: 8px 0 !important;
    white-space: normal !important;
  }
  img, video, iframe, table { max-width: 100% !important; height: auto !important; }
  table { table-layout: fixed !important; display: table !important; }
  th, td { white-space: normal !important; overflow-wrap: anywhere !important; }
}
</style>
```

## Cache + routing pitfalls

- Purge Cloudflare after writing the post.
- Clear PhastPress/on-site cache when present; Cloudflare purge alone may leave old HTML.
- If the clean slug still serves stale/broken HTML but `?fresh=<timestamp>` is fixed, add a temporary Worker route/query bypass for the slug to fetch by post ID (`/?p=POST_ID&fresh=1`) until caches expire.
- Verify both clean URL and cache-busted URL.

## Success criteria

- Mobile iframe viewport around 382-390px reports `documentElement.scrollWidth <= innerWidth` or only a few px less due iframe borders.
- Hero/internal block display is `block` or intended stacked layout, not inherited theme flex.
- Visual inspection confirms text is readable, not a skinny column, and badges/pills are stacked or wrapped cleanly.
