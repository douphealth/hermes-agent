#!/usr/bin/env python3
"""
Sitewide affiliate link gap scanner.

Scans every URL on a WordPress site (from sitemaps) for Amazon affiliate links,
reports which pages are missing them, and generates an XLSX report.

Usage:
  python3 affiliate-gap-scanner.py https://example.com -o /tmp/audit.xlsx

Options:
  -o, --output      Path for XLSX report (default: ./amazon_affiliate_audit.xlsx)
  -w, --workers     Concurrent fetches (default: 20)
  -t, --timeout     Per-page timeout in seconds (default: 15)
  --tag             Amazon tracking tag to search for (e.g. 'gearu-20')
                    If provided, pages with Amazon links without this tag
                    are flagged as "wrong tag" rather than "has links"

Features:
  - Parses sitemap_index.xml, post-sitemap.xml, post-sitemap2.xml, page-sitemap.xml
  - ThreadPoolExecutor for concurrent HTTP scanning (default 20 workers)
  - Regex covering 20+ Amazon TLDs + amzn.to + amzn.com
  - Classifies pages: /review/ /fitness/ /nutrition/ /weight-loss/ /static/ /other/
  - Priority tiers: CRITICAL (product pages w/o links), HIGH, LOW, EXCLUDE
  - 3-sheet XLSX: Missing Links, Full Site Audit, Summary Dashboard
"""

import argparse
import json
import os
import re
import sys
import textwrap
import xml.etree.ElementTree as ET
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime
from urllib.parse import urlparse, urljoin
from urllib.request import Request, urlopen

try:
    from openpyxl import Workbook
    from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
except ImportError:
    import subprocess
    subprocess.check_call(
        [sys.executable, "-m", "pip", "install", "openpyxl", "-q", "--no-warn-script-location"]
    )
    from openpyxl import Workbook
    from openpyxl.styles import Font, PatternFill, Alignment, Border, Side


# ── Constants ──

AMAZON_PATTERN = re.compile(
    r"(?:"
    r"amazon\.(?:com|co\.uk|de|fr|ca|it|es|com\.au|cn|in|jp|nl|se|sg|ae|sa|br|mx)"
    r"|amzn\.to"
    r"|amzn\.com"
    r")",
    re.IGNORECASE,
)

# High-priority product pages that critically need affiliate links.
# Key heuristics: URL paths mentioning specific products by name.
CRITICAL_PRODUCT_PATTERNS = re.compile(
    r"(?:"
    r"resistance-band|kettlebell|home-gym|dumbbell|barbell|squat-rack|bench|"
    r"gym-equipment|fitness-tracker|smartwatch|running-shoe|yoga-mat|foam-roller|"
    r"jump-rope|massage-gun|protein-powder|protein-shake|collagen|creatine|"
    r"pre-workout|electrolyte|supplement-stack|vitamin|fat-burner|waist-trainer|"
    r"best-|top-|vs-|-vs-|essential-gear|essential-equipment|equipment-list"
    r")",
    re.IGNORECASE,
)

# Pages that should never have affiliate links (excluded from audit)
EXCLUDE_PATTERNS = re.compile(
    r"(?:"
    r"/about(?:-us)?/?$|/contact(?:-us)?/?$|/privacy(?:-policy)?/?$|"
    r"/terms(?:-of-service|-conditions)?/?$|/disclaimer/?$|"
    r"/disclosure/?$|/cookies?/?$|/accessibility/?$|/sitemap|"
    r"/author/|/category/|/tag/|/page/|/amp/|"
    r"/review-methodology/|/editorial-policy/"
    r")",
    re.IGNORECASE,
)

# ── Helpers ──

def fetch_url(url, timeout=15, user_agent="Mozilla/5.0 AffiliateGapScanner/1.0"):
    """Fetch a URL and return (url, status, html_or_error_message)."""
    try:
        req = Request(url, headers={"User-Agent": user_agent})
        resp = urlopen(req, timeout=timeout)
        html = resp.read().decode("utf-8", errors="replace")
        return url, resp.status, html
    except Exception as e:
        return url, None, str(e)[:200]


