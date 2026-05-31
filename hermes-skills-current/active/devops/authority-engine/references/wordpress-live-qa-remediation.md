# WordPress live QA remediation after Authority Engine deployments

Use this after REST-based SEO/AEO/GEO upgrades before telling the user work is complete.

## Why this exists
A live Gear Up to Grow deployment fixed content, links, trust pages, hubs, redirects, and schema, but final QA caught one remaining issue: `/about/` had **zero public H1s**. The REST page title was correct, but the theme hid the page title and an H1-cleanup step had removed the manual body H1.

## Required verification loop
1. Crawl the public site, preferably from sitemap URLs plus WP REST post/page inventory.
2. For every priority URL, fetch rendered HTML and verify:
   - HTTP 200 final response
   - exactly one visible `<h1>` with non-empty text
   - expected authority/answer block markers exist where added
   - representative posts include `Article` or `BlogPosting` schema when schema was part of the work
3. Build a de-duplicated set of internal links from crawled pages and HEAD/GET sample them.
4. Test deliberate legacy redirects with `allow_redirects=False` so 301 behavior is explicit.
5. If any issue remains, patch via REST/snippet, then re-run the same QA. Do not report completion from the pre-fix result.

## H1 pitfall: hidden theme title + body H1 cleanup
Some WordPress themes/plugins hide page titles in templates (`entry-title` disabled, transparent title areas, page builder settings, Astra/Kadence options). If an execution script removes or demotes body H1s to enforce one-H1 discipline, public pages can end up with **0 H1s**.

Repair choices:
- Preferred for individual trust/hub pages: add one manual body H1 at the top of the REST content.
- Alternative: re-enable the theme/page title if doing so preserves design.

REST repair pattern:
```python
page = session.get(f'{site}/wp-json/wp/v2/pages/{page_id}?context=edit').json()
content = page['content']['raw'] or page['content']['rendered']
content = re.sub(r'<h1\\b[^>]*>.*?</h1>\\s*', '', content, flags=re.I|re.S)
content = '<h1>About Gear Up to Grow</h1>\n' + content
session.post(f'{site}/wp-json/wp/v2/pages/{page_id}', json={
    'title': 'About Gear Up to Grow',
    'content': content,
    'status': 'publish',
})
```

Then re-run public QA and require:
- `BLANK_H1 0`
- `H1_NOT_ONE 0`
- `BAD_PAGES 0`
- `BAD_LINKS 0`

## Efficient QA output contract
Keep the user-facing result short and evidence-based:
- URL count checked
- bad pages count
- blank/missing/multiple H1 counts
- internal links checked and bad-link count
- redirect tests passed
- priority pages verified
- remaining issue found/fixed, if any

Do not paste large JSON unless asked; preserve it in a temp artifact if useful.
