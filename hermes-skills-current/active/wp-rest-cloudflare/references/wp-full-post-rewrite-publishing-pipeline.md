# WordPress full-post rewrite publishing pipeline

Use this when the user provides rewritten HTML articles/posts and asks to replace existing WordPress posts one-by-one or in a batch, especially on Cloudflare-protected sites.

## Core pattern

1. **Start with one post before batch publishing.** The first post is the quality gate: prove the pipeline preserves layout, CSS, metadata, schema, links, media, and mobile readability before touching the rest.
2. **Map source file to existing post URL/post ID.** Use the slug and XML-RPC/REST discovery. Do not infer solely from filenames if the URL list is available.
3. **Back up the current post first.** Save raw XML-RPC/REST post response, including custom fields, before editing.
4. **Prefer XML-RPC for rich HTML rewrites.** REST sanitizers can strip `<style>`, `@media`, and scripts/JSON-LD or leave visible CSS. `metaWeblog.editPost` with CDATA preserves full HTML.
5. **Strip publisher-only planning sections before publish.** Rewrites may include editorial brief residue such as `Recommended internal links`. Do not publish these as body content. Remove sections whose headings indicate internal-link recommendations, content briefs, implementation notes, or publisher instructions while preserving reader-facing contextual/internal links already embedded in the article.
6. **Avoid duplicate H1s by removing body H1s, not just restyling them.** WordPress themes usually render the post title as the single page H1. If the rewrite includes an internal `<h1>` or a styled duplicate article title immediately under the theme title, remove it from the imported body. If a visual intro label is needed, use a short non-repetitive H2 such as `What readers should know first`; do not repeat the full SEO title under the theme H1.
7. **Update SEO custom fields, not just content.** Verify and update likely Yoast/RankMath/theme keys:
   - `_yoast_wpseo_title`, `_yoast_wpseo_metadesc`, `_yoast_wpseo_focuskw`
   - `_yoast_wpseo_opengraph-title`, `_yoast_wpseo_opengraph-description`
   - `_yoast_wpseo_twitter-title`, `_yoast_wpseo_twitter-description`
   - `rank_math_title`, `rank_math_description`, `rank_math_focus_keyword`
   - `rank_math_facebook_title`, `rank_math_facebook_description`
   - `rank_math_twitter_title`, `rank_math_twitter_description`
   - site/theme-specific keys such as `kk_seo_title`, `kk_seo_desc`, `wds_title`, `wds_description`, `metabox_post_title`, `metabox_post_description`, `_kad_post_title`, etc. when present. Some AMFS/Kadence/head-injector surfaces can use these for the visible theme H1 or pre-Yoast `<title>`/description even when the XML-RPC post title and Yoast/RankMath fields are correct.
7. **Do not blindly admin-save after XML-RPC rewrites.** On AMFS, automated `/wp-admin/post.php` form saves can re-submit stale edit-form title/meta values and overwrite freshly applied XML-RPC titles/excerpts. If admin-save is needed to regenerate indexables, first prove the edit form contains the new values or immediately re-publish via XML-RPC afterward.
8. **Verify live public HTML after publish.** Check the normal URL and a cache-busted URL.

## Verification contract for the first post

Reusable script: run `python scripts/wp-full-post-rewrite-verify.py URL...` from this skill directory, or copy it into the working directory, for the public-URL checks below.

For emergency cleanup after a bad publish, also use `references/wp-article-quality-rescue.md`.

Report evidence, not vibes:

- HTTP loads publicly without Cloudflare/challenge/login wall.
- `<title>` matches intended title.
- Meta description, OpenGraph description, and Twitter description match intended clean copy.
- Canonical is the target URL.
- Robots meta is not accidentally `noindex`.
- H1 count is exactly 1 unless the theme intentionally differs.
- Imported article/body H1 count is 0 for theme-rendered post templates.
- Publisher-only brief sections such as `Recommended internal links` are not visible in the rendered body.
- Article CSS is preserved but not visibly leaked. Strip `<style>` and `<script>` before searching for raw CSS/schema leaks.
- JSON-LD scripts are present when source contains schema; visible `@context`/`schema.org` outside scripts is a failure.
- Media assets and iframes return valid statuses/content types.
- Browser render is readable: no raw code, no huge horizontal overflow, no duplicate title stack, no collapsed content.
- For mobile-first rewrites, run a rendered mobile/desktop check before claiming SOTA.

