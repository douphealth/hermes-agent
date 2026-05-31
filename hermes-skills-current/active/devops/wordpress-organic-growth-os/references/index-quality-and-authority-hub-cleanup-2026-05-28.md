# AMFS index-quality cleanup and authority-hub hardening — 2026-05-28

## Trigger
Use this pattern when a managed WordPress site has SEO/GEO/AEO ambitions but public quality leaks undermine trust: duplicate theme/footer/sidebar blocks, visible archive artifacts such as “No posts,” indexed app/login/tool subdomains, broken robots.txt on subdomains, old category/tag/author archives, empty placeholders, or legacy pages with unsupported claims.

## Durable lesson
AI visibility work must not outrank crawl/index quality. Before building more GEO/AEO assets, clean the public index surface: remove template pollution, noindex low-trust/unsupported pages, protect apps/tools from indexing, and turn hubs into intentional authority pages rather than archive lists.

## Priority order that worked
1. **P0 index-quality cleanup first**
   - Audit homepage, major hubs, category/tag/author/search archives, and every Cloudflare DNS subdomain that resolves publicly.
   - Search visible rendered text for “No posts,” duplicate navigation/footer/sidebar blocks, “Initializing Engine,” empty placeholders, and old related-reading/template injections.
   - For pages that should remain indexable, remove visible template pollution without changing canonical intent.
   - For pages that should not be in search, apply both header-level and HTML-level noindex where possible.

2. **Subdomain/app/tool protection**
   - Do not rely on weak robots rules alone for login/tool/staging apps.
   - At Cloudflare edge, serve a real `/robots.txt` on protected subdomains:
     ```txt
     User-agent: *
     Disallow: /
     X-Robots-Tag: noindex, nofollow
     ```
   - Add `X-Robots-Tag: noindex, nofollow, noarchive, nosnippet` to all protected subdomain responses.
   - Inject `<meta name="robots" content="noindex, nofollow, noarchive, nosnippet">` into HTML responses.
   - Add `Cache-Control: no-store` for app/login surfaces.

3. **Legacy trust cleanup before hub expansion**
   - Immediately noindex pages with unsupported/fake-looking revenue, deliverability, ranking, benchmark, testimonial, or “bypass/detection” claims.
   - Examples of risk phrases to search for: “X% faster,” “95%+ deliverability,” “free tier is a trap,” “open rates jumped,” “dominate,” “crush,” “secret,” “bypass detection,” stale model/version claims, and URL/title intent mismatches.
   - Rewrite only when claims can be supported by visible methodology; otherwise keep noindexed, merge, or delete.

4. **Authority hubs after cleanup**
   - Build hubs manually; do not leave archive-list pages as core topical authority hubs.
   - Each hub should include: 40–60 word direct answer, decision tree, curated best guides, beginner/intermediate/advanced paths, entity glossary, internal authority links, last-reviewed note, visible FAQ answers, and only valid schema that matches visible content.

## Cloudflare Worker edge-guard pattern
A practical emergency layer can:
- strip legacy WordPress theme elements from apex HTML (`#masthead`, `.site-header`, navigation, sidebars, old footers, related/sidebar widgets);
- noindex archive/search/legacy-risk URL patterns with `X-Robots-Tag: noindex, follow, noarchive`;
- protect app/tool subdomains with `noindex,nofollow` and a real robots.txt;
- leave AI discovery routes (for example `/llms.txt`, `/.well-known/ai.txt`, `/ai/*.json`) on their dedicated Worker route so GEO endpoints continue working.

## Verification checklist
For every changed URL, verify public/cached output, not just deploy/API success:
- HTTP status and final URL.
- `X-Robots-Tag` value.
- meta robots presence/absence.
- canonical URL.
- page title and H1 match intent.
- absence of `#masthead`, `#colophon`, `#secondary`, duplicate nav/footer blocks, “No posts,” “Initializing Engine,” and raw placeholder links/images.
- for protected subdomains: `/robots.txt` returns plain text disallow/noindex, not the app shell.
- for AI discovery: `/llms.txt` and `/ai/summary.json` still return the discovery Worker headers/content.

## Pitfalls
- Do not call a page “fixed” if the API update succeeded but the public cached page still exposes the old template/head output.
- Do not invent `sameAs`, reviews, ratings, prices, testimonials, benchmark numbers, or freshness claims to satisfy schema/audit tools.
- Do not let GEO/AEO work become a distraction from basic index quality; Google’s AI/search surfaces still depend on core SEO clarity, helpful content, crawlability, and trust.
- A Worker can be an emergency guardrail, but follow up by fixing WordPress templates/content when practical so the origin is clean too.
