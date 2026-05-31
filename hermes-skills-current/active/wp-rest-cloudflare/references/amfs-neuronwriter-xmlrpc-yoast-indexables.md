# AMFS NeuronWriter + XML-RPC publishing lessons

Use for affiliatemarketingforsuccess.com full-post SEO rewrites that need NeuronWriter scoring, XML-RPC publishing, cache purge, and public metadata verification.

## NeuronWriter automation facts

- AMFS NeuronWriter project signature observed: `de592047df7acdd5`.
- Creating an analysis can be done via `POST https://app.neuronwriter.com/backend/new-analysis` with session cookies.
- Important payload quirks:
  - `language` must be `English`, not `en`.
  - `additional_keywords` should be newline-separated, not comma-separated.
  - Include `project`, `keyword`, `target_url`, `engine` (`google.com`), and `prefer_lang=1`.
- Existing editor HTML/JS can expose scoring data and endpoints. A working scoring bridge can parse editor page data and call backend scoring/readability endpoints with the draft title, description, body text, and content terms.
- NeuronWriter score should be verified from the backend response and saved as JSON before publishing, not claimed from visual/editor assumptions.

## WordPress publishing pattern that worked

- Back up posts with XML-RPC `metaWeblog.getPost` before edits.
- Publish rich HTML via XML-RPC `metaWeblog.editPost` with CDATA to avoid REST/Cloudflare/sanitizer issues.
- Remove body `<h1>` because the WordPress theme renders the page H1.
- Update SEO field families together when present:
  - `_yoast_wpseo_title`, `_yoast_wpseo_metadesc`, `_yoast_wpseo_focuskw`
  - Yoast social fields: `_yoast_wpseo_opengraph-title`, `_yoast_wpseo_opengraph-description`, `_yoast_wpseo_twitter-title`, `_yoast_wpseo_twitter-description`
  - Rank Math title/description/focus/social fields
  - `wds_*`, `kk_seo_*`, `metabox_post_title`, `metabox_post_description`, and common AIOSEO/Genesis/SEOPress keys if present
- After publish, purge both WordPress/Seraphinite cache and Cloudflare exact URLs, then QA cache-busted public URLs.

## Yoast indexables / public meta pitfall

Stored post custom fields can be correct while public `<meta name="description">`, `og:description`, and `twitter:description` remain stale because Yoast/frontend indexables or another platform cache still emits old values.

Do not call metadata complete until all three surfaces agree:

1. Stored post/API/XML-RPC custom fields.
2. WP admin edit screen visible Yoast fields.
3. Public raw HTML head tags on a cache-busted URL.

If stored fields and admin edit fields are correct but public head output remains stale, force a real WP admin post save/update for the affected posts (classic `post.php` flow with `_wpnonce`, `post_ID`, `post_title`, `content`, `excerpt`, `yoast_wpseo_*` fields), then purge WordPress/Seraphinite and Cloudflare again and re-check public raw HTML.

## AMFS content-quality guardrails

- Do not invent earnings claims. Remove or source unsupported revenue claims such as `$2.4M` before publishing.
- Affiliate pages need visible affiliate disclosure when affiliate programs/products/links are discussed.
- Verify public content for: HTTP 200, expected title, canonical, single H1, no unsupported claims, Quick Answer present, new core sections present, and no visible planning artifacts.
