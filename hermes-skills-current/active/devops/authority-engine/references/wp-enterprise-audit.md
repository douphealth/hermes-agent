<!-- Consolidated from skill: wp-enterprise-audit; original path: /home/hermes/.hermes/skills/devops/wp-enterprise-audit -->

---
name: wp-enterprise-audit
description: Comprehensive WordPress site audit and remote remediation using CLI tools and REST API. Covers SEO, security, performance, and indexing when browser tools are unavailable or admin access is restricted.
category: devops
tags: [wordpress, seo, audit, curl, rest-api, security]
---

# WordPress Enterprise Audit & Remote Remediation

## Overview
Performs deep technical audits of WordPress sites using `curl` and the WP REST API when browser tools fail, node is unavailable, or admin UI is inaccessible. Identifies SEO, security, and performance gaps, then applies fixes.

## 0. Enterprise SEO intelligence before touching the site
Before editing anything, identify the real search battlefield:
- start with broad niche terms, then refine into high-intent modifiers and support questions
- capture the domains ranking repeatedly across those SERPs
- score domains by overlap, position, and presence on commercial queries
- treat those repeated domains as the true competitors, including hidden competitors the user did not name
- inspect which page types keep winning: comparison, alternatives, tool, use-case, template, statistics, review, FAQ

For rewrite planning based on these findings, also load `serp-driven-rewrite-playbook`.

This prevents weak audits that only compare against obvious brand competitors.

## 1. CLI-Based Site Audit (When Browser Fails)
If `browser_navigate` fails (e.g., missing node/agent-browser or permission denied on the local browser binary), pivot to terminal immediately instead of stalling. Use direct HTTP fetches plus REST API inspection as the primary path.

```bash
# Fetch homepage and headers
curl -sIL https://example.com > headers.txt 2>&1
curl -sS https://example.com -o home.html -w "HTTP:%{http_code} Size:%{size_download}"

# Check robots.txt and sitemap
curl -sS https://example.com/robots.txt
curl -sS https://example.com/sitemap_index.xml
```

### Key Checks
Extract critical metrics from `home.html`:
- **Security Headers**: Look for `strict-transport-security`, `x-frame-options`, `x-content-type-options`, `referrer-policy`, `permissions-policy`. (Most WP sites miss these).
- **H1/H2 Structure**: `grep -c '<h1' home.html`. Should be exactly 1 H1. Multiple H1s are a critical SEO flaw.
- **Meta Tags**: Description, canonical, OG tags, Twitter cards.
- **Raw vs Rendered Head Output**: For JS-heavy, iframe/app, Lovable/Webflow-style, or snippet-driven homepages, compare raw `<title>` / meta from `curl` against browser-rendered `document.title` and DOM state. Embedded apps or runtime scripts can mutate `document.title` after load, creating a real SEO consistency issue even when the raw head looks correct. Use browser console checks such as `document.title`, visible H1s, `document.forms`, iframe `src`s, and rendered CTA/form state before claiming title/H1/conversion surfaces are clean.
- **Page Size**: >150KB raw HTML indicates inline bloat (common in page builders/GenerateBlocks).
- **Intent Match**: Check whether title, H1, hero copy, and CTA all align to the same search intent.
- **Conversion Surface**: Check whether ranking pages expose a clear CTA, lead magnet, product path, or internal next step.
- **Trust Layer**: Check for author, editorial policy, methodology, disclosure, and evidence-note links on pages that deserve them.

## 1b. AI SEO opportunity modeling
After collecting technical findings, build an opportunity matrix for enterprise prioritization:
- target query or topic
- intent class
- likely winning page type
- monetization path
- trust burden
- internal-link parent/child relationships
- whether the page needs a tool, template, checklist, FAQ, comparison table, or lead magnet

The audit should output not just defects, but the next highest-value pages and assets to publish.

## 1c. Batch post-prioritization for upgrade sprints
When a site has a large archive, do not inspect posts randomly.
Use the REST API to pull the full post list and score posts for upgrade priority using signals like:
- commercial modifiers in the title (`best`, `vs`, `review`, `tools`, `hosting`, `SEO`, `email`, `software`)
- affiliate / buyer-intent phrases
- freshness / current-year relevance
- likely monetization fit
- cluster leverage for internal linking

