#!/usr/bin/env python3
"""전체 정적 사이트의 링크·앵커·구조·연구 참조·부록 정합성 검사."""
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urlsplit, unquote
from collections import Counter
import re, json, hashlib
ROOT=Path(__file__).resolve().parents[3]
SITE=ROOT/'site'
class Page(HTMLParser):
 def __init__(self,path):
  super().__init__(); self.path=path; self.nodes=[]; self.feed(path.read_text())
 def handle_starttag(self,tag,attrs): self.nodes.append((tag,dict(attrs)))
pages={p:Page(p) for p in SITE.rglob('*.html')}
errors=[]; link_count=0; terms=0; facts=0
known_facts=set(re.findall(r'^\| ([A-Z]+-\d+) \|',(ROOT/'research/FACT-SHEET.md').read_text(),re.M))
glossary_ids={a['id'] for _,a in pages[SITE/'glossary.html'].nodes if 'data-glossary-entry' in a}
source_ids=set(re.findall(r'^### (S\d+)\.',(ROOT/'research/SOURCES.md').read_text(),re.M))
cited=set()
for path,page in pages.items():
 ids=[a['id'] for _,a in page.nodes if 'id' in a]
 for id_,n in Counter(ids).items():
  if n>1: errors.append(f'{path.name}: duplicate {id_}')
 if 'fact-pending' in path.read_text():errors.append(f'{path.name}: unresolved fact')
 for tag,a in page.nodes:
  for field in ['href','src','poster']:
   if field not in a:continue
   u=urlsplit(a[field]);
   if u.scheme or u.netloc:continue
   if a[field].startswith('/'):errors.append(f'{path.name}: absolute internal {a[field]}');continue
   target=(path.parent/unquote(u.path)).resolve() if u.path else path
   link_count+=1
   if not target.is_file(): errors.append(f'{path.name}: missing {a[field]}');continue
   if u.fragment and target.suffix=='.html':
    target_ids={attrs.get('id') for _,attrs in pages[target].nodes}
    if unquote(u.fragment) not in target_ids:errors.append(f'{path.name}: missing anchor {a[field]}')
  if 'data-term' in a:
   terms+=1
   if a.get('data-term') not in glossary_ids or a.get('href','').split('#')[-1]!=a['data-term']: errors.append(f'{path.name}: glossary mismatch {a}')
  for id_ in a.get('data-fact-id','').split():
   facts+=1
   if id_ not in known_facts:errors.append(f'{path.name}: unknown fact {id_}')
 if path.parent.name=='chapters' and path.name[:2].isdigit():
  num=int(path.name[:2]); notes=re.search(r'<aside class="source-notes".*?</aside>',path.read_text(),re.S)[0]
  cited.update(re.findall(r'\bS\d{3}\b',notes))
  if 2<=num<=14:
   blocks=[a['data-block'] for _,a in page.nodes if 'data-block' in a]
   if blocks!=['question','figure','principle','simulator','case','workshop','story','summary','quiz']:errors.append(f'{path.name}: wrong block order {blocks}')
  for hook in ['data-chapter-meta','data-chapter-pager']:
   if not any(hook in a for _,a in page.nodes):errors.append(f'{path.name}: missing hook {hook}')
credits={a['id'].upper() for _,a in pages[SITE/'credits.html'].nodes if re.fullmatch(r's\d{3}',a.get('id',''))}
if credits!=cited:errors.append(f'citation difference {credits^cited}')
if not cited<=source_ids:errors.append(f'unknown sources {cited-source_ids}')
samples=list((SITE/'assets/img/samples').iterdir()); size=sum(p.stat().st_size for p in samples)
for sample in samples:
 original=ROOT/'starter-kit/samples'/sample.name
 if original.is_file() and sample.read_bytes()!=original.read_bytes():errors.append(f'copied sample differs: {sample.name}')
if size>2_000_000:errors.append(f'samples total {size}>2MB')
result=dict(html_pages=len(pages),internal_links_and_assets=link_count,term_links=terms,glossary_terms=len(glossary_ids),fact_references=facts,cited_sources=len(cited),sample_bytes=size,errors=errors)
(ROOT/'docs/results/phase-5d/static-check.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
print(json.dumps(result,ensure_ascii=False,indent=2))
raise SystemExit(bool(errors))
