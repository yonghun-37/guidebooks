"""승인 틀·닫힌 데이터·최종 바이트가 모두 맞을 때만 무승인 예약한다."""
import copy
import json
import shutil
from pathlib import Path
import pytest
from content.markdown import render
from core.state import Store
from core.approval import approve_document, inspect_document
from wordpress.client import Client
from wordpress.mock_server import running_server
from wordpress.prepare import prepare_draft
from wordpress.publish import publish_draft

ROOT = Path(__file__).resolve().parents[1]
TODAY = '2026-10-27'

@pytest.fixture
def kit(tmp_path):
    for directory in ('samples', 'content/templates', 'content/data'):
        shutil.copytree(ROOT / directory, tmp_path / directory)
    shutil.copy(ROOT / 'config.example.toml', tmp_path / 'config.example.toml')
    return tmp_path, Store(tmp_path)


def document(root):
    from content.templates import template_document
    data = json.loads((root / 'content/data/library.json').read_text())
    return template_document(root, 'library', data, TODAY)


def approve(root, store):
    from content.templates import approve_template
    return approve_template(root, store, 'library', '서윤', TODAY)


def schedule(root, store, doc):
    with running_server(root, port=0, today=TODAY) as url:
        client = Client(url)
        try:
            prepare_draft(root, store, client, doc, TODAY, ['info', 'play'])
            row = publish_draft(root, store, client, doc, TODAY, 'auto')
        except ValueError:
            assert all(p['status'] == 'draft' for p in client.request('GET', 'posts'))
            return 'draft'
        return row['status']


def test_approved_template_valid_data_auto_schedules_without_article_approval(kit):
    root, store = kit
    record = approve(root, store)
    assert record['reviewer'] == '서윤' and len(record['template_hash']) == 64
    assert schedule(root, store, document(root)) == 'future'
    assert not store.get('posts', 'library').get('approval')


def test_missing_template_approval_stays_draft(kit):
    root, store = kit
    assert schedule(root, store, document(root)) == 'draft'


@pytest.mark.parametrize('change', ['template', 'schema', 'body', 'html', 'title', 'description',
                                    'extra', 'experience', 'photo', 'llm', 'unknown_value',
                                    'unknown_url', 'long_string', 'extra_data', 'wrong_type'])
def test_modified_template_data_or_output_stays_draft(kit, change):
    root, store = kit
    approve(root, store)
    doc = document(root)
    if change in ('template', 'schema'):
        path = root / ('content/templates/library.' + ('md' if change == 'template' else 'schema.json'))
        path.write_bytes(path.read_bytes() + b' ')
    elif change == 'body':
        doc['markdown'] += '\n'
        doc['html'] = render(doc['markdown'])
    elif change == 'html': doc['html'] += '\n'
    elif change in ('title', 'description'): doc[change] += ' 바꿈'
    elif change == 'experience': doc['experience'] = '내가 쓴 자유 문장'
    elif change == 'photo': doc['photos'] = ['아이 사진']
    elif change == 'llm': doc['authoring_path'] = 'llm'
    elif change == 'extra': doc['free_text'] = '자유 문장'
    else:
        values = {'unknown_value': ('topic', 'fever'), 'unknown_url': ('source_url', 'https://evil.test'),
                  'long_string': ('topic', '가' * 10000), 'extra_data': ('sentence', '해 열 제'),
                  'wrong_type': ('topic', ['자연'])}
        key, value = values[change]
        doc['template_data'][key] = value
    assert schedule(root, store, doc) == 'draft'


@pytest.mark.parametrize('key,value', [('topic', 'fever'), ('topic', '가' * 1000),
    ('source_url', 'https://www.nl.go.kr.evil.test/'), ('source_url', 'https://evil.test/'),
    ('source_url', 'https://www.nl.go.kr/@x\n문장'), ('sentence', '자유 문장'), ('topic', 1)])
def test_schema_rejects_invalid_data_before_rendering(kit, key, value):
    from content.templates import template_document
    root, _ = kit
    data = document(root)['template_data']
    data[key] = value
    with pytest.raises(ValueError): template_document(root, 'library', data, TODAY)


def test_schema_change_requires_new_approval_and_free_sentence_schema_is_rejected(kit):
    root, store = kit
    approve(root, store)
    path = root / 'content/templates/library.schema.json'
    schema = json.loads(path.read_text())
    schema['properties']['topic'] = {'type': 'string', 'maxLength': 80}
    path.write_text(json.dumps(schema))
    with pytest.raises(ValueError): approve(root, store)


def test_current_config_is_rechecked_after_draft_preparation(kit):
    root, store = kit
    approve(root, store)
    doc = document(root)
    with running_server(root, port=0, today=TODAY) as url:
        client = Client(url)
        prepare_draft(root, store, client, doc, TODAY, ['info'])
        path = root / 'config.example.toml'
        path.write_text(path.read_text().replace('auto_allowed_domains = ["www.nl.go.kr"]', 'auto_allowed_domains = []'))
        with pytest.raises(ValueError, match='사람 승인'):
            publish_draft(root, store, client, doc, TODAY, 'auto')
        assert client.request('GET', 'posts')[0]['status'] == 'draft'


def test_changed_template_is_checked_after_preparation(kit):
    root, store = kit
    approve(root, store)
    doc = document(root)
    with running_server(root, port=0, today=TODAY) as url:
        client = Client(url)
        prepare_draft(root, store, client, doc, TODAY, ['info'])
        path = root / 'content/templates/library.md'
        path.write_bytes(path.read_bytes() + b' ')
        with pytest.raises(ValueError, match='사람 승인'):
            publish_draft(root, store, client, doc, TODAY, 'auto')
        assert client.request('GET', 'posts')[0]['status'] == 'draft'


def test_free_prose_can_schedule_only_after_article_approval(kit):
    root, store = kit
    doc = document(root)
    doc['markdown'] += '\n\n내가 고른 주제를 더해요.'
    doc['html'] = render(doc['markdown'])
    with running_server(root, port=0, today=TODAY) as url:
        client = Client(url)
        prepare_draft(root, store, client, doc, TODAY, ['info'])
        with pytest.raises(ValueError, match='사람 승인'):
            publish_draft(root, store, client, doc, TODAY, 'auto')
        approve_document(root, store, doc, '서윤', TODAY)
        assert publish_draft(root, store, client, doc, TODAY, 'auto')['status'] == 'future'


def test_integer_enum_cannot_accept_boolean_as_integer():
    from content.template_schema import validate_data
    schema = {'type': 'object', 'additionalProperties': False, 'required': ['month'],
              'properties': {'month': {'type': 'integer', 'minimum': 1, 'maximum': 12,
                                       'enum': [True]}}}
    with pytest.raises(ValueError): validate_data(schema, {'month': 1}, [])
