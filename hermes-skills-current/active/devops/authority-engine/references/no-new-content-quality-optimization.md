# No-new-content quality optimization for existing SEO implementations

Use when the user wants better quality, professionalism, efficiency, AEO/GEO extraction, or implementation optimization but explicitly does **not** want more content, new pages, or topical expansion.

## Core correction
Do not interpret “improve/optimize all this implementation” as permission to add more pages, hubs, or content blocks. For this user, first assume the desired intervention is **existing-content quality refinement** unless they explicitly ask for expansion.

## Allowed interventions
- Rewrite/refine wording inside existing modules or article sections.
- Remove generic SEO phrasing and repetitive language.
- Tighten direct answers, headings, FAQs, and schema to match visible content.
- Improve clarity, specificity, and human readability without increasing topical scope.
- Fix implementation mismatches where REST-updated content differs from public HTML.
- Improve internal/funnel link presentation only where the link already belongs contextually.
- Verify normal and cache-busted public HTML before reporting success.

## Disallowed by default
- New pages.
- New hub/cluster expansion.
- Broad new topical sections.
- Net-new content campaigns.
- Extra thin FAQ stuffing.
- New affiliate/link blocks unless already part of the existing intent and user-approved.

## Execution pattern
1. Build an optimization queue from existing deployment/public verification artifacts.
2. Fetch each existing WP post/page via REST `context=edit` and back up raw content.
3. Locate the existing module/section marker rather than appending more material.
4. Replace or refine the existing module in place. Use a new quality marker such as `hermes-quality-optimized-v2` to make QA deterministic.
5. Keep schema aligned to visible FAQ/answer text.
6. Update only the public-serving post/page ID.
7. Purge cache where possible; at minimum check both plain and cache-busted URLs.
8. Verify: HTTP 200, canonical, no `noindex`, marker present, schema present, no old generic phrases, no duplicate questions, internal/funnel links still present.

## Important pitfall: public duplicate post/version mismatch
A WordPress URL can publicly render a different post ID than the one updated through REST. Example failure mode: REST update succeeds on one post ID, but public HTML `postid-XXXXX` shows a duplicate post still serving older content.

Diagnosis:
- Fetch public HTML and extract `postid-([0-9]+)`.
- Compare against the REST ID updated.
- Fetch both IDs with `/wp-json/wp/v2/posts/{id}?context=edit`.
- If links/canonicals point to the same URL but public HTML uses the other ID, update the public-serving ID directly.

Do not keep re-purging cache or resubmitting to GSC if public HTML shows the wrong post ID; fix the ID mismatch first.

## Reporting contract
Say explicitly:
- no new pages/content expansion was done
- how many existing URLs/modules were quality-optimized
- public/cache-busted verification counts
- any duplicate-post/cache/template anomalies fixed
- remaining blockers only if verified
