# WordPress Affiliate Product Box Deployment via REST

Use this pattern when adding affiliate recommendations to WordPress articles where wp-admin may be blocked by Cloudflare.

## Production pattern
1. Verify or reuse only real affiliate/deep links already known to be valid. Do not publish dashboard/login URLs or invented URLs.
2. Map products to articles by topical intent, not by commission opportunity. Keep modules focused (usually 3-4 products) and avoid sitewide stuffing.
3. Back up each target REST object before writing: full JSON with `context=edit`.
4. Insert one scoped `<!-- wp:html -->` block near the start of the article, preferably before the first meaningful `<h2>` after the intro.
5. Scope all CSS to a unique wrapper class such as `.amfs-affiliate-product-box-v1`; avoid global theme changes.
6. Each CTA should use `target="_blank"` and `rel="sponsored nofollow noopener"`.
7. Include a visible affiliate disclosure inside the module.
8. Update through REST with `POST` + `X-HTTP-Method-Override: PUT` to bypass WAF issues.

## ⚠️ CRITICAL: Verify Amazon Links Work Before Publishing

**Never publish `amzn.to` shortlinks without resolving them first.** Broken Amazon shortlinks are the most common quality failure — they silently redirect to the Amazon homepage instead of a specific product, which means users see an irrelevant search page and earn zero commissions.

### 🔴 MANDATORY: Verify the Affiliate Tag Before Building Any Links

**This is the #1 cause of user frustration.** Do not assume the affiliate tag — verify it explicitly:

1. Check memory: `papalex-20` is confirmed for gearuptofit.com
2. Check the site secrets file: `/home/hermes/.secrets/alexiios-websites-credentials.txt` may contain the tag
3. If uncertain: ASK THE USER before writing a single link

Wrong tag examples (production failures):
- ❌ Used `gearuptofit-20` when real tag is `papalex-20` → **every single link wrong, user furious**
- ✅ Ask first, or look up the confirmed tag from memory

### 🔴 MANDATORY: Verify Every ASIN Resolves to a Real Product

**ASINs can go 404.** Do not deploy links to products that no longer exist. Verified broken ASINs from production:
- ❌ `B00X25R2CC` (Ovasitol by Theralogix) → **Page Not Found** — replaced with `B0C1G3ZN6W` (Wholesome Story Myo-Inositol)
- ❌ `B00004ZBM3` (OXO Good Grips Cookie Scoop) → **Page Not Found** — replaced with `B0DF78YQGW` (new listing)

**Verification flow:**
1. Try `curl -sI "https://www.amazon.com/dp/ASIN?tag=YOURTAG"` — if it returns 503/blocked, that's OK (Amazon bot detection)
2. If CPU returns 404 (`Page Not Found`) or redirects to homepage, the ASIN is **DEAD** — find a replacement
3. For 503/blocked: verify with browser (navigate to the ASIN URL)
4. Before deploying to 20+ pages, spot-check 2-3 ASINs in browser to confirm they load products

### Required link verification flow

1. **Resolve every `amzn.to` shortlink** before including it:
   ```bash
   curl -sI -L --max-redirs 3 "https://amzn.to/YOURCODE"
   ```
   If the final destination is `https://www.amazon.com/` (homepage), the link is **dead** — do not use it. The correct destination should be something like `https://www.amazon.com/dp/ASIN...`.

2. **Prefer direct `amazon.com/dp/ASIN` URLs over shortlinks**:
   ```text
   ✅ https://www.amazon.com/dp/B0019LRYK8?tag=gearuptofit-20
   ❌ https://amzn.to/4jRnvHp
   ```
   Direct ASIN URLs do not expire, are verifiable ahead of time, and work with your affiliate tag appended.

3. **Use real product data** — never invent ratings, review counts, or prices:
   - Extract the real star rating and review count from the Amazon product page
   - Format: `4.5/5 — 5,578 ratings`
   - Include an inline link to reviews: `amazon.com/dp/ASIN#customerReviews`

