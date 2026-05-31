---
name: authority-engine-memory-and-kpi-loop
description: Feedback-loop layer for the Authority Engine. Tracks KPI review cadence, refresh triggers, campaign memory, change logging patterns, and recurring optimization loops so SEO work compounds instead of resetting each cycle.
version: 1.0.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [seo, kpi, feedback-loop, refresh-cycle, campaign-memory, optimization, cadence, authority-engine]
    triggers: ["kpi loop", "seo feedback loop", "campaign memory", "refresh triggers", "what to revisit", "recurring optimization"]
---

# Authority Engine Memory and KPI Loop

Use this when the user wants the SEO system to keep learning from prior work instead of acting like every cycle starts from zero.

This is the feedback layer for:
- KPI review cadence
- refresh triggers
- recurring optimization loops
- campaign-memory patterns
- revisit logic
- what-changed / what-to-do-next framing

## Mandatory loads
Load these before serious execution:
- `devops/authority-engine`
- `devops/authority-engine-command-center`
- `devops/authority-engine-batch-optimizer`
- `devops/authority-engine-site-audit`

Load conditionally when relevant:
- `devops/authority-engine-serp-lab`
- `devops/authority-engine-wordpress-execution`
- `devops/wordpress-commercial-cluster-builder`
- `devops/enterprise-ai-seo-competitor-mining`

## Mission
Turn SEO from a sequence of disconnected tasks into a compounding operating loop with explicit review cycles, trigger conditions, and next-wave logic.

## Core principles
1. If nothing is reviewed, gains decay.
2. Not every page needs the same refresh cadence.
3. KPI drops matter only when tied to action thresholds.
4. Memory should preserve useful strategic context, not noisy logs.
5. Every wave should create the next review queue.
6. Separate signal from churn: do not revisit pages just because time passed if no trigger fired.

## Loop model
Every serious program should maintain five states:
1. baseline
   - what mattered before changes
2. change set
   - what was updated
3. observation window
   - what metrics should move and when
4. trigger logic
   - when to revisit, escalate, or deprioritize
5. next-wave queue
   - what to do after the observation window

## KPI categories
Track and review by bucket:
- organic sessions
- rankings (top 3 / top 10 / key money terms)
- CTR
- snippet ownership
- AI Overview / citation presence
- internal-link coverage
- conversions / lead actions / revenue proxy
- freshness age on priority pages
- trust/page-quality gaps still unresolved

## Review cadence model
Use these default cadences unless the niche or site suggests otherwise:
- weekly
  - active rollout pages
  - newly updated money pages
  - pages in an observation window
- monthly
  - top traffic pages
  - top money clusters
  - snippet/AIO opportunity pages
- quarterly
  - full cluster health review
  - trust/schema/internal-link re-check
  - duplicate/cannibalization review
- event-triggered
  - ranking drop
  - CTR drop
  - query shift
  - major product/category/site update
  - SERP feature change

## Refresh triggers
A page or cluster should re-enter the queue when one or more of these fire:
- rankings stall or drop materially
- CTR underperforms despite visibility
- snippet/AIO opportunity appears and the page is under-optimized
- page is high-value and freshness age crosses threshold
- new supporting pages change internal-link possibilities
- trust-sensitive page still lacks sufficient evidence or trust routing
- cannibalization or duplication becomes visible
- competitors change page type or intent model in the SERP

## Memory model
Preserve only durable campaign memory such as:
- canonical trust-page targets
- which clusters are priority clusters
- which page patterns worked well on the site
- known plugin/cache blockers
- recurring split-brain metadata issues
- which rollout waves are complete vs pending
- which triggers should cause revisit

Do not preserve noisy per-day metric chatter as durable memory.

## Standard loop workflow

### Phase 1 — define the unit of review
Choose whether the loop tracks:
- a single money page
- a cluster
- a site section
- the whole site

### Phase 2 — capture baseline
Record:
- current state
- key target metrics
- current blockers
- current trust/internal-link/supporting-page state

### Phase 3 — tie changes to observation window
For each update wave, define:
- what changed
- which KPIs should move
- how long to wait before meaningful review
- what would count as success vs underperformance

### Phase 4 — apply trigger logic
At review time, classify each item as:
- continue / no action needed
- incremental upgrade
- re-brief through SERP lab
- re-prioritize through batch optimizer
- re-audit due to deeper blockers
- deprioritize / monitor only

### Phase 5 — generate next-wave queue
Every review should produce:
- keep monitoring list
- pages to refresh now
- clusters to reinforce now
- blockers needing separate remediation
- pages safe to leave alone

## Handoff rules
- KPI drop with unclear cause -> route to `authority-engine-site-audit`
- query/intent shift -> route to `authority-engine-serp-lab`
- many pages now need refresh -> route to `authority-engine-batch-optimizer`
- page is ready for live changes -> route to `authority-engine-wordpress-execution`

## Output contract
Report:
- unit of review
- baseline state
- review cadence
- refresh triggers
- current observation status
- next-wave queue
- which layer should act next

## Quality bar
A good KPI/memory loop should make it obvious what to revisit, what to ignore, and why. If it creates constant churn without clear triggers, it failed.