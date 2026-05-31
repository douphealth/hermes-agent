#!/usr/bin/env python3
"""
Enterprise SEO/GEO/AEO scorecard for public URLs.

Zero-dependency crawler/scorer inspired by public SEO/GEO/AEO skill repos.
It does NOT claim rankings. It emits confidence-labeled, evidence-backed
findings across four vectors: technical accessibility, content citability,
structured data, and entity/brand signals.
"""
from __future__ import annotations

import argparse
import json
import re
import ssl
import sys
import time
from dataclasses import dataclass, asdict
from html.parser import HTMLParser
from pathlib import Path
from typing import Any
from urllib.parse import urljoin, urlparse
from urllib.request import Request, urlopen
from urllib.error import HTTPError, URLError

AI_BOTS = [
    "GPTBot", "ChatGPT-User", "OAI-SearchBot", "ClaudeBot", "Claude-User",
    "PerplexityBot", "Google-Extended", "Googlebot", "Bingbot", "Applebot",
    "YouBot", "CCBot", "Bytespider"
]

PROFILE_WEIGHTS = {
    "default":   {"technical": .20, "citability": .35, "schema": .20, "entity": .25},
    "publisher": {"technical": .15, "citability": .45, "schema": .20, "entity": .20},
    "affiliate": {"technical": .18, "citability": .35, "schema": .25, "entity": .22},
    "ecommerce": {"technical": .18, "citability": .25, "schema": .32, "entity": .25},
    "local":     {"technical": .18, "citability": .25, "schema": .22, "entity": .35},
    "saas":      {"technical": .18, "citability": .32, "schema": .25, "entity": .25},
}

@dataclass
class Finding:
    id: str
    severity: str
    confidence: str
    vector: str
    message: str
    evidence: list[str]
    recommendation: str
    impact: int = 0

class Parser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.title = ""
        self.meta = []
        self.links = []
        self.imgs = []
        self.headings = []
        self.scripts = []
        self.current_tag = None
        self.current_attrs = {}
        self.text_parts = []
        self.title_parts = []
        self.schema_json = []
        self.in_script_jsonld = False
        self.script_buf = []

    def handle_starttag(self, tag, attrs):
        a = {k.lower(): (v or "") for k, v in attrs}
        self.current_tag = tag.lower()
        self.current_attrs = a
        if tag.lower() == "meta": self.meta.append(a)
        elif tag.lower() == "a": self.links.append(a)
        elif tag.lower() == "img": self.imgs.append(a)
        elif tag.lower() in ["h1","h2","h3","h4","h5","h6"]: self.headings.append([tag.lower(), ""])
        elif tag.lower() == "script":
            self.scripts.append(a)
            if "ld+json" in a.get("type", "").lower():
                self.in_script_jsonld = True
                self.script_buf = []

    def handle_endtag(self, tag):
        if tag.lower() == "script" and self.in_script_jsonld:
            raw = "".join(self.script_buf).strip()
            if raw: self.schema_json.append(raw)
            self.in_script_jsonld = False
            self.script_buf = []
        self.current_tag = None
        self.current_attrs = {}

    def handle_data(self, data):
        if self.in_script_jsonld:
            self.script_buf.append(data)
            return
        txt = re.sub(r"\s+", " ", data).strip()
        if not txt: return
        if self.current_tag == "title": self.title_parts.append(txt)
        elif self.current_tag in ["h1","h2","h3","h4","h5","h6"] and self.headings:
            self.headings[-1][1] += (" " + txt).strip()
        elif self.current_tag not in ["style", "script", "noscript"]:
            self.text_parts.append(txt)

    def finish(self):
        self.title = " ".join(self.title_parts).strip()
        return self

