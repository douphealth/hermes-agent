# WordPress REST SOTA Article Rewrite + Live QA Pattern

Use this when rewriting a live WordPress article through REST for SEO/GEO/AEO quality, especially on sites where wp-admin is blocked or slow.

## Proven workflow
1. **Fetch and back up the exact REST object first.** Resolve the slug through `/wp-json/wp/v2/posts?slug=...&context=edit`, save the full JSON, raw content, title, excerpt, categories/tags, and modified timestamp locally before editing.
2. **Research before writing.** Build the query/entity map from trusted sources: Google autocomplete/related/PAA when available, SERP-visible patterns, authoritative guidance, academic/government sources, and existing site cluster pages. Do not expose private Search Console/Bing data in visible content.
3. **Rewrite as a complete answer asset, not just nicer prose.** Include: answer-first intro, jump links, extraction-ready definitions/steps/tables, topical entities, trusted sources, fair caveats, internal links, FAQ, and Article/FAQPage schema where appropriate.
4. **Preserve monetization/trust modules unless intentionally replacing them.** If a post already contains an affiliate/product box, extract and reinsert it once. Do not duplicate or strip it during a full content rebuild.
5. **Avoid visible keyword-stuffing labels.** It is useful to build a semantic focus list internally, but visible sections titled like “Semantic focus for this article” can look artificial. Integrate keywords/entities naturally in the content instead.
6. **Publish via REST using authenticated app-password credentials from the approved local secrets source.** Use Python/requests when shell redaction or quoting issues are likely.
7. **Verify both canonical and cache-busted URLs.** Check live HTML for status 200, exactly one H1, body markers from the new rewrite, FAQ/schema presence, source/internal links, preserved affiliate disclosure/CTA attributes, and absence of old duplicate blocks.
8. **Browser-spot-check the rendered page.** Accept cookies if needed and visually inspect for broken layout, overlap, missing content, or theme/plugin artifacts.

## QA details that prevented false failures
- Theme/plugin HTML can wrap CTA classes differently from the working source. For AMFS affiliate boxes, CTA buttons use `.amfs-aff-btn`, not `.amfs-product-cta`; live QA should select the actual rendered class.
- If the theme already renders the WordPress post title as the public H1, a body-level `<h1>` in the imported article creates duplicate live H1s. Demote the body H1 to a styled non-H1 (`<div class="...">` or H2) before publishing, then verify canonical and cache-busted public HTML for exactly one `<h1>`.
- Rewritten article packages can be structurally good but templated: scan early H2s/intros for wrong primary-offer names, visible internal phrases like “SEO/GEO/AEO optimization notes” or “publishing checklist,” and package comments. Remove reader-visible implementation scaffolding before publishing.
- Preserve existing monetization/measurement modules from the live post unless intentionally replacing them. If a package lacks `amfs-affiliate-box`, extract/reinsert the existing live box so `data-amfs-offer`, `data-amfs-position`, `rel="sponsored"`, and `affiliate_click` surfaces survive the rewrite.
- A redirecting internal URL can be acceptable if the final URL is a live, relevant internal page. Record the final URL in QA.
- Yoast/snippet metadata may not change from body/excerpt/custom-field updates alone. Some sites have output-buffer/meta override layers that keep stale `<title>`, meta description, OG, or Twitter tags even after `_yoast_wpseo_*`, Rank Math, WDS, and metabox fields are updated. Inspect the public `<head>` separately and treat stale head output as a blocker until the override layer is fixed or purged.
- Cache-busting with `?amfsqa=<timestamp>` is useful but still verify the plain canonical URL too. If canonical is stale while cache-busted is correct, purge the exact URL at Cloudflare and the active performance plugin, then recheck both surfaces.

## Suggested local artifacts
- `backups/<site>-<slug>-<postid>-<timestamp>.json` — exact original REST backup.
- `<slug>-research.json` — query/entity/source evidence and link checks.
- `<slug>-rewrite.html` — final body HTML pushed through REST.
- `<slug>-publish-result.json` — REST update status, link, modified timestamp, content length.
- `<slug>-live-qa.json` — canonical/cache-busted QA report and link checks.
