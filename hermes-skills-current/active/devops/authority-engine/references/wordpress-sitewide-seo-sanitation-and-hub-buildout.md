# WordPress Sitewide SEO Sanitation + Hub Buildout Pattern

Use this when a WordPress site has over-optimized/AI-looking content artifacts, raw keyword/entity dumps, mixed topical architecture, weak category archives, or trust contradictions, and the user wants maximum SEO/GEO/AEO/topical-authority improvements.

## Session-derived pattern
A high-impact AMFS pass found that the fastest material wins were not more copy generation, but sanitation + architecture:

1. **Crawl REST inventory first**
   - Use WordPress REST with `context=edit` when credentials are available.
   - Pull posts/pages/categories/titles/slugs/raw content/rendered content.
   - Avoid wp-admin when Cloudflare blocks admin pages; REST is usually safer.

2. **Detect visible scaffolding and raw entity dumps**
   Search content/rendered HTML for visible artifacts such as:
   - `SEO optimized`
   - `AEO/GEO ready`
   - `WordPress-safe HTML`
   - `Reader intent map`
   - `Primary keyword:` / `Secondary keywords:` / `Keywords:` / `Entities:`
   - long comma-separated keyword/entity strings presented as body copy
   - rewrite notes, publisher notes, template names, or internal content-system labels

3. **Sanitize before expanding**
   - Remove visible scaffolding blocks completely.
   - Convert useful semantic terms into natural paragraphs, headings, FAQ answers, styled glossary/tag chips, image alt text, and schema only where visible and true.
   - Do not leave naked keyword strings in body copy.
   - Preserve monetization modules and existing useful design blocks unless they are broken or misleading.
   - Back up each object before REST update.

4. **Normalize trust claims**
   - Remove or qualify vague `reviewed by experts` claims unless there is a named reviewer, credentials, review date, and scope.
   - Add/retain visible author/update/methodology/proof elements on money pages.

5. **Build true pillar hubs instead of archive-list pages**
   For major clusters, create custom hub pages with:
   - clear definition and reader promise
   - who it is for / best-use cards
   - decision framework table
   - curated supporting-guide cards with contextual descriptions
   - glossary/entity chips that look like UI, not raw keyword dumps
   - FAQs with visible answers
   - `CollectionPage`, `ItemList`, `BreadcrumbList` where valid
   - internal links to support pages and later backlinks from support pages to hub

6. **H1 pitfall with WordPress themes**
   Many themes inject the page title as the live H1 outside REST content. If custom hub HTML also contains an `<h1>`, live output can show duplicate H1s. Prefer a styled non-H1 hero title (`<div class="...title">`) inside REST content unless you have verified the theme hides the title. Always crawl public HTML after publishing and enforce exactly one live H1.

7. **Verification gate**
   Check plain + cache-busted live URLs:
   - HTTP 200
   - exactly one live H1
   - no scaffold markers visible
   - schema parses and represents visible content
   - hub pages contain intended `CollectionPage`/`ItemList`
   - affiliate CTAs, if present, retain `target="_blank"` and `rel="sponsored nofollow noopener"`
   - browser spot-check at least one newly built hub to confirm chips/cards look polished and no empty paragraph artifacts are visible

## Rollout priority
1. Week 1: remove template artifacts, raw keyword dumps, trust contradictions, duplicate/footer clutter where accessible, and stale metadata.
2. Weeks 2–4: rebuild core hubs as true pillars.
3. Month 2: merge/redirect thin or overlapping legacy posts and rewrite hype-heavy titles.
4. Month 3: upgrade top revenue/traffic pages with first-hand evidence, screenshots, source notes, schema, and stronger internal links.

## Common hub cluster set for affiliate sites
- Affiliate Marketing
- Affiliate SEO
- Affiliate Programs
- Affiliate Tools
- AEO/GEO / AI Search Visibility
- Affiliate Content Strategy
- Email Monetization

## Reporting standard
Report only what was actually changed and verified. Avoid ranking guarantees. Phrase expected ranking/traffic benefits as material improvements to topical clarity, E-E-A-T, answer extraction, crawl understanding, and conversion paths.
