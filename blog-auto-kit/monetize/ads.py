"""광고 준비 자료와 위치 예시를 만든다."""
from html import escape
from pathlib import Path
import re
from core.files import write_json


def build_ads(root, config, today):
    """수동 점검표, ads.txt, 광고 위치, 모의 보고서를 생성한다."""
    base = Path(root) / 'output' / 'ads'
    base.mkdir(parents=True, exist_ok=True)
    n = int(config.get('ad_after_h2', 2))
    if n < 1: raise ValueError('광고 위치는 1 이상이어야 합니다')
    article = str(config.get('article_html', '<h2>첫째</h2><p>본문</p><h2>둘째</h2><p>본문</p>'))
    matches = list(re.finditer(r'</h2\s*>', article, re.I))
    if len(matches) >= n:
        pos = matches[n - 1].end()
        article = article[:pos] + '<aside>광고 위치 예시 (실제 광고 없음)</aside>' + article[pos:]
    publisher = config.get('publisher_id', 'pub-REPLACE_ME')
    metrics = {'mock': True, 'date': today, 'timezone': 'Asia/Seoul', 'page_views': 100,
               'estimated_usd': '0.12', 'final_usd': '0.00', 'paid_usd': '0.00'}
    write_json(base / 'metrics.json', metrics)
    files = {'checklist.txt': '자체 콘텐츠·HTML 관리권·탐색·정책·개인정보처리방침 확인\n'
             '최소 글 수·방문자: 공식 기준 없음; 개별 심사 확인\n'
             'ads.txt 권장, 실제 판매자 정보 확인\n아동 광고 설정과 코드 유형 확인\n'
             '한국 가입 연령: 만 19세 이상. 한국어 AdSense 이용약관을 확인하세요.\n',
             'ads.txt': '# BX025 공식 형식 예시; 실제 계정 행으로 교체 후 루트에 게시\n'
                        f'google.com, {publisher}, DIRECT, f08c47fec0942fa0\n',
             'layout.html': article,
             'report.html': f'<h1>모의 광고 보고서</h1><p>기준일 {escape(today)} · Asia/Seoul · 아래 숫자는 고정 가상 데이터입니다.</p>'
                            '<table><tr><th>페이지뷰</th><th>예상 USD</th><th>확정 USD</th><th>실입금 USD</th></tr>'
                            '<tr><td>100</td><td>0.12</td><td>0.00</td><td>0.00</td></tr></table>'}
    for name, value in files.items(): (base / name).write_text(value, encoding='utf-8', newline='\n')
    return [str(base / name) for name in files] + [str(base / 'metrics.json')]
