# WordPress XML-RPC media insertion pitfalls

Use this reference when adding generated or uploaded media to an existing WordPress post through XML-RPC on a Cloudflare-protected site.

## Durable lessons

1. **Verify stored post body after every XML-RPC edit.** `metaWeblog.editPost` can return success while a large fetched-and-mutated post object does not persist the intended body changes. After publishing, call `metaWeblog.getPost` and check that unique markers, image URLs, captions, and alt text are present in `description` before checking the public page.

2. **Prefer minimal edit payloads for surgical body updates.** For image insertion into an existing post, send a minimal post struct such as:

```python
edit_post(PID, {
  'title': TITLE,
  'description': updated_html,
  'mt_excerpt': META,
  'post_status': 'publish',
})
```

Avoid round-tripping the entire `getPost` response unless you must preserve/update custom fields in the same call. If custom fields are needed, merge them deliberately and re-verify stored state.

3. **Use stable insertion markers.** Insert comments like `<!-- amfs-helpful-image-1 -->` around new media blocks so stored-body and public HTML checks can distinguish newly inserted assets from theme/sidebar images.

4. **Do not assume the uploaded filename extension stays unchanged.** WordPress/performance plugins may convert uploaded PNG/JPEG assets to WebP and return a `.webp` URL from `wp.uploadFile`. Always embed the returned `url`, not the local filename you uploaded.

5. **SVG uploads may be blocked.** If SVG upload fails with “not allowed to upload this file type,” generate a raster PNG/WebP infographic instead, upload it, and embed the returned WebP URL. For deterministic helpful visuals, Pillow-generated 1600×900 WebP/PNG diagrams are a reliable fallback when external image generation is unavailable.

6. **Verify the public and rendered image surfaces.** After purge, check:
- public HTML contains the image tags, alt text, and captions;
- image URLs return `200` with `image/*` content type;
- rendered browser images have `complete=true` and non-zero `naturalWidth`/`naturalHeight` after scrolling lazy-loaded images into view;
- canonical, H1 count, and robots/indexability remain unchanged.

## Minimal verification signals to report

- Live URL
- Uploaded image URLs
- Stored-body marker presence
- Public image tag count and alt/caption presence
- Image URL status/content-type/bytes
- Rendered natural dimensions
- Cache purge result
- Backup path
