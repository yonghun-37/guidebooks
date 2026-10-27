"""초안을 저장하고 불명확한 생성 결과는 조회만으로 복구한다."""
from pathlib import Path
from gates.privacy_exif import image_format, inspect_exif, strip_exif
from urllib.error import URLError
from core.approval import inspect_document, require_ready
from core.hashes import content_hash, approval_hash, digest
from core.logs import record_event
from wordpress.integrity import recent_documents


def reconcile(store, client, row, key):
    rows = client.find_slug(row['slug'])
    if len(rows) != 1:
        raise ValueError('발행 결과 불명 → status로 조회하세요. 재POST는 금지됩니다')
    row.update(post_id=rows[0]['id'], status=rows[0]['status'])
    from wordpress.integrity import verify_remote
    verify_remote(client, row)
    store.put('posts', row['id'], row)
    store.put('runs', key, {'id': key, 'state': 'reconciled', 'post_id': row['post_id']})
    return row


def remote_assets(root, client, doc):
    categories = [client.ensure_term('categories', '육아·교육')]
    tags = [client.ensure_term('tags', doc['content_type'])]
    media = []
    hashes = {}
    for item in doc.get('media', []):
        path = root / item['path']
        data = strip_exif(path.read_bytes())
        if inspect_exif(data):
            raise ValueError('공개용 사본에 메타데이터가 남아 있습니다')
        kind = image_format(data)
        extension, mime = ('.jpg', 'image/jpeg') if kind == 'JPEG' else ('.png', 'image/png')
        public = Path(root) / 'private/public-media' / (digest(data) + extension)
        public.parent.mkdir(parents=True, exist_ok=True)
        public.write_bytes(data)
        if inspect_exif(public.read_bytes()):
            raise ValueError('공개용 사본 재검사 실패')
        response = client.upload_media(public.read_bytes(), public.name, mime)
        media.append(response['id'])
        hashes[str(response['id'])] = digest(data)
    return {'categories': categories, 'tags': tags, 'media': media, 'media_hashes': hashes,
            'destination': client.destination}


def post_payload(doc, row):
    assets = row['prepared']
    return {'slug': row['slug'], 'title': doc['title'], 'content': doc['html'],
            'excerpt': doc['description'], 'status': 'draft', 'categories': assets['categories'],
            'tags': assets['tags'], 'featured_media': next(iter(assets['media']), 0)}


def prepare_draft(root, store, client, doc, today, auto_allowed_types=()):
    require_ready(inspect_document(root, doc, today=today, recent=recent_documents(store, doc), store=store))
    ident = doc['content_id']
    row = store.get('posts', ident)
    if row and row['destination'] != client.destination:
        raise ValueError('목적지 변경 → 별도 키트 폴더에서 새 연결을 시작하세요')
    key = 'create:' + client.destination + ':' + ident
    if row and not row.get('post_id'):
        return reconcile(store, client, row, key)
    if row and row.get('post_id'):
        return update_draft(root, store, client, doc, row, today)
    row = discover_record(client, doc, today, auto_allowed_types)
    if row['is_update']:
        store.put('posts', ident, row)
        return update_draft(root, store, client, doc, row, today)
    if not store.claim(key, {'id': key, 'state': 'sending'}):
        raise ValueError('중복 실행 잠금 → status로 이전 실행을 확인하세요')
    store.put('posts', ident, row)
    try:
        row['prepared'] = remote_assets(root, client, doc)
        row['draft_hash'] = approval_hash(root, doc)
        row['snapshot'] = post_payload(doc, row)
        response = client.request('POST', 'posts', row['snapshot'])
        row.update(post_id=response['id'], status=response['status'])
        store.put('runs', key, {'id': key, 'state': 'done', 'post_id': response['id']})
    except (TimeoutError, URLError, OSError):
        row['status'] = 'unknown'
        store.put('posts', ident, row)
        return reconcile(store, client, row, key)
    finally:
        store.put('posts', ident, row)
    record_event(root, 'draft_saved', ident, today)
    return row


def discover_record(client, doc, today, auto_allowed_types):
    """서버의 post_id 또는 안정적인 slug로 기존 글을 먼저 찾는다."""
    slug = doc.get('slug') or 'bx-' + doc['content_id']
    found = client.find_slug(slug)
    if doc.get('post_id'):
        remote = client.request('GET', f"posts/{int(doc['post_id'])}?context=edit")
        found = [remote]
        slug = remote['slug']
    if len(found) > 1:
        raise ValueError('같은 slug의 서버 글이 여러 개입니다 → 서버에서 확인하세요')
    row = {'id': doc['content_id'], 'content_hash': content_hash(doc), 'slug': slug,
           'destination': client.destination, 'status': 'sending', 'doc': doc, 'date': today,
           'is_update': bool(found), 'server_new_confirmed': not found,
           'server_checked': True, 'auto_allowed_types': list(auto_allowed_types)}
    if found:
        row.update(post_id=found[0]['id'], status=found[0]['status'])
    return row


def update_draft(root, store, client, doc, row, today):
    remote = client.request('GET', f"posts/{row['post_id']}?context=edit")
    row['is_update'] = True
    row['server_new_confirmed'] = False
    row['server_checked'] = True
    row['server_history'] = list(dict.fromkeys([*row.get('server_history', []), remote['status']]))
    store.put('posts', doc['content_id'], row)
    if row['doc'] == doc and row.get('draft_hash') == approval_hash(root, doc):
        from wordpress.integrity import verify_remote
        try:
            verify_remote(client, row)
            return row
        except ValueError:
            pass
    if remote['status'] in ('future', 'publish'):
        client.request('POST', f"posts/{row['post_id']}", {'status': 'draft'})
    if doc.get('content_type') == 'sponsor':
        from core.sponsor_flow import invalidate_sponsor
        invalidate_sponsor(store, doc, today)
    row['approval'] = None
    row['status'] = 'unknown'
    store.put('posts', doc['content_id'], row)
    row['prepared'] = remote_assets(root, client, doc)
    row['revision'] = row.get('revision', 0) + 1
    row['prepared']['revision'] = row['revision']
    row['draft_hash'] = approval_hash(root, doc)
    row['doc'], row['content_hash'] = doc, content_hash(doc)
    row['snapshot'] = post_payload(doc, row)
    response = client.request('POST', f"posts/{row['post_id']}", row['snapshot'])
    row['status'] = response['status']
    store.put('posts', doc['content_id'], row)
    record_event(root, 'approval_invalidated', doc['content_id'], today)
    return row
