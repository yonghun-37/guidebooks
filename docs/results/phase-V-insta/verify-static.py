"""시각자료 검사기 회귀와 작업 범위·원래 인터랙션 계약 보존 확인."""
import importlib.util
import json
from pathlib import Path
import subprocess
import tempfile
import sys
import re

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / 'scripts/tests'))
from test_check_site import CheckSiteTests, checker

checks = []
def ok(name, condition):
    assert condition, name
    checks.append(name)

fixture = CheckSiteTests()
fixture.setUp()
try:
    ok('그림 없는 페이지도 통과', not checker.check(root=fixture.root)['errors'])
    path = fixture.root / 'site/visual.html'
    def check_figure(content):
        path.write_text(content)
        return checker.check(root=fixture.root)['errors']
    ok('빈 캡션 거부', any('figcaption' in e for e in check_figure('<figure><svg aria-label="파일 흐름"></svg><figcaption> </figcaption></figure>')))
    ok('캡션 없는 그림 거부', any('figcaption' in e for e in check_figure('<figure><svg aria-label="파일 흐름"></svg></figure>')))
    ok('SVG 이름 누락 거부', any('SVG' in e for e in check_figure('<figure><svg><rect/></svg><figcaption>흐름</figcaption></figure>')))
    ok('자체 제목 있는 SVG 허용', not check_figure('<figure><svg role="img"><title>검수 흐름</title><rect/></svg><figcaption>검수 뒤 승인</figcaption></figure>'))
    ok('크롭용 중첩 SVG를 독립 그림으로 오인하지 않음', not check_figure('<figure><svg role="img"><title>크롭 비교</title><svg><use href="data:,"/></svg></svg><figcaption>크롭을 비교</figcaption></figure>'))
    ok('독립 img 역할인 중첩 SVG 이름 누락 거부', any('SVG' in e for e in check_figure('<figure><svg role="img"><title>큰 그림</title><svg role="img"><rect/></svg></svg><figcaption>구성</figcaption></figure>')))
    ok('img alt 누락 거부', any('대체 텍스트' in e for e in check_figure('<figure><img src="data:,"><figcaption>결과</figcaption></figure>')))
    ok('의미 있는 img alt 허용', not check_figure('<figure><img src="data:," alt="날짜와 출처를 배치한 카드"><figcaption>결과</figcaption></figure>'))
    fixture.write('research-blog/SOURCES.md', '### B001. 블로그 원출처')
    fixture.write('site-blog/index.html', '<figure><svg aria-label="제작 흐름"></svg><figcaption>제작 흐름 [B001]</figcaption></figure>')
    fixture.write('shelf/index.html', '<a href="blog/">블로그</a>')
    ok('site-blog 배포 경로·출처 지원', not checker.check(root=fixture.root, site='site-blog')['errors'])
    fixture.write('site-blog/index.html', '<p>[B999]</p>')
    ok('site-blog 미등록 출처 거부', any('미등록 출처 B999' in e for e in checker.check(root=fixture.root, site='site-blog')['errors']))
finally:
    fixture.doCleanups()

help_text = subprocess.run([sys.executable, str(ROOT / 'scripts/check_site.py'), '--help'], capture_output=True, text=True, check=True).stdout
ok('그림 수량 경고 옵션 제거', '--fig-warn' not in help_text)
# 원래의 사용자 입력·퀴즈·저장 키와 링크 계약은 그림 추가와 무관하게 유지한다.
for path in sorted((ROOT / 'site').rglob('*.html')):
    relative = path.relative_to(ROOT)
    original = subprocess.run(['git', 'show', 'HEAD:' + str(relative)], cwd=ROOT, capture_output=True, text=True, check=True).stdout
    now = checker.Page(path)
    with tempfile.TemporaryDirectory() as tmp:
        old_path = Path(tmp) / 'original.html'
        old_path.write_text(original)
        old = checker.Page(old_path)
    contract = lambda page: [(e.tag, {k:v for k,v in e.attrs.items() if (k.startswith('data-') and k != 'data-figure-type') or (e.tag in {'input','button','select','textarea'} and k in {'id','type','name','value','min','max','step'})}) for e in page.elements if any(k.startswith('data-') and k != 'data-figure-type' for k in e.attrs) or e.tag in {'input','button','select','textarea'}]
    ok(str(relative) + ' 인터랙션 계약 보존', contract(old) == contract(now))
    old_ids = {a['id'] for tag,a in old.nodes if 'id' in a and tag not in {'title','desc'}}
    new_ids = {a['id'] for _,a in now.nodes if 'id' in a}
    ok(str(relative) + ' 기존 앵커 보존', old_ids <= new_ids)
# 이전 신규 이미지 중 사용하지 않는 인물·로봇은 배포하지 않는다.
ok('의무 인물 삽화 파일 제거', not (ROOT/'site/assets/img/characters').exists())
ok('사용하지 않는 종이 로봇 파일 제거', not (ROOT/'site/assets/img/ai-examples/paper-robot.webp').exists())
result = {'passed': len(checks), 'checks': checks}
(ROOT/'docs/results/phase-V-insta/static-regression.json').write_text(json.dumps(result, ensure_ascii=False, indent=2) + '\n')
print('PASS', len(checks))
