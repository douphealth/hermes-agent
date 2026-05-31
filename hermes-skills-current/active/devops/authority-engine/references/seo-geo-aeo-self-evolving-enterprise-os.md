# SEO/GEO/AEO Self-Evolving Enterprise OS

Use this reference when the user asks for maximum/SOTA/enterprise SEO, GEO, AEO, topical authority, AI visibility, WordPress portfolio growth, self-critique, self-optimization, or self-evolving SEO workflows.

This layer fuses the best reusable ideas from:

- `aaron-he-zhu/seo-geo-claude-skills` — main strategic workflow library for topical authority, keyword/content planning, GEO optimization, technical audits, rank tracking, CORE/E-E-A-T/CITE-style quality gates, and repeatable SEO ops.
- `metawhisp/best-aeo-skill` — measurable AEO/GEO audit model: 4-vector 0-100 score, confidence-labeled findings, evidence collectors, AI-citation readiness checks, llms.txt/robots/schema/entity/accessibility review.
- `caio295/geo-authority-suite-v1.2` — WordPress implementation inspiration only: Schema.org entities, JSON-LD, llms.txt, AI-friendly sitemaps, and AI indexing directives. Treat as immature/optional; never install or recommend as the primary strategy without backup, plugin-conflict review, and live validation.

Local source mirrors, for inspection only:

- `/home/hermes/vendor/seo-geo-repos/seo-geo-claude-skills`
- `/home/hermes/vendor/seo-geo-repos/best-aeo-skill`
- `/home/hermes/vendor/seo-geo-repos/geo-authority-suite-v1.2`

## Non-negotiable operating principles

1. **No magic ranking claims.** Do not say a change will boost rankings/traffic/citations unless backed by live data, GSC/Bing exports, ranking tools, or measured post-change outcomes.
2. **Evidence before recommendations.** Every finding must be labeled:
   - `Confirmed`: directly observed in crawl/source/API/export.
   - `Likely`: inferred from 2+ evidence sources.
   - `Hypothesis`: strategic judgment; needs validation.
3. **Technical before prose when blocked.** If indexing, robots, canonicals, status codes, JS accessibility, schema validity, or crawlability are broken, those cap SEO/GEO performance.
4. **Yoast-first for Alexiios WordPress sites unless told otherwise.** Avoid duplicate SEO/schema plugins. Treat Yoast as the control plane and add lightweight custom code only after conflict checks.
5. **Per-post source separation.** Keep each article/page’s facts, sources, schema, affiliate products, images, and internal links distinct. No cross-post fact leakage.
6. **Affiliate compliance.** No fake prices, ratings, specs, claims, or review language. Amazon links use `papalex-20` where applicable, `rel="sponsored nofollow"`, and disclosure before first affiliate link.
7. **AI visibility means retrievable + quotable + attributable.** Build direct answer blocks, citations, entity clarity, JSON-LD, llms.txt guidance, and stable crawl paths.
8. **Self-evolution is controlled, not reckless.** Propose/patch skills only from observed failures, repeated wins, repo evidence, or user feedback; preserve rollback and validation notes.

## Enterprise workflow stack

### Layer 0 — Mission classifier

Classify the task as one or more:

- `technical-indexation-recovery`
- `single-page-surgical-refresh`
- `cluster/topical-map-buildout`
- `wordpress-live-implementation`
- `GEO/AEO/AI-citation-audit`
- `content-decay/recovery`
- `SERP-crossover/cannibalization`
- `affiliate-commercial-upgrade`
- `trust/entity/E-E-A-T hardening`
- `schema/llms/AI-discovery-file implementation`
- `monitoring/rank/citation-feedback loop`

Load relevant Authority Engine references after classification.

### Layer 1 — Evidence intake

Minimum evidence by task:

- **Public crawl:** status, canonical, title, meta, H1-H6, word count, internal/outbound links, images/alt, schema, robots, sitemap, llms.txt.
- **WordPress authenticated context when editing:** post/page ID, status, slug, content, Yoast meta, categories/tags, featured image, media candidates, revisions/backups.
- **Search evidence where available:** GSC clicks/impressions/queries/pages, Bing Webmaster, rank tracker, SERP/PAA/autocomplete, competitor pages, sitemap inventory.
- **AI visibility evidence:** robots access for GPTBot/ClaudeBot/PerplexityBot/Google-Extended, llms.txt, schema, concise answer blocks, citation/source density, entity clarity, markdown/plain accessibility.

If premium data is unavailable, say so. Do not invent keyword volume, KD, trend direction, rankings, traffic, backlinks, or AI citations.

### Layer 2 — 4-vector GEO/AEO score

Use a 0-100 composite score inspired by `best-aeo-skill`. Default weights:

- Technical Accessibility: 20%
- Content Citability: 35%
- Structured Data: 20%
- Entity & Brand Signals: 25%

Profile overrides:

- Publisher/news/affiliate informational: Citability 45%, Technical 15%, Schema 20%, Entity 20%.
- Ecommerce/commercial review: Schema 32%, Citability 25%, Technical 18%, Entity 25%.
- Local: Entity 35%, Citability 25%, Schema 22%, Technical 18%.
- SaaS/tools: Schema 25%, Citability 32%, Entity 25%, Technical 18%.

Score bands:

- 86-100: Excellent — maintain freshness and monitor.
- 68-85: Good — apply top 3 fixes.
- 36-67: Foundation — full audit and fix all high-impact gaps.
- 0-35: Critical — technical/schema first.

Run local helper where useful:

```bash
python3 ~/.hermes/skills/devops/authority-engine/scripts/geo-aeo-enterprise-scorecard.py \
  --url https://example.com \
  --profile publisher \
  --format markdown \
  --out ./geo-aeo-scorecard.md
```

### Layer 3 — CORE/E-E-A-T/CITE quality gate

Before draft/publish, grade content against:

- **Comprehensiveness:** covers the actual intent, sub-questions, exceptions, definitions, comparisons, and next steps.
- **Originality/information gain:** adds useful frameworks, examples, calculators, checklists, diagrams, or decision aids beyond commodity SERP summaries.
- **Readability/mobile:** short paragraphs, scannable headings, answer blocks, tables only when useful, no walls of text.
- **Evidence:** source-backed facts, clear dates, named entities, methodology, no fabricated stats.
- **Trust:** author/editor/reviewer context where legitimate, disclosure, privacy/contact/about signals, organization consistency.
- **Extractability:** direct 40-60 word definitions, concise lists, FAQ/PAA sections, schema that matches visible content.
- **Citations:** outbound authoritative references for claims that need support; avoid linking only to commercial/affiliate targets.

Veto publish if: unsupported YMYL advice, fake reviews/prices/ratings, hidden schema, broken canonical/indexability, duplicate H1 chaos, irrelevant internal links, or unverified affiliate claims.

### Layer 4 — Topical authority engine

For every strategic topic:

1. Define the pillar/hub page.
2. Map support articles by intent: definition, how-to, comparison, best/list, alternatives, troubleshooting, statistics, templates, case studies, reviews, local/industry modifiers.
3. Determine parent/sibling/child links and exact natural anchors.
4. Identify cannibalization by SERP overlap, not title similarity alone.
5. Build `first-post gate`: do not scale a cluster until the first page proves quality, indexability, render, schema, and internal-link model.
6. Refresh existing pages before creating new thin pages unless intent demands a new URL.

Output for topical maps:

- Pillar URL/status
- Missing support URLs
- Existing pages to refresh/consolidate
- Internal link graph
- Entity coverage map
- Evidence gaps
- Publishing order
- KPI/measurement plan

### Layer 5 — WordPress implementation layer

Before live edits:

