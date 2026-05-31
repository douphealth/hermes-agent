#!/usr/bin/env python3
"""URL-level post-sitemap SEO/GEO/AEO growth sprint artifact generator.

Inputs an exact sitemap URL and emits URL action table, cannibalization map, internal-linking blueprint,
claims cleanup list, and top refresh briefs. Designed for planning artifacts, not direct site edits.
"""
import argparse, csv, html, json, re, time
from collections import defaultdict
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path
from urllib.parse import urlparse
from xml.etree import ElementTree as ET

import requests

UA = 'Mozilla/5.0 (compatible; Hermes-URL-Level-Growth-Sprint/1.0)'

STOP = r'\b(202[0-9]|ultimate|complete|guide|beginners?|beginner|best|top|how|to|the|a|an|for|and|in|with|on|of|your|proven|strategies|tips|ways|review|reviews)\b'


def clean_text(s):
    s = re.sub(r'(?is)<(script|style|noscript|svg)[^>]*>.*?</\1>', ' ', s or '')
    s = re.sub(r'<[^>]+>', ' ', s)
    return re.sub(r'\s+', ' ', html.unescape(s)).strip()


def tag(htmls, pat):
    m = re.search(pat, htmls, re.I | re.S)
    return html.unescape(m.group(1).strip()) if m else ''


def alltags(htmls, pat):
    return [clean_text(x) for x in re.findall(pat, htmls, re.I | re.S)]


def hub_for(url, title=''):
    p = urlparse(url).path.lower(); t = (title or '').lower(); s = p + ' ' + t
    rules = [
        ('/ai-search-visibility/', ['ai-search','generative-engine','geo','aeo','chatgpt','perplexity','ai overview','ai visibility','ai powered','chatbot','large-language-model']),
        ('/seo/', ['seo','keyword','backlink','rank','search engine','on-page','technical seo','google search','e-e-a-t','eeat']),
        ('/affiliate-marketing/', ['affiliate','commission','amazon affiliate','clickbank','cpa','network','niche','blog monetization','make money blogging']),
        ('/monetization/', ['monetization','make money','income','revenue','passive income','side hustle','earn money','selling','digital product']),
        ('/email-marketing/', ['email','newsletter','mailchimp','convertkit','aweber','lead magnet','list building']),
        ('/tools/', ['tool','software','calculator','generator','template','platform','app','plugin','wordpress','hosting','analytics']),
        ('/reviews/', ['review','best','vs','comparison','alternative','alternatives','semrush','ahrefs','surfer','jasper','rank math','yoast']),
        ('/start-here/', ['start','beginner','learn']),
    ]
    for hub, needles in rules:
        if any(x in s for x in needles): return hub
    return '/affiliate-marketing/'


def topic_key(url):
    slug = urlparse(url).path.strip('/').split('/')[-1]
    s = re.sub(r'[-_]+', ' ', slug.lower())
    s = re.sub(STOP, ' ', s)
    words = [w for w in re.findall(r'[a-z0-9]+', s) if len(w) > 2]
    return ' '.join(words[:5]) or slug


def intent_bucket(url, title):
    s = (url + ' ' + title).lower()
    if any(x in s for x in ['review','best','vs','comparison','alternatives','tools','software','platform']): return 'commercial/tool-review'
    if any(x in s for x in ['how to','guide','beginners','start','learn','tutorial','step']): return 'how-to/educational'
    if any(x in s for x in ['make money','monetization','income','revenue','commission']): return 'monetization-commercial'
    if any(x in s for x in ['seo','rank','keyword','backlink']): return 'seo-growth'
    return 'supporting-informational'


def fetch_sitemap(sitemap):
    r = requests.get(sitemap, timeout=30, headers={'User-Agent': UA}); r.raise_for_status()
    root = ET.fromstring(r.content); ns = {'sm': 'http://www.sitemaps.org/schemas/sitemap/0.9'}
    urls = []
    for u in root.findall('.//sm:url', ns):
        loc = u.findtext('sm:loc', default='', namespaces=ns).strip()
        lastmod = u.findtext('sm:lastmod', default='', namespaces=ns).strip()
        if loc: urls.append({'url': loc, 'lastmod': lastmod})
    return urls


