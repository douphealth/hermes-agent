# GearUpToFit visual layout verification for imported/review posts

Use this when fixing GearUpToFit WordPress review posts with custom imported HTML, affiliate cards, star ratings, comparison/spec tables, or schema/template residue. The durable lesson: **string cleanup is not visual cleanup**. A page can pass bad-string checks and still be unusable on mobile.

## Required workflow

1. **Audit rendered mobile and desktop, not just raw HTML.**
   - Use a real browser/iframe/mobile viewport around 390px width and a desktop viewport.
   - Check `document.documentElement.scrollWidth`, `document.body.scrollWidth`, and overflowing elements.
   - Do not claim visual success from `curl`/REST/string checks alone.

2. **DOM overflow probe for mobile.** Run from browser context after page load. For repeatable QA across URLs, use the packaged script `scripts/gutf-rendered-responsive-probe.js` from this skill (requires `puppeteer-core` and a Chrome/headless-shell executable):

```bash
node scripts/gutf-rendered-responsive-probe.js /path/to/chrome \
  https://gearuptofit.com/running/hoka-speedgoat-7/ \
  https://gearuptofit.com/fitness-and-health-calculators/calculate-bmi-bmr-and-whr-now/
```

Inline probe:

```js
(() => {
  const w = window.innerWidth;
  const bad = [];
  document.querySelectorAll('body *').forEach(el => {
    const r = el.getBoundingClientRect();
    const cs = getComputedStyle(el);
    if (r.width > w + 8 && cs.display !== 'none') {
      bad.push({
        tag: el.tagName,
        cls: String(el.className),
        w: Math.round(r.width),
        left: Math.round(r.left),
        text: (el.innerText || '').slice(0, 80)
      });
    }
  });
  return {
    vw: w,
    docScroll: document.documentElement.scrollWidth,
    bodyScroll: document.body.scrollWidth,
    bad: bad.slice(0, 20)
  };
})()
```

3. **Known failure pattern.** Imported review pages can have wrappers such as `.sota-root`, `.sota-card`, `.sota-author-row`, `.sota-bread`, Elementor `.e-con-inner > div`, custom hero classes (`.gutf-hero`, `.guf-hero`), chip rows (`.guf-chips`), grids/cards (`summary-grid`, `review-grid`, `product-grid`, `calculator-grid`), and inline `table style="min-width:700px; display:block; overflow:auto"`. These can force 640–700px content inside a 390px viewport or create ultra-narrow text columns even after bad shortcode/schema strings are removed. On the 320px viewport, a table may not increase `documentElement.scrollWidth` if `overflow-x:hidden` is masking it; also scan for “skinny” readable text nodes below ~95px width.

4. **Hardened scoped CSS pattern.** Prefer scoped post-level CSS when a full rewrite is too risky. If editing post content is unsafe because PhastPress/REST may mangle CSS, inject at the Cloudflare Worker/edge HTML layer for only the affected URL(s) via the apex Worker’s WordPress HTML hardening branch. Keep it URL-scoped, not global.

Basic overflow hardfix:

```html
<style id="gutf-mobile-visual-hardfix">
html,body{overflow-x:hidden!important}
body.single-post table{max-width:100%!important;width:100%!important;min-width:0!important;table-layout:fixed!important;display:table!important}
body.single-post th,body.single-post td{white-space:normal!important;word-break:break-word!important}
.entry-content,.post-content,.content-area,.site-content,#primary,main,article{max-width:100%!important;box-sizing:border-box!important}
.elementor-location-single .e-con-inner>div,.sota-root,.sota-card,.sota-author-row,.sota-bread,.sota-badges,.sota-divider{width:100%!important;max-width:100%!important;min-width:0!important;box-sizing:border-box!important;overflow-wrap:anywhere!important}
.sota-author-row,.sota-badges,.review-card,.product-card,.quick-pick-card{display:flex;flex-wrap:wrap;gap:10px}
img,video,iframe{max-width:100%!important;height:auto!important}
@media(max-width:760px){
  body{width:100%!important}
  .elementor-location-single .e-con-inner>div{width:100%!important;max-width:100%!important;min-width:0!important;overflow-x:hidden!important}
  body.single-post table{max-width:100%!important;width:100%!important;min-width:0!important;table-layout:fixed!important;display:table!important}
  body.single-post th,body.single-post td{white-space:normal!important;word-break:break-word!important;padding:8px!important;font-size:12px!important}
  .sota-root{padding-left:16px!important;padding-right:16px!important}
  .sota-card{padding:18px!important;border-radius:18px!important}
  .sota-author-row,.sota-badges,.review-card,.product-card,.quick-pick-card{display:block!important}
  a.button,.wp-block-button__link,.cta-button{display:block!important;width:100%!important;text-align:center!important;box-sizing:border-box!important}
}
</style>
```

