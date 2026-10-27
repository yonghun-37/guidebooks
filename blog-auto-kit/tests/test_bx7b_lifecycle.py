"""실제 CLI 승인과 예약 뒤 틀 변경도 확인한다."""
import json
import shutil
from pathlib import Path
import pytest
from core.state import Store
from wordpress.client import Client
from wordpress.mock_server import running_server
from wordpress.prepare import prepare_draft
from wordpress.publish import publish_draft
from content.templates import approve_template, template_document

ROOT = Path(__file__).resolve().parents[1]
TODAY = '2026-10-27'

@pytest.fixture
def kit(tmp_path):
    for name in ('samples', 'content/templates', 'content/data'):
        shutil.copytree(ROOT / name, tmp_path / name)
    shutil.copy(ROOT / 'config.example.toml', tmp_path / 'config.example.toml')
    return tmp_path, Store(tmp_path)


def test_cli_never_approves_template_implicitly(kit, monkeypatch, capsys):
    import blog
    from core.cli import make_parser
    root, store = kit
    monkeypatch.setattr(blog, 'ROOT', root)
    settings = (root / 'config.example.toml').read_text().replace('mode = "approval"', 'mode = "auto"')
    (root / 'config.toml').write_text(settings)
    parser = make_parser()
    assert blog.execute(parser.parse_args(['run', '--sample', 'library'])) == 1
    assert not store.get('runs', 'template-approval:library')
    assert blog.execute(parser.parse_args(['template', 'approve', 'library', '--by', '서윤'])) == 0
    assert store.get('runs', 'template-approval:library')['reviewer'] == '서윤'
    # 첫 실행이 남긴 초안을 새 글로 속이지 않는다. 별도 복사본의 신규 시연을 쓴다.
    with running_server(root, port=0, today=TODAY) as url:
        assert Client(url).request('GET', 'posts')[0]['status'] == 'draft'
    assert '틀 해시:' in capsys.readouterr().out


def test_cli_approved_template_demo_schedules_and_makes_no_article_approval(kit, monkeypatch):
    import blog
    from core.cli import make_parser
    root, store = kit
    monkeypatch.setattr(blog, 'ROOT', root)
    settings = (root / 'config.example.toml').read_text().replace('mode = "approval"', 'mode = "auto"')
    (root / 'config.toml').write_text(settings)
    parser = make_parser()
    assert blog.execute(parser.parse_args(['template', 'approve', 'library', '--by', '서윤'])) == 0
    assert blog.execute(parser.parse_args(['run', '--sample', 'library'])) == 0
    row = store.get('posts', 'library')
    assert row['status'] == 'future' and not row.get('approval')
    assert not store.all('costs')


def test_changed_template_recalls_already_auto_scheduled_post(kit):
    root, store = kit
    approve_template(root, store, 'library', '서윤', TODAY)
    data = json.loads((root / 'content/data/library.json').read_text())
    doc = template_document(root, 'library', data, TODAY)
    with running_server(root, port=0, today=TODAY) as url:
        client = Client(url)
        prepare_draft(root, store, client, doc, TODAY, ['info'])
        assert publish_draft(root, store, client, doc, TODAY, 'auto')['status'] == 'future'
        path = root / 'content/templates/library.md'
        path.write_bytes(path.read_bytes() + b' ')
        with pytest.raises(ValueError):
            publish_draft(root, store, client, doc, TODAY, 'auto')
        assert client.request('GET', 'posts')[0]['status'] == 'draft'


def test_default_free_prose_demo_cannot_create_a_human_approval(kit, monkeypatch):
    import blog
    from core.cli import make_parser
    root, store = kit
    monkeypatch.setattr(blog, 'ROOT', root)
    parser = make_parser()
    assert blog.execute(parser.parse_args(['run', '--sample'])) == 1
    assert not store.get('posts', 'info').get('approval')
    assert store.get('posts', 'info')['status'] == 'draft'
    assert blog.execute(parser.parse_args(['gate', '--sample', 'info', '--approve', '서윤'])) == 0
    assert blog.execute(parser.parse_args(['run', '--sample'])) == 0
    assert store.get('posts', 'info')['status'] == 'future'
    assert store.get('posts', 'info')['approval']['reviewer'] == '서윤'


def test_cli_selected_config_controls_template_url_allowlist(kit, monkeypatch):
    import blog
    from core.cli import make_parser
    root, store = kit
    monkeypatch.setattr(blog, 'ROOT', root)
    settings = (root / 'config.example.toml').read_text().replace('mode = "approval"', 'mode = "auto"')
    settings = settings.replace('auto_allowed_domains = ["www.nl.go.kr"]', 'auto_allowed_domains = []')
    (root / 'strict.toml').write_text(settings)
    parser = make_parser()
    assert blog.execute(parser.parse_args(['template', 'approve', 'library', '--by', '서윤'])) == 0
    assert blog.execute(parser.parse_args(['run', '--sample', 'library', '--config', 'strict.toml'])) == 1
    assert not store.get('posts', 'library') or store.get('posts', 'library')['status'] == 'draft'


def test_selected_config_file_is_reloaded_at_publish_time(kit):
    root, store = kit
    approve_template(root, store, 'library', '서윤', TODAY)
    path = root / 'selected.toml'
    path.write_text((root / 'config.example.toml').read_text())
    data = json.loads((root / 'content/data/library.json').read_text())
    doc = template_document(root, 'library', data, TODAY, config_path='selected.toml')
    with running_server(root, port=0, today=TODAY) as url:
        client = Client(url)
        prepare_draft(root, store, client, doc, TODAY, ['info'], config_path='selected.toml')
        path.write_text(path.read_text().replace('auto_allowed_domains = ["www.nl.go.kr"]',
                                                'auto_allowed_domains = []'))
        # 호출자가 경로를 생략해도 준비 때 고른 설정 파일을 다시 읽는다.
        with pytest.raises(ValueError, match='사람 승인'):
            publish_draft(root, store, client, doc, TODAY, 'auto')
        assert client.request('GET', 'posts')[0]['status'] == 'draft'
