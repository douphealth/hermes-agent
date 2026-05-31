# Scoped Cloudflare Worker redirect when Redirect Rules are unavailable

Use when a WordPress/Cloudflare site needs one or a few exact legacy 301 redirects, but the Cloudflare Rulesets/Dynamic Redirect API is unavailable or returns authorization errors while Workers API + Worker routes are available.

## Pattern

1. Verify the old URL currently fails and the canonical target returns `200`.
2. Try the normal Redirect Rule / Rulesets path first if permitted.
3. If Rulesets are blocked but `#worker:edit` and Worker Routes are available, create a tiny route-scoped Worker rather than editing WordPress, `.htaccess`, or a broad site Worker.
4. Back up current Worker routes and any existing script with the intended name.
5. Upload a minimal module Worker that:
   - checks the host
   - normalizes the exact legacy path by trimming trailing slashes
   - redirects only the exact old slug
   - preserves query strings if desired
   - returns `fetch(request)` for anything else that matched the route unexpectedly
6. Attach the Worker only to the narrow path patterns, e.g.:
   - `example.com/review/old-slug*`
   - `www.example.com/review/old-slug*`
7. Verify with `allow_redirects=False` and then final fetch:
   - old slash and non-slash URL return `301`
   - `Location` is canonical target
   - final target is `200`
   - history is exactly `[301]`
   - query-string preservation works if relevant
   - target URL itself is still `200` with no redirect loop

## Minimal module Worker

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

## Rollback

Remove or detach the two Worker routes. The Worker script may remain dormant if no route points to it.

## Pitfalls

- Do not create a broad `example.com/*` Worker for a single redirect; route only the legacy path.
- Route patterns ending in `*` can match path variants. Keep exact-path checks inside the Worker and fall through to origin for non-exact matches.
- Preserve UTM/query strings unless there is a reason to discard them.
- Always verify final target separately to catch loops.
