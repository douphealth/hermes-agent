---
name: codewhale-powercharge
description: "CodeWhale-inspired Hermes operating mode for SOTA coding/repo work: Fin-style cheap coordination, strict subagent role postures, evidence-first child output, context/cache hygiene, and verification discipline."
version: 1.0.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [codewhale, delegation, subagents, coding, verification, context-efficiency]
    related_skills: [hermes-agent, subagent-driven-development, auto-verification, workspace-instruction-discovery]
---

# CodeWhale Powercharge

Use this skill when the user asks to power-charge Hermes with CodeWhale ideas, when running serious multi-agent coding/repo work, or when you need maximum evidence density with low context waste.

## Imported ideas from CodeWhale

- **Fin seam:** use a cheap/fast coordination path for routing, summarization, and lightweight classification; reserve the main model for hard reasoning.
- **Role postures:** classify child work as `explore`, `plan`, `review`, `implementer`, or `verifier` rather than spawning generic workers.
- **Fresh vs forked context:** default child tasks should receive only the specific task/context they need; pass prior decisions explicitly when continuation is required.
- **Evidence contract:** child results must include concrete artifacts instead of narrative-only summaries.
- **Context/cache hygiene:** preserve stable prompts and avoid dumping large transcripts into the parent; pass handles/paths/slices where possible.
- **Verification before completion:** implementers run focused checks; verifiers report pass/fail and do not silently fix.

## Hermes execution pattern

1. **Discover instructions first**
   - Load repo-local `AGENTS.md` / `CLAUDE.md` / rule files before serious edits.
   - Check `git status --short` before writing; do not overwrite user changes.

2. **Route subagents by posture**
   - `explore`: read-only mapping, return `path:line` evidence.
   - `plan`: strategy/checklist, minimal/no writes.
   - `review`: severity-ranked findings, no patches.
   - `implementer`: smallest correct edit plus focused verification.
   - `verifier`: run tests/QA and report exact pass/fail.

3. **Use Hermes delegate_task with explicit context**
   - Give each child a self-contained goal, exact repo path, relevant files/errors, desired role posture, and output format.
   - Use parallel batches only for independent workstreams.
   - Children cannot ask the user; the parent must supply missing context or choose defaults.

4. **Require child output sections**
   - `SUMMARY`: one paragraph.
   - `EVIDENCE`: concrete file refs, command exit codes, URLs/statuses, or tool outputs.
   - `CHANGES`: exact writes or `None.`
   - `RISKS`: unresolved risks or `None observed.`
   - `BLOCKERS`: blockers or `None.`

5. **Keep context lean**
   - Prefer typed tools over shell for reads/search/edits.
   - Summarize or slice large files rather than pasting full blobs.
   - Preserve prompt-cache stability: avoid unnecessary system/config churn mid-task.

6. **Verify and report**
   - Run focused tests for changed surfaces.
   - If full tests are too expensive, run the smallest meaningful proof and state the verification gap.

## Pitfalls

- Do not blindly port Rust/TUI internals into Hermes; translate the useful patterns into Hermes' Python/tooling architecture.
- Do not use paid sibling delegation models if the user's config says free-only delegation.
- Do not claim CodeWhale features like durable detached subagents are now available unless implemented and verified in Hermes.
- Do not let role labels replace evidence; every result still needs proof.

## Source anchor

Derived from public CodeWhale repo inspection at `https://github.com/Hmbown/CodeWhale`, especially README feature list, `docs/SUBAGENTS.md`, `crates/tui/src/tui/auto_router.rs`, and `crates/tui/src/prompts/subagent_output_format.md`.
