# GearUpToFit Worker-Level Index Consolidation Pattern

Use this when GearUpToFit has duplicate/indexable brand, hub, or legacy URLs that should consolidate without editing WordPress content.

## Trigger
- Public crawl shows competing 200/indexable pages for the same intent, especially broad start pages or duplicate hubs.
- Yoast/page sitemap still lists a URL that is being redirected or should stop being indexed.
- WordPress/Yoast old-slug behavior may create redirect chains unless the Cloudflare Worker catches exact paths first.

## Production-safe sequence
1. Capture pre-change public evidence for each target URL:
   - `status`
   - `Location`
   - `cf-cache-status`
   - title/H1/canonical when HTML is returned
   - sitemap presence in `page-sitemap.xml`, `sitemap.xml`, and `sitemap_index.xml`
2. Backup the active Cloudflare Worker before edits.
   - Cloudflare API `GET /accounts/{account_id}/workers/scripts/{script}` can return a multipart body. Preserve the raw backup, then extract the `worker.js` part before patching.
3. Add exact `REDIRECTS_301` entries only; avoid wildcard redirects for SEO consolidation.
   - Include both slash and non-slash forms when both can be requested.
4. If a redirected URL remains in public sitemap output and WordPress/Yoast cannot be safely edited immediately, add a narrow Worker sitemap XML filter.
   - Filter only exact `<url><loc>...</loc>...</url>` blocks for known redirected URLs.
   - Return `application/xml; charset=utf-8` and verify XML parses.
5. Validate locally/syntactically before upload.
   - For module-style Worker code, `node --check worker.js` catches syntax errors.
6. Upload Worker via multipart module upload.
   - Metadata must include `{"main_module":"worker.js"}`.
   - Raw `application/javascript` upload can fail on module scripts.
7. Purge Cloudflare exact URLs after deploy.
8. Verify:
   - one-hop redirect chain (`history == [301]`)
   - final destination `200`
   - destination canonical unchanged
   - sitemap XML parses and does not include redirected URLs
   - normal URL and cache-hit state after purge
9. Write a changelog with backup path, changed paths, validation evidence, and rollback.

## Example redirects from the 2026-05 cleanup
Exact redirects added at Worker level:
- `/home-gearuptofit/` -> `/`
- `/home-gearuptofit` -> `/`
- `/expert-guides-honest-reviews-real-results/` -> `/`
- `/expert-guides-honest-reviews-real-results` -> `/`
- `/app/` -> `/category/running/`
- `/app` -> `/category/running/`

## Rollback
1. Restore the raw pre-change Worker backup or remove the exact redirect/filter entries.
2. Redeploy Worker.
3. Purge the same exact URLs.
4. Verify old paths behave as intended and sitemap output is expected.

## Pitfalls
- Do not call a redirect done until you verify redirect chain length; a WordPress-origin redirect after Worker redirect can create two-hop chains.
- Do not rely only on normal browser fetches after cache changes; verify sitemap XML parse and cache state.
- Do not use broad sitemap regexes. Restrict removal to exact known URL blocks.
- Do not edit WordPress content/database for duplicate URL consolidation when an exact Worker redirect solves the index issue with lower blast radius.