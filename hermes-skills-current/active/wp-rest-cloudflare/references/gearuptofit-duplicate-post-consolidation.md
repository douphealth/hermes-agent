# GearUpToFit Duplicate/Same-Intent WordPress Post Consolidation

Use when the user reports multiple WordPress posts competing for the same query/slug intent (for example exact-keyword slug plus older abbreviated slug).

## Fast workflow

1. Discover candidates through WordPress REST search, not only sitemap search:
   - `wp-json/wp/v2/posts?search=<query>&per_page=100&context=edit&_fields=id,date,modified,slug,status,link,title,content,yoast_head_json`
   - Also check `wp-json/wp/v2/search?search=<query>&per_page=100&subtype=any` to catch pages and odd matches.
2. For each real candidate, record:
   - ID, slug, status, link, title, date/modified, approximate word count, Yoast/user canonical if exposed.
   - Live HTTP status, HTML canonical, robots meta, and whether it appears in `post-sitemap.xml` / `post-sitemap2.xml`.
3. Choose the keeper by search intent and URL quality, not just age/word count:
   - Prefer exact-keyword, clean, current canonical slug if content quality is adequate.
   - Redirect older abbreviated/near-duplicate same-intent slugs into the keeper.
4. Implement a 301 at the edge when the apex Worker already centralizes routing. This avoids touching WordPress post content/layout and gives Google a strong consolidation signal.
5. Purge Cloudflare for old URL, no-slash old URL, keeper URL, and relevant sitemaps.
6. Verify:
   - Old URL and no-slash old URL return `301` to keeper.
   - Keeper returns `200`, self-canonical, `index, follow`.
   - Duplicate slug absent from sitemap; keeper present.
   - Inspect both URLs in GSC where access exists; resubmit master sitemap and the sitemap containing the keeper.

## GearUpToFit edge pattern

The apex Worker (`gearuptofit-lovable`) has a `REDIRECTS_301` map. Add both trailing and non-trailing versions:

```js
"/health/old-duplicate-slug": "/health/preferred-canonical-slug/",
"/health/old-duplicate-slug/": "/health/preferred-canonical-slug/",
```

Then syntax-check as ESM (`node --check` on a `.mjs` copy), deploy the Worker, purge the exact URLs, and verify with `allow_redirects=False`.

## Pitfalls

- Sitemap absence is not enough. A duplicate can be absent from sitemaps but still live as `200 index, follow` with a self-canonical; consolidate it anyway.
- GSC `URL is unknown to Google` on the duplicate is not a reason to leave it live. A 301 prevents future discovery/indexing and consolidates any internal/external links.
- Do not delete posts or edit medical/YMYL content as the first move when the goal is URL management. Use 301 consolidation first unless the user explicitly wants content pruning.
- REST search can return broad false positives for medical terms. Only redirect true same-intent duplicates, not loosely related posts mentioning the words.