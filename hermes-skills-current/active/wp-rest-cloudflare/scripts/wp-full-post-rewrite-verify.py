#!/usr/bin/env python3
"""
Verify public WordPress full-post rewrites after XML-RPC/REST publishing.

Input: one or more URLs as argv, or a newline-delimited file via --file urls.txt.
Output: JSON report to stdout. Exits 2 if any URL fails.

Checks:
- public page loads
- exactly one live H1
- imported article/body H1 count is zero for article.amfs-wrap-style imports
- publisher-only `Recommended internal links` is absent from visible HTML
- no raw CSS leak outside <style>
- no visible JSON-LD/schema leak outside <script>
- title, meta description, canonical, schema, CTA presence
- representative image/iframe assets return valid HTTP status
"""
import argparse, html, json, re, ssl, sys, time, urllib.request

UA = "Hermes-WP-Full-Post-Rewrite-Verify/1.0"

def textify(s):
    return re.sub(r"\s+", " ", re.sub(r"<.*?>", "", s or "")).strip()

def fetch(url, timeout=45):
    req = urllib.request.Request(url, headers={"User-Agent": UA, "Cache-Control": "no-cache"})
    with urllib.request.urlopen(req, timeout=timeout, context=ssl._create_unverified_context()) as r:
        return r.status, r.geturl(), r.read().decode("utf-8", "ignore"), r.headers

def first_meta(body, pattern):
    m = re.search(pattern, body, re.I)
    return html.unescape(m.group(1)) if m else ""

def asset_ok(url):
    url = url.replace("&#038;", "&")
    try:
        req = urllib.request.Request(url, headers={"User-Agent": UA, "Range": "bytes=0-0"})
        with urllib.request.urlopen(req, timeout=15, context=ssl._create_unverified_context()) as r:
            return {"url": url, "status": r.status, "type": r.headers.get("content-type", "")[:60], "ok": r.status in (200, 206)}
    except Exception as e:
        return {"url": url, "error": type(e).__name__ + ": " + str(e)[:200], "ok": False}

def verify(url):
    sep = "&" if "?" in url else "?"
    status, final, body, headers = fetch(url + sep + "hermes_verify=" + str(int(time.time())))
    no_scripts = re.sub(r"<script.*?</script>", "", body, flags=re.S | re.I)
    no_styles = re.sub(r"<style.*?</style>", "", no_scripts, flags=re.S | re.I)
    amfs = re.search(r"<article[^>]+class=[\"'][^\"']*amfs-wrap[^\"']*[\"'][^>]*>.*?</article>", body, re.S | re.I)
    article_html = amfs.group(0) if amfs else body
    h1s = [textify(x) for x in re.findall(r"<h1[^>]*>(.*?)</h1>", body, re.S | re.I)]
    title = textify(first_meta(body, r"<title[^>]*>(.*?)</title>"))
    imgs = sorted(set(re.findall(r"<img[^>]+src=[\"']([^\"']+)", article_html, re.I)))
    iframes = sorted(set(re.findall(r"<iframe[^>]+src=[\"']([^\"']+)", article_html, re.I)))
    asset_checks = [asset_ok(u) for u in (imgs[:2] + iframes[:1])]
    forbidden = {
        "recommended_internal_links": bool(re.search(r"Recommended\s+internal\s+links", no_scripts, re.I)),
        "raw_css_leak": bool(re.search(r"\.[a-z0-9_-]+\s*\{", no_styles, re.I)),
        "visible_schema_leak": bool(re.search(r"@context|schema\.org", re.sub(r"<script.*?</script>", "", article_html, flags=re.S | re.I), re.I)),
        "article_body_h1": bool(re.search(r"<h1\b", article_html, re.I)) if amfs else False,
    }
    checks = {
        "loaded": len(body) > 10000,
        "one_h1": len(h1s) == 1,
        "no_article_body_h1": not forbidden["article_body_h1"],
        "no_recommended_internal_links": not forbidden["recommended_internal_links"],
        "no_raw_css_leak": not forbidden["raw_css_leak"],
        "no_visible_schema_leak": not forbidden["visible_schema_leak"],
        "title_present": bool(title),
        "meta_desc_present": bool(first_meta(body, r"<meta name=[\"']description[\"'][^>]*content=[\"']([^\"']*)[\"']")),
        "canonical_present": bool(first_meta(body, r"<link rel=[\"']canonical[\"'][^>]*href=[\"']([^\"']*)[\"']")),
        "schema_present": bool(re.search(r"application/ld\+json", body, re.I)),
        "cta_present": bool(re.search(r"class=[\"'][^\"']*(?:amfs-btn|button|cta)[^\"']*[\"']", article_html, re.I)),
        "assets_ok": all(a.get("ok") for a in asset_checks) if asset_checks else True,
    }
    return {
        "url": url,
        "final": final.split("?")[0],
        "status": status,
        "title": title,
        "h1_count": len(h1s),
        "h1s": h1s,
        "meta_description": first_meta(body, r"<meta name=[\"']description[\"'][^>]*content=[\"']([^\"']*)[\"']"),
        "canonical": first_meta(body, r"<link rel=[\"']canonical[\"'][^>]*href=[\"']([^\"']*)[\"']"),
        "jsonld_count": len(re.findall(r"application/ld\+json", body, re.I)),
        "article_images": len(imgs),
        "article_iframes": len(iframes),
        "forbidden": forbidden,
        "checks": checks,
        "asset_checks": asset_checks,
        "passed": all(checks.values()),
    }

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("urls", nargs="*")
    ap.add_argument("--file")
    args = ap.parse_args()
    urls = list(args.urls)
    if args.file:
        urls.extend([x.strip() for x in open(args.file, encoding="utf-8") if x.strip() and not x.startswith("#")])
    if not urls:
        ap.error("provide URLs or --file")
    report = [verify(u.rstrip("/") + "/" if u.startswith("http") else u) for u in urls]
    print(json.dumps(report, indent=2, ensure_ascii=False))
    if not all(r["passed"] for r in report):
        sys.exit(2)

if __name__ == "__main__":
    main()
