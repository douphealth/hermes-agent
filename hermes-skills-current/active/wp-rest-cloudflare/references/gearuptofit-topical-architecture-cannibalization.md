# GearUpToFit Topical Architecture + Cannibalization Consolidation

Use when the user reports duplicate/same-intent GearUpToFit URLs, category-hub topic drift, or AI/SEO retrieval confusion from competing pages.

## Core rule

One search intent must have one canonical URL owner. For GearUpToFit, commercial/affiliate shoe roundups should generally live under `/review/`; running education/how-to pages should generally live under `/running/` and link to the relevant `/review/` money page without targeting the same commercial query.

## Fast workflow

1. **Pick the canonical owner before editing.**
   - Example: broad “best running shoes 2026” intent → `/review/best-running-shoes/`.
   - Supporting pages remain live only if their intent is distinct: daily trainers, beginners, wide feet, fit guidance, shoe-selection education.
2. **Audit live signals.**
   - Check duplicate URL status, final URL, canonical tag, robots meta, H1 count, and sitemap presence.
   - Check category hubs publicly before assuming template drift is still present; do not edit hubs if the stale copy is no longer live.
3. **Implement exact one-hop redirects at Cloudflare Worker level when Worker is already the canonical edge control.**
   - Add both slash and slashless variants when applicable.
   - Preserve only exact path redirects; do not broad-redirect `/running/best-*` without classifying each URL.
4. **Clean internal links to the de-optimized duplicate.**
   - Use WP REST search to find likely pages, then raw/live HTML checks for exact old hrefs.
   - Patch stored content with XML-RPC/origin when rich HTML or Cloudflare blocks make REST unsafe.
5. **Update local topical artifacts.**
   - `TOPICAL_MAP.md`: canonical ownership rules, pillar/supporting pages, do-not-compete rules.
   - `CONTENT_INVENTORY.md`: KEEP/REDIRECT/MERGE/REFRESH/NOINDEX status for affected URLs.
6. **Purge + verify.**
   - Cloudflare exact purge; if stale HIT remains, use purge-everything.
   - Verify redirect chains with `allow_redirects=False`: old URL should be `301` directly to canonical; canonical should be `200`.
   - Verify canonical keeper: `200`, self-canonical, `index, follow`, exactly one H1.
   - Verify sitemaps: duplicate absent, keeper present.
   - Verify internal-link source pages no longer contain the exact old href.
7. **Resubmit relevant sitemaps in GSC** when access exists.

## Category-hub handling

- Running hub: can discuss training, shoes, gear, calculators/tools.
- Review hub: commercial comparisons and product reviews.
- Weight-loss hub: sustainable weight management for active people/runners; must not reuse running-hub copy.
- Nutrition hub: runner fueling, hydration, practical nutrition; avoid unsupported broad fasting/diet claims.
- Health hub: recovery, injury prevention, educational wellness; YMYL pages need caution/medical signposting.

## Pitfalls

- Do not delete duplicate WordPress posts when an edge 301 + sitemap cleanup achieves the consolidation safely.
- Do not assume a user-reported category-template issue is still live; verify the public hub copy first.
- Do not collapse supporting pages that serve distinct modifiers (`daily`, `beginner`, `wide feet`, `fit`, `how to choose`). Link them into the canonical cluster instead.
- Do not claim architecture rebuild from only a redirect. Update the topical map/content inventory and verify sitemap/canonical/internal-link signals.

## Evidence contract for final reply

Report only compact evidence:

- Redirect chain old → canonical → `200`.
- Canonical URL, robots, H1 count.
- Sitemap duplicate absent / keeper present.
- Internal links cleaned count or specific pages.
- Category hub copy status.
- Artifact paths: final verification JSON, changelog, Worker backup, content backups.