When tables are still producing skinny columns at 320px, convert tables to stacked mobile cards instead of horizontal scroll. This is often better for user perception on GearUpToFit review/calculator pages:

```css
@media(max-width:760px){
  body.single-post table,
  body.single-post thead,
  body.single-post tbody,
  body.single-post tr,
  body.single-post th,
  body.single-post td{
    display:block!important;
    width:100%!important;
    max-width:100%!important;
    min-width:0!important;
  }
  body.single-post table{overflow:visible!important;table-layout:auto!important;border-spacing:0!important}
  body.single-post thead{position:absolute!important;left:-9999px!important;top:auto!important;width:1px!important;height:1px!important;overflow:hidden!important}
  body.single-post tr{border:1px solid rgba(15,23,42,.12)!important;border-radius:14px!important;margin:0 0 12px!important;padding:8px!important;background:#fff!important}
  body.single-post th,body.single-post td{padding:8px 10px!important;font-size:13px!important;line-height:1.45!important;text-align:left!important;white-space:normal!important;overflow-wrap:anywhere!important}
}
@media(max-width:360px){body.single-post th,body.single-post td{min-width:0!important;font-size:12px!important;padding:8px!important}}
```

For custom hero/chip/card/grid failures, add URL-scoped rules like:

```css
@media(max-width:760px){
  body.single-post .gutf-hero,body.single-post .guf-hero,
  body.single-post [class*="hero"],body.single-post [class*="summary"],body.single-post [class*="card"],body.single-post [class*="grid"]{
    max-width:100%!important;min-width:0!important;grid-template-columns:1fr!important;flex-direction:column!important;overflow-wrap:anywhere!important;
  }
  body.single-post .gutf-hero .subtitle,body.single-post .gutf-hero .meta,
  body.single-post .guf-hero .guf-sub,body.single-post .guf-chips,body.single-post .guf-chip{
    width:100%!important;max-width:100%!important;min-width:0!important;display:block!important;line-height:1.55!important;text-align:left!important;white-space:normal!important;
  }
  body.single-post .guf-chips{display:grid!important;grid-template-columns:1fr!important;gap:10px!important}
}
```


5. **Clean invalid imported markup before CSS.** Remove broken visible JSON-LD blocks, `Replace COMPARISON_VIDEO_ID`, and invalid wrapper residue such as `</script></p>` / paragraphs around block elements; otherwise CSS fixes may be overridden or create phantom layout artifacts.

6. **Cache verification.** Purge Cloudflare, then verify both normal URL and cache-busted URL. If PhastPress/minification persists, use `?phast=-phast` to distinguish source HTML from optimizer output, but final pass must verify the normal URL.

## Success criteria

- Mobile DOM probe returns no meaningful `bad` overflow elements at both ~390px and 320px.
- `documentElement.scrollWidth` **and** `body.scrollWidth` are at or below viewport width, not 640–1000px. Do not accept a page just because `documentElement.scrollWidth` is clean; `body.scrollWidth` can still reveal masked table/grid overflow.
- Skinny-text probe returns zero meaningful narrow content blocks on mobile; especially no hero subtitle/meta/chips, dek paragraphs, CTA rows, or table cells under ~95px wide.
- Browser verification scrolls lazy-loaded article images into view and confirms product-box images have nonzero `naturalWidth/naturalHeight`. Supporting old AVIF/gravatar images may be separately noted, but product-box images are the monetization-critical acceptance gate.
- Browser/vision inspection confirms the blog post is readable on 390px mobile and desktop.
- Verify both the normal clean URL and a cache-busted URL after purge. The hardfix marker/style should be present in both surfaces when edge injection is used.
- Bad-string checks still pass: no visible `[bulkimporter_image`, `[wpbread]`, `Replace COMPARISON_VIDEO_ID`, `origin.gearuptofit.com`, or visible JSON-LD outside scripts.

## Communication rule for this user

When the user reports a visual regression after a claimed fix, stop summarizing string checks. Immediately run rendered visual/mobile verification, patch, purge, and report only concrete evidence: viewport width, scroll width, overflow count, and whether desktop/mobile are readable.