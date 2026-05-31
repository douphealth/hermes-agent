---
name: skill-router
description: Use first when unsure which skill to load, when a task spans multiple skills, or when you want the smallest effective workflow with minimal token waste.
version: 1.0.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [routing, orchestration, token-efficiency, workflow]
    triggers: [which skill, route this, multi-step, ambiguous task, minimize tokens]
    do_not_use_for: [direct feature implementation, deep domain execution]
    compatible_workflows: [classify-route-execute-verify]
---

# Skill Router

## Purpose
Choose the smallest correct skill or workflow shape, avoid over-loading context, and prefer direct execution when decomposition adds no value.

## When to Use
- The right skill is unclear
- The task spans planning, implementation, review, and verification
- Multiple adjacent skills could apply
- Token efficiency matters

## Do NOT Use For
- Replacing the chosen specialist skill
- Over-engineering tiny tasks
- Delaying execution when the next step is obvious

## Workflow
1. Classify the task type.
2. Prefer the smallest likely matching skill.
3. Deep-load only one skill first.
4. Add a second skill only if the first explicitly hands off.
5. For unfamiliar repos, run `workspace-instruction-discovery` before heavy code work.
6. For risky or user-visible work, end with `auto-verification`.
7. Use swarm/subagent orchestration only when independent deliverables or verification separation justify the overhead.

## Routing Rules
- Tiny and obvious → execute directly.
- Multi-step but single-threaded → planning or specialist skill first.
- Independent deliverables → subagent/swarm pattern.
- High-risk, ambiguous, or production-sensitive → plan first, then execute, then verify.

## Verification
- State which skill was chosen.
- State why smaller alternatives were insufficient.
- State whether a verifier step is required.

## Output Contract
- Artifact: chosen skill/workflow shape
- Evidence: task classification and constraints
- Decision: direct / single-skill / multi-skill / subagent
- Next: exact next skill or action