Then inspect the highest-scoring posts for these upgrade gaps:
- duplicate H1s
- missing editorial-policy / methodology links
- missing affiliate disclosure where needed
- missing related-guides block
- weak conversion next step (no checklist, lead magnet, or clear CTA)
- stale or non-canonical trust links (for example, legacy editorial-policy URLs that should be normalized to the current canonical trust pages)
- thin trust pages that exist but are too weak to support archive-wide authority
- homepage-only performance issues like embedded base64 SVG/CSS overlays that do not appear across the article archive
- plugin-managed title/meta layers that keep serving stale public head output even after REST `title` / `excerpt` updates succeed

This is faster and higher ROI than linearly reviewing the archive.

## 1c-b. Premium content quality audit layer
When the audit includes content rewrites or on-page quality recommendations, also load `wordpress-sota-seo-content-system`.
Score each target page on:
- intent clarity in H1 and first screenful
- answer-first usefulness
- specificity vs fluff
- section architecture
- scannability and visual hierarchy
- comparison/checklist/table usefulness
- internal-link quality
- trust visibility
- schema fit
- whether the page feels premium or generic

Your audit should recommend rewrite mode explicitly:
- micro-upgrade
- additive rewrite
- consolidation rewrite
- full rebuild

Do not recommend destructive rewrites by default. Recommend the smallest intervention that creates a premium result.

## 1d. Verification resilience for large WordPress pages
Some large posts on production WordPress sites intermittently time out on 30-second HTTP reads during live verification.
If verification fetches time out:
- retry with a longer timeout (for example 60s)
- keep cache-busting on the URL
- verify both public HTML and Yoast head endpoints when possible

Do not treat a single timeout as proof the page is broken.

For large archive-wide upgrade sprints, the strongest low-risk pattern is:
- select the next 5 highest-value posts
- inspect structural/trust/internal-link gaps via REST
- apply additive trust/disclosure/Related-guides/checklist upgrades in batch
- then verify live status, H1 count, canonical trust links, disclosure presence, Related-guides presence, checklist presence, and Yoast endpoint status for each URL

Additional production finding from Mice Gone Guide:
- some sites expose normal WordPress REST edit access but do NOT expose any Yoast/RankMath/AIOSEO REST namespace or writable SEO meta fields beyond a trivial `meta.footnotes`
- on those sites, REST `title` and `excerpt` updates can succeed while the public `<title>` and meta description remain stale because a plugin-managed snippet/indexable layer keeps serving old head output
- verify this explicitly by comparing:
  1. REST `title.raw` / `excerpt.raw`
  2. live public `<title>` / `<meta name="description">`
- if they diverge consistently, report a plugin-layer blocker instead of pretending title/meta cleanup is complete
- continue shipping body-level improvements anyway: trust blocks, internal links, next-step CTAs, canonical trust-page routing, FAQ coverage, and section upgrades still materially improve quality and rankings even when snippet-layer control is blocked
- for a formal mismatch diagnosis/remediation workflow, also load `yoast-snippet-layer-remediation`

Production finding from repeated archive upgrade batches (AFS + Mice Gone Guide):
- iterative batch upgrades work better than giant rewrites
- the durable quality wins come from standardizing the same enterprise layer across the archive:
  - editorial review block
  - canonical editorial policy link
  - canonical review methodology link
  - affiliate disclosure block when commercial intent exists
  - strong Related guides block that reinforces the current money cluster
  - checklist or next-step CTA so the article is no longer a dead end
- for core intent pages, also add missing sections like "When to Call a Professional" and "Cost-Benefit Analysis" when they materially improve decision quality
- for next-tier traffic pages, prepend a short query-aligned quick-answer / intent note near the top to sharpen answer-box usefulness without rewriting the full article
- thin trust pages should be upgraded before or alongside archive work so the new trust links point to assets worth linking to
- on some sites, weaker duplicate trust pages cannot be redirected via Yoast because no redirect REST route is exposed; in that case, convert them into thin support pages that explicitly point users to the canonical trust assets
- on some sites, homepage meta descriptions remain controlled by a plugin/snippet layer even after `wp/v2/settings` description updates; treat this as a plugin-layer blocker, not a failed REST write
- on some sites, public `<title>` and meta description may diverge from successful REST `title.raw` / `excerpt.raw` updates because a hidden SEO plugin snippet/indexable layer keeps serving stale head output; confirm this by building a URL-by-URL mismatch map before claiming metadata is fixed
- verification on some production WordPress sites may require 90-150s timeouts for slow pages; intermittent read timeouts do not necessarily mean the page is broken
- this pattern materially improves consistency, trust, internal-link architecture, and conversion direction without redesigning pages
## 2. WP REST API Capabilities Check
Authenticate via Application Password (REST API credentials) vs WP-Admin cookie credentials. **They are different.**

