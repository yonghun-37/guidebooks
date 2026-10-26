#!/usr/bin/env python3
"""담당 12페이지의 링크·앵커·단계/E2E·각주를 표준 라이브러리로 검사한다."""
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urlsplit, unquote
import re, json, hashlib

ROOT=Path(__file__).resolve().parents[3];OUT=Path(__file__).parent
class Page(HTMLParser):
    def __init__(self,path):
        super().__init__();self.ids=[];self.refs=[];self.keys=[];self.screens=[];self.steps=[];self.faq=[]
        self.feed(path.read_text())
    def handle_starttag(self,tag,attrs):
        a=dict(attrs)
        if 'id' in a:self.ids.append(a['id'])
        for key in ('href','src'):
            if key in a:self.refs.append(a[key])
        if 'data-step' in a:self.steps.append(a['data-step'])
        if 'data-practice-check' in a:self.keys.append(a['data-practice-check'])
        if 'data-screen' in a:self.screens.append(a['data-screen'])
pages={p:Page(p) for p in sorted((ROOT/'site/practice').glob('*.html'))}
count=0;errors=[]
for p,page in pages.items():
    if len(page.ids)!=len(set(page.ids)):errors.append(f'duplicate id: {p.name}')
    for ref in page.refs:
        u=urlsplit(ref)
        if u.scheme or u.netloc or not ref:continue
        target=(p.parent/unquote(u.path)).resolve() if u.path else p
        count+=1
        if not target.exists():errors.append(f'{p.name}: missing {ref}');continue
        if u.fragment and target.suffix=='.html':
            dest=pages.get(target) or Page(target)
            if unquote(u.fragment) not in dest.ids:errors.append(f'{p.name}: missing anchor {ref}')
    old=Path('/tmp/phase9d-before')/p.name
    if old.exists():
        removed=set(Page(old).ids)-set(page.ids)
        if removed:errors.append(f'{p.name}: removed anchors {removed}')
keys=[key for p,page in pages.items() if p.name!='e2e.html' for key in page.keys]
e2e=pages[ROOT/'site/practice/e2e.html'].keys
assert len(keys)==35 and len(keys)==len(set(keys)) and sorted(keys)==sorted(e2e)
screens=sum(len(p.screens) for p in pages.values());assert screens==18
assert all(len(p.keys)==len(p.steps) for f,p in pages.items() if f.name!='e2e.html')
results={'pages':len(pages),'local_references':count,'preserved_step_keys':len(keys),'documented_app_menu_blocks':screens,'errors':errors,'sha256':{str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest() for p in pages}}
(OUT/'static-check.json').write_text(json.dumps(results,ensure_ascii=False,indent=2)+'\n')
print(json.dumps({k:v for k,v in results.items() if k!='sha256'},ensure_ascii=False))
assert not errors
