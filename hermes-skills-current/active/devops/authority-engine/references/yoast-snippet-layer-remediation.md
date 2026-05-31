<!-- Consolidated from skill: yoast-snippet-layer-remediation; original path: /home/hermes/.hermes/skills/devops/yoast-snippet-layer-remediation -->

---
name: yoast-snippet-layer-remediation
description: Diagnose and remediate split-brain WordPress metadata where body content updates succeed but Yoast or plugin-managed public title/meta output remains stale.
version: 1.0.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [yoast, seo, metadata, wordpress, snippet-layer]
    triggers: [yoast stale title, meta not updating, snippet mismatch, title mismatch]
---

# Yoast Snippet-Layer Remediation

## Purpose
Handle cases where REST title/excerpt/body updates work but the live public `<title>` and meta description remain stale.

## Diagnostic workflow
1. Fetch REST object with `context=edit`.
2. Compare:
   - `title.raw`
   - `excerpt.raw`
   - live `<title>`
   - live meta description
   - `og:title`
   - Yoast `/wp-json/yoast/v1/get_head?url=...`
3. Determine mismatch type:
   - full sync
   - body-only sync
   - og-only sync
   - title stale, description stale
   - title partial sync, description stale
4. Trigger available indexing endpoints.
5. Re-check public output.
6. If still stale, document plugin-layer blocker explicitly.

## Important rules
- Never claim metadata is fixed if only H1/body changed.
- Verify both normal and cache-busted public URLs when caches are involved.
- Compare `<title>`, meta description, and `og:title` separately.
- Save mismatch maps for evidence on larger sites.

## Remediation paths
- reindex posts
- reindex links
- reindex general indexables
- attempt writable SEO meta fields only if actually exposed
- if Yoast/plugin UI writes are impractical but runtime hooks are available, use an active Code Snippets override to force corrected title/meta on target URLs via Yoast filters
- otherwise report a true blocker and continue body-layer improvements

## Targeted single-URL Code Snippets override pattern
Use this when one rewritten page/post is live in the body layer but the public head still shows stale Yoast/plugin output.

1. Discover the target object from the public URL first (`postid-*` / `post-*` in public HTML), then re-read that exact object through REST with `context=edit`.
2. Back up the object JSON and save the snippet payload under `/tmp` before writing.
3. Create a **new active front-end Code Snippets snippet** instead of repeatedly editing a stubborn old snippet when live behavior does not change.
4. Scope the snippet narrowly:
   - hook on `wp`
   - guard with `is_singular()` and `get_queried_object_id() === <target_id>`
   - set `pre_get_document_title`, `wpseo_title`, `wpseo_metadesc`, `wpseo_opengraph_title`, `wpseo_opengraph_desc`, `wpseo_twitter_title`, `wpseo_twitter_description`, and `wpseo_canonical`
   - if schema headlines/descriptions are stale, also filter `wpseo_schema_webpage` and `wpseo_schema_article`
5. Re-read the created snippet and verify `active:true` and `code_error:null`.
6. Verify the public URL and a cache-busted URL separately for `<title>`, meta description, `og:title`, canonical, and JSON-LD headline/description if relevant.

This pattern is safer than a global override when only one page needs metadata alignment after a REST content rewrite.

## Cache split lesson
On LiteSpeed or similar acceleration stacks, a Yoast/runtime fix can be **correct on cache-busted URLs while stale on plain no-query URLs**.

Interpretation rule:
- cache-busted correct + plain URL stale = likely origin/plugin page cache issue, not failed SEO override logic
- verify after Cloudflare purge, then check origin cache behavior separately
- do not claim full live remediation until both surfaces converge, but do distinguish implementation success from cache lag in your report

## Output contract
Report:
- url-by-url mismatch state
- what reindex actions were attempted
- what synced and what stayed stale
- whether final remediation requires plugin-level or dashboard-level access
