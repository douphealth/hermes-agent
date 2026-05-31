# Amazon Affiliate Product Box Live Audit + QA

Use this when auditing or repairing existing Amazon affiliate product boxes in WordPress posts via REST, especially on GearUpToFit-style custom HTML modules.

## Proven production workflow

1. Fetch target posts/pages via REST with `context=edit` and back up each full object JSON before writing.
2. Extract from the **unescaped/rendered content**, not raw JSON text. WordPress REST JSON escapes URLs as `https:\/\/...`; naive regex over the raw response can miss or misclassify Amazon links/images.
3. Normalize affiliate product links to direct ASIN URLs:
   - `https://www.amazon.com/dp/ASIN?tag=<confirmed-tag>`
   - GearUpToFit confirmed tag: `papalex-20`.
4. Verify every ASIN/product URL and image URL independently:
   - Amazon product links: accept live `200` or Amazon geo/session `302` redirects; reject clear `404` / homepage-only redirects.
   - Amazon CDN images: require `200` and nonzero byte size from `https://m.media-amazon.com/images/I/...`.
5. Replace dead ASINs and image hashes only with validated product/image pairs. Do not derive CDN image hashes from ASINs.
6. Re-save via WordPress REST using `POST` + `X-HTTP-Method-Override: PUT` when Cloudflare/WAF may block direct `PUT`.
7. Re-fetch live public pages after the write and run two verification layers:
   - HTTP/content audit: link count, image count, tag check, ASIN statuses, image statuses/sizes.
   - Browser render audit: mobile and desktop viewport, count rendered Amazon anchors/images, ensure images have nonzero `naturalWidth`/`naturalHeight`, and catch layout/render problems raw HTML cannot see.

## Extraction notes

Product boxes may be custom `<!-- wp:html -->` blocks. Do not assume one class name; GearUpToFit has used variants such as `.gutf-products`, `.gutf-prods`, `.gutf-product-card`, and related card wrappers. Search for both Amazon URLs and site-specific wrapper prefixes.

When extracting from REST responses:

```python
obj = response.json()
content = obj.get('content', {}).get('raw') or obj.get('content', {}).get('rendered', '')
# If working with raw response text or serialized JSON, unescape before URL regexes.
content = content.replace('\\/', '/')
```

## Validation standards

- Product links must contain the confirmed affiliate tag.
- CTA anchors should use `rel="sponsored nofollow noopener"` where applicable.
- Image URLs must be Amazon CDN URLs (`m.media-amazon.com/images/I/...`) and load with nonzero bytes.
- Image count should normally match product-link count inside the scoped module.
- **Full-page content integrity is mandatory.** Do not call an affiliate repair complete just because Amazon links/images pass. Before and after each write, compare `content.raw` length, article text length, H2/H3 counts, paragraph/list/table counts, and topic markers. A product-box-only page with valid Amazon links is still a production failure.
- Browser verification must inspect the article body, not only the product boxes: confirm the page is not blank/thin, has the expected H1/article text, and contains substantial visible content around the affiliate module.
- Report `0 problems` only after both HTTP-level and browser-level checks pass **and** content-integrity checks show the original article was not accidentally removed or collapsed.

## Browser fallback

If Python Playwright is unavailable, use Node/npm locally:

```bash
mkdir -p /tmp/gutf-render-check
cd /tmp/gutf-render-check
npm init -y >/dev/null 2>&1
npm install playwright-chromium
```

Then run a small Chromium script over the audited URL list twice: once with a mobile viewport/user agent and once with desktop. Save JSON artifacts under `/tmp` for proof.

## Amazon response interpretation

Amazon often redirects or blocks automated clients because of geo/session/bot handling.

- `200`: acceptable product page response.
- `302`: acceptable when the ASIN is direct and the redirect is Amazon session/geo handling.
- `404`: broken/dead ASIN; replace.
- `503`/challenge: verify in browser before deciding.
- Image CDN check is stricter: require `200` and nonzero bytes.

## Blank/thin page emergency recovery after affiliate repairs

If a user reports that a URL became blank or lost content after an affiliate/product-box pass, treat it as an active production incident and repair first.

