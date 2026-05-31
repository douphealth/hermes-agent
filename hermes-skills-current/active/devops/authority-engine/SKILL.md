---
name: authority-engine
description: Unified enterprise SEO execution system for planning, writing, rewriting, clustering, and upgrading content to maximize #1 rankings, topical authority, Featured Snippets, AI Overviews, answer-engine extraction, AI visibility, and conversions. Includes non-plugin AI discovery endpoint patterns in references/ai-discovery-worker-geo-aeo-pattern.md.
version: 1.0.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [seo, geo, aeo, ai-visibility, topical-authority, content-strategy, wordpress, serp, conversion, ymyl, medical-content]
    triggers: ["authority engine", "rank number one", "maximum seo quality", "geo optimization", "aeo optimization", "ai visibility", "topical authority", "enterprise seo content", "ymyl medical content", "health content rewrite", "medical diagnosis page"]
---

# Authority Engine

Use this when the user wants the strongest possible SEO content system rather than a single isolated article pass.

This is the orchestration layer for:
- blue-link rankings
- topical authority
- Featured Snippets
- People Also Ask
- voice-answer extraction
- AI Overviews
- Bing Copilot / Perplexity / LLM citation
- E-E-A-T hardening
- internal-link authority routing
- conversion-aware content architecture

## Mandatory loads
Load these before serious execution:
- `devops/wordpress-sota-seo-content-system`
- `devops/serp-driven-rewrite-playbook`
- `devops/enterprise-ai-seo-competitor-mining`
- `devops/faq-schema-and-answer-box-optimizer`
- `devops/wordpress-commercial-cluster-builder`

Load conditionally when relevant:
- `devops/authority-engine-command-center` for intake routing, workflow selection, and layer handoffs
- `devops/authority-engine-memory-and-kpi-loop` for refresh triggers, KPI review cadence, and recurring optimization loops
- `devops/authority-engine-trust-and-entity-graph` for entity consistency, trust architecture, and AI visibility reinforcement
- `devops/authority-engine-cluster-factory` for pillar/cluster architecture, support-page planning, and internal-link blueprints
- `devops/authority-engine-snippet-and-ai-overview-strike-system` for snippet capture, PAA extraction, and AI Overview section design
- `devops/authority-engine-site-audit` for technical/content/trust/schema/internal-link auditing and remediation planning
- `devops/authority-engine-serp-lab` for query modeling, SERP pattern extraction, and page-brief generation
- `devops/authority-engine-wordpress-execution` for push-button WordPress REST deployment
- `devops/authority-engine-batch-optimizer` for archive-scale audits, scoring, and rollout queues
- `devops/wordpress-rest-commercial-seo-funnel` for REST-based WordPress execution
- `devops/wordpress-category-hub-architecture` for hub/taxonomy work
- `devops/wordpress-trust-blocks-and-proof-elements` for trust UI
- `devops/premium-wordpress-html-blocks` for premium theme-safe modules
- `devops/wordpress-image-alt-caption-snippet-optimizer` for image/search-surface refinement
- `devops/wordpress-eeat-remediation-via-rest` for sitewide trust hardening

## Mission
Turn content operations into an authority engine that compounds rankings, citations, topical coverage, and conversions over time.

## Core model
Every serious content task must be evaluated across 8 layers:
1. technical readiness
2. SERP intent fit
3. on-page structure and snippet readiness
4. topical authority contribution
5. AEO / answer extraction strength
6. GEO / AI Overview citation strength
7. E-E-A-T / entity trust strength
8. conversion and internal-link routing

Do not optimize only one layer and call the job done.

## High-risk WordPress claim cleanup

When SEO/GEO/AEO work involves unsupported claims, invented stats, fake/future algorithm references, autoblogging/AI-risk language, or source-widget contradictions, use `references/wordpress-risk-claim-cleanup-playbook.md` before editing. The required pattern is: exact risky phrase list → raw backup → source/meta/custom-field cleanup → visible citations or relabeling → cache purge → raw + cache-busted public verification. Never claim reindexing unless Search Console/IndexNow credentials prove it.

