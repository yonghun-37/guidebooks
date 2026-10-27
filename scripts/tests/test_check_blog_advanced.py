"""본문의 명령·성공 출력·줄 번호가 변조되면 통합 게이트가 막는지 검사한다."""
import importlib.util
from pathlib import Path
import shutil
import sys

import pytest

SCRIPTS = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(SCRIPTS))
spec = importlib.util.spec_from_file_location('advanced_checker', SCRIPTS / 'check_blog_advanced.py')
checker = importlib.util.module_from_spec(spec)
spec.loader.exec_module(checker)


@pytest.fixture
def root(tmp_path):
    for directory in ('site-blog/advanced', 'blog-auto-kit'):
        shutil.copytree(SCRIPTS.parent / directory, tmp_path / directory,
                        ignore=shutil.ignore_patterns('.env', '.venv', 'private', 'output', '__pycache__', '.pytest_cache'))
    return tmp_path


def test_actual_manuscript_matches(root):
    assert checker.check(root)['errors'] == []


@pytest.mark.parametrize('old,new,fragment', [
    ('python blog.py pages', 'python blog.py pagez', '명령'),
    ('✔ 통과: pages 생성', '✔ 통과: 다른 출력', '성공 출력'),
    ('data-source="monetize/pages.py:', 'data-source="monetize/missing.py:', '발췌'),
    ('data-course="A2"', 'data-course="A99"', '명령'),
    ('data-expected="A2|', 'data-expected="A99|', '성공 출력'),
])
def test_manuscript_mutations_fail(root, old, new, fragment):
    page = root / 'site-blog/advanced/02-wordpress.html'
    text = page.read_text()
    assert old in text
    page.write_text(text.replace(old, new, 1))
    assert any(fragment in error for error in checker.check(root)['errors'])


def test_new_unregistered_change_command_is_not_ignored(root):
    page = root / 'site-blog/advanced/02-wordpress.html'
    page.write_text(page.read_text().replace('id="change">', 'id="change"><code data-run="common">python blog.py typo</code>', 1))
    assert any('명령 밖' in e for e in checker.check(root)['errors'])


def test_command_from_another_chapter_cannot_hide_in_main_route(root):
    page = root / 'site-blog/advanced/02-wordpress.html'
    page.write_text(page.read_text().replace('id="pages">', 'id="pages"><code data-run="common">python blog.py topics</code>', 1))
    assert any('명령 표시' in e for e in checker.check(root)['errors'])


def test_checkpoint_command_order_is_checked(root):
    page = root / 'site-blog/advanced/01-environment.html'
    text = page.read_text()
    before, checkpoint = text.split('id="checkpoint">', 1)
    checkpoint = checkpoint.replace('python course.py doctor\npython blog.py status --mock',
                                    'python blog.py status --mock\npython course.py doctor')
    page.write_text(before + 'id="checkpoint">' + checkpoint)
    assert any('체크포인트 복원' in e for e in checker.check(root)['errors'])


def test_expected_cannot_silently_drop_bypass_bundle(root):
    import json
    path = root / 'blog-auto-kit/course/expected/E2E/outputs.json'
    outputs = json.loads(path.read_text())
    outputs['python blog.py run --scenarios']['stdout'] = '✔ 통과: mock_normal\n'
    path.write_text(json.dumps(outputs, ensure_ascii=False))
    assert any('우회 시도' in error for error in checker.check(root)['errors'])


def test_empty_inline_error_example_is_not_accepted(root):
    page = root / 'site-blog/advanced/07-ads.html'
    page.write_text(page.read_text().replace('id="change">', 'id="change"><code></code>', 1))
    assert any('빈 코드' in error for error in checker.check(root)['errors'])
