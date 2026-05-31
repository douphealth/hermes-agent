# Mice Gone Guide commercial affiliate cluster pattern

Use when building buyer-intent affiliate review pages on `micegoneguide.com` while preserving existing informational authority guides.

## Intent split
- Existing URLs are informational authority pages. Do not overwrite or repurpose them into commercial listicles unless the user explicitly asks.
- New commercial URLs should target buyer-intent keywords such as `best mouse traps`, `best humane mouse traps`, and `best mouse proofing materials`.
- Treat the commercial pages as cluster expansion, not rewrites/consolidations.

## Safe execution workflow
1. Confirm target slugs are absent across both `wp/v2/posts` and `wp/v2/pages` before creating anything.
2. Confirm protected existing URLs by slug and object type; MGG may use a mix of posts and pages.
   - Example: `/mouse-elimination-plan/` is a page, not a post.
3. Back up every existing object JSON to `/tmp` before appending links.
4. Create the new review pages as `posts` with `status=publish` and REST `content: {"raw":"..."}`.
5. Use a styled non-H1 hero title inside the HTML block when the theme already renders the post title as the live H1. This prevents duplicate H1s while preserving premium visual layout.
6. Add explicit affiliate disclosure near the top of each commercial page.
7. Link new commercial posts back to core information pages contextually:
   - `/how-to-get-rid-of-mice/` with anchor like `how to get rid of mice safely`
   - `/seal-home-from-mice/` with anchor like `seal your home from mice`
   - `/traps-and-bait-recommendations-from-experts/` with anchor like `mouse traps and bait placement guide`
8. Append a compact contextual tool-choice block to relevant existing informational pages linking to all new commercial reviews. Keep the block reader-useful; avoid generic SEO machinery headings.
9. Re-read/cache-busted verify every changed URL; purge Cloudflare exact URLs if plain output is stale.
10. Verify new posts are included in `https://micegoneguide.com/sitemap-posts.xml`.

## Product/affiliate QA
- Do not publish guessed ASINs. Verify ASIN-product fit using Amazon when accessible and a second evidence source such as DuckDuckGo result snippets/camelcamelcamel/Ubuy when Amazon hides titles or redirects by locale.
- Amazon may return 200 while omitting product title, redirecting to a different locale, or serving a 404 for stale ASINs. Check `status`, final URL, page-not-found text, and external search snippets.
- If a user supplied an ASIN that resolves poorly, replace it with a better-supported ASIN before final verification and purge cache.
- Require `tag=papalex-20`, `rel="nofollow sponsored noopener"`, and no stale/wrong ASIN strings in final public HTML.

## Final verification checklist
For each new commercial URL and every touched informational URL:
- HTTP 200 on plain URL and cache-busted URL
- exactly one live H1
- required inbound/outbound internal links present
- expected Amazon affiliate tag count on commercial pages
- no stale rejected ASINs in public HTML
- Cloudflare cache purged when plain URL differs from cache-busted URL
- sitemap-posts.xml contains the new posts

## Notes from 2026-05 MGG deployment
- Created as new posts: `/best-mouse-traps-for-homes/`, `/best-humane-mouse-traps/`, `/best-mouse-proofing-materials/`.
- Protected existing informational URLs: `/humane-mouse-traps/`, `/seal-home-from-mice/`, `/traps-and-bait-recommendations-from-experts/`, `/mouse-elimination-plan/`, `/how-to-get-rid-of-mice/`.
- Found `/mouse-elimination-plan/` via pages endpoint.
- Fixed stale ASINs before final report and purged Cloudflare exact URLs.