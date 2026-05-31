<!-- Consolidated from skill: wp-page-content-redesign; original path: /home/hermes/.hermes/skills/wp-page-content-redesign -->

---
name: wp-page-content-redesign
description: Deploy custom HTML/CSS/JS pages via the WP REST API. Covers theme reset, Cloudflare workarounds, and WordPress auto-tag prevention
category: devops
tags: [wordpress, rest-api, homepage, css, html, redesign, cloudflare]
---

# WordPress Page Content Redesign via REST API

## Overview
Deploy rich custom HTML/CSS/JS directly into WordPress page content via the REST API. Used for complete homepage redesigns with custom CSS animations, responsive layouts, and modern design without theme modification.

## The Core Challenges

### 1. Cloudflare WAF blocks PUT requests (1010 error)
Cloudflare returns "error code: 1010" when you try to PUT to the REST API. Workaround - use POST with X-HTTP-Method-Override header.

### 2. WordPress auto-injects p tags (destroys layout)
WordPress wraps raw HTML in p tags, breaking CSS grids and flexbox. Prevent this by wrapping content in an HTML block comment.

### 3. JSON BOM character in REST responses
WordPress REST API responses may start with a UTF-8 BOM character. Strip it before parsing.

### 4. Use data-binary with file for large payloads
Never pass large HTML/CSS content via command line dash-d string. Shell escaping breaks. Write to a temp file and use data-binary at-file.

## Complete Workflow

If the task includes not just redesign but SEO-content upgrading inside the page body, also load `wordpress-sota-seo-content-system`.
That companion skill defines:
- answer-first intros
- premium human-writing standards
- restrained visual HTML modules
- schema decisions
- internal-link architecture
- rewrite safety and verification rules

### Step 1 - Find the page
```python
import subprocess, json, base64

site = "https://example.com"
rest_creds = "username:app_password"
b64 = base64.b64encode(rest_creds.encode()).decode()

r = subprocess.run(f'scurl -sS "{site}/wp-json/wp/v2/settings" -H "Authorization=[REDACTED] {b64}"', shell=True, capture_output=True, text=True)
data = json.loads(r.stdout.lstrip('\ufeff'))
page_id = data.get('page_on_front')
```

### Step 2 - Build clean HTML
Key CSS reset rules for GeneratePress/Themes:
- `body.home .entry-content, body.home .inside-article { background: transparent !important; }` strips theme wrappers
- `body.home .entry-title { display: none !important; }` hides the auto-title
- `body.home { overflow-x: hidden !important; }` prevents horizontal scroll
- Scope ALL CSS with `body.home .your-prefix` selectors
- Keep all HTML inside one wrapper div with a unique class
- Balance all opening/closing tags carefully

### Step 3 - Wrap and deploy
```python
import json

# Wrap to prevent WordPress wpautop filter
wrapped = f'<!-- wp:html -->\n{your_content}\n<!-- /wp:html -->'

payload_file = '/tmp/payload.json'
with open(payload_file, 'w') as f:
    json.dump({"content": wrapped}, f)

# Deploy via POST with Cloudflare bypass
import subprocess
cmd = (
    'curl -sS --max-time 60 -X POST '
    f'{site}/wp-json/wp/v2/pages/{page_id}?context=edit '
    f'-H "Authorization=[REDACTED] {b64}" '
    f'-H "Content-Type: application/json" '
    f'-H "X-HTTP-Method-Override: PUT" '
    f'-H "User-Agent: Mozilla/5.0" '
    f'--data-binary @{payload_file}'
)
r = subprocess.run(cmd, shell=True, capture_output=True, text=True)
```

