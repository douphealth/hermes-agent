# MysticalDigits batch rewrite repair pattern — source section isolation, cache truth, and redirect traps

Use this when a multi-post WordPress rewrite import appears to have pasted every source section into every post, duplicated Amazon modules/TOC entries, or shows a different article on public URLs than the stored post body.

## Core lessons

- Fail closed and be terse: if the user reports catastrophic batch contamination, stop batching, repair surgically by explicit post ID, and report evidence only.
- Never rebuild from live/public rendered HTML after a bad import. Rebuild each post from the original source section only.
- Parse source files with bounded `START POST NN` / `END POST NN` markers. Verify each parsed record before writing:
  - exactly one source section per record;
  - no `START POST` in the record;
  - no `END POST` after cleaning;
  - one expected article title/H1 family;
  - one expected Amazon module if monetized.
- A broad parser like `START POST ... (?=next START|\Z)` can accidentally include the `END POST` marker and other source-file scaffolding. Prefer a bounded pattern such as `START POST (\d+) ... END POST \1`, then strip the header separator before the WordPress editor HTML.
- Use an explicit slug→post-ID map when public REST lookup is unreliable, timing out, or redirects hide the real target. Do not create new posts until slug/canonical conflicts are resolved.

## Stored-body repair checks

After XML-RPC edit, immediately `metaWeblog.getPost` the target and verify stored body, not the write response:

- `md-amazon-products == 1` for these monetized rewrites;
- no `START POST`, `END POST`, `COPY/PASTE`, or `IMAGE_URL_`;
- body `<h1>` removed if the theme emits the post title;
- no visible JSON-LD/source instructions in the body;
- Amazon placeholders replaced with real/verified image URLs or intentionally generated non-fake fallback tiles;
- affiliate links preserve `tag=papalex-20` and `rel="sponsored nofollow noopener"`.

## Public-render truth ladder

Stored XML-RPC success is not public success. Verify in this order:

1. Stored body via XML-RPC.
2. Origin public URL with `Host` header and redirects disabled (`allow_redirects=False` / `curl -I`).
3. Public apex URL with cache-busting query and compressed HTML enabled.
4. Browser desktop/mobile render after caches are cleared.

If stored body is clean but public HTML still shows repeated TOC/Amazon modules, suspect LiteSpeed/object/plugin cache or theme-generated cached output before rewriting the post again.

## Emergency public-duplication fix: strip Gutenberg comments and republish plain HTML

When public HTML contains repeated `wp:post-content` wrappers, repeated TOC blocks, or many Amazon modules even though the post should contain one article, inspect the stored body for malformed Gutenberg block comments. Bad imported `<!-- wp:* -->` / `<!-- /wp:* -->` structures can make WordPress parse/render the article as repeated blocks.

Fast recovery pattern:

1. Stop using the contaminated batch output and re-parse the original source section for each post by explicit post ID.
2. Convert to plain/classic HTML for emergency repair:
   - remove all `<!-- wp:* -->` and `<!-- /wp:* -->` comments;
   - remove body `<h1>` if the theme emits the post title;
   - strip visible source/editor labels, JSON-LD scripts, placeholder tokens, and publisher notes;
   - keep only one verified Amazon/product module per post.
3. Publish the stripped plain HTML with XML-RPC `metaWeblog.editPost`.
4. Immediately fetch `metaWeblog.getPost` and public cache-busted HTML; verify counts after stripping scripts/styles from the checked HTML.
5. Temporarily deactivate TOC/table-of-contents plugins if they amplify bad block structures into giant duplicated public output. Re-enable only after the plain HTML repair and cache purge if needed.

Use counts, not vibes: `public HTML size`, `md-amazon-products`, `<h1>` count, forbidden artifact list, and redirect target. A browser visual check should confirm one normal article flow before saying the site is fixed.

## Redirect/canonical traps

Before declaring a repaired slug live, check the public/origin HEAD response without following redirects. Some WordPress stacks redirect old slugs to different canonical posts/pages even after the target post body was fixed. If a target slug returns 301 to another URL, the repaired post may not be what users see.

Examples of traps to detect generically:

- source slug redirects to a different existing post slug;
- WordPress auto-created `-2` duplicate slug after a failed create;
- old slug self-redirects or loops;
- a post slug redirects to a page/hub, so the repaired post content is invisible publicly.

Fix redirects/canonicals before visual QA.

## LiteSpeed + Cloudflare cache notes

- Cloudflare purge-everything can succeed while LiteSpeed still serves stale duplicated HTML.
- For LiteSpeed Toolbox behind Cloudflare, origin HTTPS login with `Host: domain` may be required; HTTP origin login may not set admin cookies correctly.
- Use cookie jar on both login GET and POST, include `testcookie=1`, and access the LiteSpeed toolbox through origin HTTPS with SSL verification disabled if the origin certificate does not match the IP.
- Discover purge links/nonces from the toolbox page, but verify the purge action actually returns an authenticated success page; a 403 purge response means public verification is still unsafe.

## Compact final evidence format

For frustrated/urgent users, avoid long narrative. Report compact evidence:

- `stored fixed: N/N`
- `public clean: N/N`
- `redirect blockers: slug -> target`
- `cache blockers: Cloudflare purged yes/no, LiteSpeed purged yes/no`
- `remaining: exact next action`
