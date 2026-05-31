---
name: open-design-superpowers
description: Use when the user asks for SOTA design superpowers, Claude Design-like artifacts, landing pages, dashboards, decks, mobile/app prototypes, brand systems, visual redesign, critique, or design-system-driven UI. Routes Hermes through nexu-io/open-design's skills, DESIGN.md systems, craft rules, templates, frames, and anti-AI-slop critique before producing artifacts.
version: 1.0.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [design, open-design, ui, ux, artifacts, design-systems, frontend, decks, critique]
    related_skills: [design-md, popular-web-designs, claude-design, sketch, architecture-diagram, motion-impeccable-taste-design]
---

# Open Design Superpowers

## Overview

This skill turns Hermes into an Open Design-powered design agent. It uses the local clone of [`nexu-io/open-design`](https://github.com/nexu-io/open-design) at:

`/home/hermes/.hermes/vendor/open-design`

Open Design contributes a Claude Design-like workflow: skill-driven artifact creation, 150 `DESIGN.md` brand systems, universal craft references, device frames, templates, and a self-critique culture. Hermes should use it whenever the user asks for design, redesign, UI polish, decks, branded artifacts, screenshots, cards, prototypes, or design systems.

## Mandatory Workflow

1. **Route the brief through the catalog.** Run:
   ```bash
   /home/hermes/.hermes/skills/creative/open-design-superpowers/scripts/od_catalog.py search "<user brief keywords>"
   ```
   Pick one primary Open Design skill, one design system, and 2-4 craft references.

2. **Read the source files before designing.** Use the script or direct file reads:
   ```bash
   od_catalog.py show skill frontend-design
   od_catalog.py show system linear-app
   od_catalog.py show craft anti-ai-slop
   od_catalog.py show craft typography
   od_catalog.py show craft color
   ```
   The selected `SKILL.md` defines the artifact shape; the selected `DESIGN.md` defines the brand contract; craft files enforce universal quality.

3. **Ask only for genuinely missing constraints.** Otherwise choose a strong default:
   - SaaS/product: `linear-app`, `vercel`, `stripe`, `supabase`, `cursor`
   - Editorial/SEO/content: `editorial`, `monochrome`, `swiss`, `notion`
   - Luxury/fitness/consumer: `apple`, `airbnb`, `luxury`, `tesla`, `bmw`
   - Bold social/ads: `brutalism`, `colorful`, `xiaohongshu`, `canva`

4. **Produce real artifacts, not prose.** Prefer single-file HTML/CSS/JS when no repo exists. For repo tasks, patch the actual app using existing framework conventions. Include responsive states, keyboard/focus states, hover/active/disabled states, realistic copy/data, and accessible contrast.

5. **Avoid AI slop.** Ban generic purple-blue gradients, decorative blobs, random glass cards, lorem ipsum, fake metrics, ungrounded prices/claims, and icon soup. Use a single memorable visual point of view.

6. **Run a five-dimensional critique before final.** Score and fix:
   - Philosophy / point of view
   - Hierarchy / layout rhythm
   - Detail / typography / spacing / states
   - Function / accessibility / responsiveness
   - Innovation / memorability

7. **Verify visually when possible.** For HTML, open in browser or render screenshot. For repo UI, run the local app and inspect screenshots. Fix obvious visual defects before final.

## High-Leverage Routes

- **Landing page / website / dashboard / app screen:** `frontend-design` + a product design system + `typography`, `color`, `anti-ai-slop`, `accessibility-baseline`.
- **Existing UI polish:** `design-review` + active app screenshots + before/after notes.
- **Deck / pitch / report:** `deck-guizang-editorial`, `deck-swiss-international`, or `deck-open-slide-canvas` + `templates/deck-framework.html`.
- **Brand system creation:** `design-md`, `brand-guidelines`, or `creative-director`; output a `DESIGN.md` and optional Tailwind/DTCG export if relevant.
- **Social/image artifacts:** `card-xiaohongshu`, `card-twitter`, `article-magazine`, `ad-creative`, `prompt-templates/image/*`.
- **Mobile prototypes:** use device frames from `/home/hermes/.hermes/vendor/open-design/assets/frames/`.

## Reference Files

- Catalog snapshot: `references/catalog.md`
- Setup/refresh notes: `references/session-setup-and-maintenance.md`
- Search/show helper: `scripts/od_catalog.py`
- Open Design source: `/home/hermes/.hermes/vendor/open-design`

## Maintenance

Refresh the upstream Open Design clone with `git pull --ff-only` in `/home/hermes/.hermes/vendor/open-design`, then run `scripts/od_catalog.py summary` and a representative `search` query. If upstream structure changes, fix the helper script rather than copying the whole upstream library into this skill.

## Common Pitfalls

1. **Designing from memory instead of the library.** Always search/read the selected Open Design skill/system/craft first.
2. **Mixing too many design systems.** Pick one primary system; borrow only one supporting motif if needed.
3. **Claiming design quality without visual proof.** Use browser screenshots for HTML/app work whenever tools allow.
4. **Ignoring content truth.** Never invent fake prices, ratings, credentials, medical claims, financial claims, or performance claims.
5. **Over-polishing static posters for functional products.** Dashboards/apps need real controls, empty/loading/error states, and responsive behavior.

## Verification Checklist

- [ ] Catalog search performed for the brief
- [ ] Selected Open Design skill read
- [ ] Selected `DESIGN.md` read or authored
- [ ] Relevant craft references read
- [ ] Artifact/file created or app patched
- [ ] Visual/accessibility/responsive/state checks performed
- [ ] Five-dimensional critique applied
