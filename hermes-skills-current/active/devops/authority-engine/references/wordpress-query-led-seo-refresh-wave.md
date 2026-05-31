# WordPress query-led SEO refresh wave

Use after the emergency indexation/AI-discovery layer is live and the user wants maximum-efficiency traffic recovery, topical authority, AI visibility, GEO/AEO, and SERP gains across a portfolio.

## Trigger
- User asks to “proceed” after an indexation/GSC/Bing collapse remediation.
- GSC shows pages with impressions but low/zero clicks.
- Need surgical, additive WordPress changes without breaking design or rewriting whole sites.

## Fast workflow that worked
1. **Pull GSC opportunities**
   - Use Search Console Search Analytics with dimensions `page,query` for the last ~28 days.
   - Rank pages by impressions, average position, and poor CTR.
   - Prefer pages already receiving impressions: they are fastest to move with answer/CTR/schema upgrades.
2. **Deploy additive query-answer modules**
   - Use WordPress REST to update the existing post/page content; back up raw content first when possible.
   - Append an idempotent HTML block/class such as `hermes-query-answer-module-v1`.
   - Include:
     - answer-first H2/H3 sections matching observed queries
     - concise self-contained answers for AI extraction
     - FAQPage JSON-LD with class marker `hermes-faq-schema`
     - topical/entity language naturally embedded
     - internal links to sibling/hub resources and the relevant freemium app/tool
   - Keep modules additive and below existing content unless the article clearly needs a front-loaded intro rewrite.
3. **Submit and purge**
   - Submit affected sitemaps in GSC; run URL Inspection where API access allows.
   - Batch-submit refreshed URLs to Bing (`SubmitUrlbatch`).
   - Purge Cloudflare by exact URLs or zone; then verify uncached/live HTML.
4. **Verify before reporting**
   - For every refreshed URL confirm:
     - HTTP 200
     - `hermes-query-answer-module-v1` present
     - `hermes-faq-schema` or `FAQPage` present
     - app/funnel/internal link present
     - canonical exists
     - no `noindex`
   - Re-run until `bad: []`, then report compact counts.

## REST credential pitfall
When credentials are stored in a combined local file, prefer parsing the `Rest API` section rather than nearby `Wp-Admin` credentials. Admin-login passwords may authenticate in wp-admin but fail REST/application-password requests. Parse domain/user/password rows from `Rest API` through the next section marker, then validate with `/wp-json/wp/v2/users/me`.

## JSON/BOM pitfall
Some WordPress REST responses return UTF-8 BOM or non-standard headers. Decode REST bodies with `utf-8-sig` before `json.loads()` or strip BOM defensively.

## LiteSpeed stale HTML pitfall
LiteSpeed can keep serving stale public HTML even after WordPress REST content shows the module and Cloudflare purge succeeds.

Recovery pattern:
1. Verify raw REST content contains the module.
2. Fetch public HTML with normal URL and cache-busting query. If module is still absent and response shows `Page cached by LiteSpeed Cache`, use a surgical fallback.
3. If Code Snippets/WPCode REST is available, patch an existing active Hermes authority snippet to add a page-scoped `wp_footer` fallback for the single stubborn URL. The footer block should output the same answer module and FAQ schema only when `REQUEST_URI` matches the target slug.
4. Add a one-time LiteSpeed purge action in the snippet:
   - `do_action('litespeed_purge_url', $url)` when available
   - `do_action('litespeed_purge_all')` as fallback when available
   - store an option like `hermes_litespeed_purge_once_YYYYMMDD_slug` to prevent repeated purges.
5. Trigger a public request, then verify the normal URL (not only cache-busted URL) until the module/schema appear on cached HTML.

## GSC property pitfall
Sitemap submission may succeed for URL-prefix properties but return `403` for a later `sc-domain:` endpoint if that property is not granted to the service account. Do not treat a later 403 as undoing prior successful submissions; report only verified status per endpoint/property.

## Report format
For impatient SEO recovery sessions, keep the final report execution-first:
- pages refreshed count
- live verification counts
- submission/purge counts
- zero-noindex/canonical status
- notable blocker/fix only if material