## SEO Superpowers public-toolkit layer
This skill has been upgraded with distilled workflows from `aaron-he-zhu/seo-geo-claude-skills`, `StanGirard/seo-audits-toolkit`, and `searchsolved/search-solved-public-seo`. For SEO/GEO/AEO audits, ranking recovery, topical authority, internal links, AI visibility, content decay, SERP crossover, keyword gaps, or page specs, consult `references/seo-superpowers-public-toolkits.md` and use the scripts/templates when data is available.

## Self-evolving enterprise SEO/GEO/AEO OS layer
For any SOTA / enterprise / premium / self-improving / self-optimizing / AI visibility / topical authority request, also load `references/seo-geo-aeo-self-evolving-enterprise-os.md`. This is the current top-level operating system distilled from:
- `aaron-he-zhu/seo-geo-claude-skills` as the main strategy/workflow/governance source,
- `metawhisp/best-aeo-skill` as the measurable GEO/AEO scorecard and confidence-label model,
- `caio295/geo-authority-suite-v1.2` only as an optional WordPress implementation concept after backup/conflict validation.

Use the bundled zero-dependency scorecard before or alongside major recommendations when a public URL is available:

```bash
python3 ~/.hermes/skills/devops/authority-engine/scripts/geo-aeo-enterprise-scorecard.py \
  --url https://example.com \
  --profile publisher \
  --format markdown \
  --out ./geo-aeo-scorecard.md
```

Every serious SEO/GEO/AEO output must include evidence labels (`Confirmed`, `Likely`, `Hypothesis`), an explicit self-critique, and a T+14/T+45/T+90 monitoring plan when outcome data matters. Do not claim rankings, organic traffic, AI citations, or visibility improvements without measured evidence.

## Codex SEO superpowers layer
When the user asks to make Hermes agents stronger at SEO/GEO/AEO/AI visibility, mentions `AgriciDaniel/codex-seo`, asks for `/seo audit`, `/seo geo`, `/seo content`, `/seo schema`, `/seo cluster`, `/seo google`, `/seo performance`, or asks for “1000000000x” SEO agent superpowers, load `codex-seo-superpowers` first. Use the vendored Codex SEO suite at `/home/hermes/.hermes/vendor/codex-seo` plus GEO Optimizer at `/home/hermes/.hermes/vendor/geo-optimizer-skill` through `~/.hermes/skills/devops/codex-seo-superpowers/scripts/hermes_codex_seo_runner.py`. Treat `madeburo/GEO-AI-Woo` as a WordPress implementation candidate/pattern only after Yoast/schema/robots/cache conflict gates and explicit plugin approval. Treat `elmohq/elmo` as the monitoring architecture for prompt/citation snapshots, not as proof of visibility unless deployed.

## Enterprise GEO/AEO toolchain layer
This skill now has a first-class external toolchain based on `AgriciDaniel/codex-seo`, `Auriti-Labs/geo-optimizer-skill`, `madeburo/GEO-AI-Woo` implementation patterns, `elmohq/elmo` monitoring patterns, and `alexpospekhov/searchstack-aeo` / PyPI `searchstack`. When the user asks for SOTA, enterprise, premium, AI visibility, GEO, AEO, llms.txt, answer-engine optimization, ChatGPT/Perplexity/Claude/Gemini citations, or “10000000000x more powerful” SEO workflows, load `codex-seo-superpowers`, load `references/enterprise-geo-aeo-toolchain.md`, and execute the bundled runner where useful:

## Yoast-first WordPress AI visibility layer
When the user says their WordPress sites use Yoast, treat Yoast as the primary SEO control plane. Do not recommend Rank Math, do not replace Yoast, and do not stack duplicate SEO/schema plugins without conflict analysis. For Yoast-based SEO/GEO/AEO/AI-visibility work, load `references/yoast-first-ai-visibility-superpower-layer.md`. Use it to audit Yoast metadata/canonicals/robots/schema/sitemaps, evaluate RankReady-style llms.txt/markdown/crawler features, compare lightweight WordPress AI Visibility-style robots/llms/business metadata, and prevent duplicate schema or robots conflicts before implementation.

