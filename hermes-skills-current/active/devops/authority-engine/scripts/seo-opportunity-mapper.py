#!/usr/bin/env python3
"""
Authority Engine opportunity mapper inspired by public SEO tooling.

Modes:
  content-decay: GSC export with date,page,query,clicks,impressions,ctr,position
  serp-crossover: CSV with keyword,url,position or keyword,rank,url
  keyword-gap: CSVs for own and competitors with query/keyword,url/landing_page,clicks/volume

Usage:
  python3 seo-opportunity-mapper.py content-decay gsc.csv --output decay.csv
  python3 seo-opportunity-mapper.py serp-crossover serp.csv --output crossover.csv
  python3 seo-opportunity-mapper.py keyword-gap own.csv competitor1.csv competitor2.csv --output gaps.csv
"""
import argparse, csv, itertools, sys
from collections import defaultdict, Counter
from datetime import datetime
from pathlib import Path
from urllib.parse import urlparse


def norm_col(row, *names):
    low={k.lower().strip(): k for k in row.keys()}
    for n in names:
        if n in low: return low[n]
    return None


def read_csv(path):
    with open(path, newline='', encoding='utf-8-sig') as f:
        return list(csv.DictReader(f))


def write_csv(path, rows):
    if not rows:
        print('no rows')
        return
    fields=list(rows[0].keys())
    with open(path, 'w', newline='', encoding='utf-8') as f:
        w=csv.DictWriter(f, fieldnames=fields)
        w.writeheader(); w.writerows(rows)
    print(path)


def parse_date(x):
    for fmt in ('%Y-%m-%d','%m/%d/%Y','%d/%m/%Y'):
        try: return datetime.strptime(x[:10], fmt)
        except Exception: pass
    raise ValueError(f'bad date: {x}')


def content_decay(args):
    rows=read_csv(args.files[0])
    if not rows: return []
    sample=rows[0]
    date_col=norm_col(sample,'date','day')
    page_col=norm_col(sample,'page','url','landing page','landing_page')
    query_col=norm_col(sample,'query','keyword')
    clicks_col=norm_col(sample,'clicks')
    imp_col=norm_col(sample,'impressions')
    pos_col=norm_col(sample,'position','avg position','average position')
    if not (date_col and page_col and clicks_col):
        raise SystemExit('content-decay needs date,page/url,clicks columns')
    monthly=defaultdict(lambda: defaultdict(lambda: {'clicks':0.0,'impressions':0.0,'queries':Counter(),'position_sum':0.0,'position_n':0}))
    for r in rows:
        try: d=parse_date(r[date_col])
        except Exception: continue
        month=d.strftime('%Y-%m')
        page=r[page_col].strip()
        m=monthly[page][month]
        clicks=float(r.get(clicks_col) or 0); imps=float(r.get(imp_col) or 0) if imp_col else 0
        m['clicks'] += clicks; m['impressions'] += imps
        if query_col and r.get(query_col): m['queries'][r[query_col].strip()] += clicks or imps
        if pos_col and r.get(pos_col):
            try: m['position_sum'] += float(r[pos_col]); m['position_n'] += 1
            except Exception: pass
    out=[]
    for page, months in monthly.items():
        if len(months) < 2: continue
        ordered=sorted(months)
        latest=ordered[-1]
        peak=max(ordered, key=lambda m: months[m]['clicks'])
        peak_clicks=months[peak]['clicks']; latest_clicks=months[latest]['clicks']
        if peak_clicks <= 0: continue
        loss=peak_clicks-latest_clicks
        loss_pct=loss/peak_clicks
        if loss_pct < args.min_loss: continue
        latest_imps=months[latest]['impressions']
        avg_pos=(months[latest]['position_sum']/months[latest]['position_n']) if months[latest]['position_n'] else ''
        intervention='major_republish' if loss_pct>=0.5 else 'moderate_refresh' if loss_pct>=0.2 else 'micro_refresh'
        out.append({
            'page': page, 'peak_month': peak, 'latest_month': latest,
            'peak_clicks': round(peak_clicks,2), 'latest_clicks': round(latest_clicks,2),
            'clicks_lost': round(loss,2), 'loss_pct': round(loss_pct,3),
            'latest_impressions': round(latest_imps,2), 'latest_avg_position': round(avg_pos,2) if avg_pos!='' else '',
            'top_latest_queries': ' | '.join(q for q,_ in months[latest]['queries'].most_common(8)),
            'recommended_intervention': intervention,
        })
    return sorted(out, key=lambda r: (float(r['clicks_lost']), float(r['loss_pct'])), reverse=True)


