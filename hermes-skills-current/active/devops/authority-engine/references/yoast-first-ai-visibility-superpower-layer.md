# Yoast-first AI Visibility Superpower Layer

Session-derived repo synthesis from:

- `Yoast/wordpress-seo`
- `adityaarsharma/rankready`
- `Coman123-jp/wordpress-ai-visibility`

Use this reference when the user asks for WordPress SEO/GEO/AEO/AI visibility work on sites that primarily use Yoast SEO.

## Operating stance

- Yoast remains the primary SEO plugin.
- Do not recommend replacing Yoast unless explicitly asked.
- Do not install duplicate SEO plugins.
- Add AI visibility layers only after checking overlap with Yoast metadata, robots, sitemap, and schema output.
- Separate observed live facts from recommendations.

## Yoast capabilities to audit around

Evidence from `Yoast/wordpress-seo`:

- Front-end presenters output Title, Meta Description, Robots, Canonical, Open Graph, Twitter, and Schema.
- Canonical presenter suppresses the canonical tag when Yoast robots has `noindex`.
- Title and meta description pass through `wpseo_title` and `wpseo_metadesc` filters and are tag-stripped.
- Page-level Yoast fields use the `_yoast_wpseo_` prefix, including title, metadesc, canonical, robots noindex/nofollow/advanced, breadcrumb title, schema page type, and schema article type.
- Yoast XML sitemaps include post type, taxonomy, and author providers and can be extended by providers.

Convert into checks:

- title present, unique, intent-matched
- meta description present for priority pages
- canonical self or intentional target
- noindex/nofollow only when intentional
- indexable money pages included in Yoast sitemap
- schema graph present and parseable
- Organization/Person identity consistent
- breadcrumbs visible or represented appropriately

## RankReady capabilities to evaluate

Evidence from `adityaarsharma/rankready`:

- `/llms.txt` and `/llms-full.txt` generation with awareness of SEO noindex states.
- Markdown endpoints such as `URL.md`.
- `Accept: text/markdown` negotiation.
- Link/header discovery for llms, llms-full, sitemap, and markdown alternates.
- AI crawler robots handling for GPTBot, ChatGPT-User, OAI-SearchBot, Claude, Perplexity, Google-Extended, Bing, and others.
- AI crawler access logs.
- Cache-bypass headers for Cloudflare/APO, Varnish/Fastly, nginx, and WP caches.
- Optional FAQ/Author/Person/HowTo/ItemList schema ideas.

Use RankReady-style features when the site needs markdown endpoints, llms-full, crawler logs, or freshness/AI endpoint workflows. Avoid enabling overlapping schema unless duplicate Yoast schema has been ruled out.

## WordPress AI Visibility capabilities to evaluate

Evidence from `Coman123-jp/wordpress-ai-visibility`:

- Lightweight `/llms.txt` with business metadata, key URLs, socials, and sitemap fields.
- Open/Balanced/Block AI crawler modes.
- JSON-LD levels: Basic WebSite/WebPage, Enhanced LocalBusiness/Organization, Full Article/Breadcrumb/Speakable.
- No external API calls, no visitor logging, settings in `wp_options`.

Use this style when the site needs a lightweight no-API/no-tracking llms/robots layer. Do not enable Full schema on a Yoast site without rendered JSON-LD duplicate checks.

## Conflict matrix

### Yoast vs RankReady schema

Risk: duplicate Article, FAQ, HowTo, ItemList, or Person schema.

Decision: Yoast owns the base schema graph. Add RankReady-style schema only when visible content supports it and Yoast does not already output it.

### Yoast vs WordPress AI Visibility schema

Risk: duplicate WebSite, WebPage, Article, Breadcrumb, Organization/LocalBusiness, or Speakable schema.

Decision: prefer llms/robots/business metadata first; disable or avoid overlapping schema unless live JSON-LD diff validates it.

### RankReady vs WordPress AI Visibility

Risk: both may own llms.txt and robots AI bot rules.

Decision: do not run both for the same capability. Pick RankReady for markdown/logging/freshness; pick WordPress AI Visibility for lightweight llms/business metadata/robots mode.

### Physical vs virtual robots.txt

Risk: a physical robots.txt can bypass WordPress/plugin filters.

Decision: always audit the public `/robots.txt` response, not only plugin settings.

### Cache/CDN

Risk: CDN/WP cache may serve HTML for `.md` or `/llms.txt`.

Decision: validate status, `Content-Type`, and body format live for AI-readable endpoints.

## Reusable audit workflow

1. Classify site: publisher, affiliate, local/service, ecommerce, medical/YMYL, SaaS/funnel.
2. Fetch `/robots.txt`, `/sitemap_index.xml`, Yoast sitemaps, `/llms.txt`, and optional `/llms-full.txt`.
3. Crawl priority URLs from sitemap and known money pages.
4. For each URL, validate status, title, meta description, canonical, robots, H1, schema, internal links, answer block, freshness, trust/entity clarity, and AI-readable access.
5. If authenticated, inspect Yoast page-level fields via REST/context=edit before editing.
6. Compare SERP competitors when ranking uplift is part of the ask.
7. Decide AI visibility layer: none/static llms, RankReady-style, or lightweight AI Visibility-style.
8. Deliver scorecard, critical fixes, Yoast-specific fixes, AI visibility fixes, topical map, page specs, implementation checklist, validation checklist, and priority roadmap.

## Reusable implementation checklist

For each priority page:

- Set/verify Yoast SEO title.
- Set/verify Yoast meta description.
- Confirm Yoast Advanced robots is index/follow unless noindex is intentional.
- Leave canonical blank for self-canonical or set explicit target only when fixing duplication.
- Set Yoast schema page/article type only when visible content supports it.
- Set breadcrumb title when hub/page labels need cleanup.
- Confirm sitemap inclusion.
- Add answer-first section, definition block, key takeaways, useful FAQ, and trust/reviewer/methodology sections where intent warrants them.
- Add `/llms.txt` with entity summary, money pages, hubs, trust pages, and sitemap link.
- Add markdown endpoints only after cache/content-type validation.
- Verify live public output before claiming done.

## First audit command pattern

When the repo contains the Yoast AI visibility audit script, run:

```bash
python3 scripts/seo/yoast_ai_visibility_audit.py --url https://example.com --max-pages 50 --out ./audit-example-yoast-ai
```

Then validate high-priority pages with the live page validator:

```bash
python3 scripts/seo/live_page_validate.py --url https://example.com/important-page/
```
