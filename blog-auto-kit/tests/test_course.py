"""장별 복원과 출력·산출물 변조를 실제 명령으로 검사한다."""
import shutil
from pathlib import Path
import pytest
from course.steps import CHAPTERS
from course.execute import execute_chapter
from course.artifacts import check_chapter
from course.snapshots import restore_start
from core.files import read_json, write_json

KIT = Path(__file__).resolve().parents[1]


@pytest.fixture
def kit(tmp_path):
    stage = tmp_path / 'kit'
    shutil.copytree(KIT, stage, ignore=shutil.ignore_patterns(
        '.env', '.venv', 'private', 'output', 'config.toml', '__pycache__', '.pytest_cache'))
    return stage


@pytest.mark.parametrize('chapter', CHAPTERS)
def test_each_chapter_can_start_independently(kit, chapter):
    restore_start(kit, chapter)
    execute_chapter(kit, chapter, show=False)
    check_chapter(kit, chapter)


def test_checkpoint_detects_artifact_change(kit):
    restore_start(kit, 'A2')
    execute_chapter(kit, 'A2', show=False)
    (kit / 'output/pages/about.html').write_text('다른 소개')
    with pytest.raises(ValueError, match='내용 변경'):
        check_chapter(kit, 'A2')


def test_checkpoint_detects_terminal_change(kit):
    restore_start(kit, 'A1')
    execute_chapter(kit, 'A1', show=False)
    path = kit / 'private/terminal.json'
    data = read_json(path)
    data['python course.py doctor']['stdout'] = '변조'
    write_json(path, data)
    with pytest.raises(ValueError, match='명령 출력이 다름'):
        check_chapter(kit, 'A1')
