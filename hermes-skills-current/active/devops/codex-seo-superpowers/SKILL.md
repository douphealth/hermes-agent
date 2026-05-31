---
name: codex-seo-superpowers
description: "Hermes integration layer for Codex-first SEO/GEO/AEO/AI-visibility superpowers using AgriciDaniel/codex-seo, GEO Optimizer, WordPress llms.txt/plugin patterns, and AI visibility monitoring."
version: 1.0.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [seo, geo, aeo, ai-visibility, codex-seo, wordpress, llms.txt, schema, gsc, pagespeed, dataforseo, firecrawl, elmo]
    triggers: ["codex-seo", "/seo audit", "/seo geo", "AI visibility superpowers", "GEO-AI-Woo", "llms.txt", "SEO agent superpowers"]
---

# Codex SEO Superpowers for Hermes

Use when the user wants Hermes agents to become stronger at SEO/GEO/AEO/AI visibility, especially with Codex-style `/seo ...` workflows, WordPress sites, llms.txt, schema, Core Web Vitals, topical clustering, GSC/PageSpeed/DataForSEO/Firecrawl integrations, or AI citation monitoring.

## Mandatory routing

Before serious execution, load:
- `hermes-seo-geo-aeo-supercharger`
- `authority-engine`
- `devops/seo-superpowers-public-toolkits`
- Authority reference `references/codex-seo-hermes-superpowers.md` from this skill.
- Repo-update reference `references/upstreaming-hermes-seo-superpowers.md` when converting this local superpower layer into a portable Hermes Agent optional-skill PR.

## Installed local engines

Vendored toolkits are available at:

- Codex SEO: `/home/hermes/.hermes/vendor/codex-seo`
  - venv: `/home/hermes/.hermes/vendor/codex-seo/.venv/bin/python`
  - best command mapping: `/seo audit https://example.com`
- GEO Optimizer: `/home/hermes/.hermes/vendor/geo-optimizer-skill`
  - CLI: `/home/hermes/.hermes/vendor/geo-optimizer-skill/.venv/bin/geo`

Use the wrapper:

```bash
python3 ~/.hermes/skills/devops/codex-seo-superpowers/scripts/hermes_codex_seo_runner.py \
  /seo audit https://example.com \
  --out ~/.hermes/organic-growth-os/sites/example.com/codex-seo-audit
```

Supported command-style prompts:

- `/seo audit <url>` — full deterministic site/page report bundle.
- `/seo geo <url>` — GEO + AI crawler + llms/schema/citability readiness.
- `/seo content <url>` — E-E-A-T, helpfulness, answer extraction, AI citation readiness.
- `/seo schema <url>` — schema detection/validation/recommendations.
- `/seo cluster <keyword-or-url>` — topic architecture and SERP-overlap clustering guidance.
- `/seo performance <url>` — CWV/PageSpeed-oriented performance evidence.
- `/seo ecommerce <url>` — product/affiliate/WooCommerce commercial SEO.

## Execution standards

1. Always gather evidence first. Never claim rankings, traffic, search volume, AI citations, or AI visibility wins without measured data.
2. For WordPress sites, use Yoast as the primary SEO control plane unless the user explicitly approves a plugin change.
3. Treat `madeburo/GEO-AI-Woo` as an implementation pattern/plugin candidate, not an automatic install. Before live install: back up, detect Yoast/schema/robots/llms conflicts, test staging if possible, and verify public `/llms.txt`, `/llms-full.txt`, robots, headers, and schema after deployment.
4. Use `elmohq/elmo` as monitoring architecture inspiration: track prompts, brands/entities, answer-engine citations, competitors, snapshots, and deltas over time. Do not claim ongoing monitoring is active unless it is deployed/configured.
5. Use `GEO-optim/GEO` as research reference: enrich content with credible statistics, quotations, citations, fluency, and technical terms only when accurate and source-backed.
6. Report compactly: Outcome, Evidence, Artifacts, Next Actions.

## Output contract

For audits, save artifacts to disk and report paths instead of dumping raw crawl output in chat.

Each serious run should include:
- canonical URL(s) and target intent
- crawl/indexability status
- technical SEO and CWV/PageSpeed status when available
- schema/Yoast/metadata findings
- llms.txt / robots / AI crawler access findings
- content helpfulness, E-E-A-T, AEO answer-block readiness
- GEO/citability score and top fixes
- topical architecture/cannibalization flags
- WordPress implementation plan: plugin/MU/Worker/sitemap/cache/GSC actions
- monitoring plan: T+14/T+45/T+90 plus AI-answer prompt tracking if available
