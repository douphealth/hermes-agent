# OS Hardening Session — 2026-05-17

## Trigger
User asked to transform Hermes into an enterprise-grade WordPress Organic Growth OS, then expanded requirements with content inventory, money pages, internal-link graph, monetization, experiments, learnings, agent roles, prioritization formula, QA rubric, GEO/AEO rules, and self-improvement loop.

## Durable Workflow Learned
1. Treat OS transformation as both runtime state and skill-library work:
   - Runtime state: `/home/hermes/.hermes/organic-growth-os/`.
   - Reusable procedure: `wordpress-organic-growth-os` skill plus templates/scripts/references.
2. Scaffold every managed site with a complete artifact contract, not just broad profile files.
3. Add deterministic validation immediately so future sessions can verify completeness without rereading everything.
4. After scaffolding, the correct next action is a full read-only portfolio probe, not new content.
5. Technical/indexability blockers outrank content production until investigated and safely fixed.
6. For repo-level implementation, commit a class-level skill and support files; avoid narrow one-session skills.

## Required Site Artifact Contract
- `SITE_PROFILE.md`
- `TOPICAL_MAP.md`
- `CONTENT_INVENTORY.md`
- `MONEY_PAGES.md`
- `INTERNAL_LINK_GRAPH.md`
- `MONETIZATION_MAP.md`
- `GROWTH_QUEUE.md`
- `TECHNICAL_QA.md`
- `CONTENT_STANDARDS.md`
- `EXPERIMENT_LOG.md`
- `LEARNINGS.md`
- `STATE.md`

## Read-Only Probe Pattern
Use a compact reducer/probe before plans or edits. Capture only decision-grade signals:
- homepage status/final URL
- robots and sitemap statuses
- X-Robots-Tag
- meta robots
- canonical
- title/meta description
- H1 count/text
- JSON-LD count
- `/llms.txt` or `/ai.txt` status where present

## Prioritization Pattern
If the probe reveals H1 anomalies or sitemap/header `noindex` anomalies, classify next work as Scout → Technical SEO. Do not jump to content inventory or publishing until indexability/crawl clarity is understood.

## Safety Rule
Public probes and local state/template/script updates are autonomous. Production changes to H1s, templates, SEO plugin settings, headers, robots, canonicals, or indexing rules require approval.

## Output Pattern That Worked
Use the compact enterprise format:
- Result
- Highest-Impact Action
- Evidence
- Priority
- Expected Impact
- Risk
- Next Step

Keep evidence as short status lines; avoid raw logs unless diagnosing a failure.
