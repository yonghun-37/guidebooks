"""BX6의 무승인 예약 반례를 실제 로컬 HTTP 경로로 재현한다."""
import copy
import shutil
import sys
from pathlib import Path
import pytest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from content.samples import load_sample
from content.markdown import render
from core.state import Store
from core.approval import approve_document
from gates.engine import evaluate
from wordpress.client import Client
from wordpress.mock_server import running_server
from wordpress.prepare import prepare_draft
from wordpress.publish import publish_draft

TODAY = '2026-10-27'

@pytest.fixture
def kit(tmp_path):
    shutil.copytree(ROOT / 'samples', tmp_path / 'samples')
    return tmp_path, Store(tmp_path)


def general_doc():
    doc = load_sample('info')
    doc.update(title='그림책 정리', description='책을 함께 읽는 순서', media=[])
    doc['markdown'] = '그림책을 정리해요.\n\n## 함께 읽기\n\n그림을 보며 이야기를 나눠요.'
    doc['html'] = render(doc['markdown'])
    return doc

@pytest.mark.parametrize('mode', ['auto', 'after', 'approval'])
@pytest.mark.parametrize('field,text', [
    ('markdown', '해열제에 관한 설명입니다.'),
    ('markdown', '아스피린에 관한 설명입니다.'),
    ('markdown', '아기 발열에 관한 설명입니다.'),
    ('markdown', '가상 아이의 이름은 테스트봄이이고 병원은 가상병원입니다.'),
    ('description', '가상 아이 이름은 테스트봄이입니다.'),
    ('experience', '가상병원에 다녀왔어요.'),
])
def test_bx6_body_and_identification_never_auto(kit, mode, field, text):
    root, store = kit
    doc = general_doc()
    doc[field] += '\n\n' + text
    doc['html'] = render(doc['markdown'])
    with running_server(root, port=0, today=TODAY) as url:
        client = Client(url)
        try:
            prepare_draft(root, store, client, doc, TODAY, ['info'])
            publish_draft(root, store, client, doc, TODAY, mode)
        except ValueError:
            pass
        assert all(p['status'] == 'draft' for p in client.request('GET', 'posts'))
    assert any(r['decision'] != 'pass' for r in evaluate(doc, root=root))


def test_public_update_stays_update_across_prepare_retry_and_query(kit):
    root, store = kit
    doc = general_doc()
    with running_server(root, port=0, today=TODAY) as url:
        client = Client(url)
        prepare_draft(root, store, client, doc, TODAY)
        approve_document(root, store, doc, '가상 검토자', TODAY)
        publish_draft(root, store, client, doc, TODAY)
    with running_server(root, port=0, today='2026-10-30') as url:
        client = Client(url)
        assert client.request('GET', 'posts')[0]['status'] == 'publish'
        doc['markdown'] += '\n\n읽기 순서를 바꿔요.'
        doc['html'] = render(doc['markdown'])
        for _ in range(2):
            row = prepare_draft(root, store, client, doc, '2026-10-30')
            assert row.get('is_update') is True
            with pytest.raises(ValueError, match='사람 승인'):
                publish_draft(root, store, client, doc, '2026-10-30', 'auto')
            assert client.request('GET', 'posts')[0]['status'] == 'draft'
        approve_document(root, store, doc, '새 최종본 검토자', '2026-10-30')
        assert publish_draft(root, store, client, doc, '2026-10-30', 'auto')['status'] == 'future'


def test_allowlist_requires_every_pass_and_verified_new_server_record():
    from gates.risk import may_auto_publish
    doc = general_doc()
    row = {'server_new_confirmed': True, 'is_update': False, 'auto_allowed_types': ['info'],
           'server_checked': True}
    passed = [{'decision': 'pass'}]
    # 자유 문장은 예전의 모든 허용 조건이 맞아도 자동 대상이 아니다.
    assert not may_auto_publish(doc, passed, row)
    for change in ({'is_update': True}, {'server_new_confirmed': False},
                   {'server_checked': False}, {'auto_allowed_types': []}):
        assert not may_auto_publish(doc, passed, dict(row, **change))
    for decision in ('review', 'hold', 'block', 'unknown'):
        assert not may_auto_publish(doc, [{'decision': decision}], row)
    assert not may_auto_publish(doc, [], row)
    for key, value in [('title', '건강 안내'), ('description', '제품 제공'),
                       ('experience', '내 경험'), ('photos', ['photo']),
                       ('media', [{'path': '아이사진.jpg', 'alt': '아이 사진'}]),
                       ('content_type', 'unclassified')]:
        assert not may_auto_publish(dict(doc, **{key: value}), passed, row)


