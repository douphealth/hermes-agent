# WordPress index cleanup patterns from AMFS session

Use this as a compact reference for WordPress SEO index-quality cleanup where the site has Yoast, Cloudflare, uploaded HTML residue, utility pages, and mixed archive behavior.

## Discovery pattern

- Check sitemap variants first: `/sitemap_index.xml`, `/sitemap.xml`, `/wp-sitemap.xml`, Yoast child sitemaps.
- Pull REST counts from headers for posts/pages before changing anything.
- Parse XML with namespaces and distinguish primary sitemap URL `<loc>` from `<image:loc>`. Yoast image URLs inside a post/page entry are not page-index contamination by themselves.
- Sample crawl sitemap URLs for: status, canonical, meta robots, H1 count, word count, title/meta description, residue strings, and unsupported hype claims.

## Common bad URL classes

- Standalone uploaded HTML under `/wp-content/uploads/YYYY/MM/*.html`: usually accidental static exports; 301 to the best canonical WP URL if equivalent exists, otherwise 410.
- Attachment pages mirroring uploaded HTML names: 301 to the canonical WP page/post or homepage if no specific equivalent.
- `/readme.html` and `/license.txt`: 410 unless the site owner has a special reason to expose them.
- Thin utility pages/quizzes/site maps: noindex and exclude from sitemap unless they have real search demand and substantial content.
- Duplicate policy/editorial pages: 301 to one trust-page canonical.
- Tags/search/date archives: usually noindex; date archives may redirect if useless.

## Implementation pattern

- Use a reversible MU plugin for WordPress-layer changes:
  - `template_redirect` for page-level redirects/410s.
  - `wp_robots` for noindex on utility pages/search/archive/attachment logic.
  - Yoast sitemap exclusion filters to keep noindexed/redirected URLs out of XML.
  - Output filter to add `rel="sponsored nofollow"` to likely affiliate outbound links if missing — but never return raw `preg_replace*()` output blindly. For large custom `<!-- wp:html -->` homepages/front-page landing templates, broad regex filters can fail and blank the page while HTTP stays 200. Skip `is_front_page()` unless explicitly editing the homepage, assign replacement output to `$updated`, return original content if `$updated` is not a string, and verify visible word count + hero text after deployment.
- Use `.htaccess` for static files that WordPress never handles:
  - Back up root `.htaccess` before edits.
  - For uploaded HTML, add a directory-level `.htaccess` in the exact uploads folder if root rewrites do not affect static files.
- Rewrite robots.txt as clean line-by-line directives; avoid compressed single-line syntax that can confuse crawlers.

## Fast execution pattern

- Avoid one huge unbounded crawl; it can hang on slow WordPress/Cloudflare responses. Use bounded batches:
  - recursive sitemap parse for primary URL `<loc>` values;
  - REST pagination with `per_page=100`, explicit JSON-error handling, and small `_fields` payloads;
  - targeted URL checks for known bad classes plus a representative sitemap sample.
- If a REST page returns non-JSON HTML despite `200`, do not keep retrying the same script. Log `status`, `content-type`, and a short preview, then continue with sitemap + cached prior inventory where available.
- Keep a structured audit artifact (`/tmp/...json` during the session) with `urls`, `rows`, `thin`, `residue`, `badh1`, `noncanon`, and `suspect_sitemap` so the next pass can resume without re-crawling everything.

## Verification pattern

- Purge Cloudflare exact URLs after changing robots, sitemaps, redirects, or static-file rules.
- Verify from public hostname, not only origin IP:
  - use `allow_redirects=False` / `curl -I` for status and exact `Location`;
  - fetch HTML with a cache-busting query for meta robots, canonical, title, and H1 count;
  - re-fetch sitemap index and child sitemaps after cache purge/indexable rebuild.
- Run `scripts/wp-index-cleanup-verify.py` for repeatable JSON proof, for example:
  ```bash
  python scripts/wp-index-cleanup-verify.py https://site.com \
    --check /robots.txt \
    --check /readme.html \
    --check /wp-content/uploads/2026/03/example.html \
    --check /site-map/ \
    --check '/?s=test'
  ```
- Treat query-string echo in redirect `Location` during cache-busted verification as a QA artifact; recheck the clean URL if the destination itself matters.
- Only request indexing in GSC after:
  - sitemap contains only canonical index-worthy URL `<loc>` entries;
  - redirected/noindexed/thin URLs are absent;
  - priority pages have refreshed answer-first sections, proof/source sections, and cleaned unsupported claims.
