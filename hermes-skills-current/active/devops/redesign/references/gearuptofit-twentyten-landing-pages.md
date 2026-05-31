# GearUpToFit Twenty Ten landing-page quirks

Use this reference only for GearUpToFit-style WordPress landing pages running under the old Twenty Ten/Twenty Ten child layout.

## Quirk

Premium `<!-- wp:html -->` landing-page blocks can appear shifted left, clipped, or constrained because the classic theme keeps `#content` and sidebar/widget columns active even when the block itself uses `width:100vw`.

## Working pattern (landing pages)

1. Create or update the page through WordPress REST API.
2. Capture the real page ID from the REST response.
3. Replace any placeholder in the HTML/CSS with `body.page-id-{id}` selectors.
4. Apply page-scoped layout rescue:
   - `#container` and `#content`: `width:100%; max-width:none; margin:0`
   - `#primary`, `#secondary`, `.widget-area`: `display:none`
   - `.entry-content`: `width:100%; max-width:none; margin:0; overflow:visible`
5. If the hero supplies the visible H1, hide `.entry-title` off-canvas and make the hero heading the real `<h1>`.
6. Inspect fixed overlays. GearUpToFit may load Frase widgets (`#frase-iframe`, `#frase-greeting`) that can block hero app-preview cards; hide them page-scope if they obstruct conversion elements.
7. Run browser console QA for width/overflow, sidebar display, H1 visibility, CTA count, schema presence, fixed overlays, and computed contrast on dark panels.

## Homepage (front page) pattern

The homepage at gearuptofit.com uses a custom full-bleed HTML page built inside the Twenty Ten child theme's `.entry-content`. The constraints are the same as landing pages, but scoped with `body.home` instead of `body.page-id-NNN`.

### Rescue CSS for homepage

```css
/* --- Full-width container rescue --- */
body.home #container,
body.home #content {
  width: 100% !important;
  max-width: 100% !important;
  margin: 0 !important;
}

/* Remove sidebar on homepage */
body.home #primary,
body.home #secondary,
body.home .widget-area {
  display: none !important;
}

/* Let content element expand */
body.home .entry-content {
  width: 100% !important;
  max-width: 100% !important;
  margin: 0 !important;
  overflow: visible !important;
}

/* Hide Twenty Ten's auto-generated page title since the homepage hero has its own H1 */
body.home .entry-title {
  display: none !important;
}

/* Body flex fix (Elementor compatibility) — use Option A/B/C/D from wp-elementor-body-flex-blank-animation-fix.md */
body.home {
  min-height: auto !important;
}
```

### Blanks-animation pitfall

The homepage uses a custom design with:
- `body { animation: siteReveal 0.8s ease-out }` — body fades in
- `.g-rv`, `.g-rv-l`, `.g-rv-r` classes — content starts at `opacity:0` and gets `.in` class via IntersectionObserver JS
- The body has `display: flex; flex-direction: column; min-height: 577px` (Elementor default)

After the `siteReveal` animation ends (0.8s), `animation-fill-mode: none` causes the body to snap back to computed style. If the flex body hasn't expanded to contain all content, the viewport appears blank below the min-height. **Fix:** apply Option A or D from `wp-elementor-body-flex-blank-animation-fix.md`, AND verify that `g-rv` elements receive the `.in` class.

### Verification commands

```js
// Check body flex/animation constraints
const s = getComputedStyle(document.body);
console.log('display:', s.display, 'min-h:', s.minHeight, 'h:', s.height, 'anim:', s.animationName);

// Check body containment
console.log('scrollH:', document.body.scrollHeight, 'clientH:', document.body.clientHeight);

// Check reveal elements are getting applied
const revealed = document.querySelectorAll('.g-rv.in, .g-rv-l.in, .g-rv-r.in');
const total = document.querySelectorAll('.g-rv, .g-rv-l, .g-rv-r');
console.log('revealed:', revealed.length, '/', total.length);
```

## Verified examples

- `/free-fitness-plan/` used this pattern for a freemium fitness-plan app landing page.
- `/shoe-finder/` used this pattern for the Shoe Match app; the Frase widget had to be hidden after visual QA because it overlapped the hero card.
- **Front page (homepage)** — uses `body.home` selectors for the same container/sidebar/title rescue. The homepage has a full custom design with animated hero, brand strip, path cards, carousel, tool/review/guide grids, and newsletter — all served through `<!-- wp:html -->` in the page content.

Do not expose credentials or internal metrics in public page content. Use external authoritative references only when they improve user trust and are relevant to the page intent.