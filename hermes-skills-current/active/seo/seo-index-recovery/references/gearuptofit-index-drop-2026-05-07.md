# gearuptofit.com index drop — May 7, 2026

## Incident
445 indexed pages → 1 indexed page, drop started April 27.

## Diagnosis chain
1. robots.txt → ALLOW all ✅
2. Meta robots → index, follow ✅
3. X-Robots-Tag → absent ✅
4. Sitemap → 1,299 posts in sitemap-posts.xml, but ONLY 1 URL in Yoast post-sitemap.xml ❌
5. WP Core sitemap at /wp-sitemap.xml conflicting with custom sitemap ❌
6. GSC URL Inspection → "Crawled - currently not indexed" (verdict: NEUTRAL)
7. Last crawl: April 26 (day before drop)

## Root cause
Google algorithmically deindexed pages after April 26 crawl. "Crawled - currently not indexed" with NEUTRAL verdict = algorithmic content quality flag, not manual action or technical block.

## Actions taken
- Removed 4 invalid sitemaps from GSC (post-sitemap.xml, post-sitemap2.xml, page-sitemap.xml, category-sitemap.xml)
- Submitted correct sitemap.xml (links to sitemap-posts.xml with all 1,299 posts)
- Purged Cloudflare cache for sitemap URLs
- Set Cloudflare dev mode
- Disabled WP Core sitemap (add_filter('wp_sitemaps_enabled', '__return_false'))
- Set Cloudflare security to "high" for admin access

## Remaining actions (user must do)
1. GSC URL Inspection → manually "Request Indexing" for 20-30 key pages
2. Enable Indexing API in Google Cloud Console (project: seo-optimizer-456317)
3. Improve content quality / reduce content volume
4. Build backlinks from authority sites

## Key GSC site URLs
- Site: https://gearuptofit.com/
- Domain property: gearuptofit.com (not sc_domain — check both)
- Service account: gsc-api-access@seo-optimizer-456317.iam.gserviceaccount.com
