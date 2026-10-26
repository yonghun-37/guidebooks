"""현재 사이트와 Pages 조립 경로의 링크·용어·인용·재생성 정합성을 검사한다."""
from pathlib import Path
from html.parser import HTMLParser
from collections import Counter
from urllib.parse import urlsplit, unquote
import hashlib, json, re, subprocess, sys
ROOT=Path(__file__).resolve().parents[3]
sys.path.insert(0,str(ROOT/'scripts'))
from build_appendices import Document, nodes, text, has_class, PAGES
class Page(HTMLParser):
 def __init__(self,p):
  super().__init__();self.nodes=[];self.feed(p.read_text())
 def handle_starttag(self,tag,attrs):self.nodes.append((tag,dict(attrs)))
pages={p:Page(p) for p in (ROOT/'site').rglob('*.html')}
errors=[];links=0;terms=0
ids={p:{a['id'] for _,a in page.nodes if 'id' in a} for p,page in pages.items()}
glossary={a['id'] for _,a in pages[ROOT/'site/glossary.html'].nodes if 'data-glossary-entry' in a}
for p,page in pages.items():
 for id_,n in Counter(a['id'] for _,a in page.nodes if 'id' in a).items():
  if n>1:errors.append(f'{p.name}: duplicate {id_}')
 for tag,a in page.nodes:
  for attr in ('href','src','poster'):
   if attr not in a:continue
   u=urlsplit(a[attr])
   if u.scheme or u.netloc:continue
   links+=1
   if a[attr].startswith('/'):errors.append(f'{p.name}: absolute {a[attr]}')
   target=(p.parent/unquote(u.path)).resolve() if u.path else p
   if target.is_dir():target=target/'index.html'
   if not target.is_file():errors.append(f'{p.name}: missing {a[attr]}');continue
   if u.fragment and target in ids and unquote(u.fragment) not in ids[target]:errors.append(f'{p.name}: anchor {a[attr]}')
  if 'data-term' in a:
   terms+=1
   if a['data-term'] not in glossary or a['href'].split('#')[-1]!=a['data-term']:errors.append(f'{p.name}: term {a}')
# 현재 통합 시작점의 원고 앵커와 35단계 키를 보존한다.
preserved=0
for p in PAGES:
 old=subprocess.run(['git','show','HEAD:'+str(p.relative_to(ROOT))],cwd=ROOT,capture_output=True,text=True,check=True).stdout
 old_ids=set(re.findall(r'\bid="([^"]+)"',old))
 missing=old_ids-ids[p]
 preserved+=len(old_ids)
 if missing:errors.append(f'{p.name}: removed anchors {sorted(missing)}')
step_keys={a['data-practice-check'] for p,page in pages.items() if p.parent.name=='practice' and p.name!='e2e.html' for _,a in page.nodes if 'data-practice-check' in a}
e2e_keys={a['data-practice-check'] for _,a in pages[ROOT/'site/practice/e2e.html'].nodes if 'data-practice-check' in a}
if len(step_keys)!=35 or step_keys!=e2e_keys:errors.append('practice/E2E step mismatch')
# Citation expectation is independent of generator traversal: follow each body footnote to its li.
cited=set();backlinks=0
for p in PAGES:
 source=p.read_text();notes=re.search(r'<aside class="source-notes".*?</aside>',source,re.S)
 if not notes:continue
 body=source[:notes.start()]+source[notes.end():]
 for anchor in set(re.findall(r'href="#(source-[^"]+)"',body)):
  note=next((m[0] for m in re.finditer(r'<li\b[^>]*>.*?</li>',notes[0],re.S) if f'id="{anchor}"' in m[0]),None)
  if note is None:
   if anchor != 'source-kit' or f'id="{anchor}"' not in notes[0]:errors.append(f'{p.name}: no footnote {anchor}')
   continue
  cited.update(re.findall(r'\bS\d{3}\b',re.sub('<[^>]*>',' ',note)));backlinks+=1
credits={id_.upper() for id_ in ids[ROOT/'site/credits.html'] if re.fullmatch('s[0-9]{3}',id_)}
if credits!=cited:errors.append(f'citation difference {credits^cited}')
# Pages workflow: shelf -> /, site -> /reels/, generated samples -> /progress/samples/.
for p in (ROOT/'shelf').rglob('*.html'):
 for _,a in Page(p).nodes:
  for attr in ('href','src','poster'):
   u=urlsplit(a.get(attr,''))
   if not a.get(attr) or u.scheme or u.netloc:continue
   logical=(Path('/tmp/phase9int-deployed')/p.relative_to(ROOT/'shelf').parent/unquote(u.path)).resolve()
   rel=logical.relative_to('/tmp/phase9int-deployed')
   if rel.parts and rel.parts[0]=='reels':target=ROOT/'site'/Path(*rel.parts[1:])
   elif rel.parts[:2]==('progress','samples'):target=ROOT/'starter-kit/samples'/rel.name
   else:target=ROOT/'shelf'/rel
   if target.is_dir():target=target/'index.html'
   links+=1
   if not target.is_file():errors.append(f'{p}: deployed {a[attr]}')
# Regeneration must preserve every current page; the retired practice generator must refuse writes.
tracked=list((ROOT/'site').rglob('*'))+[ROOT/'docs/results/phase-7w-verify-list.md']
before={p:hashlib.sha256(p.read_bytes()).hexdigest() for p in tracked if p.is_file()}
run=subprocess.run([sys.executable,'scripts/build_appendices.py'],cwd=ROOT,capture_output=True,text=True)
if run.returncode:errors.append(run.stderr)
changed=[str(p.relative_to(ROOT)) for p,digest in before.items() if hashlib.sha256(p.read_bytes()).hexdigest()!=digest]
if changed:errors.append(f'non-idempotent appendices {changed}')
guard=subprocess.run([sys.executable,'scripts/build_practice.py'],cwd=ROOT,capture_output=True,text=True)
if guard.returncode!=1 or '실행을 중지합니다' not in guard.stderr:errors.append('practice overwrite guard')
if any(hashlib.sha256(p.read_bytes()).hexdigest()!=d for p,d in before.items()):errors.append('generator changed current pages')
result=dict(html_pages=len(pages),internal_links_and_assets=links,term_links=terms,glossary_terms=len(glossary),cited_sources=len(cited),body_footnotes=backlinks,preserved_chapter_practice_anchors=preserved,practice_steps=len(step_keys),regeneration_stable=not changed,practice_overwrite_guard=guard.returncode==1,errors=errors)
(ROOT/'docs/results/phase-9-int/static-check.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
print(json.dumps(result,ensure_ascii=False,indent=2));raise SystemExit(bool(errors))
