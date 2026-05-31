# Surgical SEO Intelligence Engine

Use this reference when the user wants the Surgical Semantic SEO Editor to outperform competitors using first-party Google Search Console data, external SEO intelligence, crawl/sitemap extraction, and semantic clustering.

## Trigger

Use when the user says or implies:
- only gives a URL and expects Hermes to infer the rest
- Surgical SEO Intelligence Engine
- supercharge Surgical Semantic SEO Editor
- GSC intelligence, keyword cannibalization, striking-distance keywords, content decay, high-impression low-CTR
- DataSEO MCP / Ahrefs-style keyword research / competitor/domain comparison
- advertools crawl, sitemap analysis, image alt audit, internal link discovery
- semantic keyword/entity clustering for SEO/GEO/AEO/AI visibility

## Core operating rule

URL-only intake is the default. If the user gives only a post URL, do not ask for target keywords, audience, internal links, competitor URLs, or Yoast fields unless access is impossible or ambiguity would cause destructive edits. Discover them from live page evidence, sitemap/crawl context, GSC when available, external keyword/SERP data when available, competitor pages, and semantic clustering.

## Data priority order

1. Live rendered page and public HTML.
2. Authenticated WordPress/Yoast fields if available.
3. First-party GSC data.
4. Sitemap/crawl/internal-link data.
5. External keyword/SERP/backlink data.
6. Competitor pages.
7. Semantic clustering.
8. Clearly labeled assumptions.

## Intelligence stack

### 1. DataSEO MCP (`egebese/dataseo-mcp`)

Purpose: external keyword/SERP/competitor/backlink intelligence.

Use for:
- keyword ideas and long-tail variants
- question keywords and AI-search style queries
- keyword difficulty and SERP rows
- competitor/domain comparison
- traffic estimates and top-page insights
- backlink/source opportunities

Important controls:
- Usually configured as MCP via `uvx --python 3.10 dataseo-mcp`.
- May require `CAPSOLVER_API_KEY` or `ANTICAPTCHA_API_KEY`; optional OpenRouter for AI query generation.
- Treat KD/traffic/backlinks as third-party estimates, not first-party truth.
- Never invent search volume, keyword difficulty, rankings, backlinks, or traffic.

### 2. GSC Advanced MCP (`arturseo-geo/mcp-gsc-advanced`)

Purpose: first-party Search Console opportunity discovery.

Use for:
- page-level query analysis
- striking-distance keywords, especially positions 4-20
- high-impression low-CTR keywords
- declining queries and content decay
- keyword cannibalization
- query/page mismatch
- before/after monitoring

Important controls:
- Review code before production credentials; repo is less established than advertools/DataSEO.
- Use read-only service account access limited to needed properties.
- Do not log service-account JSON, private keys, raw credential errors, or tokens.

### 3. advertools (`eliasdabbas/advertools`)

Purpose: mature crawl/sitemap/content extraction.

Use for:
- sitemap extraction and content inventory
- robots analysis
- title/meta/H1/H2 extraction
- internal-link discovery
- image alt audits
- technical SEO diagnostics
- text/URL analysis

Fallback: if advertools is unavailable, build a dependency-light scanner that fetches the URL, parses title/meta/headings/schema/links/images, samples sitemaps, and produces a JSON brief for the editor.

### 4. Semantic clustering

Reference implementations:
- `evemilano/keyword_clustering_easy_demo`
- `iamBlogPro/KeywordClustering`
- `jfaccioli/seo-keyword-clusters`

Preferred Hermes approach:
- use SentenceTransformers/BERTopic-style clustering when available
- fall back to lightweight token/TF-IDF/intent-modifier grouping when heavy models are unavailable

Use clustering to separate:
- primary target
- secondary/support terms
- FAQ/PAA candidates
- internal-link-only terms
- competitor-only or mismatch terms
- cannibalization risks

## URL-only article workflow

1. Crawl the target URL and extract title, meta description, H1/H2/H3, schema, internal links, external links, images/alt text, answer-block hints, FAQ hints, freshness hints, Yoast/public SEO output, and word-count/term/entity signals.
2. Pull sitemap/internal-link context to identify hub/sibling/money pages, orphan risks, related posts, and contextual internal-link opportunities.
3. If GSC access exists, run page-level query analysis and classify each query as primary target, secondary support, FAQ/PAA, internal-link candidate, mismatch, or cannibalization risk.
4. If DataSEO/external data exists, gather keyword ideas, question keywords, AI-style queries, SERP/KD data, competitor pages, domain comparison, and backlink/source gaps.
5. Cluster query/keyword/entity candidates by intent and map clusters to existing/proposed H2/H3 sections.
6. Decide surgical edit scope: no-new-content polish, micro-upgrade, additive section, FAQ addition, internal-link pass, trust/source pass, image SEO pass, Yoast field pass, or full rebuild only if explicitly allowed.
7. Produce exact implementation-ready edits and always separate observed data from recommendations.

## Query/page opportunity classes

- Primary target: best intent match for the current page.
- Secondary support: can be handled naturally in a subsection.
- FAQ/PAA candidate: deserves concise answer if visible content supports it.
- Internal-link candidate: belongs to another existing page; link out instead of stuffing.
- Cannibalization risk: multiple pages compete; recommend differentiate/consolidate/canonical/noindex/internal-link routing only after evidence.
- Mismatch: query intent does not belong on this post; reject it.

## Mandatory output additions

In addition to the Surgical Semantic SEO Editor output contract, include:
- observed data sources used vs unavailable sources
- keyword and entity gap map
- query/page opportunity map
- cannibalization risks
- semantic cluster map
- internal-link opportunity map from crawl/sitemap context
- external authority/source needs
- image SEO gap map
- Yoast field recommendations
- validation checklist

## Accuracy and safety rules

- No generic SEO advice.
- No fake search volume, KD, traffic, backlinks, rankings, or AI citations.
- No unsupported claims or statistics.
- No keyword stuffing or irrelevant entities.
- No duplicate SEO plugins; do not replace Yoast.
- Prefer first-party GSC data when available.
- Prefer live crawl/SERP evidence when available.
- Always explain why each surgical edit improves SEO, GEO, AEO, AI visibility, topical authority, trust, readability, visual quality, or organic traffic potential.
