# Link Audit Workflow (Homepage via REST)

When the user demands "all links working" on a WordPress site, use this multi-step workflow to detect, diagnose, and fix broken links entirely through REST API.

## Step 1: Extract All Links from Homepage

```bash
# Via curl (most reliable — gets raw HTML, bypasses browser rendering)
curl -s "https://site.com/" | grep -oP 'href="([^"]+)"' | grep -v 'facebook\|twitter\|#\|javascript\|//wp\|//fonts\|//cdn' | sort -u
```

Filter out noise: social media links, CDN fonts, WordPress API routes, fragment-only hashes, and JavaScript URIs.

## Step 2: Check Each Link for 404

```bash
for url in $(cat /tmp/links.txt); do
  code=$(curl -s -o /dev/null -w "%{http_code}" "$url" 2>&1)
  if [ "$code" != "200" ]; then
    echo "$code $url"
  fi
done
```

- `200` = working
- `301`/`302` = redirect (check where it goes with `curl -sL -o /dev/null -w "%{url_effective}" "$url"`)
- `404` = broken — needs fixing

Note that some WordPress redirects (301 to category archive) are NOT broken — they're expected and fine.

## Step 3: Find the Correct Slug for Broken URLs

When a link gives 404, the slug may have changed. Search the WordPress REST API for the correct URL:

```bash
# Search by post title (partial match)
curl -s "https://site.com/wp-json/wp/v2/posts?search=HOKA+Clifton+10&per_page=5" \
  -H "Authorization=[REDACTED] $B64" | python3 -c "
import json,sys
for p in json.load(sys.stdin):
    print(f'{p[\"id\"]} | {p[\"slug\"]} | {p[\"link\"]}')
"

# Try without the trailing -review suffix
curl -s "https://site.com/wp-json/wp/v2/posts?slug=hoka-clifton-10&per_page=5" \
  -H "Authorization=[REDACTED] $B64" | python3 -c "
import json,sys
for p in json.load(sys.stdin):
    print(f'{p[\"id\"]} | {p[\"slug\"]} | {p[\"link\"]}')
"

# Search by alternative keywords
curl -s "https://site.com/wp-json/wp/v2/posts?search=fueling+guide" \
  -H "Authorization=[REDACTED] $B64"
```

Common slug patterns that cause 404s:
- Post renamed: `hoka-clifton-10-review` → `hoka-clifton-10` (removed `-review`)
- Category archive moved: `running/shoes/` → `review/running-shoes/`
- Post path changed: `running/the-ultimate-fueling-guide-for-runners/` → `running/fueling-tips-for-every-runner/`

For category links, check category archives:
```bash
curl -s "https://site.com/wp-json/wp/v2/categories?search=shoes" \
  -H "Authorization=[REDACTED] $B64"
```

## Step 4: Fix Links in Homepage Content

Once you have the correct URLs, update the homepage page content. The homepage HTML lives in the `content.raw` field of the front page:

```python
# Get page ID from settings
page_id = ...  # from wp/v2/settings → page_on_front

# Get current content
content = get_page_content(page_id)['content']['raw']

# Apply all fixes
fixes = {
    'https://site.com/old-broken-url/': 'https://site.com/new-working-url/',
    # ... one per broken link
}
for old, new in fixes.items():
    count = content.count(old)
    if count > 0:
        content = content.replace(old, new)
        print(f"Fixed {count} occurrence(s): {old} → {new}")

# Save
save_page_content(page_id, content)
```

## Step 5: Verify All Fixes

```bash
# Check each fixed URL
for url in \
  "https://site.com/fixed-url-1/" \
  "https://site.com/fixed-url-2/"; do
  code=$(curl -s -o /dev/null -w "%{http_code}" "$url")
  echo "$code $url"
done
```

All should return `200`.

## Pitfalls

- **Homepage is a static page, not the blog archive.** The homepage URL may be a page (ID from `page_on_front`), not `/?p=1`. Always check `wp/v2/settings` → `show_on_front` and `page_on_front`.
- **PhastPress caches the old page.** Use `?nocache=$(date +%s)` when verifying.
- **301 redirects are OK** if they chain to a 200 page. Only fix 404s.
- **Duplicate fixes:** A broken URL may appear in multiple places (text links, carousel JS fallbacks, hub card links). `str.replace` catches them all.
- **`content.raw` vs `content.rendered`:** Always use `context=edit` to get `raw`. The `rendered` field has shortcodes/plugins already processed and is not directly editable.
