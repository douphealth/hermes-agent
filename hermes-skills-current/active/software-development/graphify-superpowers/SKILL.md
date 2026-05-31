---
name: graphify-superpowers
description: Use the Graphify skills supergraph to route, combine, and query Hermes skills with far fewer tokens. Load when a task may require multiple skills, skill routing, SEO/WordPress workflows, Hermes troubleshooting, or when the user asks for maximum efficiency.
version: 1.0.0
---

# Graphify Superpowers for Hermes Skills

This skill connects Hermes skills to the persistent Graphify skills supergraph.

## Persistent graph

- Graph JSON: `/home/hermes/.hermes/skills/graphify-out/graph.json`
- Report: `/home/hermes/.hermes/skills/graphify-out/GRAPH_REPORT.md`
- Builder: `/tmp/build_skills_graph.py`

The graph currently indexes all installed Hermes skills as nodes and connects them to categories, tags, related skills, capabilities, and conservative inferred semantic links.

## How to use

Before loading many long skills, query the graph first:

```bash
/home/hermes/.local/bin/graphify query "TASK TERMS HERE" --graph /home/hermes/.hermes/skills/graphify-out/graph.json --budget 900
```

For direct relationship checks:

```bash
/home/hermes/.local/bin/graphify path "wp-rest-cloudflare" "authority-engine"
/home/hermes/.local/bin/graphify explain "wp-rest-cloudflare" --graph /home/hermes/.hermes/skills/graphify-out/graph.json
```

Then load only the highest-signal skills with `skill_view`.

## Update after skill changes

When skills are added/removed/edited, refresh the supergraph:

```bash
GRAPHIFY_BIN=$(which graphify 2>/dev/null || echo /home/hermes/.local/bin/graphify)
PYTHON=$(head -1 "$GRAPHIFY_BIN" | tr -d '#!')
"$PYTHON" /tmp/build_skills_graph.py
```

## Benchmark

The first skills supergraph benchmark showed:

- Corpus: ~884,151 words / ~1,178,868 naive tokens
- Graph: 371 nodes / 816 edges
- Avg query cost: ~15,426 tokens
- Reduction: ~76.4x fewer tokens per query

## Rules

- Use the graph to route and combine skills; do not treat it as a replacement for loading a mandatory matching skill.
- Never invent graph edges. If a query lacks evidence, load the actual skill or inspect files.
- Keep query budgets low unless the user asks for exhaustive output.