def serp_crossover(args):
    rows=read_csv(args.files[0]);
    if not rows: return []
    sample=rows[0]
    kw_col=norm_col(sample,'keyword','query')
    url_col=norm_col(sample,'url','link')
    pos_col=norm_col(sample,'position','rank')
    if not (kw_col and url_col): raise SystemExit('serp-crossover needs keyword,url columns')
    serp=defaultdict(list)
    for r in rows:
        try: pos=int(float(r.get(pos_col) or len(serp[r[kw_col]])+1))
        except Exception: pos=999
        if pos<=args.top_n:
            serp[r[kw_col]].append(r[url_col].strip())
    out=[]
    for a,b in itertools.combinations(sorted(serp),2):
        A=set(serp[a]); B=set(serp[b]);
        if not A or not B: continue
        overlap=len(A&B)/min(len(A),len(B))
        decision='consolidate_or_cannibalization' if overlap>=0.5 else 'related_sibling_or_subhub' if overlap>=0.25 else 'separate_intent' if overlap>0 else 'unrelated_or_unstable'
        out.append({'keyword_a':a,'keyword_b':b,'overlap_pct':round(overlap,3),'shared_urls':len(A&B),'decision':decision,'examples':' | '.join(list(A&B)[:5])})
    return sorted(out, key=lambda r: r['overlap_pct'], reverse=True)


def keyword_gap(args):
    own=read_csv(args.files[0]); comps=[]
    for f in args.files[1:]: comps.extend(read_csv(f))
    def cols(rows):
        s=rows[0]; return norm_col(s,'query','keyword'), norm_col(s,'url','page','landing_page','landing page'), norm_col(s,'clicks','volume','search volume','impressions')
    own_kw, own_url, _ = cols(own); comp_kw, comp_url, comp_val = cols(comps)
    own_terms={r[own_kw].strip().lower() for r in own if r.get(own_kw)}
    agg=defaultdict(lambda: {'competitor_urls':Counter(),'value':0.0})
    for r in comps:
        kw=(r.get(comp_kw) or '').strip(); key=kw.lower()
        if not kw or key in own_terms: continue
        url=(r.get(comp_url) or '').strip()
        agg[kw]['competitor_urls'][url]+=1
        try: agg[kw]['value']+=float(r.get(comp_val) or 0)
        except Exception: pass
    out=[]
    for kw,data in agg.items():
        out.append({'missing_keyword':kw,'estimated_value':round(data['value'],2),'competitor_url_count':sum(data['competitor_urls'].values()),'top_competitor_urls':' | '.join(u for u,_ in data['competitor_urls'].most_common(5)),'recommended_action':'map_to_existing_page_or_create_new_target'})
    return sorted(out, key=lambda r:(float(r['estimated_value']), int(r['competitor_url_count'])), reverse=True)


def main():
    ap=argparse.ArgumentParser()
    ap.add_argument('mode', choices=['content-decay','serp-crossover','keyword-gap'])
    ap.add_argument('files', nargs='+')
    ap.add_argument('--output','-o', default='seo-opportunities.csv')
    ap.add_argument('--min-loss', type=float, default=0.20)
    ap.add_argument('--top-n', type=int, default=10)
    args=ap.parse_args()
    rows={'content-decay':content_decay,'serp-crossover':serp_crossover,'keyword-gap':keyword_gap}[args.mode](args)
    write_csv(args.output, rows)

if __name__=='__main__': main()
