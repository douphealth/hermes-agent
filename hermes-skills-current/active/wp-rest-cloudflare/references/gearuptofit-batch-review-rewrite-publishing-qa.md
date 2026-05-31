# GearUpToFit batch review rewrite publishing + rendered QA lessons

Use this reference when publishing a batch of full review-post rewrites on GearUpToFit that include custom HTML, product boxes, Amazon affiliate CTAs, product images, comparison tables, and mobile-specific layout risk.

## Durable workflow additions

1. **Treat product-image hosting as a publishing gate.**
   - Do not leave fragile third-party product image URLs in final post HTML when they come from brand newsrooms, CDN URLs with signed/truncated query strings, or pages that block bot/hotlink access.
   - Fetch/verify each product image, upload it into the GearUpToFit media library via WordPress XML-RPC/REST, then replace the post HTML with the local `gearuptofit.com/wp-content/uploads/...` URL.
   - Keep a product-image upload map artifact with source URL -> local media URL.

2. **Repair blocked/fallback image sources before publishing.**
   - If a source image returns 403/404, find a verified equivalent official/news/product image, validate `200 image/*`, upload locally, and use the local media URL.
   - For GearUpToFit review product modules, final acceptance is not just `<img>` count: the product-box image must load in a rendered browser with nonzero `naturalWidth/naturalHeight`.

3. **Normalize Amazon affiliate links during sanitize.**
   - GearUpToFit tag: `papalex-20`.
   - Every Amazon CTA must contain the tag and use `rel="nofollow sponsored noopener"` plus `target="_blank"`.
   - Fix source-file placeholder/censor artifacts in Amazon search queries before publish; do not allow partially redacted query strings into live CTAs.

4. **Remove body schema/scripts from imported review content.**
   - Full rewrites may contain Article/Product/Review/FAQ/Video/Breadcrumb JSON-LD inside the post body.
   - Remove body `<script type="application/ld+json">` blocks before publishing to prevent visible-schema leakage and fake price/rating risk. Let the theme/SEO plugin own head schema unless a separate, controlled schema workflow is in scope.

5. **Create/update safely, then verify stored state.**
   - Resolve slugs through WP REST first; update existing posts and create missing posts only after confirming no slug duplicate/redirect issue.
   - Back up existing post object and custom fields before edits.
   - After XML-RPC/REST write, re-fetch stored post and require: deployment marker present, expected image count, Amazon link count, affiliate tag, no body H1, no body scripts.

6. **Cloudflare cache: exact purge may not be enough.**
   - Verify normal URLs and cache-busted URLs after purge.
   - If normal URLs still show stale bodies while cache-busted URLs are correct, escalate to `purge_everything` for the zone, then re-check normal URLs.
   - Record `cf-cache-status` in the raw QA artifact.

7. **Rendered QA must fail on both `documentElement` and `body` overflow.**
   - A page can have `document.documentElement.scrollWidth == viewport` while `document.body.scrollWidth` is ~1000px because overflow is masked. Treat either as a failure.
   - Run mobile 390px, mobile 320px, and desktop 1440px.
   - Check: article text length, one H1, product box count, Amazon count/tag/rel, product images natural dimensions, `documentElement.scrollWidth`, `body.scrollWidth`, overflow elements, and skinny text blocks.

8. **Common rendered failures from custom review HTML.**
   - Comparison tables with `min-width` cause mobile overflow.
   - Intro/dek/meta/chip rows can become skinny unreadable text columns.
   - Product CTAs can overflow if kept inline/fixed width.
   - Fix with scoped post-level CSS, not global theme CSS, unless many pages share the same template and the user approves global changes.

## Final scoped CSS hardfix pattern

Use this as a starting point inside the post's existing scoped `<style>` block when rendered QA shows mobile overflow or skinny text in `.gutf-ready-review`:

```css
/* Hermes final rendered mobile hardfix */
.gutf-ready-review,.gutf-ready-review *{box-sizing:border-box}
.gutf-ready-review{width:100%;max-width:100%;overflow-x:hidden;overflow-wrap:anywhere}
.gutf-ready-review img{max-width:100%!important;height:auto!important}
.gutf-ready-review .gutf-product-box img{object-fit:contain;max-height:280px}
.gutf-ready-review iframe,.gutf-ready-review video{max-width:100%!important}
.gutf-ready-review .gutf-btn{white-space:normal;text-align:center;max-width:100%}
.gutf-ready-review .gutf-compare{max-width:100%;overflow-x:auto;-webkit-overflow-scrolling:touch}
@media(max-width:760px){
  .gutf-ready-review{padding-left:14px!important;padding-right:14px!important;overflow-x:hidden!important}
  .gutf-ready-review .gutf-hero,.gutf-ready-review .gutf-layout,.gutf-ready-review .gutf-scorebar,.gutf-ready-review .gutf-procon,.gutf-ready-review .gutf-gallery,.gutf-ready-review .gutf-related,.gutf-ready-review .gutf-product-box,.gutf-ready-review [class*="grid"]{display:grid!important;grid-template-columns:1fr!important;max-width:100%!important;min-width:0!important;width:100%!important;gap:14px!important}
  .gutf-ready-review .gutf-dek,.gutf-ready-review .gutf-meta,.gutf-ready-review .gutf-chip,.gutf-ready-review .gutf-btns,.gutf-ready-review .gutf-btn{width:100%!important;max-width:100%!important;min-width:0!important;line-height:1.55!important;text-align:left!important;white-space:normal!important;display:block!important}
  .gutf-ready-review .gutf-btn{text-align:center!important;display:flex!important;justify-content:center!important;align-items:center!important}
  .gutf-ready-review .gutf-product-box{padding:14px!important;border-radius:22px!important}
  .gutf-ready-review .gutf-card{padding:15px!important;border-radius:20px!important}
  .gutf-ready-review .gutf-product-box img{max-height:230px;width:100%;object-fit:contain}
  .gutf-ready-review table,.gutf-ready-review thead,.gutf-ready-review tbody,.gutf-ready-review tr,.gutf-ready-review th,.gutf-ready-review td{display:block!important;width:100%!important;max-width:100%!important;min-width:0!important;box-sizing:border-box!important;white-space:normal!important;overflow-wrap:anywhere!important;word-break:normal!important}
  .gutf-ready-review table{overflow:visible!important;table-layout:auto!important;border-spacing:0!important}
  .gutf-ready-review thead{position:absolute!important;left:-9999px!important;top:auto!important;width:1px!important;height:1px!important;overflow:hidden!important}
  .gutf-ready-review tr{border:1px solid rgba(15,23,42,.12)!important;border-radius:14px!important;margin:0 0 12px!important;padding:8px!important;background:#fff!important}
  .gutf-ready-review th,.gutf-ready-review td{padding:8px 10px!important;font-size:13px!important;line-height:1.45!important;text-align:left!important;border-bottom:0!important}
  .gutf-ready-review .gutf-compare table{min-width:0!important}
}
@media(max-width:360px){.gutf-ready-review{padding-left:10px!important;padding-right:10px!important}.gutf-ready-review th,.gutf-ready-review td{font-size:12px!important;padding:8px!important}}
```

## Evidence artifacts to save per batch

- `publish-results.json` — post IDs, created/updated status, stored marker/image/Amazon counts, uploaded media map.
- `raw-public-qa-after-purge.json` — normal + cache-busted raw checks.
- `rendered-visual-qa-final.json` — browser viewport checks and failures.
- `screenshots/` + `screenshot-manifest.json` — desktop and mobile screenshots for each URL.