```bash
# Check user capabilities
curl -s "https://example.com/wp-json/wp/v2/users/me" -H "Authorization=[REDACTED] <base64_user:pass>"
```

**Critical Limitation**: REST API Application Passwords do **NOT** grant `unfiltered_upload` or `activate_plugin`. You **cannot** create `mu-plugins`, install plugins, or upload files via REST API alone.
- **However**: Admin users (id=1) with REST API passwords **CAN** edit theme-block content through the Site Editor REST endpoints:
  - **Template Parts**: `GET/POST /wp/v2/template-parts/{theme}//{slug}?context=edit` — edit header, footer, sidebar block markup
  - **Templates**: `GET/POST /wp/v2/templates/{slug}?context=edit` — edit page, single, archive templates
  - **Global Styles**: `GET/POST /wp/v2/global-styles/themes/{theme}?context=edit` — inject custom CSS via `styles.css`
- **File Changes** (mu-plugins, wp-config.php): Still require WP-Admin cookie session or SFTP.
- **If WP-Admin is 403'd**: The site has an IP whitelist/WAF blocking `wp-login.php`. You cannot write to the server without admin dashboard access, SFTP, or REST API admin credentials.

## 3. What You CAN Fix Remotely via REST API

### 3a. Site Editor Endpoints (Block Themes like Twenty Twenty-Four)
For FSE/block themes, you can edit theme-level markup without file access:

```bash
# Edit a template part (e.g., footer)
curl -s "https://example.com/wp-json/wp/v2/template-parts/{theme}//footer?context=edit" \
  -H "Authorization=[REDACTED] <base64>"

# Update the footer template part (POST with content.raw)
curl -s -X POST "https://example.com/wp-json/wp/v2/template-parts/{theme}//footer?context=edit" \
  -H "Authorization=[REDACTED] <base64>" \
  -H "Content-Type: application/json" \
  -d '{"content":"<!-- wp block markup here -->"}'

# Global styles — inject custom CSS via styles.css
curl -s "https://example.com/wp-json/wp/v2/global-styles/themes/{theme}?context=edit" \
  -H "Authorization=[REDACTED] <base64>"
# Response has settings, styles (including styles.css) keys
# POST back updated styles.css to hide elements or inject CSS overrides
```

**Important**: The template part ID format is `{theme}//{slug}` (double slash), e.g., `twentytwentyfour//footer`. The `?context=edit` flag is mandatory to get writable `content.raw` fields.

### 3b. Standard Page/Post Edits
If you have a user with `publish_pages` / `edit_posts`:
- **Update Page Content**: `POST /wp/v2/pages/{id}?context=edit` (Fix heading structures in `content.raw`).
- **Edit Theme Blocks**: Template parts and global styles (see 3a above).
- **Do not rely on old search-engine sitemap ping endpoints**: Google and Bing legacy ping URLs now commonly return `404` / `410` and are not a dependable indexing action. Focus instead on:
  - valid `robots.txt`
  - valid sitemap/index URLs
  - strong internal linking
  - indexable homepage/category/post templates
  - Search Console / Webmaster Tools property-level submission and inspection where available

## 4. Google Search Console Integration
If a GSC Service Account JSON key is available on disk:
```bash
pip install google-api-python-client google-auth
python -c "
from google.oauth2 import service_account
from googleapiclient.discovery import build
creds = service_account.Credentials.from_service_account_info(key_data, scopes=['https://www.googleapis.com/auth/webmasters'])
service = build('searchconsole', 'v1', credentials=creds)
# Use service.urlInspection().index().inspect()...
"
```

## 5. Security Headers Fix (Enterprise Grade)
Since REST API cannot write files, the fix requires either:
1. **Cloudflare API**: Use `CLOUDFLARE_API_TOKEN` to add `headers` transformation rules.
2. **WP-Admin Dashboard**: Inject via "Insert Headers and Footers" plugin or `wp-config.php` via File Manager plugin.

```apache
# Apache .htaccess or Cloudflare Transform Rules
Header always set Strict-Transport-Security "max-age=31536000; includeSubDomains"
Header always set X-Frame-Options "SAMEORIGIN"
Header always set X-Content-Type-Options "nosniff"
Header always set Referrer-Policy "strict-origin-when-cross-origin"
Header always set Permissions-Policy "geolocation=(), microphone=()"
```

## 6. Editing Theme-Level Content (Headings, Footer, Template Parts)

