# CSS Pitfalls in WordPress REST API Content

## `@media` Queries Get Stripped from `<style>` Blocks in Post Content

**The problem:** When you save post content via REST API with `<style>` blocks containing `@media` queries, WordPress's content sanitization (`wp_filter_post_kses`) strips the `@media` keyword and emits the remaining CSS rules as **visible text outside the `<style>` tag**.

### What happens step by step

1. You POST: `<style>@media (max-width: 768px) { .foo { color: red; } }</style>`
2. WordPress stores in DB (`edit=true`): Looks clean — the `<style>` tag and `@media` are intact
3. WordPress RENDERS (public endpoint): `<style></style><p>@media (max-width: 768px) { .foo { color: red; } }</p>`

The CSS rules are now **visible text** on the page because:
- `wp_kses` allows `<style>` tags but doesn't preserve their content as CSS
- The `@media` keyword gets treated as plain text
- WordPress auto-p wraps the text in `<p>` tags
- The CSS rules survive as text nodes

### Detection Script

Run this after any REST API post update that includes CSS:

```bash
curl -s -u "user:app_password" "https://site.com/wp-json/wp/v2/posts/ID" \
  | python3 -c "
import sys,json,re
d=json.load(sys.stdin)
c=d['content']['rendered']
text_only = re.sub(r'<style>.*?</style>', '', c, flags=re.DOTALL)
if 'max-width' in text_only or '!important' in text_only:
    print('❌ CSS is visible text outside <style> tags')
    for m in re.finditer(r'[^.<]{0,30}(?:max-width|!important)[^<]{0,60}', text_only):
        print(f'   {m.group().strip()[:80]}')
else:
    print('✅ No visible CSS outside style blocks')
```

### Workarounds

| Method | How | Pros | Cons |
|--------|-----|------|------|
| **`wp_head` injection** | Add CSS via functions.php `add_action('wp_head')` | No content sanitization; works everywhere | Requires theme file access |
| **Elementor Snippet** | Create snippet at `elementor_head` location via REST API | No post content filter; survives theme updates | Limited to Elementor sites |
| **Insert Headers and Footers** | Plugin with dedicated code injection area | Simple UI; no filters | Requires plugin + admin session |
| **Mobile-first CSS without `@media`** | Default styles are mobile layout; add `min-width` overrides | Works inside post content | Only for simple layouts |
| **Direct theme file edit** | Edit style.css via WP File Manager or theme editor | Full CSS support | Requires writable theme |
| **Inline styles on elements** | `style="width:100%"` on HTML elements | Survives all filters | Messy; poor maintainability |

### Key Insight

The `edit=true` endpoint **will show the CSS correctly** (it returns raw DB content), while the public endpoint **will show broken CSS**. Always check BOTH endpoints before confirming a fix:

```bash
# Check public (may be broken)
curl -s -u "user:pass" "https://site.com/wp-json/wp/v2/posts/ID" \
  | python3 -c "import sys,json,re; c=json.load(sys.stdin)['content']['rendered']; s=re.sub(r'<style>.*?</style>','',c,flags=re.DOTALL); print('BROKEN' if '!important' in s else 'OK')"

# Check DB (usually clean)
curl -s -u "user:pass" "https://site.com/wp-json/wp/v2/posts/ID?edit=true" \
  | python3 -c "import sys,json,re; c=json.load(sys.stdin)['content']['rendered']; s=re.sub(r'<style>.*?</style>','',c,flags=re.DOTALL); print('BROKEN' if '!important' in s else 'OK')"
```

## `edit=true` vs Regular Content Discrepancy

This is the companion pitfall to the `@media` issue. The standard `/wp/v2/posts/ID` endpoint returns content passed through `the_content` filter — which includes PhastPress processing, auto-p (adding `<p>` tags), shortcode expansion, and any other content filters. The `/wp/v2/posts/ID?edit=true` endpoint returns raw `post_content` from the database.

**When lengths diverge significantly**, PhastPress or another filter is transforming the content. Always check `edit=true` first when debugging content issues, because that's what you actually stored.

## App Password Credentials Mismatch

The secrets file (`/home/hermes/.secrets/alexiios-websites-credentials.txt`) has TWO sections per site:

```
[WP-Admin Credentials]        ← for wp-login.php / origin IP
site.com|username|password

[REST API Passwords]          ← for REST API calls
site.com|username|app_password
```

These may use different usernames and passwords. `rest_cannot_edit` or `rest_not_logged_in` when writing via REST API = wrong app password. Always verify against BOTH sections.

**Example from real site (gearuptofit.com):**
```
[WP-Admin]
gearuptofit.com|admin|99d(J@%aVil@$dbkkv!ke8Fd

[REST API]
gearuptofit.com|admin|K7k7 EHZT mOtf ae5C 0XeL zieo
```

Note: Same username (`admin`) but completely different password strings. The REST API call uses the APPLICATION PASSWORD, not the wp-admin login password.
