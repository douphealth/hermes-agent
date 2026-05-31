# Portfolio indexation submission playbook

Use when the user asks to index or submit all URLs across multiple websites. This is a submission/discovery workflow, not a guarantee of indexing: Google and Bing decide final indexation.

## User expectation
When Alexiios says “try and index all the websites URLs,” execute immediately and report counts/statuses after. Avoid long caveats before acting. Still be precise afterward: say what was submitted, what was accepted, and what was blocked by API/domain verification.

## Workflow
1. Discover portfolio hosts from credentials, known site inventory, sitemap indexes, app/funnel subdomains, and static-site internal links.
2. For each host, discover URL inventory in this order:
   - `/sitemap_index.xml`
   - `/sitemap.xml`
   - sitemap URLs declared in `/robots.txt`
   - recursive sitemap parsing for nested post/page/category sitemaps
   - for static sites without sitemaps, crawl root/internal links conservatively.
3. Normalize and filter URLs:
   - same host only unless intentionally including app/funnel subdomains
   - HTTP 200/canonical targets preferred
   - exclude admin, wp-json, feeds, query-only duplicates, assets, tag archives if intentionally not submitted
   - dedupe exact URLs.
4. Audit every discovered URL before submission. Capture status, final URL, redirect flag, canonical URL/self-match, robots meta/noindex, title, H1 count, schema count, public post ID when present, same-host outbound links, and inbound internal link count from the discovered graph. Classify into `INDEXABLE`, `INDEXABLE_ORPHAN_RISK`, `FETCH_ERROR`, `REDIRECT`, `BLOCKED_NOINDEX`, `BLOCKED_ROBOTS`, `CANONICALIZED_AWAY`, `NOT_FOUND`, or server/non-200 buckets.
5. Retry `FETCH_ERROR` URLs aggressively before final reporting. A high-concurrency first pass can create false timeout noise on Cloudflare/LiteSpeed WordPress sites; run a second pass only against failures with longer read timeouts, streaming partial HTML, and a moderate worker count. Merge recovered URLs back into the master inventory and submit newly recovered indexable URLs.
6. If the user says important pages “don’t have internal links,” reinforce existing pages before/while submitting: identify `INDEXABLE_ORPHAN_RISK` URLs, choose 1–3 strong source pages per host (homepage/start/about/hub/strong guide), and add a small theme-safe `wp:html` “Related guides” module via WordPress REST. Verify public HTML after writes. Note that static front-page/theme rendering or cache may hide REST content on homepages; non-home source pages are usually more reliable for visible link modules.
7. Google Search Console:
   - submit sitemap indexes/sitemaps via `https://www.googleapis.com/webmasters/v3/sites/{siteUrl}/sitemaps/{feedpath}` using service-account JWT OAuth where available.
   - run URL Inspection only for sampled/high-priority URLs; GSC is quota-sensitive and has no bulk force-index endpoint.
   - Treat HTTP 204 for sitemap submit as success and HTTP 200 for URL Inspection as success.
8. Bing/IndexNow:
   - submit URL batches to `https://api.indexnow.org/indexnow` with the Bing/Webmaster key if available.
   - batch in chunks (100–500); if a host returns 403/422, retry smaller chunks (100 then 10) to separate quota/domain-verification failures from payload failures.
   - For subdomains, expect `InvalidRequestParameters`/domain verification failures unless that exact host is verified or the key is accepted for it.
9. Save artifacts:
   - discovered URL inventory
   - classification/master audit JSON
   - per-host submission responses
   - retry results
   - internal-link reinforcement write/verification results when performed
   - final summary with accepted/failed/blocker counts.

## Common response codes
- Google sitemap submit `204`: accepted.
- GSC URL Inspection `200`: inspection response returned; not an indexing guarantee.
- IndexNow `200`/`202`: accepted/accepted for processing depending provider behavior.
- IndexNow `403 UserForbiddedToAccessSite`: key/user lacks verified access for that host or provider refuses later batches.
- IndexNow `422 InvalidRequestParameters`: URL host not related to verified domain or payload contains unrelated hosts.

## Reporting contract
Report:
- number of hosts discovered
- number of URLs audited/discovered
- clean indexable URL count
- classification summary (`INDEXABLE`, orphan risk, fetch errors, redirects, noindex, canonicalized-away, not found)
- GSC sitemap success count
- GSC inspection success/sample count
- IndexNow accepted URL count by host and latest retry-wave accepted count
- internal-link reinforcement counts when performed: source pages updated, orphan-risk targets linked, public verification count
- hosts/batches blocked by domain verification, API limits, cache/theme rendering, or server instability
- artifact paths

Do not say “indexed” unless confirmed by search/index status. Say “submitted for indexing,” “pushed to IndexNow,” or “surfaced through sitemap submission.”

## Pitfalls learned
- A single fast audit pass may overstate `FETCH_ERROR` on large WordPress portfolios. Retry only failures with longer read timeouts before concluding pages are broken.
- IndexNow acceptance can differ by host even with the same portfolio key; report accepted URL counts by host and do not assume all verified properties accept all batches.
- WordPress REST can update homepage content successfully while the public homepage still omits the module because the theme/static front-page template overrides content or cache is stale. Verify public HTML and use non-home authority pages as backup link sources.
- Internal-link modules should be small, contextual, and wrapped in `wp:html`; avoid footer-like sitewide dumps or keyword-stuffed anchors.
