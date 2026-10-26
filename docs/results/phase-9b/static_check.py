from pathlib import Path
from html.parser import HTMLParser
from urllib.parse import urlsplit,unquote
import json,re,hashlib
class Page(HTMLParser):
 def __init__(self,s):super().__init__();self.ids=[];self.links=[];self.feed(s)
 def handle_starttag(self,t,a):
  d=dict(a)
  if 'id' in d:self.ids.append(d['id'])
  for k in ['href','src']:
   if k in d:self.links.append(d[k])
root=Path.cwd();pages={p.resolve():Page(p.read_text()) for p in Path('site').rglob('*.html')}
own={p.resolve() for p in Path('site/chapters').glob('0[5-9]-*.html')}
errors=[];other=[];local=0;incoming=0
for path,doc in pages.items():
 if path in own:
  assert len(doc.ids)==len(set(doc.ids)),str(path)
  # 인라인 전용 JS도 실제 JS 파서로 검사한다.
  source=path.read_text();scripts=re.findall(r'<script>(.*?)</script>',source,re.S)
  for script in scripts:
   import subprocess
   run=subprocess.run(['node','--check','-'],input=script,text=True,capture_output=True);assert run.returncode==0,run.stderr
 for link in doc.links:
  url=urlsplit(link)
  if url.scheme or url.netloc:continue
  target=(path.parent/unquote(url.path)).resolve() if url.path else path
  if path in own:local+=1
  if path not in own and target in own:incoming+=1
  error=None
  if not target.exists():error='missing file'
  elif url.fragment and target in pages and unquote(url.fragment) not in pages[target].ids:error='missing anchor'
  if error:(errors if path in own or target in own else other).append({'page':str(path.relative_to(root)),'link':link,'error':error})
old=json.loads(Path('/tmp/phase9b-site-start.json').read_text())
legacy=['site/assets/sim/'+name for name in ['ch05.js','ch6-writing.js','ch7-cards.js','ch8-reels.js','ch9-pipeline.js']]
assert all(hashlib.sha256(Path(p).read_bytes()).hexdigest()==old[p] for p in legacy)
result={'scope':'이론 5~9장 내부 링크와 모든 페이지에서 담당 장으로 향하는 링크','outgoing_local':local,'incoming':incoming,'errors':errors,'unrelated_pending':other,'old_js_preserved':legacy,'inline_js_syntax':'passed'}
Path('docs/results/phase-9b/static-check.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
print(json.dumps({'outgoing':local,'incoming':incoming,'errors':errors,'unrelated_pending':len(other)},ensure_ascii=False));assert not errors
