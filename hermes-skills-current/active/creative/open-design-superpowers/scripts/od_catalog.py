#!/usr/bin/env python3
"""Search/Open Design library for Hermes skills.
Usage:
  python scripts/od_catalog.py summary
  python scripts/od_catalog.py search "saas dashboard linear"
  python scripts/od_catalog.py show skill frontend-design
  python scripts/od_catalog.py show system linear-app
  python scripts/od_catalog.py show craft anti-ai-slop
"""
from pathlib import Path
import sys, re, yaml, json
ROOT = Path('/home/hermes/.hermes/vendor/open-design')

def frontmatter(path):
    txt=path.read_text(errors='ignore')
    body=txt
    fm={}
    if txt.startswith('---'):
        m=re.search(r'\n---\s*\n', txt[3:])
        if m:
            try: fm=yaml.safe_load(txt[3:m.start()+3]) or {}
            except Exception: fm={}
            body=txt[m.end()+3:]
    return fm, body

def compact(s,n=180): return ' '.join(str(s or '').split())[:n]

def skills():
    for p in sorted((ROOT/'skills').glob('*/SKILL.md')):
        fm, body=frontmatter(p); od=fm.get('od') if isinstance(fm.get('od'),dict) else {}
        yield {'kind':'skill','name':fm.get('name') or p.parent.name,'path':str(p),'mode':od.get('mode','prototype'),'scenario':od.get('scenario') or fm.get('scenario') or od.get('category') or 'general','desc':compact(fm.get('description') or fm.get('en_description') or body,240)}

def systems():
    for p in sorted((ROOT/'design-systems').glob('*/DESIGN.md')):
        lines=p.read_text(errors='ignore').splitlines(); title=lines[0].lstrip('# ').strip() if lines else p.parent.name
        text=' '.join(lines[:25])
        yield {'kind':'system','name':p.parent.name,'path':str(p),'mode':'design-system','scenario':'brand','desc':compact(title+' '+text,260)}

def crafts():
    for p in sorted((ROOT/'craft').glob('*.md')):
        if p.name=='README.md': continue
        txt=p.read_text(errors='ignore')
        yield {'kind':'craft','name':p.stem,'path':str(p),'mode':'craft','scenario':'craft','desc':compact(txt,220)}

def score(item, terms):
    hay=(item['name']+' '+item['mode']+' '+item['scenario']+' '+item['desc']).lower()
    return sum(3 if t in item['name'].lower() else 1 for t in terms if t in hay)

def search(q):
    terms=[t.lower() for t in re.findall(r'[a-zA-Z0-9_-]+', q)]
    items=list(skills())+list(systems())+list(crafts())
    ranked=sorted(((score(i,terms),i) for i in items), key=lambda x:(x[0], x[1]['kind']=='system'), reverse=True)
    return [i for sc,i in ranked if sc>0][:30]

def show(kind,name):
    base={'skill':ROOT/'skills'/name/'SKILL.md','system':ROOT/'design-systems'/name/'DESIGN.md','craft':ROOT/'craft'/(name+'.md')}.get(kind)
    if not base or not base.exists(): raise SystemExit(f'not found: {kind} {name}')
    print(base.read_text(errors='ignore'))

if __name__=='__main__':
    cmd=sys.argv[1] if len(sys.argv)>1 else 'summary'
    if cmd=='summary':
        print(json.dumps({'root':str(ROOT),'skills':len(list(skills())),'design_systems':len(list(systems())),'craft':len(list(crafts()))},indent=2))
    elif cmd=='search':
        for i in search(' '.join(sys.argv[2:])):
            print(f"{i['kind']:6} {i['name']:32} {i['mode']:14} {i['scenario']:14} {i['desc']}")
    elif cmd=='show': show(sys.argv[2], sys.argv[3])
    else: raise SystemExit(__doc__)
