# WordPress SEO/GEO/AEO Implementation Sprint Pattern

Use after a full audit has already generated URL-level action artifacts and the user explicitly says to proceed from artifacts rather than re-auditing.

## Trigger
- User provides or references: `url_action_table.csv`, `cannibalization_map.csv`, `internal_linking_blueprint.csv`, `top_20_refresh_briefs.json`, claims cleanup files, review trust standards, or a 30-day backlog.
- User asks for implementation batches: cannibalization cleanup, top refreshes, internal linking, claim cleanup, review hardening, hub reinforcement.

## Source-of-truth rule
Do not rerun a full site crawl unless needed for a specific URL before editing. Load the existing artifacts and operate from them. Only live-check URLs being edited or redirected.

## Safe execution sequence
1. **Load artifacts first**: parse URL actions, cannibalization groups, link blueprint, refresh briefs, and claim-risk files into local CSV/JSON outputs.
2. **Confirm write path**: for WordPress behind Cloudflare, prefer XML-RPC/origin-IP with `Host: domain` when REST write is blocked or sanitizes HTML. Retrieve secrets only from the local secrets file; never store or print them.
3. **Back up before edit**: save each post/page exact title/content/custom fields to `/tmp/...` before `metaWeblog.editPost` or REST update.
4. **Batch commercial refreshes first**: top review/tool pages usually produce the fastest trust + conversion + AI-extraction lift.
5. **Use additive modules**: prepend/insert sprint modules rather than replacing whole articles unless the brief explicitly calls for a rebuild.
6. **Purge cache once per batch**: after writes, purge Cloudflare/site cache, then QA cache-busted and normal public URLs.
7. **Emit machine-readable changelogs**: JSON/CSV with URL, post ID, old/new titles, quick answer, claims changed, backup path, QA status.

## Cannibalization cleanup rules
- Treat `MERGE_OR_301` as a candidate, not permission to destroy.
- Confirm the primary URL and preserve unique useful sections before any redirect.
- Do not blindly redirect program/platform-specific pages such as Amazon, ClickBank, Shopify, Pinterest, Instagram, dropshipping, or tool-specific posts when they can become narrower supporting pages.
- Use `KEEP_AS_SUPPORTING` when the competing URL has unique intent; add a contextual link to the primary and narrow its intro/title in a later refresh.
- Use `MERGE_INTO_PRIMARY_THEN_301` only after copying useful examples, checklists, tables, FAQs, or proof sections into the primary.
- Keep redirects/noindex as a ready map until preservation and QA are complete.

## Commercial review/tool refresh module
For each priority review/tool page, add a visible top module containing:
- 45–75 word query-specific Quick Answer
- Best for / Not best for
- Pricing/date checked
- How we evaluated this:
  - Reviewed by
  - Last checked
  - Product or plan checked
  - Pricing checked
  - Features evaluated
  - Best for
  - Not best for
  - Alternatives considered
  - Affiliate relationship
  - Evidence used
- Alternatives
- Sources and verification
- Affiliate disclosure before commercial CTAs
- Contextual internal links to parent hub, review/tools hub, methodology/disclosure, and two sibling pages
- FAQ only when the questions are visible on the page

Avoid fake ratings, hidden schema, or unsupported “tested/best” claims. Recommend Review/FAQ/Article/Breadcrumb schema only where visible content supports it.

## Claim cleanup rules
Process high-risk claims before cosmetic copy:
- revenue/month, ROI, conversion uplift, traffic growth, rankings, open rates
- “tested X tools”, “best” claims, benchmark claims, pricing/model details

Actions:
- `PROVED`: keep only with visible source/proof and last-checked date.
- `REWRITTEN`: convert to scenario, illustrative wording, or softer fit language.
- `REMOVED`: delete misleading/unverifiable copy.

Do not use broad runtime regex filters for affiliate/link/claim cleanup. They can collapse long post bodies while returning HTTP 200. Use offline batch edits or targeted XML-RPC/REST writes with backups.

## Metadata caveat
SEO plugins and performance/header optimizers may duplicate or override meta tags after XML-RPC title/content edits. Verify `<title>`, meta description, canonical, robots, H1, and visible body separately. If meta fields do not update via custom fields, use the site’s SEO plugin API/options or a narrowly scoped output-buffer override only for the edited URLs, then verify there are not conflicting duplicate descriptions.

## Final QA before reporting ready for GSC
For every changed URL verify:
- HTTP 200
- self-canonical if indexable
- intended `index, follow`
- exactly one visible H1
- title/meta updated or known blocker documented
- Quick Answer present
- no visible shortcode/prompt/editor residue
- no unsupported high-risk claim residue
- sources/verification present
- trust module present for review/tool/commercial pages
- affiliate disclosure before CTA where needed
- internal links to hub + sibling pages present
- schema only if visible content supports it
- URL remains in sitemap if intended to rank

Do not submit to Google Search Console until this QA passes. Report URLs ready vs not ready and why.