### Step 4 - Verify
```python
# Verify API saved it
r = subprocess.run(f'curl -sS "{site}/wp-json/wp/v2/pages/{page_id}?context=edit" -H "Authorization=[REDACTED] {b64}"', shell=True, capture_output=True, text=True)
data = json.loads(r.stdout.lstrip('\ufeff'))
content = data['content']['raw']

# Check for p-tag wrapping errors
assert '<p><style>' not in content
assert '<p>  <section' not in content

# Verify live page with cache-buster
subprocess.run(f'curl -sS "{site}/?nocache=1" -o /tmp/verify.html', shell=True)
with open('/tmp/verify.html') as f:
    html = f.read()

# Check sections present
for section in expected_sections:
    assert f'class="{section}"' in html, f"Missing section: {section}"
```

## REST API Credentials
Application passwords (not WP-Admin login credentials) are used for REST API auth. They are separate credentials stored in the user's secret file.

## Common Pitfalls
- Missing context=edit returns only rendered HTML, not the editable content
- Cloudflare WAF (error 1010) blocks direct PUT. Always use POST with X-HTTP-Method-Override header
- WordPress wpautop filter wraps raw HTML in p tags. Always wrap in `<!-- wp:html -->` ... `<!-- /wp:html -->`
- Large payloads via shell dash-d argument break on special chars. Use `--data-binary @file`
- UTF-8 BOM in REST responses breaks json.loads. Strip with `.lstrip('\\ufeff')`
- Theme CSS conflicts. Use `body.home .entry-content { background: transparent !important; }`
- Div tag balance matters. Mismatched divs cause layout cascade failures
- For homepage redesigns, scope all CSS with `body.home .your-prefix` selectors
- GeneratePress `separate-containers` can leave a persistent blank strip on the right even when parent wrappers are `width:100%`. If the page must truly fill the viewport, force the actual content node full-bleed: `body.page-id-XXX .entry-content { width:100vw !important; max-width:100vw !important; margin:0 calc(50% - 50vw) !important; overflow:hidden !important; }`
- Older / classic themes (including Twenty Ten child-theme layouts) can keep iframe pages boxed because the real constraints live on `#wrapper`, `#container`, `#content`, and sidebar columns like `#primary` / `#secondary`, not just the iframe block. For page-scoped full-bleed fixes, reset those exact wrappers to `width/max-width:100%`, `margin:0`, `padding:0`, `float:none`, hide the sidebars and `.entry-title`, then force `#content` itself to `width:100vw` with `margin:0 calc(50% - 50vw)`.
- Critical production finding for classic-theme + Elementor hybrid sites: even after page-level iframe/full-bleed fixes, the public homepage HTML can still include legacy sidebar/footer/header noise from theme widget areas and global Elementor templates. Inspect `/wp-json/wp/v2/sidebars` and `/wp-json/wp/v2/widgets?sidebar=primary-widget-area&context=edit` to find classic widgets such as search, archives, recent posts, and meta blocks that continue polluting homepage source.
- Reusable cleanup pattern for that case:
  1. Back up the active sidebar and widget objects.
  2. Move noisy widgets out of `primary-widget-area` into `wp_inactive_widgets` via `/wp-json/wp/v2/widgets/{id}` updates and/or clear the sidebar widget list via `/wp-json/wp/v2/sidebars/primary-widget-area`.
  3. Add page-scoped cleanup JS/CSS in the homepage content as a last-mile render cleanup for nodes like `#primary`, `.widget-area`, `.entry-title`, or known Elementor footer/header wrappers.
  4. Verify both homepage and a normal article page after any global widget or template change so you do not break the rest of the site.
