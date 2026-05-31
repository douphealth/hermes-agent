---
name: faq-schema-and-answer-box-optimizer
description: Improve WordPress pages for FAQ schema, answer-box extraction, and quick-answer usefulness without adding spammy or fake FAQ sections.
version: 1.0.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [wordpress, faq, schema, snippets, answer-box, seo]
    triggers: [faq schema, answer box, people also ask, quick answers]
---

# FAQ Schema and Answer-Box Optimizer

## Purpose
Increase answer extraction quality and FAQ usefulness while avoiding low-value schema stuffing.

## Workflow
1. Determine whether the page naturally supports FAQ treatment.
2. Identify real recurring user questions from page intent, SERP/PAA patterns, objections, and query modifiers.
3. Add concise answer-first responses.
4. Keep FAQ answers specific, short, and self-contained.
5. Add FAQPage schema only when the on-page FAQ is real and useful.
6. Add other extraction-friendly formats when a paragraph alone is weak: lists, steps, small tables, pros/cons, or scenario bullets.
7. Verify schema is present in live HTML and does not conflict badly with existing plugin output.

## Good FAQ candidates
- troubleshooting pages
- care guides
- setup/how-to guides
- comparisons with recurring objections
- beginner guides with natural common questions

## Bad FAQ candidates
- pages where FAQs are obviously bolted on for SEO only
- pages with no real question-driven intent
- pages already overloaded with repetitive headings

## Answer-box rules
- answer the main question in 1–3 sentences near the top
- use direct phrasing
- avoid long throat-clearing intros
- define terms plainly
- use small tables or bullet summaries when faster than prose
- for “What is …” style headings, aim for a clean 40–60 word definition paragraph
- for “How to …” style headings, prefer numbered steps
- for comparison / cost / specs queries, prefer small tables
- make every answer block self-contained so it still works when extracted into snippets, AI Overviews, or voice answers

## AEO / GEO reinforcement
When optimizing answer sections, also check:
- does the heading match a real query or PAA phrasing?
- is the answer in the first 1–2 sentences below the heading?
- are risks, alternatives, mistakes, cost, and suitability questions covered where relevant?
- does the page include enough evidence or source support for trust-sensitive claims?
- can at least one answer block be cited cleanly by AI systems without surrounding context?

## Output contract
Report:
- quick-answer block added or improved
- FAQ questions added
- schema added or intentionally skipped
- which snippet / PAA / AIO patterns were targeted
- live verification state
