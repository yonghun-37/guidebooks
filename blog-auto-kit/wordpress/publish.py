"""승인된 원고를 예약하고 서버의 공개 상태를 다시 확인한다."""
from core.approval import binding, inspect_document, require_ready
from core.clock import scheduled_date
from core.hashes import content_hash
from core.logs import record_event
from gates.risk import may_auto_publish
from wordpress.quota import reserve_slot
from wordpress.integrity import recent_documents, require_draft_match, verify_remote


def recall_post(store, client, row):
    """승인을 취소하고 서버 공개·예약 상태를 초안으로 회수한다."""
    row['approval'] = None
    row['status'] = 'unknown'
    store.put('posts', row['id'], row)
    try:
        route = f"posts/{row['post_id']}"
        remote = client.request('GET', route + '?context=edit')
        if remote['status'] in ('future', 'publish'):
            client.request('POST', route, {'status': 'draft'})
        remote = client.request('GET', route + '?context=edit')
        if remote['status'] != 'draft':
            raise ValueError('서버가 초안 상태가 아닙니다')
        row['status'] = 'draft'
        store.put('posts', row['id'], row)
    except Exception as exc:
        raise ValueError('예약 회수 상태 확인 실패 → 서버에서 직접 공개 여부를 확인하세요') from exc


def require_approval(root, store, client, doc, row, mode, results, config_path=None):
    """승인 해시와 사람 승인 필요 여부를 확인한다."""
    approval = row.get('approval')
    current = binding(root, doc, row)
    if approval and approval['hash'] != current:
        recall_post(store, client, row)
        raise ValueError('승인 후 내용이 바뀜 → gate --approve로 재승인하세요')
    if (mode not in ('auto', 'after') or not may_auto_publish(doc, results, row, root, store, config_path)) and not approval:
        if row['status'] in ('future', 'publish'):
            recall_post(store, client, row)
        raise ValueError('사람 승인 대기 → blog.py gate --approve 검토자명을 실행하세요')


def publish_draft(root, store, client, doc, today, mode='approval', config_path=None):
    row = store.get('posts', doc['content_id'])
    if not row or not row.get('post_id'):
        raise ValueError('서버 초안 없음 → blog.py publish --prepare를 실행하세요')
    config_path = config_path or row.get('config_path')
    if row['destination'] != client.destination:
        raise ValueError('목적지가 다름 → 승인한 WordPress 주소로 돌아가세요')
    try:
        require_draft_match(root, doc, row)
        remote = verify_remote(client, row)
        row['server_checked'] = True
        if remote['status'] in ('future', 'publish'):
            row.update(is_update=True, server_new_confirmed=False, status=remote['status'])
            row['server_history'] = list(dict.fromkeys([*row.get('server_history', []), remote['status']]))
        store.put('posts', row['id'], row)
        if doc.get('content_type') == 'sponsor':
            from core.sponsor_flow import require_sponsor_approval
            require_sponsor_approval(store, row)
    except Exception:
        recall_post(store, client, row)
        raise
    existing = [p for p in store.all('posts') if p['id'] != doc['content_id']
                and p.get('status') in ('future', 'publish')]
    if any(p['content_hash'] == content_hash(doc) for p in existing):
        raise ValueError('동일 내용의 글이 이미 있음 → 기존 post_id를 확인하세요')
    count = sum(p.get('date') == today for p in existing)
    results = inspect_document(root, doc, today=today, daily_count=count,
                               limit=row.get('daily_limit', 2), recent=recent_documents(store, doc), store=store, config_path=config_path)
    require_ready(results)
    require_approval(root, store, client, doc, row, mode, results, config_path)
    if row['status'] in ('future', 'publish'):
        return check_remote_status(store, client, row)
    if row['doc'] != doc:
        raise ValueError('서버 초안과 다름 → publish --prepare 후 재승인하세요')
    reserve_slot(store, client.destination, row['id'], today, row.get('daily_limit', 2),
                 content_digest=row['content_hash'])
    return schedule_post(root, store, client, row, today)


def schedule_post(root, store, client, row, today):
    version = binding(root, row['doc'], row)
    key = 'schedule:' + client.destination + ':' + str(row['post_id']) + ':' + version
    if not store.claim(key, {'id': key, 'state': 'sending'}):
        return check_remote_status(store, client, row)
    row['status'] = 'unknown'
    store.put('posts', row['id'], row)
    try:
        client.request('POST', f"posts/{row['post_id']}",
                       {'status': 'future', 'date': scheduled_date(today)})
    finally:
        # 시간 초과에도 같은 갱신 요청을 반복하지 않고 서버를 읽는다.
        row = check_remote_status(store, client, row)
    record_event(root, 'reservation_checked', row['id'], today)
    return row


def check_remote_status(store, client, row):
    try:
        remote = verify_remote(client, row)
    except Exception:
        recall_post(store, client, row)
        raise
    if remote['status'] in ('future', 'publish'):
        row['server_history'] = list(dict.fromkeys([*row.get('server_history', []), remote['status']]))
    row.update(status=remote['status'], server_date=remote['date'], url=remote['link'])
    store.put('posts', row['id'], row)
    return row