4. **Use real images from Amazon CDN**:
   - Image URL pattern: `https://m.media-amazon.com/images/I/XXXX._AC_SX522_.jpg`
   - Extract from the product page via browser automation
   - Set `loading="lazy"` and `object-fit:contain`
   - Do NOT use generic/placeholder images or WordPress media library uploads

5. **Verify with browser** when Amazon blocks curl:
   - Amazon may return `503` or bot detection to CLI requests
   - If curl gets blocked, open the product page in Playwright/browser automation and verify the link renders properly
   - Check that the product name, image, and price button load

### Amazon link failure signatures

| Symptom | Cause | Action |
|---|---|---|
| `amzn.to` redirects to `www.amazon.com/` | Dead/expired shortlink | Replace with correct `amazon.com/dp/ASIN` link |
| `amazon.com/dp/ASIN` returns `Page Not Found` | Wrong ASIN | Re-verify ASIN on actual product page |
| curl returns `503` but browser works | Amazon bot detection | Verify with browser, trust browser result |
| Product image missing / broken | Hotlink blocked or wrong URL | Use `m.media-amazon.com/images/` URLs |

### Verify every product image actually loads

After deploying, check the image-to-link ratio and verify images resolve:

```bash
# Check image-to-link ratio on each page
links=$(curl -sS "https://site.com/page/" | grep -coP 'amazon\.com/dp/[A-Z0-9]+')
imgs=$(curl -sS "https://site.com/page/" | grep -coP 'm\.media-amazon\.com/images/I/[^"\'\\s]+')
echo "links:$links images:$imgs"  # Must be equal (1:1)
```

**Production failures:**
- ❌ Fabricating image URLs from the ASIN — each product has a unique CDN hash like `71tWTWashCL` that must be extracted from the actual Amazon product page
- ❌ Using `_SX522_` instead of `_AC_SL1500_` for Retina display quality
- ❌ Image URL looks correct but returns 404 (wrong CDN path hash)

**Correct URL format:** `https://m.media-amazon.com/images/I/<UNIQUE_HASH>._AC_SL1500_.jpg`

**Safe extraction:** Navigate to the product page in browser, find the main product image in `#landingImage` or `.imgTagWrapper img`, extract the `m.media-amazon.com/...` URL exactly as-is.

### Real example (from production failure)
- ❌ Old: `amzn.to/4jRnvHp` → redirects to `www.amazon.com/` (homepage)
- ✅ New: `https://www.amazon.com/dp/B0019LRYK8?tag=gearuptofit-20` → NOW Foods EGCg Green Tea Extract product page
- ✅ Real image: `https://m.media-amazon.com/images/I/71PCPDH3LtL._AC_SX522_.jpg`
- ✅ Real rating: `4.5/5 — 5,578 ratings`

## Premium product box CSS architecture

For enterprise-grade product boxes, use a comprehensive component system instead of simple bordered cards:

### Component class hierarchy
```
.gutf-products                     → CSS Grid or flex wrapper (2-col on 900px+, 1-col mobile)
.gutf-product-card                 → Individual card: 24px radius, glass-white, hover lift 4px
.gutf-product-card.featured        → Featured card: spans full grid width on desktop
.gutf-product-badge                → Ribbon badge (top-left): gradient bg, uppercase, drop shadow
.gutf-product-image-wrap           → 1:1 aspect-ratio image container: soft gradient bg, inner shadow
.gutf-product-image-wrap img       → object-fit:contain, hover scale(1.06)
.gutf-product-info                 → Flex column for text content
.gutf-product-title                → Font-weight 800, dark slate
.gutf-stars                        → Inline flex for star ratings
.gutf-star                         → Gold (#f59e0b), with .empty variant for unrated
.gutf-rating-number                → Bold numeric rating text
.gutf-rating-count                 → Muted gray (#64748b)
.gutf-price-row                    → Flex row: current price + pills
.gutf-price-current                → Large bold price (1.3rem, 800 weight)
.gutf-pills                        → Flex wrap container for mini badges
.gutf-pill                         → Mini badge with variants: .choice, .seller, .prime, .bestseller
.gutf-cta-btn                      → Gradient button: full-width, arrow-animated on hover
.gutf-cta-arrow                    → Animated inline arrow (translateX on hover)
.gutf-disclosure                   → Italic small text, Amazon affiliate disclosure
```

