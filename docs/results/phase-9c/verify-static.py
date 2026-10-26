"""저장소 루트에서 python3 docs/results/phase-9c/verify-static.py."""
from pathlib import Path
from html.parser import HTMLParser
from urllib.parse import urlsplit, unquote
from collections import Counter
import json, subprocess

ROOT = Path.cwd()
OUT = ROOT / 'docs/results/phase-9c'
FILES = sorted((ROOT / 'site/chapters').glob('1[0-4]-*.html'))
class Page(HTMLParser):
    def __init__(self, text):
        super().__init__(); self.ids=[]; self.links=[]; self.feed(text)
    def handle_starttag(self, tag, attrs):
        data=dict(attrs)
        if 'id' in data:self.ids.append(data['id'])
        for key in ('href','src'):
            if key in data:self.links.append(data[key])
errors=[]; count=0; old_count=0; cache={}
for file in FILES:
    page=Page(file.read_text());cache[file]=page
    for id,n in Counter(page.ids).items():
        if n>1: errors.append(f'{file.name}: duplicate {id}')
    previous=subprocess.run(['git','show',f'HEAD:{file.relative_to(ROOT)}'],capture_output=True,text=True,check=True).stdout
    old=Page(previous).ids;old_count+=len(old)
    for id in set(old)-set(page.ids):errors.append(f'{file.name}: missing old anchor {id}')
    for href in page.links:
        url=urlsplit(href)
        if url.scheme or url.netloc:continue
        if href.startswith('/'):errors.append(f'{file.name}: absolute internal {href}')
        target=(file.parent/unquote(url.path)).resolve() if url.path else file
        count+=1
        if not target.exists():errors.append(f'{file.name}: missing {href}');continue
        if url.fragment and target.suffix=='.html':
            parsed=cache.setdefault(target,Page(target.read_text()))
            if unquote(url.fragment) not in parsed.ids:errors.append(f'{file.name}: missing fragment {href}')
report={'pages':len(FILES),'internal_links_assets':count,'old_anchors_preserved':old_count,'errors':errors}
(OUT/'static-check.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
print(json.dumps(report,ensure_ascii=False));assert not errors
