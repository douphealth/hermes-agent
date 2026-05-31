---
name: wp-rest-cloudflare
description: Patterns for working with WordPress REST API when Cloudflare blocks wp-admin. Covers authentication, content updates with WAF bypass, XML-RPC fallback, Elementor CSS issues, and preventing WordPress auto-wrapping of HTML.
category: devops
tags: [wordpress, rest-api, cloudflare, curl, content-edit, xmlrpc, elementor]
---

# WordPress REST API + Cloudflare Working Patterns

> **Emergency WSOD reference:** `references/cyberpanel-wsod-mu-plugin-recovery.md` — when WordPress shows a critical error and wp-admin/REST are down, but CyberPanel is reachable, use File Manager plus one-shot cron to disable/fix MU-plugin fatals, clean public debug logs, remove temporary crons, and verify with live HTTP/REST evidence.

---

> **Related skill:** `wordpress-performance-optimization` — for PhastPress tuning, SOTA blog post meta injection, Cloudflare caching page rules, and Elementor-compatible performance hacks. This REST skill covers auth + content editing; the performance skill covers speed optimization.
>
> **Reference:** `references/wp-crash-recovery-code-snippets.md` — Crash recovery ladder for Code Snippets / WP 500s, including the `wp_die('DONE')` active-snippet pattern, REST deactivation path, WP File Manager fallback, debug-log cleanup, and Cloudflare/LiteSpeed verification.
>
> **Reference:** `references/mainwp-localwp-connection-repair.md` — MainWP Dashboard running in LocalWP on Windows: discover LocalWP MySQL/PHP paths from WSL, repair child-site sync errors caused by stale `adminname`, fix `openssl_pkey_export(): Cannot get key from parameter 1` warnings from stale OpenSSL config, switch to PHPSECLIB fallback, and verify with `MainWP_Sync::sync_site()` plus PowerShell localhost probes.
>
> **Reference:** `references/elementor-kit-css-leak.md` — Detection and fix for Elementor CSS text leaking outside `<style>` tags, showing as visible CSS at the top of blog posts. Covers the `_elementor_global_css` option, Elementor Kit post meta, and CSS Print Method issues.
>
> **Reference:** `references/gearuptofit-mu-output-guard.md` — GearUpToFit MU-plugin output guard pattern: fix Elementor CSS leak, normalize `origin.gearuptofit.com` links, hide duplicated Elementor chrome on self-contained imported review pages, recover broken `/blog/` archive output, verify desktop/mobile, and purge Cloudflare.
>
> **Template:** `templates/gutf-leak-guard.php` — known-good MU-plugin output guard skeleton for GearUpToFit CSS leak/origin-host/self-contained-review and broken `/blog/` archive regressions. Copy through WP File Manager elFinder and adjust narrowly.
>
> **Reference:** `references/editing-custom-pages-via-rest.md` — Editing full HTML pages (classic homepage templates) via `wp/v2/pages` with `<!-- wp:html -->` blocks.
>
> **Cross-skill reference:** `authority-engine/references/wordpress-cloudflare-canonical-control.md` — When WordPress sits behind Cloudflare Workers/React/Lovable, use origin-only `noindex` plus apex/domain edge overrides; verify both HTML robots meta and `X-Robots-Tag` so backend protection does not accidentally noindex public ranking pages.
>
> **Reference:** `references/cloudflare-worker-app-proxy-seo.md` — Edge pattern for serving a React/Vite/Lovable app at a canonical WordPress path before WP fallback, adding crawlable SEO shell/schema, rewriting `/assets/` under a subpath, handling BrowserRouter basename, keeping the old app subdomain noindex/canonical until loop risk is gone, and validating with curl/browser tests.
>
> **Reference:** `references/wp-admin-cloudflare-worker-recovery.md` — Recovery pattern when Cloudflare firewall rules or an apex Worker break wp-admin plugin activation/deactivation and post editing: remove admin/login challenges, keep cache bypass, set apex Host for admin upstream requests, rewrite origin hosts in redirects, skip public SEO transforms for admin HTML, and verify with real admin pages.
>
> **Reference:** `references/gearuptofit-worker-index-consolidation.md` — GearUpToFit Cloudflare Worker-level exact redirect + sitemap-filter pattern for duplicate indexable pages/hubs: backup multipart Worker source, patch `REDIRECTS_301`, upload module Worker with `main_module`, exact Cloudflare purge, one-hop chain verification, and XML sitemap parse verification.
>
> **Reference:** `references/gearuptofit-runmatch-canonicalization-2026-05.md` — Session-specific GearUpToFit RunMatch cleanup notes: direct Pages upstream, safe legacy subdomain 301 timing, sitemap Worker delegation, app sitemap inclusion, origin-host noindex caution, and verification snippets.
>
> **Reference:** `references/gearuptofit-canonical-subdomain-category-cleanup.md` — GearUpToFit class pattern for origin-host 301s without breaking apex Worker upstream, category hub copy guards, widget clutter removal, root `/llms.txt`, staging subdomain redirects, low-value archive noindex, and verification bundle.
>
> **Reference:** `references/gearuptofit-lead-capture-audit.md` — GearUpToFit lead-capture audit pattern: public curl/browser checks, Elementor form/backend parsing, CRM/email plugin detection, and interpretation rules for contact vs real newsletter/marketing capture.
>
> **Reference:** `references/wp-post-image-placeholder-repair.md` — WordPress article image repair workflow: find placeholder URLs, reuse site media, patch raw post HTML via XML-RPC/origin-IP bypass when Cloudflare blocks XML-RPC, purge cache, and verify lazy-loaded images by scrolling and checking natural dimensions.
>
> **Reference:** `references/amazon-affiliate-box-live-audit-qa.md` — Amazon affiliate product-box QA for WordPress posts: validate direct ASIN links, Amazon CDN images, affiliate tag/rel attributes, rendered mobile/desktop image dimensions, duplicate module counts, product relevance, and XML-RPC timeout/slug-creation pitfalls during batch rewrites.
>
> **Reference:** `references/mainwp-local-dashboard-repair.md` — MainWP local dashboard repair workflow for child sites that appear disconnected: public probes, child admin-user verification, LocalWP MySQL/PHP access, fixing stale `adminname` values, clearing `wp_mainwp_wp_sync.sync_errors`, and triggering `MainWP_Sync::sync_site()` from the local dashboard code.
>
> **Reference:** `references/cloudflare-scoped-worker-redirect.md` — Narrow Cloudflare Worker-route pattern for exact legacy 301 redirects when Redirect Rules/Rulesets API is unavailable but Workers API and route creation are permitted. Covers backup, exact-path guard, query preservation, one-hop verification, and rollback.
>
> **Reference:** `references/wp-affiliate-measurement-system.md` — Enterprise affiliate monetization rollout pattern: central offer registry, tracked CTA metadata, GA4/GTM-compatible `affiliate_click` events, KPI dashboard columns/formulas, daily link-health monitor, conversion-module structure, and verification contract.
>
> **Reference:** `references/wp-affiliate-revenue-recovery.md` — Revenue-critical affiliate recovery after a tracking rollout: logged-out raw+DOM verification for all monetized URLs, fake/future claim cleanup, safe affiliate sub-ID support matrix, GA4 key-event/custom-dimension honesty, homepage money-route placement, and final KPI baseline reporting.
>
> **Reference:** `references/amfs-homepage-mobile-rescue-cache.md` — AffiliateMarketingForSuccess homepage mobile-rescue pattern: XML-RPC stored-content marker verification, Cloudflare + Seraphinite Accelerator cache clearing, CookieYes mobile width fixes, off-canvas drawer rescue, and the rule that XML-RPC success is not proof the public homepage is serving the fix.
>
> **Reference:** `references/wp-mu-plugin-content-filter-safety.md` — Safety rules for MU-plugin `the_content` filters: never return raw `preg_replace*()` on large homepage/custom HTML content, skip front-page landing templates unless explicitly repairing them, fallback to original content on regex failure, and verify visible words/hero text after deploy.
>
> **Reference:** `references/wp-mu-plugin-fatal-recovery.md` — MU-plugin deployment safety and emergency recovery: lint the exact PHP before upload, confirm hosting/SSH/FTP rollback access before writing production MU plugins, and remember that a fatal MU plugin can also break wp-admin/admin-ajax/WP File Manager rollback because MU plugins load first.
>
> **Reference:** `references/gearuptofit-batch-content-residue-cleanup.md` — Fast batch cleanup workflow for GearUpToFit WordPress URLs with visible broken shortcodes, template placeholders, visible JSON-LD, origin-host residue, canonical slug mismatches, and stale SEO titles; includes script strategy and compact verification contract.
>
> **Reference:** `references/wp-visible-schema-leak-cleanup.md` — WordPress visible JSON-LD/schema leakage cleanup pattern: strip real scripts before detection, use bounded block removal instead of broad regex, preserve newly added modules, restore from raw backup if cleanup is over-broad, then purge and browser-verify.
>
> **Reference:** `references/gearuptofit-surgical-seo-publishing.md` — GearUpToFit production pattern for Surgical Semantic SEO post edits: intelligence brief first, REST raw read, backup, XML-RPC origin-IP publish with Yoast custom fields, Cloudflare exact purge, and cache-busted + browser visual verification.
>
> **Reference:** `references/gearuptofit-duplicate-post-consolidation.md` — Fast duplicate/same-intent WordPress post consolidation pattern for GearUpToFit: REST discovery, canonical keeper choice, edge 301 redirects, sitemap/GSC checks, and no-delete/no-layout-risk management.
>
> **Reference:** `references/gearuptofit-topical-architecture-cannibalization.md` — GearUpToFit topical-architecture consolidation pattern: choose one canonical owner per intent, keep `/review/` for commercial shoe roundups and `/running/` for education, exact Worker 301 duplicates, clean internal links, verify category hub copy publicly, update `TOPICAL_MAP.md`/`CONTENT_INVENTORY.md`, resubmit sitemaps, and report compact evidence.
>
> **Reference:** `references/gearuptofit-visual-layout-verification.md` — Required rendered mobile/desktop verification pattern for imported GearUpToFit review pages. Covers DOM overflow probes, skinny-column detection, `.sota-root`/Elementor wrapper blowouts, fixed-width tables, URL-scoped edge CSS injection, stacked mobile table cards, and the rule that string cleanup is not visual cleanup. Includes script `scripts/gutf-rendered-responsive-probe.js` for repeatable Puppeteer-based mobile/desktop QA.
>
> **Reference:** `references/gearuptofit-batch-review-rewrite-publishing-qa.md` — Batch review rewrite publish/QA workflow for GearUpToFit: local product-image uploads, Amazon CTA normalization, body schema removal, exact/purge-everything cache escalation, mobile table/card CSS hardfix, and final raw/rendered/screenshot artifacts.
>
> **Reference:** `references/wp-imported-rewrite-layout-recovery.md` — Emergency recovery pattern when a rewritten/imported WordPress post is visually distorted after publish: rebuild from the clean source instead of contaminated rendered HTML, strip old TOC/review/template fragments, reinsert only verified monetization modules, add scoped layout hardfix CSS, purge cache, and verify H1/overflow/rendered readability.
>
> **Reference:** `references/wp-full-post-rewrite-publishing-pipeline.md` — First-post quality-gate workflow for replacing existing WordPress posts with rich rewritten HTML: XML-RPC preservation, backups, duplicate-H1 prevention, Yoast/RankMath/social metadata updates, cache-busted public verification, media/schema checks, and terse proceed/no-proceed reporting. Includes the rule to strip publisher-only brief sections such as `Recommended internal links` and remove imported/body H1s before batch publishing.
>
> **Reference:** `references/wp-multi-post-rewrite-source-file-publishing.md` — Multi-post source-file publishing pattern learned from batch rewrite deployments: parse target URL/slug/title/meta/raw HTML, backup, XML-RPC origin publish, remove visible JSON-LD/publisher artifacts, handle theme-specific H1 suppression/demotion, purge Cloudflare, and verify every public URL.
>
> **Reference:** `references/wp-batch-rewrite-rendered-qa-hardening.md` — Enterprise batch rewrite hardening: XML-RPC publish, Amazon/product image normalization, exact/public cache verification, theme-dependent H1 fallback, rendered 320/390/desktop QA, skinny mobile-table detection, lazy-loaded image probes, and screenshot evidence contract.
>
> **Reference:** `references/micegoneguide-batch-rewrite-consolidation.md` — Batch WordPress rewrite/consolidation pattern for source files containing multiple rewritten posts plus legacy intents: map canonical targets before publishing, use XML-RPC for rich HTML, avoid duplicate H1s, add exact one-hop MU/Worker redirects, clear Cloudflare + Seraphinite cache, and verify canonical pages plus redirect chains.
>
> **Reference:** `references/mysticaldigits-batch-rewrite-repair.md` — Emergency repair pattern for multi-post rewrite imports where public pages show repeated TOC/Amazon modules or apparently pasted-all-posts contamination: rebuild each post from bounded START/END source sections, repair by explicit post ID, verify stored body separately from public render, catch redirect/canonical traps, and clear LiteSpeed/Cloudflare before visual QA.
>
> **Reference:** `references/wp-xmlrpc-media-insertion-pitfalls.md` — WordPress XML-RPC media insertion pitfalls: verify stored body markers after `editPost`, prefer minimal edit payloads for surgical image blocks, embed returned upload URLs because PNG/JPEG may become WebP, fall back from blocked SVG uploads to raster diagrams, and verify lazy-loaded render dimensions.
>
> **Reference:** `references/amfs-authority-links-inline-svg-upgrade.md` — AMFS post-quality upgrade pattern for adding contextual internal authority-link modules and accessible inline SVG process diagrams after a full SEO rewrite, with live-link and rendered-layout QA.
>
> **Script:** `scripts/wp-full-post-rewrite-verify.py` — Reusable public-URL verifier for full-post rewrite batches. Checks single-H1, no imported/body H1, no `Recommended internal links`, no raw CSS/schema leaks, title/meta/canonical/schema/CTA presence, and representative media assets.
>
> **Reference:** `references/wp-plugin-install-without-file-access.md` — Plugin install/upgrade workarounds when wp-admin/SSH/file access is unavailable, including REST media + Code Snippets installers, cookie-auth fallback activation, and MainWP LocalWP bulk ZIP install failures where child sites cannot fetch `localhost` signed `mwpdl` URLs; covers public tunnel/base-URL override, separate static ZIP tunnel for endless 0% AJAX deadlocks, frontend timeout handling, and the MainWP 2MB server-side upload cap mismatch.
>
> **Reference:** `references/single-slug-worker-redirect-fallback.md` — One-URL Cloudflare Worker redirect fallback when Redirect Rules/Rulesets are unauthorized but Worker routes are available: backup routes, create a tiny exact-path guarded Worker, attach only old-slug route patterns, preserve query strings, verify one-hop 301 to a 200 target, and roll back by detaching routes.

