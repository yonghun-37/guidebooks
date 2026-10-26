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
for path in SITE.joinpath('practice').glob('[0-9][0-9]-*.html'):
 cited.update(re.findall(r'\bS\d{3}\b',re.search(r'<aside class="source-notes".*?</aside>',path.read_text(),re.S)[0]))
credits={a['id'].upper() for _,a in pages[SITE/'credits.html'].nodes if re.fullmatch(r's\d{3}',a.get('id',''))}
if credits!=cited:errors.append(f'citation difference {credits^cited}')
if not cited<=source_ids:errors.append(f'unknown sources {cited-source_ids}')
samples=list((SITE/'assets/img/samples').iterdir()); size=sum(p.stat().st_size for p in samples)
for sample in samples:
 original=ROOT/'starter-kit/samples'/sample.name
 if original.is_file() and sample.read_bytes()!=original.read_bytes():errors.append(f'copied sample differs: {sample.name}')
if size>2_000_000:errors.append(f'samples total {size}>2MB')
# 공통 실습 단계/E2E/미확인 목록/기존 앵커 계약.
practice=list(SITE.joinpath('practice').glob('[0-9][0-9]-*.html'))
step_keys=set();menu_count=0
for path in practice:
 text=path.read_text(); nodes=pages[path].nodes
 for section in re.findall(r'<section class="chapter-block practice-step".*?</section>',text,re.S):
  key=re.search(r'data-step="([^"]+)"',section)[1];step_keys.add(key)
  for title in ('지금 하는 일','왜 하는지','따라 하기','이렇게 보이면 성공','이렇게 보이면?'):
   if f'<h3>{title}</h3>' not in section: errors.append(f'{path.name}: missing component {key} {title}')
  if 'data-os-panel="windows"' not in section or 'data-os-panel="macos"' not in section: errors.append(f'{path.name}: missing OS panel')
 for block in re.findall(r'<div class="menu-unverified".*?</div>',text,re.S):
  menu_count+=1
  if 'data-verify="app-menu"' not in block or '앱 버전에 따라 이름이 다를 수 있음 — 보통 이런 이름' not in block or '공식 도움말' not in block:errors.append(f'{path.name}: menu verification contract')
 if '(실습)' not in text or '2026년 10월 조사 기준' not in text:errors.append(f'{path.name}: missing track/date')
e2e={a['data-practice-check'] for _,a in pages[SITE/'practice/e2e.html'].nodes if 'data-practice-check' in a}
if step_keys!=e2e:errors.append(f'E2E mismatch {step_keys^e2e}')
verify=(ROOT/'docs/results/phase-7w-verify-list.md').read_text()
if len(re.findall(r'^\| \[실습',verify,re.M))!=menu_count:errors.append('7v menu list mismatch')
import subprocess
for path in SITE.rglob('*.html'):
 relative=str(path.relative_to(ROOT))
 previous=subprocess.run(['git','show','HEAD:'+relative],capture_output=True,text=True)
 if previous.returncode:continue
 old=set(re.findall(r'(?<![\w-])id="([^"]+)"',previous.stdout))
 now={a['id'] for _,a in pages[path].nodes if 'id' in a}
 if old-now:errors.append(f'old anchor removed {relative}: {old-now}')
result=dict(html_pages=len(pages),practice_steps=len(step_keys),unverified_menus=menu_count,internal_links_and_assets=link_count,term_links=terms,glossary_terms=len(glossary_ids),fact_references=facts,cited_sources=len(cited),sample_bytes=size,errors=errors)
(ROOT/'docs/results/phase-7w/static-check.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
print(json.dumps(result,ensure_ascii=False,indent=2))
raise SystemExit(bool(errors))
