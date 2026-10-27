"""협찬 대장에 실제 승인과 서버 상태 확인을 연결한다."""
from core.files import json_text
from core.hashes import digest
from monetize.sponsor.ledger import transition
from monetize.sponsor.demo import export_reports


def record_sponsor_approval(root, store, approval, today):
    records = {'content_hash': approval['hash'], 'reviewer': approval['reviewer'],
               'reviewed_at': today}
    transition(store, 'shelf', 'human_approval', records, today)
    transition(store, 'shelf', 'approved', {'approval_hash': approval['hash'],
               'allowed_at': today, 'destination': 'mock'}, today)
    export_reports(root, store, today)


def record_sponsor_remote(root, store, row, today):
    sponsor = store.get('sponsors', 'shelf')
    if not sponsor:
        return
    if row['status'] == 'future' and sponsor['state'] == 'approved':
        transition(store, 'shelf', 'scheduled', {'post_id': row['post_id'],
                   'scheduled_at': row['server_date'], 'timezone': 'Asia/Seoul',
                   'server_status': 'future'}, today)
    if row['status'] == 'publish' and sponsor['state'] in ('scheduled', 'approved'):
        contract_hash = sponsor_material(store)
        transition(store, 'shelf', 'published', {'url': row['url'],
                   'published_at': row['server_date'], 'contract_hash': contract_hash,
                   'disclosure': row['doc']['commercial_relations']}, today)
    export_reports(root, store, today)


def settle_sponsor(root, store, today):
    if store.get('sponsors', 'shelf', {}).get('state') != 'published':
        raise ValueError('공개 상태 확인 전 → status --sample sponsor --advance-days 2를 실행하세요')
    transition(store, 'shelf', 'reported', {'period': '2026-10-01~2026-10-27',
               'metrics_definition': 'mock 방문 120·검색 클릭 20',
               'allowed_data': '집계만', 'privacy_checked': True}, today)
    transition(store, 'shelf', 'settlement_pending', {'cash': 0, 'goods': '가상 그림책꽂이',
               'return_terms': '반납 없음', 'withholding': '세무 상담 확인',
               'invoice': '해당 여부 확인', 'payment_due': '2026-11-10'}, today)
    transition(store, 'shelf', 'settled', {'paid_at': today, 'paid_amount': '0(현금 없음)',
               'goods': '가상 그림책꽂이', 'expenses': '가상 기록 없음',
               'evidence': '가상 제공 명세 v1', 'tax_check': '국세청126 확인 과제'}, today)
    return export_reports(root, store, today)


def invalidate_sponsor(store, doc, today):
    """수정한 협찬 원고를 광고주 확인 전 작성 단계로 되돌린다."""
    row = store.get('sponsors', 'shelf', {})
    if row.get('state') in ('approved', 'scheduled', 'human_approval', 'brand_review'):
        transition(store, 'shelf', 'writing', {'authoring_path': '사람 수정', 'experience': doc.get('experience') or '사람 확인 필요', 'photos': '원고 미디어 재검토', 'sources': '원고 출처 재검토', 'disclosure': '원고 표시 재검토'}, today)


def require_sponsor_approval(store, row):
    """협찬 대장과 사람 승인 해시가 같은지 확인한다."""
    sponsor = store.get('sponsors', 'shelf', {})
    history = sponsor.get('history', [])
    approved = next((entry['records'] for entry in reversed(history) if entry['state'] == 'approved'), {})
    if (sponsor.get('state') not in ('approved', 'scheduled') or approved.get('approval_hash') != (row.get('approval') or {}).get('hash') or row.get('sponsor_material') != sponsor_material(store)):
        raise ValueError('협찬 대장 승인 불일치 → 광고주 확인과 사람 승인을 다시 받으세요')


def review_sponsor(root, store, today):
    """가상 시연에서만 수정된 초안의 광고주 확인을 기록한다."""
    row = store.get('posts', 'sponsor', {})
    sponsor = store.get('sponsors', 'shelf', {})
    first = sponsor.get('history', [{}])[0].get('records', {})
    if first.get('advertiser') != '도담' or first.get('contact') != '가상 연락처' or row.get('destination') != 'mock':
        raise ValueError('가상 시연만 지원 → 실제 계약은 대장에 확인 자료를 입력하세요')
    if sponsor.get('state') != 'writing' or not row.get('draft_hash'):
        raise ValueError('수정 초안 준비 후 광고주 확인을 기록하세요')
    transition(store, 'shelf', 'brand_review', {'feedback': '가상 광고주 확인 시연, 외부 회신 없음', 'version': row['draft_hash'], 'count': 1}, today)
    return export_reports(root, store, today)


def sponsor_material(store):
    """승인에 영향을 주는 최신 계약과 검토 자료의 해시를 만든다."""
    sponsor = store.get('sponsors', 'shelf', {})
    material = {}
    for entry in sponsor.get('history', []):
        if entry['state'] in ('reviewing', 'contracted', 'received', 'writing', 'brand_review'):
            material[entry['state']] = entry['records']
    return digest(json_text(material).encode('utf-8'))