---

## 1. Authentication Methods

### 1.1 Application Passwords (REST API only)
- Created in wp-admin → Users → Manage API Keys
- Format: `username:XXXX XXXX XXXX XXXX XXXX XXXX`
- Usage: `curl -u "admin:XXXX XXXX XXXX XXXX XXXX XXXX" ...`
- **REST API READ works**: posts, pages, users (basic)
- **REST API WRITE returns `rest_forbidden`** — application passwords on gearuptofit.com only have read scope
- Does NOT work with XML-RPC (returns "incorrect username or password")

### 1.2 Admin Password (XML-RPC)
- Works with XML-RPC for READ + WRITE
- Usage in curl: `password goes in XML body as <string>` (no special escaping needed)
- Works for: `metaWeblog.getPost`, `metaWeblog.editPost`, `wp.getPosts`, `wp.getOptions`
- Does NOT work with REST API `wp/v2/settings` (returns `rest_forbidden`)

### 1.3 Cookie-Based Login (via origin IP)
- Two-step process to bypass WordPress cookie check:
  ```
  # Step 1: GET login page to receive test cookie
  curl -sk -c cookies.txt -b cookies.txt \
    -H "Host: gearuptofit.com" \
    "https://104.168.100.41/wp-login.php" > /dev/null

  # Step 2: POST credentials with testcookie=1
  curl -sk -c cookies.txt -b cookies.txt -L \
    -H "Host: gearuptofit.com" \
    --data-urlencode "log=admin" \
    --data-urlencode "pwd=[REDACTED] \
    --data-urlencode "wp-submit=Log In" \
    --data-urlencode "redirect_to=/wp-admin/" \
    --data-urlencode "testcookie=1" \
    "https://104.168.100.41/wp-login.php"
  ```
