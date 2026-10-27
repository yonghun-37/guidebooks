"""예약된 원고의 무결성 오류를 회수하고 복구한다."""
import shutil
import sys
from pathlib import Path
import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from content.samples import load_sample, with_human_notes
from core.approval import approve_document
from core.sponsor_flow import record_sponsor_approval, record_sponsor_remote
from core.state import Store
from monetize.sponsor.demo import run_sponsor_demo
from wordpress.client import Client
from wordpress.mock_server import running_server
from wordpress.prepare import prepare_draft
from wordpress.publish import publish_draft

TODAY = '2026-10-27'

@pytest.fixture
def env(tmp_path):
    root = Path(__file__).resolve().parents[1]
    shutil.copytree(root / 'samples', tmp_path / 'samples')
    return tmp_path, Store(tmp_path)


def test_remote_corruption_of_future_cancels_and_prepare_restores(env):
    root, store = env; doc = load_sample('info')
    with running_server(root, port=0) as url:
        client = Client(url); row = prepare_draft(root, store, client, doc, TODAY)
        approve_document(root, store, doc, '사람', TODAY)
        publish_draft(root, store, client, doc, TODAY)
        client.request('POST', f"posts/{row['post_id']}", {'content': '변조'})
        with pytest.raises(ValueError): publish_draft(root, store, client, doc, TODAY)
        assert client.request('GET', f"posts/{row['post_id']}")['status'] == 'draft'
        assert not store.get('posts', 'info').get('approval')
        prepare_draft(root, store, client, doc, TODAY)
        assert client.request('GET', f"posts/{row['post_id']}")['content'] == doc['html']


def test_sponsor_contract_change_recalls_future(env):
    root, store = env; doc = with_human_notes(load_sample('sponsor'))
    run_sponsor_demo(root, store, TODAY)
    with running_server(root, port=0) as url:
        client = Client(url); row = prepare_draft(root, store, client, doc, TODAY)
        approval = approve_document(root, store, doc, '사람', TODAY)
        record_sponsor_approval(root, store, approval, TODAY)
        scheduled = publish_draft(root, store, client, doc, TODAY)
        record_sponsor_remote(root, store, scheduled, TODAY)
        sponsor = store.get('sponsors', 'shelf')
        next(x for x in sponsor['history'] if x['state'] == 'contracted')['records']['cash'] = '100원'
        store.put('sponsors', 'shelf', sponsor)
        with pytest.raises(ValueError): publish_draft(root, store, client, doc, TODAY)
        assert client.request('GET', f"posts/{row['post_id']}")['status'] == 'draft'
        assert not store.get('posts', 'sponsor').get('approval')


def test_cannot_confirm_recall_records_unknown(env):
    root, store = env; doc = load_sample('info')
    with running_server(root, port=0) as url:
        client = Client(url); row = prepare_draft(root, store, client, doc, TODAY)
        approve_document(root, store, doc, '사람', TODAY)
        publish_draft(root, store, client, doc, TODAY)
        client.request('POST', f"posts/{row['post_id']}", {'content': '변조'})
        original = client.request
        def failing(method, route, data=None, headers=None):
            if method == 'POST' and data == {'status': 'draft'}: raise OSError('오프라인')
            return original(method, route, data, headers)
        client.request = failing
        with pytest.raises(ValueError, match='회수.*확인'): publish_draft(root, store, client, doc, TODAY)
        assert store.get('posts', 'info')['status'] == 'unknown'
        assert not store.get('posts', 'info').get('approval')