## Surgical SEO Intelligence Engine layer
For existing blog-post optimization, URL-only intake is the default: if the user gives only a URL, infer keywords, intent, audience, internal links, external sources, image gaps, Yoast fields, entity gaps, and surgical edits instead of asking for all details. For SOTA surgical blog-post work, load `references/surgical-semantic-seo-editor.md` and `references/surgical-seo-intelligence-engine.md`. Prefer first-party GSC data, then crawl/sitemap context, then external SEO/SERP/competitor data such as DataSEO MCP, then semantic clustering. Always separate observed data from recommendations and never invent search volume, KD, rankings, traffic, backlinks, or AI citations. When the user asks for maximum/superpower execution, uses extreme multipliers, or says the changes are too small, use `references/surgical-seo-visible-impact-mode.md` plus `references/surgical-seo-max-force-token-efficient-workflow.md`: add substantial live-visible utility modules without destructive full rewrites, while keeping chat output artifact-first and compact.

```bash
python3 ~/.hermes/skills/devops/authority-engine/scripts/enterprise-geo-aeo-runner.py \
  --url https://example.com \
  --sitemap https://example.com/sitemap_index.xml \
  --max-urls 50 \
  --out ./seo-audit-example
```

Use `geo-optimizer-skill` as the improvement/audit engine: robots, llms.txt, llms-full.txt, JSON-LD, meta, brand/entity signals, AI discovery files, JavaScript accessibility, crawler access, prompt-injection risk, RAG chunk readiness, content decay, and platform citation readiness. Use `searchstack` as the monitoring/outcome layer: AI citations, Google AI Overview checks, GSC movement, technical audits, llms validation, and reports. Do not claim AI visibility improvements until live files/pages are verified and outcome monitoring is configured or explicitly unavailable.

New execution assets:
- `scripts/enterprise-geo-aeo-runner.py` runs `geo` and `searchstack` through `uvx`, stores machine-readable audit artifacts, generates a staging `llms.txt`, and creates a `.searchstack.toml` template.
- `references/enterprise-geo-aeo-toolchain.md` documents the full crawl → fix → validate → monitor loop and exact CLI commands.
- `scripts/public-wordpress-seo-audit.py` now checks H1/meta/canonical/schema parse validity, image alt gaps, weak AEO/GEO structure, internal anchor quality, llms.txt, page scorecards, and internal link targets.
- `scripts/seo-opportunity-mapper.py` runs content-decay analysis from GSC exports, SERP crossover/cannibalization decisions from SERP CSVs, and keyword-gap extraction from own vs competitor exports.
- `templates/page-spec-template.md` now includes evidence inputs, SERP crossover, topical-map placement, GEO/AI visibility, internal-link anchors, and a 12-point scorecard.

Accuracy rule: do not invent rankings, traffic, search volume, keyword demand, trend direction, AI citations, SERP overlap, NeuronWriter scores, or publish status. Use live crawl/search/export/evidence when possible; otherwise label recommendations as structural/probabilistic. When the user asks for the “best,” “actual,” “accurate,” or “precise” keywords/entities for blog posts, treat this as an evidence-gated requirement: gather or request access to trusted keyword/entity sources (Google Keyword Planner, Google Trends, GSC, live SERP/PAA/autocomplete, reputable SEO tools, competitor pages) before finalizing the page spec or content. If a premium source is inaccessible, say which evidence sources were used and avoid implying Keyword Planner/Trends verification happened. Follow `references/keyword-entity-evidence-workflow.md` for the concrete research, filtering, placement, and public-copy QA pattern.

