"""관문 검토와 현재 최종본의 사람 승인을 분리해 저장한다."""
from core.hashes import approval_hash
from gates.engine import evaluate, write_report
from wordpress.integrity import recent_documents, require_draft_match


def binding(root, doc, record):
    final = dict(doc, wordpress=record.get('prepared', {}), sponsor_material=record.get('sponsor_material'))
    return approval_hash(root, final)


def inspect_document(root, doc, store=None, config_path=None, **kwargs):
    from copy import deepcopy
    checked = deepcopy(doc)
    registered = []
    if store is not None:
        urls = {link.get('url') for link in doc.get('links', []) + doc.get('paid_links', [])}
        for link in store.all('links'):
            if link.get('url') in urls or link.get('content_id') == doc['content_id']:
                registered.append(dict(link, kind=link.get('kind', 'affiliate'),
                                       details=link.get('details', '판매 수수료')))
        for sponsor in store.all('sponsors'):
            if sponsor.get('content_id') != doc['content_id']:
                continue
            for event in sponsor.get('history', []):
                if event['state'] != 'contracted':
                    continue
                records = event['records']
                if records.get('cash') and records['cash'] not in ('0', '0원', '현금 없음'):
                    registered.append({'kind': 'cash', 'details': '광고비 ' + str(records['cash'])})
                if records.get('goods'):
                    loan = records.get('return_terms') not in (None, '', '반납 없음', '해당 없음')
                    registered.append({'kind': 'loan' if loan else 'gift',
                                       'details': '대여' if loan else '제품 제공'})
    checked['registered_relations'] = registered
    results = evaluate(checked, root=root, config_path=config_path, **kwargs)
    from content.templates import template_errors
    from gates.checks import result
    errors = template_errors(root, store, doc, config_path)
    if errors:
        results = [r for r in results if r['rule_id'] != 'general']
        results.append(result('automation.T1', 'review', 'template', '; '.join(errors),
                              '자유 문장·경험·사진은 최종본을 읽고 사람이 승인하세요.', [], True))
    write_report(root, doc, results)
    return results


def require_ready(results):
    blocked = [item for item in results if item['decision'] in ('block', 'hold') or (
        item['decision'] == 'review' and not item.get('human_resolvable'))]
    if blocked:
        item = blocked[0]
        raise ValueError(item['reason_ko'] + ' → ' + item['next_action_ko'])


def approve_document(root, store, doc, reviewer, today, config_path=None):
    if not reviewer.strip():
        raise ValueError('검토자 이름 없음 → --approve 검토자 이름을 넣으세요')
    results = inspect_document(root, doc, today=today, recent=recent_documents(store, doc), store=store, config_path=config_path)
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
