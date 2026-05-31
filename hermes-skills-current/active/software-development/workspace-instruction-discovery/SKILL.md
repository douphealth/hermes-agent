---
name: workspace-instruction-discovery
description: Discover and digest repo-local instruction files before serious code or workspace work so execution follows local rules instead of generic defaults.
version: 1.0.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [workspace, instructions, repo, routing, token-efficiency]
    triggers: [AGENTS.md, CLAUDE.md, repo rules, workspace instructions, local conventions]
    do_not_use_for: [feature implementation, code review, debugging]
    compatible_workflows: [inspect-digest-plan-execute-verify]
---

# Workspace Instruction Discovery

## Purpose
Build a compact digest of project-local instruction files so later work obeys the nearest active workspace rules.

## When to Use
- Before serious repo or code work
- Before planning in an unfamiliar workspace
- When behavior may be constrained by local docs
- When multiple instruction files may overlap

## Do NOT Use For
- Implementing features by itself
- Replacing code review or verification
- Dumping long docs into the main context window

## Workflow
1. Search from the current working directory upward.
2. Look for `AGENTS.md`, `CLAUDE.md`, `.claude/CLAUDE.md`, `.claude/rules/*.md`, and obvious local workflow docs.
3. Prefer the closest workspace rules first, then parent/global rules.
4. Deduplicate repeated guidance.
5. Note conflicts explicitly and prefer the most local rule unless the repo states otherwise.
6. Produce a compact digest instead of pasting raw files.

## Rules
- Keep the digest short and actionable.
- Capture only constraints that affect execution quality, safety, style, approval gates, or verification.
- If no local instructions exist, state that clearly and continue normally.
- Re-run discovery when moving into a different repo/worktree.

## Verification
- List the source files found.
- Show which rules are active versus merely present.
- Call out any unresolved conflict or ambiguity.

## Output Contract
- Artifact: compact instruction digest
- Evidence: source files and precedence order
- Decision: which rules are active
- Next: whether planning/execution can proceed or needs clarification
