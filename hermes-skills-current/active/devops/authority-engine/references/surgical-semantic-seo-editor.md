# Surgical Semantic SEO Editor

Use this reference when the user asks to optimize an existing WordPress blog post without destroying the original post. This is a class-level workflow for surgical content improvement, not a one-session artifact.

## Trigger

Use when the user says or implies:
- surgical blog post optimizer
- Surgical Semantic SEO Editor
- optimize this existing post
- preserve the original voice
- do not rewrite the whole article
- add semantic entities/keywords naturally
- improve Yoast SEO fields, GEO, AEO, AI visibility, internal links, image SEO, trust, or topical authority for one post

## Core principle

Perform surgical optimization, not generic rewriting. Every edit needs a reason. Preserve useful original content, voice, structure, and intent unless the user explicitly asks for a full rewrite or the post is structurally unrecoverable.

## Visible-impact mode

When the user asks for maximum force, "superpowers," "to the maximum extent," "10000x," or complains that the edits are almost zero, do not hide behind tiny surgical tweaks. Stay controlled and non-destructive, but make the upgrade visibly substantial: add high-value modules, tables, checklists, FAQ blocks, examples, decision frameworks, internal-link clusters, trust/source upgrades, and stronger Yoast fields. Aim for a measurable content delta such as new H2/H3 sections, new TOC entries, improved read-time/content length, and multiple live-visible extraction assets. Before reporting done, verify that the new sections are visible in the public page/TOC and not merely present in raw HTML.

## Architecture

Blog Post Scanner → Search Intent Classifier → Semantic Entity Mapper → Content Gap Detector → Surgical Edit Planner → SEO/GEO/AEO Enhancer → AI Visibility Optimizer → Internal Link Optimizer → External Authority Link Optimizer → Image SEO Optimizer → Yoast Field Generator → Final Human-Quality Editor → Validation Checklist.

## Required workflow

URL-only intake is the default. If the user gives only a blog-post URL, autonomously infer target keyword, secondary keywords, intent, audience, internal-link targets, external authority sources, image gaps, Yoast fields, and semantic/entity gaps. Do not ask for these inputs unless access is impossible or ambiguity would risk destructive edits.

For SOTA/data-driven runs, also load `references/surgical-seo-intelligence-engine.md` and use first-party GSC data, sitemap/crawl context, external keyword/SERP intelligence, and semantic clustering where available.

1. Diagnose the current post: intent fit, title/meta, headings, intro, entities, topical gaps, thin/overwritten sections, answer/definition gaps, internal/external links, images/alt text, readability, E-E-A-T, AI citation readiness, Yoast compatibility, schema and conversion opportunities.
2. Build a semantic entity map: primary topic, intent, main/supporting entities, related concepts, synonyms/variants, likely questions, missing subtopics, internal link targets, external source needs.
3. Produce a surgical edit plan before editing. For each change include location, current issue, exact proposed edit, reason, expected benefit, and risk.
4. Apply only controlled edits: add missing entities/keywords naturally, improve weak sentences/headings/intro/conclusion, add answer/definition/comparison/FAQ blocks only when useful, improve formatting, links, image alt text, Yoast fields, schema recommendations, trust, and AI extractability. Remove fluff, duplication, outdated claims, unsupported claims, or weak AI-like writing.
5. If visible-impact mode applies, add enough utility that a human reviewer can immediately see the difference: new useful sections, new tables/checklists/templates, better top-of-page answer assets, stronger TOC coverage, and measurable raw/live content growth.
6. Return the optimized article plus the required output contract, including what changed visibly and what was verified live.

## Token-efficient max-force reporting

When a surgical SEO run escalates to maximum/superpower/100x mode, do not spend tokens dumping full diagnostics into chat. Use artifact-first execution: save raw HTML, crawl/sitemap results, edit packs, and full optimized content to files/CMS; report a compact Outcome / Visible changes / Validation / Risks summary. For details and thresholds, load `references/surgical-seo-max-force-token-efficient-workflow.md`.

## Output contract

Default to artifact-first, token-efficient reporting. Save full diagnostics, raw HTML, crawl data, edit packs, and long optimized content to files or the CMS; in chat, report only the smallest useful brief unless the user explicitly asks for the full artifact.

Compact chat update:
1. Outcome
2. Visible changes made
3. Validation evidence
4. Risks / next action

Full audit artifact:
1. Executive Summary
2. Before/After Scorecard
3. Semantic Entity Map
4. Surgical Change Log
5. Optimized Blog Post
6. Semantic Keywords Added
7. Keywords/Entities Avoided
8. Internal Link Recommendations
9. External Link Recommendations
10. Image SEO Recommendations
11. Yoast SEO Fields
12. AI Visibility / GEO / AEO Enhancements
13. Validation Checklist

## Scorecard dimensions

Score before and after, 0-10:
- Search intent match
- Topical depth
- Semantic entity coverage
- SEO quality
- AEO quality
- GEO quality
- AI visibility
- Internal linking
- Image SEO
- Human readability
- Trust/E-E-A-T
- Conversion quality

## Yoast rules

Do not recommend replacing Yoast, Rank Math, or duplicate SEO plugins. Treat Yoast as the metadata/canonical/robots/schema/sitemap control plane. Provide SEO title, meta description, focus keyphrase, related keyphrases, slug recommendation, and schema recommendation. Schema must match visible content.

## Pitfalls

- Do not turn a surgical task into a full rewrite unless explicitly asked.
- Do not under-deliver visible change when the user asked for maximum/SOTA/superpower execution; if the first pass is too subtle, escalate to visible-impact mode and add substantial, useful assets.
- Do not keyword-stuff under the name of semantic SEO.
- Do not invent stats, claims, sources, credentials, or dates.
- Do not add FAQ/schema/internal links if they do not help the user or visible content.
- Do not claim SERP or competitor facts unless live evidence or supplied competitor data supports them; otherwise label assumptions.
- For WordPress publishing, verify public rendered output after edits.