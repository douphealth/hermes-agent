---
name: gearuptofit-seo-crawl-triage
description: Read-only GearUpToFit.com SEO/GEO/AEO crawl triage workflow before production edits. Captures public-surface audit commands, known URL classes, and recurring pitfalls for category/tool/template checks.
---

# GearUpToFit SEO Crawl Triage

Use when starting a GearUpToFit.com technical/content SEO, GEO, AEO, affiliate, or WordPress performance workflow.

## Safety contract
- Read-only first: do not edit production before a backup, rollback plan, changelog, and exact patch proposal.
- Treat Cloudflare/PhastPress/Worker cache as a verification risk; validate normal URLs and cache-busted URLs when changes are later made.
- For health, nutrition, supplement, weight-loss, and fitness claims, require evidence-aware and safety-first language.
- When the user says “make sure you do not break anything” or similar, switch into explicit safety-gate mode: backup first, exact reversible edits only, small batch first, no broad/sitewide regex or wildcard redirects, validate normal + cache-busted URLs, and report rollback path before claiming done. See `references/index-cleanup-safety-gates.md`.

## Fast public audit commands
```bash
python3 /home/hermes/.hermes/organic-growth-os/scripts/wp_readonly_probe.py gearuptofit.com
mkdir -p /home/hermes/.hermes/organic-growth-os/gearuptofit.com/audits/$(date +%F)-initial
python3 /home/hermes/.hermes/skills/devops/authority-engine/scripts/public-wordpress-seo-audit.py https://gearuptofit.com \
  > /home/hermes/.hermes/organic-growth-os/gearuptofit.com/audits/$(date +%F)-initial/public-wp-seo-audit.json
```

If the bundled public audit is too slow, use a bounded custom sitemap/REST crawler and save artifacts under:
`/home/hermes/.hermes/organic-growth-os/gearuptofit.com/audits/<date>-<scope>/`.

## Surfaces to include before planning
- `/`, `/robots.txt`, `/sitemap.xml`, `/sitemap_index.xml`, `/llms.txt`, `/ai.txt`
- category hubs: `/category/review/`, `/category/running/`, `/category/nutrition/`, `/category/health/`, `/category/weight-loss/`, `/category/fitness/`
- tool/app paths: `/shoe-finder/`, `/shoe-match/`, `/runmatch/`, `/watch-match/`, `/fitness-calculators/`, `/tools/`
- trust pages: `/editorial-policy/`, `/testing-standards/`, `/affiliate-disclosure/`, `/medical-fitness-disclaimer/`
- recent posts from WP REST and high-value sitemap patterns: `review`, `best-`, `calculator`, `bmi`, `calorie`, `macro`, `shoe`, `watch`, `fitbit`, `garmin`, `amazfit`, `nutrition`, `weight-loss`, `protein`, `supplement`.

## Recurring GearUpToFit pitfalls to check
- Template cross-contamination: category/tool routes can return a valid 200 while rendering the wrong visible hub copy/H1/title. Browser-verify `/category/fitness/`, `/runmatch/`, `/fitness-calculators/`, and `/tools/` instead of trusting status alone.
- Cache validation pitfall: GearUpToFit uses Cloudflare plus Seraphinite Accelerator page cache (`wp-content/cache/seraphinite-accelerator/pc`). Query-string validation can show a MU-plugin fix while normal URLs remain stale. After MU/page-output fixes, purge Seraphinite page cache and Cloudflare; verify both MISS and subsequent HIT responses for normal URLs.
- MU-plugin deployment safety: when local PHP CLI is unavailable, syntax-smoke-test a candidate MU plugin by uploading it temporarily outside `mu-plugins` (e.g. `wp-content/gutf-lint-*.php`) and requesting it directly; parse errors return 5xx while a safe file exits empty because `ABSPATH` is undefined. Remove the lint file after testing.
- Oversized/duplicated post bodies can trigger Cloudflare Worker 503 resource-limit errors. For a sitemap URL returning 503, check REST `context=edit` raw content length; a repeated/corrupted body may need raw-content backup plus replacement with clean, safety-first content.
- Sitemap pollution: verify every P0/503/noindex URL is not still listed in `post-sitemap.xml`/other Yoast sitemaps.
- Origin/subdomain canonicalization: `origin.gearuptofit.com` should 301 path-for-path to apex with `X-Robots-Tag: noindex, nofollow`; legacy subdomains should 301 to apex canonical paths.
- GearUpToFit apex runs through Cloudflare Worker `gearuptofit-lovable` on route `gearuptofit.com/*`; for SEO consolidation redirects that must beat WordPress old-slug/canonical redirects and avoid two-hop chains, patch the Worker `REDIRECTS_301` map first, then keep a narrow MU-plugin fallback and Yoast sitemap exclusion by post ID. Use multipart module upload with metadata `{main_module:"worker.js"}`; raw `application/javascript` upload fails on module scripts with `Unexpected token 'export'`. For duplicate indexable pages/hubs, use exact slash + non-slash Worker redirects, capture pre/post evidence, purge exact Cloudflare URLs, verify one-hop chains, and if Yoast/page sitemap still leaks redirected URLs, add a narrow Worker sitemap XML filter only for exact URL blocks. See `references/gearuptofit-worker-index-consolidation.md`.
- Affiliate reviews: check visible FTC disclosure and `rel="sponsored nofollow noopener"` on Amazon/affiliate links. For Amazon deep links, verify each unique ASIN with Amazon.com using `Cookie: i18n-prefs=USD; lc-main=en_US` and a real browser UA to avoid misleading geo-redirected titles; preserve `tag=papalex-20`, add `language=en_US`, and do not claim product specs/prices/ratings unless verified from the live listing/source.
- GearUpToFit Yoast/indexable staleness: after XML-RPC/REST title rewrites, public HTML can still contain duplicate/stale Yoast `<title>` or schema `WebPage.name`. For URL-scoped pillar fixes, MU-plugin output normalization may be needed to remove duplicate title tags, replace stale schema/page names, and force the current meta description without changing global Yoast settings.
- Review pages and tool pages: look for FAQ/answer blocks, schema support, internal links to tool/app pages, and visible proof/methodology blocks.
- YMYL pages: check for visible source/references/safety language and remove unsupported medical or supplement promises.

## Output format
For each finding include exact issue, affected URLs, why it matters, exact fix, priority, estimated impact, implementation steps, validation method, and production risk/rollback note.