1. Confirm site credentials/source path safely; never print secrets.
2. Fetch original content/meta and save timestamped backup.
3. Identify WP route: REST, XML-RPC, origin bypass, or admin/browser fallback.
4. Confirm Yoast fields and schema plugin conflicts.
5. Apply smallest effective change set.
6. Purge/bypass cache with exact URL query strings.
7. Verify public plain + cache-busted HTML, REST output, schema parseability, links, mobile/desktop render, and no plugin overlay breakage.

For llms.txt / AI discovery:

- Verify robots does not block needed AI bots.
- Add llms.txt only when source URLs are stable and valuable.
- Prefer concise, curated markdown guidance over dumping the whole sitemap.
- If using a plugin, test duplicate schema/robots/sitemap conflicts first.

### Layer 6 — Self-critique loop

Every audit/draft/implementation must include a compact self-critique:

- What evidence was used?
- What evidence was missing?
- Which recommendations are confirmed vs likely vs hypothesis?
- What could backfire?
- Which change has highest expected ROI and lowest risk?
- What must be verified after publish?
- What should be tracked at T+14/T+45/T+90?

### Layer 7 — Outcome feedback and self-evolution

For serious campaigns, create a feedback record outside persistent memory unless the user asks for durable tracking. Suggested artifact:

```yaml
url: https://example.com/post
profile: publisher
predicted_geo_score: 72
audit_date: 2026-05-30
primary_queries:
  - "best affiliate marketing tools for beginners"
  - "how to start affiliate marketing without a website"
first_measurement_due: 2026-06-13
next_measurements: [T+14, T+45, T+90]
evidence_mode: tool_backed | user_provided | unavailable
```

Measure:

- GSC clicks/impressions/query movement
- indexing state
- target query rankings if rank tools available
- AI citation/mention behavior in ChatGPT, Perplexity, Claude, Gemini, Google AI Overviews if tools/user evidence available
- snippets/PAA capture
- affiliate/conversion movement if analytics available

Skill evolution triggers:

- repeated audit miss
- user correction
- failed publish/cache/schema/Yoast workflow
- recurring blocker across sites
- new validated repo/tool method
- measured GEO score drift > 15 points across 10+ records

When triggered, patch the relevant skill/reference with:

- evidence source
- new rule/procedure
- validation command/checklist
- rollback note

Do not create automatic background self-modification or claim autonomous SEO gains without measurements.

## Standard output format for SOTA SEO/GEO/AEO work

Use this compact structure unless the user asks for a full report:

1. **Objective**
2. **Evidence used / unavailable**
3. **Scorecard**: Technical, Citability, Schema, Entity, composite GEO/AEO score
4. **Critical blockers**
5. **High-ROI actions** ranked by impact/risk
6. **Implementation plan** or exact changes applied
7. **Validation evidence**
8. **Self-critique / unknowns**
9. **T+14/T+45/T+90 monitoring plan**

## Repo-specific usage decisions

- Use `aaron-he-zhu/seo-geo-claude-skills` as the broad workflow inspiration and governance model.
- Use `best-aeo-skill` for scoring, evidence collectors, confidence labels, and AI-citation readiness checks.
- Use `geo-authority-suite-v1.2` only as a possible WP implementation concept; do not install automatically. Prefer Yoast-compatible custom output or a vetted plugin after backup/conflict analysis.

## Fast commands

Public WordPress audit:

```bash
python3 ~/.hermes/skills/devops/authority-engine/scripts/public-wordpress-seo-audit.py https://example.com --max-pages 25 --out ./audit
```

GEO/AEO scorecard:

```bash
python3 ~/.hermes/skills/devops/authority-engine/scripts/geo-aeo-enterprise-scorecard.py --url https://example.com --profile publisher --format json --out ./scorecard.json
```

Enterprise toolchain where external CLIs are available:

```bash
python3 ~/.hermes/skills/devops/authority-engine/scripts/enterprise-geo-aeo-runner.py --url https://example.com --sitemap https://example.com/sitemap_index.xml --max-urls 50 --out ./geo-aeo-run
```
