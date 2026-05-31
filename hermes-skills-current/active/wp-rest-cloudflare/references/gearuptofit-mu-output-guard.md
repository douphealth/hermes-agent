# GearUpToFit MU Output Guard Pattern

Use this when GearUpToFit public pages are visually broken by generated Elementor/theme output but database/source edits are risky or inaccessible. This is an output-layer guard, not a content rewrite.

## When to use

- Plaintext CSS leaks after `</style>` and appears at the top of posts.
- Public HTML contains `origin.gearuptofit.com` links even though WP `home`/`siteurl` are correct.
- Imported/self-contained review posts include their own complete layout (`<main class="gutf-review-page">`) but Elementor also prints duplicated title/meta/featured-image/TOC above them.
- `/blog/` or another public hub route resolves to the wrong Elementor archive/category template, shows a mismatched hero (e.g. “RUNNING HUB”), and then prints “It seems we can't find what you're looking for.”
- Theme Editor refuses PHP changes with a loopback/fatal-check rollback behind Cloudflare.

## Safer deployment route

1. Login through Puppeteer with origin mapping:
   - `--ignore-certificate-errors`
   - `--host-resolver-rules=MAP gearuptofit.com 104.168.100.41`
2. Open `https://gearuptofit.com/wp-admin/admin.php?page=wp_file_manager`.
3. Wait for `window.fmfparams.nonce` and `window.fmfparams.ajaxurl`.
4. Use elFinder AJAX connector:
   - `action=mk_file_folder_manager`
   - `_wpnonce=<fmfparams.nonce>`
   - `cmd=mkdir|mkfile|put|get`
5. Write the guard as a must-use plugin:
   - `wp-content/mu-plugins/gutf-leak-guard.php`

Known elFinder hashes on GearUpToFit:
- public_html/root: `l1_Lw`
- `wp-content`: `l1_d3AtY29udGVudA`
- `wp-content/mu-plugins`: `l1_d3AtY29udGVudC9tdS1wbHVnaW5z`
- `wp-content/mu-plugins/gutf-leak-guard.php`: `l1_d3AtY29udGVudC9tdS1wbHVnaW5zL2d1dGYtbGVhay1ndWFyZC5waHA`

## Guard behavior that worked

Inside a non-admin output buffer:

1. Normalize origin hostname everywhere in public output:
   - Replace bare `origin.gearuptofit.com` with `gearuptofit.com`.
   - This catches normal anchors, URL-encoded oEmbed URLs, and JS-escaped Elementor REST URLs.
   - Do not only replace `https://origin...`; encoded strings will remain.

2. Remove only the duplicated CSS leak:
   - Preserve the valid real `<style>` block.
   - Handle BOTH variants observed in production:
     - text node immediately after `</style>` beginning with `.gutf-article`
     - stale/generated body text node immediately after `<body...>` beginning with `.gutf-article` before the header/banner
   - Use broad-enough matching around the GUTF block (`.gutf-article` through the final `@media (max-width:480px)` block), not one exact selector order; Huawei had a different selector order than Speedgoat/Nike.
   - Verify no `</style>\s*\.gutf-article` remains and the visible body start does not contain `.gutf-article`.

3. For self-contained imported review pages only:
   - If output contains `class="gutf-review-page"` or `class='gutf-review-page'`, inject a scoped CSS guard hiding duplicate Elementor chrome:
     - `.elementor-widget-theme-post-title`
     - `.elementor-widget-post-info`
     - `.elementor-widget-theme-post-featured-image`
     - `.elementor-widget-table-of-contents`
     - `.sota-root`
   - Scope to `body.single-post` and only inject when the self-contained review wrapper exists.
   - This prevents destroying normal post templates.

4. For `/blog/` archive-template breakage:
   - Symptom: `/blog/` shows a mismatched hub/category hero (e.g. “RUNNING HUB”) plus “It seems we can't find what you're looking for,” instead of a blog index.
   - Cause observed: Elementor archive template applied to the route/category context; fixing individual posts will not help.
   - Safe recovery: in MU plugin `template_redirect`, check exact path `trim(parse_url($_SERVER['REQUEST_URI'], PHP_URL_PATH), '/') === 'blog'`, then render a latest-posts index with `get_header()`, `WP_Query(['post_type'=>'post','post_status'=>'publish','posts_per_page'=>18])`, responsive card CSS, `get_footer()`, and `exit`.
   - Keep this override exact-path only; do not hijack all archives/categories. It is a surgical recovery for a broken public route.

## Verification checklist

Fetch full files, not capped terminal output.

For affected URLs:
- `https://gearuptofit.com/blog/`
- `https://gearuptofit.com/free-fitness-plan/`
- `https://gearuptofit.com/review/huawei-watch-gt-runner-2/`
- `https://gearuptofit.com/review/huawei-watch-gt-runner-2/?noncache` (verify the exact query URL, not only a unique cachebuster)
- `https://gearuptofit.com/review/nike-pegasus-trail-5/`
- `https://gearuptofit.com/running/hoka-speedgoat-7/`

Check:
- `origin_refs == 0`
- logo anchor points to `https://gearuptofit.com/`
- no `Fatal error|Parse error|syntax error`
- no `</style>\s*\.gutf-article`
- no generic `</style>\s*\.[a-zA-Z0-9_-]+\s*\{`
- self-contained review pages include the guard CSS
- `/blog/` contains the blog override wrapper (`gutf-blog-index`), has post cards, does not contain the not-found message, and no longer shows the mismatched archive hero as page chrome

Browser checks:
- Desktop and mobile `document.documentElement.scrollWidth <= clientWidth + 2`.
- Logo `href` is `https://gearuptofit.com/`.
- Duplicate Elementor widgets have computed `display: none` on self-contained review pages.
- Real article begins with its own review content, e.g. `GEARUPTOFIT REVIEW`, not the duplicated Elementor title/TOC.

## Cloudflare cache pitfall

A fix can be live on `?nocache=...` while normal URLs still show stale `cf-cache-status: HIT`. Use the Cloudflare token from local secrets and purge.

Correct API shape:

```bash
curl -sS -X POST "https://api.cloudflare.com/client/v4/zones/$ZONE_ID/purge_cache" \
  -H "Authorization=[REDACTED] $CLOUDFLARE_API_TOKEN" \
  -H "Content-Type: application/json" \
  --data '{"files":["https://gearuptofit.com/free-fitness-plan/"]}'
```

If exact-file purge succeeds but stale HIT remains, perform:

```json
{"purge_everything": true}
```

Then recheck normal URLs, not only cache-busted URLs.

Also verify the exact complaint URL/query string. Browser automation can keep an old in-memory/cache copy of `?noncache`; launch a clean headless profile with cache disabled (`page.setCacheEnabled(false)` and `--disable-cache`) and inspect `document.body.innerText.slice(0, 2500)` for `.gutf-article`. A fresh `?noncache=unique` pass is not enough if the user reported the exact bare `?noncache` URL.

## Workflow pitfall from user correction

Do not fix one URL and declare the class solved. When the user reports “many problematic URLs,” immediately switch to global-source debugging plus a sweep of representative routes. Always verify the exact URL/query string the user pasted, then sweep at least: a hub/archive route (`/blog/`), a page (`/free-fitness-plan/`), a normal review post, a self-contained review post, and the originally broken post.

## Safety notes

- Do not print credential/token values.
- Do not edit individual posts for a global output issue.
- Prefer MU plugin over theme file edits for recovery guards; it survives theme changes and avoids Theme Editor rollback.
- Keep the guard narrow: preserve real CSS and suppress duplicate chrome only when a self-contained review wrapper is present.
