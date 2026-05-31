<!-- Consolidated from skill: wordpress-image-alt-caption-snippet-optimizer; original path: /home/hermes/.hermes/skills/devops/wordpress-image-alt-caption-snippet-optimizer -->

---
name: wordpress-image-alt-caption-snippet-optimizer
description: Improve WordPress image alt text, captions, and snippet usefulness for SEO and accessibility without turning images into keyword-stuffed nonsense.
version: 1.0.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [wordpress, images, alt-text, captions, seo, accessibility]
    triggers: [alt text, image optimization, captions, snippet optimization, media seo]
---

# WordPress Image Alt / Caption / Snippet Optimizer

## Purpose
Make page imagery more useful for users, accessibility, and search by improving alt text and captions where they actually help.

## Rules
- Alt text describes the image, not the target keyword list.
- Captions should add context, not repeat the alt text word-for-word.
- Decorative images should not receive bloated SEO alt text.
- Informational images should clarify what the user is seeing and why it matters.

## Workflow
1. Audit images in the target page.
2. Identify missing, weak, or spammy alt text.
3. Improve alt text for meaningful images.
4. Improve captions when they can increase understanding.
5. Check featured image usefulness where relevant.
6. Verify changes live when image markup is content-controlled.

## Reusable production pattern: replace or add featured images from local files
Use this when the user has generated/downloaded images locally and wants them attached accurately to specific WordPress posts.

1. Inventory the local folder first and map files to target post slugs by filename/topic. Do not assume every claimed image is actually present.
2. Verify the target posts via REST (`/wp-json/wp/v2/posts?slug=...&context=edit`) and back up the full post JSON before editing.
3. Compress oversized source PNGs to efficient web-ready assets before upload. A strong default when Pillow/cwebp are unavailable is ffmpeg:
   - `ffmpeg -y -i input.png -vf scale=1280:-2:flags=lanczos -c:v libwebp -quality 82 -compression_level 6 -preset picture output.webp`
4. Upload the compressed file to `/wp-json/wp/v2/media` with:
   - browser-like `User-Agent`
   - `Content-Disposition: attachment; filename="..."`
   - correct `Content-Type` such as `image/webp`
5. Immediately update the media object with meaningful metadata:
   - `title`
   - `alt_text`
   - `caption`
   - `description`
   - optionally attach `post`
6. Set the post's `featured_media` to the new media ID via REST (`POST` + `X-HTTP-Method-Override: PUT` is the safest cross-Cloudflare pattern).
7. If the user wants the image to appear *inside the article body* too, do not stop at `featured_media`.
   - fetch `content.raw`
   - build a real WordPress image block using the uploaded media ID, source URL, alt text, and caption:
     `<!-- wp:image {"id":123,"sizeSlug":"full","linkDestination":"none","align":"center"} --> ... <!-- /wp:image -->`
   - insert it at a safe early point in the article, usually after the first paragraph or after an opening answer/intro section
   - avoid duplicate insertion by checking whether the new media URL is already present in `content.raw`
8. Verify on both surfaces:
   - REST post now references the new `featured_media`
   - `content.raw` contains the new media URL when inline insertion was requested
   - public page HTML contains the new media URL on both the plain URL and a cache-busted URL
9. If plain live HTML initially fails to show the new media while the cache-busted URL does, re-check once after a short delay before escalating. On some WordPress stacks the plain page cache lags briefly behind a successful REST write.
10. If one of the expected local source files is missing, do not guess. Complete the posts you can, report the missing file precisely, and if useful improve metadata on the existing live image so the page is still left in a better state.
11. If the uploaded image exists in REST and in public HTML but still renders as broken/missing to users, inspect the live page visually. Some optimization layers rewrite `<picture>` / WebP / AVIF sources into broken variants even when the JPEG attachment itself is valid.
12. Reusable recovery pattern for broken optimizer-generated image sources:
   - verify the direct public media URL returns `200` with a real image content-type before trusting it
   - if WordPress/optimizer keeps emitting broken `<picture>` sources, replace the visible in-post image with a guaranteed-render path such as a custom HTML block using a `div` background image pointing to the stable JPEG URL
   - add a cache-busting query string to the visible image URL when the optimizer keeps rewriting plain file references incorrectly
   - when using a background-image fallback, quote the URL explicitly inside `background:url('...')` so the markup survives theme/plugin rewriting cleanly
   - purge Cloudflare/cache for both the post URLs and the exact media URLs after the fix
   - verify again on the plain no-query post URL with browser vision, not just HTML presence
13. Strong production lesson from PlantasticHaven image rollout: HTML presence is not proof of visible rendering. A page can contain the new image URL and still show a broken placeholder because an optimization plugin transforms the source set into dead `.webp` / `.avif` assets. When that happens, switch from normal WordPress image blocks to a more forceful visible-render strategy and verify visually.

## Important audit lesson: do not trust sitemap image counts alone
When a user asks which WordPress posts "do not have an image," do **not** rely only on the XML sitemap `Images` column or Yoast image counts.

Reusable verification pattern:
1. Pull the post inventory from `/wp-json/wp/v2/posts`.
2. Compare against the post sitemap if useful, but treat sitemap image counts as a hint only.
3. Check `featured_media` for each post via REST.
4. Fetch the live post HTML and verify whether `<img>` tags exist.
5. Optionally also check for `og:image` as a secondary social/featured-image signal.
6. Only classify a post as truly image-less when the live URL has no meaningful image presence after verification.

Why this matters:
- sitemap image counts can under-report or omit images
- a post can still have a featured image and live rendered images even when a sitemap entry looks suspicious
- reporting "missing images" from sitemap data alone can create false positives

## Good alt text examples
- what the image shows
- why the image matters in context
- plain language

## Bad alt text examples
- repeated exact-match keyword chains
- generic placeholders like image123
- captions copied into alt text verbatim when unnecessary

## Output contract
Report:
- number of images improved
- where alt text changed
- where captions changed
- any media-library or theme-layer blockers