- Older / classic themes (including Twenty Ten child-theme layouts) can keep iframe pages boxed because the real constraints live on `#wrapper`, `#container`, `#content`, and sidebar columns like `#primary` / `#secondary`, not just the iframe block. For page-scoped full-bleed fixes, reset those exact wrappers to `width/max-width:100%`, `margin:0`, `padding:0`, `float:none`, hide the sidebars and `.entry-title`, then force `#content` itself to `width:100vw` with `margin:0 calc(50% - 50vw)`.
- For iframe homepages on GeneratePress, do not rely only on parent container resets. Also set `.site`, `.site-content`, `.content-area`, `.site-main`, `article`, `.inside-article` to `max-width:none`, `margin:0`, `padding:0`, then force the iframe wrapper and iframe itself to `width:100vw` and `height/min-height:100vh` (or `100dvh` where supported)
- For old-theme iframe pages, after resetting classic wrappers, also set the iframe wrapper and iframe to `width/min-width:100vw` and `height/min-height:100dvh` with a `100vh` fallback via `@supports not (height: 100dvh)`. This avoids residual gutters and short viewport embeds on mobile browsers.
- If you see empty black or cream space beside an embedded app, that is usually the theme container still constraining layout, not the remote app itself. Verify by checking front-end HTML for GeneratePress wrappers and by inspecting the embedded app bundle/CSS separately before changing the app URL
- New production finding for old-theme + Elementor hybrid homepages (for example Twenty Ten child theme with Elementor header/footer plus iframe front page): page-content cleanup alone may not remove raw homepage source clutter. Even after adding a hidden H1/trust block and DOM-removal JS, the public HTML can still include server-rendered sidebar widgets, footer promos, newsletter blocks, archive lists, and other legacy chrome.
- In this setup, inspect both: (1) the page content for the front page object, and (2) the site-wide theme/widget/template layer. Useful endpoints: `/wp-json/wp/v2/sidebars`, `/wp-json/wp/v2/widgets`, `/wp-json/wp/v2/elementor_library`, and `/wp-json/elementor/v1/site-editor/templates-conditions/{id}`.
- High-value remediation path discovered in production:
  1. Add a nonvisual homepage H1 + summary + trust/topic links inside the front-page content.
  2. If the raw HTML still contains sidebar clutter (`Search`, `Archives`, `Meta`, old recent-post widgets), inspect `primary-widget-area` and move those widgets to `wp_inactive_widgets` via the widgets REST API.
  3. If the homepage is still wrapped by unwanted theme/header chrome, consider switching the front page template to `elementor_canvas` when safe. This can remove the old global header from the homepage response while preserving the iframe/app shell.
  4. Verify both the raw HTML and the extracted meaningful text after the change. Success is not just “the link exists in DOM”; success is that meaningful homepage text starts with the intended title/H1/summary and the old sidebar/archive/meta clutter no longer appears in the extracted text.
- Important limitation learned in production: Elementor header/footer condition updates via `/wp-json/elementor/v1/site-editor/templates-conditions/{id}` may return success but not reliably remove already-cached global templates from the public homepage. Treat that route as experimental and always verify the public HTML after cache clearing. Do not claim header/footer exclusion worked unless the live homepage response actually changed.
- Another production finding: even after successful REST config changes, some stale theme/template fragments may persist in the public raw HTML because of caching or theme-level rendering. Be explicit with the user about what is fixed at the content/config layer versus what still persists in cached server output.
- Critical production finding for iframe / mirrored-app homepages: visible SEO trust rows or visible intro sections can distort the visual homepage even if the HTML is simple. If the user wants the homepage appearance untouched, do NOT prepend visible trust bars, intro paragraphs, or hero copy above the iframe/app shell.
- New production finding for Astra-based custom HTML homepages: even when the custom page is correctly scoped under a unique wrapper, the design can still look boxed, distorted, or partially hidden because the theme's `.ast-container` and related wrappers continue constraining width/padding, while animation/reveal CSS leaves sections invisible until JS runs.
- Reusable hardening pattern for Astra homepage deployments:
  1. Back up the front-page REST object first.
  2. Add page-scoped CSS targeting `body.page-id-XXX` that resets `.ast-container`, `.content-area.primary`, `.site-main`, `.entry-content.clear`, and `.ast-article-single` to `width:100%`, `max-width:none`, `margin:0`, `padding:0`.
  3. Force the custom homepage wrapper itself to true full bleed with `width:100vw`, `max-width:100vw`, and `margin:0 calc(50% - 50vw)`.
  4. Hide interfering default theme chrome such as `.entry-header` and `.post-thumb-img-content` when the custom homepage already provides its own hero.
  5. If sections appear as giant blank/placeholder blocks, change reveal-on-scroll patterns so content is visible by default and enhanced by JS second, not hidden by default waiting for JS/IntersectionObserver.
  6. Re-check both plain and cache-busted URLs, because plain HTML may still show the distorted pre-fix container state until caches refresh.
