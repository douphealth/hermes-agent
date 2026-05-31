# WordPress batch rewrite rendered-QA hardening

Use this reference for multi-post rewrite batches where the user expects enterprise/SOTA publication quality, especially affiliate/product posts with rich CSS, tables, and images.

## When this applies
- User supplies one combined source document for many WordPress posts.
- Content contains custom CSS, product boxes, Amazon CTAs, tables, or imported/publisher artifacts.
- User complains previous posts were visually broken or explicitly requires mobile + desktop verification.

## Fast pipeline
1. Parse every record first: title, slug/URL, target post ID if existing, source HTML, excerpt/meta if present.
2. Back up raw stored content for every affected post before writing.
3. Sanitize before publish:
   - remove body JSON-LD/scripts and publisher-only/source-brief artifacts;
   - remove/demote body H1 unless public theme verification proves the template suppresses its own H1;
   - normalize Amazon links to `tag=papalex-20`, `target="_blank"`, and `rel="nofollow sponsored noopener"`;
   - upload or reuse local media for product/article images when external URLs are blocked, hotlinked, or unreliable.
4. Publish via XML-RPC when content contains `<style>`, media-rich HTML, or Gutenberg/REST sanitization risk.
5. Re-fetch stored XML-RPC body immediately; verify marker, image count, Amazon count/tag, and no unsafe artifacts.
6. Purge Cloudflare exact URLs. If normal URLs still serve stale `cf-cache-status: HIT`, escalate to purge-everything or repeat exact purges and verify the normal URL, not only cache-busted variants.
7. Raw public QA all URLs: status 200, article wrapper present, exactly one public H1, sufficient images, Amazon links tagged, no origin-host/importer/schema artifacts.
8. Rendered browser QA all URLs at 320px, 390px, and desktop. Fail on horizontal overflow, skinny text columns, broken lazy-loaded image dimensions, missing product boxes/CTAs, or duplicate/missing H1.
9. Save screenshot evidence for at least mobile + desktop of every post.

## H1 handling pitfall
Do not blindly strip every body H1 and assume the theme title will appear. Some WordPress templates/import contexts suppress the theme title for specific posts. Preferred sequence:
1. remove body H1 before initial publish to avoid duplicates;
2. public raw/rendered check exact H1 count;
3. if a page has zero public H1, add one accessible body H1 only for that URL;
4. re-purge and re-check exactly one H1.

## Mobile table pitfall
A table can have no horizontal overflow but still be visually unreadable because header cells collapse into 18–30px columns. Rendered QA should include a skinny-text detector on `.post`/article `p`, `li`, `td`, `th`, CTA links, and product cards. If mobile tables fail:

```css
@media(max-width:760px){
  .post-content table,.post-content tbody,.post-content tr,.post-content th,.post-content td{
    display:block!important;width:100%!important;min-width:100%!important;max-width:100%!important;
    float:none!important;clear:both!important;white-space:normal!important;overflow-wrap:break-word!important;text-align:left!important;
  }
  .post-content th,.post-content td{padding:10px 12px!important;line-height:1.5!important}
  .post-content colgroup,.post-content col{display:none!important}
}
```

If a theme/UA keeps `<thead>` visually clipped while body rows are fine, do not overfit the QA to hidden header fragments; inspect the rendered table and either hide/restyle the header intentionally or transform tables into card rows.

## Lazy-loaded image verification
Do not count an image as broken until the browser has scrolled it into view and waited briefly. For rendered QA, scroll page sections and each article image into view, then check `complete`, `naturalWidth`, and `naturalHeight`.

## Evidence contract
Final report should be terse and evidence-first:
- Published/backed up counts.
- Created vs updated counts.
- Raw public QA pass/fail count.
- Rendered QA viewport matrix and fail count.
- Product/Amazon/image check counts.
- Screenshot count + artifact directory.
- Mention any cache escalation performed.
