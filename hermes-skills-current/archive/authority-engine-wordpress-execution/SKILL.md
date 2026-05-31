---
name: authority-engine-wordpress-execution
description: Push-button WordPress REST execution layer for the Authority Engine. Publishes and upgrades pages/posts with enterprise-grade SEO, AEO, GEO, trust, internal links, and verification while working around Cloudflare and plugin-layer blockers.
version: 1.0.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [wordpress, rest-api, seo, aeo, geo, authority-engine, cloudflare, internal-linking, schema, eeat]
    triggers: ["wordpress authority engine", "rest seo execution", "publish via wordpress rest", "cloudflare wordpress seo", "maximum quality wordpress seo"]
---

# Authority Engine WordPress Execution

Use this when the user wants the Authority Engine turned into an execution system that can actually ship changes on live WordPress sites via REST.

This is the deployment layer for:
- page and post rewrites
- new page/post creation
- cluster buildout
- internal-link rollout
- trust-block rollout
- FAQ / snippet / AEO upgrades
- GEO / AI citation improvements
- schema-aware execution
- live verification under Cloudflare and cache/plugin interference

## Mandatory loads
Load these before serious execution:
- `devops/authority-engine`
- `devops/wordpress-sota-seo-content-system`
- `devops/wordpress-rest-commercial-seo-funnel`
- `wp-rest-cloudflare`

Load conditionally when relevant:
- `devops/faq-schema-and-answer-box-optimizer`
- `devops/wordpress-commercial-cluster-builder`
- `devops/wordpress-category-hub-architecture`
- `devops/wordpress-trust-blocks-and-proof-elements`
- `devops/premium-wordpress-html-blocks`
- `devops/wordpress-eeat-remediation-via-rest`
- `devops/yoast-snippet-layer-remediation`

## Mission
Take high-level SEO strategy and convert it into safe, verified, live WordPress changes with maximum quality and minimum wasted motion.

## Core execution rules
1. Use REST, not wp-admin, when Cloudflare or site controls make wp-admin unreliable.
2. Back up every object JSON to `/tmp` before editing.
3. Prefer additive upgrades over destructive rewrites.
4. Preserve visible design unless the user explicitly wants redesign.
5. Wrap custom HTML/CSS/JS in `<!-- wp:html -->` blocks to stop WordPress auto-wrapping from breaking layouts.
6. Verify the public page, not just the REST response.
7. Check body-layer SEO and head-layer metadata separately.
8. If plugin/snippet layers block metadata updates, document the blocker and still ship body-layer gains.

## Standard execution workflow

### Phase 1 — access and target discovery
Before editing:
- get REST credentials from the secret file
- verify auth with `/wp-json/wp/v2/users/me?context=edit`
- discover relevant endpoints from `/wp-json/` when needed
- identify target page/post IDs
- prefer REST slug/permalink lookup with `context=edit` and confirm the returned object's `link` matches the target URL before writing
- do not rely on arbitrary public HTML `post-123` / `postid-123` matches alone; related-post widgets, cached fragments, inline `postid-*` in recommendations, or templates can expose different post IDs and cause edits to the wrong object
- when slug lookup is empty or link-mismatched, identify the live object ID using high-confidence markers only: `<body class="... postid-123 ...">`, the main `<article id="post-123">`, `rel='shortlink' href='...?p=123'`, or `wp-json/wp/v2/posts/123` links; then re-read that exact REST object and compare its returned `link`/public title to the target URL before writing
- after writing, verify the intended URL contains the new marker and also spot-check any accidentally suspected object URL to confirm it was not changed; if a wrong object was touched, restore it from the `/tmp` backup immediately and re-verify both URLs
- identify trust-page slugs already live on the site
- identify whether the site is using Yoast / RankMath / AIOSEO / custom schema plugins

### Phase 2 — preflight backup
Before every edit:
- fetch the full current object with `context=edit`
- save raw JSON backup locally under `/tmp`
- if doing a cluster pass, save one backup per object
- if editing users/authors/settings, back those up too

### Phase 3 — page-spec to execution map
Convert the Authority Engine brief into implementation fields:
- `title`
- `excerpt`
- `content.raw`
- schema additions or supporting blocks
- trust links
- contextual internal-link placements inside useful editorial sections
- bespoke next-step CTA only when it is genuinely helpful and non-boilerplate
- FAQ / answer blocks
- comparison / checklist / warning modules
- internal links to parent, siblings, trust, and next-step pages