- Verification rule for Astra custom homepages: do not rely only on REST content or accessibility snapshots. Also inspect computed wrapper widths in-browser and use a real visual screenshot to confirm the boxed/container distortion is gone and that sections are no longer hidden.
- New production finding for block-theme homepage replacements (for example Twenty Twenty-Four / `.wp-site-blocks` themes): users often provide a full standalone document (`<!DOCTYPE html>`, `<html>`, `<head>`, meta tags, footer, scripts) that must be adapted before inserting into WordPress page content. Do **not** paste the whole document raw into `content.raw`.
- Reusable hardening pattern for block-theme homepage replacements:
  1. Back up the front-page object first.
  2. Strip document-shell markup and extract only the pieces that belong inside page content: schema script, CSS, body HTML, and JS.
  3. Wrap the visible homepage inside one page-scoped shell such as `.site-homepage-shell` and force it full-bleed with `width:100vw`, `max-width:100vw`, and `margin:0 calc(50% - 50vw)`.
  4. Add page-scoped CSS that resets `.wp-site-blocks > main`, `.wp-block-post-content`, `.wp-block-group`, and similar wrappers to `width:100%`, `max-width:none`, `margin:0`, `padding:0`.
  5. Hide duplicate block-theme template parts on that page only when the custom homepage already includes its own nav/footer, for example `body.page-id-XXX .wp-site-blocks > header.wp-block-template-part` and `body.page-id-XXX .wp-site-blocks > footer.wp-block-template-part`.
  6. If the site outputs extra homepage-only blocks after the custom footer (for example an injected newsletter section), identify the offending node in-browser and hide it page-scoped rather than leaving a second pseudo-footer below the page.
  7. Fix supplied internal links before publish. Standalone homepage mocks often use placeholder slugs like `/about/`, `/contact/`, `/privacy/`, `/terms/`, `/mouse-prevention/`; verify the live site's real slugs and remap them before deployment.
  8. For counters and reveal-on-scroll UI, make the page usable without JS: counters should have sensible initial values and reveal blocks should be visible by default, with JS only enhancing them.
  9. Verify both plain and cache-busted URLs, because stale no-query output can temporarily keep the old homepage or old theme header/footer visible even after REST success.
- Verification rule for block-theme homepage replacements: check not only the DOM text but also that there is no duplicate site header/footer, no giant blank sections from hidden reveal blocks, no orphan section below the footer, and that the custom wrapper actually spans the viewport.
- Safer pattern for non-distorting homepage SEO on sensitive custom pages: inject a small offscreen HTML block wrapped in `<!-- wp:html -->` with `position:absolute`, `left:-10000px`, `width:1px`, `height:1px`, `overflow:hidden`. Put the H1, short descriptive paragraph, and internal trust links there so the content exists in the HTML without altering the visible layout.
- Verify the non-distorting pattern by fetching live HTML and checking both: (1) the marker block exists, and (2) the previously visible/distorting phrases no longer appear in the rendered visual surface. If the user complains that the homepage was 'fucked up' or distorted, immediately remove the visible block and switch to the offscreen pattern instead of debating the SEO tradeoff.
- On iframe/Lovable homepage deployments, visible trust rows or intro sections injected above the iframe can distort the intended hero/layout.
- Earlier guidance preferred an offscreen SEO block as a compromise, but production experience showed that even hidden/offscreen injections can still trigger user-visible weirdness on some devices, cached renders, or embedded-app/theme combinations. Examples include unexpected text surfacing at the top of the homepage or users reporting the homepage was still 'fucked up' despite the block being offscreen in raw HTML.
- Updated safest rule: if the homepage is a sensitive embedded app / iframe experience and the user prioritizes pristine visuals, do NOT inject any homepage trust/H1/intro block at all unless you can visually verify on the real rendered page that it is completely non-visible on both mobile and desktop.
- Preferred order for these sensitive homepages:
  1. First improve trust via separate About / Editorial Policy / Review Methodology / Contact pages.
  2. Improve author entities, article-level trust blocks, excerpts, and internal links.
  3. Only consider homepage DOM injections if strong visual verification is available.
