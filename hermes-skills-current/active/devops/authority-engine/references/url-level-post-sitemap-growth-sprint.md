# URL-Level Post-Sitemap SEO/GEO/AEO Growth Sprint

Use this when the user asks for an enterprise SEO/GEO/AEO growth sprint, topical-authority map, cannibalization map, internal-linking plan, refresh backlog, or URL-level execution plan from a specific sitemap feed.

## Critical user-workflow rule
If the user names an exact sitemap feed as the source of truth, use that feed only. Do **not** substitute `sitemap_index.xml`, a parent sitemap, WP core sitemap, or another discovery path unless the user explicitly asks for it. If the exact feed is `post-sitemap.xml`, treat that as the working inventory even if other sitemap URLs exist.

## Required output shape
Produce URL-level actions, not generic SEO advice:

- canonical hub for every sitemap URL
- cannibalization action: `PRIMARY`, `MERGE_OR_301`, `KEEP_SUPPORTING`, `REFRESH`, `REFRESH_COMMERCIAL`, `NOINDEX_OR_FIX_STATUS`
- internal-linking blueprint: source URL, target URL, anchor text, placement, reason
- top 20 refresh briefs
- title tag, H1, meta, and query-specific Quick Answer rewrites
- GEO/AEO blocks: quick answer, best for, not best for, cost/difficulty/time, steps, common mistake, next step, FAQ, sources/verification
- claims to remove/prove: revenue, ROI, traffic, rankings, conversion, testing, “best”, “proven”, “guaranteed”
- review trust module requirements for commercial/review/tool URLs
- 30-day backlog ranked by impact/difficulty
- Search Console reindex checklist that excludes merge/noindex URLs

## Fast execution pattern
1. Fetch the exact sitemap XML and parse only primary `<loc>` entries in the sitemap namespace.
2. Crawl each URL with a cache-busting query and collect: status, title, meta description, canonical, robots, H1 count/text, H2s, visible word count, Quick Answer presence, FAQ presence, schema types, internal link count, affiliate-link count, and high-risk claim snippets.
3. Map each URL to one canonical hub using URL slug + title/H1 vocabulary. Default AMFS hubs are:
   - `/start-here/`
   - `/seo/`
   - `/ai-search-visibility/` or `/seo/generative-engine-optimization/`
   - `/affiliate-marketing/`
   - `/monetization/`
   - `/email-marketing/`
   - `/tools/`
   - `/reviews/`
4. Cluster by hub + normalized topic key. Remove stopwords like `ultimate`, `complete`, `guide`, `best`, `how`, `to`, `for`, year tokens, and generic modifiers.
5. Pick the primary in each cannibalization cluster using: stronger intent fit, deeper content, cleaner URL, commercial value, freshness, and internal-link equity.
6. Build artifacts first: CSV/JSON/MD. For Telegram delivery, attach files and summarize the top items directly.
7. Do not apply redirects/noindex/content edits during the planning sprint unless the user explicitly asks to execute changes.

## Commercial/review trust standard
For every review/tool/comparison page, specify a visible proof module:

- checked by: named person/entity
- date checked
- plan/pricing checked
- features reviewed
- best for
- not best for
- alternatives
- affiliate relationship
- evidence/source URLs

Do not add Review/FAQ/HowTo schema unless the visible content supports it.

## AMFS-specific durable convention
For AffiliateMarketingForSuccess.com post-level growth sprints, the user explicitly wants `https://affiliatemarketingforsuccess.com/post-sitemap.xml` as the source of truth and does not want irrelevant `sitemap_index.xml` checks during this workflow.

- `scripts/url_level_post_sitemap_growth_sprint.py` is the reusable artifact generator for this workflow. Example:

```bash
python3 ~/.hermes/skills/devops/authority-engine/scripts/url_level_post_sitemap_growth_sprint.py \
  --sitemap https://example.com/post-sitemap.xml \
  --out /tmp/example_growth_sprint
```

## Verification before final response
- Confirm exact sitemap URL used.
- Confirm URL count crawled.
- Confirm artifact file paths exist.
- Spot-check at least the top-priority rows for sane titles/actions.
- State whether recommendations are crawl-derived structural decisions, not GSC/rank/traffic claims unless those data sources were actually used.
