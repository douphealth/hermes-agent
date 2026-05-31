# WordPress: Elementor body flex + animation → blank page fix

## Symptom

The homepage or landing page loads, plays an entry animation (fade-in, siteReveal, etc.), and then **becomes blank/white** — even though the full HTML/CSS is present. Scrolling or resizing the window may restore visibility.

## Root cause

Elementor sets:

```css
body {
  display: flex;
  flex-direction: column;
  min-height: 577px;       /* or similar fixed value from Elementor */
  animation: siteReveal 0.8s ease-out;
}
```

- The `animation-fill-mode` defaults to `none`, meaning the element snaps back to its computed style after the last keyframe.
- If `@keyframes siteReveal` goes from `opacity: 0` → `opacity: 1`, the body returns to computed opacity (1) after the animation ends — *unless* the flex layout fails to expand the body to contain full-bleed children.
- With `display: flex; min-height: 577px` and no `flex-grow` on a direct child, the body may not grow to contain full-bleed (`width: 100vw`) content, causing the viewport to display only the constrained body height below the header.
- The animation duration (0.8s) masks the initial viewport; after it ends, the empty area below `min-height` shows as blank.

## Quick verification

In browser console:

```js
// Check body flex/height constraints
const s = getComputedStyle(document.body);
console.log('display:', s.display, 'min-height:', s.minHeight, 'height:', s.height, 'animation:', s.animationName);

// Check if body is shorter than scrollable content
console.log('scrollHeight:', document.body.scrollHeight, 'clientHeight:', document.body.clientHeight);
// If scrollHeight >> clientHeight, content is overflowing the body container

// Check for reveal-class elements stuck at opacity:0 (IntersectionObserver fail)
const stuck = Array.from(document.querySelectorAll('.g-rv, .g-rv-l, .g-rv-r, .g-rv-s'))
  .filter(el => getComputedStyle(el).opacity === '0' && el.offsetHeight > 10);
console.log('reveal elements stuck at opacity:0:', stuck.length);
```

## Fix

Scope the fix to the affected page type (home, landing page). Do not globally alter Elementor body styles.

### Option A: Force body/home container to full height

```css
body.home #container,
body.home #content,
body.home .entry-content {
  min-height: 100dvh !important;
  height: auto !important;
}
body.home .entry-content {
  overflow: visible !important;
}
```

### Option B: Reset body flex on homepage only (if not needed)

```css
body.home {
  display: block !important;
  min-height: auto !important;
  animation: none !important;
}
```
**⚠️ Side effect:** Resetting `display: block` on body may break Elementor sticky headers that depend on the flex column layout. Verify after deploying.

### Option C: Extend the animation fill mode so opacity stays at 1

```css
body.home {
  animation-fill-mode: forwards !important;
}
```
(This only fixes the visual blink; the root flex constraint remains.)

### Option D: Force body to contain flex children

```css
body.home,
body.home #container,
body.home #content,
body.home .entry-content {
  min-height: 100vh !important;
  height: auto !important;
  flex: 1 0 auto !important;
}
```
Preserves the flex layout for Elementor compatibility while ensuring the body expands to full viewport height.

## Prevention checklist

When fixing full-bleed WordPress homepages or landing pages on Elementor sites:

- [ ] Check body computed style for `display: flex` + `min-height`
- [ ] Check body `animation-name` and `animation-fill-mode`  
- [ ] If full-bleed scoped CSS was applied (`width: 100vw; margin-left: calc(50% - 50vw)`), verify the parent containers expand to contain it
- [ ] Check `body.scrollHeight vs body.clientHeight` — a big gap means content overflows body
- [ ] On mobile, test with slow connection or after animation completes to catch the blank state
- [ ] **Check reveal-class elements** (`.g-rv`, `.g-rv-l`, `.g-rv-r`, `.g-rv-s`) — these start at `opacity: 0` with CSS and rely on IntersectionObserver JS. If the observer fails or the body flex issue prevents them from being in the viewport, they stay invisible. Verify they get `.in` class applied.
- [ ] **Body `animation-fill-mode`** — if set to `none` (default), the body snaps back to its computed style after animation ends. Set to `forwards` if the animation's end state (usually `opacity: 1`) must persist.

## Related

- `wordpress-full-bleed-responsive-landing-pages.md` — full-bleed CSS scoping for WordPress HTML blocks under classic themes
- `gearuptofit-twentyten-landing-pages.md` — site-specific Twenty Ten container/sidebar rescue pattern
