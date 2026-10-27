"""승인과 서버 원고가 동일한지 실제 mock HTTP로 확인한다."""
import copy
import shutil
import sys
from pathlib import Path
import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from content.samples import load_sample, with_human_notes
from content.markdown import render
from core.approval import approve_document
from core.sponsor_flow import record_sponsor_approval
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
    shutil.copy(root / 'config.example.toml', tmp_path / 'config.example.toml')
    return tmp_path, Store(tmp_path)


def test_media_changed_after_prepare_cannot_be_approved(env):
    root, store = env; doc = load_sample('info')
    with running_server(root, port=0) as url:
        client = Client(url); prepare_draft(root, store, client, doc, TODAY)
        (root / doc['media'][0]['path']).write_bytes(b'changed')
        with pytest.raises(ValueError): approve_document(root, store, doc, '사람', TODAY)


def test_remote_modified_html_never_scheduled(env):
    root, store = env; doc = load_sample('info')
    with running_server(root, port=0) as url:
        client = Client(url); row = prepare_draft(root, store, client, doc, TODAY)
        approve_document(root, store, doc, '사람', TODAY)
        client.request('POST', f"posts/{row['post_id']}", {'content': '<p>UNAPPROVED CONTENT</p>'})
        with pytest.raises(ValueError): publish_draft(root, store, client, doc, TODAY)
        assert client.request('GET', f"posts/{row['post_id']}")['status'] == 'draft'


def test_sponsor_changed_requires_new_brand_review(env):
    root, store = env; doc = with_human_notes(load_sample('sponsor'))
    run_sponsor_demo(root, store, TODAY)
    with running_server(root, port=0) as url:
        client = Client(url); prepare_draft(root, store, client, doc, TODAY)
        approval = approve_document(root, store, doc, '사람', TODAY)
        record_sponsor_approval(root, store, approval, TODAY)
        revised = copy.deepcopy(doc); revised['markdown'] += '\n\n새 내용'; revised['html'] = render(revised['markdown'])
        prepare_draft(root, store, client, revised, TODAY)
        assert store.get('sponsors', 'shelf')['state'] == 'writing'
        with pytest.raises(ValueError): approve_document(root, store, revised, '사람', TODAY)


def test_near_duplicate_preparation_is_held(env):
    root, store = env; doc = load_sample('info')
    with running_server(root, port=0) as url:
        client = Client(url); prepare_draft(root, store, client, doc, TODAY)
        approve_document(root, store, doc, '사람', TODAY)
        publish_draft(root, store, client, doc, TODAY)
        revised = copy.deepcopy(doc); revised['content_id'] = 'info2'; revised['markdown'] += '\n새 문장'; revised['html'] += '<p>새 문장</p>'
        with pytest.raises(ValueError): prepare_draft(root, store, client, revised, TODAY)


def test_sponsor_contract_change_invalidates_approval(env):
    root, store = env; doc = with_human_notes(load_sample('sponsor'))
    run_sponsor_demo(root, store, TODAY)
    with running_server(root, port=0) as url:
        client = Client(url); prepare_draft(root, store, client, doc, TODAY)
        approval = approve_document(root, store, doc, '사람', TODAY)
        record_sponsor_approval(root, store, approval, TODAY)
        sponsor = store.get('sponsors', 'shelf')
        next(x for x in sponsor['history'] if x['state'] == 'contracted')['records']['cash'] = '100원'
        store.put('sponsors', 'shelf', sponsor)
        with pytest.raises(ValueError): publish_draft(root, store, client, doc, TODAY)


def test_sponsor_ai_draft_respects_ledger_contract(env):
    from core.workflow import make_draft
    root, store = env
    run_sponsor_demo(root, store, TODAY)
    with pytest.raises(ValueError): make_draft(root, store, 'sponsor', TODAY)
    doc = make_draft(root, store, 'sponsor', TODAY, human_notes=True)
    assert doc['contract']['ai_allowed'] is False


def test_sponsor_review_enables_new_human_approval(env):
    from core.sponsor_flow import review_sponsor
    from content.markdown import render
    root, store = env; doc = with_human_notes(load_sample('sponsor'))
    run_sponsor_demo(root, store, TODAY)
    with running_server(root, port=0) as url:
        client = Client(url); prepare_draft(root, store, client, doc, TODAY)
        approval = approve_document(root, store, doc, '사람', TODAY)
        record_sponsor_approval(root, store, approval, TODAY)
        revised = copy.deepcopy(doc); revised['markdown'] += '\n\n수정한 가상 후기'; revised['html'] = render(revised['markdown'])
        prepare_draft(root, store, client, revised, TODAY)
        review_sponsor(root, store, TODAY)
        approval = approve_document(root, store, revised, '사람', TODAY)
        with pytest.raises(ValueError): publish_draft(root, store, client, revised, TODAY)
        approval = approve_document(root, store, revised, '사람', TODAY)
        record_sponsor_approval(root, store, approval, TODAY)
        assert publish_draft(root, store, client, revised, TODAY)['status'] == 'future'
