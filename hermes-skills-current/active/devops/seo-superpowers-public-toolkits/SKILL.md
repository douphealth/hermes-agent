---
name: seo-superpowers-public-toolkits
description: "SOTA SEO/GEO/AEO execution layer distilled from public SEO skills/toolkits: GEO citations, technical audits, SERP crossover, content decay, topical maps, keyword gaps, entity extraction, internal linking."
version: 1.0.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [seo, geo, aeo, ai-visibility, serp-crossover, content-decay, topical-authority, internal-linking, technical-seo, keyword-gap]
    triggers: ["seo superpowers", "GEO optimization", "AI visibility", "SERP crossover", "content decay", "keyword gap", "topical map", "internal link audit", "technical SEO audit"]
---

# SEO Superpowers Public Toolkits

Use when the user wants SOTA SEO/GEO/AEO execution, especially audits, traffic recovery, topical authority, AI visibility, or rank-improvement systems.

This skill is a routing layer. For implementation, load `authority-engine` and its linked reference `references/seo-superpowers-public-toolkits.md`.

## Source synthesis
Best parts distilled from:
- `aaron-he-zhu/seo-geo-claude-skills`: primary strategy/workflow source for topical authority, keyword/content planning, GEO optimization, technical audits, rank tracking, CORE/E-E-A-T/CITE-style gates, and controlled evolution.
- `metawhisp/best-aeo-skill`: AEO/GEO measurement layer — 4-vector 0-100 score, 33-style evidence collector model, confidence labels, AI-citation readiness, llms.txt/robots/schema/entity checks.
- `caio295/geo-authority-suite-v1.2`: WordPress implementation inspiration only — Schema.org entities, JSON-LD, llms.txt, AI-friendly sitemaps, AI indexing directives; never treat as the main strategy or auto-install without backup/conflict/live validation.
- `StanGirard/seo-audits-toolkit`: crawl-first audit architecture; sitemap, extraction, links, headers, images, security, Lighthouse task separation.
- `searchsolved/search-solved-public-seo`: practical SEO scripts for content decay, SERP crossover, topical maps, keyword gaps, entity extraction, anchor relevance, link quality, sitemap extraction, page intent, title/meta optimization.

## Mandatory workflow
1. Load `authority-engine`.
2. Load `authority-engine/references/seo-geo-aeo-self-evolving-enterprise-os.md` for SOTA/self-improving/enterprise SEO/GEO/AEO requests.
3. Use evidence loops: crawl, SERP, authority/entity, outcomes, and post-change monitoring.
4. Use scripts when data exists:
   - GEO/AEO scorecard: `/home/hermes/.hermes/skills/devops/authority-engine/scripts/geo-aeo-enterprise-scorecard.py --url https://example.com --profile publisher --format markdown`
   - Public WordPress crawl: `/home/hermes/.hermes/skills/devops/authority-engine/scripts/public-wordpress-seo-audit.py https://example.com`
   - GSC content decay: `/home/hermes/.hermes/skills/devops/authority-engine/scripts/seo-opportunity-mapper.py content-decay gsc.csv -o decay.csv`
   - SERP crossover: `/home/hermes/.hermes/skills/devops/authority-engine/scripts/seo-opportunity-mapper.py serp-crossover serp.csv -o crossover.csv`
   - Keyword gap: `/home/hermes/.hermes/skills/devops/authority-engine/scripts/seo-opportunity-mapper.py keyword-gap own.csv competitor.csv -o gaps.csv`
5. For page planning, use `/home/hermes/.hermes/skills/devops/authority-engine/templates/page-spec-template.md`.
6. Every serious report must include evidence labels (`Confirmed`, `Likely`, `Hypothesis`), self-critique, and T+14/T+45/T+90 monitoring plan when outcome measurement matters.
7. Never claim rankings, volume, traffic, or AI citations without live data or user-provided exports.

## Decision rules
- SERP overlap 50%+: consolidate/single target or cannibalization fix.
- SERP overlap 25–50%: related sibling/subhub, differentiated angle.
- SERP overlap 1–25%: separate intent/page.
- Content decay 20–50% click loss from peak: moderate refresh.
- Content decay 50%+ click loss: major republish/rebuild.
- Important page with low internal links: high-priority link equity fix.
- Page without direct-answer/question blocks: weak AEO/GEO readiness.

## Output contract
Report exact evidence, affected URLs/queries, intervention type, before/after verification, and remaining unknowns.