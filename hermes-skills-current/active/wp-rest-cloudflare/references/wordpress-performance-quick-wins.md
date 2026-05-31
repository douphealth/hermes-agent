<!-- Consolidated from skill: wordpress-performance-quick-wins; original path: /home/hermes/.hermes/skills/software-development/wordpress-performance-quick-wins -->

---
name: wordpress-performance-quick-wins
description: "Speed up a WordPress site quickly using the strongest low-risk wins first: baseline with short timeouts, check caching, inspect plugins via REST API, activate LiteSpeed Cache if installed but inactive, then verify live improvement."
version: 1.0.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [wordpress, performance, caching, litespeed, rest-api, verification]
    triggers: [make site faster, speed up wordpress, slow homepage, high TTFB, cache hit]
    do_not_use_for: [deep theme refactors, risky production rewrites, speculative optimization without measurement]
    compatible_workflows: [baseline-access-check-cache-fix-verify]
---

# WordPress Performance Quick Wins

## Purpose
Apply the highest-impact safe performance improvement first, with minimal token/tool waste and strong verification.

## When to Use
- User says a WordPress site is slow
- TTFB is high and caching appears absent
- You have REST API or wp-admin credentials
- You need a fast production-safe first win before deeper tuning

## Do NOT Use For
- Rebuilding templates or moving infrastructure
- Large plugin/theme audits before securing an immediate win
- Long exploratory loops when a cache-layer fix is likely available

## Workflow
1. Get a short baseline with strict timeouts.
2. Inspect live response headers for caching.
3. If WordPress REST credentials exist, use REST API instead of browser login.
4. Check installed plugins via `/wp-json/wp/v2/plugins`.
5. If LiteSpeed Cache is installed but inactive on LiteSpeed infrastructure, activate it first.
6. Re-test homepage multiple times and verify `x-litespeed-cache: hit` plus improved warm-cache TTFB.
7. Only then continue to deeper optimization (CSS/JS, Cloudflare, homepage payload reduction).

## Baseline Commands
Use short, reliable checks to avoid getting stuck:

```bash
curl -o /dev/null -sS --max-time 15 \
  -w 'ttfb=%{time_starttransfer} total=%{time_total} code=%{http_code} size=%{size_download}\n' \
  https://example.com/

curl -I -sS --max-time 15 https://example.com/ | head -n 20
```

Look for:
- `cf-cache-status`
- `x-litespeed-cache`
- total HTML size
- repeated TTFB behavior

## REST API Checks
Prefer REST over browser automation when credentials are available.

### Discover plugin state
```python
requests.get(
  'https://example.com/wp-json/wp/v2/plugins?per_page=100',
  auth=(user, app_password),
  timeout=15,
)
```

### Activate LiteSpeed Cache if present
```python
requests.post(
  'https://example.com/wp-json/wp/v2/plugins/litespeed-cache/litespeed-cache',
  auth=(user, app_password),
  json={'status': 'active'},
  timeout=20,
)
```

### Install LiteSpeed Cache if not installed
If the plugin is not installed at all, POST to `/wp/v2/plugins` with the WordPress.org slug:
```python
requests.post(
  'https://example.com/wp-json/wp/v2/plugins',
  auth=(user, app_password),
  json={'slug': 'litespeed-cache', 'status': 'active'},
  timeout=30,
)
```
This installs and activates in one call. Requires the site to have direct filesystem write access (most hosts allow this via WP REST API).

## Decision Rules
- If homepage is uncached and LiteSpeed Cache exists but is inactive: activate it first.
- If Cloudflare is present but token permissions are weak: do not stall there; switch to WordPress-side caching.
- If wp-admin is blocked by a Cloudflare challenge, do not keep fighting the browser login path if REST API access already works.
- If REST calls hang, reduce scope and use short timeouts rather than broad discovery.
- After a plugin change, refresh the homepage artifact so old cache output does not fool verification.
- Verify with repeated live requests; one fast request alone is not enough.

## Safe Follow-up Win: Remove Non-Core Frontend Bloat
## Safe Follow-up Win: Remove or Defer Non-Core Frontend Bloat
After caching is fixed, inspect homepage asset URLs and identify obviously non-core frontend payloads.

If the next phase includes homepage or article-body visual cleanup, also load `wordpress-sota-seo-content-system` and prefer premium, restrained HTML/content modules over random decorative bloat. Performance fixes should not make the page uglier or more generic.

Good candidates:
- related-posts widgets/scripts on the homepage
- plugins injecting frontend JS/CSS that do not support the main conversion path
- decorative features that are not needed above the fold
- heavy third-party analytics/marketing scripts added by header/footer injection plugins

### Option A — deactivate nonessential plugins via REST
Example REST deactivation:
```python
requests.post(
  'https://example.com/wp-json/wp/v2/plugins/related-posts-thumbnails/related-posts-thumbnails',
  auth=(user, app_password),
  json={'status': 'inactive'},
  timeout=15,
)
```

Then force a fresh homepage artifact by updating the page with the same content through REST if needed, and verify the script URLs disappeared from the live HTML.

