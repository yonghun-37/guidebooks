"""빈 키트에서 명령을 실행해 예상 출력과 시작 상태를 만든다."""
import argparse
import json
import shutil
import sys
import tempfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from core.files import write_json, write_text
from core.hashes import digest
from core.state import Store
from course.steps import CHAPTERS
from course.execute import execute_chapter
from course.artifacts import manifest
from course.snapshots import save_start


def tree_bytes(path):
    return {p.relative_to(path).as_posix(): digest(p.read_bytes())
            for p in sorted(path.rglob('*')) if p.is_file() and '__pycache__' not in p.parts}


def build(root, destination):
    with tempfile.TemporaryDirectory(prefix='blog-expected-') as directory:
        stage = Path(directory) / 'kit'
        shutil.copytree(root, stage, ignore=shutil.ignore_patterns(
            '.env', '.venv', 'private', 'output', 'config.toml', '__pycache__', '.pytest_cache'))
        for chapter in CHAPTERS:
            save_start(stage, destination / 'states' / (chapter + '.zip'))
            outputs = execute_chapter(stage, chapter, show=False)
            target = destination / 'expected' / chapter
            write_json(target / 'outputs.json', outputs)
            write_text(target / 'terminal.txt', ''.join('$ ' + command + '\n' + result['stdout']
                                                      for command, result in outputs.items()))
            write_json(target / 'hashes.json', manifest(stage))
            compact = json.dumps(Store(stage).snapshot(), ensure_ascii=False, sort_keys=True,
                                 separators=(',', ':')) + '\n'
            write_text(target / 'state.json', compact)
            print('✔ 통과: ' + chapter + ' 예상 출력 생성', flush=True)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--check', action='store_true', help='현재 출력과 저장된 예상 출력 비교')
    args = parser.parse_args()
    root = Path(__file__).resolve().parents[1]
    try:
        with tempfile.TemporaryDirectory(prefix='blog-check-') as directory:
            destination = Path(directory)
            build(root, destination)
            for folder in ('expected', 'states'):
                if args.check:
                    if tree_bytes(root / 'course' / folder) != tree_bytes(destination / folder):
                        raise ValueError(folder + ' 내용이 다름 → build_expected.py로 다시 생성하세요')
                else:
                    shutil.copytree(destination / folder, root / 'course' / folder, dirs_exist_ok=True)
        print('✔ 통과: 예상 출력과 장 시작 상태 일치' if args.check else '✔ 통과: 예상 출력과 장 시작 상태 저장')
        return 0
    except (ValueError, OSError) as error:
        print('✖ 막힘: ' + str(error))
        return 1


if __name__ == '__main__':
    raise SystemExit(main())