def crawl(row):
    u = row['url']
    try:
        sep = '&' if '?' in u else '?'
        r = requests.get(u + sep + 'hermes_growth_sprint=1', timeout=35, headers={'User-Agent': UA})
        hs = r.text; text = clean_text(hs); lower = text.lower()
        title = clean_text(tag(hs, r'<title[^>]*>(.*?)</title>'))
        meta = tag(hs, r'<meta[^>]+name=["\']description["\'][^>]+content=["\'](.*?)["\']') or tag(hs, r'<meta[^>]+content=["\'](.*?)["\'][^>]+name=["\']description["\']')
        h1s = alltags(hs, r'<h1[^>]*>(.*?)</h1>')
        claims = []
        for p in [r'\$\s?\d+[\d,]*(?:k|m)?(?:/month| per month)?', r'\d+[\d,]*%\s+(?:roi|increase|growth|conversion|traffic|ranking|revenue|commission)', r'\b(?:guaranteed|guarantee|proven|tested|best|#1|number one|10k|six figures|passive income)\b']:
            for m in re.finditer(p, lower, re.I):
                claims.append(re.sub(r'\s+', ' ', text[max(0, m.start()-80):m.end()+100])[:220])
                if len(claims) >= 5: break
            if len(claims) >= 5: break
        links = re.findall(r'<a\s+[^>]*href=["\']([^"\']+)["\'][^>]*>(.*?)</a>', hs, re.I | re.S)
        own_host = urlparse(u).netloc
        internal = [x for x in links if urlparse(x[0]).netloc == own_host or x[0].startswith('/')]
        aff = [x for x in links if any(n in x[0].lower() for n in ['amazon.','shareasale','impact.com','cj.com','clickbank','partner','affiliate','ref=','tag=','utm_'])]
        clean_title = title.replace(' - Affiliate Marketing for Success','').replace(' | Affiliate Marketing for Success','')
        h1 = ' | '.join(h1s)
        return {**row, 'status': r.status_code, 'title': clean_title, 'meta': clean_text(meta), 'h1': h1, 'h1_count': len(h1s), 'word_count': len(text.split()), 'quick_answer': bool(re.search(r'quick answer|key takeaway|answer:', lower)), 'faq': bool(re.search(r'frequently asked questions|\bfaq\b', lower)), 'schema_types': '|'.join(sorted(set(re.findall(r'"@type"\s*:\s*"([^"]+)"', hs)))), 'internal_link_count': len(internal), 'affiliate_link_count': len(aff), 'claims': ' || '.join(claims), 'error': ''}
    except Exception as e:
        return {**row, 'status': 'ERR', 'error': repr(e), 'title': '', 'h1': '', 'word_count': 0}


