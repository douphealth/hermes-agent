# WordPress Tool-Page Rewrite QA Pattern

Use this after rewriting a WordPress tool/calculator/generator page through REST, especially when the defect involves stale year framing, broken rendered JavaScript, exposed code, or a browser-side widget.

## Trigger symptoms
- Public title, breadcrumb, H1, or category cards disagree on freshness/year (for example page says `[2025]` while archive positions it as 2026).
- Raw JavaScript or shortcode/code appears in the visible article body.
- REST `content.raw` looks fixed but public render still exposes old head, breadcrumb, schema, or plugin output.
- The page includes a client-side tool that must be tested in-browser, not just via HTML fetch.

## Proven execution sequence
1. Identify the exact object from the live URL using body `postid-*`, article ID, shortlink, or REST links. Do not rely only on slug search.
2. Back up the full REST object JSON before writing.
3. Update the REST object fields that are actually writable: `title`, `content`, `excerpt`, and visible body modules.
4. If the public head/breadcrumb/schema keeps stale values after REST writes, use a targeted active Code Snippets output-layer override rather than repeatedly rewriting the page body.
5. If raw JS is visible in the content, ensure the script is inside a safe HTML block and add a render-cleanup guard if the theme/plugin escapes or surfaces script text.
6. For browser tools, run a real browser functional test:
   - enter representative input values
   - click the generated action button
   - verify generated output fields, status messages, and no raw-code leakage in visible text.
7. Verify both plain and cache-busted URLs. Plain no-query URLs can remain stale even when cache-busted URLs are fresh.

## QA checkpoints
- HTTP `200` on plain URL.
- HTTP `200` on cache-busted URL.
- Browser-rendered `document.title` matches the intended current title.
- Breadcrumb and H1 match the current asset framing/year.
- Exactly one visible H1.
- No old-year token in title, breadcrumb, H1, or rewritten content block.
- No visible raw-code markers in rewritten content (`document.addEventListener`, `querySelectorAll`, `function(){`, `const safeUrl`, etc.).
- Schema JSON-LD still exists where relevant.
- Tool UI actually works in-browser.

## Link-check scoping pitfall
Theme/author/footer widgets can inject unrelated social/profile/email links into the same article wrapper. These may include Cloudflare email-protection pseudo-links or third-party profiles that return `403` to bots. Do not let those unrelated injected links falsely fail a page-specific rewrite.

For final acceptance:
- Check all links inside the rewritten content/tool block.
- Separately note unrelated injected theme/author/footer link defects if discovered.
- Do not claim sitewide link health from a scoped page rewrite unless a full-page/site crawl was requested.

## Reporting standard
Report evidence, not vibes:
- URL checked
- plain/cache-busted statuses
- final browser title
- H1 count/text
- breadcrumb text
- raw-code leak count
- old-year leak count in target surfaces
- rewritten-content links checked/bad count
- browser tool functional result
