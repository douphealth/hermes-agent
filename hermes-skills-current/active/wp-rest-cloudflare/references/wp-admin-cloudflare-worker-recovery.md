# WordPress Admin Recovery Behind Cloudflare Workers

Use when a WordPress site behind Cloudflare/Workers allows public pages but wp-admin cannot activate/deactivate plugins, edit posts, or save admin forms.

## Symptom pattern

- `/wp-admin/plugins.php` or `/wp-admin/post.php?...&action=edit` returns Cloudflare `403` with `cf-mitigated: challenge` and a `Just a moment...` body.
- `/wp-login.php` may also be challenged.
- After challenge removal, unauthenticated admin redirects may contain `redirect_to=https%3A%2F%2Forigin.example.com%2Fwp-admin...` instead of the apex host.
- Logged-in admin pages load, but forms/actions may still carry stale origin host links unless the Worker rewrites admin HTML/redirects safely.
- Plugin activate/deactivate clicks return a normal-looking admin page but do not change state when the Worker treats any URL containing `?s`/`&s` as public WordPress search. WordPress plugin action links often include a bare `s` query parameter, e.g. `/wp-admin/plugins.php?action=activate&plugin=...&s&_wpnonce=...`.

## Root-cause checklist

1. Check Cloudflare firewall/custom rules and legacy firewall rules for `managed_challenge` on `/wp-admin` and `/wp-login.php`.
2. Keep security blocks that are unrelated to the admin UI intact (for example XML-RPC blocks and AI crawler rules), unless the task explicitly requires them.
3. Check Cloudflare Page Rules/cache rules: `/wp-admin*` must bypass cache and disable apps where possible.
4. If a Worker proxies apex to an origin hostname, inspect Worker request headers and route selection:
   - Public WordPress proxy can fetch `https://origin.example.com` internally.
   - For wp-admin/wp-login requests, set upstream `Host` to the public apex when WordPress URL generation/cookies depend on the apex.
   - Preserve `x-forwarded-host: apex` and `x-forwarded-proto: https`.
   - Classify admin/login paths before generic search handling. Do not route `/wp-admin/*` or `/wp-login.php` to public search just because the query string has `s`; plugin action URLs can include `&s`.
5. Do not run public SEO hardening transforms on wp-admin HTML. Those transforms can add canonical headers, strip robots headers, or rewrite URLs in ways that break admin flows.

## Worker patch pattern

For WordPress admin/login requests inside an apex Worker, classify the admin path before generic public query routing:

```js
const wpAdminPath = url.pathname.startsWith('/wp-admin') || url.pathname === '/wp-login.php';
const searchRequest = !wpAdminPath && url.searchParams.has('s');
const wpAdminRequest = target === WP && wpAdminPath;
```

Do **not** use `const searchRequest = url.searchParams.has('s')` globally: plugin activation/deactivation URLs can include a bare `&s`, causing the Worker to proxy the request as public search instead of executing the admin action.

Then set apex-forwarded headers:

```js
const headers = new Headers(request.headers);
headers.set('host', target === WP ? APEX : new URL(target).host);
headers.set('x-forwarded-host', APEX);
headers.set('x-forwarded-proto', 'https');
```

When handling upstream redirects, rewrite both direct and URL-encoded origin hosts inside the `Location` header:

```js
let fixedLocation = fixed.toString()
  .replace(/https%3A%2F%2Forigin\.example\.com/gi, `https%3A%2F%2F${APEX}`)
  .replace(/http%3A%2F%2Forigin\.example\.com/gi, `https%3A%2F%2F${APEX}`)
  .replace(/https:\/\/origin\.example\.com/gi, `https://${APEX}`)
  .replace(/http:\/\/origin\.example\.com/gi, `https://${APEX}`);
newHeaders.set('location', fixedLocation);
```

For admin HTML, either leave it untouched or apply only the minimum origin-to-apex rewrite. Skip public SEO transforms:

```js
if (wpAdminRequest) {
  html = html
    .replace(/https:\/\/origin\.example\.com/gi, `https://${APEX}`)
    .replace(/http:\/\/origin\.example\.com/gi, `https://${APEX}`)
    .replace(/https%3A%2F%2Forigin\.example\.com/gi, `https%3A%2F%2F${APEX}`)
    .replace(/http%3A%2F%2Forigin\.example\.com/gi, `https%3A%2F%2F${APEX}`);
} else {
  // public SEO/canonical transforms
}
```

## Verification

Use all of these before claiming admin is fixed:

```bash
curl -sS -D - -o /tmp/wp-login.html https://example.com/wp-login.php | sed -n '1,25p'
curl -sS -D - -o /tmp/plugins.html https://example.com/wp-admin/plugins.php | sed -n '1,25p'
```

Expected unauthenticated behavior:

- `/wp-login.php`: `200`, WordPress login page, no `cf-mitigated: challenge`.
- `/wp-admin/plugins.php`: `302` to apex `/wp-login.php?redirect_to=https%3A%2F%2Fexample.com%2Fwp-admin%2Fplugins.php...`, not origin.

Then test with a real admin cookie/session:

- `/wp-admin/plugins.php` returns `200` and contains plugin nonces/actions.
- The plugin page source has `origin.example.com` count `0`; specifically check the admin canonical link and `wp.apiFetch.createRootURLMiddleware(...)` root.
- Activate and then deactivate one harmless inactive plugin to prove action URLs execute. A safe verification plugin is one that does not alter frontend output materially (for example Query Monitor if dependencies are satisfied, or Disable Comments only if you immediately deactivate it afterward). Expected notices: `Plugin activated` then `Plugin deactivated`, with no origin host in the final URL/body.
- `/wp-admin/edit.php` returns `200`.
- `/wp-admin/post-new.php` returns `200`.
- An existing real post edit URL returns `200` and loads the block/classic editor.
- No `Just a moment...` body.
- No `href=` or `action=` attributes point to the origin host.
- Public routes still work, especially any Worker app proxies and sitemap routes.

## Pitfalls

- Fixing the Cloudflare challenge alone may not fix admin if WordPress still builds `redirect_to` with the origin host.
- Bare `&s` on `/wp-admin/plugins.php` is not a public search request. If plugin activation/deactivation silently fails while pages still load, inspect Worker query routing before blaming WordPress permissions or cache.
- Rewriting visible text that mentions the origin host in plugin notices is not necessarily required. Focus on `href=`, `action=`, redirect locations, REST/AJAX endpoints, and editor assets.
- Do not 301 the origin host if the Worker still uses it as WordPress upstream; use public noindex/containment plus Worker bypass logic instead.
