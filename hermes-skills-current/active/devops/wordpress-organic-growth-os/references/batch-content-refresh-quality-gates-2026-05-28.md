# Batch content refresh quality gates — AMFS lesson (2026-05-28)

Use this when upgrading multiple WordPress posts for SEO/GEO/AEO, especially after user frustration about low-quality output.

## Hard quality lesson
For Alexiios' WordPress/SEO work, content that merely satisfies keyword coverage is not acceptable. Treat these as publish blockers, not post-hoc cleanup:

- keyword-stuffed term dumps (`use this as an audit label`, repeated keyword variants, tool-density padding)
- duplicated title/hero/H1-style blocks inside article body
- generic filler sections that do not help the reader make a decision or execute
- unsupported future claims, anecdotal claims, earnings claims, or source-count/research mismatches
- SERP/title intent mismatch between slug, public title, H1, and article promise
- internal links that are only in bottom modules or are injected to 404 URLs
- raw CSS leaks, shortcode/template residue, hidden broken modules, or horizontal overflow

## Required upgrade shape
For each refreshed article, create a reader-facing editorial asset, not a keyword patch:

1. Back up the current post body and metadata before edits.
2. Resolve the actual search intent and visible SERP promise.
3. Replace low-quality sections with useful modules:
   - real methodology/review process
   - hands-on test protocol or decision criteria
   - alternatives/comparison matrix where useful
   - beginner roadmap/framework/checklist when informational
   - deliverability/pricing/automation/compliance/use-case sections for SaaS/email/affiliate tools
   - transparent source/methodology note when claims imply research
4. Keep body HTML at H2 or lower. The theme renders the H1.
5. Add contextual internal links inside the article body, not only a bottom authority block.
6. Avoid publishing “SEO terms” as prose. If a phrase exists only for optimizer coverage, either integrate it naturally or drop it.
7. Update all major SEO metadata families when possible: Yoast, Rank Math, WDS, KK/legacy SEO fields, Open Graph, Twitter, excerpt.

## Verification contract
Before reporting completion, verify all three layers:

- **Stored body**: edited HTML no longer contains bad phrases, body H1s, broken injected links, or literal template artifacts.
- **Raw public HTML**: cache-busted URL returns 200, expected title/H1/sections are present, bad phrases absent, no raw CSS leaks.
- **Rendered browser**: one page H1, zero article/body H1s, no horizontal overflow, no visible low-quality modules, internal links visible and contextual.

Run internal link checks with retries. Distinguish confirmed 404s from transient request timeouts.

## WordPress head-layer caveat
A post body and custom fields can be correct while the public `<title>`/meta description remains stale because of Yoast indexables, a legacy SEO plugin, theme head filter, cache layer, or another title injector. Do not claim title mismatch is fixed until the public `<title>` verifies.

If stored titles/meta are correct but the public head remains stale:

1. trigger admin save for the post,
2. run Yoast indexing endpoints if available,
3. purge Cloudflare and WordPress/Seraphinite caches,
4. verify origin and public URL with cache busters,
5. report the residual head-layer caveat explicitly if it persists.

## WPIL/auto-linker caveat
Link Whisper/WPIL or similar auto-linkers may inject links after the manual body edit. If a rendered page contains a 404 link that is not in the intended source module, search the stored HTML for `wpil_keyword_link`, the URL slug, and linked anchor text. Remove or rewrite the entire sentence if necessary, then purge and re-verify public HTML.