def action_for(r, group_size, primary_url):
    if r.get('status') != 200: return 'NOINDEX_OR_FIX_STATUS'
    if r.get('word_count', 0) < 700: return 'NOINDEX_OR_MERGE'
    if group_size > 1 and r['url'] != primary_url: return 'MERGE_OR_301'
    if r['intent'] == 'commercial/tool-review': return 'PRIMARY' if r.get('word_count', 0) >= 1400 else 'REFRESH_COMMERCIAL'
    return 'REFRESH' if r.get('word_count', 0) < 1200 else ('PRIMARY' if group_size > 1 else 'KEEP_SUPPORTING')


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--sitemap', required=True, help='Exact sitemap feed to use as source of truth')
    ap.add_argument('--out', required=True)
    ap.add_argument('--workers', type=int, default=12)
    args = ap.parse_args()
    out = Path(args.out); out.mkdir(parents=True, exist_ok=True)
    rows = []
    urls = fetch_sitemap(args.sitemap)
    with ThreadPoolExecutor(max_workers=args.workers) as ex:
        for f in as_completed([ex.submit(crawl, u) for u in urls]): rows.append(f.result())
    for r in rows:
        r['hub'] = hub_for(r['url'], r.get('title','') + ' ' + r.get('h1',''))
        r['topic_key'] = topic_key(r['url'])
        r['intent'] = intent_bucket(r['url'], r.get('title',''))
    by = defaultdict(list)
    for r in rows: by[(r['hub'], ' '.join(r['topic_key'].split()[:2]))].append(r)
    for grp in by.values():
        primary = max(grp, key=lambda x: (x.get('word_count',0), x.get('internal_link_count',0), -len(x['url'])))['url']
        for r in grp:
            r['primary_url'] = primary
            r['cannibalization_action'] = action_for(r, len(grp), primary)
            r['needs_geo_blocks'] = 'NO' if r.get('quick_answer') and r.get('faq') else 'YES'
            r['needs_trust_module'] = 'YES' if r['intent'] == 'commercial/tool-review' or r.get('affiliate_link_count',0) > 0 else 'NO'
            r['unsupported_claims_flag'] = 'YES' if r.get('claims') else 'NO'
            r['priority_score'] = (10 if r['hub'] in ['/affiliate-marketing/','/seo/','/ai-search-visibility/'] else 7) + (4 if r['needs_geo_blocks']=='YES' else 0) + (3 if r['unsupported_claims_flag']=='YES' else 0) + (2 if r['needs_trust_module']=='YES' else 0)
    fields = ['url','status','lastmod','hub','intent','topic_key','cannibalization_action','primary_url','word_count','h1_count','title','h1','meta','quick_answer','faq','schema_types','internal_link_count','affiliate_link_count','needs_geo_blocks','needs_trust_module','unsupported_claims_flag','claims','priority_score']
    with open(out/'url_action_table.csv','w',newline='',encoding='utf-8') as fh:
        w = csv.DictWriter(fh, fields); w.writeheader(); w.writerows([{k:r.get(k,'') for k in fields} for r in sorted(rows, key=lambda x: -x['priority_score'])])
    cann = [r for r in rows if r.get('primary_url') != r['url'] or sum(1 for x in rows if x.get('primary_url') == r.get('primary_url')) > 1]
    with open(out/'cannibalization_map.csv','w',newline='',encoding='utf-8') as fh:
        w = csv.DictWriter(fh, ['hub','topic_key','url','cannibalization_action','primary_url','title','word_count']); w.writeheader(); w.writerows([{k:r.get(k,'') for k in ['hub','topic_key','url','cannibalization_action','primary_url','title','word_count']} for r in cann])
    with open(out/'claims_to_remove_or_prove.csv','w',newline='',encoding='utf-8') as fh:
        w = csv.DictWriter(fh, ['url','hub','action','claim_snippets']); w.writeheader()
        w.writerows([{'url': r['url'], 'hub': r.get('hub',''), 'action': 'REMOVE_OR_PROVE', 'claim_snippets': r.get('claims','')} for r in rows if r.get('claims')])
    links = []
    hub_urls = {h: urlparse(args.sitemap).scheme + '://' + urlparse(args.sitemap).netloc + h for h in sorted(set(r['hub'] for r in rows))}
    for r in sorted(rows, key=lambda x: -x['priority_score'])[:80]:
        links.append({'source_url': r['url'], 'target_url': hub_urls.get(r['hub'], ''), 'anchor_text': r['hub'].strip('/').replace('-', ' ') + ' hub', 'placement': 'Intro or first 25% after Quick Answer', 'reason': 'route topical authority to canonical hub'})
        if r.get('primary_url') and r['primary_url'] != r['url']:
            links.append({'source_url': r['url'], 'target_url': r['primary_url'], 'anchor_text': 'complete guide to ' + r.get('topic_key','topic'), 'placement': 'Top notice or first relevant H2', 'reason': 'consolidate cannibalized intent'})
    with open(out/'internal_linking_blueprint.csv','w',newline='',encoding='utf-8') as fh:
        w = csv.DictWriter(fh, ['source_url','target_url','anchor_text','placement','reason']); w.writeheader(); w.writerows(links)
    top20 = []
    for r in sorted(rows, key=lambda x: -x['priority_score'])[:20]:
        h1 = (r.get('h1') or r.get('title') or urlparse(r['url']).path.strip('/').replace('-', ' ').title()).split('|')[0].strip()
        top20.append({'url': r['url'], 'hub': r.get('hub',''), 'action': r.get('cannibalization_action',''), 'score': r.get('priority_score',0), 'title_direction': h1[:55] + ' | Updated Guide', 'h1': h1, 'meta_direction': 'Answer the query directly, add sources, remove unsupported claims, and route readers to the next relevant hub/tool/review.', 'quick_answer_direction': f'{h1} should answer the query first, then show fit, tradeoffs, proof, steps, common mistakes, and the next best action.', 'geo_aeo_blocks': 'Quick answer; best for; not best for; cost/difficulty/time; steps; common mistake; next step; FAQ; sources and verification.', 'trust_module': 'Proof/review module required' if r.get('needs_trust_module') == 'YES' else 'Editorial source/last-verified box required', 'claims_action': 'Remove or prove high-risk claims' if r.get('claims') else 'No high-risk claim pattern detected in crawl sample'})
    (out/'top20_refresh_briefs.json').write_text(json.dumps(top20, indent=2, ensure_ascii=False), encoding='utf-8')
    md = [f'# URL-Level Growth Sprint\n\nSource of truth: {args.sitemap}\nURLs crawled: {len(rows)}\nGenerated: {time.strftime("%Y-%m-%d %H:%M:%S")}\n', '## Top 20 Refresh Queue']
    for i,r in enumerate(sorted(rows, key=lambda x: -x['priority_score'])[:20], 1):
        md.append(f"{i}. {r['url']} — {r['hub']} — {r['cannibalization_action']} — score {r['priority_score']}")
    (out/'executive_sprint_plan.md').write_text('\n'.join(md), encoding='utf-8')
    print(json.dumps({'sitemap': args.sitemap, 'urls': len(rows), 'out': str(out)}, indent=2))

if __name__ == '__main__':
    main()
