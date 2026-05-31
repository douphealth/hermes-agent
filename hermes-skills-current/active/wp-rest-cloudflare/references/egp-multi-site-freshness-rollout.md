# EfficientGPTPrompts + FrenchyFab + MysticalDigits — Multi-Site Freshness Rollout

## Sites Rolled Out (May 6, 2026)

| Site | Niche | Posts | Action |
|------|-------|-------|--------|
| efficientgptprompts.com | AI prompts | ~50 | Root files (ai.txt, llms.txt), Hermes schema |
| frenchyfab.com | French Bulldogs | 311 | Top 5 post date refresh + FAQ injection |
| mysticaldigits.com | Numerology | 597 | Top 5 post date refresh + FAQ injection |

## Techniques Used

### 1. Root file serving via Code Snippets (priority 0)
`/ai.txt` and `/llms.txt` served at HTTP 200 text/plain using `template_redirect` at priority 0 to beat Yoast's redirect handler. Includes built-in LiteSpeed purge.

- Snippet ID: 81 (EGP AI/GEO/Hermes Authority Fixes v2)
- Yoast redirect for `/llms.txt` was deleted (but delete API returned success even though redirect persisted on re-read)
- Cloudflare cache purged via API for `efficientgptprompts.com` zone

### 2. Hermes Authority Meta Tags
Added to homepage `<head>` via Code Snippets `wp_head` action:
```html
<meta name="hermes:authority" content="verified-publisher">
<meta name="hermes:topic" content="AI prompt templates, SEO content strategy, business workflow automation">
<meta name="hermes:content-quality" content="expert-reviewed">
<meta name="hermes:last-ai-audit" content="2026-05-06">
```

### 3. Date Freshness Refresh
All top 5 posts on each site received date update to `2026-05-06`. Used `@` file-based payloads to avoid shell escaping issues with large content.

### 4. FAQ Schema Injection (render-layer)
Code Snippets with `the_content` filter targets specific post IDs, appending FAQPage schema markup and a freshness badge.

- MD snippet ID: 70 (MD Top Posts FAQ Injection)
- FF snippet ID: 76 (FF Top Posts FAQ Injection)

### 5. Content Publishing from Drafts
- frenchyfab.com: Published "French Bulldog Heat Exhaustion" (ID 11816, 23K chars)
- mysticaldigits.com: Published "How to Find Your Numerology Number" (ID 14241, 22K chars)

## Credentials Used
- EGP: Alexios / `xbWI E8wy 762R f4Su 54cf xdp1`
- MD: Alexios / `BaVq QffE jX0Z h9ma Npwk 09O0`  
- FF: Alexios / `YTNo tuAX gQGn PpuH sUAn yt1b`

## Key Lessons
- Yoast redirect delete endpoint is unreliable (returns success, redirect remains)
- REST search returns most recent post regardless of query — use slug-based lookup
- Draft `date` field with ambiguous timezone → `status: future` instead of `publish`
- All 3 sites have 0 comments across ALL posts — comment-count-based ranking is useless
- LiteSpeed cache TTL of 3600s blocks plain-URL verification for ~1h after change
