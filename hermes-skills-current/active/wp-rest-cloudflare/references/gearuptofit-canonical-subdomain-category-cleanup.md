# GearUpToFit canonical/subdomain/category cleanup pattern

Use for GearUpToFit SEO cleanup when WordPress, Cloudflare Workers, old staging subdomains, and Elementor/category templates interact.

## Origin host canonicalization without breaking apex Worker

Problem: `origin.gearuptofit.com` can be public/indexed while the apex Worker still needs it as WordPress upstream.

Safe pattern:
1. In the apex Worker, fetch WordPress upstream at `https://origin.gearuptofit.com` but send:
   - `Host: gearuptofit.com`
   - `x-forwarded-host: gearuptofit.com`
   - `x-forwarded-proto: https`
   - optional bypass marker: `x-gutf-canonical-proxy: 1`
2. In a WordPress MU-plugin, add an early `template_redirect` that 301s only when `HTTP_HOST === origin.gearuptofit.com` and bypass marker is absent.
3. Redirect path-for-path: `https://origin.gearuptofit.com/$path -> https://gearuptofit.com/$path`.
4. Verify with `allow_redirects=False` for homepage, date archive, and representative post/review URL.
5. Also verify apex homepage/wp-admin still return 200.

## Category hub template copy guard

When Elementor/shared templates reuse the same visible hub copy across categories, add a narrow output guard in MU-plugin rather than editing broad theme layout blindly.

Success criteria for `/category/review/`, `/category/nutrition/`, `/category/health/`, `/category/weight-loss/`:
- Correct H1 in the rendered HTML.
- Correct category-specific intro in visible text.
- Old strings like `Gear Up to Fit Running Hub` and `Start here for running training, shoes, gear, and calculators` absent from normal non-cache-busted URLs.
- Page title/OG labels do not include old clickbait labels like `Shocking 2025...` or unrelated health titles.

Regex pitfall: the original replacement can fail if the `<section>` has multiple classes, e.g. `class="running-hub-intro gutf-category-hub-intro"`. Match with a word-boundary inside the class value:

```php
preg_replace('~<section\s+class="[^"]*\brunning-hub-intro\b[^"]*".*?</section>~is', $replacement, $html, 1);
```

## Default WordPress widget clutter cleanup

On TwentyTen/old WP wrappers, public pages may inject:
- search widget
- monthly archives
- Meta
- Log in link

If Appearance → Widgets is not reliable or needs immediate surgical cleanup, remove the rendered wrapper in the MU output guard:

```php
$html = preg_replace('~\s*<div\s+id="primary"\s+class="widget-area"\s+role="complementary">.*?</div>\s*<!--\s*#primary\s+\.widget-area\s*-->~is', "\n", $html, 1);
```

Verify by checking real pages such as `/shoe-finder/` and `/editorial-policy/` for absence of `Archives`, `Meta`, `wp-login.php`, and old menu labels. Do not treat the word `Meta` in `<meta>` tags as widget evidence.

## Low-value index surfaces

Prefer `noindex, follow` for accessible low-value WordPress surfaces instead of blocking them with robots.txt before Google can see noindex:
- date archives
- internal search results
- tag archives unless curated
- author archives unless curated
- attachment pages

Add via `wp_robots` filter and verify raw HTML robots meta on representative URLs.

## Duplicate WordPress post/slug consolidation

When the user reports multiple same-intent posts, search wider than the obvious slug:
1. Use REST search for exact and near queries (`multiple sclerosis diagnosis`, `multiple-sclerosis-diagnosis`, `ms diagnosis guide`) and include `wp/v2/search?subtype=any` so `/posts/...` aliases or pages are not missed.
2. Inspect every candidate's live state with `allow_redirects=False`: status, `Location`, HTML canonical, robots meta, `Link` canonical header, sitemap presence, and GSC URL Inspection if available.
3. Pick one canonical keeper using exact-keyword slug, strongest content/status, sitemap presence, and self-canonical. For GearUpToFit MS diagnosis, the preferred keeper is `https://gearuptofit.com/health/multiple-sclerosis-diagnosis/`.
4. Consolidate duplicate/legacy aliases with 301s in the apex Worker `REDIRECTS_301` map rather than deleting WordPress posts or editing layouts. Include both slash and no-slash variants, e.g.:
   - `/health/ms-diagnosis-guide` and `/health/ms-diagnosis-guide/` -> `/health/multiple-sclerosis-diagnosis/`
   - `/posts/multiple-sclerosis-diagnosis` and `/posts/multiple-sclerosis-diagnosis/` -> `/health/multiple-sclerosis-diagnosis/`
5. Purge Cloudflare for duplicate URLs, canonical URL, and sitemap URLs; then verify duplicate URLs return 301 and the keeper remains 200 with self-canonical and `index, follow`.
6. Check sitemaps: duplicates should be absent, keeper present in the appropriate post sitemap. Resubmit `sitemap.xml` and the specific post sitemap in GSC after the redirect deployment.

Pitfall: WordPress can serve an alternate `/posts/<slug>/` URL as a full `200 index, follow` page with a self-canonical even when the canonical category permalink exists. Do not assume absence from sitemap means it is safe; test the live URL directly.

## Legacy/staging subdomain consolidation

For proxied Cloudflare-controlled subdomains, use a host-control Worker with host-specific redirects:
- `new.gearuptofit.com/* -> https://gearuptofit.com/`
- `landing-pages.gearuptofit.com/* -> https://gearuptofit.com/`
- `shoe-match.gearuptofit.com/* -> https://gearuptofit.com/shoe-match/`
- `running.gearuptofit.com/* -> https://gearuptofit.com/category/running/`, but shoe/gear/outdoor app paths -> `/shoe-match/`
- `fitness.gearuptofit.com/* -> https://gearuptofit.com/fitness-2/` unless a better canonical fitness hub exists.

If DNS is grey-clouded/unproxied, first switch the CNAME to `proxied: true`, then add the Worker route. DNS propagation can make Python `requests` hit old origin briefly; verify final Cloudflare behavior with `curl` and, if needed, `--resolve`.

## Root llms.txt via Worker

If WordPress serves a weak `/llms.txt` or only has one under uploads, return a root-level `text/plain; charset=utf-8` response directly from the apex Worker. Include core pages, best resources, and editorial standards. Verify `https://gearuptofit.com/llms.txt` is root, 200, text/plain, and contains RunMatch/app/trust pages.

## Verification bundle

Before reporting done, check:
- origin homepage/archive/review URL: 301 to apex path-for-path.
- category hub H1/title/intro/old-copy absence on normal URLs.
- `/shoe-finder/` and `/editorial-policy/`: no Archives/Meta/Login widget clutter; `/shoe-finder/` CTAs should use the clean canonical app URL (`https://gearuptofit.com/shoe-match/`) with no legacy `shoe-match.gearuptofit.com` links and no tracking-query variants on primary CTAs.
- `/shoe-match/`: canonical + `WebApplication` + `BreadcrumbList` + `FAQPage` in raw source, and direct fetches for default curl, Googlebot, Mozilla, slashless path, and query-param path all show RunMatch rather than the WordPress shell.
- `/llms.txt`: root 200 text/plain with expected content.
- staging subdomains: 301 via Cloudflare.
- wp-admin plugin page still 200 and no Cloudflare challenge.