1. Open the live page in a browser immediately and check visible article text, not just HTTP `200`.
2. Fetch the exact REST object by high-confidence post ID (`postid-*`, shortlink, REST link, or known ID) with `context=edit`; save a full backup before any new write.
3. Check `/wp-json/wp/v2/posts/{id}/revisions?context=edit` and any local `/tmp` backups from the previous script. Compare each revision for `raw_len`, visible text length, H2/H3 counts, paragraph/list counts, and Amazon count.
4. If revisions/backups are already thin because the earlier script overwrote the article, do not restore the thin revision. Rebuild a concise, topic-faithful article body and preserve the currently verified product box/ASIN/image pairs.
5. Deploy via REST (`POST` + `X-HTTP-Method-Override: PUT`), then verify both plain and cache-busted live URLs.
6. Browser console proof should include: article text length, H1 text, H2 count, Amazon links, Amazon images with nonzero `naturalWidth`/`naturalHeight`, and `bodyBlank: false`.
7. In the final report, acknowledge the page was restored and give concrete verification counts; do not over-explain the mistake unless the user asks.

## Batch rewrite + affiliate module pitfalls

When the source document contains many full post rewrites with Amazon placeholder tokens, the affiliate QA must be part of the publishing gate, not a post-hoc string check.

- Resolve placeholders into explicit `{asin,title,image,url}` records and save a product map artifact before writing. Each URL must be a direct Amazon `/dp/ASIN/?tag=<confirmed-tag>` link and each image must be a real `m.media-amazon.com/images/I/...` asset. Do not accept weak/fallback matches just because they return an image; review relevance before calling the module final.
- Enforce **one monetization module per intended placement**. Raw counts such as `amazon tag appears` can hide repeated product modules caused by import wrappers, TOC duplication, or appended rendered fragments. Verify scoped module count, product-card count, and unique ASIN count per post.
- If public HTML is unusually large for a normal article, or `.amazon-products`/site-specific product wrappers appear many times, stop the batch and inspect for duplicated modules before continuing.
- Do not treat `img total = 0` from a bad regex as proof images are absent; confirm with a broader `<img\b` probe, product-wrapper DOM selectors, and browser-rendered `naturalWidth`/`naturalHeight` after scrolling lazy-loaded cards into view.
- For source-file rewrites, remove body JSON-LD/scripts and publisher-only notes before adding product cards; visible-schema checks must strip legitimate `<script>`/`<style>` blocks first, then search remaining body text for `@context`/`schema.org`.
- Product box CSS should be self-contained and mobile-safe: inline styles or scoped classes, `object-fit:contain`, bounded media boxes, no fixed-width table/card layouts, and CTAs with `rel="sponsored nofollow noopener"`.
- For GearUpToFit review rewrites, do not leave fragile third-party product images in the live module when they come from brand newsrooms, signed/truncated CDN URLs, or sources that 403/404 under automated fetch. Validate `200 image/*`, upload the product image into the GearUpToFit media library, replace the article HTML with the local media URL, and save a source->local upload map artifact.
- If the source file includes placeholder/censored Amazon query artifacts, repair them before publish; every live Amazon CTA must contain the confirmed tag (`papalex-20`) and must not include redacted query fragments.

## XML-RPC timeout and slug creation caution

Some Cloudflare/LiteSpeed WordPress origins complete an XML-RPC `editPost`/`newPost` write but fail to return before the client timeout. The durable lesson is not “XML-RPC is broken”; it is to verify state before retrying.

1. Use a short timeout around the write.
2. On timeout, wait briefly, then re-fetch by known post ID or by slug via REST/XML-RPC.
3. If the expected unique marker/content changed, treat the write as completed and continue verification.
4. If the post did not exist and `newPost` timed out, resolve the slug carefully before retrying. Check for `-2` duplicates, 301 loops, stale redirects, and existing near-match titles. Do not blindly rerun `newPost`, because duplicate posts or redirect loops can be created.
5. Only batch-create missing posts after the first missing-slug case has been manually resolved and verified publicly.

## GearUpToFit production lesson

A 23-page GearUpToFit repair used this pattern successfully:
- 16 pages patched via REST, 7 unchanged, 0 REST failures.
- Final audit: 62 Amazon links, 62 Amazon images, 34 unique ASINs/images, 0 problems.
- Desktop and mobile Chromium render checks found 0 bad pages.

Keep secret credentials out of all reports and artifacts; read approved local secret files only at execution time and redact values in output.