"""심화편 전용: A 출처는 기존 check_site의 Y 출처 검사와 별도로 검증한다."""
from pathlib import Path
from html.parser import HTMLParser
import re,json,hashlib,subprocess
ROOT=Path(__file__).resolve().parents[3]
class Page(HTMLParser):
 def __init__(self,text):
  super().__init__();self.nodes=[];self.feed(text)
 def handle_starttag(self,tag,attrs):self.nodes.append((tag,dict(attrs)))
s=ROOT/'site-shorts/advanced'; sources=(ROOT/'research-advanced/SOURCES.md').read_text()
registered={k:(title,url) for k,title,url in re.findall(r'### (A\d{3})\. ([^\n]+)\n\n- URL: ([^\n]+)',sources)}
errors=[];pages=[];used=set()
for p in sorted(s.glob('*.html')):
 text=p.read_text();page=Page(text);ids=[a['id'] for _,a in page.nodes if 'id' in a]
 if len(ids)!=len(set(ids)):errors.append(f'{p.name}: duplicate ids')
 faqs=[a for tag,a in page.nodes if tag=='details' and re.fullmatch('faq-[1-5]',a.get('id',''))]
 if len(faqs)!=5:errors.append(f'{p.name}: FAQ count')
 questions=[a for _,a in page.nodes if 'data-question' in a]
 if len(questions)!=3:errors.append(f'{p.name}: quiz count')
 citations=set(re.findall(r'\[(A\d{3})\]',text));used.update(citations)
 for k in citations:
  if k not in registered or f'id="source-{k.lower()}"' not in text:errors.append(f'{p.name}: source {k}')
  elif registered[k][1].replace('&','&amp;') not in text:errors.append(f'{p.name}: source URL {k}')
 for needle in ['이 장에서 만드는 것','이렇게 보이면 성공','확인할 점','비용 · 편당과 한 달','data-os-tab="windows"','data-os-tab="macos"','지금 할 일' if p.stem!='e2e' else 'data-advanced-reset']:
  if needle not in text:errors.append(f'{p.name}: missing {needle}')
 for banned in ['Canva','미리캔버스','CapCut','Clipchamp','Hermes','ADV-','Phase']:
  if banned in text:errors.append(f'{p.name}: banned {banned}')
 pages.append({'page':p.name,'faq':len(faqs),'quiz':len(questions),'figures':sum(t=='figure' for t,a in page.nodes),'sources':len(citations)})
assert len(pages)==11
before_path=Path(__file__).with_name('protected-before.json');before=json.loads(before_path.read_text())
protected={k:v for k,v in before.items() if k.split('/')[0] in ['auto-kit','shorts-kit','starter-kit','blog-kit','research-advanced']}
# The concurrently owned books/research are intentionally not asserted against a global snapshot.
for k,v in protected.items():
 if not (ROOT/k).is_file() or hashlib.sha256((ROOT/k).read_bytes()).hexdigest()!=v:errors.append('protected changed: '+k)
for name in ['assets/book.css','assets/practice.js','assets/sim/common.js']:
 path='site-shorts/'+name;old=subprocess.check_output(['git','show','HEAD:'+path],cwd=ROOT)
 if old!=(ROOT/path).read_bytes():errors.append('common asset changed: '+path)
result={'pages':pages,'a_sources':len(used),'quiz_questions':sum(p['quiz'] for p in pages),'figures':sum(p['figures'] for p in pages),'protected_files':len(protected),'errors':errors}
Path(__file__).with_name('content-check.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
# Keep only the meaningful ownership snapshot, without unrelated concurrent work.
before_path.write_text(json.dumps(protected,ensure_ascii=False,indent=2)+'\n')
print(json.dumps(result,ensure_ascii=False,indent=2));raise SystemExit(bool(errors))
