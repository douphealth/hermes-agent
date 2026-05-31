<!-- Consolidated from skill: wordpress-sota-seo-content-system; original path: /home/hermes/.hermes/skills/devops/wordpress-sota-seo-content-system -->

---
name: wordpress-sota-seo-content-system
description: SOTA enterprise-grade system for rewriting and upgrading WordPress content via REST with premium human-style copy, visual HTML modules, schema planning, SERP intent matching, duplicate consolidation, and strict verification.
version: 1.0.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [wordpress, seo, content, serp, schema, copywriting, eeat, html, visual-design]
    triggers: [rewrite post, upgrade content, improve seo content, premium article, human written, visual html elements]
---

# WordPress SOTA SEO Content System

Use this when rewriting, upgrading, consolidating, or publishing WordPress pages/posts where the goal is not just "better copy" but materially stronger rankings, CTR, conversion support, answer-engine usefulness, and perceived quality.

For maximum-quality, multi-layer SEO execution, load `devops/authority-engine` first and use this skill as the page-execution layer.

## Mission
Ship pages that feel:
- human-written
- visually premium
- commercially intelligent
- structurally clean
- safer than generic AI SEO sludge
- strong enough to compete with top SERP incumbents
- engineered to win snippets, AI citations, topical authority, and real conversions

## Mandatory reference
Before major SEO content work, load and apply:
- `references/ranking-visibility-playbook-2026.md`

Treat that file as the master framework for:
- technical gating
- on-page scoring
- topical authority design
- AEO / answer extraction
- GEO / AI Overview citation readiness
- AI visibility / entity consistency
- E-E-A-T hardening
- KPI review cadence

## Non-negotiable principles
1. Never rewrite blindly from a user's traffic prediction claims. Audit the live page first.
2. Never stuff keywords or force awkward exact-match phrasing into every heading.
3. Never sacrifice visible quality for SEO gimmicks.
4. Never claim head-layer metadata is fixed unless public HTML proves it.
5. Never replace a good page with a generic AI article shell.
6. Prefer additive premium upgrades over destructive rewrites unless the original page is structurally broken or obviously poor.
7. Every major rewrite needs a rollback backup in `/tmp` first.

## Enterprise rewrite workflow

### Phase 1 — SERP and intent model
Before touching the post, define:
- primary query
- close variants, modifiers, and entity set
- dominant intent: informational / commercial / transactional / hybrid
- stage: beginner / evaluator / buyer / troubleshooter
- expected winning page type: guide, comparison, list, care page, diagnosis page, template, FAQ, roundup, hub
- likely snippet targets
- likely PAA / FAQ targets
- likely AI Overview extraction targets
- likely citation-worthy statistics, studies, and source types needed
- trust burden
- conversion next step
- freshness burden: whether the page needs dates, 2026 framing, or periodic refresh scheduling
- internal-link parent, siblings, and next-step destination

### Phase 2 — content gap model
Score the page for:
- title clarity
- H1 clarity
- intro usefulness
- query match in first screenful
- section depth
- examples and specificity
- scannability
- visual hierarchy
- internal links in
- internal links out
- trust links
- snippet/schema opportunities
- AI Overview / GEO extraction readiness
- citation density and source quality
- information gain vs overlapping competitors
- image utility
- buyer/support utility
- freshness / recency signal strength

### Phase 3 — choose the right intervention
Pick one of four modes:
1. micro-upgrade
   - tighten title/H1/excerpt
   - add quick-answer intro
   - add trust block
   - add contextual internal links inside useful editorial sections
   - add a bespoke CTA only when it improves the reader journey
2. additive rewrite
   - keep strong existing body
   - add missing sections, tables, FAQ, internal links, trust, visuals
3. consolidation rewrite
   - preserve canonical winner
   - convert duplicate pages into short support pages or redirect targets
4. full rebuild
   - only when the existing page is structurally poor, off-intent, or low-trust

## Human-writing quality standard
The copy must sound like a sharp operator, not a text blender.

