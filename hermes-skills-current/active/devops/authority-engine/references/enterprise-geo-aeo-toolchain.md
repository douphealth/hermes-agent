# Enterprise GEO/AEO Toolchain Layer

Use this reference when the user asks for SOTA SEO, GEO, AEO, AI-search visibility, llms.txt, answer-engine visibility, AI crawler readiness, AI citations, or enterprise-grade SEO automation.

This layer combines:

- `AgriciDaniel/codex-seo` — Codex-first orchestration layer for `/seo audit`, `/seo geo`, `/seo content`, `/seo schema`, `/seo cluster`, `/seo google`, `/seo performance`, and `/seo ecommerce`; local vendored path: `/home/hermes/.hermes/vendor/codex-seo`.
- `Auriti-Labs/geo-optimizer-skill` — focused improvement engine for crawlability, llms.txt, schema, bot access, brand/entity signals, AI discovery files, prompt-injection risk, RAG chunk readiness, content decay, platform citation readiness, and GEO scorecards; local vendored path: `/home/hermes/.hermes/vendor/geo-optimizer-skill`.
- `madeburo/GEO-AI-Woo` — WordPress/WooCommerce implementation candidate/pattern for llms.txt, llms-full.txt, AI bot rules, AI metadata, HTTP Link headers, REST/WP-CLI controls, and product schema; never auto-install without backup, conflict analysis, explicit approval, cache purge, and public verification.
- `elmohq/elmo` — AI visibility monitoring architecture for prompt/citation snapshots, competitor mentions, source URLs, and answer drift.
- `alexpospekhov/searchstack-aeo` / PyPI `searchstack` — monitoring and outcome layer for whether ChatGPT, Perplexity, Claude, Grok, Google AI Overview, GSC, traffic analytics, and llms.txt validation show actual visibility progress.

## Core rule

Do **not** treat AI visibility as “add schema and done.” Run the stack as a closed loop:

1. **Clean index first** — only canonical, useful URLs should be crawlable/indexable and in sitemaps.
2. **Audit AI-readiness** — robots, llms.txt, schema, meta, content extraction, trust/entity, JS accessibility, AI discovery.
3. **Fix deployable gaps** — robots, llms.txt, llms-full.txt, schema suggestions, page structure, answer blocks, citations, trust pages.
4. **Validate live** — cache-busted HTTP, rendered HTML, schema parse, robots access, sitemap primary locs, llms files.
5. **Monitor outcomes** — AI citations, AIO mentions, GSC query/page movement, AI referral traffic, content decay.
6. **Iterate only on evidence** — improve pages that are eligible, cited-but-weak, or high-impression/no-click; no blind new content flood.

## Install / local execution

Hermes now has local vendored engines for the two main open-source layers:

```bash
# Codex SEO deterministic wrapper through Hermes
python3 ~/.hermes/skills/devops/codex-seo-superpowers/scripts/hermes_codex_seo_runner.py \
  /seo audit https://example.com \
  --out ./codex-seo-audit

# Direct Codex SEO runner if needed
/home/hermes/.hermes/vendor/codex-seo/.venv/bin/python \
  /home/hermes/.hermes/vendor/codex-seo/scripts/run_skill_workflow.py \
  --skill seo-audit --json https://example.com

# Direct GEO Optimizer CLI
/home/hermes/.hermes/vendor/geo-optimizer-skill/.venv/bin/geo audit \
  --url https://example.com --format json
```

For other ephemeral tools where no local install exists, prefer `uvx` so the tools run without permanently polluting the venv:

```bash
uvx --from geo-optimizer-skill geo --help
uvx --from searchstack searchstack --help
```

Permanent install only if user wants it:

```bash
uv tool install geo-optimizer-skill
uv tool install searchstack
```

## Phase 0 — prerequisite hygiene gate

Before running GEO/AEO scoring at scale, verify:

