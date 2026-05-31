# WordPress Visible Schema Leakage Cleanup

Use this when a WordPress post renders JSON-LD/schema text visibly inside the article body instead of only inside `<script type="application/ld+json">` blocks.

## Detection

1. Fetch public HTML.
2. Remove all real script blocks before testing:
   ```python
   visible = re.sub(r'<script.*?</script>', ' ', html, flags=re.I|re.S)
   leaked = '@context' in visible or 'schema.org' in visible
   ```
3. Do not fail a page merely because valid JSON-LD exists in scripts/head. Only visible body leakage is a content defect.

## Safe repair workflow

1. Back up the exact raw WordPress post body before cleanup.
2. Locate the malformed visible block by bounded markers, not broad one-line paragraph regexes. Common start/end examples:
   - start: `<p>{<br />`
   - end: the matching `}</p>` or a known adjacent script/related-reading boundary
3. Replace only the malformed visible block with a short HTML comment or nothing.
4. Preserve any newly added content marker/module and all legitimate article sections.
5. Repair broken/trash internal links found inside the same area if the target is obvious.
6. Publish through XML-RPC/origin bypass when REST sanitizes or Cloudflare blocks writes.
7. Purge cache.
8. Verify:
   - marker/new module still exists
   - visible content word count did not collapse
   - exactly one H1
   - no visible `@context`/`schema.org` outside scripts
   - public browser view shows the intended section/table and no raw code

## Recovery if cleanup is too broad

If the cleanup removes real content or the new SOTA marker disappears, immediately restore from the pre-cleanup backup and reapply a narrower bounded removal. Do not try to reconstruct the missing article from rendered public HTML unless no raw backup exists.
