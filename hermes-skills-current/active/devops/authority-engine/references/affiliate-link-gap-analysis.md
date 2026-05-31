# Affiliate Link Gap Analysis — Sitewide Scan

Use this when auditing a WordPress site for pages that **should** have Amazon affiliate product links but currently don't. This is a discovery workflow, not a deployment workflow (use `affiliate-link-placement-accuracy.md` and `wp-affiliate-product-box-deployment.md` for the actual insertion).

## Quick-start (recommended)

Use the Python script for automated scanning + XLSX report generation:

```bash
python3 /home/hermes/.hermes/skills/devops/authority-engine/scripts/affiliate-gap-scanner.py \
  https://gearuptofit.com \
  -o /tmp/amazon_audit.xlsx \
  -w 20 \
  --tag gearu-20
```

The script:
- Discovers all URLs from sitemaps
- Scans with ThreadPoolExecutor (default 20 concurrent workers)
- Checks for Amazon links across 20+ Amazon TLDs + amzn.to + amzn.com
- Classifies pages by category (/review/, /fitness/, /nutrition/, /weight-loss/, etc.)
- Flags pages by priority: CRITICAL (product pages w/o links), HIGH, WRONG_TAG, LOW
- Generates a 3-sheet XLSX: Missing Amazon Links, Full Site Audit, Summary Dashboard
- Validates tracking tags when `--tag` is provided

See `scripts/affiliate-gap-scanner.py --help` for full options.

## Workflow

### Phase 1 — Discover all site URLs

Fetch the sitemap index, then all sub-sitemaps:

```bash
curl -sS "https://example.com/sitemap_index.xml" | grep -oP '<loc>\K[^<]+'
```

Typical sub-sitemaps: `post-sitemap.xml`, `post-sitemap2.xml`, `page-sitemap.xml`. Extract all `<loc>` entries.

### Phase 2 — Classify pages

Categorize each URL by path prefix:

- **/review/** — Highest priority. These explicitly review/rank products. Nearly 100% should have Amazon links.
- **/fitness/, /running/, /nutrition/, /weight-loss/, /health/** — Medium-high priority. Depends on article topic. Product-recommending articles (best-of lists, gear guides, supplement reviews) must have links; purely informational articles may not.
- **Static pages** (/about-us/, /contact-us/, /disclaimer/, /privacy-policy/, /terms/) — Skip. No affiliate links needed.
- **Utility pages** (/review-methodology/, /editorial-policy/, calculators) — Skip.
- **App/tool pages** (calorie calculators, shoe finders, etc.) — Skip for this audit.

### Phase 3 — Identify product-adjacent pages

Not all /fitness/ or /nutrition/ articles recommend products. Use keyword heuristics on the URL path to flag pages that likely discuss specific products:

```
best-, top-, vs-, -vs-, essential-gear, essential-equipment,
home-gym, equipment, dumbbell, kettlebell, resistance-band,
foam-roller, fitness-tracker, smartwatch, running-shoe,
workout-gear, exercise-equipment, protein-powder, supplement,
vitamin, jump-rope, yoga-mat, waist-trainer, treadmill,
elliptical, rowing-machine, massage-gun, sleep-aid,
fat-burner, pre-workout, electrolyte, collagen, bone-broth,
mushroom-coffee, running-hat, running-sunglasses, headphone,
earbud, garmin, fitbit, polar, suunto, coros, amazfit,
walking-shoe, walking-pad, meal-prep, meal-plan, cold-plunge,
weight-loss-gumm, keto-gumm, apple-cider-vinegar
```

Also scan all `/health/` and `/nutrition/` paths for `ranking-the-best` or `best-` substrings — these are almost always product articles.

### Phase 4 — Scan for Amazon links

For each priority page, check for Amazon affiliate patterns in the rendered HTML:

```python
import re

AMAZON_PATTERNS = [
    r'amazon\.(?:com|co\.uk|de|fr|ca|jp|it|es|com\.au|in)/',
    r'amzn\.to/',
    r'tag=gearu',
]

def has_amazon_links(html):
    for p in AMAZON_PATTERNS:
        if re.search(p, html, re.IGNORECASE):
            return True
    return False
```

Use curl with a realistic User-Agent to fetch HTML:

```bash
curl -sS --max-time 15 -H 'User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36' "$URL" | grep -c -iE 'amazon\.com/(dp/|gp/product|exec/obidos/ASIN)|amzn\.to/[A-Za-z0-9]+|tag=gearu'
```

### Phase 5 — Batch for efficiency

Scanning hundreds of pages one-by-one will time out. Use parallel strategies:

```bash
# xargs with parallel curl (adjust -P for parallelism)
cat urls.txt | xargs -I{} -P6 sh -c '
  count=$(curl -sS --max-time 15 -H "User-Agent: Mozilla/5.0" "{}" 2>/dev/null | grep -c -iE "amazon\.com/(dp/|gp/product)|amzn\.to/|tag=gearu")
  [ "$count" -eq 0 ] && echo "MISSING: {}"
'
```

Or batch in a Python script with `subprocess.run()`, 5–8 at a time, with a short sleep between batches to avoid rate limiting.

### Phase 6 — Prioritize findings

Organize results in priority tiers:

**🔴 CRITICAL** — Product review pages without links (e.g., `/fitness/how-to-use-resistance-bands/`). These explicitly discuss products with zero affiliate links.

**🟡 HIGH** — Product-adjacent articles that recommend items but have no links (e.g., `/nutrition/high-protein-low-carb-foods/` — lists specific foods/brands with no links).

**🟢 LOW** — Informational articles that could benefit from contextual links (e.g., `/fitness/how-long-hiit-workout-to-lose-weight/` — could link to fitness trackers/equipment but not critical).

**⚪ EXCLUDE** — Static pages, methodology pages, calculators, etc.

## Common failure modes & solutions

| Problem | Solution |
|---|---|
| **curl timeouts on slow WordPress sites** | Reduce batch size, increase timeout to 20-25s, skip fully dead URLs |
| **Amazon blocks curl with 503** | The page may still have links; trust grep results on partial HTML or use browser verification |
| **JS-loaded affiliate links** | curl won't find them. Use browser automation (Playwright/headless) to verify suspect pages |
| **Only 25/762 URLs succeed** | Timeouts from slow origin + Cloudflare. Retry with longer timeouts, skip unresponsive URLs, focus on confirmed reads |
| **False negatives from partial HTML** | Truncated HTML may miss links at bottom of page. Verify via browser for suspect pages |
| **False negatives from raw WordPress REST JSON** | WordPress escapes URLs as `https:\/\/...`; parse JSON and inspect `content.raw`/`content.rendered`, or unescape before regex extraction |
| **Existing boxes have links but broken product images** | Audit Amazon CDN `img` URLs separately from Amazon `href` anchors; `m.media-amazon.com/images/I/...` must return `200` and nonzero bytes |
| **Product URL returns 302** | Direct Amazon `/dp/ASIN?tag=...` links often 302 for geo/session handling. Treat as acceptable unless it becomes a clear 404 or homepage-only redirect |

## Reporting format

For each page, report:
- URL path
- Page title (from `<title>`)
- Whether it has Amazon links (✅/❌)
- Category (/review/, /fitness/, /nutrition/, etc.)
- Priority tier (CRITICAL / HIGH / LOW)

Collect results by category for a readable report:

```
🏋️  /fitness/ (9 pages checked)
  ❌ /fitness/how-to-use-resistance-bands/
     Title: Resistance Bands Exercises for Total Body Toning
  ✅ /fitness/some-other-page/
```

## Pitfalls

- **Do not skip bc of volume**: 1,200+ pages on a typical content site. Batch-processing and priority classification make it manageable.
- **Don't trust curl on Amazon CDN images**: `m.media-amazon.com` images in img src are NOT affiliate links. Only check href anchors.
- **Some sites use CSS classes instead of domain-based detection**: GearUpToFit marks affiliate links with a specific CSS class (`.amazon-affiliate-link`). Before writing link-check regex, curl a few representative pages and `grep -oP 'class="[^"]*amazon[^"]*"'` to see if the site uses class-based link marking. If so, the detection regex should include class matching as a primary signal.
- **Tag confirmation is mandatory**: GearUpToFit uses `papelax-20` (yes, that's the confirmed tag). Do not assume `gearu-20`, `gearuptofit-20`, or any other variation. The confirmed tag for gearuptofit.com is `papalex-20`. Verify against the site secrets file or ask the user before committing to a tag value.
- **Tag patterns vary**: Some sites use `tag=gearuptofit-20`, others `tag=gearu-20`, or completely different sub-IDs. Check the known tag from the site's existing links first.
- **Review pages rarely miss links** — on well-monetized sites, you'll find 90%+ coverage on /review/. The real opportunity is product-adjacent /fitness/ and /nutrition/ articles.
- **Bot detection varies**: If curl keeps erroring, use `-v` to see the response body (maybe empty or a challenge page). Switch to a different UA or browser automation.
- **Performance cost**: Each URL fetch uses ~50-200KB data. 1,000 pages = ~50-200MB total. Run during low-traffic hours if bandwidth-sensitive.