## Editorial quality gate

When a rewrite is SEO/AEO-heavy, do not silently publish obvious machine-like repetition if the user asked for human quality. Preserve SEO intent but reduce repeated full-keyword headings during the batch when safe. Examples:

- Replace repeated full-title headings with `Quick Summary`, `What This Guide Covers`, `What readers should know first`, `Decision Framework`, `Best Fits`, or `FAQs`.
- Remove internal planning artifacts (`Recommended internal links`, editorial instructions, brief notes) rather than trying to make them reader-facing.
- Keep one exact-match title/H1 and natural variants elsewhere.
- Do not remove useful answer blocks, comparison tables, affiliate disclosures, schema, or CTAs.

### Hard fail: keyword-stuffing artifacts

Do not publish NeuronWriter/SEO term-padding as reader-facing content. Treat repeated blocks like `term: include this concept in your operating checklist...`, generic repeated headings (`Become An Affiliate Marketer`, `Affiliate Marketer`, `Beginner`) or mechanically generated “implementation notes” as a publish blocker. Remove the entire block and replace it with useful prose, a checklist, or examples that genuinely help the reader. Verify the exact bad phrase is absent from stored post body, raw public HTML, and rendered `document.body.innerText`.

### Internal links must be contextual, not only a bottom module

If asked to add internal links for topical authority/AI visibility, add links in the natural article body using rich contextual anchor text where the concepts are discussed. A styled “related resources” module is acceptable as a supplement, but it does not satisfy the request by itself. Verification should report: total article internal links, unique internal URLs, contextual inline paragraph links, related-module links, and HTTP status for each unique target.

### Duplicate-title pitfall

A visually large body H2 immediately repeating or paraphrasing the theme H1 still reads as a duplicate title even if it is not technically an `<h1>`. For WordPress post rewrites, prefer a short `Quick strategy brief:` paragraph or non-title intro below the theme H1 instead of another oversized hero headline.

## Batch publishing contract

After the first post passes, batch with the same guardrails instead of manually repeating pages:

1. Inventory every source file and resolve its canonical URL to the existing WordPress post ID from live HTML/REST/XML-RPC; fail closed on unresolved IDs.
2. If a slug is missing, do not immediately `newPost` in the batch. First check live redirects, `-2` duplicate slugs, near-match titles, canonical URLs, and sitemap/search results; resolve that one missing-slug case before creating anything.
3. For each post, write a sanitized production-safe source artifact and save a pre-edit backup response.
4. Remove imported/body H1s, duplicate styled title blocks, publisher-only planning sections, and body JSON-LD/scripts that would be visible if inserted into classic content. Preserve reader-facing schema only where the site safely emits it.
5. Update all active SEO/social metadata families present on the site, then purge Cloudflare by exact edited URLs.
6. Verify every public URL with a structured pass/fail contract: load, one H1, no body H1, no publisher notes, no raw CSS/schema leak outside style/script, title/meta/canonical present, CTAs present, representative assets OK.
7. For monetized rewrites, additionally verify product module count, unique ASIN count, affiliate tag, Amazon image CDN URLs, image natural dimensions, and that the page has no duplicated product modules or abnormally bloated HTML. See `references/amazon-affiliate-box-live-audit-qa.md`.
8. Produce machine-readable JSON/CSV/XLSX dashboard artifacts so failures are actionable without a long chat transcript.

## XML-RPC implementation notes

- Wrap large HTML in CDATA and escape `]]>` safely.
- `metaWeblog.getPost` is useful for backup and for finding existing custom field IDs; include the `id` when updating existing fields to avoid duplicates.
- `metaWeblog.editPost` with `publish=true` should return `<boolean>1</boolean>`.
- If an XML-RPC write times out on a Cloudflare/LiteSpeed origin, do **not** blindly retry. Wait briefly, re-fetch the post by ID/slug, and verify a unique marker/content length/title before deciding whether it failed. Some writes complete server-side after the client times out.
- If `newPost` times out, resolve the slug before retrying; duplicates and redirect loops are worse than a delayed publish.
- If the apex is Cloudflare-blocked, post XML-RPC to the origin IP with the public `Host` header.
- Use the site credential file only at runtime; never print or save passwords/tokens.

## Reporting style for this user

For first-post proof, keep the report short and operational:

- URL updated
- Post ID
- Source file
- Key fixes made
- Verification bullets
- Backup path
- Clear verdict: proceed / do not proceed
