# OpenHands project superpowers bridge for Hermes

Session-derived implementation pattern for making Hermes understand OpenHands-style repo-local capabilities.

## Context

OpenHands repositories can define repo-local skills/microagents under:

- `.openhands/skills/*.md`
- `.openhands/microagents/*.md`

These markdown files often include YAML frontmatter such as:

```yaml
---
name: documentation
type: knowledge
triggers:
- documentation
- docs
---
```

The durable content is the markdown body. Hermes should not blindly inject metadata as instructions.

## Efficient Hermes integration

Best first integration point: `agent/prompt_builder.py`, in project context assembly.

Implementation shape:

1. Find the nearest directory containing `.openhands/skills` or `.openhands/microagents`.
2. Walk upward only to the git root to avoid unrelated parent-tree contamination.
3. Load direct `*.md` children from both directories in deterministic sorted order.
4. Parse and strip YAML frontmatter with Hermes' existing `parse_frontmatter` helper.
5. Run every body through the same context prompt-injection scanner used for `AGENTS.md`/`.hermes.md`.
6. Add a section such as `OpenHands Project Microagents` to project context.
7. Keep the primary Hermes context precedence unchanged: `.hermes.md` > `AGENTS.md` > `CLAUDE.md` > `.cursorrules`.
8. Load OpenHands superpowers additively, not as a replacement.
9. Reuse existing context truncation to protect prompt budget and cache stability.

## Tests to add

- `.openhands/microagents/*.md` loads alongside `AGENTS.md`.
- `.openhands/skills/*.md` loads when present.
- Nested cwd below git root still discovers repo-root `.openhands`.
- Prompt injection text inside an OpenHands microagent is blocked/sanitized.
- Frontmatter metadata is stripped from injected content.

## Verification example

Focused slice:

```bash
source venv/bin/activate && pytest -q tests/agent/test_prompt_builder.py -k openhands
```

Regression around context loading:

```bash
source venv/bin/activate && pytest -q tests/agent/test_prompt_builder.py
source venv/bin/activate && pytest -q tests/agent/test_subdirectory_hints.py
```

## Next upgrade

Static additive loading is the low-risk compatibility bridge. The next higher-power step is dynamic trigger activation: parse OpenHands `triggers` and inject only relevant microagents per user task/tool context, while preserving Hermes prompt-cache invariants.
