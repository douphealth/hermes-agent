# AMFS authority-link + inline SVG article upgrade pattern

Use this when improving existing AffiliateMarketingForSuccess/WordPress pillar posts for topical authority, AI visibility, engagement, and visual quality after the core SEO rewrite is already live.

## Pattern

1. **Back up the full XML-RPC post object first** (`metaWeblog.getPost`) before touching body HTML.
2. **Preserve the existing premium/scoped article wrapper** rather than replacing the whole rewrite. Add small, idempotent modules:
   - scoped CSS appended inside the existing article `<style>` block;
   - one contextual internal authority-link module near the final CTA;
   - one helpful visual figure near the top/article navigation.
3. **Prefer deterministic inline SVG diagrams for factual/strategy visuals** when image generation/upload is unavailable or risky. SVGs can be responsive, fast, accessible, and claim-safe if they describe processes rather than fake statistics.
4. **Make visuals accessible**:
   - `<svg role="img" aria-labelledby="...">`
   - `<title>` and `<desc>` inside the SVG
   - `<figcaption>` explaining how the reader should use the diagram.
5. **Build internal-link modules as contextual cards**, not bare link dumps. Each card should include:
   - rich anchor text matching an existing topical hub or supporting URL;
   - one sentence explaining why the destination matters;
   - absolute canonical URL;
   - no speculative/fake promises.
6. **Use live URL checks for every internal link** before finalizing. Require HTTP 200/final canonical proof for each destination.
7. **Keep WordPress body H1-free**. The theme renders H1. Article modules should start at H2.
8. **Purge both Cloudflare and the site cache** after publish. For Seraphinite Accelerator, admin-ajax `CacheOpBegin` can return text `0` while still accepting the purge; verify public cache-busted HTML afterward.

## QA contract

For each edited post, verify:

- public URL HTTP 200;
- design marker still present;
- authority-link module present;
- expected internal-link count and every link returns 200;
- SVG/figure present;
- accessible SVG title/description present;
- figcaption present;
- exactly one page H1 and no body/article H1;
- unsupported claims remain absent;
- no raw CSS leak in visible body text;
- no raw SVG markup leak such as visible `<rect`;
- rendered browser overflow is `0` on desktop and ideally mobile too.

## Notes from AMFS 2026 pillar upgrades

- Affiliate strategy post: use internal links to affiliate marketing hub, affiliate SEO hub, affiliate content strategy hub, affiliate programs hub, niche selection, affiliate program comparison, SEO for affiliate marketing, and affiliate mistakes.
- Content strategy post: use internal links to content strategy guide, affiliate content strategy hub, affiliate SEO hub, on-page SEO, link building, existing-page ranking improvement, sustainable content, and semantic clustering.
- The inline SVG diagrams should support the article's strategic model: affiliate operating system or content audit/topical-authority map.