```bash
curl -sI https://example.com/
curl -s https://example.com/robots.txt
curl -sI https://example.com/sitemap_index.xml || curl -sI https://example.com/sitemap.xml
curl -s https://example.com/llms.txt | head
```

Blockers to fix before AI visibility claims:

- homepage or priority pages blank/broken
- `Disallow: /` or blocked citation bots
- sitemap returns HTML, stale Worker content, redirects, noindexed URLs, or uploaded/test URLs as primary locs
- canonical points to wrong host/subdomain
- Cloudflare/challenge blocks common crawlers
- hidden noindex or X-Robots-Tag on priority URLs
- severe template residue, shortcode leaks, prompt-injection text, or unsupported affiliate claims

## Phase 1 — GEO Optimizer audit commands

Single URL:

```bash
uvx --from geo-optimizer-skill geo audit \
  --url https://example.com \
  --format json \
  --output ./geo-audit-home.json
```

Sitemap sample:

```bash
uvx --from geo-optimizer-skill geo audit \
  --sitemap https://example.com/sitemap_index.xml \
  --max-urls 50 \
  --concurrency 5 \
  --format json \
  --output ./geo-audit-sitemap.json
```

Human/client report:

```bash
uvx --from geo-optimizer-skill geo audit \
  --url https://example.com \
  --format html \
  --output ./geo-audit.html
```

Regression tracking:

```bash
uvx --from geo-optimizer-skill geo audit \
  --url https://example.com \
  --save-history \
  --regression \
  --threshold 70
uvx --from geo-optimizer-skill geo history --url https://example.com
```

## Phase 2 — llms.txt / AI discovery file generation

Generate to a staging file first. Do not overwrite production blindly.

```bash
uvx --from geo-optimizer-skill geo llms \
  --base-url https://example.com \
  --sitemap https://example.com/sitemap_index.xml \
  --site-name "Brand Name" \
  --description "One-sentence site/entity description." \
  --output ./llms.txt
```

For slower but richer titles, add `--fetch-titles` only after confirming sitemap quality and keeping the URL count small.

Validation with searchstack:

```bash
uvx --from searchstack searchstack llms validate
uvx --from searchstack searchstack llms check
```

Production requirements:

- `/llms.txt` must be public, 200, fast, text/plain or readable text.
- Include brand/entity summary, canonical hubs, best resources, policies/methodology, tools, and update cadence.
- Keep it curated; do not dump every low-value URL.
- If adding `/llms-full.txt`, include only canonical index-worthy pages and exclude noindex/redirect/test/upload artifacts.

## Phase 3 — schema and citability

Generate suggestions, then verify visible-content support before publishing:

```bash
uvx --from geo-optimizer-skill geo schema --type organization --url https://example.com
uvx --from geo-optimizer-skill geo schema --type website --url https://example.com
uvx --from geo-optimizer-skill geo schema --type faq --url https://example.com/page/
```

Schema rules:

- Organization/WebSite/Person/BreadcrumbList can be sitewide if facts are visible and stable.
- Article only on articles.
- FAQPage only where the exact Q&A is visible on-page.
- HowTo only for visible step-by-step instructions.
- Review only with visible methodology/proof; never fake ratings.
- Affiliate/commercial reviews must include disclosure, proof box, date checked, alternatives, and rel="sponsored nofollow" where relevant.

## Phase 4 — searchstack monitoring layer

Create `.searchstack.toml` in a client/project workdir, not inside Hermes source, with available services only:

```toml
domain = "example.com"
sitemap = "https://example.com/sitemap_index.xml"

# Optional paid/API integrations; omit if unavailable.
# [openai]
# api_key=[REDACTED]
# [perplexity]
# api_key=[REDACTED]
# [anthropic]
# api_key=[REDACTED]
# [gsc]
# service_account = "/path/to/service-account.json"
# property = "https://example.com/"
```

No-key technical commands:

