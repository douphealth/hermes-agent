# WordPress full-bleed responsive landing page pattern

Use this when a WordPress page built inside the normal theme/content column feels too narrow, does not cover the screen well, or needs a premium app/SaaS-style landing-page canvas while staying inside one `<!-- wp:html -->` block.

## CSS pattern

Scope everything under the page wrapper. Do not globally alter the WordPress theme.

```css
.lp-page{
  position:relative;
  isolation:isolate;
  overflow-x:clip;
  width:100vw;
  max-width:100vw;
  margin-left:calc(50% - 50vw);
  margin-right:calc(50% - 50vw);
  margin-top:clamp(-84px,-6vw,-44px); /* optional: tighten theme gap above hero */
  padding:clamp(10px,1.5vw,22px) 0 clamp(48px,7vw,90px);
}
.lp-wrap{
  width:min(100%,1480px);
  max-width:1480px;
  margin:0 auto;
  padding:0 clamp(12px,2.4vw,40px);
}
.lp-hero{
  min-height:clamp(560px,calc(100dvh - 96px),780px);
  display:grid;
  align-items:center;
  padding:clamp(38px,5.4vw,86px) clamp(22px,4.5vw,72px);
}
.lp-hero-grid{
  display:grid;
  grid-template-columns:minmax(0,1.18fr) minmax(320px,.82fr);
  gap:clamp(24px,4vw,64px);
  align-items:center;
  width:100%;
}
@media (min-width:1181px){
  .lp-display{font-size:clamp(44px,4.15vw,66px);line-height:1.04;}
  .lp-lead{font-size:clamp(18px,1.35vw,22px);}
  .lp-sidecard{max-width:500px;justify-self:end;}
}
@media (min-width:901px) and (max-width:1180px){
  .lp-hero{min-height:auto;padding:48px 32px;}
  .lp-hero-grid{grid-template-columns:minmax(0,1fr) minmax(300px,.82fr);gap:28px;}
}
@media (max-width:900px){
  .lp-wrap{padding:0 clamp(10px,3vw,20px);}
  .lp-hero{min-height:auto;padding:clamp(30px,6vw,48px) clamp(18px,4.2vw,30px);}
  .lp-hero-grid{grid-template-columns:1fr;}
  .lp-sidecard{width:100%;max-width:680px;margin:0 auto;}
}
@media (max-width:560px){
  .lp-wrap{padding:0 8px;}
  .lp-display{font-size:clamp(30px,10.2vw,42px);line-height:1.08;}
  .lp-lead{font-size:16px;line-height:1.58;}
  .lp-cta-row{display:grid;grid-template-columns:1fr;gap:10px;}
  .lp-btn{width:100%;}
}
```

## Pitfalls

- `height:100vh` causes mobile browser viewport bugs. Use `min-height:100dvh` or a `clamp(..., calc(100dvh - header), ...)` variant.
- Full-bleed wrappers inside WordPress often need `margin-left:calc(50% - 50vw)` and `width:100vw`; otherwise the page remains trapped in the theme content column.
- **Classic theme content/sidebar math can break full-bleed math.** Twenty Ten-style themes may keep `#content` at ~970px with a sidebar margin; a `100vw` child then appears shifted left/clipped with a blank right column. Fix the page template with page-scoped CSS before tuning the hero:

```css
body.page-id-123 #container{width:100%!important;max-width:none!important;margin:0!important;}
body.page-id-123 #content{width:100%!important;max-width:none!important;margin:0!important;}
body.page-id-123 #primary,
body.page-id-123 #secondary,
body.page-id-123 .widget-area{display:none!important;}
body.page-id-123 .entry-content{width:100%!important;max-width:none!important;margin:0!important;overflow:visible!important;}
/* If the HTML block supplies the visible hero H1, hide the theme page title off-canvas to avoid a duplicate visible title. */
body.page-id-123 .entry-title{position:absolute!important;left:-9999px!important;width:1px!important;height:1px!important;overflow:hidden!important;clip:rect(0 0 0 0)!important;}
```

- If the theme/page title is hidden, put the real visible `<h1>` inside the landing page hero. Do not leave the page with only an off-canvas H1, and do not allow two visible H1/title blocks.
- Third-party fixed widgets can ruin otherwise premium heroes. On app landing pages, inspect `position:fixed` elements after publishing; if chat/help widgets overlap the hero card or CTA, hide or reposition them page-scope only:

```css
body.page-id-123 #frase-iframe,
body.page-id-123 #frase-greeting{display:none!important;visibility:hidden!important;opacity:0!important;pointer-events:none!important;}
```

- Diagonal/light-gradient hero backgrounds can accidentally cut under white hero text at desktop widths. After visual QA, shift the color stop deeper into the safe/dark side or add a dark text plate behind microcopy/secondary CTAs.
- After widening the canvas, large headings can become too tall. Rebalance desktop typography with a max font size and tighter hero grid instead of simply making everything bigger.
- A hero can cover the screen but still waste the first viewport if the theme inserts a large gap above it. A small scoped negative `margin-top:clamp(...)` can tighten the handoff from header to hero.
- `overflow-x:clip` on the scoped wrapper prevents decorative blobs and full-bleed math from creating horizontal scroll.
- Dark/gradient panels inside old WordPress themes may inherit theme heading colors (`h2 { color:#000 }`) even when the parent panel text is white. Add targeted `!important` rules for dark-panel headings, body copy, microcopy, and footer/editorial notes, then verify computed colors in the browser console.

## Verification

Use browser metrics and visual QA after publishing:

```js
(()=>{
  const q=s=>{const e=document.querySelector(s); if(!e)return null; const b=e.getBoundingClientRect(); return {x:Math.round(b.x),y:Math.round(b.y),w:Math.round(b.width),h:Math.round(b.height),bottom:Math.round(b.bottom),right:Math.round(b.right)}};
  return {
    vw:innerWidth,
    vh:innerHeight,
    scrollW:document.documentElement.scrollWidth,
    overflow:document.documentElement.scrollWidth-innerWidth,
    page:q('.lp-page'),
    hero:q('.lp-hero'),
    h1:q('h1'),
    sidecard:q('.lp-sidecard'),
    widgets:[...document.querySelectorAll('#primary,#secondary,.widget-area')].map(e=>getComputedStyle(e).display),
    fixed:[...document.querySelectorAll('*')].filter(e=>getComputedStyle(e).position==='fixed').map(e=>({tag:e.tagName,id:e.id,cls:String(e.className).slice(0,80),display:getComputedStyle(e).display,rect:(()=>{const b=e.getBoundingClientRect();return {x:Math.round(b.x),y:Math.round(b.y),w:Math.round(b.width),h:Math.round(b.height)}})()})),
    darkHeadings:[...document.querySelectorAll('.lp-page .dark h2,.lp-page .dark h3,.lp-final h2')].map(e=>({text:e.textContent.trim().slice(0,60),color:getComputedStyle(e).color,bg:getComputedStyle(e.parentElement).backgroundColor}))
  };
})()
```

Acceptance:
- public update returns HTTP 200
- one visible, meaningful hero H1 remains; any theme page title is hidden off-canvas only if replaced by a real visible landing-page H1
- primary CTA remains present and functional
- schema/script blocks remain present if applicable
- `overflow <= 0` or no visible horizontal scroll
- sidebar/widget areas are hidden or absent for the landing page when using a full-width canvas
- dark-panel headings and microcopy have high contrast by computed style, not only by intended parent color
- browser/vision check confirms the hero covers the viewport better, has no clipping, and looks polished above the fold
