#!/usr/bin/env python3
"""
Public WordPress SEO audit probe for Authority Engine work.

Runs without WP credentials. It checks public robots/sitemaps/WP REST inventory,
page H1/meta/canonical/schema/word-count/image-alt/anchor/GEO-readiness signals, duplicate post/page slug
conflicts, sitemap inventory, internal 404/redirect leakage, and page scorecards inspired by public SEO/GEO toolkits.

Usage:
  python3 scripts/public-wordpress-seo-audit.py https://example.com
"""
import collections
import html
import json
import re
import xml.etree.ElementTree as ET
import sys
import time
from urllib.parse import urljoin, urlparse, urldefrag

import requests


def clean(text: str) -> str:
    text = re.sub(r"<script[\s\S]*?</script>|<style[\s\S]*?</style>", " ", text, flags=re.I)
    text = re.sub(r"<[^>]+>", " ", text)
    return re.sub(r"\s+", " ", html.unescape(text)).strip()


def tag_texts(ht: str, tag: str, limit=None):
    vals = []
    for m in re.finditer(fr"<{tag}\b[^>]*>([\s\S]*?)</{tag}>", ht, flags=re.I):
        vals.append(clean(m.group(1)))
        if limit and len(vals) >= limit:
            break
    return vals


def meta(ht: str, name: str) -> str:
    for m in re.finditer(r"<meta\b([^>]*)>", ht, flags=re.I):
        attrs = m.group(1)
        if re.search(r"(?:name|property)\s*=\s*[\"']?" + re.escape(name) + r"[\"']?", attrs, flags=re.I):
            cm = re.search(r"content\s*=\s*[\"']([^\"']*)", attrs, flags=re.I)
            return html.unescape(cm.group(1)) if cm else ""
    return ""


def img_alts(ht: str):
    imgs = re.findall(r"<img\b([^>]*)>", ht, flags=re.I)
    missing = 0
    empty = 0
    for attrs in imgs:
        m = re.search(r"alt\s*=\s*[\"']([^\"']*)", attrs, flags=re.I)
        if not m:
            missing += 1
        elif not m.group(1).strip():
            empty += 1
    return {"images": len(imgs), "missing_alt": missing, "empty_alt": empty}


def anchors(ht: str, base_url: str, domain: str):
    out = []
    for m in re.finditer(r"<a\b([^>]*)>([\s\S]*?)</a>", ht, flags=re.I):
        attrs, inner = m.group(1), m.group(2)
        hm = re.search(r"href=[\"']([^\"']+)", attrs, flags=re.I)
        if not hm:
            continue
        href = hm.group(1)
        if href.startswith(("mailto:", "tel:", "#", "javascript:")):
            continue
        full = urldefrag(urljoin(base_url, href))[0]
        text = clean(inner)
        if urlparse(full).netloc.endswith(domain):
            out.append({"target": full, "anchor": text[:160]})
    return out


def bad_anchor_reason(text: str) -> str:
    t = (text or "").strip().lower()
    if not t:
        return "empty"
    if t in {"click here", "here", "read more", "learn more", "more", "this", "link"}:
        return "generic"
    if len(t.split()) > 12:
        return "too_long"
    if re.search(r"\b(best|top|cheap|buy)\b", t) and len(t.split()) <= 4:
        return "possible_exact_match_spam"
    if t.endswith("?") and len(t.split()) > 3:
        return "question_fragment"
    return ""


def canonical(ht: str) -> str:
    m = re.search(r"<link\b(?=[^>]*rel=[\"'][^\"']*canonical)([^>]*)>", ht, flags=re.I)
    if not m:
        return ""
    hm = re.search(r"href=[\"']([^\"']+)", m.group(1), flags=re.I)
    return html.unescape(hm.group(1)) if hm else ""


def fetch(session, url, timeout=25, method="GET"):
    try:
        if method == "HEAD":
            r = session.head(url, timeout=timeout, allow_redirects=True)
            if r.status_code in (403, 405):
                r = session.get(url, timeout=timeout, allow_redirects=True, stream=True)
        else:
            r = session.get(url, timeout=timeout, allow_redirects=True)
        return r
    except Exception as e:
        return e


def wp_rest_all(session, base, kind):
    out = []
    page = 1
    while True:
        url = f"{base}/wp-json/wp/v2/{kind}?per_page=100&page={page}&_fields=id,link,title,slug,date,modified,categories,excerpt,status"
        r = fetch(session, url)
        if isinstance(r, Exception) or r.status_code != 200:
            break
        data = r.json()
        out.extend(data)
        if page >= int(r.headers.get("X-WP-TotalPages", "1")):
            break
        page += 1
    return out


