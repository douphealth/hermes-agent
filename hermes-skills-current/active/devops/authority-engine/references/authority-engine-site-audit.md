<!-- Consolidated from skill: authority-engine-site-audit; original path: /home/hermes/.hermes/skills/devops/authority-engine-site-audit -->

---
name: authority-engine-site-audit
description: Diagnostic and control-layer SEO audit system for technical SEO, content quality, topical coverage, trust/E-E-A-T, schema, snippet/AIO opportunity, and internal-link architecture. Produces prioritized remediation plans for enterprise SEO execution.
version: 1.0.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [seo, site-audit, technical-seo, eeat, schema, internal-linking, aeo, geo, wordpress]
    triggers: ["site audit", "technical seo audit", "authority engine audit", "seo control layer", "internal link audit", "schema audit", "eeat audit"]
---

# Authority Engine Site Audit

Use this when the user wants a control-layer audit before or alongside execution.

This is the system for:
- technical SEO auditing
- content inventory auditing
- topical authority auditing
- trust / E-E-A-T auditing
- schema auditing
- snippet / PAA / AI Overview opportunity auditing
- internal-link graph auditing
- prioritized remediation planning

## Mandatory loads
Load these before serious execution:
- `devops/authority-engine`
- `devops/authority-engine-batch-optimizer`
- `devops/authority-engine-wordpress-execution`

Load conditionally when relevant:
- `devops/wordpress-sota-seo-content-system`
- `devops/enterprise-ai-seo-competitor-mining`
- `devops/faq-schema-and-answer-box-optimizer`
- `devops/wordpress-commercial-cluster-builder`
- `wp-rest-cloudflare`
- `devops/yoast-snippet-layer-remediation`
- `devops/wordpress-eeat-remediation-via-rest`

## Mission
Produce a truthful, prioritized, execution-ready audit that identifies the highest-leverage fixes without drowning the operator in low-value observations.

## Core principles
1. Audit for action, not for theater.
2. Separate ranking ceilings from quick wins.
3. Distinguish body-layer issues from plugin/head-layer issues.
4. Group findings by remediation pattern so fixes can be batched.
5. Prioritize by business value, authority leverage, and ease of remediation.
6. Never mix cosmetic issues with true ranking blockers.

## Audit layers

### Layer 1 — technical SEO
Check for:
- indexability and crawlability
- robots/canonical issues
- sitemap health
- redirect chains / loops
- broken internal links / server errors
- mobile usability
- page-speed / Core Web Vitals red flags
- orphan-page risk
- obvious duplicate/cannibalization patterns

### Layer 2 — content quality and intent
Check whether important pages:
- match dominant query intent
- use the right page type
- answer the query early
- have strong heading structure
- contain enough specificity / examples / utility
- include extraction-friendly assets where useful
- show information gain vs generic competitors

### Layer 3 — topical authority
Check for:
- hub/spoke completeness
- missing cluster-support pages
- weak pillar pages
- over-fragmented or duplicated topics
- orphan or under-linked pages
- weak freshness/update cadence on important topics

### Layer 4 — AEO / GEO opportunity
Check for:
- snippet-ready definition/list/table/step blocks
- PAA / FAQ coverage gaps
- AI Overview-friendly answer sections
- self-contained paragraphs that can be cited cleanly
- weak or missing recency signals
- insufficient evidence/citations for trust-sensitive topics

### Layer 5 — trust / E-E-A-T
Check for:
- bylines and author context
- author/about/editorial-policy/review-methodology/disclosure pages
- trust-page visibility from commercial pages
- first-hand experience or proof signals
- weak or inconsistent entity definitions
- contact/policy-page weaknesses

### Layer 6 — schema and metadata
Check for:
- schema presence and relevance
- duplicate/conflicting schema risk
- stale or split-brain metadata layers
- title/meta/og divergence
- raw-vs-rendered head divergence, especially when JS-heavy homepages, iframes, embedded apps, or runtime snippets mutate `document.title` after load even though `curl` shows the intended SEO title
- plugin-layer blockers preventing full remediation

### Layer 7 — internal-link architecture
Check for:
- parent/hub links
- sibling/support links
- trust links
- next-step conversion links
- under-linked priority pages
- cluster authority flow failures

## Standard audit workflow

### Public WordPress reconnaissance shortcut
For a credential-free WordPress audit, use `scripts/public-wordpress-seo-audit.py` before writing recommendations:

```bash
python3 /home/hermes/.hermes/skills/devops/authority-engine/scripts/public-wordpress-seo-audit.py https://example.com > /tmp/public-wp-seo-audit.json
```

This probes robots, sitemaps, WP REST inventory, duplicate post/page slug conflicts, H1/meta/canonical/schema/word-count signals, thin pages, and internal 404/redirect leakage. It is especially useful when Cloudflare/wp-admin access is blocked but the public site and REST API are reachable. Treat internal 404s, blank H1s, duplicate post/page objects, and missing Article schema on posts as P0/P1 findings before recommending more content.

### Phase 1 — define audit scope
Decide whether the audit covers:
- full site
- priority archive subset
- single cluster
- commercial pages only
- trust layer only
- technical audit only

### Phase 2 — collect inventory
For the chosen scope, collect:
- URL
- page type / post type
- title
- modified date
- likely query class
- commercial value tier
- cluster/topic assignment
- trust-sensitive classification

### Phase 3 — score by layer
Score each important URL or cluster for:
- technical readiness
- intent fit
- content strength
- snippet/AIO opportunity
- trust strength
- schema/metadata health
- internal-link health
- business leverage

### Phase 4 — classify findings
Group findings into:
- critical blockers
- high-leverage quick wins
- money-page upgrades
- cluster reinforcement needs
- trust-layer deficits
- metadata/plugin blockers
- cleanup / consolidation needs

### Phase 5 — convert findings into rollout queues
The audit is not done until findings map into:
- immediate fixes
- next-wave upgrades
- batchable patterns
- blocked items requiring plugin/access changes
- deprioritized low-ROI items

## Severity model
Use these levels:
- P0: real ranking/conversion blocker
- P1: high-leverage fix with strong ROI
- P2: useful improvement, not urgent
- P3: low-value or cosmetic

## Output contract
Every site audit should report:
- scope audited
- methodology used
- critical blockers
- top quick wins
- top money-page opportunities
- trust/schema/internal-link gaps
- batch patterns available
- blocker map for access/plugin/cache constraints
- prioritized remediation plan by wave

## Quality bar
A good site audit should make the next 30 days of execution obvious. If it produces a long issue list without clear remediation order, it failed.