### Option B — when the user wants scripts kept, defer them instead of removing them
If the site already has `phastpress/phastpress` installed but inactive, activating it can be a low-code way to rewrite blocking scripts into deferred `text/phast` script tags.

Example REST activation:
```python
requests.post(
  'https://example.com/wp-json/wp/v2/plugins/phastpress/phastpress',
  auth=(user, app_password),
  json={'status': 'active'},
  timeout=20,
)
```

Verification:
- fetch live HTML with a cache-busting query string
- confirm homepage still renders
- confirm target scripts still exist but are rewritten, e.g. `type="text/phast"` or `data-phast-original-src`
- re-measure TTFB / payload and compare with baseline

### Learned production finding
On AMFS, activating PhastPress safely deferred restored scripts such as Google Analytics, Link Whisper, and third-party injected trackers without manually editing the theme or header code. This is useful when the user explicitly wants analytics kept alive rather than removed.

### Learned production-safe pattern: remove script injectors before deeper refactors
On some WordPress sites, a single script-injection plugin can be responsible for multiple third-party payloads at once.

Example: deactivating `header-and-footer-scripts/shfs` removed injected GA/gtag, Litlyx, Metricool, Grow.me, and ClickRank scripts from the homepage in one step, with much lower breakage risk than editing raw theme/header code.

Also safe to check separately:
- `microsoft-clarity/clarity`
- other analytics or ad-tech plugins that only inject tracking code

Verification pattern:
1. baseline homepage HTML and enumerate external `<script src>` URLs
2. deactivate one injector plugin at a time via REST
3. fetch homepage again with `Cache-Control: no-cache` and a cache-busting query string
4. confirm the target script URLs disappeared and the homepage still renders correctly

Do not assume the removed scripts came from the plugin whose name matches the script vendor. Many are injected centrally by a generic header/footer plugin.

## Learned production-safe pattern: fix homepage image waste via raw content srcset surgery
If homepage images are embedded as raw HTML inside a page builder/custom HTML block, WordPress may not auto-add `srcset` and `sizes`.

Safe approach:
1. back up the raw page content first
2. resolve each image through `/wp-json/wp/v2/media` to confirm available generated sizes
3. replace raw `<img>` tags with explicit `srcset` and `sizes`
4. if an image URL on the homepage returns 404, replace it with a known-good media asset before finalizing
5. verify live HTML no longer has missing `srcset` on upload images

This is lower risk than theme-level responsive-image rewrites when the issue is isolated to one high-traffic page.

## Learned production-safe pattern: ship llms.txt without filesystem access
If only REST/API access is available and root-file deployment is blocked:
1. upload `llms.txt` and `llms-full.txt` via `/wp-json/wp/v2/media` with `Content-Type: text/plain`
2. create Yoast redirects from `/llms.txt` and `/llms-full.txt` to the uploaded media URLs using `/wp-json/yoast/v1/redirects`
3. verify the public URLs return `200` and `text/plain`

This is a practical workaround for Cloudflare/WAF/file-access constraints when the goal is to expose crawler guidance at stable root paths.

## Seraphinite Accelerator → LiteSpeed Cache swap

Seraphinite Accelerator and LiteSpeed Cache both optimize CSS/JS but conflict when active together. On LiteSpeed server infrastructure, LiteSpeed Cache is vastly superior because it adds full-page caching at the server level (Seraphinite only does CSS/JS optimization).

Swap steps:
1. Install LiteSpeed Cache: `POST /wp/v2/plugins {"slug": "litespeed-cache", "status": "active"}`
2. Verify activation via `/wp/v2/plugins` list
3. Deactivate Seraphinite: `POST /wp/v2/plugins/seraphinite-accelerator-ext/plugin_root` with `{"status": "inactive"}`

**Important**: The Seraphinite plugin slug contains a `/` and is `seraphinite-accelerator-ext/plugin_root`. Use it literally in the URL path (no URL-encoding needed). The REST endpoint resolves the real plugin path server-side.

**Verification**: After swap, check `x-litespeed-cache: hit` in response headers. TTFB should drop from ~1s+ to ~0.2s for warm-cache requests.

**Pitfall**: If Seraphinite deactivation via REST returns `rest_plugin_not_found (404)`, the plugin slug may differ from what the list endpoint returns. Compare the exact `plugin` field from the `/wp/v2/plugins` listing — that's the canonical slug to use in the URL.

## Verification
Success evidence should include:
- before/after TTFB samples
- before/after response size when relevant
- cache header proof such as `x-litespeed-cache: hit`
- explicit statement whether improvement is cold-cache, warm-cache, or both

## Output Contract
- Artifact: live performance improvement or a precise blocked diagnosis
- Evidence: curl timings, headers, plugin activation response
- Decision: fixed first-layer caching / blocked / needs deeper tuning
- Next: LiteSpeed tuning, Cloudflare rules, or homepage payload reduction

## Learned Pitfalls
- Some Cloudflare API tokens can list zones but still lack permission to change cache settings or page rules.
- Long REST discovery calls can waste time; prefer narrow endpoints and short timeouts.
- A WordPress site may already run on LiteSpeed infrastructure with the cache plugin installed but inactive — this is often the fastest safe win.