def test_verified_new_free_prose_still_waits_for_human(kit):
    root, store = kit
    doc = general_doc()
    with running_server(root, port=0, today=TODAY) as url:
        client = Client(url)
        row = prepare_draft(root, store, client, doc, TODAY, ['info'])
        assert row['server_new_confirmed'] is True
        with pytest.raises(ValueError, match='사람 승인'):
            publish_draft(root, store, client, doc, TODAY, 'auto')
        assert client.request('GET', 'posts')[0]['status'] == 'draft'
        assert store.get('posts', doc['content_id']).get('approval') is None


def test_cost_status_reads_reserved_and_settled_without_connecting(kit, capsys):
    from core.publish_actions import wordpress_action
    from types import SimpleNamespace
    from providers.costs import reserve_cost, settle_cost
    root, store = kit
    reserve_cost(store, 'draft:info:' + TODAY, '0', TODAY, '1')
    settle_cost(store, 'draft:info:' + TODAY, '0', TODAY)
    reserve_cost(store, 'pending', '0.01', TODAY, '1')
    before = store.snapshot()
    wordpress_action(root, store, {'wordpress': {'mode': 'live'}},
                     SimpleNamespace(command='status', costs=True, today=TODAY))
    text = capsys.readouterr().out
    assert 'draft:info:2026-10-27 | 2026-10-27 | settled | 0.000000 USD' in text
    assert 'pending | 2026-10-27 | reserved | 0.010000 USD' in text
    assert store.snapshot() == before


def test_weekly_report_includes_separate_fixed_overdue_example(kit):
    from analytics.report import build_report
    root, store = kit
    report = Path(build_report(root, store, TODAY)[0]).read_text()
    assert '가상 갱신 예제' in report and '2026-10-01' in report
    assert 'review_due' in report and '원문' in report
    assert not store.all('posts')


@pytest.mark.parametrize('lookup', ['slug', 'post_id'])
def test_server_existing_post_is_update_without_local_post_record(kit, lookup):
    root, store = kit
    doc = general_doc()
    with running_server(root, port=0, today=TODAY) as url:
        client = Client(url)
        first = prepare_draft(root, store, client, doc, TODAY, ['info'])
        with store.connect() as db:
            db.execute('DELETE FROM posts')
        if lookup == 'post_id':
            doc['post_id'] = first['post_id']
        recovered = prepare_draft(root, store, client, doc, TODAY, ['info'])
        assert recovered['post_id'] == first['post_id'] and recovered['is_update'] is True
        with pytest.raises(ValueError, match='사람 승인'):
            publish_draft(root, store, client, doc, TODAY, 'auto')
        assert len(client.request('GET', 'posts')) == 1


def test_body_fever_requires_common_text_and_all_ten_templates_stay_equal():
    import json
    from gates.checks import EMERGENCY
    doc = general_doc(); doc['markdown'] += '\n\n아기 발열에 관한 설명입니다.'
    doc['html'] = render(doc['markdown'])
    assert any(r['rule_id'] == 'health_safety.H4' and r['decision'] == 'block'
               for r in evaluate(doc))
    import hashlib
    # 2026-10-28 BabyBook 원문/조사와 직접 대조한 10문구의 고정 지문.
    assert len(EMERGENCY) == 10
    fingerprint = hashlib.sha256(json.dumps([r['text'] for r in EMERGENCY], ensure_ascii=False).encode()).hexdigest()
    assert fingerprint == 'afb2516f69f6dfc70e5a941c1c311a7026abe0ab1aab82646051860de1dfb928'


def test_publish_reads_server_status_before_auto_reschedule(kit):
    root, store = kit
    doc = general_doc()
    with running_server(root, port=0, today=TODAY) as url:
        client = Client(url)
        row = prepare_draft(root, store, client, doc, TODAY, ['info'])
        # 로컬 기록이 draft여도 서버에서 이미 공개한 글은 신규가 아니다.
        client.request('POST', f"posts/{row['post_id']}", {'status': 'publish'})
        with pytest.raises(ValueError, match='사람 승인'):
            publish_draft(root, store, client, doc, TODAY, 'auto')
        saved = store.get('posts', doc['content_id'])
        assert saved['is_update'] is True and saved['server_new_confirmed'] is False
        assert client.request('GET', f"posts/{row['post_id']}")['status'] == 'draft'
