---
name: authority-engine-serp-lab
description: SERP research and modeling layer for the Authority Engine. Generates query sets, maps winning page types, detects snippet and AI Overview triggers, models competitor patterns, and turns findings into page briefs with information-gain angles.
version: 1.0.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [seo, serp, research, query-expansion, snippets, ai-overviews, competitor-analysis, content-briefs, geo, aeo]
    triggers: ["serp lab", "serp research", "query set generation", "aio mapping", "snippet mapping", "competitor page model", "keyword brief generation"]
---

# Authority Engine SERP Lab

Use this when the user wants a research-grade SERP intelligence layer before writing, rewriting, clustering, or auditing.

This is the system for:
- query-set generation
- modifier expansion
- SERP pattern extraction
- snippet/PAA/AIO trigger mapping
- competitor page-type modeling
- information-gain discovery
- per-keyword or per-cluster brief generation

## Mandatory loads
Load these before serious execution:
- `devops/authority-engine`
- `devops/serp-driven-rewrite-playbook`
- `devops/enterprise-ai-seo-competitor-mining`

Load conditionally when relevant:
- `devops/authority-engine-site-audit`
- `devops/authority-engine-batch-optimizer`
- `devops/wordpress-sota-seo-content-system`
- `devops/faq-schema-and-answer-box-optimizer`
- `devops/wordpress-commercial-cluster-builder`

## Mission
Turn raw keywords into a structured demand map that tells the operator exactly what to publish, how to structure it, what to avoid, and where information gain exists.

## Core principles
1. Search demand is a shape, not a single keyword.
2. Query modifiers reveal page-type expectations.
3. Repeated page formats are stronger signals than isolated pages.
4. Snippet and AI Overview triggers must be modeled separately from blue-link rankings.
5. Information gain matters more than paraphrase.
6. Every SERP read should end in an execution-ready brief or queue, not just observations.

## SERP lab workflow

### Phase 1 — seed term definition
Start with:
- head term
- close variants
- commercial intent variants
- support-question variants
- audience/use-case modifiers
- geography/industry/tool modifiers when relevant

### Phase 2 — query ladder generation
Expand each seed into:
- head terms
- mid-tail terms
- long-tail modifiers
- alternatives/vs terms
- cost/pricing terms
- problem/mistake/risk terms
- best-for / use-case terms
- how-to / checklist / template / examples terms
- statistics / benchmark / trend terms

### Phase 3 — SERP surface mapping
For each query bucket, capture:
- repeated ranking domains
- repeated URL/page formats
- dominant intent class
- snippet/PAA triggers
- AI Overview likelihood
- trust burden
- conversion proximity

### Phase 4 — page-type modeling
Identify which page formats are actually winning:
- guide
- category/hub
- comparison
- alternatives
- use-case page
- template
- checklist
- FAQ
- glossary/definition
- stats page
- tool/calculator
- review page

Then map which formats deserve to exist on the target site.

### Phase 5 — extraction opportunity mapping
For important queries, identify:
- paragraph snippet opportunities
- definition snippet opportunities
- list snippet opportunities
- table snippet opportunities
- step/how-to opportunities
- FAQ/PAA coverage gaps
- AI Overview citation opportunities
- weak incumbent answers that can be replaced with clearer self-contained blocks

### Phase 6 — competitor pattern intelligence
For the true competitors, model:
- repeated heading patterns
- common trust elements near the top
- recurring internal-link routes
- recurring conversion assets
- where incumbents are vague, generic, outdated, unsourced, or structurally weak

### Phase 7 — information-gain modeling
For each target query or cluster, define:
- what incumbents repeat
- what they skip
- what the target site can explain better
- what proof or examples the target can add
- what comparisons/tables/frameworks are missing
- what adjacent questions AI systems synthesize but pages answer poorly

### Phase 8 — brief generation
Every SERP-lab brief should define:
- exact target query or query set
- dominant intent
- winning page type
- title/H1 direction
- intro answer angle
- must-cover entities and subquestions
- snippet and AIO targets
- evidence/source burden
- trust elements required
- internal-link relationships
- conversion next step
- freshness/update triggers
- explicit information-gain angle

## Deliverable types
Use one or more of these outputs:
- single-keyword brief
- cluster brief set
- query ladder map
- SERP pattern summary
- snippet/AIO opportunity map
- competitor page-type matrix
- publish queue recommendation

## Severity / priority model
Prioritize queries by:
- commercial value
- ranking feasibility
- snippet/AIO upside
- authority leverage
- content differentiation potential
- speed to publish well

## Anti-patterns
- one-keyword-one-page thinking with no modifier logic
- copying top 3 headings and calling it research
- treating all ranking pages as equally relevant
- ignoring AI Overview / PAA patterns
- generating briefs with no information-gain angle
- confusing volume with revenue or authority leverage

## Output contract
Report:
- seed terms used
- query buckets generated
- repeated competitors found
- winning page types by bucket
- snippet/AIO patterns detected
- information-gain opportunities
- recommended page brief(s) or queue

## Quality bar
A good SERP lab should reduce guesswork. If the research does not make page structure, targeting, and differentiation more obvious, it failed.