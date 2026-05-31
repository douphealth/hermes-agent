# Multi-Post Rewrite Source-File Publishing Pattern — 2026-05-29

Use when the user provides one document containing several rewritten WordPress posts and asks for precise SOTA application.

## Recommended workflow
1. Parse the source file into per-post records: target URL, slug, title/H1, meta title, meta description, raw HTML.
2. Resolve existing post IDs via public REST; use authenticated REST only when needed and reliable.
3. Back up each original post body/metadata before editing.
4. Use XML-RPC against the origin IP with the public `Host` header when the rewrite contains `<style>`, rich article wrappers, tables, or other markup REST may sanitize.
5. Sanitize production copy before write:
   - remove publisher/editorial notes and media placeholders;
   - remove duplicate/body H1s unless live output proves the theme emits none;
   - remove unapproved dynamic video-search embeds;
   - remove body JSON-LD if the stack visibly escapes scripts;
   - preserve affiliate disclosures and tags.
6. Update post title/status/body and the common SEO meta families when available.
7. Purge Cloudflare after writes; if exact purges do not clear stale output, use purge-everything and recheck after a few seconds.
8. Verify every live public URL, not only stored bodies.

## Verification contract
For each URL verify:
- HTTP 200 and no WordPress critical error marker.
- Canonical matches the target URL.
- Premium wrapper/article marker exists.
- One effective primary heading exists. Count theme `<h1>` plus verified accessible primary headings when a site filter strips/demotes body `<h1>`.
- No duplicate body H1 inside the custom article wrapper.
- No visible raw CSS after `</style>`.
- No visible schema leakage after stripping real `<script>` blocks.
- No leftover publisher artifacts (`Editorial note`, `Publisher note`, media-library instructions, self-referential rewrite text).
- Affiliate disclosure and expected tag are present on monetized posts.

## Pitfalls
- Public `<title>` can remain stale even after post/meta fields update; report this as a head-layer/cache/template caveat unless a safe SEO-plugin regeneration path is available.
- MU-plugin head normalizers are not safe by default. A fatal MU plugin can block admin-ajax and WP File Manager rollback; require lint plus out-of-band file access before deploy.
- Some content filters remove `aria-level` but preserve `role="heading"`; if using accessible fallback headings, inspect rendered HTML and adapt the verifier to the actual output.
