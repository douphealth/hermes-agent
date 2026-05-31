# Single-slug Cloudflare Worker redirect fallback

Use when a WordPress/SEO cleanup needs one exact old URL redirected, but the normal Cloudflare Redirect Rules / Rulesets API is unavailable or returns an authorization error while Worker permissions/routes are available.

## Pattern

1. Verify the old URL currently fails and the canonical target is healthy:
   - old URL with `allow_redirects=false` should show the current problem, often `404`.
   - target URL should return `200` and should not redirect.
2. Check Cloudflare zone/account permissions:
   - `GET /zones?name=example.com` for `zone_id` and `account.id`.
   - `GET /zones/{zone_id}/workers/routes` to see existing routes.
   - If Rulesets/Redirect Rules return `403 request is not authorized`, do not stop if Worker edit/routes are permitted.
3. Back up current Worker routes and any existing script with the intended script name.
4. Create a tiny module Worker scoped to the legacy slug only.
5. Attach route patterns only for the broken URL family, e.g.:
   - `example.com/review/old-slug*`
   - `www.example.com/review/old-slug*`
6. In the Worker, normalize only the exact legacy pathname and return `301`; otherwise `return fetch(request)` so accidental route over-match does not break nearby URLs.
7. Verify with and without trailing slash, with a sample query string, and with `www` if routed.

## Worker template

```js
export default {
  async fetch(request) {
    const url = new URL(request.url);
    if (url.hostname === "example.com" || url.hostname === "www.example.com") {
      const p = url.pathname.replace(/\/+$/, "");
      if (p === "/review/old-slug") {
        const target = new URL(request.url);
        target.hostname = "example.com";
        target.pathname = "/review/new-slug/";
        return Response.redirect(target.toString(), 301);
      }
    }
    return fetch(request);
  }
};
```

## Verification contract

Record:
- old URL status = `301`
- `Location` is the canonical target
- final URL returns `200`
- redirect history is exactly `[301]` (one-hop)
- query strings are preserved when relevant
- target URL itself still returns `200` without redirect

## Rollback

Delete or detach the two Worker routes. The Worker script can remain dormant if no route points to it.

## Pitfalls

- Do not create a broad apex Worker route for a one-URL redirect.
- Do not use a Worker that redirects every path matching a broad wildcard without an exact-path guard.
- Preserve query strings unless there is a specific SEO reason to drop them.
- Back up existing routes before creating new ones; route conflicts can silently change behavior if updated carelessly.
