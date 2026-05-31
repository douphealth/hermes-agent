# WPCode EEAT/author box placement and visual rescue

Use this when a WPCode EEAT/author snippet is active but the user says it is not visible, ugly, or in the wrong location.

## Failure pattern

- Snippet root exists in HTML (`guf-eeat`, `aegis-root`, etc.) but the user reports “not working.”
- Curl/source checks pass, but desktop browser view still appears broken because:
  - cached no-query URLs serve stale HTML;
  - the box is below/above the wrong component (TOC, related posts, existing author box);
  - headings inside the box are captured by the TOC plugin;
  - CSS makes the box look like a raw/plain content dump.

## Safer sequence

1. Verify exact requested placement before changing return order.
   - Top: `return $html . $content;`
   - End: `return $content . $html;`
2. Compare offsets for snippet root, TOC, related posts, and any existing author block.
3. Use browser automation to verify visual placement, not only `curl`.
4. If TOC captures EEAT headings, convert internal `h2/h3` to `div role="heading" aria-level="..."`.
5. Apply scoped CSS to the snippet root, not global article headings.
6. Flush PhastPress/Cloudflare and verify both cache-busted and exact normal URLs.
7. If temporary cache-flush PHP is injected, remove it immediately after use and re-verify.

## Premium CSS direction

For author/EEAT blocks, prefer:

- a semantic `<aside>` root;
- max-width around 1000–1120px with mobile margins;
- soft gradient/radial background, not flat white box;
- tinted teal/brand shadows and a thin accent top bar;
- author avatar as rounded-square/squircle with verification badge;
- responsive grid: author card + review/proof card on desktop, stacked on mobile;
- proof pills for editorial policy, testing standards, corrections, affiliate transparency, medical disclaimer;
- footer strip for reader-support/affiliate disclosure;
- `@media` breakpoints at ~900px and ~520px.

## Do not claim done until

- The no-query URL contains the final code after cache flush.
- Browser render shows the block at the requested location.
- The TOC does not include EEAT/author internal headings unless explicitly desired.
- No raw JS/PHP text appears.