def get_sitemap_urls(base_url, timeout=30):
    """Discover all URLs from the site's sitemaps (index → sub-sitemaps)."""
    sitemap_paths = [
        "/sitemap_index.xml",
        "/sitemap.xml",
        "/wp-sitemap.xml",
        "/post-sitemap.xml",
        "/post-sitemap2.xml",
        "/page-sitemap.xml",
    ]
    domain = urlparse(base_url).netloc

    # Discover sitemap index
    all_urls = []
    seen = set()

    for sp in sitemap_paths:
        url = urljoin(base_url, sp)
        _, status, html = fetch_url(url, timeout=15)
        if status and status == 200 and "<loc>" in html:
            locs = re.findall(r"<loc>(.*?)</loc>", html)
            all_urls.extend(locs)
            seen.add(url)

    if not all_urls:
        print("WARNING: No sitemap found. Falling back to robots.txt discovery.")
        _, _, html = fetch_url(urljoin(base_url, "/robots.txt"), timeout=15)
        for m in re.finditer(r"Sitemap:\s*(\S+)", html, re.IGNORECASE):
            _, _, sm_html = fetch_url(m.group(1).strip(), timeout=15)
            if sm_html and "<loc>" in sm_html:
                all_urls.extend(re.findall(r"<loc>(.*?)</loc>", sm_html))

    # Filter to same-domain and de-duplicate
    all_urls = list(
        dict.fromkeys(
            u for u in all_urls if urlparse(u).netloc.endswith(domain) or u.startswith("/")
        )
    )

    # Normalize relative to absolute
    all_urls = [urljoin(base_url, u) if u.startswith("/") else u for u in all_urls]

    return all_urls


def classify_url(url):
    """Classify a URL → (category, priority, products_mentioned, is_excluded)."""
    path = urlparse(url).path.rstrip("/")
    if not path:
        path = "/"

    if EXCLUDE_PATTERNS.search(path):
        return "Excluded", "EXCLUDE", "", True

    if "/review/" in path:
        return "Review", "REVIEW", "Review-page product mentions", False
    if "/fitness/" in path:
        return "Fitness", "CRITICAL" if CRITICAL_PRODUCT_PATTERNS.search(path) else "HIGH", "", False
    if "/nutrition/" in path:
        return "Nutrition", "CRITICAL" if CRITICAL_PRODUCT_PATTERNS.search(path) else "HIGH", "", False
    if "/weight-loss/" in path:
        return "Weight Loss", "HIGH", "", False
    if "/workout/" in path:
        return "Workout", "HIGH" if CRITICAL_PRODUCT_PATTERNS.search(path) else "LOW", "", False
    if "/video/" in path:
        return "Video", "LOW", "", False
    if path in ("/", ""):
        return "Home", "LOW", "", False

    return "Other", "LOW", "", False


def product_recommendations_for(url):
    """Return a string of products mentioned in the URL path."""
    path = urlparse(url).path
    product_keywords = {
        "resistance-band": "Resistance bands, loop bands",
        "kettlebell": "Kettlebells, adjustable kettlebells",
        "home-gym": "Dumbbells, barbells, squat racks, benches, gym mats",
        "dumbbell": "Dumbbells, adjustable dumbbells",
        "jump-rope": "Jump ropes, speed ropes, weighted jump ropes",
        "protein": "Protein powder, protein bars, supplements",
        "vitamin": "Vitamins, supplements",
        "collagen": "Collagen powder, beauty supplements",
        "high-protein": "Protein powder, high-protein snacks",
        "weight-loss": "Weight loss supplements, meal plans, food scale",
        "yoga-mat": "Yoga mats, yoga accessories",
        "foam-roller": "Foam rollers, recovery tools",
        "running-shoe": "Running shoes, athletic footwear",
        "hydrat": "Water bottles, hydration packs",
        "meal-prep": "Meal prep containers, kitchen tools",
        "mediterranean-diet": "Olive oil, Mediterranean cookbooks, kitchen tools",
        "vegan-diet": "Plant protein, vegan supplements",
        "pcos": "PCOS supplements, myo-inositol, berberine",
        "diabetes": "Glucose monitors, diabetic-friendly supplements",
        "personal-trainer": "Fitness apps, workout equipment",
        "cold": "Cold gear, thermal wear, gloves, cold plunge tubs",
    }
    hits = []
    for kw, desc in product_keywords.items():
        if kw in path.lower():
            hits.append(desc)
    return "; ".join(dict.fromkeys(hits))  # deduplicate preserving order


# ── Audit Logic ──

