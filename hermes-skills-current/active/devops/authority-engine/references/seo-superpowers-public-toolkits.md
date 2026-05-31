# SEO Superpowers Layer — Public Toolkit Synthesis

Sources inspected and distilled:

- `aaron-he-zhu/seo-geo-claude-skills` — GEO, schema, content quality, entity, internal linking, technical SEO, rank/reporting skill contracts.
- `StanGirard/seo-audits-toolkit` — repeatable audit architecture: extraction, sitemap, links, headers, images, security, Lighthouse-style task separation.
- `searchsolved/search-solved-public-seo` — practical SEO scripts: topical maps, SERP crossover, keyword gaps, content decay, entity extraction, sitemap extraction, anchor relevance, link quality, page intent, meta/title tools.

This reference does not replace Authority Engine. It adds a sharper execution layer for SEO/AEO/GEO work.

## 1. SOTA operating model

Every SEO task should now be routed through four evidence loops:

1. **Crawl evidence** — sitemap inventory, HTTP status, canonical, indexability, H1/title/meta, schema, internal links, image alt, headings, content length.
2. **SERP evidence** — ranking page type, intent overlap, SERP feature pattern, competitor overlap/crossover, repeated entities, snippet formats.
3. **Authority evidence** — entity clarity, trust pages, author/org facts, citations, topical coverage, internal-link flow, freshness.
4. **Outcome evidence** — GSC decay/gains, keyword gaps, high-value pages with low internal links, rank/SERP-feature movement.

Never optimize from opinion if one of these evidence loops is available.

## 2. GEO / AI visibility extraction standard

From the GEO skill library, adopt these page requirements for AI citations and answer engines:

- Include self-contained, quotable paragraphs that name the entity, claim, scope, and condition.
- Use explicit dates or freshness context for facts that can age.
- Add source/citation context near important factual claims.
- Put direct answers immediately under question-matching headings.
- Use 40–60 word definition blocks for core concepts.
- Include concise comparison tables/lists where AI systems synthesize options.
- Ensure brand/entity facts are consistent across About, author, org schema, sameAs, social profiles, and trust pages.
- Treat unsupported superlatives as a trust risk; either source them or remove them.

### GEO page block pattern

```html
<section class="geo-answer-block">
  <h2>What is [topic]?</h2>
  <p><strong>[Topic]</strong> is ... [40–60 word answer with entity, scope, and practical condition].</p>
  <ul>
    <li><strong>Best for:</strong> ...</li>
    <li><strong>Not ideal for:</strong> ...</li>
    <li><strong>Evidence to check:</strong> ...</li>
  </ul>
</section>
```

## 3. SERP crossover and cannibalization rules

From Search Solved SERP crossover logic:

- **50%+ top-10 URL overlap** between two keywords usually means one page can target both or pages are cannibalizing.
- **25–50% overlap** means related but distinct; use hub/sibling architecture and differentiated angles.
- **1–25% overlap** means separate intent; create/maintain separate pages.
- **0% overlap** means unrelated or SERP too unstable; do not force into the same cluster.

Use SERP overlap, not keyword similarity alone, to decide consolidation vs separation.

## 4. Topical map / hub rules

From topical-map and content-hub tooling:

For each topic set, output a hierarchy:

- Pillar / hub
- Category / subhub
- Support articles
- Long-tail FAQ/HowTo pages
- Commercial/affiliate/review pages where relevant
- Internal-link routes: hub → support, support → hub, sibling → sibling, trust/methodology where needed

Every keyword should belong to exactly one primary page target. If it fits multiple pages, classify it as:

- primary target
- secondary mention
- anchor text candidate
- cannibalization risk

## 5. Content decay trigger model

From Search Solved content decay analyzer:

Use GSC exports with date/page/query/clicks when available.

Prioritize refreshes when:

- latest complete month clicks are materially below the page's peak month
- page has many impressions but falling CTR
- queries changed intent or SERP features changed
- rankings slipped for existing high-intent queries
- page has stale dates, outdated examples, or missing new entities

Refresh type:

- **Micro refresh:** <20% content change; add facts, links, dateModified only if meaningful.
- **Moderate refresh:** 20–50% change; update sections, add missing entities/examples, strengthen snippets.
- **Major republish:** 50%+ change; rework structure, update schema dateModified/lastmod, re-crawl, monitor 4–8 weeks.

## 6. Internal-link superpower rules

From internal-linking and link-quality tools:

Audit each link on:

- source URL
- target URL
- anchor text
- in-content vs nav/footer/sidebar
- status code
- relevance to target page
- anchor naturalness
- target commercial/authority value

Auto-fail anchors:

- vague: “click here”, “read more” unless context is excellent
- question fragments that do not describe the destination
- over-optimized exact-match spam
- misleading anchors
- typo/grammar errors

Prioritize links to:

- high-value pages with low incoming internal links
- fresh/updated pages needing discovery
- pillar pages from relevant support articles
- support articles from hub pages
- trust/methodology pages from review/commercial content

## 7. Entity extraction and topical authority rules

From entity extraction and entity optimizer workflows:

For each priority page, identify:

- named entities present
- missing expected entities from SERP competitors
- brand/entity statements
- author/org/trust mentions
- source/citation entities
- entity frequency without keyword stuffing

Entity optimization is not just adding nouns. Each important entity should be connected by a factual relationship:

- [Brand] reviews [category] using [methodology].
- [Author] has experience with [topic/tool/process].
- [Topic] relates to [subtopic] because [explicit relationship].

## 8. Technical SEO audit dimensions

From SEO audit toolkit and technical checker patterns, the minimum crawl checks are:

- status code and final URL
- title presence/length/duplication
- meta description presence/length/duplication
- robots meta / noindex
- canonical presence and self/other target
- exactly one visible H1 for important pages
- heading hierarchy anomalies
- schema JSON-LD presence/type/parse validity
- internal broken links
- redirect chains
- sitemap membership
- image missing alt
- word count / thin content risk
- hreflang if multilingual
- security headers when site-level technical audit is requested
- LLM crawler accessibility when GEO/AI visibility is requested

## 9. Scorecard

Score each page 0–2:

- indexability
- title/meta CTR fit
- intent match
- H1/heading clarity
- schema/rich-result eligibility
- snippet/AEO extraction readiness
- GEO/AI citation readiness
- entity completeness
- trust/E-E-A-T
- internal-link equity
- freshness
- conversion path

Total interpretation:

- **21–24:** strong; monitor and defend
- **16–20:** viable; targeted upgrades
- **10–15:** capped; needs structural/content fixes
- **0–9:** rebuild or consolidate

## 10. Execution contract

When using this layer, report:

- Evidence source used: crawl, SERP, GSC, competitor CSV, WordPress REST, code search.
- Exact pages/queries affected.
- Intervention type: technical fix, refresh, consolidation, new page, hub, internal-link pass, schema pass.
- Before/after checks.
- Remaining unknowns or blocked data.

Accuracy rule: do not claim rankings, volume, traffic, or citations without live data or provided exports. If unavailable, state that the recommendation is structural/probabilistic, not measured outcome evidence.