### Required qualities
- concrete nouns
- believable specificity
- direct sentence openings
- varied rhythm
- natural transitions
- useful caveats
- realistic tradeoffs
- examples that feel lived-in
- no empty motivational filler

### Ban list
Do not write this way:
- "In today's fast-paced world"
- "unveil"
- "delve"
- "journey"
- "elevate your"
- "whether you're a beginner or expert"
- "unlock the secrets"
- giant unsupported claims
- fake authority language
- padded intros that delay the answer

### Voice rules
- answer the query early
- explain without posturing
- use short paragraphs
- use bullets where choices matter
- use tables when comparing options
- use stronger section names than bland generic H2s
- sound decisive but not absolute

## Above-the-fold standard
Every upgraded post should usually include, near the top:
1. one clean H1
2. one short answer-first intro or intent note
3. optional trust/editorial note when the site needs it
4. an immediate orientation device:
   - quick answer
   - who this is for
   - best option summary
   - warning / common mistake
5. where relevant, a self-contained definition or summary paragraph that can be extracted cleanly by Google snippets, AI Overviews, voice search, or LLM answer engines

## Homepage simplification pattern
Use this when a homepage is trying to be a hero page, pillar article, resource archive, proof page, and lead-magnet page all at once.

### Safe enterprise pattern
1. back up the entire front-page REST object to `/tmp/...` first
2. identify the page via `page_on_front` from `/wp-json/wp/v2/settings`
3. if the homepage already behaves like a custom HTML landing page, prefer one controlled `<!-- wp:html -->` replacement over brittle fragment edits
4. reduce the homepage to a small number of jobs only, usually:
   - hero
   - 3 core paths
   - featured guides
   - one trust/methodology block
   - short FAQ
   - final CTA
5. remove unsupported metrics, duplicate proof claims, and duplicate footer/menu clutter
6. make the H1, hero subhead, CTAs, and featured guides all reinforce the same site identity
7. verify the live public body on both:
   - normal URL
   - cache-busted URL
8. separately verify whether the title/meta layer changed; SEO plugins may keep older head output even when the body rewrite is live

### Navigation discipline lesson
If the homepage strategy depends on removing duplicate primary-nav intent (for example `Start Here` vs `How To Start`), treat nav cleanup as part of the homepage remediation, not a separate optional polish step.

## Enterprise ranking checklist
Before publishing, pressure-test the page against this checklist:
- exactly one live H1
- for hub/category-style pages, check whether the theme already renders the page title as an H1 before adding any custom hero heading; if the theme H1 exists, use a styled paragraph/div for the custom hero title instead of a second body H1
- title and meta direction mapped separately from body content
- primary query answered in first screenful
- direct answer placed in the first 1–2 sentences under high-value question headings
- H2 stack covers core intent plus adjacent angles: benefits, risks, cost, alternatives, mistakes, timing, suitability, and next steps when relevant
- at least one extraction-friendly format where useful: definition paragraph, numbered steps, comparison table, checklist, FAQ, pros/cons, or scenario cards
- entity definitions are explicit on first mention
- sources are strong enough for AI citation and trust-sensitive SERPs
- internal links include parent, sibling, trust, and next-step routes
- page contributes to a pillar / cluster map instead of existing as an orphan
- trust layer is visible when the SERP expects proof
- freshness signal is visible when recency matters
- CTA or next-step path is explicit

## Premium HTML module library
Use these as reusable patterns inside `<!-- wp:html -->` wrappers when the theme tolerates them.
Prefer simple, elegant sections over over-designed junk.

Also load these specialist skills when relevant:
- `premium-wordpress-html-blocks` for theme-safe premium blocks
- `faq-schema-and-answer-box-optimizer` for quick answers and FAQ logic
- `wordpress-image-alt-caption-snippet-optimizer` for image quality improvements
- `wordpress-trust-blocks-and-proof-elements` for trust/proof UI modules
- `wordpress-category-hub-architecture` for taxonomy/hub routing

