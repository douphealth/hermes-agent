# EEAT / Author Trust Block Visibility Debugging

Session lesson from GearUpToFit (Twenty Ten + Elementor + WPCode + PhastPress): HTML presence is not enough. A trust block can appear in source, be after Related Posts, and still be invisible because it is nested inside a hidden parent created by a prior snippet/filter.

## Failure pattern

- New/server-rendered EEAT block exists in HTML (`#gutf-server-eeat-end`).
- Browser query finds the element and text.
- User sees only a blank strip below Related Posts.
- Computed style on the block says `display:block; visibility:visible; opacity:1`, but `getBoundingClientRect()` returns width/height `0` or the visible page shows a blank line.
- Parent chain reveals the real issue:
  - `#gutf-server-eeat-end` is nested inside `aside.guf-eeat`.
  - `aside.guf-eeat` was hidden by CSS such as `body.single-post aside.guf-eeat{display:none!important;}`.
  - Child styles cannot make the block visible while the parent is `display:none`.

## Browser probe

Run after page load:

```js
new Promise(resolve=>setTimeout(()=>{
  const box=document.getElementById('gutf-server-eeat-end') || document.querySelector('aside.guf-eeat');
  let n=box, chain=[];
  while(n && chain.length<10){
    const cs=getComputedStyle(n), r=n.getBoundingClientRect();
    chain.push({tag:n.tagName,id:n.id,cls:n.className,display:cs.display,visibility:cs.visibility,opacity:cs.opacity,overflow:cs.overflow,w:r.width,h:r.height,top:r.top});
    n=n.parentElement;
  }
  const related=[...document.querySelectorAll('h2,h3,strong')].find(e=>/related posts/i.test(e.textContent));
  resolve({exists:!!box,text:box?.innerText?.slice(0,180),afterRelated:box&&related?!!(related.compareDocumentPosition(box)&Node.DOCUMENT_POSITION_FOLLOWING):null,chain});
},1200))
```

## Fix pattern

If the new block is nested inside the legacy/WPCode wrapper, do **not** hide the legacy wrapper globally. Instead, either:

1. Move the server block outside the old wrapper before the footer; or
2. Force the parent wrapper visible and size-safe:

```css
body.single-post aside.guf-eeat{
  display:block!important;
  visibility:visible!important;
  opacity:1!important;
  width:100%!important;
  max-width:1080px!important;
  margin:54px auto 64px!important;
  clear:both!important;
  overflow:visible!important;
}
body.single-post aside.guf-eeat #gutf-server-eeat-end{
  width:100%!important;
  max-width:1080px!important;
  margin:0 auto!important;
  padding:0!important;
  display:block!important;
  visibility:visible!important;
  opacity:1!important;
}
```

## Verification standard

Before claiming fixed:

- Verify raw/source marker on `?phast=-phast`.
- Hard purge PhastPress/cache if normal URLs are stale.
- Verify no-query URL.
- Use browser automation to confirm real dimensions, not just selector existence:

```js
const box=document.getElementById('gutf-server-eeat-end');
const r=box.getBoundingClientRect();
({display:getComputedStyle(box).display, visibility:getComputedStyle(box).visibility, opacity:getComputedStyle(box).opacity, width:r.width, height:r.height, text:box.innerText.slice(0,120)})
```

Require non-zero width and height. If the user says it is missing and provides a screenshot with a blank strip, trust the screenshot and inspect parent-chain CSS immediately.

## Mobile distortion / overlay pattern

A block that is fixed on desktop can still be visually unusable on phones. In the GearUpToFit case, the EEAT block became visible but the user's Android screenshot showed it distorted and overlapping article text because multiple mobile-specific problems stacked:

- The server block inherited desktop/container widths from Twenty Ten/Elementor/WPCode (`aside.guf-eeat`) and exceeded the phone column.
- The new block was nested with old WPCode trust content, producing duplicate trust sections and overlay-looking content below the premium block.
- A sticky Elementor mobile header (`header.elementor-location-header`, `position: sticky`, `z-index:1000`) and a fixed chat greeting (`#frase-greeting`) floated over the EEAT section during scroll.
- Browser-source verification and desktop screenshots missed the problem; only a real mobile viewport measurement exposed it.

