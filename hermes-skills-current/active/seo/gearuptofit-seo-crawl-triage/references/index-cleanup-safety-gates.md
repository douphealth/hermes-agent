# GearUpToFit Index Cleanup Safety Gates

Use this reference when consolidating duplicate/indexable GearUpToFit pages, especially homepage/start-page duplicates, category/tool-route cannibalization, and stale SEO title cleanup.

## Trigger

User asks for GearUpToFit SEO/index cleanup, redirects, canonicalization, sitemap cleanup, title/date drift repair, or responds with risk concern such as “make sure you do not break anything.”

## Safety-first response pattern

Before production edits, explicitly state and follow these gates:

1. **Read-only evidence first**
   - Public crawl relevant URLs.
   - Save audit artifacts under `~/.hermes/organic-growth-os/gearuptofit.com/audits/<date>-<scope>/`.
   - Capture status, final URL, title, H1, canonical, robots, and sitemap presence.

2. **Backup and rollback before writes**
   - Back up database before WordPress content/meta edits.
   - Back up any Worker/MU-plugin/file configuration before redirect or output-normalization edits.
   - Save the previous redirect map/config and describe rollback as removing exact entries + purging cache.

3. **Exact changes only**
   - Prefer exact one-hop 301 redirects for duplicate pages.
   - Avoid wildcard redirects unless separately justified and approved.
   - Do not delete WordPress pages/posts as the first move; redirect/consolidate so recovery is possible.
   - Do not use broad `the_content` filters or sitewide regex cleanup for index cleanup.

4. **Small batch first**
   - Start with the highest-confidence duplicate set only.
   - For the 2026-05 duplicate-start-page pattern, safe first batch was:
     - `/home-gearuptofit/` -> `/`
     - `/expert-guides-honest-reviews-real-results/` -> `/`
   - Do **not** blindly redirect `/app/`; first decide whether it is a real tools/app hub or merely a duplicated Running Hub. Redirect only if duplicated; otherwise rewrite/canonicalize as a unique hub.

5. **Cloudflare/Worker ordering**
   - GearUpToFit apex runs through Cloudflare Worker routing, so redirects that must beat WordPress old-slug/canonical logic should be patched in the Worker `REDIRECTS_301` map first.
   - Keep any WordPress/MU fallback narrow and URL-specific.
   - Verify Worker upload method supports module scripts; multipart module upload with metadata is safer than raw `application/javascript` for module Workers.

6. **Cache-aware verification**
   - Validate normal URL and cache-busted URL.
   - Purge Seraphinite/Cloudflare after production changes.
   - Recheck after cache returns `HIT`, not only immediately after a `MISS`/bypass.

## Verification contract

For every changed URL, record:

- Before: status, final URL, title/H1/canonical/robots, sitemap presence.
- After: `curl -I` shows exactly one 301 when redirecting.
- Destination status is 200 and canonical is the destination.
- No redirect chain.
- Yoast sitemap no longer lists redirected URLs when applicable.
- Normal and cache-busted public HTML agree after cache purge.
- Rollback path is written in the report.

## User-facing reporting

Keep it terse and evidence-first:

- Outcome
- Findings
- Action
- Implementation
- Validation
- Risks/Rollback

If the user expresses fear about breaking production, do not over-explain theory. Confirm the safety gates and narrow scope, then proceed only after explicit approval for writes.