### Phase 4 — REST-safe write strategy
Use the safest write path available:
- use `POST` + `X-HTTP-Method-Override: PUT` when Cloudflare blocks PUT
- keep a browser-like User-Agent
- throttle batch write/read cycles by about 2.5–3.0 seconds between WordPress REST calls on Alexiios-style Cloudflare/CDN sites to reduce rate-limit, cache, and WAF friction
- send payloads as JSON files when content is large or fragile
- wrap custom HTML in `<!-- wp:html -->` blocks
- use additive prepends/appends for archive upgrades when a full-body rewrite is unnecessary

### Phase 5 — maximum-quality page upgrade pattern
For serious pages, the minimum live upgrade usually includes:
- tightened title/H1/query alignment
- answer-first intro or intent note near the top
- visible trust/editorial/methodology routing where relevant
- one or more extraction assets where useful:
  - definition block
  - steps
  - checklist
  - comparison table
  - FAQ block
  - mistakes/warning box
  - scenario cards
- editorial internal links placed where they help the reader, not generic related-guide modules
- bespoke next-step CTA only if it improves the page’s actual user journey
- canonical trust links
- fixes for duplicate-H1 issues

### Phase 5b — Alexiios quality guardrail: no generic related-guide sludge
Do **not** ship visible boilerplate modules such as “Related guides that strengthen this topic,” “Related guides to keep building the topic,” “Next guides to read,” or “Next step: use these connected guides…”. These read like SEO machinery and damage premium blog quality. If a prior batch added them, remove both the visible section and leftover source/CSS markers such as `ae-rel5`, `ae-related-wave2`, `ae-related-wave3`, `ae-related-wave4`, and `authority-engine-wave*-related`, then verify the public HTML is clean.

### Phase 6 — cluster reinforcement
For any important page, also execute:
- link to parent / hub
- link to siblings
- link to trust page(s)
- link to next-step conversion destination
- where appropriate, add inbound links from stronger existing pages in the cluster

### Phase 7 — schema-aware execution
Schema rules during live execution:
- do not blindly duplicate plugin-generated schema
- add page-specific schema only when it improves extraction or trust
- if the plugin layer already emits a graph, prefer content structures that reinforce schema rather than conflicting with it
- verify live HTML for schema presence after deployment

### Phase 8 — verification stack
After every write, verify all of these where possible:
- REST object reflects the intended change
- public URL returns 200
- cache-busted URL returns 200
- exactly one H1 is live
- new blocks are visibly present
- internal links are live
- trust links are live
- when adding contextual internal links or bespoke CTA blocks in a batch, extract every href from the changed content, follow redirects, and require final non-4xx status before claiming the wave is clean; stale old paths in reusable link templates can silently create 404s even when the updated page itself verifies perfectly
- schema markers exist if added
- title/meta/og/head output checked separately from body content

### Phase 9 — cache/plugin blocker detection
Treat these as first-class diagnostics, not edge cases:
- plain URL differs from cache-busted URL
- body is updated but `<title>` / description stay stale
- og:title updates but title/meta description do not
- plugin-generated JSON-LD keeps stale copy after body fixes
- optimization plugins reintroduce broken no-query HTML

If this happens:
- document exact divergence
- report body-layer success separately from head-layer blocker
- keep shipping the gains that REST can control

## Execution patterns

### Pattern A — existing page additive upgrade
Use when the page is decent but underpowered.
- prepend a compact quick-answer / intent note
- prepend or insert trust block if missing
- add contextual internal links inside relevant paragraphs, tables, checklists, or decision points
- add a bespoke next-step CTA only when it is natural and useful
- normalize trust links
- add FAQ/checklist/comparison block where useful
- demote decorative duplicate H1s to H2s if the theme already renders the canonical H1

### Pattern B — money-page commercial upgrade
Use when a page already targets a valuable term.
- tighten commercial query alignment
- sharpen top-of-page summary
- add proof / methodology / disclosure routing
- add SERP-gap module covering what weak pages miss
- weave dense internal links contextually into buying criteria, alternatives, FAQs, and decision tables instead of dumping a generic related-guides block
- add stronger conversion CTA