### High-res Amazon images
Use `_AC_SL1500_` suffix for Retina-quality product images instead of `_AC_SX522_`:

```html
✅ High-res: https://m.media-amazon.com/images/I/71PCPDH3LtL._AC_SL1500_.jpg
❌ Standard: https://m.media-amazon.com/images/I/71PCPDH3LtL._AC_SX522_.jpg
```

The SL1500 variant provides 1500px resolution images that look pristine on Retina/Mac displays, while SX522 only provides 522px.

### Responsive grid pattern
```css
/* Mobile: stacked single column */
.gutf-products { display: flex; flex-direction: column; gap: 1.5rem; }

/* Tablet 640px+: side-by-side image + info within each card */
@media(min-width:640px) {
  .gutf-product-card { grid-template-columns: 180px 1fr; padding: 1.75rem; }
}

/* Desktop 900px+: 2-column grid, featured card spans full width */
@media(min-width:900px) {
  .gutf-products { display: grid; grid-template-columns: 1fr 1fr; }
  .gutf-product-card.featured { grid-column: 1 / -1; grid-template-columns: 200px 1fr; }
}
```

### Key CSS properties for premium feel
- `border-radius: 24px` on cards, `16px` on image wraps
- `box-shadow: 0 1px 3px rgba(0,0,0,0.06), 0 4px 12px rgba(0,0,0,0.04)` (subtle layered shadow)
- `transition: transform 0.3s cubic-bezier(0.34,1.56,0.64,1)` (spring-like hover)
- `background: linear-gradient(135deg, #f8fafc, #f1f5f9)` for image wrap backgrounds
- Pill badge colors: `.choice` (amber), `.seller` (red), `.prime` (blue), `.bestseller` (green)
- CTA button: `linear-gradient(135deg, #2563eb, #1d4ed8)` with hover shadow `0 8px 20px rgba(37,99,235,0.3)`

## ⚠️ Slug Discovery: Sitemap Slugs vs. Actual Post Slugs

**Critical production finding:** A WordPress sitemap URL does not guarantee the REST slug search will find it. The sitemap path `/nutrition/what-causes-diabetes/` may map to actual slug `what-causes-type-2-diabetes` (post ID 7574), and `/nutrition/why-water-fasting-is-an-unhealthy-way-to-lose-weight/` may map to `why-water-fasting-is-an-unhealthy-way-to-lose-weight-dangers` (not the expected ID). 

### Reliable slug-to-ID lookup pattern

```python
import base64, urllib.request, json

auth_b64 = base64.b64encode(b'username:app_password').decode()

# Method 1: Try exact slug first
url = f"https://example.com/wp-json/wp/v2/posts?slug={slug}&_fields=id,slug,link"
req = urllib.request.Request(url, headers={
    'Authorization': f'Basic {auth_b64}',
    'User-Agent': 'Mozilla/5.0'
})
results = json.loads(urllib.request.urlopen(req).read())

# Method 2: If not found, search by keyword
url = f"https://example.com/wp-json/wp/v2/posts?search={keyword}&per_page=5&_fields=id,slug,link,title"

# Method 3: Request the intended public URL and extract post ID from the body HTML
# Look for: postid-<ID> class on <body> or article#post-<ID>
```

### When you find a slug mismatch

If REST slug search returns empty but the sitemap path exists:
1. Check all slugs for the parent path: `curl -s "https://example.com/wp-json/wp/v2/posts?search=water%20fasting&per_page=10&_fields=id,slug"`
2. Compare each returned slug against the sitemap path
3. The actual live page canonical often differs from the sitemap entry
4. Use the REST `link` field as source of truth, not the sitemap URL

### Verify the right post was updated

After any REST write: compare the public `postid-*` on the live URL against the REST object ID you touched. A slug collision can cause updates to hit an unrelated post.

## Bulk Multi-Page Product Box Deployment