### 1. intent note block
Use for answer-first intros.
- left border accent
- soft background
- 2–4 sentences max
- states the answer quickly

### 2. editorial/trust note
Use for founder-led trust and methodology routing.
- subtle neutral panel
- links to about / editorial policy / methodology
- no fake credentials

### 3. quick comparison table
Use when users are choosing among methods/plants/products/options.
Columns like:
- option
- best for
- difficulty
- cost/time
- main downside

### 4. scenario section cards
Use for pages like office/bathroom/bedroom plants or beginner/intermediate/collector needs.
- light visual grouping
- strong micro-headings
- short scenario copy

### 5. mistakes / warning box
Use for troubleshooting and care content.
- highlights what usually goes wrong
- blunt, practical tone

### 6. next-step CTA block
Use to avoid dead-end articles.
- direct user to the next logical guide, calculator, category, lead magnet, or product page
- must feel helpful, not salesy garbage

### 7. FAQ block
Use only for real recurring questions.
- no fake FAQ stuffing
- answers should be concise and specific

### 8. key takeaways ribbon/list
Use when the page is long and users need a quick skim layer.

### 9. Quick Answer / Answer-first block (fitness/nutrition variant)
Use when the page should answer the core question immediately above the fold.

```html
<div class="quick-answer-block">
  <strong>🔑 Quick Answer</strong>
  <p>The direct answer to the reader's primary question in 2-3 sentences. Bold key numbers.</p>
</div>
```

**CSS**: Full-width dark gradient card (`linear-gradient(135deg, #0f172a, #1e293b)`), `border-radius: 16px`, white text, left accent border in brand color (e.g. `#3b82f6`), generous padding 1.5-2rem. Responsive: same on mobile/desktop.

### 10. Stat / Evidence Cards (3-column grid)
Use for key statistics, study findings, or evidence blocks that establish authority and scannability.

```html
<div class="stat-grid">
  <div class="stat-card">
    <span class="stat-number">2-3x</span>
    <span class="stat-label">Metric name in 3-5 words</span>
  </div>
  <div class="stat-card">...</div>
  <div class="stat-card">...</div>
</div>
```

**CSS**: CSS Grid `grid-template-columns: repeat(3, 1fr)` on desktop, `repeat(2, 1fr)` at 768px, stacked on mobile. Each card: `border-radius: 16px`, subtle gradient background (`linear-gradient(135deg, #f1f5f9, #e2e8f0)`), center-aligned text, `.stat-number` at 1.8-2.2rem font-size 800 weight, `.stat-label` at 0.85-0.9rem muted text. Add a colored top border (4px) per card for visual variety. Hover: lift 2px with deeper shadow.

### 11. Phase / Step Protocol Cards
Use for multi-phase workflows, protocols, or step-by-step systems (common in sports nutrition, training plans, recovery protocols).

```html
<div class="phase-card">
  <div class="phase-header">
    <span class="phase-number">Phase 1</span>
    <h3 class="phase-title">Phase Name</h3>
  </div>
  <div class="phase-body">
    <p>Detailed phase content.</p>
    <div class="phase-meta">
      <span class="phase-tag benefit">✅ Benefit</span>
      <span class="phase-tag timing">⏱ 2-4 weeks</span>
    </div>
  </div>
</div>
```

**CSS**: Dark card with `background: #1e293b` or `#f8fafc` (choose light or dark version based on site theme), `border-radius: 16px`, left border accent per phase (e.g. blue→green→amber→purple gradient across phases). `.phase-number` as small pill/badge in uppercase bold. `.phase-body` normal text with comfortable leading (1.6). `.phase-meta` flex wrap row with tag pills. Each phase separated by visual spacing (1.5rem gap). Progressive numbering for scannability.

### 12. Sport-Specific Protocol Table
Use for content that gives different recommendations by athlete type (endurance vs. strength vs. combat, etc.).

