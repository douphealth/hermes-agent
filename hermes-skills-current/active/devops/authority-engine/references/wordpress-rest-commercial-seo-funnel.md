<!-- Consolidated from skill: wordpress-rest-commercial-seo-funnel; original path: /home/hermes/.hermes/skills/devops/wordpress-rest-commercial-seo-funnel -->

---
name: wordpress-rest-commercial-seo-funnel
description: Build a commercial SEO cluster and lead funnel on a WordPress site via REST when wp-admin is blocked by Cloudflare. Covers safe page/post creation, Spectra form embedding, thank-you/download flow, and internal-link reinforcement.
---

# WordPress REST Commercial SEO Funnel

Use this when a WordPress site needs revenue-focused SEO improvements but wp-admin is blocked and REST works.

## Scope
- create/update commercial landing pages and posts
- build a lead magnet page with embedded Spectra/UAGB form
- create thank-you page and downloadable asset via media upload
- strengthen internal links across the cluster
- verify live URLs after every change

## Workflow
1. Fetch REST credentials from the secret file.
2. Back up every page/post JSON to /tmp before editing.
3. Before creating pages, run hidden-competitor discovery using SERP overlap:
   - start with a broad niche term
   - refine into commercial modifiers, use cases, and support questions
   - capture which domains keep ranking across those query sets
   - treat repeated domains as the real competitive set, even if the user did not name them initially
4. Convert the competitor set into an opportunity map:
   - money pages
   - comparisons / alternatives
   - use-case pages
   - informational support posts
   - trust assets and conversion assets
5. Upload downloadable lead-magnet asset with `/wp-json/wp/v2/media`.
6. Create thank-you page first so the lead page can redirect to it.
7. Update the lead page with:
   - stronger CTA above the fold
   - embedded Spectra/UAGB form block
   - success message + JS redirect to thank-you page
   - supporting conversion block explaining what the user gets
8. Create supporting commercial posts around audience/use-case intent.
9. Append a `Related guides` block to key cluster pages so the internal-link graph becomes dense and commercial.
10. Trigger Yoast indexing endpoints.
11. Verify all URLs live with cache-busting requests.

## Enterprise planning layer
Before writing any page, define:
- primary intent: commercial / transactional / informational
- buyer stage
- target page type: landing page, comparison, alternatives, use-case, checklist, tutorial, template, FAQ
- conversion action
- trust requirements: disclosure, methodology, proof, examples, author context
- parent and child internal links

Do not create random blog posts. Create a connected revenue-first cluster.

## AI SEO brief pattern
Use AI for synthesis, not generic copy.
For every target page, produce a mini brief with:
- dominant intent
- secondary intents to satisfy
- must-cover entities and objections
- missing angles competitors ignore
- required schema
- snippet / FAQ / AIO targets
- CTA placement
- internal links in and out
- freshness/update triggers

This produces stronger pages than asking for a generic article draft.

For live SERP-to-structure decisions, also load `serp-driven-rewrite-playbook`.
For the full ranking / AEO / GEO / AI visibility rubric, also load `wordpress-sota-seo-content-system` and its `references/ranking-visibility-playbook-2026.md` reference.

## Premium rewrite / content-upgrade standard
When the task includes rewriting or materially upgrading a page, also load `wordpress-sota-seo-content-system` and follow it.

Minimum upgrade standard for serious pages:
- answer-first intro or intent note near the top
- visible trust/editorial routing where appropriate
- cleaner section hierarchy aligned to search intent
- at least one meaningful comparison / scenario / checklist / FAQ / warning module when it improves utility
- deliberate internal links to parent, sibling, and next-step pages
- copy that sounds human, specific, and decisive — not like generic AI sludge
- HTML modules that are elegant and restrained, not flashy or fragile

Default rewrite mode should be additive, not destructive:
- preserve anything uniquely useful in the original
- add missing premium sections and visual modules
- only full-rebuild when the original page is structurally poor or clearly off-intent

## Spectra form pattern
- Reuse the exact block structure used by existing Spectra forms on the site.
- Required minimum fields: name + email.
- Optional field: use case / message.
- `afterSubmitToEmail` can send submissions to the site email when no CRM form endpoint is available.
- Add a MutationObserver watching the success-message element; redirect to the thank-you page when the hidden class is removed.

## Download asset pattern
- Upload the text or PDF asset to Media.
- Link directly to the uploaded media URL from the thank-you page.
- If `/llms.txt`-style root redirects are attempted through Yoast, do not trust API success alone; verify the real public path. The redirect may report success but still 404 publicly.