- **Critical:** Use `-c` (cookie jar) AND `-b` (cookie file) on BOTH steps
- SSL cert error on origin IP (`ERR_CERT_COMMON_NAME_INVALID`): use `-k` flag
- Cloudflare may serve a challenge page through the domain — use origin IP with `Host` header instead

---

## 2. Content Editing Patterns

### 2.0 Article Rewrite Quality Gate

Before publishing SEO/NeuronWriter-driven WordPress rewrites, fail closed on reader-hostile artifacts:

- No body `<h1>` and no oversized body H2 that repeats the theme-rendered H1.
- No keyword-padding blocks such as `use this as an audit label...` or `include this concept in your operating checklist...`.
- Internal links must appear contextually inside natural article paragraphs/bullets; a bottom related-resources grid is supplemental only.
- For screenshot complaints, search the stored post body for exact visible text, remove the full parent block, replace with useful prose/checklists/examples, then verify raw HTML and browser `document.body.innerText`.
- After publish, verify stored body, raw public HTML, and rendered browser DOM before claiming done. Use `references/wp-article-quality-rescue.md` for the rescue checklist.

### 2.1 REST API — Direct Post Update
```
curl -X POST -u "admin:APP_PASSWORD" \
  -H "Content-Type: application/json" \
  -d '{"content":{"raw":"<div>HTML content</div>"}}' \
  "http://104.168.100.41/wp-json/wp/v2/posts/POST_ID"
```
- Content field must be `{"raw":"<html>"}` (object with raw key), NOT a plain string
- Pass `?context=edit` to read raw content without rendering
- **STRIPS `<style>` tags and `@media` queries** via content sanitizer — USE XML-RPC INSTEAD

