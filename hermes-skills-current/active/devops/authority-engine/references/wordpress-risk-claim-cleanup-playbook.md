# WordPress Risk-Claim Cleanup Playbook

Use this reference for SEO/GEO/AEO cleanup when a WordPress site has unsupported claims, invented stats, future-looking algorithm claims, source-widget inconsistencies, or AI/autoblogging risk that could damage trust, snippets, E-E-A-T, or AI citation readiness.

## Trigger patterns
- A page says `Source-Verified Claims` while also exposing `0 external sources cited`.
- Search snippets or page HTML expose unsupported earnings, traffic, conversion, study, algorithm-update, or model-detection claims.
- AI/autoblogging pages mention future updates, made-up algorithm names, unsupported fingerprint percentages, fake expert quotes, or implied Google penalties without visible sources.
- Claims are exact-phrase discoverable from public HTML, related-post modules, excerpts, schema, or custom fields.

## Enterprise-safe sequence
1. **Define exact risky strings first.** Build a phrase list from the user's report plus nearby variants. Include punctuation/Unicode variants when relevant.
2. **Back up before editing.** Save raw post HTML and relevant custom fields/meta before each mutation. Never rely on public cache as the source of truth.
3. **Patch source content, not only rendered HTML.** Search and clean post body, excerpts, SEO/meta/custom fields, related reusable blocks if accessible, and any generated trust widgets that embed claim counts.
4. **Prefer substantiation over deletion when safe.** If a label says source-verified but sources are absent, either add visible editorial references that actually support the general guidance or relabel the section as editorial framework. Do not leave a source/count contradiction.
5. **Replace risky claims with conservative language.** Examples:
   - private/fake earnings → `substantial revenue` or remove
   - precise unsupported percentages → qualitative wording or remove
   - future/internal studies → `editorial review` only if true and clearly non-public
   - fake Google/MUM/update claims → Google Search quality/helpful-content guidance
   - fake attribution/quotes → editorial note
6. **Preserve URLs, links, layout, categories, and Gutenberg structure.** Use surgical text replacements. Do not redesign unless asked.
7. **Purge caches.** Purge exact URLs and full zone/site cache when available.
8. **Verify both raw and public states.** Re-fetch raw WordPress content and cache-busted public URLs. Fail the task if any exact risky phrase remains.
9. **Widen only when evidence demands it.** If target-page verification finds the same risky snippet coming from related posts or sidebar cards, scan recent/posts for the exact phrase set and patch only confirmed hits.
10. **Do not fake reindexing.** Use Search Console/IndexNow only when credentials or a configured key exist. Otherwise state that recrawl acceleration is still manual.

## Verification checklist
- Raw WordPress content: zero exact risky-phrase hits.
- Public cache-busted HTML: zero exact risky-phrase hits.
- Target pages show visible references or no source-verified language.
- Related modules/excerpts no longer expose risky phrases.
- Cache purge result captured.
- Backup path captured.

## AMFS-specific notes from prior run
- Direct origin XML-RPC with correct `Host` header was the reliable write path.
- Store backups under `/home/hermes/backups/amfs-risk-claim-cleanup/` or a dated subdirectory.
- Use visible editorial references for general Google/FTC guidance when repairing `0 external sources cited` contradictions.
- Exact public verification should include priority URLs plus any related URLs found by raw phrase scan.
