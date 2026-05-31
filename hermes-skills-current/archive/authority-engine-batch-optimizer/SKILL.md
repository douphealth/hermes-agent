---
name: authority-engine-batch-optimizer
description: Archive-scale SEO optimization system for auditing, scoring, prioritizing, and batching page upgrades across a WordPress site or content corpus. Designed for maximum ROI, topical authority growth, AEO/GEO gains, and efficient rollout.
version: 1.0.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [seo, wordpress, batch-optimization, audit, prioritization, topical-authority, aeo, geo, internal-linking]
    triggers: ["batch seo optimization", "archive optimization", "sitewide seo pass", "optimize all posts", "seo rollout queue", "money page prioritization"]
---

# Authority Engine Batch Optimizer

Use this when the user wants archive-scale execution instead of one-off page work.

This is the system for:
- inventorying posts/pages
- scoring opportunity at scale
- prioritizing high-ROI pages
- batching additive upgrades
- rolling out trust/internal-link/AEO/GEO improvements across many URLs
- sequencing cluster expansion and cleanup

## Mandatory loads
Load these before serious execution:
- `devops/authority-engine`
- `devops/authority-engine-wordpress-execution`
- `devops/wordpress-commercial-cluster-builder`
- `devops/enterprise-ai-seo-competitor-mining`

Load conditionally when relevant:
- `devops/faq-schema-and-answer-box-optimizer`
- `devops/wordpress-sota-seo-content-system`
- `devops/wordpress-category-hub-architecture`
  - `devops/yoast-snippet-layer-remediation`
  - `wp-rest-cloudflare`

Also use this skill for archive-scale affiliate monetization gap audits, such as finding commercial/review/best/product-intent URLs that should contain Amazon affiliate links but do not.

## Mission
Turn a large archive into a prioritized compounding SEO system instead of a pile of disconnected URLs.

## Core principles
1. Not all pages deserve equal effort.
2. Traffic alone is not the priority; traffic × monetization × fixability × authority leverage wins.
3. Additive upgrades beat destructive rewrites for large archives unless a page is structurally broken.
4. Upgrade clusters, not isolated URLs.
5. Build repeatable upgrade patterns and deploy them in waves.
6. Track blockers separately so plugin/cache issues do not stall body-layer wins.

### Affiliate monetization gap audit
Use this when the user asks which URLs should have affiliate links, Amazon links, product CTAs, or monetized buyer links but currently do not.

Recommended workflow:
1. Inventory all publishable content through WordPress REST, including `posts`, `pages`, and any relevant custom post types exposed by `/wp-json/wp/v2/types`.
2. Detect existing affiliate coverage in both stored REST content and public live HTML. For Amazon, match `amazon.`, `amzn.to`, `a.co/`, and known store IDs such as `papalex-20` when relevant.
3. Score “must-have” candidates by commercial intent signals: `/review/`, `/best-`, `/buying-guide/`, product-category paths, product/brand terms, titles containing “best”, “review”, “top”, “vs”, “buyer’s guide”, “tested”, or “where to buy”, and content containing price/check-price/buy/pros-cons language.
4. Separate confirmed money leaks from secondary contextual opportunities. Do not over-label generic workout, diet, recipe, calculator, or informational articles as must-have affiliate pages unless they contain clear product intent.
5. Verify the final candidate set against the live public URL, not just REST content, because snippets/widgets/cache layers can inject affiliate links outside `content.raw`.
6. Export a CSV/JSON artifact under `/tmp` with URL, post type, ID, title, score, reason markers, live status, affiliate-link count, and priority bucket before reporting.

## Batch workflow

### Phase 1 — inventory the corpus
Collect for every relevant URL where possible:
- post/page ID
- URL
- title
- post type
- category / taxonomy position
- modified date
- word-count estimate
- commercial intent markers
- obvious cluster/topic label
- trust-sensitive vs low-trust-sensitive classification

### Phase 2 — opportunity scoring
Score each URL on 0–5 or low/medium/high for:
- commercial value
- ranking potential
- existing authority / internal-link leverage
- snippet / AEO potential
- AI Overview / GEO potential
- freshness need
- trust weakness
- structural weakness
- ease of additive improvement
- duplication / cannibalization risk

