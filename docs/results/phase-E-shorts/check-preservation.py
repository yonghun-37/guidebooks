"""교체 전 스냅샷·Git 본문과 최종 예시의 정책·수치·조작 구조를 대조한다."""
import ast
from collections import Counter
import hashlib
import json
from pathlib import Path
import re
import subprocess
from bs4 import BeautifulSoup

ROOT = Path(__file__).resolve().parents[3]
OUT = ROOT / 'docs/results/phase-E-shorts'
REV = '40997bce3fda926a4ffe0257f6cbff450e30a114'
BASE = json.loads((OUT / 'baseline.json').read_text())
checks, failures, notes = [], [], []
def check(name, okay, detail=None):
    checks.append(name)
    if not okay:
        failures.append({'check': name, 'detail': detail})

def numbers(tag):
    text = tag.get_text(' ', strip=True)
    text = re.sub(r'\[Y\d+\]', '', text)
    text = text.replace('자취생 10분 생존법', '가상 채널명')
    return re.findall(r'\d[\d,.]*(?:%|px|fps|p|분|초|원|MB|Mbps)?', text)

def source_numbers(soup):
    # 같은 순서의 각주가 속한 문장에서 정책·가격·계산 숫자를 대조한다.
    result = []
    for ref in soup.select('sup.footnote-ref'):
        block = ref.find_parent(['p', 'dd', 'td', 'figcaption', 'li'])
        result.append((ref.get_text(), numbers(block)))
    return result

for name, before in BASE.items():
    path = ROOT / name
    if not path.exists() or path.suffix != '.html':
        continue
    current = path.read_text()
    check(name + ': 각주 전체', sorted(re.findall(r'\[Y\d+\]', current)) == before['footnotes'])
    after_ids = sorted(re.findall(r'\bid="([^"]+)"', current))
    # 외부 앵커가 아닌 훅 그림 내부 이름 하나를 소재에 맞춰 바꿨다.
    missing = set(before['ids']) - set(after_ids)
    check(name + ': 기존 앵커', missing <= ({'moving-cable'} if name.endswith('03-hook.html') else set()), sorted(missing))
    soup = BeautifulSoup(current, 'html.parser')
    controls = [(t.name, dict(t.attrs)) for t in soup.select('input,select,button,textarea')]
    old_controls = [(t, a) for t, a in before['controls']]
    # 예문을 담은 문자열 value는 바뀔 수 있으나 숫자·동작 속성은 유지한다.
    def clean(rows):
        return [(tag, {k:v for k,v in attrs.items() if not (k == 'value' and isinstance(v,str) and not re.fullmatch(r'[\d.]+',v))}) for tag,attrs in rows]
    check(name + ': 입력·버튼 속성', clean(controls) == clean(old_controls))
    if name.startswith('site-shorts/') and '/samples/' not in name:
        old = subprocess.run(['git','show',REV+':'+name], cwd=ROOT, capture_output=True, text=True, check=True).stdout
        orig = BeautifulSoup(old, 'html.parser')
        check(name + ': 정책·수치 각주 문맥', source_numbers(orig) == source_numbers(soup), {'before':source_numbers(orig),'after':source_numbers(soup)} if source_numbers(orig) != source_numbers(soup) else None)
        old_sources = [(x.get('id'),x.get_text(' ',strip=True)) for x in orig.select('[id^="source-y"]')]
        new_sources = [(x.get('id'),x.get_text(' ',strip=True)) for x in soup.select('[id^="source-y"]')]
        check(name + ': 출처 원문 목록', old_sources == new_sources)
        links = lambda doc: sorted(x.get('href') for x in doc.select('a[href^="https:"]'))
        check(name + ': 외부 근거 링크', links(orig) == links(soup))

# 핵심 키트 로직은 example 함수 밖을 AST로 대조한다.
p = ROOT/'shorts-kit/write_script.py'
old = subprocess.run(['git','show',REV+':shorts-kit/write_script.py'],cwd=ROOT,capture_output=True,text=True,check=True).stdout
old_tree,new_tree = ast.parse(old),ast.parse(p.read_text())
for tree in [old_tree,new_tree]:
    tree.body = [x for x in tree.body if not (isinstance(x,ast.FunctionDef) and x.name=='example')]
check('키트: 예시 함수 밖 로직',ast.dump(old_tree)==ast.dump(new_tree))
for name in ['common.py','render.py','review.py','run_pipeline.py','upload.py','daily.py','oauth_setup.py','schedule_setup.py','tests/test_upload.py']:
    path=ROOT/'shorts-kit'/name
    check('키트: '+name+' 보존',hashlib.sha256(path.read_bytes()).hexdigest()==BASE['shorts-kit/'+name]['sha256'])
# JS 계산·이벤트 로직: 그림을 그리는 함수 외에는 문자열만 바꿨다.
for name in ['assets/operations.js','assets/y4b.js','assets/shorts.js','assets/catalog.js']:
    old=subprocess.run(['git','show',REV+':site-shorts/'+name],cwd=ROOT,capture_output=True,text=True,check=True).stdout
    new=(ROOT/'site-shorts'/name).read_text()
    def normalize(text):
        if name.endswith('y4b.js'):
            text=re.sub(r'    function scene\(ctx, time\) \{.*?\n    const paint =','    const paint =',text,flags=re.S)
        text=re.sub(r'/\*.*?\*/|//[^\n]*','',text,flags=re.S)
        text=re.sub(r"'(?:\\.|[^'\\])*'|\"(?:\\.|[^\"\\])*\"",'STRING',text)
        return re.sub(r'\s+','',text)
    check('JS 계산·이벤트: '+name,normalize(old)==normalize(new))
notes.append('moving-cable → moving-note는 훅 도식 내부 ID이며 재생·시간·선택 필드는 유지했다.')
notes.append('y4b.js scene()의 그리기 명령과 SVG 소재만 다시 그렸고 계산·시간축·이벤트는 그대로다.')
result={'checks':len(checks),'failures':failures,'notes':notes}
(OUT/'preservation-check.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
print(json.dumps({'checks':len(checks),'failures':[(f['check']) for f in failures]},ensure_ascii=False))
raise SystemExit(bool(failures))
