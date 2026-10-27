"""발행 승인·예약·불명확한 결과의 안전 회귀 검사."""
import copy
import sys
import threading
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from content.samples import load_sample
from core.approval import binding
from core.hashes import content_hash
from core.state import Store
from wordpress.prepare import prepare_draft
from wordpress.publish import publish_draft

TODAY = '2026-10-27'


class FakeClient:
    destination = 'mock'
    def __init__(self):
        self.calls = []
        self.remote = {}
        self.found = []
    def request(self, method, route, data=None):
        self.calls.append((method, route, copy.deepcopy(data)))
        if method == 'GET': return self.remote[int(route.split('/')[-1].split('?')[0])]
        if route == 'posts':
            post = {'id': 1, 'status': 'draft', 'date': '', 'link': '', **data}
            self.remote[1] = post
            return post
        ident = int(route.split('/')[-1])
        self.remote[ident].update(data)
        return self.remote[ident]
    def find_slug(self, slug): return self.found
    def ensure_term(self, kind, name): return 1
    def upload_media(self, data, filename, mime): return {'id': 1}


@pytest.fixture
def env(tmp_path, monkeypatch):
    import wordpress.prepare as prep
    import wordpress.publish as pub
    monkeypatch.setattr(prep, 'inspect_document', lambda *a, **k: [])
    monkeypatch.setattr(pub, 'inspect_document', lambda *a, **k: [])
    store, client = Store(tmp_path), FakeClient()
    doc = load_sample('info')
    doc.update(media=[], experience='', photos=[], risk_flags=[], commercial_relations=[])
    return tmp_path, store, client, doc


def setup_row(root, store, client, doc, approval=False, status='draft', post_id=1):
    row = {'id': doc['content_id'], 'post_id': post_id, 'destination': 'mock', 'status': status,
           'doc': copy.deepcopy(doc), 'content_hash': content_hash(doc), 'date': TODAY,
           'slug': 'test-' + doc['content_id'], 'prepared': {'media': [], 'categories': [], 'tags': [], 'destination': 'mock'}}
    if approval: row['approval'] = {'hash': binding(root, doc, row), 'reviewer': '사람'}
    store.put('posts', row['id'], row)
    client.remote[post_id] = {'id': post_id, 'status': status, 'date': '', 'link': ''}
    return row


@pytest.mark.parametrize('mode', ['approval', 'auto'])
@pytest.mark.parametrize('risk', ['health', 'affiliate', 'sponsor', 'child_photo', 'experience'])
def test_risk_never_schedules_without_human(env, mode, risk):
    root, store, client, doc = env
    if risk == 'health': doc['title'] = '아이 발열'
    elif risk in ('affiliate', 'sponsor'): doc['content_type'] = risk
    elif risk == 'child_photo': doc['photos'] = ['child']
    else: doc['experience'] = '경험'
    setup_row(root, store, client, doc)
    with pytest.raises(ValueError): publish_draft(root, store, client, doc, TODAY, mode)
    assert not any(call[0] == 'POST' for call in client.calls)


def test_block_cannot_be_bypassed_by_approval(env, monkeypatch):
    import wordpress.publish as pub
    root, store, client, doc = env
    setup_row(root, store, client, doc, approval=True)
    monkeypatch.setattr(pub, 'inspect_document', lambda *a, **k: [{'decision': 'block', 'reason_ko': '차단', 'next_action_ko': '수정'}])
    with pytest.raises(ValueError): publish_draft(root, store, client, doc, TODAY)
    assert not any(method == 'POST' and data.get('status') == 'future'
                   for method, route, data in client.calls)


