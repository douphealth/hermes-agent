# WordPress SEO meta residue cleanup after sprint edits

Use this when XML-RPC/REST content edits and SEO custom-field updates succeed, but live HTML still shows stale/high-risk `<meta name="description">`, OG/Twitter descriptions, or title fragments from Yoast/RankMath/theme/performance output.

## Trigger

After an SEO/GEO/AEO implementation sprint, live verification shows:

- body/H1/Quick Answer/trust module updated correctly
- custom fields such as `_yoast_wpseo_metadesc`, `rank_math_description`, or title fields are updated
- but public HTML still emits old meta snippets such as unsupported pricing, revenue, ROI, ranking, benchmark, or "best/fastest" claims

## Safe resolution pattern

1. Do **not** mass-edit the whole site and do **not** add broad `the_content` filters.
2. Scope the fix to the sprint-edited URL paths only via a URL map.
3. Add a narrowly scoped MU-plugin output-buffer normalization layer:
   - start an outer buffer as early as possible for front-end non-admin requests
   - only run when current path matches the sprint override map
   - remove every stale `<meta name="description">`
   - remove stale `og:description` and `twitter:description`
   - replace `<title>` if needed
   - insert exactly one clean meta description plus aligned OG/Twitter descriptions
   - fallback to original HTML if regex output is empty/non-string
4. Add only necessary URL repairs, e.g. `/reviews/` → `/review/`, when a canonical hub path was found to 404.
5. Purge Cloudflare after deploy.

## Verification contract

For every edited URL, cache-busted public HTML must show:

- HTTP 200
- exactly one `<meta name="description">`
- no stale high-risk phrases in meta (`$X/month`, `boost rankings`, `40% better`, `fastest`, unsupported ROI/revenue/traffic claims)
- self-canonical unchanged
- one H1
- Quick Answer present
- trust/proof module present where commercial
- sources/verification present

Also check representative non-target surfaces (homepage, a large long-form post, sitemap XML) still render with normal visible word counts. This catches MU-plugin output-buffer mistakes before reporting done.

## Pitfalls

- Updating SEO plugin custom fields does not guarantee public meta output changes; themes/performance plugins may inject stale snippets later in the render stack.
- A `wp_head` echo may appear before the stale plugin meta but not replace it; verifiers often capture the later stale `<meta name="description">`. Remove all old description tags in the final buffer and insert one canonical tag.
- Do not rely on status 200 alone. Previous broad regex filters can leave pages technically 200 while article bodies collapse.