When deploying affiliate boxes to 20+ pages in one session (e.g., after a site-wide audit), use a structured approach rather than one-off edits.

### Architecture

```
PRODUCTS dict (14+ categories × 2-4 products each)
  ↓ category assignment
PAGE_CONFIG dict (post_id → {cat: str, pos: 'after_intro'})
  ↓ build_product_box()
Scoped HTML block with CSS + cards
  ↓ rest_update()
Each page via POST + X-HTTP-Method-Override: PUT
  ↓ verification
curl + grep on every live URL
```

### Product category system (proven categories)

Build a `PRODUCTS` dict where each category contains 2-4 products with real ASINs, images (SL1500), ratings, review counts, and prices. Map categories to post IDs in a `PAGE_CONFIG` dict.

Proven categories for a fitness affiliate site (`tag=papalex-20`):
- **resistance_bands** (3 products): WHATAFIT Set B07DWSPQQY $19.99, Fit Simplify Loop B01AVDVHTI $9.95, Pull Up Assist B0CGX2256B $22.99
- **kettlebells** (2): BowFlex SelectTech 840 B07X64MXBS $139.99, Yes4All Cast Iron B0093CMYSM $21.99
- **jump_ropes** (3): Redify Weighted B08RB46DBY $24.99, Speed Rope B09DF9NWC7 $8.99, Titan Armour Pro B0CR6QHR2K $24.99
- **home_gym** (4): Adjustable Dumbbells B0FYNZQVB9 $159.99, YOLEO Bench B099JZT1WR $67.99, ProsourceFit Mat B00B4IHXRU $28.04, Stamina Power Tower B009NO30LA $309.99
- **protein** (3): Transparent Labs Whey B0CQ3JTR6F $59.99, Orgain Vegan B08PPDS7C6 $25.99, Vital Proteins Collagen B07K31N3P3 $26.98
- **hydration** (3): Hydro Flask B0764FMJFN $44.95, Liquid IV B09R3L1V1Y $23.98, Brita B08QD3G432 $34.99
- **weight_loss** (3): Etekcity Scale B0949MNLQ8 $13.99, Bentgo Containers B07MGPPFVT $24.99, NatureWise CLA B07DKS8H1T $19.99
- **mediterranean** (2): Pompeian Olive Oil B00BHM9X4I $19.99, Med Cookbook B01C34C8X0 $21.99
- **vegan** (2): Orgain Organic Vegan Protein B01BGQ1HMQ $48.02, Garden of Life Organic Vegan Protein B00CLD74WQ $74.00  ⚠️ B08PPDS7C6 and B07HFCB9VL both went 404 on .com — do not reuse
- **pcos** (2): Wholesome Story Myo-Inositol B0C1G3ZN6W $29.99, NOW Berberine B0019LRYK9 $21.99
- **diabetes** (2): Contour Next One B07N1B4VT2 $19.99, CareSens Strips B07GBNYSL1 $26.99
- **recipes** (3): Nordic Ware Sheets B002L16JMY $16.97, OXO Scoop B0DF78YQGW $14.99, Ozeri Scale B00L36CJMK $11.99
- **general_fitness** (3): Garmin HRM-Dual B07PV2W81P $59.99, Gymnext Timer B08XRQNM89 $24.99, UA ColdGear B075MY1LST $44.99
- **meal_replacement** (2): Hydro Flask B0764FMJFN $44.95, Premier Protein B00NQ2Y6KS $25.98

### Automated content insertion

```python
def find_insertion_point(content, strategy='after_intro'):
    """Insert product box just before the first <h2>."""
    import re
    h2_matches = list(re.finditer(r'<h2[^>]*>', content, re.IGNORECASE))
    if h2_matches and len(h2_matches) >= 1:
        return h2_matches[0].start()
    return len(content) // 3  # fallback

def build_product_box(category, products):
    """Generate scoped HTML block with premium CSS + cards."""
    cards_html = ''.join(build_card_html(p) for p in products)
    # Wrap in <!-- wp:html --> block, include disclosure
    return f'<!-- wp:html -->\n{PRODUCT_BOX_CSS}\n<div class="gutf-prods">...cards...</div>\n<!-- /wp:html -->'
```