### 2.2 XML-RPC — Full HTML Preserved (PREFERRED for CSS/style injection)
- `metaWeblog.editPost` preserves `<style>` tags, `@media` queries, and all HTML
- CDATA wrapping recommended for large content:
  ```xml
  <?xml version="1.0"?>
  <methodCall>
    <methodName>metaWeblog.editPost</methodName>
    <params>
      <param><value><string>POST_ID</string></value></param>
      <param><value><string>admin</string></value></param>
      <param><value><string>ADMIN_PASSWORD</string></value></param>
      <param><value><struct>
        <member>
          <name>description</name>
          <value><string><![CDATA[FULL_HTML_CONTENT]]></string></value>
        </member>
      </struct></value></param>
      <param><value><boolean>1</boolean></value></param>
    </params>
  </methodCall>
  ```
- Send with: `curl -s -H "Host: gearuptofit.com" -H "Content-Type: text/xml" -d @file.xml "http://104.168.100.41/xmlrpc.php"`
- If a high-level XML-RPC client returns origin `404` despite `curl -I`/POST showing `/xmlrpc.php` exists, do not conclude XML-RPC is unavailable. Build and POST the raw XML request yourself with explicit `Host: gearuptofit.com`, `Content-Type: text/xml`, and CDATA. In Python, `urllib.request.Request('https://104.168.100.41/xmlrpc.php', data=body, headers={'Host':'gearuptofit.com','Content-Type':'text/xml'}, method='POST')` with an unverified SSL context works for origin-IP XML-RPC while preserving public-domain WordPress context.
- Returns `<boolean>1</boolean>` on success

### 2.3 Available XML-RPC Methods (gearuptofit.com)
- `metaWeblog.getPost` / `metaWeblog.editPost` / `metaWeblog.newPost`
- `wp.getPosts` / `wp.getPost` (for standard post types only)
- `wp.getOptions` / `wp.setOptions` (core options only, not plugin options)
- `wp.editPost` / `wp.getRevisions`
- **NOT available for plugin options or Elementor CPTs** (`elementor_css`, `elementor_library` return "Invalid post type" or "Incorrect username or password")

---

## 3. Elementor-Specific Issues

### 3.1 Elementor CSS Leak Pattern
When Elementor has global custom CSS and `css_print_method` is `external` but CSS files don't exist (404), Elementor falls back to inline CSS. **BUT it can output the same CSS TWICE:**
- Once minified inside `<style>` tags (correct)
- Once pretty-printed OUTSIDE `</style>` as visible text (the leak)

The leak shows as plaintext CSS code at the top of blog posts. It affects ALL pages because it's a global setting.

**Detection:**
- Search for `</style>\n.` in the page HTML (CSS text between `</style>` and next `<style>`)
- The leak is typically ~2500 chars of pretty-printed CSS with `!important` rules
- The `<style>` block with no `id` attribute right after the Elementor meta tag is the source

**Fix (requires wp-admin access):**
1. Elementor → Tools → Regenerate CSS
2. Elementor → Custom CSS section — delete any `.gutf-article` / `.product-box-*` rules
3. Or Appearance → Customize → Additional CSS if it was pasted there

### 3.2 Elementor Global CSS Storage
- Stored in database as `elementor_global_css` option in `wp_options` table
- Or as a custom post type `elementor_css` (not accessible via XML-RPC)
- CSS files expected at: `wp-content/uploads/elementor/css/global.css` (often missing/404)
- When files missing and `css_print_method=external`, Elementor inlines everything

### 3.3 Elementor REST API Endpoints
- `wp-json/elementor/v1/globals` — returns `rest_forbidden` without proper nonce auth
- `wp-json/elementor/v1/global-settings` — returns `rest_no_route` (not exposed via REST)
- Cannot be accessed with application passwords — requires wp-admin session

---

## 4. Cloudflare Interaction Patterns

### 4.0 wp-admin/plugin/editor recovery behind Cloudflare Workers

When the user reports they cannot activate/deactivate plugins or edit posts, first reproduce the admin HTTP path before touching plugins. A Cloudflare challenge on `/wp-admin/*` or `/wp-login.php` presents as `HTTP 403`, `cf-mitigated: challenge`, and a `Just a moment...` body. Remove/relax the admin/login challenge rule while keeping unrelated XML-RPC/bot protections intact, confirm `/wp-admin*` bypasses cache, and then inspect the apex Worker.

If the Worker proxies apex WordPress requests to an origin hostname, admin/login requests may still fail because WordPress generates cookies, redirects, form actions, and editor URLs using the origin host. For wp-admin/wp-login requests, classify admin paths before generic `?s` public-search routing (plugin activation links often include `&s`), set upstream `Host` to the public apex, keep `x-forwarded-host: apex` and `x-forwarded-proto: https`, rewrite origin hosts in redirect `Location` headers including URL-encoded `redirect_to=...`, and skip public SEO/canonical transformations for admin HTML. See `references/wp-admin-cloudflare-worker-recovery.md` for the exact patch/verification pattern.

### 4.1 Origin IP Access

> **Reference:** `references/cloudflare-pages-dns-portfolio-inventory.md` — Portfolio inventory workflow for Cloudflare Pages + DNS: verify token/account split, handle Pages pagination quirks, pull Pages project/repo/custom-domain/deployment fields, pull DNS zones/records, and merge into a multi-sheet repo/app/domain workbook. Key pitfall: a token can have correct Zone permissions but return zero zones if it belongs to the Pages account while DNS lives under another Cloudflare account/email.
>
> **Reference:** `references/lovable-portfolio-enrichment-without-oauth.md` — Public-first Lovable enrichment pattern for app portfolio workbooks: probe known `lovable.dev/projects/<uuid>` and `*.lovable.app` URLs, extract DNS `_lovable` verification clues, merge evidence into the workbook, then ask only for the exact private dashboard fields/access method still needed.