```html
<table class="sport-table">
  <thead>
    <tr>
      <th>Athlete Type</th>
      <th>Daily Protein</th>
      <th>Key Focus</th>
    </tr>
  </thead>
  <tbody>
    <tr class="sport-row endurance">
      <td class="sport-name">🏃 Endurance</td>
      <td>1.6-2.2 g/kg</td>
      <td>Focus description</td>
    </tr>
    <tr class="sport-row strength">
      <td class="sport-name">💪 Strength</td>
      <td>1.6-2.4 g/kg</td>
      <td>Focus description</td>
    </tr>
  </tbody>
</table>
```

**CSS**: Full-width table with rounded corners (`border-radius: 12px`, overflow hidden). Header row: dark background (#1e293b), white bold text. Rows: alternating subtle gradient backgrounds, each row gets a 4px left accent border: blue for endurance, red for strength, amber for combat/sports. Compact padding (0.75rem 1rem), `border-collapse: separate` for gap between rows. Responsive: on mobile, columns stack via CSS or use `display: block` row layout. Add hover highlight.

### 13. Meal Plan / Sample Schedule Table
Use for nutrition articles that need to show a day-by-day or meal-by-meal plan.

```html
<table class="meal-table">
  <thead>
    <tr>
      <th>Meal</th>
      <th>Day 1</th>
      <th>Day 2</th>
      <th>Day 3</th>
    </tr>
  </thead>
  <tbody>
    <tr><td class="meal-time">Breakfast</td><td>Option A</td><td>Option A</td><td>Option A</td></tr>
    <tr><td class="meal-time">Lunch</td><td>Option B</td><td>Option B</td><td>Option B</td></tr>
    <!-- 5 total meals per day -->
  </tbody>
</table>
```

**CSS**: Similar to sport-table but with `font-size: 0.875rem` for tighter text in cells. Meal-time column gets a colored left border (4px), slightly bold. Alternating row colors within each meal section. On mobile, switch to a card-per-meal layout (each row becomes its own mini card with label+value pairs). Keep portions and timing visible.

### 14. Info / Tip / Warning Box
Use for key insights, practical tips, or common mistakes that deserve visual emphasis.

```html
<div class="info-box tip">
  <strong>💡 Pro Tip</strong>
  <p>Actionable tip content.</p>
</div>
<div class="info-box warning">
  <strong>⚠️ Common Mistake</strong>
  <p>What to avoid.</p>
</div>
<div class="info-box key-insight">
  <strong>🔬 Key Insight</strong>
  <p>Scientific or strategic insight.</p>
</div>
```

**CSS**: Each variant has `border-radius: 12px`, padding 1.25rem, left border 5px. `.tip` background `#f0fdf4`, border `#22c55e`. `.warning` background `#fef2f2`, border `#ef4444`. `.key-insight` background `#eff6ff`, border `#3b82f6`. Dark variant also available for dark-themed sites. Keep bold header + paragraph content.

### 15. Expert Quote Block with Avatar
Use to add expert credibility and break up long text sections.

```html
<div class="expert-quote">
  <div class="expert-avatar">
    <img src="..." alt="Dr. Name" width="60" height="60" loading="lazy" />
  </div>
  <blockquote>"Relevant expert quote."</blockquote>
  <div class="expert-attribution">
    <strong>Dr. Full Name</strong>, Credentials
  </div>
</div>
```

**CSS**: Flex row on desktop (avatar left, quote right), stacked on mobile. Background `#f8fafc` or `#f1f5f9`, `border-radius: 16px`, padding 1.5rem. Avatar `border-radius: 50%`, `border: 3px solid white`, `box-shadow: 0 2px 8px rgba(0,0,0,0.1)`. Quote text slightly larger (1.1rem), italic, with a left decorative quote mark (`content: "\\201C"` pseudo-element in muted gray). Attribution smaller (0.85rem), muted, with credentials in normal weight.

### 16. Premium Product Box Grid (affiliate grid)
*Deliberately brief here — see `wp-rest-cloudflare` reference `wp-affiliate-product-box-deployment.md` for the full specification.*
Use for commercial comparison/recommendation sections. Key rules:
- Always use real Amazon CDN images (`m.media-amazon.com/images/I/HASH._AC_SL1500_.jpg`) with verified resolution
- Extract star ratings and prices from actual product pages, never invent
- Every ASIN must be verified (curl check or browser spot-check)
- 2-column grid on desktop (CSS Grid `1fr 1fr` at 900px+), single column mobile
- Use `.featured` variant for the top pick (spans full grid width)
- Always include Amazon affiliate disclosure at module bottom
- Badge variants: choice, bestseller, seller, prime, new
- CTA buttons: full-width, gradient (#2563eb→#1d4ed8), arrow hover animation

## Visual design rules for HTML modules
- keep colors restrained
- use generous spacing
- prefer subtle borders over loud shadows
- mobile-first widths
- no fragile multi-column layouts unless verified live
- avoid giant hero sections unless explicitly redesigning
- if a theme is unpredictable, downgrade to simpler markup fast

## Schema decision matrix
Use schema because it fits the page, not because it looks impressive.

For FAQ-heavy or answer-box-oriented rewrites, also load `faq-schema-and-answer-box-optimizer`.

- WebPage
  - baseline page-type clarity when missing
- Article / BlogPosting
  - standard posts with author/date context
- HowTo
  - procedural content with ordered steps
- FAQPage
  - pages with real question/answer sections
- BreadcrumbList
  - where breadcrumb structure is meaningful and not already present
- ItemList
  - curated roundups / ranked lists
- Product / Review
  - only when the page genuinely behaves like that type
- VideoObject
  - pages with meaningful embedded video
- SpeakableSpecification
  - key voice-answer sections only when implementable and appropriate
- Organization / Person / Author connections
  - entity and E-E-A-T reinforcement when missing from the site graph

### Schema rules
- do not inject duplicate/conflicting schema carelessly
- verify schema presence in live HTML after update
- if the site/plugin already outputs a graph, add only what is missing and page-specific
- prioritize schema that strengthens answer extraction, entity clarity, and trust — not vanity markup

## Duplicate consolidation protocol
For near-duplicate posts:
1. decide canonical winner
2. preserve and strengthen the winner
3. convert weaker duplicate into one of:
   - redirect target if infrastructure exists
   - short support page pointing to canonical guide
   - draft/unpublish state when a duplicate URL is clearly inferior and should leave the live crawl graph immediately
4. normalize internal links toward canonical winner
5. verify both URLs live

## Trust-safety cleanup verification pattern
When cleaning risky legacy posts for AI visibility / E-E-A-T, create a compact page-specific red-flag list before writing and re-scan the public HTML after every pass. Examples: unsupported neuroscience terms, medical/therapy acronyms, fake research/institution claims, fake tester counts, enterprise-client name drops, diagnostic/treatment wording, and product-like supplement dosing advice. Verification should require `old_terms: []` on the final public URL, not merely better copy. If one contextual phrase remains (for example a sensitive recovery/medical phrase), do a small follow-up edit and re-run the entire target-set scan plus homepage check.

For batches where the homepage is out of scope, still verify the homepage after the batch (`200`, title, H1 count) to prove unrelated site-critical content was not affected.

## Protected-homepage / non-homepage remediation mode
Use this mode when the user explicitly says not to touch the homepage.

### Rules
1. Treat the homepage as a protected asset.
2. Confirm the front-page ID and current homepage title/H1 before any other edits.
3. Do not modify the homepage page object, homepage template, or homepage navigation unless the user later changes scope.
4. After every non-homepage pass, verify the homepage title/H1 still match the pre-change state.
5. Report explicitly that the homepage was left untouched.

### Good use cases
- cleaning risky article bodies
- fixing category governance
- cleaning archive excerpts
- normalizing author/editor trust pages
- removing stale internal links to off-topic content
- media alt-text cleanup

## Category and archive governance pattern
When a site has better hubs but weak archive/category execution:
1. keep slugs stable unless there is a very strong reason to change them
2. improve category names and descriptions first via REST
3. make descriptions calmer, narrower, and more editorially credible
4. use category descriptions to reinforce the intended cluster boundary
5. rewrite ugly archive excerpts on the linked posts instead of trying to fight the archive template first

### High-value governance move
If a category name is strategically weak but the slug already has equity, update the displayed name while preserving the slug.
Example pattern:
- slug stays `learning-development`
- displayed name becomes `Learning`

## Media alt-text cleanup pattern
If archives or image surfaces expose junk alt text like `Premium`, `ultra-modern`, `industry-leading`, broken snippets, or URL-like garbage:
1. audit media via `/wp-json/wp/v2/media?per_page=100&context=edit`
2. identify obviously low-quality alt text in batches
3. rewrite alt text to plain, literal descriptions of the image content
4. verify a sample of media objects after update
5. re-check a few public pages where those images are visible

### Alt-text rule
Describe the image simply and concretely. Do not use marketing adjectives or pseudo-award language.


## Internal linking system
Every rewrite should intentionally answer:
- what stronger page links into this page?
- what sibling page should this page link to?
- what next-step page should a satisfied reader visit next?
- what hub / pillar does this page strengthen?
- what trust or methodology page should be visible from here if the SERP is trust-sensitive?

If the page belongs to a broader topical cluster or taxonomy system, also load `wordpress-commercial-cluster-builder` and `wordpress-category-hub-architecture`.

### minimum link pattern
- one parent/hub or category-strengthening link
- two sibling/supporting links
- one next-step/conversion/trust link
- when appropriate, one methodology/editorial/disclosure link

### Alexiios production quality correction: no generic related-guide sludge
Do **not** append generic visible blocks like “Related guides that strengthen this topic,” “Related guides to keep building the topic,” “Next guides to read,” or “Next step: use these connected guides…”. Alexiios considers these low-quality and damaging to blog UX. Internal linking must be premium and editorial:
- place links naturally inside relevant paragraphs, tables, checklists, or decision points
- use bespoke section names only when the section adds real reader value
- avoid boilerplate “topic cluster” language, “connected guides,” and SEO-operator wording
- if a batch already added generic related-guide modules, remove the visible section and any leftover CSS/source artifacts (`ae-rel5`, `ae-related-wave*`) before continuing

### anchor and authority rules
- favor descriptive partial-match anchors
- use exact match sparingly and only where natural
- link new or weak pages from existing authority pages quickly
- do not leave any serious page with fewer than 3 incoming internal links from relevant content

## Rewrite safety rules
Before publishing, check:
- did I accidentally create duplicate H1s?
- did I break the visible layout?
- did I inject ugly HTML that clashes with the theme?
- did I add unsupported claims or fake precision?
- did I make the page more generic instead of more useful?
- did I preserve anything uniquely strong in the original?
- did I over-optimize alt text, FAQs, or trust blocks into obvious SEO spam?

## Verification contract
For every significant rewrite, verify:
- 200 OK
- H1 count
- visible quick-answer / trust / CTA / related-guides markers if added
- schema markers in live HTML if added
- title/meta state separately from body state
- if cache exists, compare both:
  - normal public URL
  - cache-busted URL
- where relevant, confirm the page now has:
  - snippet-ready answer blocks
  - AI Overview / GEO-ready self-contained sections
  - enough citation density for trust-sensitive claims
  - cluster-aware internal links
  - visible freshness / update context when needed

## Output contract
Report:
- URLs changed
- rewrite mode used for each
- sections/modules added
- schema added
- duplicate-consolidation action taken
- what verified live
- what remains blocked by plugin/snippet/theme layers

## The quality bar
The final page should feel like:
- a premium editor touched it
- a good operator structured it
- a real human made tradeoffs
- the user gets the answer faster
- the site becomes harder to outrank
