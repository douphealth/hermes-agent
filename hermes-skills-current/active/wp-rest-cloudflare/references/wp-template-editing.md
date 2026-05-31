<!-- Consolidated from skill: wp-template-editing; original path: /home/hermes/.hermes/skills/devops/wp-template-editing -->

---
name: wp-template-editing
description: Edit WordPress block theme templates, template parts (header, footer), and global styles via the WP REST API when browser tools are unavailable.
category: devops
tags: [wordpress, rest-api, templates, block-editor, curl]
---

# WordPress Template Editing via REST API

## Overview
Edit block theme templates, template parts (header, footer), and global styles using the WP REST API. Works when browser tools fail or no browser is available.

If the template work affects visible content quality, article chrome, hero modules, or in-page visual HTML blocks, also load `wordpress-sota-seo-content-system`.
Use it to keep the end result:
- structurally clean
- premium in tone
- visually restrained instead of theme-breaking
- verified at both body and head layers where relevant

## Authentication
Use WP Application Password (REST API credentials, NOT WP-Admin login cookies):
```python
import base64
rest_creds = "user@app.com:xxxx xxxx xxxx xxxx"
b64 = base64.b64encode(rest_creds.encode()).decode()
```

## Endpoints
All use context=edit to access raw content:

```
GET  /wp-json/wp/v2/templates/{theme}//{slug}?context=edit
POST /wp-json/wp/v2/templates/{theme}//{slug}
GET  /wp-json/wp/v2/template-parts/{theme}//{slug}?context=edit
POST /wp-json/wp/v2/template-parts/{theme}//{slug}
GET  /wp-json/wp/v2/global-styles/themes/{theme-slug}?context=edit
```

Common template slugs: `page`, `single`, `index`, `home`, `404`, `search`, `archive`
Common template part slugs: `header`, `footer`, `sidebar`

Theme slug is usually the theme directory name: `twentytwentyfour`, `astra`, `generatepress`, etc.

## Listing Templates
```bash
curl -sS "SITE/wp-json/wp/v2/templates" -H "Authorization=[REDACTED] $B64"
curl -sS "SITE/wp-json/wp/v2/template-parts" -H "Authorization=[REDACTED] $B64"
```
Returns list with `slug` and `theme` for each.

## Reading a Template
```bash
curl -sS "SITE/wp-json/wp/v2/template-parts/THEME//footer?context=edit" -H "Authorization=[REDACTED] $B64"
```
Returns JSON with `content.raw` — the full block markup.

## Updating a Template
POST with JSON body: `{"content": "<block markup>"}`

### Cloudflare WAF Bypass
Cloudflare frequently returns "error code: 1010" when PUTting to the REST API. Use POST with override header instead:
```bash
curl -sS -X POST "SITE/wp-json/wp/v2/templates/..." \\
  -H "Authorization=[REDACTED] $B64" \\
  -H "Content-Type: application/json" \\
  -H "X-HTTP-Method-Override: PUT" \\
  -H "User-Agent: Mozilla/5.0" \\
  --data-binary @payload.json
```
Write the payload to a temp file first: `json.dump({"content": markup}, f)` then use `--data-binary @file` — never pass large content via `-d 'string'` due to shell escaping issues.

### UTF-8 BOM
Strip the BOM before parsing REST responses: `json.loads(r.stdout.lstrip('\ufeff'))`

```bash
curl -sS -X POST "SITE/wp-json/wp/v2/template-parts/THEME//footer" \
  -H "Authorization=[REDACTED] $B64" \
  -H "Content-Type: application/json" \
  -d '{"content": "<new block markup>"}'
```

The `content` field must be complete block markup (comment-delimited WP blocks), not a partial diff. You must provide the entire template content, not just a snippet.

## Updating Global Styles (Custom CSS)
```bash
curl -sS -X PATCH "SITE/wp-json/wp/v2/global-styles/THEME-ID" \
  -H "Authorization=[REDACTED] $B64" \
  -H "Content-Type: application/json" \
  -d '{"styles":{"css":"your CSS here"}}'
```

Note: The global-styles theme endpoint returns `id: null` for theme styles. You may need to create user-defined global styles first or use the `/wp-json/wp/v2/global-styles` list to find the correct ID.

## Verification
After updating, immediately GET the template again with `context=edit` to confirm changes saved. Then fetch the front-end with a cache-buster query parameter to verify:
```bash
curl -sS "SITE/?_=$(date +%s)" -o /tmp/page.html
```

## Cache
WP sites often use persistent page caching (LiteSpeed, WP Super Cache, Cloudflare). Use cache-busting query params (`?_=<timestamp>` or `?v=unique`) to bypass.

## GeneratePress Elements can override post/page hero output
On GeneratePress-based sites, broken titles or fake placeholders may come from Elements instead of templates.

Useful endpoint:
- `GET /wp-json/wp/v2/gp_elements?context=edit`
- `GET /wp-json/wp/v2/gp_elements/{id}?context=edit`
- `POST /wp-json/wp/v2/gp_elements/{id}` with `X-HTTP-Method-Override: PUT`

What to look for:
- `_generate_block_type: page-hero`
- `_generate_hook: generate_after_header`
- `_generate_disable_title: true`
- `_generate_disable_primary_post_meta: true`

This combination often means the site-wide single-post header is being driven by a GeneratePress Element, not the theme template.

Production finding:
- Some imported GeneratePress / GenerateBlocks hero elements store fallback strings like `Hello World`, `Post date`, and `Post author name` in their rendered block HTML.
- If the dynamic block output is broken, those fallbacks can leak live across every post.
- Fix path: back up the `gp_elements` object, patch the hero content, and verify live on multiple posts.
- When server-side dynamic rendering is unreliable, a practical fallback is to populate the hero from existing head metadata (`og:title`, `meta[name="author"]`, `article:published_time`) with a small front-end script and blank out the visible placeholder text so users never see the fake labels.

## Common Pitfalls
- Two H1 headings: Block themes render site-title (header) AND post-title (template) — both show as `Mice Gone Guide`. Remove both by editing header template part AND page template.
- Site-title is in header template as `<!-- wp:site-title {...} /-->` block
- post-title is in page template as `<!-- wp:post-title {...} /-->` block
- Footer copyright is typically a `<!-- wp:paragraph -->` block in the footer template part
- On GeneratePress, broken hero text may live in `gp_elements` rather than `/templates` or `/template-parts`
- You must send the FULL template or element content on POST — partial updates are not supported
- The `//` double-slash in the URL is intentional: `{theme}//{slug}` is the WP REST ID format for theme resources
- REST API credentials differ from WP-Admin credentials — they are separate application passwords