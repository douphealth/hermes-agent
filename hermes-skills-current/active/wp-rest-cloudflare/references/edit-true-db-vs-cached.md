# `?edit=true` — GET Actual DB Content vs Cached Rendered

## The Problem

On PhastPress-cached WordPress sites, the public REST API endpoint returns **cached/rendered** content (passed through `the_content` filter). This cached version may be hours or days stale — your recent DB edits won't show.

## The Fix: `?edit=true`

Appending `?edit=true` to any WordPress REST API GET request returns the **actual database content** (raw, unfiltered):

```bash
# Returns cached/rendered — may be stale
curl -s -u "user:app_password" "https://site.com/wp-json/wp/v2/posts/123"

# Returns actual DB content — always fresh
curl -s -u "user:app_password" "https://site.com/wp-json/wp/v2/posts/123?edit=true"
```

## When to Use

- **Reading post content for modification** — ensure you're editing the actual current version
- **Verifying updates persisted** — confirm your POST/PUT write took effect
- **Debugging "my CSS isn't showing" issues** — check if the CSS is in the DB even if the cached page doesn't show it
- **Comparing DB vs rendered** — detect if a plugin/cache layer is transforming your content

## Requirements

- Requires authentication with `edit_posts` capability
- `content.raw` field is exposed when the user has edit permissions (not available without `?edit=true`)
- `content.rendered` at `?edit=true` may differ from the public `content.rendered` due to caching

## Example: Post Content Length Comparison

```python
import json, requests, base64

auth = base64.b64encode(b'admin:app_password').decode()
headers = {"Authorization": f"Basic {auth}"}

# Cached version
resp1 = requests.get("https://site.com/wp-json/wp/v2/posts/123", headers=headers)
d1 = resp1.json()

# DB version
resp2 = requests.get("https://site.com/wp-json/wp/v2/posts/123?edit=true", headers=headers)
d2 = resp2.json()

print(f"Cached: {len(d1['content']['rendered'])} bytes")
print(f"DB:     {len(d2['content']['rendered'])} bytes")
```

If lengths differ, the public endpoint is serving a cached version.
