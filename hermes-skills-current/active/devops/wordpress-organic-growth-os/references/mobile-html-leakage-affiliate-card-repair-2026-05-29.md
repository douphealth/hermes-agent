# Mobile HTML Leakage + Affiliate Card Repair Pattern (2026-05-29)

Use when a WordPress SEO/content batch edit produces visible raw HTML/CSS, duplicated article bodies, or mobile-broken affiliate/product modules.

## Trigger signals
- User provides a mobile screenshot showing squeezed cards, horizontal overflow, floating widget overlap, or raw code/artifact text.
- User complains about “HTML leakage,” “not mobile fitted,” duplicated content, or visual breakage after an API/XML-RPC edit.
- Public browser/screenshot evidence contradicts earlier automated checks.

## Operator posture
- Do not defend previous verification. Acknowledge the visible failure in one sentence and fix immediately.
- Treat screenshots as higher-priority evidence than HTML-only checks.
- Do not claim “perfect” from source inspection alone; run public rendered geometry checks and leakage checks.

## Proven workflow
1. **Bypass caches when possible**: use origin IP + `Host:` header for admin/XML-RPC work; use cache-busting query strings for public checks.
2. **Backup first**: save the pre-edit post body/theme snippet if changing production bodies or CSS.
3. **Strip parser artifacts**: remove Gutenberg block comments (`<!-- wp:* -->`), internal source markers (`START POST`, `END POST`, `COPY/PASTE`), placeholder implementation notes, raw JSON-LD blocks visible in body, and any CSS accidentally stored as visible content.
4. **Prefer plain, valid HTML for emergency body repair** when block-parser recursion or Gutenberg comment mismatch is duplicating content.
5. **Fix mobile at source, not only CSS** when inline styles are embedded in post bodies:
   - remove product-card `min-width` values such as `min-width:245px` that force cramped mobile columns;
   - avoid `auto-fit minmax(260px, 1fr)` for narrow article containers if cards still squeeze text;
   - for emergency-safe affiliate modules, use a vertical card: image top, copy below, full-width CTA;
   - set `box-sizing:border-box`, `width:100%`, `min-width:0`, and block layout on cards/buttons.
6. **Add a site-wide rescue CSS layer only as a guardrail**, not as the sole fix, when post bodies contain inline styles. Put CSS in the theme/customizer/head layer so it is not visible in article text.
7. **Purge server/CDN cache** after body/CSS edits and verify the public page, not only REST/XML-RPC success.

## Minimum verification before saying done
Run checks against cache-busted public URLs:
- HTTP 200 for direct posts.
- Exactly one target Amazon/affiliate section unless intentionally more.
- No visible leakage after stripping scripts/styles and tags: `<div`, `</div>`, `<section`, `</section>`, `<!-- wp:`, `@media`, `IMAGE_URL_`, `START POST`, `END POST`, `COPY/PASTE`, internal placeholder notes.
- Rendered mobile geometry at 320px and/or 393px:
  - `documentElement.scrollWidth <= viewport width`;
  - product card is vertical/block, not side-by-side squeezed;
  - CTA is block/full-width inside card;
  - no fixed/min widths exceed the article container.
- Browser/screenshot inspection of at least one representative post after cache purge.

## Caveats
- A text/DOM snapshot may miss visual card squeezing. Use rendered geometry or screenshot/vision when the user’s complaint is visual.
- If two slugs are still redirecting because of a permalink/rewrite plugin, report that separately from body/mobile fixes; do not let redirect blockers mask verified fixes on direct URLs.
- Floating Telegram/share/cookie widgets can obscure content on screenshots; still fix the underlying card width first, then consider widget positioning only if it remains intrusive.