@pytest.mark.parametrize('change', ['html', 'link', 'contract', 'media'])
def test_approval_changes_cancel_future(env, change):
    root, store, client, doc = env
    if change == 'media':
        (root / 'image.svg').write_text('first')
        doc['media'] = [{'path': 'image.svg'}]
    setup_row(root, store, client, doc, approval=True, status='future')
    modified = copy.deepcopy(doc)
    if change == 'html': modified['html'] += '수정'
    if change == 'link': modified['html'] += '<a href="https://example.test">링크</a>'
    if change == 'contract': modified['contract'] = {'ai_allowed': False}
    if change == 'media': (root / 'image.svg').write_text('second')
    with pytest.raises(ValueError): publish_draft(root, store, client, modified, TODAY)
    assert client.remote[1]['status'] == 'draft'
    assert not store.get('posts', doc['content_id']).get('approval')


def test_brand_review_does_not_approve(env):
    root, store, client, doc = env
    doc['content_type'] = 'sponsor'
    store.put('sponsors', 'shelf', {'state': 'brand_review'})
    setup_row(root, store, client, doc)
    with pytest.raises(ValueError): publish_draft(root, store, client, doc, TODAY, 'auto')
    assert not client.calls


def test_timeout_after_creation_reconciles_without_second_post(env):
    root, store, client, doc = env
    original = client.request
    def request(method, route, data=None):
        if method == 'POST' and route == 'posts':
            original(method, route, data)
            client.found = [{'id': 1, 'status': 'draft'}]
            raise TimeoutError()
        return original(method, route, data)
    client.request = request
    assert prepare_draft(root, store, client, doc, TODAY)['post_id'] == 1
    assert prepare_draft(root, store, client, doc, TODAY)['post_id'] == 1
    assert sum(method == 'POST' and route == 'posts' for method, route, _ in client.calls) == 1


@pytest.mark.parametrize('found', [[], [{'id': 1, 'status': 'draft'}, {'id': 2, 'status': 'draft'}]])
def test_unknown_slug_ambiguous_never_reposts(env, found):
    root, store, client, doc = env
    store.put('posts', doc['content_id'], {'id': doc['content_id'], 'destination': 'mock', 'slug': 'unknown', 'status': 'unknown'})
    client.found = found
    for _ in range(2):
        with pytest.raises(ValueError): prepare_draft(root, store, client, doc, TODAY)
    assert not client.calls


def test_existing_post_updated_without_new_post(env):
    root, store, client, doc = env
    setup_row(root, store, client, doc, post_id=9)
    modified = dict(doc, title='새 제목')
    row = prepare_draft(root, store, client, modified, TODAY)
    assert row['post_id'] == 9
    assert [call[1] for call in client.calls if call[0] == 'POST'] == ['posts/9']


def test_concurrent_schedules_respect_shared_daily_limit(env, monkeypatch):
    import wordpress.publish as pub
    root, store, client, doc = env
    second = copy.deepcopy(doc); second['content_id'] = 'other'; second['html'] += ' different'
    for i, item in enumerate((doc, second), 1):
        row = setup_row(root, store, client, item, approval=True, post_id=i)
        row['daily_limit'] = 1; store.put('posts', item['content_id'], row)
    barrier = threading.Barrier(2)
    original = pub.inspect_document
    def inspect(*args, **kwargs):
        try: barrier.wait(timeout=1)
        except threading.BrokenBarrierError: pass
        return original(*args, **kwargs)
    monkeypatch.setattr(pub, 'inspect_document', inspect)
    def run(item):
        try: return publish_draft(root, store, client, item, TODAY)
        except ValueError: return None
    with ThreadPoolExecutor(max_workers=2) as pool: list(pool.map(run, (doc, second)))
    assert sum(c[0] == 'POST' and c[2].get('status') == 'future' for c in client.calls) <= 1


def test_changed_media_bytes_cannot_keep_old_draft_approval(env):
    root, store, client, doc = env
    (root / 'image.svg').write_text('first')
    doc['media'] = [{'path': 'image.svg'}]
    setup_row(root, store, client, doc, approval=True)
    (root / 'image.svg').write_text('second')
    row = prepare_draft(root, store, client, doc, TODAY)
    assert not row.get('approval')
    assert any(call[0] == 'POST' for call in client.calls)
