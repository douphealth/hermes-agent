# WordPress + Cloudflare canonical-control remediation pattern

Use when a WordPress site is fronted by Cloudflare Workers / Pages / React SSR and the ranking problem is duplicate hosts, staging surfaces, route fallbacks, sitemap conflicts, or mixed canonical signals.

## Core safety rule
Do not hard-redirect or block an origin hostname until you confirm whether a Cloudflare Worker uses that host as the WordPress/backend upstream. If it is an upstream, protect it with `X-Robots-Tag: noindex, nofollow` and/or a small MU-plugin robots guard instead of redirecting it, otherwise the public proxy can break.

## Execution pattern
1. Back up current Cloudflare Worker scripts before edits.
2. Map host roles:
   - apex canonical SEO surface
   - WordPress origin/upstream
   - Lovable/React/Pages app surfaces
   - staging/remnant subdomains
3. Map duplicate paths and SPA fallbacks with status, title, canonical, H1 count, robots, sitemap inclusion.
4. Fix duplicate landing paths with 301s to the chosen canonical URL.
5. Fix fallback routes by redirecting to real hubs/categories, or `noindex` if they must remain app routes.
6. Convert app subdomains into conversion surfaces:
   - keep app functionality live
   - add `X-Robots-Tag: noindex, follow`
   - emit a canonical `Link` header and, if HTML is proxied, rewrite the HTML canonical to the main-domain SEO landing page.
7. Keep the main-domain SEO landing page indexable and internally linked; app subdomain converts.
8. Clean sitemaps so only canonical URLs are listed. Remove staging, fallback, duplicate, and redirected URLs. Submit one authoritative master sitemap in GSC.
9. Fix AI-discovery files (`/ai.txt`, `llms.txt`) as plain text, not WordPress-themed HTML.
10. Purge Cloudflare cache after Worker/WP/MU-plugin edits.
11. Verify with cache-busted and plain public requests.

## WordPress implementation notes
- MU-plugin guards are useful for origin-only robots headers/meta and title/meta overrides on trust pages.
- **Critical split-brain robots rule:** if the WordPress origin emits `X-Robots-Tag: noindex` or origin-only robots meta, the public canonical Worker must explicitly remove/override those signals on the apex/domain routes that should rank. Keep origin hosts `noindex, nofollow`, but make public WordPress pages `index, follow` with a self-canonical HTML tag and canonical `Link` header. Verify both origin and apex separately.
- For WordPress REST content updates, back up the exact REST payload and verify with `context=edit` when possible.
- Avoid relying on REST title alone for H1 correctness: themes can hide, inject, or cache H1s differently than raw content.
- If a page slug redirects because of WordPress canonical rules, a Worker can proxy by page ID (`/?page_id=ID`) at the desired public slug, then rewrite title/canonical/robots/H1 and redirect the old slug to the desired slug. This avoids editing theme routing while preventing redirect loops.
- For trust/legal pages that WordPress themes already render with a title H1, avoid adding a second raw-content `<h1>`; if duplicates appear, remove the content H1 and let the theme H1 stand.

## Verification checklist
For each priority URL, record:
- status code
- redirect location if any
- content type
- `X-Robots-Tag`
- `Link` canonical header
- HTML robots meta
- HTML canonical
- `<title>`
- meta description presence/content for priority pages
- live H1 count and text
- obvious themed fallback text such as “can't find what you're looking for”
- sitemap presence/absence
- Cloudflare cache status where relevant

Check both:
- final public URL (`allow_redirects=False`) to verify exact 301/200/noindex behavior
- plain non-cache-busted URL after purge, because Google and users see the cached edge key, not only the cache-busted QA URL

Pass conditions:
- canonical homepage/path has `200`, one H1, correct canonical, indexable robots.
- duplicate paths 301 to final canonical URLs.
- staging/remnant hosts redirect or noindex.
- origin/upstream host is noindexed if public.
- app subdomains have noindex/follow and canonical to main-domain SEO landing page.
- sitemap master excludes duplicate, redirected, fallback, and staging URLs.
- GSC has one authoritative submitted sitemap.

## Pitfalls
- Cloudflare `Link` canonical headers do not override an inconsistent HTML canonical for all consumers; rewrite both when proxying HTML.
- If the HTML canonical is absent, insert one before `</head>` rather than assuming the `Link` header is enough.
- A public origin host with a canonical to apex can still be crawled/indexed; canonical alone is weaker than noindex for true staging/origin surfaces.
- Sitemap cleanup must match redirect decisions. Do not list URLs that now 301 or are noindexed.
- Cache HIT can make public verification stale after REST or Worker updates; purge and re-check both cache-busted and non-cache-busted URLs.
- Privacy/legal pages often have slug/canonical plugin rewrites; test for redirect loops after changing `/privacy-policy/` vs `/privacy-policy-2/`.
- If WordPress redirects the desired public slug to an older internal slug, use a Worker page-ID fetch (`/?page_id=ID`) at the desired slug, rewrite title/canonical/H1, and redirect the old slug to the desired slug.
- REST content updates may not immediately fix live H1s because theme output or cache can still emit stale/empty headings; edge-rewrite the smallest safe HTML fragment only after verifying the live public HTML.
- Edge title/meta/H1 fixes are acceptable as a low-risk bridge for React/Lovable or WordPress theme constraints, but keep them narrow, route-scoped, syntax-check the Worker before deploy, purge cache, and verify with live HTML. Do not use broad regexes that can rewrite unrelated pages.
- Product-review trust fixes should not invent specs. If official/retailer specs conflict, remove over-specific unsupported claims, add a visible QA label/date/context, and phrase weight/stack/foam as source-checked or size/sample-dependent until fully verified.