- If a visible trust block distorts an iframe homepage, remove it immediately.
- If an offscreen trust block still leads to user-reported visual artifacts, remove that offscreen block too instead of debating whether it should have been invisible.
- For sensitive iframe/Lovable homepages, the production-safe default is now: keep the homepage DOM as close to the original embedded experience as possible, and move SEO/E-E-A-T improvements to trust pages, metadata/excerpts, author pages, and article-level internal linking.
- Verification rule: do not rely only on raw HTML or source inspection for these homepage changes. Use real visual QA when available (browser screenshot or user-provided screenshot). If browser tooling is unavailable, treat user-reported visual distortion as authoritative and roll back homepage injections immediately.
- New production finding for iframe/Lovable homepages on classic WordPress themes: adding a hidden/offscreen homepage H1, summary paragraph, trust links, and topic links inside the page content is a safe, effective way to improve homepage SEO/AEO/AI visibility without changing the visible hero.
- Reusable pattern for these source-safe homepage boosts:
  1. Keep the iframe/app shell visually unchanged.
  2. Add one hidden but crawlable H1 aligned to the title tag.
  3. Add one short hidden summary paragraph describing the site’s exact topic cluster.
  4. Add hidden trust/topic navigation links to About, Contact, legal pages, key hubs, and a few flagship articles.
  5. Optionally upload and link an `llms.txt` asset from Media when root-level deployment is unavailable.
- Critical limitation discovered on GearUpToFit/Twenty Ten-child style homepages: page-content changes alone do NOT remove all legacy theme source clutter. Even after visually hiding theme chrome and adding better hidden homepage SEO blocks, the raw homepage HTML can still contain old sidebar/archive/footer text, widget output, and legacy promotional fragments emitted by the theme/template layer.
- Practical rule: if the user wants the visual homepage preserved but cleaner source-level SEO signals, page-content editing is enough to add H1/trust/topic reinforcement. If the user wants the raw homepage HTML fully purged of legacy archives/sidebar/footer boilerplate, that requires theme/template-level cleanup rather than only updating `content.raw`.
- New production finding for trust/editorial/methodology pages: avoid aggressive custom CSS redesigns (hero gradients, card grids, shadows, complex responsive layouts) unless the user explicitly asks for a visual redesign and the theme has been tested. These pages can distort badly on both desktop and mobile because theme CSS and plugin wrappers interact unpredictably.
- Safer default for premium trust pages on unknown WordPress themes: ship high-quality content-first HTML with native headings, paragraphs, lists, and simple links inside one `<!-- wp:html -->` wrapper, with minimal or no custom CSS. Prioritize readability, structure, and trust content over decorative styling.
- If a trust page gets visually distorted after a premium redesign, immediately roll back the custom styled layout, keep the stronger copy, and redeploy a stripped-down content-only version. Verify distortion is gone by checking that custom style markers are absent from live HTML and that the page still returns the upgraded headings/lists/links.
- Critical production finding for theme-managed inner pages: user-visible junk can come from theme/header output that does not exist in `content.raw`. Example: MysticalDigits/GeneratePress emitted `<div class="page-hero">...<!-- Merge Hero -->...</div>` plus a rogue `<h1 class="gb-headline gb-headline-cbeb28df">Hello World</h1>` above the actual page content on `/review-methodology/`.
- When the user reports a visible heading or hero block that you cannot find in the REST page content, inspect the live public HTML around the top of the page and search for theme wrappers such as `.page-hero`, `.inside-page-hero`, `.entry-header`, `h1.gb-headline`, or generated headline classes. Do not assume the bug is inside the page body.
- Safe emergency mitigation for a rogue theme-injected heading on a single page: add page-scoped CSS inside the page content targeting `body.page-id-XXX .page-hero`, `body.page-id-XXX h1.gb-headline`, and any known generated class (for example `.gb-headline-cbeb28df`) with `display:none !important; visibility:hidden !important; height:0 !important; overflow:hidden !important; margin:0 !important; padding:0 !important;`.
- If CSS suppression is not enough or cached/render timing still exposes the rogue node, add a tiny page-scoped `DOMContentLoaded` script that removes those hero/headline nodes from the DOM. Use this only as a last-mile mitigation when direct theme editing is unavailable through REST.
- Verification rule for theme-injected junk: screenshots/user reports outrank assumptions from `content.raw`. Confirm with live HTML that the rogue string/class exists, deploy the page-scoped kill switch, and then verify the kill-switch CSS/JS is present on the public page.
- Source-level GeneratePress fix discovered in production: the rogue heading may come from global GP Elements, not the page itself. Inspect `/wp-json/wp/v2/gp_elements?per_page=100&context=edit` and read candidate `gp_elements` objects such as `page-hero` elements hooked into `generate_after_header`.
- In the MysticalDigits case, the real source of visible `Hello World` headings was two global elements (`site-hero-new` and `posts-hero-new`) whose `content.raw` contained a GenerateBlocks headline block with `gpDynamicTextReplace` set to `Hello World` and rendered `<h1 class="gb-headline gb-headline-cbeb28df gb-headline-text">Hello World</h1>` above page/post content.
- Reusable fix pattern for this class of bug:
  1. Query `gp_elements` via REST.
  2. Search `content.raw` for the rogue text or generated class.
  3. Patch the offending global element(s), removing the hardcoded replacement text.
  4. If the hero should still exist, inject a tiny script after the empty hero `<h1>` that sets the hero title from `document.title` on `DOMContentLoaded`.
  5. Verify across multiple URLs (page, about page, posts), not just the originally reported URL.