- Origin IP: `104.168.100.41` (port 443 for HTTPS, 8090 for hosting panel)
- Always send `-H "Host: gearuptofit.com"` header
- SSL cert doesn't match origin IP — use `-k` flag with curl
- Cloudflare does NOT cache wp-admin pages (no `cf-cache-status` header)
- But Cloudflare DOES return 403 for `wp-admin/plugins.php` through CF

### 4.2 Cloudflare Cache Behavior
- `cf-cache-status: HIT` means Cloudflare edge is serving cached content
- `age: NNN` shows seconds since cache was stored
- Purge via: Cloudflare Dashboard → Caching → Purge Everything
- Query params like `?nocache=1` bypass Cloudflare edge cache
- Cloudflare API token format: `cfut_XXXX...XXXX`; retrieve from the local secrets file only when needed and never print it
- For Cloudflare Pages/DNS inventory across app portfolios, see `references/cloudflare-pages-dns-cross-account-inventory.md`. Important pitfall: Pages projects and DNS zones can live under different Cloudflare accounts/emails; a valid Pages token with correct permissions can list Pages but return zero zones because the zones are in another account.
- Use `POST` + `--data` for API purge, not stdin without `--data`:
  ```bash
  curl -sS -X POST "https://api.cloudflare.com/client/v4/zones/$ZONE_ID/purge_cache" \
    -H "Authorization=[REDACTED] $CLOUDFLARE_API_TOKEN" \
    -H "Content-Type: application/json" \
    --data '{"files":["https://gearuptofit.com/path/"]}'
  ```
- If exact-file purge succeeds but the normal URL still returns stale `cf-cache-status: HIT`, the cache key likely differs; use `{"purge_everything":true}` and recheck normal URLs after a few seconds
- Some sites use Seraphinite Accelerator rather than PhastPress/LiteSpeed. In wp-admin, the menu appears as **Accelerator → Manager** and its JS calls `admin-ajax.php?action=seraph_accel_api&fn=CacheOpBegin`. For an exact URL purge, log in via origin IP + Host header, load `admin.php?page=seraph_accel_manage`, extract the nonce from `OnCacheOp(this,2,"NONCE")`, then GET `/wp-admin/admin-ajax.php?action=seraph_accel_api&fn=CacheOpBegin&type=uri&op=2&uri=/path/&v=&_wpnonce=NONCE`. A `0` response can still mean the operation was accepted; verify by comparing canonical vs cache-busted public HTML and Cloudflare status.

### 4.3 Browser Access Through Cloudflare
- Cloudflare JS challenge page ("Just a moment...") may block browser automation
- Checkbox challenges can be clicked via browser tools but may not resolve
- Origin IP `https://104.168.100.41` has SSL cert issues for browser access too
- Hosting panel at `104.168.100.41:8090` with SSL redirect

---

### 4.5 Browser Automation via Origin IP (Puppeteer/Playwright)

When Cloudflare's JS challenge blocks the domain, use Puppeteer with `--host-resolver-rules` to resolve the domain to the origin IP while keeping the correct TLS hostname:

```js
const puppeteer = require('puppeteer-core');
const browser = await puppeteer.launch({
  executablePath: '/path/to/chrome',
  headless: true,
  args: [
    '--ignore-certificate-errors',
    '--no-sandbox',
    '--disable-setuid-sandbox',
    '--host-resolver-rules=MAP gearuptofit.com 104.168.100.41, MAP origin.gearuptofit.com 104.168.100.41'
  ]
});
const page = await browser.newPage();
await page.goto('https://gearuptofit.com/wp-login.php', { waitUntil: 'networkidle0', timeout: 30000 });
```

**Key details:**
- `--ignore-certificate-errors` — required because origin IP cert doesn't match
- `--host-resolver-rules=MAP gearuptofit.com IP` — forces DNS resolution to origin IP
- Browser uses the proper HTTPS connection with correct SNI/domain
- After login, navigate to ANY wp-admin URL using the domain name
- Login form handling: `page.type('#user_login', 'admin')`, `page.type('#user_pass', 'pwd')`, `page.click('#wp-submit')`, `page.waitForNavigation()`
- Available for wp-admin: Theme Editor, Elementor Tools, Options page, Plugin manager, WP File Manager
- WP File Manager exposes an elFinder AJAX connector when logged in:
  - open `wp-admin/admin.php?page=wp_file_manager`
  - wait for `window.fmfparams.nonce` and `window.fmfparams.ajaxurl`
  - POST to `ajaxurl` with `action=mk_file_folder_manager`, `_wpnonce`, and elFinder commands like `mkdir`, `mkfile`, `put`, `get`
  - use this for direct file writes when Theme Editor rolls back PHP because the Cloudflare/origin setup breaks WordPress loopback fatal checks

**Pitfalls:**
- Puppeteer `request.continue()` cannot override `Host` header (browser security)
- `has-text()` pseudo-selector not available in Puppeteer's `page.$()` — use `page.evaluate()` and `querySelectorAll` instead
- `page.waitForTimeout()` doesn't exist in puppeteer-core — use `new Promise(r => setTimeout(r, N))`
- Theme Editor can inject PHP code temporarily (MUST restore afterward)
- Elementor Kit editor is an SPA — gear icon, then tab navigation, then CodeMirror for custom CSS

## 5. References

> **Reference:** `references/elementor-kit-css-leak.md` — Detection and fix for Elementor CSS text leaking outside `<style>` tags, showing as visible CSS at the top of blog posts. Covers the `_elementor_global_css` option, Elementor Kit post meta, and CSS Print Method issues.

> **Reference:** `references/gearuptofit-mu-output-guard.md` — GearUpToFit MU-plugin output guard pattern: fix Elementor CSS leak, normalize `origin.gearuptofit.com` links, hide duplicated Elementor chrome on self-contained imported review pages, recover broken `/blog/` archive output, verify desktop/mobile, and purge Cloudflare.