def fetch(url: str, ua: str = "Mozilla/5.0 HermesSEOAudit/1.0", timeout: int = 20):
    ctx = ssl._create_unverified_context()
    req = Request(url, headers={"User-Agent": ua, "Accept": "text/html,application/xhtml+xml"})
    started = time.time()
    try:
        with urlopen(req, timeout=timeout, context=ctx) as r:
            body = r.read(3_000_000)
            ctype = r.headers.get("content-type", "")
            final = r.geturl()
            status = r.status
            headers = dict(r.headers.items())
        text = body.decode("utf-8", "replace")
        return {"ok": True, "status": status, "url": url, "final_url": final, "headers": headers, "content_type": ctype, "html": text, "elapsed": round(time.time()-started,2)}
    except HTTPError as e:
        body = e.read(200000).decode("utf-8", "replace") if e.fp else ""
        return {"ok": False, "status": e.code, "url": url, "final_url": url, "headers": dict(e.headers.items()) if e.headers else {}, "html": body, "error": str(e), "elapsed": round(time.time()-started,2)}
    except Exception as e:
        return {"ok": False, "status": None, "url": url, "final_url": url, "headers": {}, "html": "", "error": repr(e), "elapsed": round(time.time()-started,2)}

def origin(url):
    p=urlparse(url)
    return f"{p.scheme}://{p.netloc}"

def robots_url(url): return urljoin(origin(url), "/robots.txt")
def llms_url(url): return urljoin(origin(url), "/llms.txt")
def sitemap_url(url): return urljoin(origin(url), "/sitemap.xml")

def text_meta(p: Parser, name: str):
    for m in p.meta:
        if m.get("name", "").lower() == name.lower() or m.get("property", "").lower() == name.lower():
            return m.get("content", "")
    return ""

def canonical(p: Parser):
    for l in p.links:
        if "canonical" in l.get("rel", "").lower(): return l.get("href", "")
    return ""

def parse_schema(raws):
    out=[]; errors=[]
    for raw in raws:
        try:
            data=json.loads(raw)
            if isinstance(data, list): out.extend(data)
            else: out.append(data)
        except Exception as e:
            errors.append(str(e))
    types=[]
    def walk(x):
        if isinstance(x, dict):
            t=x.get("@type")
            if isinstance(t, str): types.append(t)
            elif isinstance(t, list): types.extend([str(i) for i in t])
            for v in x.values(): walk(v)
        elif isinstance(x, list):
            for v in x: walk(v)
    walk(out)
    return sorted(set(types)), errors

def count_words(text): return len(re.findall(r"\b[\w'-]+\b", text))
def count_stats(text):
    return len(re.findall(r"(?:\b\d+(?:\.\d+)?\s?%\b|\b\d{4}\b|\b\d+(?:\.\d+)?\s?(?:x|times|million|billion|hours|days|weeks|months|years)\b)", text, re.I))
def external_citations(p: Parser, base: str):
    host=urlparse(base).netloc.replace("www.","")
    ex=[]
    for a in p.links:
        href=a.get("href","")
        if href.startswith("http") and host not in urlparse(href).netloc.replace("www.",""):
            ex.append(href)
    return ex

def robots_allows(robots_text: str, bot: str):
    # Conservative simplified parser: detects explicit user-agent section disallow /.
    if not robots_text: return None
    lines=[ln.strip() for ln in robots_text.splitlines() if ln.strip() and not ln.strip().startswith('#')]
    active=False; matched=False; dis=[]
    for ln in lines:
        if ':' not in ln: continue
        k,v=[x.strip() for x in ln.split(':',1)]
        if k.lower()=="user-agent":
            active = (v.lower() in [bot.lower(), '*'])
            matched = matched or active
        elif active and k.lower()=="disallow":
            dis.append(v)
    if any(d == '/' for d in dis): return False
    return True if matched else None

