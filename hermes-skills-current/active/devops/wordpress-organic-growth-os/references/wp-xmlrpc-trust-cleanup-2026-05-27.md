# WordPress XML-RPC trust cleanup pattern — 2026-05-27

Use when a managed WordPress site needs emergency trust/SEO cleanup but normal REST endpoints are blocked by Cloudflare, app passwords fail, or public REST search does not expose the needed posts.

## Durable workflow

1. **Public bounded audit first**
   - Crawl only the named target URLs and the sitemap subset needed for lookup.
   - Capture: status, redirect target, title, meta description, H1 count/text, visible text flags, raw HTML flags, canonical, cache header.
   - Separate page-body defects from template/wrapper defects.

2. **Back up before every production write**
   - Use `metaWeblog.getPost` through XML-RPC and save the full XML response per post ID before editing.
   - Keep separate backup folders for content, metadata, and broad custom-field/meta-family patches.
   - Never store or print secrets; read them from the local secret file only at runtime.

3. **Use origin XML-RPC when Cloudflare blocks normal routes**
   - POST to the origin IP XML-RPC endpoint with `Host: <domain>` and `verify=False` if the origin certificate is not valid for the IP.
   - Methods used successfully: `metaWeblog.getPost`, `metaWeblog.editPost`.
   - This can work even when public REST auth/search is blocked or incomplete.

4. **Patch content and metadata separately**
   - Content body/title/excerpt via `metaWeblog.editPost`.
   - Metadata via `custom_fields` using existing field IDs when available.
   - Patch all accessible SEO families when the active head generator is uncertain:
     - Yoast: `_yoast_wpseo_title`, `_yoast_wpseo_metadesc`, social title/description
     - RankMath: `rank_math_title`, `rank_math_description`, social title/description
     - SmartCrawl/WDS: `wds_title`, `wds_description`, `wds_metadesc`
     - theme/metabox/legacy: `metabox_post_title`, `metabox_post_description`, `kk_seo_title`, `kk_seo_desc`

5. **Purge exact Cloudflare files**
   - Purge changed public URLs only unless a template-layer change requires broader purge.
   - Then verify normal and cache-busted URLs.

6. **Final verification must distinguish surfaces**
   - Stored XML-RPC content may be clean while live wrapper still injects related-post/template text such as `No posts`.
   - Public `<title>`/meta can still come from a plugin indexable, builder, legacy head injector, or template layer after common custom fields are patched.
   - Report remaining platform-layer issues explicitly instead of hiding them.

## AMFS session-specific learnings

- High-risk trust cleanup succeeded by rewriting the post bodies for pages with future/unverifiable claims (`Q4 2026`, `2,847`, `15,000`, `5.7x`, `$8,340`, medical diagnostics framing).
- Exposed shortcode leakage in an archive/hub was fixed by updating the source tool post title/excerpt/body; public archive verification confirmed `[wpcode]` disappeared.
- Remaining live `No posts` text was wrapper/template related, not in edited bodies.
- Remaining stale generated SEO titles on some pages persisted despite common SEO meta-family patches; treat as an admin/template/indexable issue for the next deeper pass.

## Report format for this user

Keep the final short and evidence-first:
- Outcome
- Implemented URLs
- Removed risk flags
- Verification evidence
- Remaining gaps by layer
- Rollback artifact paths
