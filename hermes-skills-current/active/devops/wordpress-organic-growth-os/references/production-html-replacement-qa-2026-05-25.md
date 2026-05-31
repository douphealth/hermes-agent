# Production HTML Replacement QA Pattern — GearUpToFit Smartwatch Session (2026-05-25)

Use this reference when replacing a live WordPress money/pillar page with user-supplied premium HTML/CSS/JSON-LD, especially via XML-RPC/REST with Cloudflare and MU-plugin head guards in play.

## Durable Pattern
1. **Backup the exact current post payload first**
   - Save XML-RPC/REST response to the site audit directory before any body/title/meta write.
   - Save the normalized publish artifact separately so rollback and diff are practical.
2. **Extract only the actual code block from user-provided text**
   - Do not blindly publish the full message file.
   - Strip chat/instruction wrapper text such as “use this for…” before the first real `<style>`, `<article>`, or content block and after the final intended `</script>` / final HTML block.
   - Validation must explicitly search the public visible text for leaked instruction phrases.
3. **Normalize affiliate links during publish, not after**
   - Preserve verified ASINs and anchors.
   - Ensure Amazon URLs include `tag=papalex-20` and `language=en_US`.
   - Ensure affiliate anchors use `rel="sponsored nofollow noopener"` and `target="_blank"`.
4. **Keep Yoast/head/MU-plugin normalization aligned with the new content**
   - If a surgical MU-plugin head guard exists for the page, patch its exact-path title/meta override to the new title/meta in the same workflow.
   - Public QA must verify a single `<title>`, one meta description, no stale title fragments, and one H1.
5. **Guard against duplicate H1 from theme + post body**
   - If the theme already emits the WP title as H1 and the body code includes its own H1, either remove one in content or add an exact-path output-buffer cleanup in the MU-plugin.
   - Never apply global H1 rewrites.
6. **Purge and verify through the public URL**
   - Purge Cloudflare/edge cache after writes.
   - Verify cache-busted public URL, not just API success.

## Minimum Live QA JSON Fields
- HTTP status and Cloudflare cache status
- `<title>` text and count
- meta description count/content
- H1 list/count
- visible leaked-instruction phrase check
- product/entity section presence checks
- visible word count
- affiliate link count, unique ASINs, and bad affiliate-link list
- JSON-LD presence
- raw CSS/code leak check
- stale title fragment scan

## Pitfall Captured
A first publish used the whole message file and accidentally exposed the user's instruction line as visible body text. The correct durable fix is to extract the real HTML/code region before publishing and then include a negative visible-text QA assertion for instruction leakage.