def score(url: str, profile: str):
    f=[]
    res=fetch(url)
    html=res.get("html","")
    p=Parser(); p.feed(html); p.finish()
    visible=" ".join(p.text_parts)
    words=count_words(visible)
    title=p.title
    desc=text_meta(p, "description")
    canon=canonical(p)
    h1=[h[1].strip() for h in p.headings if h[0]=='h1' and h[1].strip()]
    h2=[h[1].strip() for h in p.headings if h[0]=='h2' and h[1].strip()]
    schema_types, schema_errors=parse_schema(p.schema_json)
    robots=fetch(robots_url(url), ua="HermesSEOAudit/1.0")
    llms=fetch(llms_url(url), ua="HermesSEOAudit/1.0")
    sitemap=fetch(sitemap_url(url), ua="HermesSEOAudit/1.0")
    scores={"technical":100,"citability":100,"schema":100,"entity":100}

    def add(id, sev, conf, vec, msg, ev, rec, impact):
        f.append(Finding(id, sev, conf, vec, msg, ev, rec, impact)); scores[vec]=max(0, scores[vec]-impact)

    # Technical
    if res.get("status") != 200:
        add("T-001","critical","Confirmed","technical",f"Page returns status {res.get('status')}",["fetch_page"],"Fix status/indexability before content work.",35)
    if urlparse(res.get("final_url",url)).netloc != urlparse(url).netloc or res.get("final_url") != url:
        f.append(Finding("T-002","low","Confirmed","technical",f"Final URL differs: {res.get('final_url')}",["fetch_page"],"Confirm redirect/canonical intent.",0))
    if not canon:
        add("T-003","medium","Confirmed","technical","No canonical link detected.",["html_parse"],"Add a self-referencing canonical or intended canonical.",10)
    if robots.get("status") != 200:
        add("T-004","medium","Confirmed","technical","robots.txt not reachable at /robots.txt.",["robots_fetch"],"Publish robots.txt with sitemap and AI crawler policy.",12)
    else:
        blocked=[b for b in AI_BOTS if robots_allows(robots.get("html",""), b) is False]
        if blocked:
            add("T-005","high","Confirmed","technical",f"AI/search bots blocked in robots.txt: {', '.join(blocked[:8])}",["robots_parse"],"Review bot policy; allow wanted AI/search crawlers.",min(30,5*len(blocked)))
    if len(html) < 5000:
        add("T-006","medium","Likely","technical",f"HTML is very small ({len(html)} bytes); content may be thin or JS-dependent.",["html_size"],"Ensure primary content renders in initial HTML for search and AI retrievers.",8)

    # Citability
    stats=count_stats(visible); ex=external_citations(p,url)
    if words < 700:
        add("C-001","high","Confirmed","citability",f"Low visible word count: {words} words.",["text_extract"],"Add useful answer-first sections, examples, comparisons, FAQs, and evidence — no filler.",20)
    if words > 300 and stats / max(words,1) * 100 < 0.25:
        add("C-002","medium","Confirmed","citability",f"Low statistic/factual-number density: {stats} detected in {words} words.",["stat_pattern"],"Add source-backed statistics, dates, measurements, examples, and concrete criteria where truthful.",10)
    if words > 500 and len(ex) < 2:
        add("C-003","medium","Confirmed","citability",f"Few outbound authoritative citations: {len(ex)} external links.",["link_extract"],"Cite primary/authoritative sources for claims that need support.",10)
    question_heads=sum(1 for _,t in p.headings if '?' in t or re.match(r"(?i)^(what|how|why|when|where|which|can|does|is|are)\b",t.strip()))
    if question_heads < 2:
        add("C-004","medium","Confirmed","citability",f"Only {question_heads} question-style headings detected.",["heading_extract"],"Add answer-engine-friendly H2/H3 questions aligned to PAA/user intent.",8)

    # Schema
    if not p.schema_json:
        add("S-001","high","Confirmed","schema","No JSON-LD schema detected.",["jsonld_extract"],"Add Article/WebPage/BreadcrumbList/FAQPage/HowTo/Product schema only when visible content supports it.",25)
    if schema_errors:
        add("S-002","high","Confirmed","schema",f"JSON-LD parse errors: {len(schema_errors)}.",["jsonld_parse"],"Fix invalid JSON-LD before expanding schema.",20)
    desirable={"Article","BlogPosting","WebPage","FAQPage","HowTo","BreadcrumbList","Organization","Person","Product","Review"}
    if p.schema_json and not (set(schema_types) & desirable):
        add("S-003","medium","Confirmed","schema",f"Schema types may be weak for SEO/GEO: {schema_types[:8]}",["jsonld_types"],"Add page-appropriate schema matching visible content.",10)
    if not any(t in schema_types for t in ["Organization","Person"]):
        add("S-004","low","Confirmed","schema","No Organization/Person entity schema detected.",["jsonld_types"],"Expose accurate brand/author entity markup without fake credentials.",6)

    # Entity
    sameas = "sameAs" in html
    about = bool(re.search(r"(?i)\b(about us|editorial|methodology|reviewed by|written by|author|contact)\b", visible))
    if not about:
        add("E-001","medium","Likely","entity","Weak visible trust/entity signals (author/about/editorial/contact terms not detected).",["text_extract"],"Add accurate author/editorial/about/contact/trust context where appropriate.",15)
    if not sameas:
        add("E-002","low","Confirmed","entity","No sameAs entity links detected in source.",["html_search"],"Connect brand/entity profiles in Organization/Person schema if accurate.",8)
    if llms.get("status") != 200:
        add("E-003","medium","Confirmed","entity","/llms.txt not reachable.",["llms_fetch"],"Consider curated llms.txt for important pages after Yoast/cache/plugin conflict checks.",8)
    if sitemap.get("status") != 200:
        f.append(Finding("E-004","low","Confirmed","entity","/sitemap.xml not reachable; WP may use sitemap_index.xml.",["sitemap_fetch"],"Verify sitemap index and submit canonical sitemap in search consoles.",0))

    weights=PROFILE_WEIGHTS.get(profile, PROFILE_WEIGHTS["default"])
    composite=round(sum(scores[k]*weights[k] for k in weights))
    band="Excellent" if composite>=86 else "Good" if composite>=68 else "Foundation" if composite>=36 else "Critical"
    return {
        "url": url, "final_url": res.get("final_url"), "profile": profile, "timestamp": int(time.time()),
        "status": res.get("status"), "elapsed_seconds": res.get("elapsed"),
        "title": title, "meta_description": desc, "canonical": canon,
        "h1": h1, "h2_count": len(h2), "word_count": words,
        "schema_types": schema_types, "schema_errors": schema_errors,
        "robots_status": robots.get("status"), "llms_status": llms.get("status"), "sitemap_status": sitemap.get("status"),
        "scores": scores, "weights": weights, "geo_aeo_score": composite, "score_band": band,
        "findings": [asdict(x) for x in sorted(f, key=lambda x: ({"critical":0,"high":1,"medium":2,"low":3}.get(x.severity,9), -x.impact))]
    }

