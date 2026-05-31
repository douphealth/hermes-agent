<!-- Consolidated from skill: premium-wordpress-html-blocks; original path: /home/hermes/.hermes/skills/devops/premium-wordpress-html-blocks -->

---
name: premium-wordpress-html-blocks
description: Reusable premium HTML/CSS content blocks for WordPress pages and posts. Focuses on elegant, theme-safe visual modules that improve readability, conversions, and perceived quality without breaking layouts.
version: 1.0.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [wordpress, html, css, visual-design, content-blocks, premium]
    triggers: [beautiful html elements, visual blocks, premium content modules, wordpress html blocks]
---

# Premium WordPress HTML Blocks

Use this when a WordPress post/page needs visual structure that feels premium but must remain safe inside unpredictable themes.

## Core rules
1. Always wrap custom HTML in `<!-- wp:html -->`.
2. Prefer single-column or simple stacked structures.
3. Avoid fragile multi-column grids unless verified live.
4. Use restrained borders, spacing, and backgrounds instead of flashy gradients and giant shadows.
5. Keep typography and spacing doing most of the work.
6. If the theme distorts a module, immediately downgrade to simpler markup.

## Block library

### Intent note
Short answer-first block for above the fold.

### Editorial note
Trust panel with links to about/editorial/methodology.

### Mistake box
Warns about common errors in a direct tone.

### Comparison table
Best for methods/options/product or plant comparisons.

### Scenario cards
Use for office/bathroom/bedroom or beginner/intermediate/collector segmentation.

### Checklist block
Use for process pages, beginner steps, seasonal care, or audits.

### Next-step CTA
Move readers to the next logical page without salesy nonsense.

### FAQ section
Only use for real recurring questions.

### Affiliate / Amazon product cards
Use when an article already has affiliate product boxes and the user asks for them to look more premium, modern, or conversion-ready.

Production-safe pattern:
1. Preserve the existing affiliate URLs, store IDs, product count, images, and surrounding article structure unless explicitly asked to replace products.
2. Update or replace only the scoped CSS/HTML for the product-card wrapper; do not rewrite the whole post just to polish cards.
3. Scope everything to a unique article/card class. Avoid global `.wp-block-image`, `.button`, `.card`, or `img` rules.
4. Make cards fit the article column, not the viewport: `width:100%`, `max-width:100%`, `box-sizing:border-box`, `min-width:0` on grid children, and constrained media/buttons.
5. On desktop, a clean 2-column grid is acceptable; on mobile, stack cards and force long product names/buttons to wrap (`overflow-wrap:anywhere` where needed).
7. If related-post or internal-link plugins inject blocks inside affiliate cards, hide those injections only inside the product-card scope. Do not globally disable related posts or remove normal editorial links elsewhere.
8. Verify both plain no-query URLs and cache-busted URLs at mobile and desktop widths. Required checks: no horizontal overflow, card count unchanged, images visible, affiliate CTA count unchanged, and no plugin-injected related blocks visible inside cards.
9. Avoid placing product modules inside existing CTA/quote/card grids. If a module is accidentally inserted inside a narrow parent (for example a two-column CTA wrapper), move the whole module outside that parent before styling. CSS alone cannot make a 940px product module look premium inside a 300px grid cell.
10. Use container queries for product cards, not viewport-only media queries. Default cards to stacked layout, then switch to image/text columns only when the card/container is wide enough (for example `container-type:inline-size` on the module and `@container (min-width:720px)`). This prevents desktop-width pages with narrow parent columns from squeezing titles into one-word lines.

### Concrete CSS component architecture for premium affiliate cards

Component class hierarchy:
```
.gutf-products                     → Wrapper: flex column on mobile, 2-col CSS Grid on desktop
.gutf-product-card                 → Card: 24px radius, glass-white bg, hover lift (translateY -4px)
.gutf-product-card.featured        → Featured card: spans full grid width, larger image area
.gutf-product-badge                → Ribbon badge: gradient bg, uppercase, drop shadow
.gutf-product-image-wrap           → 1:1 image container: gradient bg, inner shadow, hover zoom
.gutf-product-image-wrap img       → object-fit:contain, SL1500 high-res images
.gutf-star / .gutf-star.empty      → Individual star system for precise rating control
.gutf-pill / .gutf-pill.choice     → Mini badge pills with color variants
.gutf-cta-btn                      → Full-width gradient CTA with animated arrow
.gutf-disclosure                   → Italic affiliate disclosure
```

Key design values:
- `border-radius: 24px` on cards, `16px` on image wraps
- Layered shadow: `0 4px 12px rgba(0,0,0,0.04)` + `0 1px 3px rgba(0,0,0,0.06)`
- Spring hover: `cubic-bezier(0.34,1.56,0.64,1)` easing
- Pill badge colors: choice (amber `#fffbeb`), seller (red `#fef2f2`), prime (blue `#eff6ff`), bestseller (green `#f0fdf4`)
- CTA: `linear-gradient(135deg, #2563eb, #1d4ed8)` with `rgba(37,99,235,0.3)` hover shadow
- High-res product images: `_AC_SL1500_` suffix for Retina quality

## Styling rules
- border radius: 8px to 16px
- spacing: generous vertical rhythm
- backgrounds: soft neutral tints
- avoid pure black and loud neon accents
- mobile-first widths only
- line-height around 1.7 to 1.85 for dense guidance blocks

## Verification
After deployment verify:
- block renders cleanly
- no injected `<p><style>` corruption
- mobile width still works
- links remain clickable
- H1 structure not broken

## Output contract
Report:
- which blocks were used
- where they were inserted
- whether the page stayed visually stable live