- After the source-level GP Elements fix is deployed, remove page-level emergency kill switches when possible. Leaving the kill switch in place can hide the now-correct hero title or leave a blank heading area.
- New production finding for custom article blocks inserted inside normal WordPress posts/pages: do not apply homepage/full-bleed patterns to article bodies unless the design explicitly calls for it. A custom wrapper such as `.ff-post` can render wider than `.entry-content`, causing right-side clipping even when REST content and HTTP checks pass.
- Reusable containment fix for article-body HTML blocks:
  1. Scope a patch to the article wrapper and page content, for example `.entry-content > .ff-post, .ff-post { width:100% !important; max-width:100% !important; margin-left:0 !important; margin-right:0 !important; box-sizing:border-box !important; }`.
  2. Constrain descendants with `.ff-post * { box-sizing:border-box !important; max-width:100% !important; }` and media with `img, picture, video, iframe, svg { max-width:100% !important; height:auto !important; }`.
  3. Pay special attention to tables: fixed-width tables, `thead/tr/th/td`, and long labels can be the real right-edge offenders on mobile. Add scoped table rules such as `width:100%`, `max-width:100%`, `table-layout:auto/fixed` as appropriate, wrapping/breaking long text, and overflow containment only inside the article wrapper.
  4. Preserve the theme’s normal content column rather than forcing `100vw`; the goal is fit-within-column, not full-bleed.
