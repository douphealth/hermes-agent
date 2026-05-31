# GearUpToFit RunMatch canonical app-path cleanup (2026-05)

Session-specific reference for consolidating a React/Lovable/Pages app onto a WordPress apex path behind Cloudflare Workers.

## Durable lessons

- Canonical app URL: `https://gearuptofit.com/shoe-match/`; do **not** redirect it to `/shoe-finder/`.
- Serve the app at the edge before WordPress fallback. If the path hits WP, symptoms include WP/Yoast HTML, generic title, and archive/meta clutter.
- Prefer a non-public upstream only after browser-verifying the app at the canonical subpath. For RunMatch, `https://runmatch-ai-buddy.pages.dev` can return valid HTML/assets but still render an in-app 404 when proxied at `/shoe-match/`; `https://runmatch-ai-buddy.lovable.app` is the known-good upstream for the current Worker because the browser renders the RunMatch page at `/shoe-match/`.
- For CSR apps, inject crawlable initial HTML around the React root: title, description, canonical, robots, H1, explanatory sections, internal links, WebApplication/Breadcrumb/FAQ schema. Keep app functionality intact. Curl success is not enough: browser-check the canonical path and click the primary CTA, then inspect console for internal route errors such as `404 Error: User attempted to access non-existent route: /shoe-match/`.
- Vite subpath proxy needs both asset rewrites (`/shoe-match/assets/*` -> upstream `/assets/*`) and BrowserRouter basename handling. Edge-patching minified JS is acceptable only when source deployment is unavailable; browser-verify refresh/client flow afterward.
- Sitemaps can silently regress when an apex catch-all Worker proxies to WP before sitemap-specific routes. Verify sitemap endpoints return XML and not WP HTML. If needed, delegate sitemap paths from the catch-all Worker to the sitemap Worker before WP fallback.
- Add custom app sitemap (`/sitemap-lovable.xml`) to the master sitemap index (`/sitemap.xml`) before submitting to GSC; submit/list exact feeds via API.
- If a redirecting legacy WordPress page (for example `/new-homepage/` -> `/`) appears in the Worker-generated `sitemap-pages.xml`, fix the sitemap Worker, not the public page. Keep the 301, filter REST page results before `buildUrlset()`, expose an audit header such as `x-sitemap-source: wp-rest-pages-filtered`, purge the sitemap URLs, and verify the legacy path is absent while canonical app paths (such as `/shoe-match/`) remain present.
- `origin.gearuptofit.com` is a WordPress origin dependency. Public noindex/nofollow is safe; a public 301 is risky unless Worker-to-origin fetches bypass it.
- Unproxied subdomains on external CDNs (e.g. Bunny/SwipePages) cannot be fixed by Workers until DNS is proxied or the external platform is changed. Treat them as a separate DNS/routing decision.

## Verification snippets

```bash
curl -sS -D - -o /dev/null https://gearuptofit.com/shoe-match/
curl -sS https://gearuptofit.com/shoe-match/ | grep -E 'RunMatch AI|canonical|FAQPage|WebApplication'
curl -sS -D - https://gearuptofit.com/sitemap.xml | head
curl -sS https://gearuptofit.com/sitemap.xml | grep sitemap-lovable
curl -sS -D - https://gearuptofit.com/sitemap-pages.xml | grep -Ei 'x-sitemap-source|x-url-count|content-type'
curl -sS https://gearuptofit.com/sitemap-pages.xml | grep -q 'new-homepage' && echo 'BAD: legacy page in sitemap' || echo 'OK: legacy page excluded'
curl -sS https://gearuptofit.com/sitemap-pages.xml | grep 'https://gearuptofit.com/shoe-match/'
curl -sS https://gearuptofit.com/sitemap-lovable.xml | grep shoe-match
curl -sS -D - -o /dev/null https://shoe-match.gearuptofit.com/
```

Expected post-cleanup signals:

- `/shoe-match/`: `200`, canonical to itself, no noindex, app flow works in browser.
- `shoe-match.gearuptofit.com`: `301` to `https://gearuptofit.com/shoe-match/` once direct upstream is used.
- `sitemap.xml`: XML sitemap index including `sitemap-lovable.xml`.
- `sitemap-lovable.xml`: XML urlset including `/shoe-match/`.