### Mobile-safe CSS pattern

Use mobile-first containment on the single-post trust wrapper and suppress legacy children only inside the final wrapper, not globally:

```css
body.single-post aside.guf-eeat.gutf-eeat-final-bottom{
  display:block!important;
  visibility:visible!important;
  opacity:1!important;
  width:min(100% - 28px, 1080px)!important;
  max-width:1080px!important;
  margin:42px auto 60px!important;
  padding:0!important;
  clear:both!important;
  overflow:visible!important;
  box-sizing:border-box!important;
}
body.single-post aside.guf-eeat.gutf-eeat-final-bottom > :not(#gutf-server-eeat-end){
  display:none!important;
  visibility:hidden!important;
  opacity:0!important;
  height:0!important;
  min-height:0!important;
  margin:0!important;
  padding:0!important;
  overflow:hidden!important;
}
body.single-post #gutf-server-eeat-end,
body.single-post #gutf-server-eeat-end *{
  box-sizing:border-box!important;
  max-width:100%!important;
}
@media (max-width:767px){
  body.single-post aside.guf-eeat.gutf-eeat-final-bottom,
  body.single-post #gutf-server-eeat-end{
    width:calc(100vw - 70px)!important;
    max-width:320px!important;
    margin-left:auto!important;
    margin-right:auto!important;
    overflow:visible!important;
  }
  body.single-post #gutf-server-eeat-end .gutf-eeat-shell,
  body.single-post #gutf-server-eeat-end .gutf-eeat-hero,
  body.single-post #gutf-server-eeat-end .gutf-eeat-panel,
  body.single-post #gutf-server-eeat-end .gutf-eeat-card{
    width:100%!important;
    max-width:100%!important;
    min-width:0!important;
    overflow:hidden!important;
  }
  body.single-post header.elementor-location-header,
  body.single-post .elementor-location-header{
    position:relative!important;
    top:auto!important;
    z-index:20!important;
  }
  body.single-post #frase-greeting{
    display:none!important;
    visibility:hidden!important;
    opacity:0!important;
    pointer-events:none!important;
  }
}
```

### Mobile verification standard

Do not rely on desktop browser resize alone. Use Playwright or equivalent with an actual mobile viewport and user agent, then measure document and block width:

```js
const { chromium } = require('playwright');
const browser = await chromium.launch({headless:true});
const context = await browser.newContext({
  viewport:{width:390,height:844}, deviceScaleFactor:3,
  isMobile:true, hasTouch:true,
  userAgent:'Mozilla/5.0 (Linux; Android 13; Pixel 7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0 Mobile Safari/537.36'
});
const page = await context.newPage();
await page.goto(URL, {waitUntil:'domcontentloaded'});
await page.waitForTimeout(4000);
const data = await page.locator('#gutf-server-eeat-end').evaluate(el => {
  const r = el.getBoundingClientRect();
  return {innerWidth, docWidth:document.documentElement.scrollWidth, bodyWidth:document.body.scrollWidth, width:r.width, height:r.height, text:el.innerText.slice(0,120)};
});
```

Accept only when:

- `docWidth <= innerWidth` (or no meaningful horizontal overflow from the block).
- EEAT width is within the mobile viewport (e.g. 320px inside 390px).
- Element screenshot shows one trust block, no duplicate overlay, and no sticky header/chat overlay covering content.
- A fixed-position scan returns no large sticky/fixed overlays over article content:

```js
[...document.querySelectorAll('body *')]
  .map(e=>{const r=e.getBoundingClientRect(), cs=getComputedStyle(e); return {tag:e.tagName,id:e.id,cls:String(e.className).slice(0,80),pos:cs.position,z:cs.zIndex,w:r.width,h:r.height,top:r.top,text:e.innerText?.slice(0,60)}})
  .filter(x=>(x.pos==='fixed'||x.pos==='sticky')&&x.w>100&&x.h>20)
```
