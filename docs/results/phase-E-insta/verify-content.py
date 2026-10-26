"""교체 전 스냅샷과 정책·각주·입력·퀴즈·게시 차단을 비교한다."""
from pathlib import Path
from html.parser import HTMLParser
from collections import Counter
import ast, hashlib, json, re
root=Path(__file__).resolve().parents[3]
before=Path('/tmp/e-insta-before')
checks=[]
def ok(name,condition):
 if not condition:raise AssertionError(name)
 checks.append(name)
class Page(HTMLParser):
 def __init__(self,text):super().__init__();self.nodes=[];self.feed(text)
 def handle_starttag(self,t,a):self.nodes.append((t,dict(a)))
for p in sorted((root/'site').rglob('*.html')):
 old=Page((before/p.relative_to(root)).read_text());new=Page(p.read_text())
 ids=lambda p:{a['id'] for _,a in p.nodes if 'id' in a}
 ok(str(p.relative_to(root))+' anchors',ids(old)<=ids(new))
 source=lambda p:Counter(a.get('href') for t,a in p.nodes if t=='a' and ('source-s' in a.get('href','') or a.get('href','').startswith('https://')))
 ok(str(p.relative_to(root))+' official links/footnotes',not (source(old)-source(new)))
 def controls(p):
  return [(t,{k:v for k,v in a.items() if (k.startswith('data-') and k not in {'data-explanation'}) or (t in {'input','button','select','textarea'} and k in {'id','type','name','value','min','max','step'})}) for t,a in p.nodes if any(k.startswith('data-') for k in a) or t in {'input','button','select','textarea'}]
 ok(str(p.relative_to(root))+' controls/storage/quiz flags',controls(old)==controls(new))
# API/권리/승인 로직을 바꾸지 않았다.
for name in ['publish.py','review.py','prepare_hosting.py','run_pipeline.py','fetch_news.py','common.py','audio.py','make_reel.py','daily.py','schedule_setup.py','token_check.py']:
 p=root/'starter-kit'/name
 ok(name+' unchanged',p.read_bytes()==(before/'starter-kit'/name).read_bytes())
class RemoveWords(ast.NodeTransformer):
 def visit_Constant(self,node):
  return ast.copy_location(ast.Constant(value='' if isinstance(node.value,str) else node.value),node)
for name in ['write_copy.py','render_cards.py']:
 norm=lambda text:ast.dump(RemoveWords().visit(ast.parse(text)),include_attributes=False)
 ok(name+' only string constants changed',norm((root/'starter-kit'/name).read_text())==norm((before/'starter-kit'/name).read_text()))
# 가격·모델 표의 숫자/문구를 통째로 보존한다.
for a,b in [('<section id="subscriptions"','<section id="'),('<div data-model-section>','</tbody></table></div>')]:
 old=(before/'site/ai-models.html').read_text();new=(root/'site/ai-models.html').read_text()
 if a=='<div data-model-section>':
  pattern=re.escape(a)+'.*?'+re.escape(b)
  ok('all model rows unchanged',re.findall(pattern,old,re.S)==re.findall(pattern,new,re.S))
# 기존 계산 숫자·입력 조건은 같은 채로 주제 문자열만 바꾼다.
for name in ['ch02.js','ch03.js','ch04.js','ch05.js','revenue-guide.js','analytics-v2.js','publishing.js','roadmap-v2.js','ai-guide.js']:
 p=root/'site/assets/sim'/name
 if not p.exists():p=root/'site/assets'/name
 ok(name+' calculations unchanged',p.read_bytes()==(before/p.relative_to(root)).read_bytes())
for name in ['news.json','copy.json','subtitles.srt','reel.mp4',*[f'card-{i:02d}.png' for i in range(1,6)]]:
 ok('sample mirror '+name,(root/'starter-kit/samples'/name).read_bytes()==(root/'site/assets/img/samples'/name).read_bytes())
copy=json.loads((root/'starter-kit/samples/copy.json').read_text());news=json.loads((root/'starter-kit/samples/news.json').read_text())
ok('sample synthetic safeguards',copy['synthetic'] is True and news['synthetic'] is True and all(a['synthetic'] for a in news['articles']))
ok('AI cover identified',copy['is_ai_generated'] is True and 'AI 생성' in copy['label'] and '예시 문안' in copy['caption'])
banned=re.compile(r'별빛|은솔|연습도서관|도서관|독서 모임|초록작업실|종이 재사용|달빛마을|산책 지도|종이 로봇|paper robot|flowerpot|library-evening|한 장 실험실|오늘의 발견|다음 발견|추가 대출|예약 도서|성인 회원|수요일 휴관',re.I)
hits=[]
for base in ['site','starter-kit']:
 for p in (root/base).rglob('*'):
  if not p.is_file() or any(s in p.parts for s in ('.venv','.cache','output','__pycache__','.pytest_cache')):continue
  if p.suffix not in ('.html','.js','.css','.svg','.md','.py','.xml','.yaml','.json','.srt','.txt'):continue
  if banned.search(p.read_text()):hits.append(str(p.relative_to(root)))
ok('old artificial examples zero',not hits)
result={'passed':len(checks),'checks':checks,'old_example_matches':hits}
(root/'docs/results/phase-E-insta/content-preservation.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
print('PASS',len(checks))
