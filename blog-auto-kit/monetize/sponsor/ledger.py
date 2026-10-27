"""협찬 제안의 상태와 근거 기록을 관리한다."""
from .states import STATES


def _validate(target, records):
    """상태 진입에 필요한 기록이 있는지 확인한다."""
    missing = [key for key in STATES[target][0] if key not in records or records[key] is None or records[key] == '']
    if missing:
        raise ValueError('필수 기록 누락: ' + ', '.join(missing))


def create_inquiry(store, id, record, today):
    """중복 없는 문의를 등록한다."""
    if store.get('sponsors', id) is not None:
        raise ValueError('이미 등록된 문의입니다')
    _validate('inquiry', record)
    row = {'id': id, 'content_id': record.get('content_id'), 'state': 'inquiry', 'history': [{'state': 'inquiry', 'date': today, 'records': dict(record)}]}
    store.put('sponsors', id, row)
    return row


def transition(store, id, target, records, today):
    """허용된 전이와 필수 기록을 확인하고 이력을 보존한다."""
    row = store.get('sponsors', id)
    if not row or target not in STATES:
        raise ValueError('문의 또는 상태가 없습니다')
    current = row['state']
    if current == 'on_hold':
        allowed = [row['history'][-1]['records']['return_state']]
    else:
        allowed = STATES[current][1]
    if target not in allowed:
        raise ValueError('허용되지 않은 전이입니다')
    _validate(target, records)
    if target == 'on_hold' and records['return_state'] != current:
        raise ValueError('복귀 상태는 보류 전 상태여야 합니다')
    if target == 'approved':
        approved = row['history'][-1]['records']['content_hash']
        if records['approval_hash'] != approved:
            raise ValueError('승인 해시가 일치하지 않습니다')
    row = dict(row, state=target, history=row['history'] + [{'state': target, 'date': today, 'records': dict(records)}])
    store.put('sponsors', id, row)
    return row


def assess_offer(doc):
    """위험한 요청을 거절하고 자료가 부족하면 보류한다."""
    contract = doc.get('contract') or {}
    flags = ('requires_false_review', 'requires_disclosure_removal', 'requires_child_identity', 'requires_medical_claim', 'positive_only')
    if any(contract.get(flag) is True for flag in flags):
        return {'decision': 'declined', 'reason': '계약 요구가 안전 또는 정직한 표시 기준에 위반됩니다'}
    if not doc.get('product_records') or contract.get('ai_allowed') not in (True, False):
        return {'decision': 'on_hold', 'reason': '제품 또는 AI 허용 조건 확인 필요'}
    from gates.products import product_checks
    checks = product_checks(doc)
    if any(item['decision'] == 'block' for item in checks):
        return {'decision': 'declined', 'reason': '제품 안전 또는 광고 기준 위반'}
    if any(item['decision'] == 'review' for item in checks):
        return {'decision': 'on_hold', 'reason': '제품 안전·리콜 자료 확인 필요'}
    return {'decision': 'accepted', 'reason': '제품 자료 검토 통과; 사람이 계약 조건을 확인'}