## Internal-link reinforcement
Append a simple HTML section like:
- free prompt pack
- premium product page
- existing workflow guides
- new audience/use-case pages (agencies, consultants, founders, marketers, ecommerce)

This is safer than relying on theme widgets or unrelated archives.

For sitewide hub/spoke planning and systematic authority routing, also load `wordpress-commercial-cluster-builder`.

## Premium upgrade pattern for existing commercial posts
When upgrading an already-published money post instead of creating a new one, use this pattern:
1. back up the raw REST object to `/tmp`
2. keep the visible design intact while tightening query alignment
3. add or standardize an editorial review / trust block near the top
4. ensure affiliate disclosure is explicit where commercial links exist
5. normalize trust links to the canonical pages the site currently uses — do not assume older `/editorial-policy/` links are the preferred target
6. if the post has trust language but is still missing canonical policy/methodology links, prepend a small trust note block rather than rewriting the whole page shell
7. add a high-quality `Related guides` block that pushes authority into the money cluster
8. add a clearer conversion next step such as a checklist, lead magnet, or cluster hub
9. verify the page has exactly one live H1
10. for older archive posts, prefer additive upgrades over rewrites: prepend trust/disclosure notes, append checklist CTA + Related guides block, normalize trust links, then only touch headings when structure is invalid

## WooCommerce product page hardcut / premium offer upgrade
Use this when an existing WooCommerce product has the right product/price but weak or mismatched positioning, URL, and SEO copy.
1. Identify the product from the public URL by parsing `product type-product post-<id>` / `postid-<id>` from live HTML when REST slug lookup is uncertain.
2. Authenticate with WordPress application credentials and verify `/wp-json/wp/v2/users/me?context=edit` before writing.
3. Back up both layers before editing:
   - `/wp-json/wp/v2/product/<id>?context=edit`
   - `/wp-json/wc/v3/products/<id>`
4. Update both layers when possible, because one endpoint alone may leave product name, slug, short description, or permalink state split:
   - WP REST product object: `title`, `slug`, `excerpt`, `content`, `status`
   - WooCommerce REST product object: `name`, `slug`, `short_description`, `description`, `regular_price` when needed
5. Build the product body as a premium commercial landing section: answer-first hero, scope cards, deliverables, decision logic, comparison table, FAQ, and final purchase CTA using the real `?add-to-cart=<id>` URL.
6. If the old product slug was already indexed or live, verify whether it now `301`s to the new slug; do not assume slug changes are enough.
7. For FAQ/AEO support, add page-specific `FAQPage` JSON-LD through a small active Code Snippets snippet when inline schema inside the product body is risky. Re-read the snippet and verify live HTML contains the FAQ questions/schema; `/activate` may return an error even when `active:true` and `code_error:null` are already set.
8. Verify plain and cache-busted public URLs for: `200`, exactly one H1, updated title/meta, product price, short description, add-to-cart button/link, new offer markers, old offer text absent, FAQ/schema live, and no horizontal overflow in browser DOM.

