# MiceGoneGuide-style batch rewrite + consolidation pattern

Use this reference when a WordPress publisher provides a batch of rewritten posts that must be applied precisely, with some legacy article intents consolidated into canonical URLs.

## Durable pattern

1. **Parse source file into canonical targets before publishing**
   - Identify which source rewrites are final standalone posts and which are legacy intents that should redirect into a stronger canonical target.
   - Do not blindly publish every rewritten block as a separate live URL if the brief says to consolidate intent.
   - Produce a target map: `source title/old slug -> canonical slug -> post ID/new post?`.

2. **Back up every affected post first**
   - Save raw XML-RPC/REST body, title, slug, excerpt, and relevant SEO custom fields before editing.
   - Keep rollback instructions practical: which post IDs and which MU/plugin files must be reverted.

3. **Use XML-RPC for rich article HTML**
   - Prefer raw XML-RPC `metaWeblog.editPost`/`newPost` via origin IP + `Host` header when the article HTML includes `<style>`, JSON-LD, or rich wrappers.
   - REST may sanitize styles or turn publisher paste artifacts into visible text.

4. **Quality-normalize imported article HTML**
   - Remove publisher-only sections such as `WORDPRESS COPY/PASTE`, `Recommended internal links`, editing notes, and internal prompts.
   - Prevent duplicate H1s: if the theme renders the title H1, strip body H1; if the theme fails to render a page H1 for a specific template, keep/add exactly one body H1.
   - Verify disclosures and monetization compliance: Amazon affiliate disclosure present, correct tracking tag, no fake prices/ratings/specs.
   - Verify embedded video privacy form when relevant (`youtube-nocookie.com`).

5. **Canonical/redirect layer**
   - For exact legacy slugs, prefer exact one-hop 301s. If Cloudflare rules are unavailable, use a narrow MU plugin or a scoped Worker route.
   - Preserve query strings.
   - Keep the target canonical URL premium and live before redirecting old slugs.
   - If SEO/head output stays stale after XML-RPC meta fields, use narrowly URL-scoped head normalization only for the edited URLs; do not apply sitewide output rewrites.

6. **Cache clearing sequence**
   - Purge Cloudflare exact URLs first; if normal URLs stay stale while cache-busted URLs are correct, use purge-everything.
   - For Seraphinite Accelerator, look under **Accelerator → Manager**. Its admin page can call `admin-ajax.php?action=seraph_accel_api&fn=CacheOpBegin`; exact URI purge may return `0`, so final proof must be live/cache-busted public HTML, not the AJAX response alone.

7. **Verification contract**
   - Canonical posts: `200`, expected title/H1 pattern, exactly one H1 total, canonical URL correct, disclosure present, affiliate tag present, no raw CSS visible, no visible schema leakage, no publisher artifacts.
   - Legacy URLs: `301`, correct `Location`, query preservation, target returns `200`, single hop.
   - Run both normal and cache-busted public checks after purge. If the site is behind Cloudflare, note `cf-cache-status`/`age` where useful.

## Session-specific example

MiceGoneGuide batch rewrite required publishing 8 canonical posts while consolidating legacy herbal/electronic/ultrasonic intents. A MU plugin was used for exact legacy redirects and URL-scoped head normalization. The critical lesson was to treat source-file consolidation instructions as authoritative: the two old ultrasonic/electronic rewrites became redirects into one canonical `electronic-and-ultrasonic-pest-repellers` page rather than duplicate live posts.
