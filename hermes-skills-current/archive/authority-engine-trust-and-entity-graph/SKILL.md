---
name: authority-engine-trust-and-entity-graph
description: Trust and entity-system layer for the Authority Engine. Builds consistent author/brand/entity architecture, strengthens editorial and methodology routing, and improves AI visibility through durable trust-page and entity-graph patterns.
version: 1.0.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [seo, trust, eeat, entities, ai-visibility, author-pages, about-pages, editorial-policy, methodology, wordpress]
    triggers: ["entity graph", "trust architecture", "eeat system", "author entity", "brand entity", "ai visibility trust", "editorial policy system"]
---

# Authority Engine Trust and Entity Graph

Use this when the user wants a systematic trust/entity layer instead of isolated trust fixes.

This is the system for:
- entity consistency
- author / founder / organization definition
- About / Author / Organization architecture
- editorial policy / methodology / disclosure routing
- trust-page normalization
- AI visibility entity reinforcement
- brand/author trust graph strengthening across the site

## Mandatory loads
Load these before serious execution:
- `devops/authority-engine`
- `devops/wordpress-eeat-remediation-via-rest`
- `devops/wordpress-trust-blocks-and-proof-elements`
- `devops/authority-engine-site-audit`

Load conditionally when relevant:
- `devops/authority-engine-wordpress-execution`
- `devops/authority-engine-memory-and-kpi-loop`
- `devops/authority-engine-batch-optimizer`
- `devops/wordpress-sota-seo-content-system`
- `wp-rest-cloudflare`

## Mission
Make trust and entity signals deliberate, internally consistent, and easy for both users and search/AI systems to understand.

## Core principles
1. Trust must be true, not theatrical.
2. A site should present one coherent entity graph, not scattered fragments.
3. Important pages should route visibly to real trust assets.
4. Author, founder, brand, methodology, and disclosure signals should reinforce each other.
5. AI visibility improves when entity definitions are consistent and repeated cleanly across the site.
6. Do not fabricate credentials, staff, proof, or organizational structure.

## Entity graph model
The minimum trust/entity graph should define and connect:
- brand / site entity
- founder or primary author entity
- about page
- author page(s)
- editorial policy
- review methodology
- disclosure / affiliate policy
- contact page
- key money pages and high-traffic pages that link into the trust graph

## What to audit
Check for:
- inconsistent brand descriptions across pages
- weak or missing founder/author definition
- bylines with poor destinations
- missing or thin editorial/methodology/disclosure pages
- duplicate trust pages with unclear canonical target
- trust pages not linked from important commercial or informational pages
- inconsistent “who we are / what we do / how we review” language
- weak AI-visible entity summaries near About/Author pages

## Standard workflow

### Phase 1 — entity discovery
Identify the real entities the site can honestly support:
- brand/site
- founder/owner
- editor/author (if real)
- organization/company identity (only if real and supportable)
- product/service entities if central to the site

### Phase 2 — trust-asset discovery
Find existing live assets:
- about page
- author page
- editorial policy
- methodology page
- disclosure page
- contact page
- user profile descriptions and URLs
- duplicate policy/trust pages

### Phase 3 — canonical trust map
Define the canonical targets for:
- about
- author
- editorial policy
- methodology
- disclosure
- contact

Anything duplicate or weaker should either:
- redirect to the canonical version
- become a support page that routes clearly to the canonical one

### Phase 4 — entity-definition standard
For each core entity, define a concise stable description.
Examples of what to standardize:
- what the site is
- who runs it
- what the site publishes
- how content is researched or reviewed
- how monetization/disclosure works

These definitions should stay consistent across:
- About
- Author
- Editorial Policy
- Methodology
- Disclosure
- trust notes on important pages

### Phase 5 — trust routing architecture
Ensure important pages visibly route into the trust graph.
Minimum high-value routing:
- money pages -> methodology + disclosure + about/author as appropriate
- reviews/comparisons -> methodology + disclosure
- stat-heavy pages -> evidence/methodology notes
- founder-led sites -> author/founder/about coherence

### Phase 6 — AI visibility reinforcement
Strengthen AI-visible trust signals by:
- using clean self-contained entity descriptions
- keeping brand and founder definitions stable across pages
- reducing contradictory or inflated authority language
- making policy/methodology pages easy to crawl and internally linked
- aligning organization/author/about language with what the site actually is

### Phase 7 — execution pattern
When implementing live changes, prefer:
- canonical trust-page upgrades first
- then trust routing from important pages
- then user/author profile cleanup
- then duplicate-trust cleanup
- then cluster-wide trust-note normalization

## Standard trust blocks to use
Where appropriate, use compact modules for:
- editorial note
- methodology note
- evidence note
- disclosure note
- founder/reviewer context
- what this page does not claim

Do not spam them. Place them where trust matters most.

## Output contract
Report:
- entities defined
- canonical trust map
- inconsistent definitions found
- trust pages strengthened or needed
- important pages missing trust routing
- duplicate trust assets needing consolidation
- AI visibility/entity improvements available
- next execution wave

## Quality bar
A good trust/entity system should make the site easier to trust, easier to understand, and easier for search/AI systems to model. If it just adds generic legal fluff, it failed.