def to_markdown(r):
    lines=[f"# GEO/AEO Enterprise Scorecard", "", f"URL: {r['url']}", f"Final URL: {r.get('final_url')}", f"Profile: {r['profile']}", f"Composite GEO/AEO Score: **{r['geo_aeo_score']} / 100** ({r['score_band']})", ""]
    lines += ["## Vector scores", ""]
    for k,v in r['scores'].items(): lines.append(f"- {k}: {v}/100 (weight {r['weights'][k]:.0%})")
    lines += ["", "## Evidence snapshot", "", f"- HTTP status: {r['status']}", f"- Title: {r['title'] or 'MISSING'}", f"- Meta description: {'present' if r['meta_description'] else 'missing'}", f"- Canonical: {r['canonical'] or 'missing'}", f"- H1 count: {len(r['h1'])}", f"- Word count: {r['word_count']}", f"- Schema types: {', '.join(r['schema_types']) if r['schema_types'] else 'none'}", f"- robots.txt status: {r['robots_status']}", f"- llms.txt status: {r['llms_status']}", ""]
    lines += ["## Findings", ""]
    if not r['findings']: lines.append("- No major findings detected by this lightweight public audit.")
    for x in r['findings']:
        lines += [f"- [{x['severity'].upper()}][{x['confidence']}][{x['vector']}] {x['message']}", f"  - Evidence: {', '.join(x['evidence'])}", f"  - Recommendation: {x['recommendation']}"]
    lines += ["", "## Self-critique", "", "- This is a public, lightweight, zero-dependency audit. It cannot see GSC, rankings, conversions, WP private metadata, plugin settings, or real AI citation outcomes unless those are provided separately.", "- Treat score changes within ±3 as noise. Validate high-impact fixes after deployment with live crawl, schema tests, GSC/rank/AI citation monitoring where available."]
    return "\n".join(lines)+"\n"

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--url", required=True)
    ap.add_argument("--profile", default="default", choices=sorted(PROFILE_WEIGHTS))
    ap.add_argument("--format", default="markdown", choices=["markdown","json"])
    ap.add_argument("--out")
    args=ap.parse_args()
    r=score(args.url, args.profile)
    out=json.dumps(r, indent=2, ensure_ascii=False) if args.format=="json" else to_markdown(r)
    if args.out:
        Path(args.out).parent.mkdir(parents=True, exist_ok=True)
        Path(args.out).write_text(out, encoding="utf-8")
    print(out)

if __name__ == "__main__": main()
