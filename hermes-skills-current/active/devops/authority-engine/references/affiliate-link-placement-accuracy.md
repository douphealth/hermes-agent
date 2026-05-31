# Affiliate Link Placement Accuracy

Use this when adding affiliate monetization to SEO/blog content or auditing existing posts for affiliate opportunities.

## Core principle
Affiliate links must be **accurate, verified, and contextually relevant**. Do not maximize link count; maximize reader-fit and tracking correctness.

## Hard rules
- Never publish dashboard/login URLs as affiliate links unless the dashboard URL is also explicitly the verified tracking destination.
- Never invent affiliate links or assume a program's public homepage is the tracking link.
- Retrieve the real tracking/deep link from the partner dashboard or approved local credential source before publishing.
- Verify final outbound URLs resolve/redirect correctly before claiming completion.
- Use descriptive, natural anchors tied to reader intent; avoid generic `click here` anchors.
- Do not insert affiliate offers into trust/legal/admin pages unless the page is explicitly a recommended-tools/resources page.
- Avoid affiliate stuffing. Prefer the smallest set of highest-fit offers.
- Preserve disclosure requirements where compensation may exist.

## Efficient sitewide workflow
1. Build or load a sanitized affiliate inventory: program name, category, target topics, and known dashboard location. Exclude passwords/secrets from working files.
   - If the user supplies a raw list of affiliate programs/links and asks whether they are valid/operational, first run the operational validation workflow in `references/affiliate-link-operational-validation.md`; do not deploy links until each is categorized as `USE NOW`, `VERIFY MANUALLY BEFORE USE`, `RETRIEVE FROM DASHBOARD`, or `DO NOT USE`.
2. Pull WordPress post/page inventory via REST (`posts` + `pages`, `context=edit` when available). Handle BOM-prefixed JSON by stripping `\ufeff` before parsing.
3. Score posts by topical fit using title, excerpt, and a bounded content sample.
4. Exclude low-value publishing targets:
   - About, Contact, Privacy, Terms, Disclaimer, Disclosure
   - Editorial policy, review methodology, correction/accessibility pages
   - off-topic health/plant/pest posts unless the affiliate offer is genuinely contextual
5. Create a deployment queue with evidence terms, target URL, candidate programs, and accuracy gate.
6. Before editing a post, retrieve and verify the final affiliate/deep links from dashboards.
7. Insert links only in sections where the product/service solves the exact user problem.
8. For larger rollouts, follow `references/affiliate-manager-wordpress-rollout.md`: deploy only `USE NOW` links, insert compact disclosed CTA boxes, apply a precision remap before finalizing top pages, and emit implementation/verification artifacts.
9. Run public QA: link resolves, disclosure remains present, content reads naturally, no broken internal links introduced.

## Useful local artifact pattern
For large affiliate rollouts, create these local files:
- `affiliate-programs-sanitized.json` — program/category/topic map only, no secrets.
- `affiliate-link-placement-policy.md` — operating rules and relevance map.
- `affiliate-opportunity-map.json` — raw opportunity map from REST scan.
- `affiliate-deployment-queue-refined.md` — filtered queue suitable for human/action review.

## Program relevance examples
- AI writing / content optimization: Frase, Jasper, Writesonic, Copy.ai, SEOWriting.ai, NeuronWriter, Scalenut, MarketMuse, Originality.ai, Pictory, Perplexity, Merlin.
- SEO: SEMrush, Frase, NeuronWriter, MarketMuse, Scalenut, GrowthBar, INK, SEOWriting.ai.
- Hosting / WordPress performance: SiteGround, Cloudways, Kinsta, WPX, Bluehost, NameHero, Namecheap, WP Rocket, DigitalOcean, Vultr, Nexcess.
- Email/list-building: AWeber, GetResponse, ConvertKit, HubSpot.
- Social/content workflow: Publer, Tailwind, Canva, BuzzSumo.
- Grammar/editing: Grammarly, ProWritingAid, QuillBot.
- Affiliate marketing: Indoleads, Fiverr, ClickBank only where the offer is topically relevant.
- Spiritual/numerology content: Moon Reading / ClickBank offers only when the article intent genuinely matches.

## Pitfalls
- A raw keyword match can create bad recommendations on trust pages; filter by page type before deployment.
- REST scans can time out on slow WordPress sites; retry with smaller `per_page` and higher timeouts rather than abandoning the site.
- Some REST responses contain a UTF-8 BOM; parse with `json.loads(response.text.lstrip('\ufeff'))`.
- A site can be static-cutover or non-WordPress publicly while credentials still exist; treat REST 404 as a platform-state blocker and continue other sites.
- Do not store pasted affiliate passwords in skill files, memory, or working policy artifacts.
- A first-pass classifier can mis-map offers when incidental terms dominate the page (e.g. chatbot content mapped to hosting). For high-intent pages, precision-remap before publishing: exact reviewed product > direct comparison products > category-leading alternatives > no deployment.
- If the direct product affiliate link is missing, broken, or dashboard-only, do not fake it with the homepage. Either retrieve/verify the real link or clearly present verified alternatives as alternatives/best-fit tools.
- During full article rewrites, preserve any existing affiliate/product box exactly once unless intentionally replacing it. After publishing, verify the rendered CTA selector/class actually used by the site theme/module (for AMFS boxes this has been `.amfs-aff-btn`) before declaring rel/target QA failed or passed.
