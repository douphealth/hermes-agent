# Codex SEO → Hermes Superpowers Reference

Source stack inspected/installed 2026-05-31:

- `AgriciDaniel/codex-seo` — Codex-first orchestrator + 26 specialist workflows + TOML agents + deterministic scripts.
- `aaron-he-zhu/seo-geo-claude-skills` — broad SEO/GEO frameworks and governance patterns.
- `Auriti-Labs/geo-optimizer-skill` — focused GEO audit/fix/llms/schema/crawler-access CLI and MCP-ready engine.
- `madeburo/GEO-AI-Woo` — WordPress/WooCommerce llms.txt, crawler rules, AI metadata, product schema implementation pattern.
- `elmohq/elmo` — open-source AI visibility monitoring/analytics architecture.
- `GEO-optim/GEO` — academic GEO benchmark/reference; use research patterns, not unsupported claims.

## Local install paths

```text
/home/hermes/.hermes/vendor/codex-seo
/home/hermes/.hermes/vendor/codex-seo/.venv/bin/python
/home/hermes/.hermes/vendor/geo-optimizer-skill
/home/hermes/.hermes/vendor/geo-optimizer-skill/.venv/bin/geo
```

## Command mapping

When the user writes a Codex-style SEO command, route it to Hermes tools like this:

| User command | Primary engine | Hermes follow-up |
|---|---|---|
| `/seo audit <url>` | codex-seo `seo-audit` + smoke suite | authority-engine scorecard + public QA |
| `/seo page <url>` | codex-seo `seo-page` or page audit | surgical semantic SEO editor |
| `/seo technical <url>` | codex-seo `seo-technical` | robots/sitemap/canonical/cache validation |
| `/seo content <url>` | codex-seo `seo-content` | E-E-A-T/AEO/GEO modules |
| `/seo schema <url>` | codex-seo `seo-schema` | Yoast/schema conflict gate |
| `/seo images <url>` | codex-seo `seo-images` | WP media alt/caption fixes |
| `/seo sitemap <url>` | codex-seo `seo-sitemap` | GSC sitemap/IndexNow submission gates |
| `/seo geo <url>` | GEO Optimizer + codex-seo `seo-geo` | llms.txt/robots/schema/AI crawler plan |
| `/seo performance <url>` | codex-seo `seo-performance` | PageSpeed/CWV budget + rendered QA |
| `/seo cluster <seed>` | codex-seo `seo-cluster` | authority-engine topical map/cannibalization |
| `/seo ecommerce <url>` | codex-seo `seo-ecommerce` | affiliate/Woo/WP product schema compliance |

## Artifact-first run pattern

```bash
python3 ~/.hermes/skills/devops/codex-seo-superpowers/scripts/hermes_codex_seo_runner.py \
  /seo audit https://example.com \
  --out ~/.hermes/organic-growth-os/sites/example.com/codex-seo-audit
```

The wrapper writes:

- `run-summary.json`
- `codex-*.json` where deterministic Codex SEO runners succeed
- `geo-audit.json` / `geo-fix.txt` / `llms.txt` where GEO Optimizer succeeds
- `implementation-plan.md`

## WordPress AI visibility implementation gate

Before installing or emulating `GEO-AI-Woo` on any live WordPress site:

1. Backup current site/plugin/theme/MU state.
2. Detect active SEO/schema/robots tools: Yoast, RankMath, AIOSEO, custom MU plugins, Cloudflare Worker, robots filters, sitemap plugins.
3. Decide implementation mode:
   - **Plugin mode**: install GEO-AI-Woo only if no schema/robots conflict and user approves plugin install.
   - **Worker/MU mode**: generate `/llms.txt`, `/llms-full.txt`, AI crawler rules, and headers manually via Cloudflare Worker/MU plugin where safer.
   - **Read-only plan mode**: produce exact files/settings without live changes.
4. Verify public surfaces:
   - `/llms.txt` HTTP 200, compact site summary, canonical priority URLs.
   - `/llms-full.txt` HTTP 200 or intentional disabled status.
   - `robots.txt` allows citation bots (`OAI-SearchBot`, `PerplexityBot`, `ClaudeBot`) unless business policy says otherwise.
   - Training bots (`GPTBot`, `anthropic-ai`) may be disallowed while citation/search bots remain allowed.
   - JSON-LD validates and matches visible content.
   - HTTP Link header to llms.txt if implemented.
5. Purge cache and verify normal + cache-busted URLs.

## AI visibility monitoring model from Elmo

If the user asks for tracking/monitoring:

- Define brand/entity prompts per site and vertical.
- Track each prompt across engines if APIs/sessions exist: ChatGPT, Perplexity, Claude, Gemini, Google AI Overviews where available.
- Capture answer text, citations, competitors mentioned, source URLs, timestamp, engine, and prompt variant.
- Store snapshots under `~/.hermes/organic-growth-os/sites/<domain>/ai-visibility/`.
- Report deltas: citation gained/lost, competitor changed, answer drift, entity confusion, hallucinated facts.
- Never claim visibility improvement without comparing snapshots.

## GEO-optim research use

Use only as a strategy reference:

- prefer source-backed claims/statistics,
- add concise quotations or cited facts when accurate,
- improve readability/fluency,
- add technical terms/entities for topic completeness,
- avoid fake citations or keyword stuffing.

## Safety rules

- Do not auto-install WordPress plugins without explicit user approval.
- Do not replace Yoast as the SEO control plane unless explicitly requested.
- Do not expose API keys or credentials from local secret files.
- Do not fabricate DataForSEO/GSC/PageSpeed/Firecrawl results when credentials or APIs are unavailable.
- For YMYL pages, recommend refresh/noindex/medical review rather than aggressive unsupported GEO hacks.
