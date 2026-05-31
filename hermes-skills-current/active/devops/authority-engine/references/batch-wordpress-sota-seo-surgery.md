# Batch WordPress SOTA SEO Surgery

Use this reference when the user gives a prioritized list of WordPress URLs and asks for maximum SEO/GEO/AEO/AI-visibility/topical-authority improvement.

## Class-level pattern

Run the task as one artifact-first batch, not as many verbose single-post audits.

1. Create a manifest with priority, URL path, page role, and main goal.
2. Resolve WordPress post IDs from REST discovery, body classes, canonical/meta, or search endpoints.
3. Read raw post content with authenticated WordPress access and save exact pre-edit backups for every target before publishing.
4. Generate URL-specific modules by intent:
   - topical authority pages: strategy maps, entity/cluster checklists, internal-link hubs
   - beginner funnel pages: 90-day maps, monetization-stage tables, next-step CTAs
   - SEO support pages: intent-stage tables, keyword/cluster workflows, cannibalization rules
   - commercial reviews: decision frameworks, who-should-use/skip blocks, affiliate disclosure and trust notes
   - landing/CRO pages: above-the-fold formula, element-by-element CRO table, compliance checklist
   - tool pages: workflow tables, use-case maps, schema/visibility cleanup
5. Update all SEO/meta field families present on the post, not only one plugin family: Yoast, Rank Math, SmartCrawl/WDS, metabox/theme fields, and legacy custom SEO fields.
6. Publish via XML-RPC/origin bypass when REST sanitizes content or Cloudflare blocks writes.
7. Purge Cloudflare exact URLs; if normal URLs stay stale after exact purge, use purge-everything once and recheck.
8. Verify public output with a compact contract:
   - HTTP 200
   - exactly one public H1
   - canonical equals expected clean URL
   - new upgrade marker exists
   - quick-answer/AEO section exists
   - table/extraction asset exists
   - no `https:=`, escaped anchor residue, or visible schema/code leakage
   - strip `<script>...</script>` before testing visible JSON-LD leakage so valid schema does not create false failures
9. Run at least one browser/visual QA on the highest-risk page, especially tool pages or pages that previously leaked schema/template residue.

## Reporting

Keep final chat output compact: Outcome, URL-level changes, validation evidence, caveat/next task. Save raw backups, optimized HTML, verification JSON, and full reports as artifacts.

## Pitfalls

- Stored custom-field updates are not proof that SERP snippets changed. Verify live `<title>`, meta description, social tags, canonical, robots, and H1 separately.
- Some sites have a legacy head-output injector, theme layer, SEO plugin conflict, or performance/cache layer that emits stale public title/meta even after post fields update. Record this as a technical follow-up instead of claiming snippet completion.
- Do not remove visible JSON-LD/schema leakage with over-broad paragraph regexes. Bound the malformed block carefully and confirm the newly added content marker still exists afterward.
- If cleanup removes too much content, restore from the immediate backup and reapply a narrower bounded removal.
