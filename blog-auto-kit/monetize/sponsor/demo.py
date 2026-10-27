"""가상 협찬의 기록과 보고 자료를 만든다."""
import csv
from html import escape
from pathlib import Path
from .ledger import create_inquiry, transition

TAX_GUIDE = 'https://www.nts.go.kr/nts/cm/cntnts/cntntsView.do?cntntsId=7890&mi=6610'
RECORDS = {
    'reviewing': {'product_safety': '가상 A 모델 분류·리콜 확인', 'ai_allowed': False, 'child_privacy': '아이 신상·사진 요구 없음', 'disclosure': '첫 문단 상품 무료제공 표시', 'deadline': '2026-11-10', 'settlement': '현금 없음, 현물 가액 별도 확인', 'rights': '블로그 1회 게시; 2차 이용 별도 동의'},
    'accepted': {'agreement': '가상 제안 조건 수락, 실제 회신 없음'},
    'contracted': {'contract_version': '가상 계약 v1', 'cash': '0원', 'goods': '가상 그림책꽂이 1개', 'return_terms': '반납 없음', 'deadlines': '작성 11월 5일, 확인 11월 8일', 'revision_scope': '사실관계 1회', 'rights': '블로그 게시만', 'cancellation': '위험 발견 시 중단', 'payment': '현금 지급 없음'},
    'received': {'model': '가상 A', 'condition': '파손 없음(가상)', 'received_date': '2026-10-27', 'experience': '가상 사람의 정리 경험 시연', 'goods_valuation': '가상 제공 명세 확인, 실제 가액 미확정'},
    'writing': {'authoring_path': '사람 작성(가상 시연)', 'experience': '가상 사람이 책을 정리한 경험', 'photos': '직접 만든 그림, 아이 사진 없음', 'sources': '제품 분류 및 리콜 자료 확인(가상)', 'disclosure': '첫 문단 상품 무료제공'},
    'brand_review': {'feedback': '가상 광고주 사실관계 확인; 외부 회신 없음', 'version': '가상 초안 v1', 'count': 1},
}


def _prepare(store, today):
    """두 가상 문의를 거절 또는 광고주 확인까지 기록한다."""
    for key, brand in [('blanket', '포근담요'), ('shelf', '도담')]:
        if store.get('sponsors', key) is None:
            create_inquiry(store, key, {'advertiser': brand, 'contact': '가상 연락처', 'offer': '가상 제품', 'channel': '블로그', 'content_id': 'sponsor' if key == 'shelf' else 'blanket'}, today)
    if store.get('sponsors', 'blanket')['state'] == 'inquiry':
        transition(store, 'blanket', 'declined', {'reason': '영아 수면 안전 충돌', 'notice': '외부 회신 없음', 'return_terms': '해당 없음', 'cost_agreement': '해당 없음'}, today)
    if store.get('sponsors', 'shelf')['state'] == 'inquiry':
        for state, records in RECORDS.items():
            transition(store, 'shelf', state, records, today)


def _media_kit(base):
    """가상의 독자와 기간이 붙은 모의 미디어킷을 쓴다."""
    text = '''<!doctype html><html lang="ko"><meta charset="utf-8"><h1>가상 미디어킷</h1>
<p>주제: 육아·교육과 집 놀이 / 독자: 영유아 보호자 / 기간: 2026-10-01~2026-10-27</p>
<p>아래 숫자는 실제 측정치가 아닌 고정 모의 지표입니다.</p>
<table><tr><th>방문(모의)</th><th>검색 클릭(모의)</th></tr><tr><td>120</td><td>20</td></tr></table>
<p>대표글: 2026 부모급여·아동수당 정리 / 제공 형식: 블로그 글과 직접 제작 그림</p>
<p>연락처: 운영자가 실제 주소 입력 / 아이 개인정보는 포함하지 않습니다.</p></html>'''
    path = base / 'media-kit.html'
    path.write_text(text, encoding='utf-8', newline='\n')
    return path


def _tax_csv(base, today, entries):
    """현금·현물·실입금과 평가 근거를 구분해 내보낸다."""
    path = base / 'tax.csv'
    fields = ['date', 'cash', 'goods', 'valuation_basis', 'return_terms', 'costs', 'withholding', 'paid_amount', 'evidence', 'tax_guide']
    settled = next((e['records'] for e in reversed(entries) if e['state'] == 'settled'), {})
    pending = next((e['records'] for e in reversed(entries) if e['state'] == 'settlement_pending'), {})
    received = next((e['records'] for e in reversed(entries) if e['state'] == 'received'), {})
    contracted = next((e['records'] for e in reversed(entries) if e['state'] == 'contracted'), {})
    row = {'date': settled.get('paid_at', received.get('received_date', today)), 'cash': '0원(가상)', 'goods': '그림책꽂이 1개(가상)', 'valuation_basis': '제공 명세 확인; 실제 가액 미확정', 'withholding': pending.get('withholding', '해당 여부 확인'), 'paid_amount': settled.get('paid_amount', '미입금'), 'evidence': settled.get('evidence', '가상 계약 v1'), 'tax_guide': TAX_GUIDE}
    row.update(return_terms=contracted.get('return_terms', '확인 필요'), costs=pending.get('costs', '확인 필요'))
    with path.open('w', encoding='utf-8', newline='') as stream:
        writer = csv.DictWriter(stream, fieldnames=fields, lineterminator='\n'); writer.writeheader(); writer.writerow(row)
    return path


def export_reports(root, store, today):
    """현재 대장 기준으로 보고서와 세금 기록을 다시 만든다."""
    base = Path(root) / 'output' / 'sponsor'; base.mkdir(parents=True, exist_ok=True)
    rows = store.all('sponsors'); shelf = store.get('sponsors', 'shelf') or {}
    history = shelf.get('history', [])
    published = next((e['records'] for e in reversed(history) if e['state'] == 'published'), {})
    url = escape(str(published.get('url', '발행 전 또는 공개 확인 필요')))
    report = base / 'advertiser-report.html'
    report.write_text('<!doctype html><html lang="ko"><meta charset="utf-8"><h1>광고주 보고서 (가상)</h1><p>외부 회신 없음; 개인정보 제외. 지표는 고정 모의값: 방문 120, 검색 클릭 20.</p><p>공개 주소: ' + url + '</p><p>기간: 2026-10-01~2026-10-27</p></html>', encoding='utf-8', newline='\n')
    ledger = base / 'ledger.csv'
    with ledger.open('w', encoding='utf-8', newline='') as stream:
        writer = csv.DictWriter(stream, fieldnames=['id', 'content_id', 'state'], lineterminator='\n'); writer.writeheader()
        writer.writerows({key: row.get(key, '') for key in ('id', 'content_id', 'state')} for row in rows)
    return [str(_media_kit(base)), str(report), str(_tax_csv(base, today, history)), str(ledger)]


def run_sponsor_demo(root, store, today):
    """거절과 광고주 확인까지 가상 사례를 기록한다."""
    _prepare(store, today)
    return export_reports(root, store, today)
