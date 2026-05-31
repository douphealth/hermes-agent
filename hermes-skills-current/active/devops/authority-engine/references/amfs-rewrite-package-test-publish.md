# AMFS Rewrite Package Test-Publish QA Notes

Use when publishing user-supplied AMFS rewrite ZIP/HTML packages to live WordPress posts.

## Durable lessons
- Do not batch-publish rewrite packages blindly even when validation reports pass. Inspect one article first for wrong entity/template leakage.
- Common package residue to remove before publishing:
  - visible headings like `SEO, GEO, and AEO optimization notes`
  - `Publishing checklist for WordPress`
  - package generator comments
  - media-library/process captions that describe the package rather than helping the reader
- Some generated files may target the wrong primary entity in early H2s (example pattern: an alternatives page saying `Quick answer: is Merlin worth it?`). Check H1, first 3 H2s, hero CTA, comparison table, FAQ, schema `about`, and affiliate offers for entity alignment.
- If the existing live post has AMFS affiliate telemetry and the rewrite package only has generic `data-amfs-offer` links, preserve/reinsert the live `amfs-affiliate-box` module so above-intro monetization and `affiliate_click` survive.
- If the product has no verified affiliate URL, keep its official/direct link non-sponsored and monetize only verified alternatives. Never invent a sponsored link.
- On themes that render the WP title as the public H1, demote the article-body H1 to a styled non-H1 before publish; verify canonical and cache-busted HTML for exactly one H1.
- Public `<head>` can be controlled by a custom meta-output layer independent of Yoast/RankMath custom fields. After updating `_yoast_wpseo_*`, Rank Math, WDS, metabox, etc., still inspect live `<title>`, description, OG, and Twitter tags. Stale `2026` meta after field updates indicates an output-buffer override to fix separately.
- Use XML-RPC via origin IP + `Host` header when REST edit context/write is blocked. Send a minimal `metaWeblog.editPost` struct; reusing the whole `getPost` object can fail with `Invalid attachment ID` because of stale attachment metadata.

## Minimum one-post test publish gate
1. Extract selected HTML.
2. Back up current XML-RPC post JSON + raw HTML.
3. Polish generated article: remove internal scaffolding, fix entity mismatch, keep schema/media, preserve affiliate module.
4. Validate prepublish counts: one raw body H1 or zero if theme H1 will render; schema JSON parses; images and iframe URLs return 200; fake/future claim patterns absent.
5. Publish with minimal XML-RPC payload: `title`, `description`, `mt_excerpt`, targeted `custom_fields` only.
6. Verify canonical and cache-busted URL: 200, canonical tag, exact live H1 count, schema parse, affiliate markers, image/video presence, no fake-claim hits.
7. Purge Cloudflare exact URL and active performance plugin if canonical differs from cache-busted.
8. Inspect public `<head>` separately; do not claim meta cleanup until title/description/OG/Twitter are clean live.
