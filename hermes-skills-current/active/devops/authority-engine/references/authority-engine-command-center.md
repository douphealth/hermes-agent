<!-- Consolidated from skill: authority-engine-command-center; original path: /home/hermes/.hermes/skills/devops/authority-engine-command-center -->

---
name: authority-engine-command-center
description: Master operator workflow for the Authority Engine. Routes intake to the right layer, defines decision trees, standardizes outputs, and manages handoffs across audit, SERP research, batch prioritization, and live execution.
version: 1.0.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [seo, orchestration, workflow, routing, command-center, authority-engine, wordpress, audit, serp]
    triggers: ["command center", "authority engine operator", "seo workflow orchestration", "route seo task", "full seo operating system"]
---

# Authority Engine Command Center

Use this when the user wants the whole SEO system to behave like one coordinated operating model instead of isolated specialist skills.

This is the orchestration layer for:
- intake routing
- mission classification
- skill handoff rules
- standardized output formats
- wave planning
- escalation and blocker handling
- audit -> research -> prioritization -> execution coordination

## Mandatory loads
Load these before serious execution:
- `devops/authority-engine`
- `devops/authority-engine-site-audit`
- `devops/authority-engine-serp-lab`
- `devops/authority-engine-batch-optimizer`
- `devops/authority-engine-wordpress-execution`

Load conditionally when relevant:
- `devops/wordpress-sota-seo-content-system`
- `devops/enterprise-ai-seo-competitor-mining`
- `devops/faq-schema-and-answer-box-optimizer`
- `devops/wordpress-commercial-cluster-builder`
- `wp-rest-cloudflare`

## Mission
Take any SEO request and route it into the shortest high-quality path that reaches a verified outcome.

## Command-center rule
Do not start with maximum process by default.
Start with the minimum correct layer, then escalate only when the mission requires it.

## Intake classification
Classify each request into one primary lane:
1. audit
   - site diagnosis, blocker discovery, remediation planning
2. research
   - query modeling, SERP analysis, page briefs, cluster ideation
3. prioritization
   - archive scoring, queue design, rollout waves
4. execution
   - live page changes, internal links, trust blocks, schema-aware updates
5. compound program
   - when the user wants the full system end-to-end

## Default routing rules
- if the user asks “what is wrong / audit / assess / diagnose” -> `authority-engine-site-audit`
- if the user asks “what should we target / what should rank / build brief / analyze SERP” -> `authority-engine-serp-lab`
- if the user asks “which pages first / optimize archive / rollout across many pages” -> `authority-engine-batch-optimizer`
- if the user asks “update / publish / fix / deploy / change live page” -> `authority-engine-wordpress-execution`
- if the user asks for a full program or broad transformation -> sequence audit -> SERP lab -> batch optimizer -> execution

## Escalation tree
Use this escalation model:
- small live fix -> execution only
- single important page -> SERP lab + execution
- cluster buildout -> SERP lab + batch optimizer + execution
- sitewide uncertainty -> site audit first
- archive-scale upgrade -> site audit or batch optimizer first, then execution waves
- trust-sensitive or metadata-blocked sites -> site audit + execution with blocker map

## Standard workflow shapes

### Shape A — Rapid page fix
1. classify page intent
2. load execution layer
3. apply additive upgrade
4. verify live

### Shape B — Strategic page build
1. load SERP lab
2. generate brief
3. hand off to execution layer
4. verify live

### Shape C — Cluster rollout
1. load SERP lab for demand geometry
2. load batch optimizer for queue order
3. load execution layer for page waves
4. verify sample and rollout pattern

### Shape D — Site transformation
1. load site audit
2. isolate P0/P1 issues
3. load SERP lab for priority clusters
4. load batch optimizer for waves
5. load execution layer for deployment

## Standard output package
For any meaningful task, the command center should try to produce:
- mission type
- selected workflow shape
- skills/layers used
- primary findings or brief
- prioritized next actions
- blockers / constraints
- verification state

## Handoff rules
A layer should hand off only when it has produced its required artifact:
- site audit -> remediation plan
- SERP lab -> brief or query map
- batch optimizer -> rollout queue
- execution -> live verification report

Do not hand off vague observations.
Hand off concrete artifacts.

## Blocker handling
When blockers appear, classify them clearly:
- access blocker
- plugin/head-layer blocker
- cache/optimization blocker
- theme/layout fragility blocker
- trust/content gap blocker

Then decide:
- continue with body-layer wins
- defer until access is fixed
- route to audit for deeper diagnosis
- route to batch optimizer for re-sequencing

## Operator standards
- preserve token efficiency
- preserve visible design unless redesign is requested
- prefer additive upgrades when risk is high
- document blockers cleanly
- keep output oriented toward next action
- do not let research sprawl replace execution

## Output contract
Report:
- request classification
- workflow chosen
- skills routed
- artifact produced
- what happened next
- what remains blocked or queued

## Quality bar
A good command center makes the right next move obvious and keeps the system coordinated. If it adds ceremony without reducing ambiguity or speeding execution, it failed.