```bash
uvx --from searchstack searchstack meta
uvx --from searchstack searchstack schema
uvx --from searchstack searchstack links
uvx --from searchstack searchstack onpage https://example.com/priority-page/
uvx --from searchstack searchstack pages
```

AI/search outcome commands when configured:

```bash
uvx --from searchstack searchstack ai
uvx --from searchstack searchstack ai chatgpt
uvx --from searchstack searchstack ai perplexity
uvx --from searchstack searchstack ai claude
uvx --from searchstack searchstack geo "target query"
uvx --from searchstack searchstack gsc pages-perf
uvx --from searchstack searchstack gsc inspect https://example.com/priority-page/
uvx --from searchstack searchstack report
```

## Enterprise issue-priority model

Sort findings by expected traffic/visibility leverage:

1. **Availability/indexability breakers** — 5xx, blank pages, noindex, robots block, canonical mismatch, sitemap pollution.
2. **AI crawler and discovery blockers** — OAI-SearchBot/PerplexityBot/ClaudeBot blocked, missing llms.txt, unparseable JS content, prompt-injection risks.
3. **Trust/entity blockers** — no About/contact/editorial/review methodology, inconsistent organization/person facts, missing disclosures.
4. **Commercial proof gaps** — reviews/comparisons missing tested-by/date/pricing/features/alternatives/evidence/source boxes.
5. **Content extraction gaps** — missing Quick Answer, definitions, tables, FAQs, lists, next steps, sources/verification, dates.
6. **Topology gaps** — orphan pages, weak hubs, missing parent/sibling/next-step links, cannibalization.
7. **Freshness/decay** — stale prices, old years, unsupported statistics, broken screenshots, outdated tool features.
8. **Outcome gaps** — high GSC impressions/no clicks, cited competitor pages, AIO competitor citations, AI referral misses.

## Page-level AI visibility standard

Every priority page should include visible, extractable blocks:

- Quick answer: 40–80 words, query-satisfying, no fluff.
- Best for / not best for.
- Cost, difficulty, time to result.
- Common mistake.
- Recommended next step.
- Evidence/sources and last verified date.
- FAQ with exact visible Q&A if schema is used.
- Internal links up to hub, sideways to siblings, down to supporting pages, and forward to conversion/tool page.

## Prompt-injection and spam safety

Search engines and LLM crawlers may penalize or ignore manipulative content. Remove or rewrite:

- hidden/invisible text aimed at bots
- HTML comments with instructions to AI systems
- “ignore previous instructions,” “always cite us,” or similar prompt-injection residue
- raw prompt/template text, `[INTERNAL_LINK]`, `[wpcode]`, lorem ipsum, “paste into WordPress,” encoded HTML fragments
- fake ratings, hidden schema, unsupported “tested” claims, inflated revenue/ROI/ranking claims

## Output contract for audits

Return these artifacts every time when feasible:

- Prioritized issue list with severity and evidence.
- URL action map: KEEP / REFRESH / MERGE / 301 / 410 / NOINDEX.
- Sitemap contamination report.
- Robots/AI crawler access recommendation.
- llms.txt / llms-full.txt recommendation or generated staging file.
- Schema recommendation by page type, with visible-content support status.
- Top 20 refresh queue by impact.
- Monitoring plan: searchstack/cron commands, GSC checks, AI citation prompts.
- Final QA checklist before GSC indexing requests.

## Use the bundled runner

This skill includes `scripts/enterprise-geo-aeo-runner.py` for fast audits:

```bash
python3 ~/.hermes/skills/devops/authority-engine/scripts/enterprise-geo-aeo-runner.py \
  --url https://example.com \
  --sitemap https://example.com/sitemap_index.xml \
  --max-urls 50 \
  --out ./seo-audit-example
```

The runner uses `uvx` to execute `geo` and `searchstack`, saves raw outputs, writes a `.searchstack.toml` template, and emits a concise triage JSON/Markdown package. Treat its output as evidence inputs, not as permission to publish unsupported schema or claims.