Important experiential findings:
- many WordPress posts already have a theme-rendered `entry-title` H1
- if the post body also contains a custom hero `<h1>` in raw HTML, do NOT leave both live
- demote the custom hero heading to a visually matched `<h2>` so the design stays premium while the structure stays valid
- when upgrading old AFS posts, canonical trust links should point to `/editorial-policy-affiliate-marketing-for-success/` and `/review-methodology-affiliate-marketing-for-success/`
- on Mice Gone Guide, canonical trust links point instead to `/editorial-policy-micegoneguide/` and `/review-methodology/`; always inspect the site's actual trust-page slugs first instead of assuming a universal pattern
- some upgraded posts may already contain trust language but still fail verification because the canonical policy/methodology URLs are absent from the live HTML; fix this with an explicit near-top trust note block and re-verify
- older AI/comparison posts may also contain decorative body headings like `<h1 class="main-heading">...`; if the theme already outputs the canonical post-title H1, demote these decorative H1s to H2 rather than deleting them so the visual presentation stays intact
- for archive-wide premium SEO passes, additive upgrades beat rewrites: prepend trust/disclosure blocks, append checklist CTA + Related guides block, normalize canonical trust links, and only touch headings when a real structural problem exists
- for second-wave optimization on already-upgraded posts, add a short query-aligned quick-answer / intent note near the top to improve answer extraction and sharpen user intent match without redesigning the article
- homepage problems can differ from archive problems; for example, Mice Gone Guide's main live performance issue was a homepage base64 SVG/CSS overlay while the article archive had no widespread base64 image problem
- some sites expose no redirect REST route for Yoast or other SEO plugins; when that happens, consolidate duplicate trust pages by rewriting weaker pages into short support pages that point clearly to the canonical trust assets
- this batch pattern is reusable for large commercial archives because it improves quality every pass without breaking the visible design
- homepage problems can differ from archive problems; for example, Mice Gone Guide's main live performance issue was a homepage base64 SVG/CSS overlay while the article archive had no widespread base64 image problem
- on some sites, high-value intent pages benefit from a second pass that adds a compact quick-answer / intent-note block near the top without redesigning the page; this improves answer-engine usefulness and better aligns the page with the query immediately
- on EfficientGPTPrompts, a strong reusable pattern for commercial prompt-library pages was:
  1. audit the full post inventory via REST and score pages by commercial intent (`chatgpt`, `prompt`, `seo`, `landing page`, `sales`, `lead magnets`, `offer positioning`, `workflow`, founder/agency/consultant modifiers)
  2. prioritize pages that already rank / target money terms but still lack the enterprise layer (trust block, SERP-gap section, Related Guides, Next Step CTA)
  3. use lightweight SERP-gap analysis from the current top pages to identify missing semantic entities and business-use subtopics
  4. add an explicit section such as `What top-ranking pages cover that weak prompts miss` or another query-specific gap module, instead of fully rewriting the article body
  5. standardize a dense contextual `Related Guides` module linking across the full money cluster, often 8-10 internal links, so each page reinforces the others
  6. add a commercial `Next Step` block that routes to the next workflow page or core offer
  7. keep the visible design intact and verify live H1 count plus trust/gap/related/next-step presence
- this works especially well for prompt-template libraries where the base article is acceptable but still lacks enough semantic depth, trust visibility, and cluster routing to compete with stronger commercial SERPs
- for duplicate or weak trust pages where redirects are unavailable, convert them into support pages that explicitly route users to the canonical editorial policy, review methodology, founder page, or safety disclaimer instead of leaving multiple competing trust pages live with unclear purpose
- this batch pattern is reusable for large commercial archives because it improves quality every pass without breaking the visible design
## Verification checklist

- thank-you page returns 200 and exposes the download URL
- downloadable asset returns 200 with text/plain or correct file type
- every new commercial post returns 200
- internal-link markers appear live on updated pages
- homepage or hidden trust block includes links to key trust/commercial URLs if extra crawl reinforcement is needed
- H1 count is exactly 1 on the live page after edits
- if a custom hero section already contains an H1 but the theme outputs an `entry-title` H1, demote the hero heading to a styled H2 instead of leaving duplicate H1s live
- editorial review / policy / methodology links are visibly present on upgraded commercial posts
- upgraded posts contain a stronger next-step CTA or checklist path instead of ending as a dead-end article

## Limitations
- Yoast snippet titles/meta may be controlled outside normal page title/excerpt fields; REST page updates alone may not change live head output.
- Production finding: even after successful REST updates to page/post `title`, `excerpt`, and `content`, plus Yoast reindex calls, some sites still keep serving old `<title>` and meta description values from stale Yoast indexables/snippet storage.
- Additional production finding: some sites also inject a separate `AI SEO Schema Markup` JSON-LD block whose `headline` and `description` can stay stale after body content is fixed. This means draft/legal copy can remain exposed in head/schema even when the visible page body is clean.
- Another production finding from PlantasticHaven: body-layer `title.raw` / H1 updates can go live while Yoast still serves the old `<title>` and meta description. In that state, `og:title` may already reflect the new title while `<title>` and description remain stale. Treat that as a real split-brain snippet layer, not a successful full metadata update.
- Therefore always verify both layers after edits:
  1. visible body/H1/content
  2. live head output via public HTML or `/wp-json/yoast/v1/get_head`
  3. compare `<title>`, `meta description`, and `og:title` separately — do not assume they sync together
- If the body is fixed but stale head/schema persists and no direct Yoast/plugin editing path is exposed, report the blocker explicitly instead of pretending the metadata was fixed.
- In that scenario, keep improving the on-page content, excerpts, internal links, trust pages, and downloadable assets while documenting that final title/meta cleanup needs plugin-level access.