def main():
    if len(sys.argv) != 2:
        print("Usage: public-wordpress-seo-audit.py https://example.com", file=sys.stderr)
        sys.exit(2)
    base = sys.argv[1].rstrip("/")
    domain = urlparse(base).netloc
    s = requests.Session()
    s.headers.update({"User-Agent": "Mozilla/5.0 AuthorityEnginePublicAudit/1.0"})

    summary = {}
    for path in ["/", "/robots.txt", "/llms.txt", "/sitemap.xml", "/wp-sitemap.xml", "/wp-json/"]:
        r = fetch(s, base + path)
        if isinstance(r, Exception):
            summary[path] = {"error": repr(r)}
        else:
            summary[path] = {
                "status": r.status_code,
                "final": r.url,
                "ctype": r.headers.get("content-type", ""),
                "bytes": len(r.content),
                "server": r.headers.get("server"),
                "cache": r.headers.get("x-litespeed-cache") or r.headers.get("cf-cache-status"),
            }

    posts = wp_rest_all(s, base, "posts")
    pages = wp_rest_all(s, base, "pages")
    cats_r = fetch(s, f"{base}/wp-json/wp/v2/categories?per_page=100&_fields=id,name,slug,count,link")
    categories = cats_r.json() if not isinstance(cats_r, Exception) and cats_r.status_code == 200 else []

    sitemap_locs = []
    for path in ["/sitemap.xml", "/wp-sitemap.xml", "/sitemap_index.xml"]:
        r = fetch(s, base + path)
        if not isinstance(r, Exception) and r.status_code == 200:
            sitemap_locs.extend(re.findall(r"<loc>(.*?)</loc>", r.text))
    child_sitemaps = [u for u in dict.fromkeys(sitemap_locs) if "sitemap" in u and urlparse(u).netloc.endswith(domain)]
    urls = []
    for sm in child_sitemaps[:30]:
        r = fetch(s, sm)
        if not isinstance(r, Exception) and r.status_code == 200:
            urls.extend(re.findall(r"<loc>(.*?)</loc>", r.text))
    if not urls:
        urls = [it.get("link") for it in posts + pages if it.get("link")]
    urls = list(dict.fromkeys([u for u in urls if u and urlparse(u).netloc.endswith(domain)]))

    rows = []
    link_sources = collections.defaultdict(set)
    t0 = time.time()
    for u in urls:
        if "/author/" in u:
            continue
        r = fetch(s, u)
        if isinstance(r, Exception):
            rows.append({"url": u, "error": repr(r)})
            continue
        ht = r.text[:600000]
        title = tag_texts(ht, "title", 1)
        h1 = tag_texts(ht, "h1")
        h2 = tag_texts(ht, "h2")
        body = clean(ht)
        schemas = re.findall(r"<script[^>]+application/ld\+json[^>]*>([\s\S]*?)</script>", ht, flags=re.I)
        types = sorted(set(re.findall(r'"@type"\s*:\s*"([^"]+)"', " ".join(schemas))))
        schema_parse_errors = 0
        for block in schemas:
            try:
                json.loads(html.unescape(block).strip())
            except Exception:
                schema_parse_errors += 1
        internal_anchor_rows = anchors(ht, u, domain)
        internal = [a["target"] for a in internal_anchor_rows]
        for full in internal:
            link_sources[full].add(u)
        image_stats = img_alts(ht)
        question_h2s = [x for x in h2 if x.strip().endswith("?") or re.match(r"^(what|how|why|when|where|which|can|does|is|are)\b", x.strip(), re.I)]
        wc = len(re.findall(r"\w+", body))
        score_parts = {
            "indexability": 0 if r.status_code >= 400 or "noindex" in meta(ht, "robots").lower() else 2,
            "title_meta_ctr": (1 if title else 0) + (1 if 80 <= len(meta(ht, "description")) <= 170 else 0),
            "h1_heading_clarity": 2 if len([x for x in h1 if x.strip()]) == 1 and len(h2) >= 2 else (1 if h1 else 0),
            "schema_validity": 2 if schemas and schema_parse_errors == 0 else (1 if schemas else 0),
            "aeo_geo_readiness": min(2, (1 if question_h2s else 0) + (1 if re.search(r"\b(in summary|key takeaways|at a glance|what is|how to)\b", body, re.I) else 0)),
            "internal_link_equity": 2 if len(internal) >= 5 else (1 if internal else 0),
            "image_accessibility": 2 if image_stats["images"] and not image_stats["missing_alt"] and not image_stats["empty_alt"] else (1 if image_stats["images"] else 0),
            "content_depth": 2 if wc >= 1200 else (1 if wc >= 600 else 0),
        }
        rows.append({
            "url": u,
            "status": r.status_code,
            "final": r.url,
            "title": title[0] if title else "",
            "h1_count": len(h1),
            "h1": h1[:3],
            "h2_count": len(h2),
            "words": len(re.findall(r"\w+", body)),
            "meta_len": len(meta(ht, "description")),
            "canonical": canonical(ht),
            "robots": meta(ht, "robots"),
            "schema_types": types[:20],
            "internal_links": len(internal),
            "bad_anchor_count": sum(1 for a in internal_anchor_rows if bad_anchor_reason(a.get("anchor", ""))),
            "bad_anchor_samples": [dict(a, reason=bad_anchor_reason(a.get("anchor", ""))) for a in internal_anchor_rows if bad_anchor_reason(a.get("anchor", ""))][:8],
            "image_stats": image_stats,
            "schema_parse_errors": schema_parse_errors,
            "question_h2_count": len(question_h2s),
            "score_parts": score_parts,
            "score_total": sum(score_parts.values()),
        })

    slugmap = collections.defaultdict(list)
    for kind, items in [("post", posts), ("page", pages)]:
        for it in items:
            slugmap[it.get("slug")].append({
                "type": kind,
                "id": it.get("id"),
                "link": it.get("link"),
                "title": clean(it.get("title", {}).get("rendered", "")),
            })
    duplicates = {k: v for k, v in slugmap.items() if k and len(v) > 1}

    issues = {
        "blank_h1": [r for r in rows if r.get("h1_count", 0) > 0 and not any(x.strip() for x in r.get("h1", []))],
        "missing_h1": [r for r in rows if r.get("h1_count", 0) == 0],
        "multiple_h1": [r for r in rows if r.get("h1_count", 0) > 1],
        "thin_lt600": [r for r in rows if r.get("words", 999999) < 600 and "/category/" not in r.get("url", "")],
        "very_thin_lt400": [r for r in rows if r.get("words", 999999) < 400 and "/category/" not in r.get("url", "")],
        "short_meta": [r for r in rows if r.get("meta_len", 999) < 80],
        "missing_or_empty_image_alt": [r for r in rows if r.get("image_stats", {}).get("missing_alt", 0) or r.get("image_stats", {}).get("empty_alt", 0)],
        "weak_aeo_geo": [r for r in rows if r.get("question_h2_count", 0) == 0 and r.get("words", 0) >= 600],
        "bad_internal_anchors": [r for r in rows if r.get("bad_anchor_count", 0) > 0],
        "schema_parse_errors": [r for r in rows if r.get("schema_parse_errors", 0) > 0],
        "low_score_lt10": [r for r in rows if r.get("score_total", 99) < 10],
        "no_article_schema_posts": [r for r in rows if any(p.get("link") == r.get("url") for p in posts) and "Article" not in r.get("schema_types", []) and "BlogPosting" not in r.get("schema_types", [])],
    }

    bad_links = []
    redirects = []
    for link in sorted(link_sources)[:400]:
        path = urlparse(link).path
        if re.search(r"\.(jpg|jpeg|png|gif|webp|svg|css|js|ico|woff|xml)$", path, re.I):
            continue
        r = fetch(s, link, method="HEAD", timeout=15)
        if isinstance(r, Exception):
            bad_links.append({"url": link, "error": repr(r), "sources": list(link_sources[link])[:3]})
        elif r.status_code >= 400:
            bad_links.append({"url": link, "status": r.status_code, "sources": list(link_sources[link])[:3]})
        elif r.url.rstrip("/") != link.rstrip("/"):
            redirects.append({"url": link, "final": r.url, "status": r.status_code, "sources": list(link_sources[link])[:2]})

    report = {
        "base": base,
        "runtime_seconds": round(time.time() - t0, 2),
        "summary": summary,
        "counts": {"posts": len(posts), "pages": len(pages), "categories": len(categories), "sitemap_urls": len(urls), "audited_rows": len(rows)},
        "categories": categories,
        "duplicates_by_slug": duplicates,
        "issues_counts": {k: len(v) for k, v in issues.items()},
        "issues_samples": {k: [{kk: r.get(kk) for kk in ["url", "title", "h1", "words", "schema_types"]} for r in v[:25]] for k, v in issues.items()},
        "internal_link_audit": {"bad_count": len(bad_links), "redirect_count": len(redirects), "bad_samples": bad_links[:50], "redirect_samples": redirects[:50]},
        "strongest_wordcount_pages": sorted([{"url": r.get("url"), "words": r.get("words"), "title": r.get("title")} for r in rows if "words" in r], key=lambda x: x["words"], reverse=True)[:20],
        "thin_pages": sorted([{"url": r.get("url"), "words": r.get("words"), "title": r.get("title"), "h2_count": r.get("h2_count")} for r in issues["thin_lt600"]], key=lambda x: x["words"])[:50],
        "lowest_score_pages": sorted([{"url": r.get("url"), "score_total": r.get("score_total"), "score_parts": r.get("score_parts"), "title": r.get("title")} for r in rows if "score_total" in r], key=lambda x: x["score_total"])[:30],
        "best_internal_link_targets": sorted([{"url": url, "incoming_internal_sources": len(srcs)} for url, srcs in link_sources.items()], key=lambda x: x["incoming_internal_sources"], reverse=True)[:30],
    }
    print(json.dumps(report, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
