# WordPress public post leakage + mobile rescue workflow

Use this when a WordPress blog post appears publicly with raw HTML/CSS, leaked editor notes, duplicated article blocks, malformed Gutenberg output, or product/resource modules that collapse on mobile.

## Core lesson

Do not claim a WordPress post is fixed just because the database/post body is clean. WordPress rendering, Gutenberg parsing, shortcodes, plugin cache, object cache, and theme/widget injection can still expose broken public HTML or stale duplicated output. Verify the **public rendered page** and the **visible text**, then browser-QA mobile fit.

## Safe repair sequence

1. **Confirm storage vs render separately**
   - Fetch stored content through XML-RPC/REST/admin source.
   - Fetch public URL with cache-busting query and `Cache-Control: no-cache`.
   - If stored content is clean but public output is huge/duplicated, treat it as cache/render-layer failure, not database corruption.

2. **Remove parser hazards before republishing**
   - Strip malformed Gutenberg comments such as `<!-- wp:... -->` when the source is not valid block markup.
   - Prefer clean plain HTML for urgent recovery when block serialization is unreliable.
   - Remove internal implementation notes before publishing, especially affiliate/image instructions like “replace placeholders,” “COPY/PASTE,” or raw image-token guidance.
   - Keep only one public affiliate/resource module per post unless the user explicitly asked for more.

3. **Add mobile CSS through the safest site-level channel**
   - Prefer WordPress Customizer “Additional CSS” / `custom_css[theme]` via `wp-admin/admin-ajax.php?action=customize_save` when admin cookies are available.
   - Add a unique marker comment (example: `HERMES_<SITE>_MOBILE_FIT_V1`) so public pages can be verified without guessing.
   - Use public head CSS for global layout rescue; do **not** put `<style>`/`@media` inside post bodies if the write path may strip tags and leak CSS as visible text.

4. **Mobile rescue CSS requirements**
   - `html, body` and primary containers: max-width 100%, no horizontal overflow.
   - `.entry-content`/article body: responsive font size, sane line-height, `overflow-wrap` for long links.
   - Images/iframes/video/embed: `max-width:100%; height:auto`; iframes get aspect ratio.
   - Tables: full-width with mobile horizontal scroll wrapper or block scrolling; avoid crushed columns.
   - Product/Amazon cards: stack at mobile breakpoints, full-width buttons, no fixed-width text columns, images constrained with `object-fit: contain`.
   - Cookie/newsletter/floating widgets: clamp max-width and avoid overlaying article text.

5. **Purge and prove public freshness**
   - Purge plugin cache (LiteSpeed/PhastPress/etc.) and Cloudflare if present.
   - Verify marker exists in public apex/origin HTML after purge.
   - If the marker is absent publicly, continue cache/render debugging; do not report success.

## Public verification checklist

Run against every direct public URL that matters:

- HTTP 200 for the intended URL, or explicitly report redirects separately.
- `h1` count is exactly 1.
- Expected product/Amazon module count is exactly 1 unless otherwise specified.
- Site-level mobile CSS marker is present in public HTML.
- Visible text contains no raw leakage:
  - `<div`, `</div>`, `<section`, `</section>`, `<p>`, `</p>`
  - `<!-- wp:`
  - `@media`
  - `IMAGE_URL_`
  - `START POST`, `END POST`, `COPY/PASTE`
  - internal notes such as “replace placeholders”

Important: when testing leakage, strip real HTML tags first and search the **visible text**. Searching the raw HTML will produce false positives because legitimate tags exist in source.

## Browser/mobile QA checklist

After source checks pass, inspect at mobile widths (320px and 390px if possible):

- `document.documentElement.scrollWidth <= viewport width + 2`
- No element has a layout width wider than viewport except intentional fixed/floating overlays.
- No paragraphs/cards collapse into skinny unreadable columns.
- Tables either fit or scroll horizontally without breaking the page.
- Product cards stack vertically with full-width CTAs.
- Iframes keep a correct aspect ratio.
- No blank giant ad/embed gaps that make the post look broken.
- Cookie/share/floating buttons do not cover content.

## User-facing response discipline

When the user is upset about broken public layout, keep the reply short, evidence-first, and action-oriented:

- State what was fixed.
- State the concrete public checks that passed.
- Call out remaining redirects/cache blockers separately.
- Do not over-explain internals or claim “perfect” until public mobile/browser QA has passed.
