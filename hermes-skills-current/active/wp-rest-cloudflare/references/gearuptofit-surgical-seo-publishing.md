# GearUpToFit surgical SEO publishing pattern

Use this reference when optimizing an existing GearUpToFit WordPress post and publishing the surgical edits.

## Durable workflow

1. Run an intelligence brief first when available:
   ```bash
   python3 /tmp/hermes-audit/hermes-config-001/scripts/seo/surgical_seo_intelligence_brief.py \
     --url https://gearuptofit.com/path/to/post/ \
     --max-sitemap-urls 250 \
     --out /tmp/surgical-brief
   ```
2. Read raw WordPress content using REST with `context=edit` and the application password. On GearUpToFit, application passwords are useful for raw reads even when write scope is blocked.
3. Back up the raw post HTML before edits.
4. Build a surgical patch, not a full rewrite. Prioritize:
   - top-of-page Quick Answer / AEO block if absent
   - Yoast title/metadesc alignment
   - broken escaped anchor/link residue such as `https:=` or visible `&lt;/a&gt;`
   - unsupported exact statistics unless backed by sources
   - internal links to cluster-supporting posts
   - authority references for nutrition/medical/fitness claims
   - safety notes for YMYL topics such as low energy availability, disordered-eating risk, or medical conditions
5. If REST write is blocked or sanitizer risk exists, publish with XML-RPC against the origin IP using HTTPS + `Host: gearuptofit.com`. Manual XML body POST with CDATA is safer than relying on `xmlrpc.client` host overrides if the library request receives origin 404s.
6. Update Yoast via XML-RPC `custom_fields` in the same edit when possible:
   - `_yoast_wpseo_focuskw`
   - `_yoast_wpseo_title`
   - `_yoast_wpseo_metadesc`
7. Purge Cloudflare exact URL after publish.
8. Verify cache-busted public HTML and browser render before reporting success.

## Verification contract

For edited GearUpToFit posts, verify:

- HTTP 200 on cache-busted public URL
- canonical is the apex URL
- exactly one public meta description
- H1 count is one
- updated Yoast `<title>` and meta description are live
- Quick Answer / AEO block visible when added
- newly added section and internal links visible
- no visible raw CSS/HTML/shortcode leakage
- no `https:=`, escaped anchor residue, or old unsupported claims remain
- browser visual QA: readable top of article, no obvious layout break, no challenge page

## Notes

- Keep Yoast as the SEO control plane; do not recommend replacing it.
- For YMYL-adjacent nutrition posts, avoid fake precision and cite authority sources rather than making unsupported performance claims.
- Preserve the existing article voice/structure unless explicitly asked for a full rewrite.