- Verification rule for article-body layout fixes: HTTP 200, REST save success, and link checks are insufficient. Use real browser layout metrics across desktop/tablet/mobile to compare the custom wrapper’s left/right bounds against `.entry-content`, and inspect offenders whose bounding boxes exceed the viewport/content column. Then visually inspect at least the user-reported URLs with screenshots/browser vision before claiming the distortion is fixed.
- Production lesson from full custom PlantasticHaven homepage rebuilds: visually successful REST deployment still needs explicit homepage-specific guardrails.
  1. Add a unique marker class/data attribute to the homepage wrapper (for example `ph-home-2026`) and verify it on both normal and cache-busted public URLs after deploy.
  2. Keep exactly one visible H1 on the public page; custom homepage H1 plus theme title output can silently create duplicates.
  3. Add schema inside the HTML block only after adapting it to page content, then verify the schema marker/string exists in the public HTML.
  4. For card grids and authority-map layouts, add `min-width:0` to grid children. Otherwise long links/headings can create invisible right-edge overflow even when the section visually looks fine.
  5. For comparison/authority tables, avoid desktop `min-width` assumptions. On mobile, convert rows/cells to stacked block layout or aggressively apply `table-layout:fixed`, `min-width:0`, and `overflow-wrap:anywhere` so there is zero horizontal overflow.
  6. Chat/help widgets can auto-open greetings or launchers over the hero after otherwise clean deployments. PlantasticHaven specifically has both a custom `#pthx-card` / `#pthx-launcher` concierge and a Frase widget (`#frase-answers-bot`, `#frase-wrapper`, `#frase-greeting`). If the user wants a pristine homepage, page-scope CSS to hide all of those homepage-only, then verify with browser DOM metrics and screenshot/vision that no visible widget remains over the hero. Leaving only a compact launcher may still be considered a blocking visual issue if it overlaps hero imagery.
  7. Large editorial hero headings can split words awkwardly at desktop/tablet widths. Add `overflow-wrap:normal`, `word-break:normal`, `hyphens:none`, adjust the hero grid ratio, and reduce `clamp()` max size until browser visual QA confirms natural line breaks.
  8. On PlantasticHaven, Seraphinite Accelerator may keep the plain homepage HTML/CSS partially stale even when the cache-busted URL shows the fresh REST content. Check both normal and `?nocache=` URLs. Browser rendering may still pick up the updated page while raw curl of `/` shows stale inline CSS. Do not rely on one fetch; use cache-busted verification plus live browser verification.
  9. Final homepage QA should include HTTP 200 for normal and cache-busted URLs, marker present, schema present, one visible H1, internal-link scan with zero bad links, image load checks, browser layout metrics for desktop/tablet/mobile, zero horizontal overflow, no visible third-party widgets covering the hero, and real screenshot/vision QA.
- Bulk article ZIP deployment lesson from PlantasticHaven:
  1. Treat the ZIP manifest as authoritative for exact target URLs, body HTML files, and schema files, but verify each exact URL publicly before and after deployment. If a manifest URL is a live 404, create/update a real post/page at that exact slug instead of silently updating a near-match canonical article only.
  2. Some packages include both a desired exact URL and an existing canonical/related page. When appropriate, update both: the exact requested URL for user QA and the canonical related page for internal links and site continuity.
  3. When REST credentials are stored in grouped secret blocks, a site-specific application password may pair with a shared admin username from another block. If the obvious site-block username/password fails with `rest_not_logged_in`, test candidate username/app-password pairs against `/wp-json/wp/v2/users/me?context=edit` before declaring auth blocked. Never print the secrets.
  4. Add article-scoped fit CSS before publishing rich body HTML wrappers such as `.ph-sota`: constrain the wrapper to the theme column, set `box-sizing:border-box`, constrain media, and add mobile table rules. Fixed-width tables can pass desktop QA yet overflow on 360px mobile; a second pass may need `table-layout:fixed`, `min-width:0`, and `overflow-wrap:anywhere` on `table/thead/tbody/tr/th/td`.
  5. WordPress theme titles can create duplicate visible H1s above a custom article that already has its own H1. If browser QA shows two visible H1s, hide the theme `.entry-title` page-scoped/content-scoped in the custom CSS rather than removing the article H1.
  6. Final QA should include both cache-busted and normal no-query URLs, a public internal-link/media-target scan, and browser layout checks across desktop/tablet/mobile. Save artifacts such as `/tmp/<site>_http_qa_final.json` and `/tmp/<site>_layout_verify_final.json` before claiming completion.