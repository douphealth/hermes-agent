---
name: hermes-agent-superpower-compatibility
description: Implement SOTA agent-superpower compatibility in Hermes by adapting patterns from external agent frameworks such as OpenHands without bloating runtime or breaking prompt caching.
---

# Hermes Agent Superpower Compatibility

Use this skill when asked to make Hermes Agent more powerful based on another agent framework (OpenHands, Devin-like systems, Cursor/Claude/Codex agent conventions, repo-local skills, microagents, task skills, etc.).

## Core principle

Prefer the smallest high-leverage compatibility bridge that plugs into Hermes' existing architecture. Do not clone an external framework wholesale. Preserve Hermes strengths:

- deterministic prompt/system-prompt assembly
- prompt-cache stability
- profile-aware paths via `get_hermes_home()`
- existing prompt-injection scanning
- progressive disclosure via skills where possible
- focused tests before implementation

## Workflow

1. **Load Hermes context first**
   - Load the `hermes-agent` skill when the task touches Hermes internals.
   - Load workspace/code-quality skills if available: instruction discovery, TDD, auto-verification, systematic debugging.
   - Read repo instructions (`AGENTS.md`, `.hermes.md`, etc.) before edits.
   - Check `git status --short` before modifying files.

2. **Inspect the external framework for patterns, not code to copy**
   - Clone or inspect the upstream repo read-only.
   - Identify durable abstractions: repo-local skills, task triggers, event streams, sandbox/runtime separation, trajectory logs, delegation, resumability.
   - Choose the lowest-risk pattern that fits Hermes' current extension points.

3. **Select the highest-leverage Hermes integration point**
   - For repo-local instructions/superpowers: prefer `agent/prompt_builder.py` context loading.
   - For dynamic hints during tool use: inspect `agent/subdirectory_hints.py` and agent loop/tool-result injection points.
   - For durable async work: use kanban/cron/plugin surfaces rather than ad-hoc background loops.
   - For external agent CLIs: prefer existing ACP/delegation surfaces.

4. **Write failing tests first**
   - Add tests that express compatibility behavior, not implementation details.
   - Include safety cases: prompt-injection content must be blocked or sanitized.
   - Include nested-directory cases when repo-local discovery is involved.
   - Include coexistence with existing Hermes context files.

5. **Implement as a narrow bridge**
   - Reuse Hermes helpers (`parse_frontmatter`, context scanning, truncation, git-root discovery) instead of adding dependencies.
   - Sort discovered files for deterministic prompt caching.
   - Strip external-framework metadata/frontmatter unless Hermes explicitly consumes it.
   - Cap injected context with existing truncation limits.
   - Avoid environment-dependent assumptions or hardcoded user paths.

6. **Verify**
   - Run focused new tests first.
   - Run the surrounding regression file(s), not just the new `-k` slice.
   - Capture exact command evidence and final changed files.

## OpenHands-specific pattern

OpenHands-style repo-local superpowers commonly live under:

- `.openhands/skills/*.md`
- `.openhands/microagents/*.md`

Efficient Hermes adaptation:

- discover the nearest `.openhands` root from current working directory up to the git root
- load both directories in deterministic sorted order
- strip YAML frontmatter (`name`, `type`, `triggers`, etc.) before injection
- reuse Hermes context prompt-injection scanning
- load as additive project context alongside `.hermes.md`/`AGENTS.md`/`CLAUDE.md` rather than replacing them
- test that nested cwd under `src/` still inherits repo-root OpenHands superpowers

See `references/openhands-project-superpowers.md` for a concrete implementation note from a prior Hermes patch.

## Pitfalls

- Do not add broad framework dependencies for a simple context-compatibility bridge.
- Do not store task-specific PR numbers, commit SHAs, or temporary failures in skills.
- Do not convert transient setup failures into permanent tool limitations.
- Do not edit bundled/protected skills; create or patch a user-owned umbrella instead.
- Do not load every external file recursively without limits; this breaks context budgets and prompt caching.

## Output expectations

Report:

- chosen external pattern
- Hermes integration point
- files changed
- tests added
- exact verification commands and results
- remaining next-step upgrades, if any