NeuronWriter bridge rule: when a WordPress content update depends on NeuronWriter, follow `references/neuronwriter-wordpress-rewrite-pipeline.md`, `references/neuronwriter-wordpress-bridge.md`, and `references/neuronwriter-backend-automation.md` before editing/publishing. For login/session, project discovery, `/backend/new-analysis` payload, and durable API pitfalls, also consult `references/neuronwriter-backend-api-quirks.md`. Capture and provide the direct NeuronWriter editor URL (`/analysis/view/...`) as soon as it is opened; distinguish local draft files from content actually pasted into NeuronWriter and from content actually published on WordPress; do not lead with filesystem paths when the user asks for “the URL.”

## When to use
- the user wants “maximum quality” SEO work
- the user wants stronger rankings, not just nicer copy
- the user wants a cluster, hub, or category buildout
- the user wants AI Overview / answer-engine visibility
- the user wants traffic plus conversion support
- the user wants sitewide content standards upgraded
- the user reports GSC/Bing collapse, near-zero impressions/clicks, falling indexed pages, or urgent indexation/AI-visibility issues across WordPress properties; in this mode load `references/emergency-indexation-ai-visibility-playbook.md` and execute a first remediation wave before lengthy explanation
- the user asks to index/submit all website URLs across the portfolio; in this mode load `references/portfolio-indexation-submission-playbook.md`, discover sitemap/static/app URLs, submit sitemaps/IndexNow where credentials allow, retry smaller batches on 403/422, and report accepted vs blocked counts without implying guaranteed indexing

When the user gives an exact sitemap as the inventory source, use that sitemap only. Do not silently broaden to `sitemap_index.xml`/WP core sitemaps or rerun basic audits. For URL-level growth sprint work, use `references/url-level-post-sitemap-growth-sprint.md` and emit CSV/JSON/MD artifacts with per-URL actions. When the audit artifacts already exist and the user says to proceed/execute implementation, do not re-audit the full site; load `references/wordpress-seo-implementation-sprint.md`, operate from the artifacts, edit only verified target URLs, preserve unique content before redirects, and produce batch changelogs plus final QA.

## Anti-slop principles
- never ignore a user-specified source of truth; if they say use `post-sitemap.xml`, use that exact feed and do not detour into basic sitemap-index audits
- never publish generic AI filler
- never let keyword targets override utility
- never separate content from trust, links, or conversion paths
- never create orphan pages
- never claim metadata/schema improvements without verification
- never call content “enterprise-grade” unless it has information gain
- never rely on unsourced claims in trust-sensitive topics
- never insert affiliate links just because a keyword matches; verify contextual relevance and final tracking/deep links first

## Execution workflow

For WordPress article rewrites that require NeuronWriter scoring before publish, use `references/neuronwriter-wordpress-rewrite-pipeline.md` before editing or publishing. It covers backup, browser/API fallback, term/entity capture, source-backed rewrite, grammar cleanup after term tuning, publish gating, and public QA evidence.

### Phase 1 — classify the mission
Determine whether the task is primarily:
- page rewrite
- page upgrade
- new page creation
- cluster expansion
- topical map creation
- trust-layer remediation
- snippet / FAQ optimization
- GEO / AI citation optimization
- full-site authority buildout

### Phase 2 — technical gate
Before scaling content, check whether obvious technical blockers cap results:
- Core Web Vitals status
- indexability / crawlability
- canonicals / redirect health
- sitemap presence
- broken critical links / server errors
- mobile usability
- obvious page-speed failures

If severe blockers exist, flag them as ranking ceilings while still doing the highest-ROI content work available.

### Phase 3 — query ladder, semantic entity map, and demand geometry
For each target topic:
- define head term
- define close variants
- define modifiers: best, vs, alternatives, cost, problems, mistakes, benefits, risks, timing, audience, location, urgency
- define PAA / FAQ questions
- build a semantic keyword + entity map before drafting or rewriting: primary keyword, secondary terms, SERP/PAA variants, named entities, attributes, product/category entities, adjacent concepts, and user-problem vocabulary; for evidence-gated keyword/entity work use `references/keyword-entity-evidence-workflow.md`
- source keyword/entity candidates from trusted evidence whenever possible: Google Keyword Planner, Google Trends, Google Search Console, live SERP/PAA/autocomplete, competitor ranking pages, schema/entity extraction, reputable SEO tools, and first-party site/search data
- include the actual relevant keywords and entities naturally in headings, answer blocks, body copy, alt/caption text, FAQs, schema, internal anchors, and product/comparison sections where contextually appropriate
- reject raw keyword stuffing: the goal is comprehensive topical coverage and natural language, not visible keyword dumps
- define entities and subtopics required for topical completeness
- define the likely winning page type

