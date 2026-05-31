---
name: motion-impeccable-taste-design
description: "Use when upgrading any website, WordPress post, landing page, app UI, or Claude/Hermes-generated frontend to avoid generic AI design. Applies a three-pass system: motion/easing polish, impeccable spacing/typography/layout correction, and taste/reference-driven art direction."
version: 1.0.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [design, motion, ui, wordpress, taste, references, responsive]
    related_skills: [redesign, popular-web-designs, claude-design]
---

# Motion + Impeccable + Taste Design Pass

## Overview

This skill operationalizes the three design upgrades from the referenced video into a Hermes workflow:

1. **Motion pass** — make the UI feel alive with tasteful easing, hover/active/focus states, scroll reveals, and transform/opacity animations.
2. **Impeccable pass** — correct spacing, typography, layout, alignment, hierarchy, color, and responsive fit across the whole interface.
3. **Taste pass** — anchor the redesign in real high-quality references instead of generic AI patterns.

Use this together with `redesign` for audits and `popular-web-designs` for concrete design-system references.

## When to Use

Use when the user says any of:

- "apply the skills from the video"
- "make this design less generic"
- "make it SOTA / premium / enterprise grade"
- "add motion / polish / taste"
- "make this WordPress page 1000x better"
- "use design references"

Do not use for pure backend tasks unless the deliverable includes UI or public-facing content.

## Required Workflow

### 1. Load companion skills

Before editing, load:

- `redesign` — audit checklist and WordPress responsive pitfalls.
- `popular-web-designs` — real visual systems and template references.

If WordPress content is involved, follow `redesign` WordPress verification notes: public render is source of truth, verify 320px and 390px mobile, and avoid REST-stripped `<style>` leakage.

### 2. Pick a taste direction

Choose one or two references appropriate to the brand/content. Do not blindly copy a famous site. Borrow principles:

- **Premium editorial / wellness:** Apple, Notion, Sanity, Airbnb.
- **SEO/content authority:** Mintlify, Sanity, Notion.
- **Affiliate/commercial comparison:** Stripe clarity + Apple whitespace + Pinterest/Notion card rhythm.
- **Developer/SaaS:** Linear, Vercel, Supabase, Raycast.
- **Dark technical:** Linear, Cursor, Superhuman, ElevenLabs.

State the selected direction in the working notes before implementation.

### 3. Impeccable pass — fix structure first

Apply in order:

1. **Typography:** distinctive font pair or careful system stack; stronger headline scale; max paragraph width ~65ch; `text-wrap: balance/pretty` where safe.
2. **Spacing:** consistent section rhythm; more whitespace; no cramped cards; CTA baselines aligned.
3. **Layout:** remove generic three-equal-card rows; use asymmetric grids, editorial callouts, step modules, comparison blocks, or masonry where relevant.
4. **Color:** one accent; consistent neutral family; no purple/blue AI-gradient default unless brand-specific.
5. **Surfaces:** subtle depth, tinted shadows, soft borders, noise/texture or ambient gradients only when they add polish.
6. **Content:** remove AI clichés; use specific, helpful copy; no lorem ipsum; no fake ratings/prices/specs.

### 4. Motion pass — add life without bloat

Use low-risk CSS first:

- `transition: transform .22s cubic-bezier(.2,.8,.2,1), box-shadow .22s, border-color .22s, background .22s;`
- Hover: `transform: translateY(-2px)` for cards/buttons.
- Active: `transform: translateY(0) scale(.99)`.
- Focus: visible outline/ring, never remove focus.
- Scroll reveal only if it degrades gracefully and respects `prefers-reduced-motion`.

Rules:

- Animate only `transform` and `opacity` unless there is a deliberate exception.
- Add `@media (prefers-reduced-motion: reduce)` to disable nonessential motion.
- Avoid infinite animations except tiny ambient backgrounds; never animate layout-critical dimensions.

### 5. Taste pass — remove AI fingerprints

Actively eliminate:

- Centered hero + two buttons + three identical cards.
- Purple/blue generic gradients.
- Generic bordered white cards with default shadows.
- Lucide/Feather icon cliché rows unless already part of stack.
- Words like "elevate", "seamless", "unlock", "game-changer", "delve", "tapestry", "next-gen".
- Fake-perfect metrics like 99.99% unless sourced.

Replace with:

- Specific hierarchy and section intent.
- Editorial callouts, annotated lists, proof modules, real examples.
- Asymmetric spacing and mixed card sizes when it improves comprehension.
- Visual rhythm that fits the brand, not the model default.

## WordPress-Specific Rules

- Use public rendered HTML as truth; stored post content is not enough.
- For REST-published posts, avoid raw `<style>` blocks in post body unless preservation is already proven.
- Prefer inline-scoped modules or site-level Additional CSS/custom plugin injection when needed.
- Always test 320px and 390px widths for overflow, skinny cards, hidden text, and image/card overlap.
- Purge caches and verify the marker exists publicly before claiming live.
- For affiliate posts, preserve required disclosures and accurate Amazon tags; do not invent specs, prices, ratings, or medical claims.

## Verification Checklist

- [ ] Companion skills loaded: `redesign` and `popular-web-designs`.
- [ ] Taste direction chosen from real references.
- [ ] Typography, spacing, layout, color, and surfaces improved.
- [ ] Motion states added for hover/active/focus where useful.
- [ ] `prefers-reduced-motion` respected.
- [ ] No generic AI copy/layout fingerprints remain.
- [ ] Desktop public render verified.
- [ ] 320px and 390px mobile render verified: no horizontal overflow, overlap, raw CSS, or broken product cards.
- [ ] Cache purged or bypass-verified.
- [ ] Final report includes exact changed page/site and evidence.
