---
name: wordpress-category-hub-architecture
description: Build and upgrade WordPress category, tag, and hub-page architecture for stronger internal linking, clearer topical authority, and better crawl paths.
version: 1.0.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [wordpress, seo, taxonomy, hubs, internal-linking, category-pages]
    triggers: [category hubs, topical authority, hub and spoke taxonomy, category page optimization]
---

# WordPress Category Hub Architecture

Use this when a site has many scattered posts and weak taxonomy pages.

## Purpose
Turn categories and hub pages into real authority surfaces instead of thin archives.

## Workflow
1. Map the main topic clusters.
2. Identify the strongest parent hub for each cluster.
3. Score supporting posts by intent and authority contribution.
4. Decide which categories deserve optimization versus consolidation.
5. Add category intro copy, featured links, and clear hierarchy.
6. Normalize internal links from posts back to their correct hub.
7. Verify category/hub pages live and useful.

## Rules
- Do not create endless near-duplicate categories.
- Prefer fewer, stronger hubs over taxonomy sprawl.
- Category pages should summarize the topic and route users to the best pages, not just dump a post list.
- If a category is too thin to deserve indexable status, consolidate rather than decorate it.

## Minimum strong hub/page traits
- clear purpose
- intro paragraph with topic definition
- links to flagship pages
- links to key supporting pages
- visible trust/context if the site needs it
- no confusing overlap with another hub

## Production lesson: category description fields may strip HTML links
On some WordPress category edit screens, the taxonomy description field looks like it allows rich text, but saved output can still be sanitized back to plain text. Do not assume anchor tags in the category description will survive just because the editor UI exposes formatting controls.

Practical rule:
1. Use category description primarily for clean plain-text positioning.
2. Use Yoast term title/meta fields for archive snippet cleanup.
3. Verify the live archive HTML after save before claiming featured links were added.
4. If HTML links are stripped, route flagship links through a dedicated hub page or template/snippet layer instead of retrying the same term-description approach.

## Hub vs archive overlap resolution
When a polished standalone hub page and a category archive compete for the same intent, do not leave both indexable with near-identical positioning.

Recommended production pattern:
1. Choose the stronger surface as the canonical hub — usually the standalone page if it has curated copy, clearer routing, and better UX.
2. Keep the category archive for crawl flow and taxonomy structure.
3. Reposition the category archive as a supporting archive, not the main hub:
   - weaker archive-oriented title
   - archive-oriented meta description
   - `noindex, follow` via Yoast term settings when appropriate
4. Strengthen the winning hub page's title/meta so its role is explicit.
5. Verify live:
   - hub page = `index, follow`
   - archive = `noindex, follow`
   - both return `200`
   - the hub keeps the clean canonical URL

Example reusable pattern:
- `/learning/` = canonical hub
- `/category/learning-development/` = supporting archive, `noindex, follow`

This avoids split topical authority while preserving internal taxonomy paths.

## Output contract
Report:
- hub pages kept
- weak categories merged or deprioritized
- strongest flagship pages per hub
- internal-link routing strategy