### Phase 4 — true competitor discovery
Use SERP overlap, not assumptions.
Capture:
- repeated domains across head, mid-tail, and modifier queries
- repeated page patterns
- trust elements used near the top
- extractable answer formats
- conversion assets attached to ranking pages
- gaps where the market is thin, outdated, vague, or poorly structured

### Phase 5 — opportunity model
For each page or planned page, define:
- dominant intent
- secondary intents that can be satisfied without dilution
- page type
- buyer stage
- snippet targets
- AI Overview targets
- required evidence / source burden
- required trust elements
- internal-link parent / sibling / next-step routes
- CTA / conversion path
- update cadence

### Phase 6 — choose the intervention type
Use one:
- no-new-content quality optimization
- micro-upgrade
- additive rewrite
- consolidation rewrite
- full rebuild
- cluster expansion
- sitewide authority pass

Default to existing-content refinement/additive upgrades unless structure or intent is broken. If the user says they want to “improve/optimize the implementation” but objects to adding content, switch immediately to the no-new-content workflow in `references/no-new-content-quality-optimization.md`: refine existing modules/sections in place, remove generic/repetitive SEO phrasing, fix public REST/render mismatches, and verify plain + cache-busted HTML.

### Phase 6b — app-funnel routing when a freemium tool exists
When a site has a freemium calculator, quiz, planner, or app on a subdomain, treat it as a primary conversion path. Build or recommend a main-domain SEO landing page for the app, then route topical blog posts through contextual CTAs into that page and/or directly into the app when intent is high. Use the pattern in `references/wordpress-freemium-app-funnel-architecture.md`: main domain ranks/explains/trust-builds; subdomain app converts through free result, paid upgrade, email nurture, and affiliate/digital-product upsell.

For REST-published landing pages, follow `references/wp-rest-freemium-landing-page-qa.md`: update by slug, use a single source/live H1, add WebPage/SoftwareApplication/FAQPage/BreadcrumbList schema where appropriate, recursively discover sitemap links for internal authority, page-scope full-width CSS, suppress intrusive TOC/chat/cookie/back-to-top widgets, and complete cache-busted public browser QA before reporting done.

### Phase 7 — build the page spec
Every serious page spec should contain:
- exact query target
- title direction
- H1 direction
- intro angle
- section stack
- entity coverage map
- statistics / citations required
- snippet blocks to include
- FAQ / PAA targets
- schema recommendation
- trust elements
- internal links in / out
- next-step CTA
- freshness signal requirements

### Phase 8 — write for extraction and authority
Every page should usually include:
- answer-first intro
- exactly one H1
- direct-answer paragraphs under high-value H2s
- at least one extraction-friendly asset when useful:
  - definition block
  - ordered steps
  - checklist
  - comparison table
  - pros/cons
  - scenario cards
  - FAQ block
- self-contained paragraphs that still make sense when quoted by AI systems
- decisive language backed by evidence
- visible trust path when the SERP expects proof

### Phase 9 — cluster reinforcement
No important page ships alone.
Ensure:
- hub / pillar relationship is defined
- siblings are linked
- trust pages are linked where appropriate
- next-step conversion route exists
- under-linked pages get authority from stronger pages
- new pages get linked from existing authority pages quickly

### Phase 10 — verify and score
Before claiming completion, verify:
- 200 OK
- one live H1
- public structure matches the plan
- schema exists if added
- answer blocks are present
- internal links are live
- trust / CTA elements are visible
- title/meta checked separately from body when possible