#### Affiliate product-box rollout pattern
Use when upgrading commercial posts that should contain Amazon/affiliate recommendations.
1. Treat the post as a full editorial rewrite, not an ad insertion: add answer-first copy, buying criteria, safety/fit caveats, affiliate disclosure, comparison logic, and FAQs before/around product boxes.
2. Inspect active affiliate/product plugins first (`/wp-json/wp/v2/plugins?context=edit`) so you know whether AAWP or another Amazon plugin is available. If plugin shortcodes/API are not practical for the immediate rewrite, direct HTML cards are acceptable, but they must be self-contained, theme-safe, and verified publicly.
3. Build product cards from relevant search queries or known ASINs. Every visible card should include:
   - affiliate URL with the correct store tag, e.g. `tag=<store-id>` such as `papalex-20`
   - `rel="nofollow sponsored noopener"`
   - product title that matches the linked Amazon item closely
   - corresponding product image URL when the user requested images; use only real image URLs that render publicly, not placeholders or unrelated stock images
   - short editorial caveat telling readers to verify label, sizing, warranty, seller, price, dimensions, compatibility, or ingredients.
4. If Amazon search/pages/widgets block scraping or hide data, do not publish guessed ASIN/image pairs. Use known ASINs, verified public Amazon media image URLs, AAWP/plugin output, or reduce the product count until every card can be matched and checked.
5. Do not leave placeholder/no-image boxes live if the user explicitly asked for product images. Re-read `content.raw` after publishing and require zero placeholder markers plus the expected count of Amazon image URLs.
6. Verify public pages, not just REST objects: HTTP 200, correct `postid-*`, self-canonical, expected Amazon link count, expected Amazon image count, correct store tag count, and no unexpected 301/404.
7. If the intended old audit URL differs from the REST object's returned `link`, use the returned `link` as truth for verification and report the final canonical URL.
8. If plain no-query output stays stale while REST/cache-busted output is correct, purge origin/page cache before reporting done. On LiteSpeed/Seraphinite stacks, a temporary Code Snippets purge controller that calls `LiteSpeed_Cache_API::purge_all()`, `do_action('litespeed_purge_all')`, targeted `litespeed_purge_url`, `wp_cache_flush()`, and safely deletes `wp-content/cache/seraphinite-accelerator` can be the fastest reliable recovery; delete the temporary snippet afterward and re-check the plain URL.

### Pattern C — new page / cluster expansion
Use when a content gap must be filled.
- create the page from a spec, not from generic drafting
- include parent/sibling/next-step logic at creation time
- ensure the page has at least one extraction-friendly block
- add inbound internal links from existing pages within 48 hours when possible

### Pattern D — trust-layer remediation
Use when the site has weak editorial trust.
- audit author, about, methodology, editorial policy, disclosure, and review pages
- strengthen or create canonical trust assets
- route commercial and informational pages toward those assets
- consolidate duplicate trust pages where redirects are unavailable by turning weaker pages into support pages pointing to the canonical ones

## WordPress-specific production lessons
- many themes already render the post/page title as an H1; do not leave extra body H1s live
- REST success does not guarantee public success; verify both plain and cache-busted URLs
- plugin-managed metadata can stay stale even when body edits succeed
- HTML blocks are safer than trusting auto-formatting on complex content
- if a site strips or texturizes `<style>` / `<script>` tags in `content.raw` and exposes CSS/JSON as visible page text, remove those tags from the body and move CSS, JSON-LD, and head overrides into small active Code Snippets snippets scoped to exact paths; re-read each snippet to confirm `active:true` / `code_error:null`, purge origin/page cache, then verify no visible CSS/JSON leak in public HTML
- for large archive passes, additive upgrades are usually the best risk/reward move
- query-aligned quick-answer blocks near the top are high-leverage second-pass upgrades
- never publish internal prioritization labels or analytics data as visible reader-facing text (for example GSC/Bing impressions, average position, CTR gap, opportunity score, or “Webmaster Tools breakout”); use those privately for prioritization and convert them into natural reader-facing copy such as “Quick answer,” “Complete guide upgrade,” or a genuinely useful section heading
- do not assume trust-page slugs are the same across sites; inspect first

## Output contract
Report:
- site and objects changed
- execution pattern used
- backup location(s)
- blocks/modules added
- trust/internal-link/schema actions taken
- body-layer verification results
- head-layer verification results
- blocker map for anything outside REST control
- recommended next batch for compounding gains
