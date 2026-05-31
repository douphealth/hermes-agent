# Portfolio indexation execution notes: retry + internal links

Use as implementation detail for `portfolio-indexation-submission-playbook.md` when doing aggressive portfolio-wide indexation work for Alexiios.

## Proven execution shape
- Build one master JSON inventory of all sitemap/static/app URLs.
- First pass: concurrent audit with normalized HTTPS URLs, status/final URL, canonical, robots meta, H1/title/schema counts, public post ID, outbound same-host links, and classification.
- Second pass: retry only `FETCH_ERROR` URLs with longer read timeouts and streaming partial HTML. This can recover hundreds of URLs misclassified by a fast first pass on Cloudflare/LiteSpeed WordPress sites.
- Submit after audit, not before: GSC sitemaps, URL Inspection samples, and IndexNow per host.
- If orphan risk is present, add internal links via existing high-value pages/posts, then re-audit or verify public HTML.

## Internal-link reinforcement pattern
1. Identify URLs classified as `INDEXABLE_ORPHAN_RISK`.
2. Choose 1–3 same-host source pages, preferring homepage/start/about/hubs/strong guides.
3. Use WordPress REST credentials from the local secret file; update by slug/type (`pages` first, then `posts`).
4. Append or replace a marked module:
   - `<!-- hermes-indexation-internal-links:start -->`
   - `<!-- wp:html -->`
   - `<section class="hermes-indexation-links" aria-label="Related guides"><h2>Related guides</h2><ul>...</ul></section>`
   - `<!-- /wp:html -->`
   - `<!-- hermes-indexation-internal-links:end -->`
5. Use natural title-derived anchors, max about 18 links per source module.
6. Verify public HTML. If homepage verification fails but REST says success, assume theme/static front-page rendering or cache; rely on non-home source pages too.

## Reporting numbers that matter
- URLs audited
- clean indexable URLs
- GSC sitemap accepted/total
- GSC inspection accepted/total
- IndexNow accepted URLs by host and retry wave
- orphan-risk URLs linked
- public source pages verified live
- remaining blockers by class

## Avoid
- Saying URLs are “indexed” after submission only.
- Dumping large sitewide footer links.
- Publishing GSC/Bing metrics visibly on the site.
- Treating app/subdomain canonicalization to the main domain as an error without checking whether it is intentional.
