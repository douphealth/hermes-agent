# WordPress REST-safe mobile commercial post redesign

Use this when publishing/redesigning WordPress commercial affiliate/review posts through REST/API where wp-admin may be behind Cloudflare and post content must be visually perfect on mobile.

## Failure pattern captured

- WordPress REST sanitizers may strip `<style>` / `@media` blocks from post content.
- When the stripped CSS remains as text, the live article shows raw CSS at the top and the design collapses.
- Passing raw-string checks is not enough: a page can have no obvious shortcode residue but still be unusable on mobile due to overflow, skinny product cards, fixed tables, or theme-injected images/gaps.

## Safer build pattern

1. **Prefer XML-RPC for full HTML if available** when the design needs `<style>` or media queries.
2. **If using REST**, make the post body REST-safe:
   - no `<style>` blocks
   - no `@media` rules
   - no external CSS dependency inside post content
   - use inline `style` attributes and fluid CSS values (`clamp()`, `minmax(min(100%, ...))`, `max-width:100%`, `box-sizing:border-box`)
3. **Avoid fragile tables on mobile.** Use stacked comparison cards instead of wide tables for product comparisons.
4. **Product cards:** avoid left-number + content flex rows that leave only a tiny text column at 320px. Stack the rank badge above the title/content or use CSS grid with full-width mobile behavior.
5. **Headings in theme-sensitive posts:** if semantic `<h2>/<h3>` patterns trigger theme/plugin image injection, big blank gaps, or related-media placement inside the article, use `<div role="heading" aria-level="2/3">` for styled in-article section headings while preserving the real WordPress post title as the single `<h1>`.
6. **Do not inject body H1 duplicates.** Let the theme/post title own the `<h1>`; style the in-block hero title as a div/paragraph.
7. **Purge edge cache after updates** and verify the normal URL, not only cache-busted variants.

## Mobile verification contract

Run rendered DOM checks at **390px and 320px** before claiming done:

```js
(async () => {
  const urls = ['/target-post/'];
  const results = {};
  for (const width of [390, 320]) {
    results[width] = {};
    for (const path of urls) {
      const iframe = document.createElement('iframe');
      iframe.style.cssText = `width:${width}px;height:1400px;border:0;position:absolute;left:-9999px;top:0;background:white`;
      iframe.src = location.origin + path + '?qa=' + Date.now();
      document.body.appendChild(iframe);
      await new Promise(res => iframe.onload = res);
      await new Promise(r => setTimeout(r, 1200));
      const d = iframe.contentDocument, w = iframe.contentWindow;
      const bad = [];
      d.querySelectorAll('body *').forEach(el => {
        const r = el.getBoundingClientRect();
        const cs = w.getComputedStyle(el);
        if (r.width > width + 8 && cs.display !== 'none') bad.push({ tag: el.tagName, w: Math.round(r.width), text: (el.innerText || '').slice(0, 60) });
      });
      const skinny = [];
      d.querySelectorAll('p,li,[role="heading"],a').forEach(el => {
        const r = el.getBoundingClientRect();
        const txt = (el.innerText || '').trim();
        if (txt.length > 24 && r.width > 0 && r.width < 95) skinny.push({ tag: el.tagName, w: Math.round(r.width), text: txt.slice(0, 60) });
      });
      const text = d.body.innerText;
      results[width][path] = {
        viewport: w.innerWidth,
        docScroll: d.documentElement.scrollWidth,
        bodyScroll: d.body.scrollWidth,
        overflow: d.documentElement.scrollWidth > w.innerWidth + 2,
        badElements: bad.length,
        skinnyText: skinny.length,
        visibleCssLeak: text.includes('.mgg-post') || text.includes('--card:#fff') || text.includes('@media'),
        h1Count: d.querySelectorAll('h1').length,
        figuresInsideArticle: d.querySelector('article')?.querySelectorAll('figure').length ?? null
      };
      iframe.remove();
    }
  }
  return results;
})()
```

Pass criteria for premium mobile commercial posts:

- `overflow: false` at 320px and 390px
- `badElements: 0`
- `skinnyText: 0`
- `visibleCssLeak: false`
- `h1Count: 1`
- product/affiliate CTAs still present
- visual browser/vision check confirms no raw CSS/HTML, no blank inserted image gaps, no cramped cards

## Reporting

Report concrete viewport proof, not vibes:

- URL
- viewport width
- scroll width
- overflow yes/no
- skinny text count
- CSS/HTML leak yes/no
- H1 count
- cache purge result
