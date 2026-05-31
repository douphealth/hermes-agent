# Surgical SEO Max-Force + Token-Efficient Workflow

Use this when an existing WordPress/blog-post optimization request includes “maximum”, “superpowers”, “SOTA”, “100x/10000x/10000000x”, or the user complains that visible changes were too small. The lesson from the GearUpToFit athlete-nutrition run: a first pass can be technically correct yet visibly underwhelming; max-force mode must add public-visible utility, not only metadata or tiny copy tweaks.

## Operating rule

High quality and low tokens are compatible: write large diagnostics and raw artifacts to files/CMS, then show only compact decision/evidence summaries in chat.

## Max-force requirements

For long-form posts where risk does not block it:
- Add or upgrade at least one major H2 and several H3s.
- Add multiple extraction assets: tables, checklists, protocols, examples, FAQ/PAA blocks, comparison/decision frameworks, source blocks, or internal-link clusters.
- Update Yoast title/meta/focus/excerpt when authenticated access exists.
- Repair broken links, escaped HTML residue, unsupported claims, stale facts, and weak AI-like filler.
- Verify the public page changed visibly: TOC entries, live modules, read-time/content delta, and browser/visual QA when possible.

## Token-efficient execution pattern

1. Generate a compact edit pack first and save full artifacts to disk:
   ```bash
   python3 scripts/seo/surgical_seo_supercharger.py \
     --url <url> \
     --mode max-force \
     --out /tmp/surgical-seo-pack \
     --stdout status
   ```
2. Read `edit-pack.compact.json` before full JSON. Open full artifacts only when needed.
3. Keep top-k limits tight by default: about 120 sitemap URLs, 8 semantic clusters, 12 internal-link candidates.
4. Never paste full raw WordPress HTML, sitemap dumps, crawl logs, GSC exports, SERP exports, or credentials into chat. Report counts, deltas, selected evidence, and file paths.
5. Final chat response should be short: Outcome, Implementation, Validation, Risks/Next.

## Pitfall

Do not let “surgical” become “nearly invisible.” If the user asked for max-force or rejects a subtle pass, escalate to visible-impact/max-force mode and add real user-facing modules while preserving the article’s original voice and safety.