For WordPress REST execution, always run a live public QA pass after edits and repair before reporting done. Crawl sitemap/REST inventory, check all priority URLs, count visible H1s from rendered HTML, sample internal links, test deliberate redirects, and inspect schema on representative posts. For any sitewide runtime filter or MU-plugin content transformation, verify multiple representative post bodies with visible word counts and browser snapshots, not just homepage/status 200, because broad `the_content` filters can collapse article bodies while leaving title/header/metadata intact. Watch for Astra/Kadence-style themes that hide the page title: if a cleanup step demotes/removes body `<h1>` elements, pages such as About may end up with zero live H1s even though the REST title is correct. Fix by adding exactly one manual body H1 or re-enabling the theme title, then re-run QA. Conversely, many themes inject the page title as a live H1 on pages, so custom hub/page content should usually use a styled non-H1 hero title until public HTML proves otherwise; duplicate H1s must be repaired before reporting done. For full article rewrites via REST, back up the exact post, preserve existing monetization/trust modules, verify canonical and cache-busted URLs, and browser-spot-check the rendered page; see `references/wp-rest-sota-article-rewrite-qa.md`. For sitewide sanitation of visible SEO scaffolding, raw keyword/entity dumps, trust contradictions, and pillar hub buildout, follow `references/wordpress-sitewide-seo-sanitation-and-hub-buildout.md`. See `references/wordpress-live-qa-remediation.md` for the concrete H1 remediation pattern.

Then score 0–2 on:
- intent match
- information gain
- snippet readiness
- AIO/GEO readiness
- source quality
- trust strength
- internal-link routing
- conversion path
- freshness signal

## Page architecture standard
Every serious ranking page should try to cover the following where relevant:
- direct answer / definition
- who it is for
- benefits
- risks or downsides
- alternatives
- cost / effort / time
- mistakes
- comparison logic
- steps / process
- FAQ / objections
- next step

Do not force all sections onto all pages. Match the page type and intent.

## AEO operating standard
Use this for snippets, PAA, and voice:
- question-matching H2s
- answer in first 1–2 sentences
- definition blocks at 40–60 words when relevant
- lists for ranked or grouped answers
- steps for procedural queries
- tables for comparisons, specs, costs, and tradeoffs
- concise, spoken-style answers when voice capture is realistic

## GEO operating standard
Use this for AI Overviews and citation-oriented search:
- cite authoritative sources
- use explicit dates / recency markers
- define entities cleanly
- make paragraphs self-contained
- include quotable factual sentences
- include tables and ordered lists
- cover adjacent angles AI systems synthesize
- prefer evidence-backed confidence over hedging fluff

## AI visibility standard
When the user wants broader brand visibility:
- tighten About / author / organization definitions
- reinforce editorial policy / methodology / contact / trust pages
- recommend original data, frameworks, or case studies
- align brand/entity facts across the site and off-site profiles
- track whether AI systems actually cite the brand

## Output contract
For each task, report:
- objective
- page(s) or cluster(s) touched
- intervention type used
- query / intent model
- snippet and AIO targets
- trust and evidence changes
- internal-link / cluster changes
- conversion-path changes
- what was verified live
- what remains blocked by platform/plugin/access constraints

## Quality bar
A page or cluster is not “maximum quality” unless it is:
- stronger than generic SERP clones
- easier to extract answers from
- easier to trust
- better connected internally
- more current
- more citation-worthy
- more commercially intelligent


## Consolidated Reference Index

The following formerly separate narrow skills have been absorbed into this umbrella. Load the listed reference file only when that specific provider, failure mode, or workflow detail is needed.

