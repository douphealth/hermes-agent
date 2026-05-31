# GearUpToFit Cloudflare homepage/canonical-control case notes

Use as a concrete implementation pattern for WordPress + Cloudflare Worker + Lovable/React setups where the apex homepage is proxied from an app and WordPress remains available through an origin host.

## Durable lessons

### Keep backend origin functional while removing it from search
If `origin.example.com` is the WordPress upstream for the public Cloudflare Worker, do not 301 it blindly. Safer pattern:
- leave it reachable for Worker/backend calls
- add `X-Robots-Tag: noindex, nofollow`
- add `<meta name="robots" content="noindex, nofollow">` via MU-plugin/output guard
- verify public origin response still serves WordPress and has the robots controls

### Use edge Workers for canonical route governance
For reverse-proxied React/Lovable homepages, put the canonical decision at the edge:
- apex homepage stays `200`, self-canonical, one H1
- duplicate landing route (`/new-homepage/`) 301s to `/`
- SPA fallback paths (`/running/`, `/reviews/`, `/review/`) 301 to real WordPress category/hub URLs
- app subdomains stay usable but get `X-Robots-Tag: noindex, follow` and canonical `Link` header to a main-domain SEO landing page
- if proxying HTML, rewrite the HTML canonical too; header-only canonical is not enough

### Page-ID proxy for WordPress canonical/slug loops
If WordPress redirects a desired public slug (example: `/privacy-policy/`) to an older/internal slug (example: `/privacy-policy-2/`), a Worker can fetch the page via `/?page_id=ID`, serve it at the desired public slug, and rewrite:
- `<title>`
- HTML canonical, inserting it before `</head>` if absent
- visible/live H1 if theme content contains an empty H1
- internal origin/old-slug URLs to the canonical public URL

Then redirect the old slug to the desired public slug. Always verify both directions to avoid loops.

### HTML canonical may be absent even when Link header is correct
Verification must parse both:
- response `Link: <...>; rel="canonical"`
- HTML `<link rel="canonical" href="...">`

If HTML canonical is missing, inject one at the edge or via WordPress/plugin layer. Some parsers and crawlers prioritize visible HTML signals.

### Legal/trust page H1 fixes can be edge-safe
If WordPress REST content is updated but public theme/cache output still emits stale or empty H1s, an edge HTML rewrite can surgically normalize legal/trust pages without layout changes:
- replace `DISCLAIMER FOR CONTENTS OF SITE` H1 with `Terms and Conditions`
- replace empty/non-breaking-space H1 with `Privacy Policy`
- keep exactly one H1
- do not alter body layout modules beyond the specific H1/canonical/title fixes

### Sitemap governance
Use one master sitemap in GSC. The sitemap Worker should exclude URLs that now redirect, noindex, are staging/app-only, or are duplicate fallbacks. Verify sitemap output by counting `<loc>` entries and searching for known-bad fragments.

## Verification probes
For each target URL, collect:
- status code and redirect location
- content type
- `X-Robots-Tag`
- canonical `Link` header
- HTML canonical
- `<title>`
- live H1 count/text
- sitemap inclusion/exclusion

Minimum pass examples:
- `/` => `200`, one H1, self-canonical
- `/new-homepage/` => `301 /`
- `/privacy-policy/` => `200`, H1 `Privacy Policy`, HTML + header canonical to `/privacy-policy/`
- `/privacy-policy-2/` => `301 /privacy-policy/`
- `/term-and-conditions/` => `200`, H1 `Terms and Conditions`, HTML + header canonical to itself
- `new.example.com` => `301` to apex
- `origin.example.com` => `200` with `noindex, nofollow`
- app subdomain => `200`, `noindex, follow`, canonical to main-domain landing page
- GSC => one submitted authoritative sitemap with zero errors/warnings