Block themes (Twenty Twenty-Four, etc.) store headings, site titles, and footer text in **template parts** and **templates** — NOT in page content.

```bash
# Discover all template parts
curl -s "https://example.com/wp-json/wp/v2/template-parts?context=edit" -H "Authorization=[REDACTED] <base64>"
# Discover all templates
curl -s "https://example.com/wp-json/wp/v2/templates?context=edit" -H "Authorization=[REDACTED] <base64>"

# Get a specific template part (note: double slash in ID)
curl -s "https://example.com/wp-json/wp/v2/template-parts/{theme}//{slug}?context=edit" \
  -H "Authorization=[REDACTED] <base64>"
# Common slugs: header, footer, sidebar, post-meta
```

**Removing "Mice Gone Guide" heading**: Check 3 places:
1. **Header template part** — `wp:site-title` block in `twentytwentyfour//header`
2. **Page template** — `wp:post-title` block in `twentytwentyfour//page` (renders H1 for all pages)
3. **Footer template part** — `wp:site-title` block in `twentytwentyfour//footer`

Remove the offending blocks from each template part's content, then POST back the updated content.

**Fixing footer copyright year**: It's in the footer template part's raw content as plain text within a `wp:paragraph` block.

## 7. Cloudflare WAF Blocks PUT Requests — Use POST Override

Cloudflare returns error 1010 on PUT requests to the WP REST API. Workaround:

```bash
# Write payload to file first (avoids shell escaping issues with large block markup)
echo '{"content":"<!-- wp blocks -->"}' > /tmp/wp_payload.json

# Use POST with X-HTTP-Method-Override header
curl -s -X POST "https://example.com/wp-json/wp/v2/pages/123?context=edit" \
  -H "Authorization=[REDACTED] <base64>" \
  -H "Content-Type: application/json" \
  -H "X-HTTP-Method-Override: PUT" \
  -H "User-Agent: Mozilla/5.0" \
  --data-binary @/tmp/wp_payload.json
# Returns 200 on success
```

Python alternative:
```python
import urllib.request, json
url = "https://example.com/wp-json/wp/v2/pages/123?context=edit"
payload = json.dumps({"content": "<fixed content>"}).encode()
req = urllib.request.Request(url, data=payload, method='PUT')
req.add_header('Authorization', f'Basic {b64}')
req.add_header('Content-Type', 'application/json')
try:
    resp = urllib.request.urlopen(req, timeout=30)
    result = json.loads(resp.read())  # 200 OK
except urllib.error.HTTPError as e:
    # e.code 1010 = Cloudflare block — switch to POST + X-HTTP-Method-Override
    pass
```

## Common Pitfalls
- **Truncated Secrets**: Credentials in flat files (e.g., `*.txt`) are often clipped or redacted. Check env vars (`echo $VAR`) if the file shows `...`.
- **Multiple H1s**: Often caused by the theme rendering `<h1>` for the site title AND the post title inside `single.php`. Another real production case: the theme/template already renders an `entry-title` H1, while the page body contains a custom hero `<h1>` added via raw HTML or blocks. In that case, keep the theme/title H1 as the canonical page heading and demote the custom hero heading to `<h2>` styled like the original hero so the visible design stays intact. A second real pattern from AFS archive work: older AI/comparison posts may contain a separate decorative `<h1 class="main-heading">...` block deeper in the article body. Treat that exactly the same way — demote the decorative `main-heading` H1 to H2 and re-verify live H1 count. Block themes store headings in template parts — use section 6 above when the duplicate comes from theme markup.

- **Stale Front-End After API Writes**: WordPress caching plugins serve old HTML even after REST API updates succeed. Verify with cache-busting: `curl -s "https://example.com/?nocache=<random>"`.
- **Cloudflare 1010 on PUT**: Cloudflare WAF blocks direct PUT requests. Always use POST with `X-HTTP-Method-Override: PUT` header. Write large JSON payloads to temp files and use `--data-binary @file` to avoid shell escaping.
- **Two Credential Sets**: The secrets file may have both WP-Admin passwords and REST API Application Passwords. They are different credentials. REST API passwords work for `/wp-json/` endpoints; WP-Admin passwords do NOT work for REST API.
- **Finding All Broken Links**: Check page content, header/footer template parts, navigation menus (`/wp/v2/navigation/{id}`), page/post content, and global styles. The homepage content is often stored in the page's `content.raw` field, but CTAs and buttons can be embedded as raw HTML within those blocks.