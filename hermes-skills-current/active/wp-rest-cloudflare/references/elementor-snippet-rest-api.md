# Elementor Snippet REST API Reference

Elementor Custom Code Snippets (post type `elementor_snippet`) can be fully managed via the WordPress REST API when wp-admin is blocked by Cloudflare or security plugins.

## Endpoints

| Method | Endpoint | Purpose |
|--------|----------|---------|
| GET | `/wp/v2/elementor_snippet` | List all snippets |
| GET | `/wp/v2/elementor_snippet/{id}` | Read a single snippet |
| POST | `/wp/v2/elementor_snippet` | Create a new snippet |
| PUT/PATCH | `/wp/v2/elementor_snippet/{id}` | Update a snippet |
| DELETE | `/wp/v2/elementor_snippet/{id}` | Trash a snippet |
| DELETE | `/wp/v2/elementor_snippet/{id}?force=true` | Permanently delete |

Authentication: Application Password (Basic Auth header) works for all operations.

## Key Metadata Fields

Snippet code is stored in `meta._elementor_code`. The output location is in `meta._elementor_location`.

```json
{
  "title": { "raw": "My Snippet" },
  "status": "publish",
  "meta": {
    "_elementor_location": "elementor_head",
    "_elementor_priority": 10,
    "_elementor_code": "console.log('hello');"
  }
}
```

## Available Locations

- `elementor_head` — Outputs in `<head>`. **CRITICAL: code is output as RAW TEXT — no `<script>` tags are added.**
- `elementor_body_start` — After `<body>` opens
- `elementor_body_end` — Before `</body>` closes

## ⚠️ CRITICAL PITFALL: `elementor_head` Outputs Raw Code

When a snippet is set to location `elementor_head`, Elementor outputs the `_elementor_code` value **directly as-is** — no `<script>` wrapping, no escaping, no HTML tags added.

This means:
- **If your code is `setTimeout(...)` without `<script>` tags, it renders as visible plain text** in the `<head>` which users see at the top of the page.
- **You MUST include your own `<script>` and `</script>` tags** in `_elementor_code` if you want it executed as JavaScript.
- **CSS also needs `<style>` tags** included in the code value.

**Bad (renders as visible text at top of page):**
```json
"_elementor_code": "setTimeout(function(){...},3000);"
```

**Good (properly wrapped for execution):**
```json
"_elementor_code": "<script>setTimeout(function(){...},3000);</script>"
```

## CRUD Examples

### List all snippets
```bash
curl -s -u "user:app_password" \
  "https://site.com/wp-json/wp/v2/elementor_snippet?per_page=50"
```

### Read a single snippet (including meta)
```bash
curl -s -u "user:app_password" \
  "https://site.com/wp-json/wp/v2/elementor_snippet/91004"
```

### Update snippet code (PATCH)
```bash
curl -s -X PATCH -u "user:app_password" \
  "https://site.com/wp-json/wp/v2/elementor_snippet/91004" \
  -H "Content-Type: application/json" \
  -d '{"meta": {"_elementor_code": "<script>console.log(\"fixed\");</script>"}}'
```

### Delete permanently
```bash
curl -s -X DELETE -u "user:app_password" \
  "https://site.com/wp-json/wp/v2/elementor_snippet/91004?force=true"
```

### Create a new snippet
```bash
curl -s -X POST -u "user:app_password" \
  "https://site.com/wp-json/wp/v2/elementor_snippet" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "My Custom JS",
    "status": "publish",
    "meta": {
      "_elementor_location": "elementor_body_end",
      "_elementor_priority": 10,
      "_elementor_code": "<script>console.log(\"hello\");</script>"
    }
  }'
```

## Debugging

If a snippet's output is **missing from the page**:
1. Check the snippet `status` is `publish` (not `draft` or `trash`)
2. Check if PhastPress is caching the page — append `?phast=-phast` to bypass
3. Check if the page has a CSS `display:none` rule that hides the injected element
4. View page source and search for the snippet title or code — Elementor may have rendered it but something else hid it
