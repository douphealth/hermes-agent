# Editing Full-HTML Custom Pages via REST

When a WordPress homepage is built as a **page** (not a template) containing all HTML/CSS/JS inside `<!-- wp:html -->` blocks, the entire page can be edited by updating the page content via `wp/v2/pages/{ID}`.

## Find the Homepage Page ID

The homepage page ID is stored in WordPress settings:

```bash
curl -s "https://site.com/wp-json/wp/v2/settings" \
  -H "Authorization=[REDACTED] $B64" | python3 -c "
import json,sys; d=json.load(sys.stdin)
print('Front page:', d.get('page_on_front'))
print('Posts page:', d.get('page_for_posts'))
"
```

Alternatively, list all pages and find the one being used as front:

```bash
curl -s "https://site.com/wp-json/wp/v2/pages?per_page=100" \
  -H "Authorization=[REDACTED] $B64" | python3 -c "
import json,sys
pages = json.load(sys.stdin)
for p in pages:
    print(f\"{p['id']}: {p['title']['rendered']} ({p['slug']})\")
"
```

## Read Current Page Content

```bash
curl -s "https://site.com/wp-json/wp/v2/pages/{ID}?context=edit" \
  -H "Authorization=[REDACTED] $B64" | python3 -c "
import json,sys
d = json.load(sys.stdin)
raw = d['content']['raw']
print(f'Length: {len(raw)} chars')
print('First 300:', raw[:300])
print('Last 300:', raw[-300:])
"
```

The `raw` field contains the **full unrendered HTML** including `<style>` blocks, `<script>` blocks, and any custom markup wrapped in `<!-- wp:html --> ... <!-- /wp:html -->`.

## Update Page Content

Use Python for large content updates (avoids shell escaping issues with complex HTML/JS):

```python
import json, urllib.request, base64

creds = base64.b64encode(b'username:application_password').decode()

# Get current content
req = urllib.request.Request('https://site.com/wp-json/wp/v2/pages/{ID}?context=edit')
req.add_header('Authorization', f'Basic {creds}')
resp = urllib.request.urlopen(req)
data = json.loads(resp.read())
content = data['content']['raw']

# Modify the content (e.g., inject CSS before closing </style>)
idx = content.rfind('</style>')
new_css = '.my-class { color: red !important; }'
new_content = content[:idx] + new_css + '\n' + content[idx:]

# POST the updated content
payload = json.dumps({'content': new_content}).encode()
req2 = urllib.request.Request('https://site.com/wp-json/wp/v2/pages/{ID}',
    data=payload, method='POST')
req2.add_header('Authorization', f'Basic {creds}')
req2.add_header('Content-Type', 'application/json')
resp2 = urllib.request.urlopen(req2)
result = json.loads(resp2.read())
print('Status:', result.get('status'))
```

## Pitfalls

### CSS inserted outside the `<style>` block renders as text
If you insert CSS **after** `</style>` instead of **before** it, WordPress renders it as visible text on the page. Always insert at `content[:idx]` where `idx = content.rfind('</style>')` (before the closing tag).

### Content must not be empty or truncated
The full 60K+ character content must be sent back. If you accidentally post an empty string or read-only field, you'll wipe the entire page. **Always read the content first, modify it programmatically, and post the modified version.**

### PhastPress caching
Append `?nocache=1` or `?phast=-phast` when verifying page changes. PhastPress caches aggressively — you'll see the old page even after a successful update.

### Content stored in `content.raw`, not `content.rendered`
The `rendered` field contains the processed HTML with shortcodes expanded and blocks rendered. The `raw` field (only available with `context=edit`) contains the unprocessed editor content. **Always edit `raw`.**

## Adding New Sections or Cards to the Homepage

To add new tool cards, feature badges, or content sections:

### Step 1: Find insertion point
Identify a unique string in the HTML that marks where the new content goes (e.g. the closing `</article>\n      </div>` of the last card in a grid).

### Step 2: Build the new HTML block
```python
new_card = '''
        <article class="g-tcard g-rv" data-d="4">
          <div class="g-tic">🤖</div>
          <h3>Shoe Match</h3>
          <p>Description of the new tool.</p>
          <a class="g-btn g-btn-pri" href="https://site.com/tool-url/">Action →</a>
        </article>'''
```

### Step 3: Insert before the closing tag
```python
insert_point = '        </article>\n      </div>\n    </div>\n  </section>'
content = content.replace(insert_point, new_card + '\n' + insert_point)
```

### Step 4: Update grid CSS if adding items
If the grid had a fixed column count (e.g. `grid-template-columns: repeat(3, 1fr)`), update it to accommodate the new count:
```python
import re
content = re.sub(r'(grid-template-columns:repeat\()(3)(,1fr\))', r'\g<1>5\g<3>', content)
```

## Adding Images

Find suitable images from the media gallery:
```bash
curl -s "https://site.com/wp-json/wp/v2/media?per_page=30&media_type=image" \
  -H "Authorization=[REDACTED] $B64" | python3 -c "
import json,sys
for m in json.load(sys.stdin):
    w = m.get('media_details',{}).get('width',0)
    if w >= 500 and w <= 2000:
        print(f'{m[\"id\"]}: {m[\"title\"][\"rendered\"][:50]} | {w}x{m.get(\"media_details\",{}).get(\"height\",0)}')
"
```

Insert images as an image grid below the About section or Start Here section:
```python
images_grid = '''
<div style="display:grid;grid-template-columns:1fr 1fr;gap:20px;margin-top:32px;border-radius:18px;overflow:hidden">
  <img src="IMAGE_URL_1" alt="Alt text" style="width:100%;height:280px;object-fit:cover" loading="lazy">
  <img src="IMAGE_URL_2" alt="Alt text" style="width:100%;height:280px;object-fit:cover" loading="lazy">
</div>'''
```

Insert images block between the entity section and the next section (Start Here / Latest Posts).

## Typical Use Cases

- Inject CSS to fix reveal animations broken by PhastPress JS defer
- Add/remove style blocks for homepage sections
- Update hardcoded content sections
- Fix JavaScript that references deprecated model IDs
- Override theme CSS constraints for full-width layouts
