"""관문 검토와 현재 최종본의 사람 승인을 분리해 저장한다."""
from core.hashes import approval_hash
from gates.engine import evaluate, write_report
from wordpress.integrity import recent_documents, require_draft_match


def binding(root, doc, record):
    final = dict(doc, wordpress=record.get('prepared', {}), sponsor_material=record.get('sponsor_material'))
    return approval_hash(root, final)


def inspect_document(root, doc, **kwargs):
    results = evaluate(doc, root=root, **kwargs)
    write_report(root, doc, results)
    return results


def require_ready(results):
    blocked = [item for item in results if item['decision'] == 'block' or (
        item['decision'] == 'review' and not item.get('human_resolvable'))]
    if blocked:
        item = blocked[0]
        raise ValueError(item['reason_ko'] + ' → ' + item['next_action_ko'])


def approve_document(root, store, doc, reviewer, today):
    if not reviewer.strip():
        raise ValueError('검토자 이름 없음 → --approve 검토자 이름을 넣으세요')
    results = inspect_document(root, doc, today=today, recent=recent_documents(store, doc))
    require_ready(results)
    row = store.get('posts', doc['content_id'])
    if not row or not row.get('post_id'):
        raise ValueError('서버 초안 없음 → blog.py publish --prepare를 먼저 실행하세요')
    require_draft_match(root, doc, row)
    if doc['content_type'] == 'sponsor':
        sponsor = store.get('sponsors', 'shelf', {})
        if sponsor.get('state') != 'brand_review':
            raise ValueError('광고주 확인 전 → blog.py sponsor demo를 먼저 실행하세요')
    if doc['content_type'] == 'sponsor':
        from core.sponsor_flow import sponsor_material
        row['sponsor_material'] = sponsor_material(store)
    row['approval'] = {'hash': binding(root, doc, row), 'reviewer': reviewer,
                       'date': today, 'reviewed_rules': [r['rule_id'] for r in results
                                                      if r['decision'] == 'review']}
    store.put('posts', doc['content_id'], row)
    return row['approval']
