#!/usr/bin/env python3
"""Verify WordPress index-cleanup signals for a live site.

Usage:
  python wp-index-cleanup-verify.py https://example.com \
    --check /robots.txt --check /readme.html --check /site-map/

Outputs JSON with status/location/robots/canonical/H1 and sitemap primary-loc contamination.
This intentionally treats Yoast <image:loc> as normal image data, not page URL contamination.
"""
import argparse, html, json, re, sys, xml.etree.ElementTree as ET
from urllib.parse import urljoin

import requests

NS = "{http://www.sitemaps.org/schemas/sitemap/0.9}"

BAD_DEFAULTS = [
    "/wp-content/uploads/", "/readme.html", "/license.txt", "/site-map/",
    "/affiliate-success-planner-quiz/", "/editorial-policy-affiliate",
    "/editorial-policy-standards", "/index/", "/afs-homepage/",
]


def get(session, url, **kw):
    return session.get(url, timeout=kw.pop("timeout", 25), **kw)


def sitemap_locs(session, url, seen=None):
    seen = seen or set()
    if url in seen:
        return []
    seen.add(url)
    r = get(session, url)
    r.raise_for_status()
    root = ET.fromstring(r.content)
    out = []
    for sm in root.findall(".//" + NS + "sitemap"):
        loc = sm.find(NS + "loc")
        if loc is not None and loc.text:
            out += sitemap_locs(session, loc.text.strip(), seen)
    for u in root.findall(".//" + NS + "url"):
        loc = u.find(NS + "loc")
        if loc is not None and loc.text:
            out.append(loc.text.strip())
    return out


def html_signal(text):
    robots = re.search(r"<meta[^>]+name=[\"']robots[\"'][^>]+content=[\"']([^\"']+)", text or "", re.I)
    canonical = re.search(r"<link[^>]+rel=[\"']canonical[\"'][^>]+href=[\"']([^\"']+)", text or "", re.I)
    if not canonical:
        canonical = re.search(r"<link[^>]+href=[\"']([^\"']+)[\"'][^>]+rel=[\"']canonical", text or "", re.I)
    title = re.search(r"<title[^>]*>(.*?)</title>", text or "", re.I | re.S)
    h1s = re.findall(r"<h1[^>]*>(.*?)</h1>", text or "", re.I | re.S)
    visible = re.sub(r"(?is)<(script|style|noscript)[^>]*>.*?</\\1>", " ", text or "")
    visible = html.unescape(re.sub(r"(?s)<[^>]+>", " ", visible))
    return {
        "meta_robots": robots.group(1) if robots else None,
        "canonical": canonical.group(1) if canonical else None,
        "title": html.unescape(re.sub("<.*?>", "", title.group(1))).strip()[:140] if title else None,
        "h1_count": len(h1s),
        "words": len(re.findall(r"\w+", visible)),
    }


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("base", help="Site base URL, e.g. https://example.com")
    ap.add_argument("--sitemap", default="/sitemap_index.xml")
    ap.add_argument("--check", action="append", default=[])
    ap.add_argument("--bad-fragment", action="append", default=[])
    args = ap.parse_args()
    base = args.base.rstrip("/") + "/"
    session = requests.Session()
    session.headers.update({"User-Agent": "Mozilla/5.0 WordPress index-cleanup verifier"})

    checks = []
    for path in args.check:
        url = urljoin(base, path.lstrip("/"))
        sep = "&" if "?" in url else "?"
        r = get(session, url + sep + "nocache=seoqa", allow_redirects=False)
        text = r.text if "text/html" in r.headers.get("content-type", "") else ""
        row = {
            "path": path,
            "status": r.status_code,
            "location": r.headers.get("location"),
            "xrobots": r.headers.get("x-robots-tag"),
            "cf_cache_status": r.headers.get("cf-cache-status"),
        }
        row.update(html_signal(text))
        checks.append(row)

    locs = sitemap_locs(session, urljoin(base, args.sitemap.lstrip("/")))
    bad_fragments = args.bad_fragment or BAD_DEFAULTS
    bad = [u for u in locs if any(f in u for f in bad_fragments)]
    print(json.dumps({
        "base": base.rstrip("/"),
        "sitemap_primary_loc_count": len(locs),
        "bad_sitemap_primary_loc_count": len(bad),
        "bad_sitemap_primary_locs": bad[:100],
        "url_checks": checks,
    }, indent=2))


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(json.dumps({"error": str(e)}), file=sys.stderr)
        sys.exit(2)
