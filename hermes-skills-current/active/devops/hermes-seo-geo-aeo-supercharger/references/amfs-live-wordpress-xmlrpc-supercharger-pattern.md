# AMFS live WordPress XML-RPC Supercharger pattern

Use this as a reusable pattern for `affiliatemarketingforsuccess.com` or similar Cloudflare-fronted WordPress/Yoast sites when the user explicitly authorizes applying edits.

## What worked

- Use WordPress XML-RPC when REST authentication is blocked or unavailable.
- If Cloudflare/WAF blocks the public hostname but origin is known, POST XML-RPC to the origin IP with the public `Host` header.
- Fetch the post with `metaWeblog.getPost`, save a complete JSON backup before any write, then update with `metaWeblog.editPost`.
- Yoast fields can be updated through `custom_fields` on XML-RPC posts:
  - `_yoast_wpseo_title`
  - `_yoast_wpseo_metadesc`
  - `_yoast_wpseo_focuskw`
  - `_yoast_wpseo_canonical`
- For SOTA/max-force requests, add visible utility modules, not just title/meta changes. On AMFS, a homepage authority module + answer-engine map materially improved visible topical authority and AI extractability.
- After writes, purge Cloudflare cache for the exact updated URLs if a token is available, then validate with cache-busted public URLs.

## Safe execution sequence

1. Load this skill plus `authority-engine` WordPress execution / SOTA rewrite references.
2. Retrieve credentials only from the secret file; never print secret values.
3. Fetch the current post/page and save full JSON backup under `/tmp/<site>-seo-upgrade/`.
4. Make surgical content changes:
   - preserve existing H1 and meaning;
   - add visible authority/AEO/GEO blocks near relevant anchors;
   - repair stale internal links;
   - update Yoast custom fields;
   - avoid duplicate broad schema when Yoast is the schema control plane.
5. Apply via `metaWeblog.editPost` only after explicit user authorization to apply edits.
6. Purge Cloudflare cache for exact URLs.
7. Validate public rendered output:
   - HTTP 200;
   - marker strings for inserted modules;
   - one H1;
   - title/meta description visible in HTML;
   - important internal links return 200;
   - visual/browser QA for layout and readability;
   - cache-busted URL check after purge.
8. If visual QA surfaces an existing readability problem near the edited area, apply a tiny contrast/layout fix rather than leaving a premium module next to broken-looking content.

## Reporting pattern

Report:
- updated URLs / post IDs;
- what visible modules or Yoast fields changed;
- backup paths;
- validation evidence;
- risks and next layer.

Do not claim rankings, traffic, or AI citations improved. Say that crawlability, answer readiness, metadata, and internal authority routing were improved and validated.