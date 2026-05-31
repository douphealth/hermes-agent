# Emergency indexation + AI visibility playbook

Use when Alexiios reports that GSC/Bing show near-zero impressions/clicks, falling indexed pages, or weak AI/search visibility across multiple WordPress properties.

## Operating posture
- Execute fixes first, then report compactly. The user is alarmed by SEO collapse and expects immediate remediation, not a long audit narrative.
- Never publish GSC/Bing metrics visibly on websites; keep performance data in agent reports only.
- Treat this as a portfolio-level recovery: technical indexability, sitemap submission, AI-discovery, entity/schema, internal links, and CTR/content refreshes all matter.

## Evidence to gather quickly
1. Crawl each root domain, `/robots.txt`, `/sitemap.xml`, `/wp-sitemap.xml`, `/post-sitemap.xml`, `/page-sitemap.xml`, `/category-sitemap.xml`, `/llms.txt`, `/ai.txt`.
2. On homepage and priority hubs check:
   - HTTP status and redirects
   - `<meta name="robots" content="noindex">`
   - canonical
   - H1 count
   - JSON-LD presence/parseability
   - app/funnel link presence when a freemium app exists
3. If Google service-account credentials are available, query GSC Search Analytics for 7/28 day clicks/impressions and submit sitemaps via the Search Console API.
4. If Bing API key is available, submit homepage, hub, sitemap-derived priority URLs, and app/funnel URLs with `SubmitUrlbatch`.

## First-wave remediation that worked
Install a WordPress snippet (WPCode REST API when available) named like `Hermes Authority Engine AI Search Layer` that defensively adds:
- `/ai.txt` as `text/plain` through `template_redirect`/early request interception.
- Homepage `<link rel="llms-txt" href="/ai.txt">` meta.
- JSON-LD graph on homepage:
  - `Organization`
  - `WebSite`
  - `SoftwareApplication` for the related freemium app/subdomain
  - `ItemList` for priority URLs
  - `knowsAbout` topical entity list
- Optional `robots_txt` filter allowing major AI/search bots and appending sitemap URL.

Pitfall: On some sites `/robots.txt` is static/plugin/CDN-controlled, so WordPress `robots_txt` filters may not show publicly. Do not block on this if `/ai.txt` and homepage schema/meta verify live; record it as a platform constraint and continue.

## WordPress REST/WPCode pattern
- Prefer REST over wp-admin because Cloudflare often blocks admin UI.
- Discover WPCode/snippet endpoints via `wp-json` namespace/routes; common route: `/wp-json/wpcode/v1/snippets`.
- Some WP REST responses include a UTF-8 BOM or non-standard JSON headers; parse with `utf-8-sig` or strip BOM before JSON decoding.
- Test multiple credential candidates from the local secrets file, but never print credential values.
- Make snippets additive/idempotent: update existing matching title if present; otherwise create new active snippet.

## API submission notes
### Google Search Console
- If `googleapiclient` is unavailable, service-account JWT can be created manually with `cryptography` and posted to `https://oauth2.googleapis.com/token` using scope `https://www.googleapis.com/auth/webmasters`.
- Submit sitemaps with `PUT https://searchconsole.googleapis.com/webmasters/v3/sites/{siteUrl}/sitemaps/{feedpath}`.
- Query Search Analytics with `POST .../searchAnalytics/query`.

### Bing Webmaster Tools
- Use API key from secrets only in the request URL, never logs.
- Submit batch URLs with `POST https://ssl.bing.com/webmaster/api.svc/json/SubmitUrlbatch?apikey=[REDACTED] body:
  `{"siteUrl":"https://example.com","urlList":[...]}`.

## Verification standard
After snippets/submissions:
- Purge Cloudflare cache for affected zones when token/zone access is available.
- Cache-busted public verification for every site:
  - `/ai.txt` returns 200 and `text/plain` with brand/priority URL content.
  - Homepage has no `noindex`.
  - Homepage has one H1.
  - Homepage contains `llms-txt` discovery meta.
  - Homepage contains Hermes authority schema marker / expected JSON-LD graph.
  - Funnel/app link is present.
- Report exact counts and blockers compactly.

## Next-wave priority after infrastructure
When moving from infrastructure recovery to page-level traffic recovery, use `references/wordpress-query-led-seo-refresh-wave.md`.

1. Query-led refreshes for URLs with impressions but no clicks.
2. CTR rewrites: title/meta/intro/FAQ/direct-answer blocks.
3. Hub expansion and internal-link rescue for orphan/under-linked pages.
4. AI-answer extraction modules: concise answer blocks, comparison tables, steps, FAQ schema, entity summaries.
5. Use the strongest property as the model pattern and propagate architecture to weaker sites.

## Proven second-wave verification pattern
- Pull GSC `page,query` opportunities, choose pages with impressions and weak CTR, and append idempotent `hermes-query-answer-module-v1` blocks through REST.
- Verify every refreshed URL publicly for 200, marker, FAQ schema, app/internal link, canonical, and no `noindex`; keep repairing until `bad: []`.
- If REST content is updated but public HTML is stale under LiteSpeed, patch a page-scoped `wp_footer` fallback into an existing active Hermes snippet and trigger one-time LiteSpeed purge actions; then verify the normal cached URL, not just cache-busted URLs.
- Parse credentials from the `Rest API` section of the local secrets file, not the `Wp-Admin` section, when using WordPress REST/application-password routes.
