# AMFS batch rewrite head/cache + visual QA lessons — 2026-05-31

Use this when deploying many rewritten posts to affiliatemarketingforsuccess.com or similar WordPress sites with Yoast, Code Snippets head overrides, Cloudflare, and Seraphinite Accelerator.

## What worked

- Parse the combined source into explicit per-post records before publishing: post number, target URL, title/H1, meta description, body HTML, images, and schema/script count.
- Resolve existing post IDs by public REST slug first; if slug lookup fails but the public URL is 200, extract the true post ID from the live body/article classes (`postid-123`, `id="post-123"`). AMFS may have malformed historical slugs while the canonical URL still works.
- Back up every target with XML-RPC `metaWeblog.getPost` before any write.
- Publish rich rewrites via origin XML-RPC, not REST, when the body contains `<style>`, tables, responsive wrappers, iframes, or other markup REST may sanitize.
- Strip imported/body `<h1>` from post bodies so Kadence/theme title remains the single public H1.
- Strip body JSON-LD/scripts during batch imports unless the site is proven to preserve scripts safely without visible leakage. Let Yoast/theme handle schema or add schema through a safer head layer later.
- Update all active title/meta families together: Yoast, Rank Math, `kk_seo_*`, `wds_*`, `metabox_post_*`, and excerpt.

## Critical AMFS pitfall: public head can be stale while stored/Yoast REST is correct

On AMFS, XML-RPC stored custom fields and `/wp-json/wp/v2/posts/{id}` / Yoast REST head can show the new title/meta, while public raw HTML still emits older `<title>`, description, `og:*`, or `twitter:*` values. Causes can include active Code Snippets head overrides, legacy title patches, Seraphinite/page cache, or later output buffers.

Do not claim metadata is fixed from stored fields alone. Verify all surfaces:

1. Stored XML-RPC/custom fields.
2. Yoast REST `yoast_head_json` or `/yoast/v1/get_head?url=...`.
3. Public raw HTML on the normal URL after WordPress/Seraphinite + Cloudflare purge.
4. Public raw HTML on a cache-busted URL after purge.

If only public head is stale:

- Inspect active Code Snippets for head/title override patches before adding another override.
- Prefer patching/disabling the stale scoped override over stacking a new one.
- If a temporary safety override is needed, make it URL/post-ID scoped only, lint/validate the PHP where possible, and verify the marker appears in public HTML after cache purge.
- A created Code Snippets snippet can be `active=true` in the snippets API but still not affect public output if cached HTML is served or another later buffer rewrites the head. Treat snippet activation as setup proof, not public proof.

## Cache clearing sequence

After publishing and metadata/head changes:

1. Purge Cloudflare exact URLs.
2. Clear Seraphinite Accelerator exact URI cache from wp-admin origin session.
   - Load `admin.php?page=seraph_accel_manage`.
   - Extract `CacheOp(this, TYPE, "NONCE")` values.
   - For exact URL cache removal, use the nonce associated with type `2` if present.
   - Call `admin-ajax.php?action=seraph_accel_api&fn=CacheOpBegin&type=uri&op=2&uri=/path/&v=&_wpnonce=NONCE`.
   - A response body of `0` can still mean the operation was accepted; verify by refetching normal + cache-busted public HTML.
3. Re-purge Cloudflare exact URLs.
4. Recheck public raw HTML; do not stop at API/storage success.

## Verification contract for AMFS batch rewrites

For every target URL, produce a compact JSON/CSV artifact with:

- HTTP 200 and no critical-error marker.
- Canonical equals intended URL.
- Public `<title>` and meta description equal the intended source, not stale generated claims.
- Exactly one public H1.
- Imported `.amfs-post` body has zero body H1s.
- Article wrapper exists and has substantial length.
- No visible raw CSS after stripping real `<style>` blocks.
- No visible schema leakage after stripping real `<script>` blocks.
- No publisher/editorial artifacts such as `Recommended internal links`, `Publisher note`, `Implementation note` inside the edited article body. Scope checks to the article body when possible; AMFS theme/wrapper text can cause false positives.
- Expected images are present in the article body; use robust article scoping, not a regex that stops at the first nested `</article>` or wrapper boundary.
- Rendered desktop and mobile QA: no horizontal overflow, readable layout, images load with nonzero natural dimensions after scrolling lazy-loaded images into view, no duplicate title stack, no code leakage.

## Reporting rule

If tool/runtime limits stop before desktop/mobile browser QA, report the deployment as partial: content stored + public body verified, but final rendered visual QA remains pending. Do not call the batch “perfect” until public raw head and rendered mobile/desktop checks pass for all URLs.
