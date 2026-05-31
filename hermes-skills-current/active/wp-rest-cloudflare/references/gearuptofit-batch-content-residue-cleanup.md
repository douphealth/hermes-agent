# GearUpToFit batch content-residue cleanup pattern

Use this when the user gives a list of WordPress URLs with visible broken template residue, shortcode text, visible JSON-LD, origin-domain contamination, or stale SEO titles and demands fast reliable cleanup.

## Efficient workflow

1. **Batch first, do not manually inspect every page in the browser.** Build one Python script that:
   - maps URLs to post IDs via `wp-json/wp/v2/posts?slug=<slug>&context=edit`;
   - supports `POST_ID_OVERRIDE` for renamed/canonical-slug mismatches;
   - reads raw content with REST `context=edit`;
   - applies conservative regex cleanup;
   - writes through XML-RPC to `http://104.168.100.41/xmlrpc.php` with `Host: gearuptofit.com`;
   - purges Cloudflare once after the batch;
   - verifies every URL with cache-busting query params.

2. **Remove only explicit residue unless doing a full rewrite.** Safe batch targets:
   - `[bulkimporter_image ...]`, including HTML-entity curly quotes such as `id=&#8217;2&#8242;`;
   - `[wpbread]`, `[last_modified_date]`;
   - `Replace COMPARISON_VIDEO_ID`;
   - `origin.gearuptofit.com` host references, normalized to `gearuptofit.com`;
   - visible JSON-LD fragments outside `<script type="application/ld+json">`.

3. **BulkImporter shortcode regex must handle wrappers and entity quotes.** Use patterns like:

```python
content = re.sub(r'\s*<div[^>]*>\s*\[bulkimporter_image[^\]]*\]\s*</div>\s*', '\n', content, flags=re.I)
content = re.sub(r'\s*<span[^>]*>\s*\[bulkimporter_image[^\]]*\]\s*</span>\s*', ' ', content, flags=re.I)
content = re.sub(r'\s*\[bulkimporter_image[^\]]*\]\s*', ' ', content, flags=re.I)
```

4. **Visible schema check must ignore real scripts.** Verify with:

```python
body = re.sub(r'<script[\s\S]*?</script>', '', html, flags=re.I)
visible_schema = '@context' in body and 'schema.org' in body
```

5. **Canonical slug mismatch pattern.** If a listed URL is 404 but search/REST finds the intended post under an old slug, update `wp_slug` via XML-RPC and re-verify the listed URL returns `200`.

6. **SEO title cleanup.** If live `<title>` differs from REST post title, inspect XML-RPC `custom_fields` for keys such as `_yoast_wpseo_title`, `rank_math_title`, `kk_seo_title`, `metabox_post_title`, `wds_title`, and update them with a concise descriptive title. Update `_yoast_wpseo_metadesc` / `rank_math_description` when available.

7. **Mobile layout guard for fragile custom review pages is not enough by itself.** Prefer a small scoped guard over a full rewrite when wrappers exist, but always verify with rendered mobile + desktop checks. If the user reports visual distortion/readability problems, follow `references/gearuptofit-visual-layout-verification.md` instead of relying on string checks.

```html
<style id="gutf-layout-guard">
.gutf-review-card,.review-card,.product-card,.quick-pick-card{display:block;max-width:100%;overflow-wrap:anywhere}
.gutf-comparison-table,.comparison-table,table{width:100%;max-width:100%;overflow-x:auto}
.gutf-comparison-table table{min-width:680px}.review-rating,.star-rating{white-space:nowrap;letter-spacing:.04em}
@media(max-width:760px){.gutf-review-card,.review-card,.product-card{display:block!important}.gutf-comparison-table,.comparison-table{overflow-x:auto;-webkit-overflow-scrolling:touch}}
</style>
```

## Verification contract

For every URL, report compactly:

- HTTP status and final URL;
- live `<title>`;
- count map for bad strings: `Replace COMPARISON_VIDEO_ID`, `[wpbread]`, `[last_modified_date]`, `[bulkimporter_image`, `origin.gearuptofit.com`, placeholder image URLs;
- visible schema heuristic after stripping scripts;
- when any request is about visual/mobile/layout quality: rendered mobile viewport width, `documentElement.scrollWidth`, overflow-element count, and a desktop/mobile readability pass;
- `FAILS 0` only if all URLs are `200`, all bad counts are zero, and required rendered layout checks pass.

## User preference for this class

When the user gives a batch of WordPress cleanup URLs and asks for speed/efficiency, avoid verbose per-page narrative while working. Use batch scripts, single purge, compact verification, and final answer with only actions taken + evidence.