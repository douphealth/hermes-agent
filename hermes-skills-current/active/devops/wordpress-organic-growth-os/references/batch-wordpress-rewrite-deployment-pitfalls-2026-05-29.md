# Batch WordPress Rewrite Deployment Pitfalls — 2026-05-29

Use this when applying user-supplied rewritten blog posts across Alexiios-managed WordPress sites.

## Durable lessons

### 1. Public QA outranks API success
A post can update successfully through XML-RPC/REST while the public page still fails content QA because of theme filters, cache, legacy SEO injectors, or escaped scripts. Always verify cache-busted public URLs after Cloudflare purge.

### 2. Remove JSON-LD from imported post bodies unless the site is known-safe
Some WordPress stacks escape `<script type="application/ld+json">` from imported content into visible text (`@context`, `schema.org`, `<br />`, curly quotes). Treat visible schema leakage as a publish blocker. Prefer plugin/theme-generated schema or separately tested head injection; never leave JSON-LD inside body content if it renders visibly.

### 3. H1 handling is site/theme-specific
Default: remove body `<h1>` from imported content to avoid duplicate H1s when the theme renders the post title.

But verify live output. Some imported/legacy templates suppress the theme H1 and/or demote body H1s through filters. If public QA shows `0` H1 after update:
- inspect rendered HTML around the custom article wrapper;
- if body H1s are demoted/stripped, use a visible accessible primary heading such as `<div class="..." role="heading">Title</div>` or another site-safe heading pattern;
- count one effective primary heading in QA only after verifying visible output.

### 4. MU-plugin head fixes are high-risk without out-of-band rollback
Do not deploy a new MU plugin to normalize titles/meta/head output unless you have already verified syntax and have an out-of-band rollback path (SSH, hosting file manager, panel terminal, FTP). A fatal in `wp-content/mu-plugins/*.php` loads before `wp-admin/admin-ajax.php`, so WordPress File Manager AJAX rollback may also be blocked by the fatal.

Safer order for stale public `<title>`/meta:
1. Patch known SEO meta families via XML-RPC/REST custom fields.
2. Purge Cloudflare and local cache.
3. Recheck live head.
4. If still stale, report a head-layer/cache/template caveat or use a tested plugin/theme route with rollback ready.
5. Only use MU-plugin surgery when rollback access is proven.

### 5. Exact deployment pattern that worked
- Parse source file into target URL, slug, title/H1, meta title, meta description, raw HTML.
- Lookup existing post IDs via public REST when authenticated edit context is unreliable.
- Backup original post bodies and metadata locally before edits.
- Use XML-RPC for rich raw HTML writes when REST risks stripping `<style>` or premium markup.
- Sanitize before write: remove publisher/editorial notes, media placeholders, unapproved dynamic embeds, duplicate H1s, escaped/visible schema risks, and self-referential rewrite language.
- Preserve required disclosures and affiliate tags.
- Purge Cloudflare after writes.
- Verify every public URL: 200, no critical error, canonical, one effective primary heading, premium wrapper present, disclosure/tag present, no raw CSS/schema/artifact leakage.

## QA fields to capture in scripts
For each URL capture:
- status code
- CF-Cache-Status
- canonical match
- public `<title>` caveat if stale
- H1 count + accessible heading fallback count
- custom article wrapper present
- affiliate disclosure and tag present when applicable
- raw CSS leakage
- visible schema leakage
- editorial/publisher artifact leakage
- WordPress critical error/500 marker
