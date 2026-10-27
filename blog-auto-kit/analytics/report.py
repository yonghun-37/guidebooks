"""고정 지표와 확인할 글을 주간 보고서로 묶는다."""
from html import escape
from pathlib import Path
import re


def _needs_review(post, today):
    """기한 또는 지난 기준일의 금액·날짜 내용을 확인한다."""
    doc = post.get('doc', post)
    due = post.get('review_due') or doc.get('review_due')
    if due:
        return due < today
    as_of = doc.get('as_of', '')
    text = str(doc.get('markdown', '')) + ' ' + str(doc.get('title', ''))
    return bool(as_of and as_of < today and re.search(r'\d[\d,]*(?:\s*원|\s*년|[-./]\d)', text))


def build_report(root, store, today):
    """모의 지표와 갱신 대상 목록을 작성한다."""
    base = Path(root) / 'output' / 'analytics'
    base.mkdir(parents=True, exist_ok=True)
    posts = store.all('posts')
    outdated = [p for p in posts if _needs_review(p, today)]
    rows = ''.join('<li>' + escape(str(p.get('title', p.get('id', '제목 없음')))) + '</li>' for p in outdated) or '<li>없음</li>'
    report = '<!doctype html><html lang="ko"><meta charset="utf-8"><h1>주간 보고서 (모의)</h1>'
    report += f'<p>기준일 {escape(today)}. 방문 120, 검색 클릭 20: 모두 가상 지표.</p>'
    report += '<p>GA4는 속성 시간대, GSC는 태평양 시간 기준이며 반영 지연과 빈 행을 확인하세요.</p>'
    report += '<p>광고·제휴 예상액: 미집계 / 확정액: 미집계 / 실제 입금: 미확인</p>'
    report += f'<h2>기준일이 지난 금액·날짜 글</h2><ul>{rows}</ul>'
    report += '<h2>다음 글감 점수 (모의)</h2><p>독자 질문 3 + 공식 근거 2 + 기존 경험 1 = 6점</p></html>'
    path = base / 'weekly.html'
    path.write_text(report, encoding='utf-8', newline='\n')
    return [str(path)]