### Rate limiting

When deploying 23 pages sequentially, add `time.sleep(2)` between writes. WordPress REST can return false `200`/fast responses for queued writes that do not actually persist under load.

### Batch verification loop

```bash
for slug in "fitness/resistance-bands" "nutrition/protein" "weight-loss/plan"; do
  html=$(curl -sS "https://site.com/$slug/" -H "Mozilla/5.0 UA")
  boxes=$(echo "$html" | grep -c 'gutf-prods')
  links=$(echo "$html" | grep -coP 'www\.amazon\.com/dp/[A-Z0-9]+')
  echo "$slug → boxes:$boxes links:$links"
done
```

If a page shows `boxes:0` but the REST raw content has the box, check for:
- **Slug mismatch**: the sitemap slug may redirect to a canonical slug (e.g., `water-fasting` → `water-fasting-dangers`). Verify the canonical page, not the redirector.
- **Cache layer**: try the canonical URL (from REST `link` field), not the old sitemap path.
- **Wrong post ID**: the slug search may have returned a draft or revision, not the live published post.

## Premium product box design (production-tested)

This design shipped to 23 pages and passed all verification:

### Visual characteristics
- **Card**: white background, 20px border-radius, layered shadow (`0 1px 3px rgba(0,0,0,0.06), 0 4px 12px rgba(0,0,0,0.04)`), 1px edge stroke
- **Hover**: spring animation `cubic-bezier(0.34,1.56,0.64,1)` with 4px lift and deeper shadow
- **Badge**: absolute top-left, gradient types (amber=Choice, red=Seller, green=Pick, blue=New, purple=default), bold uppercase small text
- **Image**: 110×110px (140×140px desktop), gradient bg, rounded 14px, `object-fit:contain` with hover scale(1.06)
- **Stars**: inline flex, gold (#f59e0b) filled, gray (#d1d5db) empty, with numeric rating + review count
- **CTA**: full-width gradient blue button, `#2563eb → #1d4ed8`, 12px radius, hover shadow `0 4px 16px rgba(37,99,235,0.35)`, arrow animates translateX(4px)
- **Responsive**: single column mobile → 2-column CSS grid at 900px+
- **Disclosure**: `As an Amazon Associate I earn from qualifying purchases` styled bar at module bottom

### Amazon image quality
Use `_AC_SL1500_` for Retina-quality (1500px images). Not `_AC_SX522_` (522px).

### Product description formatting
Keep descriptions to 2-line max (`-webkit-line-clamp: 2`) — long descriptions break card layout on mobile.

## Verification checklist
- Public URL returns `200`.
- Exactly one product-box wrapper section exists on each edited article (count `.gutf-products` opening, not closing). For GearUpToFit-style pages, also search variants like `.gutf-prods` / `.gutf-product-card` rather than assuming one historical class name.
- Existing H1 integrity is preserved, normally exactly one H1.
- Product names expected for that article appear in the rendered page.
- CTA anchors inside the scoped box, not unrelated theme links, all contain `sponsored nofollow noopener`.
- **Every Amazon affiliate link resolves to a real product page** (not homepage redirect) — use curl resolution check. Treat Amazon `302` geo/session redirects from direct `/dp/ASIN?tag=...` URLs as acceptable when the ASIN is not returning a clear 404.
- **Every Amazon product image loads** from `m.media-amazon.com` (not missing/broken). Image checks are stricter than product links: require HTTP `200` and nonzero byte size.
- **Real ratings and review counts** from the product page, not invented values.
- Affiliate links resolve in browser when HTTP clients are blocked; some providers return bot-only `403` while a real browser loads the tracked URL.
- Run a real browser/vision spot check on at least one representative article to catch layout defects that raw HTML checks miss. For bulk repairs, run both mobile and desktop Chromium passes and verify images have nonzero natural dimensions.
- When auditing existing boxes from REST JSON, unescape or parse `content.raw`/`content.rendered` before URL regex extraction; raw WP JSON escapes URLs as `https:\/\/...` and can create false negatives.

## Amazon product data extraction from geo-blocked locations

When `amazon.com` is geo-blocked (redirects to `.co.uk` from European IPs), use `.co.uk` to find the right products and extract data. The CDN images and ASINs often overlap between .com and .co.uk.

### Browser console extraction from Amazon.co.uk search results

Navigate to `https://www.amazon.co.uk/s?k=<search>&tag=papalex-20`, accept cookies if prompted, then run in the browser console:

```javascript
(() => {
  const items = document.querySelectorAll('[data-asin]');
  const results = [];
  items.forEach(item => {
    const asin = item.getAttribute('data-asin');
    if (asin && asin.length === 10 && asin !== 'B000000000') {
      const img = item.querySelector('img[src*="m.media-amazon"]');
      const price = item.querySelector('.a-price-whole');
      const title = item.querySelector('h2')?.textContent?.trim();
      const ratingEl = item.querySelector('i.a-icon-star');
      const rating = ratingEl?.querySelector('span')?.textContent || item.querySelector('.a-icon-alt')?.textContent;
      results.push({
        asin, imageHash: img?.src?.match(/\/I\/([A-Za-z0-9]+)\\./)?.[1] || '?',
        price: price?.textContent?.trim() || '?',
        title: title?.substring(0, 60) || '?'
      });
    }
  });
  return JSON.stringify(results, null, 2);
})();
```

### Getting full-resolution images from product pages

After clicking a product result, extract the main image from the product page:

```javascript
const img = document.querySelector('#landingImage') || 
            document.querySelector('.imgTagWrapper img');
img?.src;  // Full CDN URL like https://m.media-amazon.com/images/I/XXXX._AC_SX679_.jpg
```

Replace `_SX679_` or `_AC_SX679_` with `_AC_SL1500_` for Retina-quality (1500px) images. The CDN hash (the `XXXX` part) stays the same.

### Cross-domain validation pattern

1. Extract ASINs from `.co.uk` search results
2. Verify ASIN on `.com`: `curl -s -o /dev/null -w '%{http_code}' --max-time 8 -H "User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36" "https://www.amazon.com/dp/ASIN"`
3. Verify image independently: `curl -s -o /dev/null -w '%{http_code} %{size_download}bytes' "https://m.media-amazon.com/images/I/HASH._AC_SL1500_.jpg"`
4. Only deploy if both return 200 — note that curl can return 503/blocked for valid pages (Amazon bot detection); in that case trust the browser verification on .co.uk and the image URL check
5. The image CDN is **not geo-restricted** — always accessible from anywhere, making it the most reliable verification target

## Pitfall: false failures from broad section extraction
If verification extracts from the first `<section ...>` through the first `</section>`, it can accidentally include unrelated nested/internal links or theme blocks and report bad rel attributes. Use a scoped selector-style extraction instead:

- Count opening tags matching `<section class="...amfs-affiliate-product-box-v1...">`.
- Inspect only `a.amfs-aff-btn` CTAs for `rel="sponsored nofollow noopener"`.
- Treat unrelated internal/context links in the article as outside the affiliate-box QA surface unless the task explicitly changed them.

## Pitfall: WordPress HTML entity encoding in verification
WordPress encodes apostrophes and special characters in post content. `Amazon's Choice` becomes `Amazon&#8217;s Choice` in the rendered HTML. When verifying live content with regex or string checks:

```python
# ❌ This will fail because WordPress encodes the apostrophe
assert "Amazon's Choice" in html  # Fails — actual HTML has &#8217;s

# ✅ Check for the entity-encoded version
assert "Amazon&#8217;s Choice" in html  # Works
```

More examples of WordPress encoding:
- `'` (apostrophe) → `&#8217;` (right single quote)
- `"` → `&#8221;` or `&rdquo;`
- `—` (em dash) → `&#8212;`
- `...` (ellipsis) → `&#8230;`

When writing verification checks, always account for WP's encoding by either:
1. Checking for the entity-encoded string, OR
2. Using a more lenient pattern (e.g., `"Amazon" in html and "Choice" in html` instead of exact match)

## Pitfall: bot-only link errors
Provider landing pages may reject Python/requests with `403` while the same affiliate URL works in browser automation. Verify suspicious failures with a browser before removing or replacing an otherwise known affiliate link.

## Pitfall: Dual credential sets for WP sites with Cloudflare
Several sites (including gearuptofit.com) maintain **two credential entries** in the secrets file:
1. **WP-Admin credentials** (under "Wp-Admin" section) — work for `wp-login.php` but NOT for REST API
2. **REST API credentials** (under "Rest API" section, usually Application Passwords) — needed for `/wp-json/` endpoints

Using WP-Admin credentials against REST API returns `rest_cannot_edit` / `401`. Always check the secrets file structure: if there's a separate "Rest API" section for that domain, use those credentials. Example from production:
- ❌ `admin / 99d(J@%aVil@$dbkkv!ke8Fd` → `rest_cannot_edit` (WP-Admin password)
- ✅ `admin / K7k7 EHZT mOtf ae5C 0XeL zieo` → works (Application Password)

**⚠️ Critical file-format detail**: The two sections use *different delimiters*.
- **Wp-Admin section**: colon-delimited (`username:pass`)
- **Rest API section**: tab-delimited lines where the password is the last whitespace-delimited field on its line. Example line format:
  ```
  https://gearuptofit.com\t\nusername:admin\t\npassword=[REDACTED] EHZT mOtf ae5C 0XeL zieo\t
  ```
  Note the password contains spaces (standard WordPress Application Password format with space-delimited groups). When parsing, split on `password:` and take everything after as the credential. Do NOT use regex that expects no-spaces passwords or colon-based section parsing — you'll get a malformed credential that produces silent 401 errors.

When REST API suddenly stops working, check for stale/expired Application Passwords in the secrets file before retrying.

## Pitfall: Amazon geo-redirect blocks .com verification from European IPs
From Greece/Europe, `amazon.com` redirects to local domain (e.g. `amazon.co.uk`). This means:
- `curl` + `-L` (follow redirects) ends up on `.co.uk`, not `.com`
- `curl` without `-L` returns HTTP `301` → the ASIN check via direct curl looks unreliable
- Browser automation opens `.co.uk` automatically due to geo-detection

Workaround: Check ASINs with `curl -s -o /dev/null -w '%{http_code}' --max-time 8` **without** `-L` and with a strong Chrome UA. If HTTP 200, the page exists on .com. If HTTP 301, it's redirecting to your local domain. If HTTP 404, the ASIN is genuinely dead on .com.

For image URLs: `m.media-amazon.com/images/I/` is **not** geo-restricted — always accessible from anywhere. Test image URLs independently with:
```bash
curl -s -o /dev/null -w '%{http_code} %{size_download}bytes' \
  "https://m.media-amazon.com/images/I/XXXX._AC_SL1500_.jpg"
```
A `200` with >0 bytes means the image loads. If `404`, the CDN hash is wrong even though the ASIN may be valid.

## Pitfall: ASIN returns HTTP 200 but its image URLs are 404
An ASIN can be valid and resolve on Amazon.com while the image CDN hash you sourced is dead/wrong. This creates a page with working affiliate links but **broken product images** — the worst user experience.

Always verify **every image URL independently**, not just the ASIN:
```bash
# ❌ NOT sufficient — ASIN exists but image may be dead
curl -I "https://www.amazon.com/dp/ASIN"

# ✅ Must also verify the image specifically
curl -I "https://m.media-amazon.com/images/I/HASH._AC_SL1500_.jpg"
```

If the image returns 404, you need to get the correct CDN hash from the actual product page (use browser automation to extract `#landingImage` src). Each ASIN has a unique image hash — you cannot derive it from the ASIN itself.

Real production failure: `B08PPDS7C6` returned 200 on .com (valid ASIN) but its image `51f-6Vx2KaL._AC_SL1500_.jpg` was 404. The image hash must be freshly extracted from the product's current main image.