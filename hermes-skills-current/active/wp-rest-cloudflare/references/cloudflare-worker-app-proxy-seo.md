# Cloudflare Worker app proxy + SEO shell pattern

Use this when a WordPress site sits behind Cloudflare and a React/Vite/Lovable/Pages app must live at a canonical path on the main domain without WordPress catching the route.

## Problem signature

- Canonical path (for example `/shoe-match/`) returns `200` but headers/body show WordPress: `x-served-by: wp`, Yoast schema for a thin page, WP/Elementor assets, generic title, Archives/Meta/Login clutter.
- The real app works on a subdomain or Pages/Lovable origin (for example `shoe-match.example.com` or `*.pages.dev`).
- Search/AI visibility needs to consolidate on the main-domain path, not the app subdomain.

## Safe sequence

1. Capture baseline before changes:
   - `curl -I https://example.com/app-path/`
   - `curl -L https://example.com/app-path/ | head -n 80`
   - same for old app subdomain and any old landing page.
2. Identify routing layer first:
   - Cloudflare Worker routes (`zones/:zone/workers/routes`), DNS records, page rules, origin headers like `x-served-by`.
   - Back up every Worker script and zone config touched.
3. Add a higher-priority app-path branch in the apex Worker before WordPress fallback:
   - match `/app-path`, `/app-path/`, `/app-path/*`.
   - fetch the real app origin directly (Pages/Lovable origin), preserving method/body/query string.
   - keep the browser URL on `https://example.com/app-path/`; do not redirect to the subdomain.
4. Rewrite root-relative Vite assets when proxying under a subpath:
   - HTML: replace `src="/assets/` and `href="/assets/` with `src="/app-path/assets/`, `href="/app-path/assets/`.
   - Route `/app-path/assets/*` back to the app origin `/assets/*`.
5. If the React app uses BrowserRouter at `/`, patch configuration at source if possible. If source is unavailable, edge-patch the JS bundle only as a last resort:
   - find the minified BrowserRouter call and inject `basename:"/app-path"`.
   - verify the app no longer renders internal 404 at `/app-path/`.
6. Inject or server-render a crawlable SEO shell into initial HTML when the app is CSR-only:
   - title, meta description, canonical, robots index, one H1, intro, internal links, WebApplication JSON-LD, BreadcrumbList JSON-LD, visible FAQ + FAQPage JSON-LD.
   - keep the actual React `<div id="root"></div>` so app functionality remains.
7. Keep old app subdomain available if it is still needed as the upstream. Do **not** 301 it until the apex path proxies from a separate direct origin and loop risk is gone.
   - Safe interim state: `X-Robots-Tag: noindex, follow` and canonical header/HTML pointing to the apex app path.
8. Update WordPress CTAs/internal links from the old app subdomain to the canonical path using REST `context=edit`; back up raw pages first.
9. Add the canonical app path to the app/custom sitemap layer and purge Cloudflare.
10. If the apex catch-all Worker (`example.com/*`) still serves WordPress for sitemap paths despite more specific sitemap routes, explicitly delegate sitemap paths inside the catch-all Worker to the sitemap Worker/origin before WordPress fallback:
   - `/sitemap.xml`, `/sitemap_index.xml`, `/sitemap-lovable.xml`, `/sitemap-posts.xml`, `/sitemap-pages.xml`.
   - Verify `content-type: application/xml` and the expected `x-sitemap-source`; a WordPress HTML response with `link: <...>; rel="canonical"` means the sitemap route is being missed.
11. Include the app/custom sitemap in the master sitemap index before GSC/Bing submission; otherwise the app path may be live and indexable but undiscoverable from the submitted sitemap index.
12. Remove redirect-only or duplicate legacy WP pages from Worker-generated page sitemaps at the sitemap layer. If `/sitemap-pages.xml` is built from `wp-json/wp/v2/pages`, filter the REST items by normalized pathname before `buildUrlset()` instead of editing/deleting a live WP page that already 301s correctly. Preserve canonical app paths in the same sitemap, add an audit header (`x-sitemap-source: ...-filtered`), purge sitemap URLs, and verify both absence of the legacy path and presence of the canonical app path.

## Validation checklist

- `curl -I https://example.com/app-path/` returns `200`, no redirect to subdomain, no `noindex`, canonical Link header to the apex path.
- Sitemap endpoints return XML, not WordPress HTML: `curl -sS -D - https://example.com/sitemap.xml | head` and `curl -sS https://example.com/sitemap.xml | grep sitemap-lovable`.
- Worker-generated page sitemap excludes redirect-only legacy paths but keeps canonical app paths: `curl -sS https://example.com/sitemap-pages.xml | grep -q old-page && echo BAD || echo OK`; `curl -sS https://example.com/sitemap-pages.xml | grep /app-path/`.
- App/custom sitemap includes the canonical path: `curl -sS https://example.com/sitemap-lovable.xml | grep /app-path/`.
- After GSC submission, list sitemaps through the API and confirm exact feed URLs are present on the exact property (`https://example.com/` vs `sc-domain:example.com`).
- Raw HTML grep finds title, canonical, H1, intro/internal links, WebApplication/Breadcrumb/FAQ schema.
- Raw HTML grep for `Archives|Meta|Log in|wp-login` is clean (beware false positives from words inside `meta` tags; inspect context).
- Asset URLs under `/app-path/assets/*` return JS/CSS MIME types.
- Browser: app loads, CTA starts questionnaire/flow, client routes/refresh work, console has no errors. **Do not trust curl-only success for CSR apps**: an upstream can return SEO HTML while the hydrated BrowserRouter renders a visible `404` at the proxied subpath. If changing upstreams or basename handling, verify the canonical path in a real browser and click the primary CTA before declaring the route fixed.
- Old subdomain: either 301s to canonical path **only if not used as upstream**, or remains noindex + canonical with no loop. Once the apex Worker fetches a separate direct origin such as `*.pages.dev`, prefer a clean 301 from the legacy public subdomain to the canonical path, but only after the direct origin is browser-verified under the canonical subpath.
- Origin host used by the Worker for WordPress fetches: do **not** blindly 301 it even if it is publicly accessible; keep public responses noindex/nofollow unless Worker-to-origin bypass/headers are confirmed. Redirecting the origin host can break the apex WordPress proxy.
- Old landing page: live as supporting guide, no links to old subdomain, CTAs point to canonical app path.

## Rollback

- Roll back routing Worker first if the app breaks.
- Roll back only SEO shell/content if crawlable content is wrong but app still works.
- Restore backed-up WordPress pages for bad link replacements.
- Avoid deleting/redirecting the old app subdomain until the main path has been browser-verified.