#### Search Console + Bing Webmaster opportunity mining
Use this when the user asks to boost organic traffic from existing signals instead of guessed keyword lists.
- Pull recent performance data from Google Search Console and Bing Webmaster Tools where credentials/API keys are available.
- Prefer the last ~90 days, ending 2–3 days ago for GSC final data lag.
- Query by `page,query` in GSC and aggregate to page level; preserve the highest-gap queries for each page.
- Pull Bing page/query stats when available and merge by canonical URL/domain.
- Score high-impression, low-click, fixable pages aggressively, especially positions 2–20 with clear CTR/snippet gaps.
- Prioritize pages with strong impressions and near-page-one positions before speculative new content.
- Export a machine-readable CSV/JSON opportunity file under `/tmp` before editing so the queue can be reused.
- For portfolio-scale or multi-wave runs, maintain a processed-URL registry/manifest and exclude already-upgraded URLs when generating the next queue; normalize URLs carefully so trailing-slash variants, root/category duplicates, and canonical permalink variants do not cause repeated work or wrong-object edits.
- After each wave, generate and save the next highest-ROI queue before reporting completion so execution can resume without re-mining the full dataset.
- Treat internal GSC/Bing metrics, opportunity scores, positions, impressions, CTR gaps, and queue labels as private operator data only; never publish them as reader-facing text in posts or pages.
- Turn the first wave into additive, query-aligned quick-answer/FAQ/internal-link blocks rather than broad rewrites unless the page is broken.

### Phase 3 — page classes
Classify each page into one of these action classes:
- money page: immediate upgrade
- near-money support page: upgrade soon
- authority support page: useful cluster support
- trust asset: strengthen and route links to it
- thin / weak / duplicate: consolidate, repurpose, or deprioritize
- archive filler: leave alone unless leverage improves

### Phase 4 — queue design
Build prioritized queues:
1. quick wins
   - strong intent + weak execution + easy additive upgrade
2. money-page lifts
   - high-value commercial pages needing trust, links, and stronger extraction assets
3. cluster reinforcement
   - sibling/support pages needed to strengthen high-value hubs
4. trust-layer rollout
   - editorial policy, review methodology, author/about/disclosure routing
5. cleanup queue
   - duplicates, cannibalization, thin pages, stale pages, orphan pages

### Phase 5 — upgrade patterns by queue

#### Quick-win batch
Use when pages are already decent but under-optimized.
Apply:
- quick-answer / intent note near the top
- related-guides block
- next-step CTA
- better trust routing
- duplicate-H1 cleanup if needed

#### Money-page batch
Apply:
- tighter title/H1/query alignment
- stronger opening summary
- trust/proof/methodology routing
- gap section covering what weak competitors miss
- comparison/checklist/FAQ modules where useful
- dense internal links from the cluster

#### Cluster-support batch
Apply:
- parent/sibling links
- answer-first intros
- extraction-friendly block
- explicit topical differentiation from nearby URLs
- next-step routing into money pages or hubs

#### Trust batch
Apply:
- strengthen canonical trust pages
- normalize internal links toward canonical trust assets
- convert duplicate trust pages into support pages when redirects are unavailable
- ensure commercial pages visibly route to trust assets

#### Cleanup batch
Apply:
- identify duplicates and cannibalization
- decide canonical winner
- convert weaker pages to support pages, merge targets, or deprioritized remnants
- fix orphaning and under-linking

## Batch scoring model
A page deserves top priority when it scores high on most of:
- money intent
- ranking upside
- snippet/AIO potential
- cluster leverage
- fixability by additive upgrade
- trust weakness that can be improved quickly

A page drops in priority when it is:
- low-value
- low-leverage
- duplicative
- far outside the main topical map
- costly to rebuild with little upside

## Standard rollout order
1. canonical trust assets
2. top money pages
3. near-money support pages
4. internal-link reinforcement from strongest pages
5. snippet / FAQ / answer-box passes
6. cluster-expansion pages
7. cleanup / consolidation pages
8. lower-value archive cleanup

## Deliverables
Every batch optimization run should try to produce:
- full URL inventory or high-value subset inventory
- scored opportunity table
- prioritized rollout queue
- cluster map or topic grouping
- trust-link normalization plan
- internal-link reinforcement plan
- batch pattern templates
- blocker map for plugin/cache/head-layer issues
- recommended next 10–20 pages to touch

## Verification contract
For each batch or wave, verify:
- prioritized pages were actually touched
- body-layer improvements render live
- H1 structure stays valid
- internal links are live
- trust links are live
- every newly inserted related-guides / cluster-link block has its hrefs crawled with redirects followed, and any 404/stale-path target is patched before final reporting
- plain vs cache-busted URLs are compared on sampled pages
- blocker patterns are documented, not hidden
- next wave is clearly defined

## Output contract
Report:
- corpus size reviewed
- scoring method used
- highest-priority URLs or clusters
- queue buckets created
- batch patterns selected
- blockers detected
- pages completed in the current wave
- next recommended wave

## Quality bar
A batch optimizer is only good if it helps the operator spend effort where compound returns are highest. If it treats every URL equally, it is failing.