- Keyword/entity evidence workflow for precise blog-post semantic coverage → `references/keyword-entity-evidence-workflow.md`
- `alexiios-seo-domination-system` → `references/alexiios-seo-domination-system.md`
- `authority-engine-batch-optimizer` → `references/authority-engine-batch-optimizer.md`
- `authority-engine-cluster-factory` → `references/authority-engine-cluster-factory.md`
- `authority-engine-command-center` → `references/authority-engine-command-center.md`
- `authority-engine-memory-and-kpi-loop` → `references/authority-engine-memory-and-kpi-loop.md`
- `authority-engine-serp-lab` → `references/authority-engine-serp-lab.md`
- `authority-engine-site-audit` → `references/authority-engine-site-audit.md`
- `authority-engine-snippet-and-ai-overview-strike-system` → `references/authority-engine-snippet-and-ai-overview-strike-system.md`
- `authority-engine-trust-and-entity-graph` → `references/authority-engine-trust-and-entity-graph.md`
- Public SEO/GEO toolkit synthesis → `references/seo-superpowers-public-toolkits.md`
- Codex SEO superpowers for Hermes agents: AgriciDaniel/codex-seo command routing, GEO Optimizer, GEO-AI-Woo implementation gates, Elmo-style monitoring → load `codex-seo-superpowers` and `references/codex-seo-hermes-superpowers.md`
- Enterprise GEO/AEO toolchain using Codex SEO + Auriti-Labs GEO Optimizer + searchstack monitoring, uvx runner, llms.txt/schema/citation workflow → `references/enterprise-geo-aeo-toolchain.md`
- URL-level post-sitemap SEO/GEO/AEO growth sprint workflow, exact-sitemap source-of-truth rule, and artifact generator → `references/url-level-post-sitemap-growth-sprint.md`; script: `scripts/url_level_post_sitemap_growth_sprint.py`
- Artifact-driven WordPress SEO/GEO/AEO implementation sprint pattern: safe cannibalization decisions, commercial trust modules, claim cleanup, internal-link deployment, and final GSC readiness QA → `references/wordpress-seo-implementation-sprint.md`
- WordPress SEO meta residue cleanup after sprint edits: scoped MU-plugin output-buffer normalization for stale/high-risk meta descriptions, OG/Twitter descriptions, and hub 404 redirects → `references/wordpress-seo-meta-residue-cleanup.md`
- Affiliate link placement accuracy and deployment queues → `references/affiliate-link-placement-accuracy.md`
- Affiliate link operational validation for user-supplied program lists, redirect/body checks, status taxonomy, and sanitized XLSX/CSV/MD master tables → `references/affiliate-link-operational-validation.md`
- Affiliate manager WordPress rollout: map verified offers to high-intent posts, inject compact disclosed CTA boxes, XML-RPC fallback, precision remap, and public verification artifacts → `references/affiliate-manager-wordpress-rollout.md`
- Mice Gone Guide commercial affiliate cluster pattern: preserve informational authority URLs, create new buyer-intent review posts, add bidirectional contextual links, verify ASINs/cache/sitemap → `references/mgg-commercial-affiliate-cluster.md`
- Measurable affiliate revenue system: central offer registry, CTA data attributes, GTM/GA4-compatible `affiliate_click` events, live browser proof, and daily link-health monitoring → `references/measurable-affiliate-revenue-system.md`
- Sitewide affiliate link gap analysis (scan all URLs for missing links) → `references/affiliate-link-gap-analysis.md`
- WordPress freemium app funnel architecture → `references/wordpress-freemium-app-funnel-architecture.md`
- WordPress REST freemium landing-page build + live QA pitfalls → `references/wp-rest-freemium-landing-page-qa.md`
- `authority-engine-wordpress-execution` → `references/authority-engine-wordpress-execution.md`
- `enterprise-ai-seo-competitor-mining` → `references/enterprise-ai-seo-competitor-mining.md`
- `faq-schema-and-answer-box-optimizer` → `references/faq-schema-and-answer-box-optimizer.md`
- `serp-driven-rewrite-playbook` → `references/serp-driven-rewrite-playbook.md`
- `wordpress-category-hub-architecture` → `references/wordpress-category-hub-architecture.md`
- `wordpress-commercial-cluster-builder` → `references/wordpress-commercial-cluster-builder.md`
- `wordpress-eeat-remediation-via-rest` → `references/wordpress-eeat-remediation-via-rest.md`
- `wordpress-live-qa-remediation` → `references/wordpress-live-qa-remediation.md`
- YMYL medical content rewrite — noindex-first safety, named expert reviewer, diagnostic accuracy, disclaimer standards → `references/ymyl-medical-content-rewrite.md`
- WordPress REST SOTA article rewrite/live QA pattern → `references/wp-rest-sota-article-rewrite-qa.md`; AMFS rewrite ZIP/package one-post test publish pitfalls → `references/amfs-rewrite-package-test-publish.md`
- WordPress sitewide SEO sanitation + hub buildout pattern → `references/wordpress-sitewide-seo-sanitation-and-hub-buildout.md`.
- Emergency portfolio indexation + AI visibility recovery via GSC/Bing/WPCode/Cloudflare → `references/emergency-indexation-ai-visibility-playbook.md`
- Portfolio-wide URL discovery and submission to GSC sitemaps, URL Inspection samples, and Bing/IndexNow with retry/blocker reporting → `references/portfolio-indexation-submission-playbook.md`; implementation notes for retrying false fetch errors and REST internal-link reinforcement → `references/portfolio-indexation-execution-notes.md`
- No-new-content quality optimization for existing SEO implementations, including duplicate public post ID mismatch diagnosis → `references/no-new-content-quality-optimization.md`
- Query-led WordPress SEO refresh wave for GSC impression/no-click pages, FAQ/AEO modules, submissions, and LiteSpeed stale-cache fallbacks → `references/wordpress-query-led-seo-refresh-wave.md`
- WordPress + Cloudflare canonical-control remediation for duplicate hosts, React/Lovable route fallbacks, public origins, app subdomains, sitemap cleanup, and GSC consolidation → `references/wordpress-cloudflare-canonical-control.md`; concrete GearUpToFit homepage/privacy/legal/app-subdomain implementation notes → `references/gearuptofit-cloudflare-homepage-canonical-case.md`
- Yoast-first AI visibility layer for WordPress sites that keep Yoast as the SEO control plane, including RankReady and WordPress AI Visibility capability/conflict analysis → `references/yoast-first-ai-visibility-superpower-layer.md`
- Surgical Semantic SEO Editor for existing WordPress blog posts: preserve original voice, plan precise edits, improve semantic entities, GEO/AEO/AI visibility, Yoast fields, internal/external links, images, and trust without full rewrites unless explicitly requested → `references/surgical-semantic-seo-editor.md`
- Surgical SEO visible-impact mode for maximum/superpower runs or user complaints that changes are too small: add substantial live-visible utility modules, tables, protocols, FAQs, and verification targets without destructive rewrites → `references/surgical-seo-visible-impact-mode.md`
- Surgical SEO max-force + token-efficient workflow for extreme multiplier requests and underwhelming first passes: artifact-first edit packs, compact chat output, visible content-delta gates, public TOC/module verification, and no raw HTML/crawl/GSC dumps in chat → `references/surgical-seo-max-force-token-efficient-workflow.md`
- Batch WordPress SOTA SEO surgery for prioritized URL lists: manifest-driven XML-RPC/Cloudflare workflow, per-intent visible modules, all-meta-family updates, compact verification, and stale head-output caveats → `references/batch-wordpress-sota-seo-surgery.md`
- Surgical SEO Intelligence Engine for URL-only blog-post optimization using GSC first-party queries, DataSEO MCP keyword/SERP/competitor data, advertools crawl/sitemap extraction, semantic clustering, query/page opportunity maps, and cannibalization/content-decay detection → `references/surgical-seo-intelligence-engine.md`
- `wordpress-rest-commercial-seo-funnel` → `references/wordpress-rest-commercial-seo-funnel.md`
- `wordpress-sota-seo-content-system` → `references/wordpress-sota-seo-content-system.md`
- `wordpress-trust-blocks-and-proof-elements` → `references/wordpress-trust-blocks-and-proof-elements.md`
- `yoast-snippet-layer-remediation` → `references/yoast-snippet-layer-remediation.md`
- `wp-enterprise-audit` → `references/wp-enterprise-audit.md`
