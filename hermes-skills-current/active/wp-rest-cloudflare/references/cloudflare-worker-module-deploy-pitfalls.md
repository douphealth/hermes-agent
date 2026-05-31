# Cloudflare Worker module deployment pitfalls for WordPress SEO fixes

Use this when a WordPress SEO fix is implemented at the Cloudflare Worker layer, especially for homepage/hub title/meta/canonical rewrites.

## Durable lessons

- Do not force-deploy a Worker patch unless you have either:
  - the current Worker source from Cloudflare, or
  - a verified current local backup known to match the deployed route.
- Some Cloudflare API tokens can list routes and purge cache but cannot read Worker script content. A `GET /accounts/{account_id}/workers/scripts/{script}/content` call may return `405` with Cloudflare error `10405` (`Method not allowed for this authentication scheme`). Treat this as a permission/scheme limitation, not proof that the Worker is absent.
- If upload validation returns Cloudflare error `10021` with `Unexpected token 'export'`, the source is likely an ES module Worker being uploaded through the wrong/plain service-worker path or with the wrong metadata/content shape. Stop and switch to module-compatible deployment (Wrangler or Cloudflare API multipart metadata with module format) rather than stripping `export` or guessing.
- For SEO-only Worker edits, verify regression surfaces after deploy: homepage, target hub URL, sitemap/robots/AI discovery URLs, WordPress admin/login bypass behavior, canonical, title, meta description, one H1, and cache-busted URL.

## Safe sequence

1. Inventory route -> script mapping.
2. Read current source if token permits; otherwise locate the latest verified backup and confirm it represents the deployed route.
3. Patch narrowly around the exact path condition.
4. Deploy with the correct Worker type:
   - service-worker syntax: plain script upload can work.
   - ES module syntax (`export default`): use module-compatible upload.
5. Purge only affected URLs where possible.
6. Verify live public HTML and route behavior before claiming success.

## Anti-patterns

- Do not overwrite a complex apex Worker from an unverified backup.
- Do not treat a successful Cloudflare purge as evidence that a Worker upload succeeded.
- Do not continue retrying identical failed upload commands; inspect the Cloudflare error and change deployment method.