> **Reference:** `references/wp-article-quality-rescue.md` — Emergency cleanup workflow for WordPress article rewrites that publish duplicate title blocks, NeuronWriter/SEO keyword-stuffing artifacts, non-contextual internal-link modules, or ugly screenshot-visible sections. Includes hard-fail phrases, replacement-section patterns, and raw HTML + browser DOM verification probes.

> **Reference:** `references/cloudflare-worker-app-proxy-seo.md` — Canonical app-path proxy pattern for React/Vite/Lovable apps on WordPress sites behind Cloudflare Workers, including route-before-WP fallback, SEO shell/schema injection, subpath asset rewrites, BrowserRouter basename fixes, safe old-subdomain noindex/canonical handling, sitemap inclusion, validation, and rollback.

---

## Pitfalls

- **Cloudflare Worker module uploads:** If a Worker source contains `export default` and Cloudflare upload validation returns `10021 Unexpected token 'export'`, stop and use module-compatible deployment instead of forcing a plain service-worker upload. See `references/cloudflare-worker-module-deploy-pitfalls.md`.
- **Read permission mismatch:** A token may list Worker routes and purge cache but return `405`/`10405` when reading script content. Do not overwrite an apex Worker unless you have current source or a verified local backup.


- **MainWP LocalWP child-site sync failures are often dashboard metadata, not the child plugin:** If MainWP says a child site does not connect and `wp_mainwp_wp_sync.sync_errors` contains `ERROR: Unexisting administrator user`, verify real child admin usernames and update `wp_mainwp_wp.adminname` in the LocalWP dashboard DB, then run `MainWP_Sync::sync_site()` from the LocalWP PHP runtime. See `references/mainwp-localwp-connection-repair.md`.
- **MainWP OpenSSL warnings on LocalWP can be stale config paths:** `openssl_pkey_export(): Cannot get key from parameter 1` in `page-mainwp-server-information-handler.php` usually means `mainwp_opensslLibLocation` points to non-existent `C:\php\extras\ssl\openssl.cnf`. Set it to the real LocalWP PHP `extras/ssl/openssl.cnf` and, if Windows OpenSSL remains noisy, set `mainwp_verify_connection_method=2` for PHPSECLIB fallback. Verify with MainWP handler methods and a Windows-local page fetch. See `references/mainwp-localwp-connection-repair.md`.
- **Affiliate measurement rollouts need site-side proof, not only GTM instructions:** For monetized WordPress posts, build a central offer registry, instrument every CTA with offer/page/position metadata, emit `affiliate_click` to both `dataLayer` and `gtag` when available, then verify with a browser-console click. If no GTM container/auth is present but GA4 `gtag` exists, deploy the GA4-compatible event layer and explicitly leave the GA4 key-event toggle as the only admin/UI step. See `references/wp-affiliate-measurement-system.md`.
- **Affiliate revenue recovery should be trust-and-measurement first, not new infrastructure:** When recovering monetized WordPress pages, publicly verify all money URLs as logged-out users with raw HTML and DOM checks, remove fake/future/unverifiable claims before CRO, add page/offer/position sub-IDs only where safely supported, and report GA4 admin gaps honestly if authentication is unavailable. See `references/wp-affiliate-revenue-recovery.md`.
- **MU-plugin `the_content` filters can blank huge pages/posts:** Broad `preg_replace_callback()` cleanup over large `<!-- wp:html -->` front-page templates or long article bodies can fail or strip rendered bodies while HTTP remains 200. Avoid sitewide `the_content` regex filters for affiliate rel/content cleanup unless absolutely necessary; prefer offline REST/XML-RPC batch edits or DOM-safe targeted rewrites. If you must filter, skip `is_front_page()` and huge content, assign regex output to `$updated`, fallback to original content if replacement fails or visible-word output collapses, and verify homepage + representative posts with cache-busted visible word counts after Cloudflare purge. If multiple posts suddenly show only title/header/metadata while HTML still returns 200, immediately disable the broad `the_content` filter first, purge Cloudflare, and verify representative posts by visible word count/browser snapshot before doing any content restoration. See `references/wp-mu-plugin-content-filter-safety.md`.
- **Bad MU plugins can lock you out of WordPress rollback routes:** MU plugins load before wp-admin and `admin-ajax.php`, so a PHP fatal in `wp-content/mu-plugins/*.php` can break WP File Manager, plugin screens, and AJAX rollback attempts. Before uploading any generated MU-plugin PHP, write the exact final file locally and run `php -l`; confirm hosting-panel/SSH/SFTP rollback access; deploy disabled/rename where possible; and keep a harmless stub ready. If the site becomes HTTP 500, stop retrying wp-admin and remove/rename the file via hosting/SSH/SFTP. If direct SSH/FTP fails but CyberPanel is available, use its per-domain cron manager as an emergency escape hatch: schedule a one-minute `/bin/mv .../mu-plugins/bad.php .../bad.php.disabled-hermes`, verify public 200s after the cron runs, then remove the cron. See `references/wp-mu-plugin-fatal-recovery.md`.
- **Cloudflare Rulesets may be unavailable while Workers still work:** If an exact old URL needs a 301 redirect and the Dynamic Redirect/Rulesets API returns `403 request is not authorized`, do not stop there. Check Worker script + route permissions. If available, deploy a tiny route-scoped Worker for only the legacy path, with an exact-path guard and `fetch(request)` fallback for non-exact matches. Back up routes/script, verify `301 -> 200` with a single-hop chain, and document route rollback. See `references/cloudflare-scoped-worker-redirect.md`.
- **Cloudflare admin challenges break plugin/post editing:** If plugin activation/deactivation or post editing fails, check `/wp-admin/plugins.php`, `/wp-admin/post.php?...`, and `/wp-login.php` for `cf-mitigated: challenge` before debugging WordPress permissions. Admin/login challenge rules can block the UI even when public pages and REST endpoints work. Relax only the admin/login challenge, leave XML-RPC/bot protections intact, and verify with a real admin cookie.
- **Portfolio inventory: do not over-ask for Lovable exports before public/API enrichment:** When cross-linking GitHub + Cloudflare + Lovable + Supabase, first build/update the artifact from GitHub, Cloudflare Pages, Cloudflare DNS, public `lovable.dev/projects/<uuid>` responses, public `*.lovable.app` pages, and `_lovable` DNS TXT records. Only after that, ask for the exact private Lovable dashboard access still needed (workspace invite link/member role, collaborator account, cookies/session, or screenshots as last resort). See `references/lovable-portfolio-enrichment-without-oauth.md`.
- **Worker origin host can leak into wp-admin redirects:** When an apex Worker fetches WordPress from `origin.example.com`, WordPress may generate `redirect_to=https%3A%2F%2Forigin.example.com%2Fwp-admin...`. For admin/login paths, set upstream `Host` to the apex and rewrite both direct and URL-encoded origin hosts in `Location` headers. Do not apply public canonical/robots rewrites to wp-admin HTML.
- **Origin hostname canonicalization behind an apex Worker:** If `origin.example.com` is publicly indexed but the apex Worker still needs it as an upstream, add a WordPress/MU-plugin `template_redirect` 301 only when `HTTP_HOST` is the origin host. Preserve Worker origin fetches by having the Worker send the apex `Host` header (or a private bypass header such as `X-GUTF-Canonical-Proxy: 1`). Verify with `allow_redirects=False`: origin homepage, archives, and post URLs should return `301 Location: https://example.com/$path`, while apex homepage/wp-admin still return 200.
- **REST API content field format:** Must be `{"raw":"<html>"}` not `"<html>"` — silent failure (no error, content silently rejected)
- **REST API strips style/media:** Any `<style>` tag or `@media` rule in post content gets stripped by the sanitizer and may leave raw CSS visibly printed at the top of the post. Use XML-RPC instead when available. If XML-RPC is blocked by Cloudflare/WAF and no snippet/file-write path is immediately available, rebuild the affected post with REST-safe inline `style` attributes (no `<style>` tags), purge Cloudflare, and verify in browser that no raw CSS text is visible and no horizontal overflow exists. For affiliate/commercial posts, do not stop at string checks: run rendered 320px and 390px mobile probes for overflow, skinny product-card text columns, injected blank image gaps/figures, single-H1, and CTA presence. See `redesign/references/wordpress-rest-safe-mobile-commercial-posts.md` for the full QA contract.
- **Application password write scope:** On gearuptofit.com, application passwords are READ-ONLY — they can't update posts, settings, or anything
- **XML-RPC CDATA:** Use `<![CDATA[...]]>` for large HTML content to avoid XML entity issues
- **Cloudflare may block XML-RPC at the apex:** If `https://gearuptofit.com/xmlrpc.php` or another WordPress domain's `/xmlrpc.php` returns a Cloudflare `403 Attention Required`, retry XML-RPC directly against the origin IP with `Host: example.com`; this preserves public-domain WordPress context while bypassing the edge challenge. For SEO batch edits, use XML-RPC when REST write is blocked or REST sanitizes HTML, but always back up raw post content first and verify cache-busted public HTML after cache purge.
- **SEO plugin/meta output may not follow XML-RPC edits:** Updating post title/content/custom fields can leave Yoast/RankMath/theme/performance-plugin title/meta output stale or duplicated. After XML-RPC edits, verify `<title>`, meta description, canonical, robots, and H1 from live HTML separately from the body. Prefer the SEO plugin API/options where available; use narrowly scoped output-buffer overrides only as a last resort and only for the edited URLs. If public HTML still emits old high-risk meta snippets after custom fields are correct, add a URL-scoped early MU-plugin output buffer that removes every stale `name="description"`, `og:description`, and `twitter:description`, inserts exactly one clean description/social description, purges Cloudflare, then verifies exact meta counts plus non-target page word counts. On AffiliateMarketingForSuccess imported rewrites, update all active SEO/meta families together when present: Yoast (`_yoast_wpseo_*`), RankMath (`rank_math_*`), SmartCrawl/WDS (`wds_title`, `wds_metadesc`, `wds_description`), theme/metabox (`metabox_post_title`, `metabox_post_description`), and legacy `kk_seo_title`/`kk_seo_desc`; live `<title>` may still be served from a cache until Cloudflare/plugin cache is purged. New AMFS NeuronWriter/XML-RPC details and Yoast indexables regeneration pattern are captured in `references/amfs-neuronwriter-xmlrpc-yoast-indexables.md`. AMFS batch rewrite head/cache/visual QA lessons are captured in `references/amfs-batch-rewrite-head-cache-visual-qa-2026-05-31.md`: malformed historical slug fallback via public body post ID, stale public head despite correct storage/Yoast REST, Code Snippets head override caution, Seraphinite exact-URI cache clearing, robust article-scoped image/artifact checks, and the rule to report partial if rendered mobile/desktop QA is not completed.
- **XML-RPC success is not public-render success on cached homepages:** For cache-heavy front pages, add a unique marker to any CSS/body rescue, then verify three surfaces: XML-RPC stored body, public apex raw HTML, and origin-IP raw HTML with `Host`. If stored content has the marker but public HTML does not, continue cache clearing before browser QA or final claims. For AMFS specifically, public wp-admin/XML-RPC may be Cloudflare-blocked; extract the AMFS origin IP from the Hosting Panel line in the local secrets file (do not assume another site's origin), publish Page ID 30 via origin XML-RPC with `Host: affiliatemarketingforsuccess.com`, wrap large homepage payloads in `<!-- wp:html -->...<!-- /wp:html -->` so WordPress does not paragraph-wrap CSS, then verify the normal `/` URL after Cloudflare purge — not only a cache-busted URL. See `references/amfs-homepage-mobile-rescue-cache.md`.
- **Full-bleed homepage CSS can be stored but paragraph-wrapped by WordPress:** If a custom WordPress homepage contains `.lumen-root`/markers in public HTML but containers render full-width, style rules do not appear in `document.styleSheets`, or a JS-injected runtime style tag never appears, inspect `<style>` blocks for inserted `<p>` wrappers. Fix the publication format before fighting specificity: republish the whole landing payload inside a Gutenberg Custom HTML block (`<!-- wp:html --> ... <!-- /wp:html -->`), then verify stored body, raw public HTML, DOM style-tag presence, desktop/mobile grid, and overflow. AMFS/Page ID 30 details live in `references/amfs-homepage-full-bleed-blockwrap.md`.
- **Lazy-loaded image false negatives:** `document.images` can show below-the-fold article images as incomplete/naturalWidth 0 until scrolled. For image repair verification, scroll each target image into view, wait briefly, then check `complete`, `naturalWidth`, and `naturalHeight`.
- **Single old-slug redirect fallback:** If Cloudflare Redirect Rules / Rulesets return `403 request is not authorized` but the token has Worker edit/route permissions, do not abandon the redirect. Use a narrowly scoped module Worker route for only the legacy slug, with an exact pathname guard and `fetch(request)` fallback. Back up existing routes/script, preserve query strings, then verify `301 -> target` with final `200` and exactly one redirect hop. See `references/single-slug-worker-redirect-fallback.md`.
- **Batch rewrite contamination emergency:** If a user reports that every blog post received all source sections, immediately stop batching and repair surgically from the original source file by explicit post ID. Do not rebuild from public/rendered HTML. Parse each source record with bounded `START POST NN` / `END POST NN` markers, verify one clean section per post before writing, then verify stored XML-RPC body and public URL separately. If public HTML shows repeated `wp:post-content`, TOC entries, or Amazon/product modules while stored bodies look clean, suspect malformed Gutenberg block comments and cache/plugin amplification: republish emergency plain HTML with all `<!-- wp:* -->` comments stripped, temporarily disable TOC plugins if they amplify the output, purge LiteSpeed/Cloudflare, and browser-verify one normal article flow. Keep the user update terse and evidence-first. See `references/mysticaldigits-batch-rewrite-repair.md`.
- **Batch cleanup should be script-first and terse:** When the user provides many GearUpToFit URLs with broken shortcode/template residue and explicitly demands speed/efficiency, do not crawl/edit/report one page at a time. Use the batch pattern in `references/gearuptofit-batch-content-residue-cleanup.md`: REST raw audit, conservative regex cleanup, XML-RPC origin write, one Cloudflare purge, cache-busted verification, compact final evidence.
- **Do not equate string cleanup with visual cleanup:** For imported/review posts, passing bad-string checks is insufficient. If the issue mentions mobile distortion, review cards, star ratings, tables, leaked HTML, or user says the blog post is visually unreadable, run rendered mobile + desktop verification before claiming done. Use the DOM overflow probe and hardfix pattern in `references/gearuptofit-visual-layout-verification.md`; report viewport width, scroll width, and overflow count instead of only shortcode counts.
- **Do not rebuild imported rewrites from contaminated rendered HTML:** If a post becomes distorted after publishing a rewrite, assume old rendered fragments may have been appended back into the clean article. Rebuild from the source rewrite file or a known-clean backup, not the live public HTML. Strip old plugin TOC markers (`ez-toc-*`), stale review/pricing modules, internal content-brief sections, duplicate body H1s, and previous template wrappers; then reinsert only minimal verified monetization blocks and scoped layout CSS. See `references/wp-imported-rewrite-layout-recovery.md`.
- **Full-post rewrites need a first-post quality gate before batch publishing:** When replacing many existing posts with rich rewritten HTML, publish exactly one target first, back it up, use XML-RPC if the rewrite contains `<style>`/JSON-LD, prevent duplicate H1s caused by the theme title plus internal article title, update Yoast/RankMath/social meta fields, then verify live public HTML and browser render before scaling. See `references/wp-full-post-rewrite-publishing-pipeline.md`.
- **Multi-post source files need batch QA, not one-off success checks:** When a user supplies one document of many rewritten posts, parse all targets first, back up every affected post, sanitize publisher-only notes/media placeholders/body JSON-LD, preserve disclosures/tags, publish via XML-RPC origin when rich HTML is present, purge Cloudflare, then verify every live URL with a compact PASS count. If a theme suppresses/demotes `<h1>` on some templates, use a site-safe accessible primary-heading fallback only after public HTML proves the issue. For SOTA/affiliate batches, add rendered 320px/390px/desktop QA, lazy-image scrolling, skinny-table detection, and screenshot evidence before claiming done. See `references/wp-multi-post-rewrite-source-file-publishing.md` and `references/wp-batch-rewrite-rendered-qa-hardening.md`.
- **XML-RPC media insertion needs stored-body proof, not just a success response:** When adding images/figures to an existing post, `metaWeblog.editPost` may return `<boolean>1</boolean>` while a full round-tripped post object fails to persist the intended body changes. Use a minimal edit payload for surgical image insertion, add unique markers around media blocks, immediately re-fetch `metaWeblog.getPost` to confirm markers/image URLs/captions in `description`, then purge and verify public HTML plus rendered lazy-loaded dimensions. See `references/wp-xmlrpc-media-insertion-pitfalls.md`.
- **BulkImporter shortcode entities:** Broken importer shortcodes may be HTML-entity encoded (`id=&#8217;2&#8242;`) and wrapped in `<div>` or `<span>` inside list items. Regex for `\[bulkimporter_image[^\]]*\]`, not only literal ASCII quotes.
- **Visible JSON-LD verification and cleanup:** Do not fail pages just because valid schema exists in scripts. Strip all `<script>...</script>` blocks, then search the remaining body for `@context` + `schema.org` to detect schema visibly leaking into content. When cleaning leaked schema from a post body, use bounded start/end markers and preserve the new content marker/module; if a broad regex removes real content, immediately restore the raw backup and reapply a narrower removal. See `references/wp-visible-schema-leak-cleanup.md`.
- **`wp.getPosts` with non-standard post types:** Returns "Invalid post type" for Elementor CPTs
- **Credentials file location:** `/home/hermes/.secrets/alexiios-websites-credentials.txt` — two password sets per site (Wp-Admin + REST API/Application Password)