def run_audit(base_url, num_workers=20, page_timeout=15, tracking_tag=None):
    """Run the full audit and return structured results."""
    print(f"🔍 Scanning: {base_url}")
    print(f"   Workers: {num_workers}  |  Timeout: {page_timeout}s  |  Tag filter: {tracking_tag or 'none'}")

    # Phase 1: Discover URLs
    print("\n📡 Discovering URLs from sitemaps...")
    all_urls = get_sitemap_urls(base_url)
    print(f"   Found {len(all_urls)} URLs")

    if not all_urls:
        print("ERROR: No URLs discovered. Check the site URL and sitemap availability.")
        return None

    # Phase 2: Classify
    print("🏷️  Classifying pages...")
    urls_to_scan = []
    excluded = []
    for url in all_urls:
        cat, priority, products, is_excluded = classify_url(url)
        if not is_excluded:
            urls_to_scan.append((url, cat, priority, products))
        else:
            excluded.append((url, cat, priority))

    print(f"   To scan: {len(urls_to_scan)}  |  Excluded: {len(excluded)}")

    # Phase 3: Scan for Amazon links
    print("🔎 Scanning for Amazon affiliate links...")
    scan_results = {}
    batch_count = 0

    urls_only = [u[0] for u in urls_to_scan]

    with ThreadPoolExecutor(max_workers=num_workers) as executor:
        futures = {executor.submit(fetch_url, url, page_timeout): url for url in urls_only}
        for i, future in enumerate(as_completed(futures), 1):
            url, status, html = future.result()
            has_amazon = False
            tag_match = None
            error = None

            if status and status < 400:
                has_amazon = bool(AMAZON_PATTERN.search(html))
                if tracking_tag and has_amazon:
                    if re.search(re.escape(tracking_tag), html, re.IGNORECASE):
                        tag_match = True
                    else:
                        tag_match = False  # Amazon links exist but wrong tag
            elif status is None:
                error = html  # error message stored in html

            wrong_tag = (tag_match is False)

            scan_results[url] = {
                "has_amazon": has_amazon,
                "wrong_tag": wrong_tag,
                "status": status,
                "error": error,
            }

            if i % max(1, len(urls_only) // 10) == 0:
                print(f"   Progress: {i}/{len(urls_only)}")

    # Phase 4: Build results
    print("\n📊 Building report...")
    results = []
    for url, cat, priority, products in urls_to_scan:
        sr = scan_results.get(url, {})
        has_amazon = sr.get("has_amazon", False)
        wrong_tag = sr.get("wrong_tag", False)

        if has_amazon and not wrong_tag:
            priority = "DONE"
            notes = "Amazon affiliate links present ✅"
        elif wrong_tag:
            priority = "WRONG_TAG"
            notes = f"Amazon links found but missing tracking tag '{tracking_tag}'"
        elif sr.get("error"):
            priority = "ERROR"
            notes = f"Fetch error: {sr['error']}"
        else:
            # Determine real priority for missing links
            if priority == "REVIEW":
                priority = "CRITICAL"
                notes = "Review page — MUST have Amazon affiliate links"
            elif priority == "CRITICAL":
                notes = "Product-focused page — MUST add Amazon affiliate links"
            elif priority == "HIGH":
                notes = "Should add Amazon affiliate links"
            else:
                notes = "No Amazon links detected (low priority)"
            products = product_recommendations_for(url)

        results.append(
            {
                "url": url,
                "category": cat,
                "priority": priority,
                "has_amazon": has_amazon,
                "notes": notes,
                "products": products,
            }
        )

    # Sort: CRITICAL → HIGH → WRONG_TAG → LOW → EXCLUDE → DONE → ERROR
    sort_order = {"CRITICAL": 0, "HIGH": 1, "WRONG_TAG": 2, "LOW": 3, "EXCLUDE": 4, "DONE": 5, "ERROR": 6}
    results.sort(key=lambda r: sort_order.get(r["priority"], 99))

    return {
        "base_url": base_url,
        "total_urls": len(all_urls),
        "scanned": len(urls_to_scan),
        "excluded": len(excluded),
        "results": results,
        "timestamp": datetime.now().isoformat(),
    }


def generate_xlsx(data, output_path):
    """Generate a 3-sheet XLSX report from audit data."""
    wb = Workbook()

    # Colors & styles
    header_font = Font(bold=True, color="FFFFFF", size=11)
    header_fill = PatternFill(start_color="1F4E79", end_color="1F4E79", fill_type="solid")
    header_align = Alignment(horizontal="center", vertical="center", wrap_text=True)
    thin_border = Border(
        left=Side(style="thin"),
        right=Side(style="thin"),
        top=Side(style="thin"),
        bottom=Side(style="thin"),
    )
    fill_critical = PatternFill(start_color="FF6B6B", end_color="FF6B6B", fill_type="solid")
    fill_high = PatternFill(start_color="FFB347", end_color="FFB347", fill_type="solid")
    fill_low = PatternFill(start_color="FFF3CD", end_color="FFF3CD", fill_type="solid")
    fill_done = PatternFill(start_color="C6EFCE", end_color="C6EFCE", fill_type="solid")
    fill_error = PatternFill(start_color="FFE699", end_color="FFE699", fill_type="solid")
    fill_wrong_tag = PatternFill(start_color="FFC7CE", end_color="FFC7CE", fill_type="solid")

    # ── Sheet 1: Missing Links ──
    ws1 = wb.active
    ws1.title = "Missing Amazon Links"

    headers1 = ["#", "Full URL", "Category", "Priority", "Products Mentioned", "Notes"]
    for col, h in enumerate(headers1, 1):
        cell = ws1.cell(row=1, column=col, value=h)
        cell.font = header_font
        cell.fill = header_fill
        cell.alignment = header_align
        cell.border = thin_border

    missing = [r for r in data["results"] if r["priority"] in ("CRITICAL", "HIGH", "WRONG_TAG")]
    for i, r in enumerate(missing, 1):
        row = i + 1
        ws1.cell(row=row, column=1, value=i).border = thin_border
        ws1.cell(row=row, column=2, value=r["url"]).border = thin_border
        ws1.cell(row=row, column=3, value=r["category"]).border = thin_border

        cell_p = ws1.cell(row=row, column=4, value=r["priority"])
        cell_p.border = thin_border
        if r["priority"] == "CRITICAL":
            cell_p.fill = fill_critical
        elif r["priority"] == "HIGH":
            cell_p.fill = fill_high
        elif r["priority"] == "WRONG_TAG":
            cell_p.fill = fill_wrong_tag

        ws1.cell(row=row, column=5, value=r["products"]).border = thin_border
        ws1.cell(row=row, column=6, value=r["notes"]).border = thin_border

    ws1.column_dimensions["A"].width = 5
    ws1.column_dimensions["B"].width = 70
    ws1.column_dimensions["C"].width = 18
    ws1.column_dimensions["D"].width = 12
    ws1.column_dimensions["E"].width = 55
    ws1.column_dimensions["F"].width = 50
    ws1.freeze_panes = "A2"

    # ── Sheet 2: Full Site Audit ──
    ws2 = wb.create_sheet("Full Site Audit")
    headers2 = ["#", "Full URL", "Category", "Priority", "Has Amazon Links?", "Notes"]
    for col, h in enumerate(headers2, 1):
        cell = ws2.cell(row=1, column=col, value=h)
        cell.font = header_font
        cell.fill = header_fill
        cell.alignment = header_align
        cell.border = thin_border

    for i, r in enumerate(data["results"], 1):
        row = i + 1
        ws2.cell(row=row, column=1, value=i).border = thin_border
        ws2.cell(row=row, column=2, value=r["url"]).border = thin_border
        ws2.cell(row=row, column=3, value=r["category"]).border = thin_border

        cell_prio = ws2.cell(row=row, column=4, value=r["priority"])
        cell_prio.border = thin_border
        if r["priority"] == "CRITICAL":
            cell_prio.fill = fill_critical
        elif r["priority"] == "HIGH":
            cell_prio.fill = fill_high
        elif r["priority"] == "WRONG_TAG":
            cell_prio.fill = fill_wrong_tag
        elif r["priority"] == "DONE":
            cell_prio.fill = fill_done
        elif r["priority"] == "ERROR":
            cell_prio.fill = fill_error
        elif r["priority"] == "LOW":
            cell_prio.fill = fill_low

        cell_status = ws2.cell(row=row, column=5, value="YES" if r["has_amazon"] else "NO")
        cell_status.border = thin_border
        if r["has_amazon"]:
            cell_status.fill = fill_done
        else:
            cell_status.fill = fill_critical if r["priority"] == "CRITICAL" else PatternFill(start_color="FFC7CE", end_color="FFC7CE", fill_type="solid")

        ws2.cell(row=row, column=6, value=r["notes"]).border = thin_border

    ws2.column_dimensions["A"].width = 6
    ws2.column_dimensions["B"].width = 70
    ws2.column_dimensions["C"].width = 18
    ws2.column_dimensions["D"].width = 12
    ws2.column_dimensions["E"].width = 18
    ws2.column_dimensions["F"].width = 55
    ws2.freeze_panes = "A2"

    # ── Sheet 3: Summary Dashboard ──
    ws3 = wb.create_sheet("Summary")
    with_links = sum(1 for r in data["results"] if r["has_amazon"])
    without_links = sum(1 for r in data["results"] if not r["has_amazon"])
    critical = sum(1 for r in data["results"] if r["priority"] == "CRITICAL")
    high = sum(1 for r in data["results"] if r["priority"] == "HIGH")
    errors = sum(1 for r in data["results"] if r["priority"] == "ERROR")
    wrong_tag = sum(1 for r in data["results"] if r["priority"] == "WRONG_TAG")
    done = sum(1 for r in data["results"] if r["priority"] == "DONE")

    summary_data = [
        ["Amazon Affiliate Link Audit", data["base_url"]],
        ["Generated", data["timestamp"].replace("T", " ")],
        ["", ""],
        ["TOTAL URLs", data["total_urls"]],
        ["Scanned (excl. static pages)", data["scanned"]],
        ["Excluded / static pages", data["excluded"]],
        ["", ""],
        ["Pages WITH Amazon links ✅", with_links],
        ["Pages WITHOUT Amazon links ❌", without_links],
        ["  → CRITICAL (product pages)", critical],
        ["  → HIGH (should add links)", high],
        ["  → WRONG tracking tag", wrong_tag],
        ["  → Fetch ERRORS", errors],
        ["", ""],
        ["Pages with links (DONE)", done],
        ["Coverage of scanned pages", f"{with_links / max(1, data['scanned']) * 100:.1f}%"],
        ["Coverage of total URLs", f"{with_links / max(1, data['total_urls']) * 100:.1f}%"],
    ]

    # Title row styling
    title_cell = ws3.cell(row=1, column=1, value=summary_data[0][0])
    title_cell.font = Font(bold=True, size=14)
    ws3.cell(row=1, column=2, value=summary_data[0][1]).font = Font(size=12)

    for i, (label, val) in enumerate(summary_data[2:], 3):
        c1 = ws3.cell(row=i, column=1, value=label)
        c2 = ws3.cell(row=i, column=2, value=val)
        if "CRITICAL" in str(label):
            c1.fill = fill_critical
            c2.fill = fill_critical
            c1.font = Font(bold=True)
        elif "HIGH" in str(label):
            c1.fill = fill_high
            c2.fill = fill_high
        elif "ERROR" in str(label):
            c1.fill = fill_error

        c1.border = thin_border
        c2.border = thin_border

    ws3.column_dimensions["A"].width = 45
    ws3.column_dimensions["B"].width = 25

    wb.save(output_path)
    return output_path


# ── Main ──

def main():
    parser = argparse.ArgumentParser(
        description="Sitewide affiliate link gap scanner for WordPress sites.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=textwrap.dedent("""\
            Examples:
              %(prog)s https://gearuptofit.com
              %(prog)s https://gearuptofit.com -o /tmp/audit.xlsx -w 30 -t 20
              %(prog)s https://gearuptofit.com --tag gearu-20
        """),
    )
    parser.add_argument("url", help="Base URL of the WordPress site (e.g. https://example.com)")
    parser.add_argument("-o", "--output", default="./amazon_affiliate_audit.xlsx", help="Output XLSX path")
    parser.add_argument("-w", "--workers", type=int, default=20, help="Concurrent HTTP workers (default: 20)")
    parser.add_argument("-t", "--timeout", type=int, default=15, help="Per-page timeout in seconds (default: 15)")
    parser.add_argument("--tag", help="Amazon tracking tag to validate (e.g. 'gearu-20')")
    args = parser.parse_args()

    base_url = args.url.rstrip("/")
    data = run_audit(base_url, args.workers, args.timeout, args.tag)

    if data is None:
        sys.exit(1)

    path = generate_xlsx(data, args.output)
    print(f"\n✅ Report saved to: {path}")

    # Print CLI summary
    critical = [r for r in data["results"] if r["priority"] == "CRITICAL"]
    high = [r for r in data["results"] if r["priority"] == "HIGH"]
    print(f"\n📊 Summary:")
    print(f"   Total URLs: {data['total_urls']}")
    print(f"   ✅ With links: {sum(1 for r in data['results'] if r['has_amazon'])}")
    print(f"   🔴 CRITICAL missing: {len(critical)}")
    print(f"   🟠 HIGH missing: {len(high)}")
    if critical:
        print(f"\n   🔴 Top missing pages:")
        for r in critical[:10]:
            print(f"      {r['url']}")


if __name__ == "__main__":
    main()
