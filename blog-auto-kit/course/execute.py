"""명령 표의 명령을 순서대로 실행하고 각 장을 검사한다."""
import argparse
import os
import shlex
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from course.steps import CHAPTERS, commands
from course.snapshots import reset


def run_command(root, command):
    words = shlex.split(command)
    if words[0] != 'python' or words[1] not in ('blog.py', 'course.py'):
        raise ValueError('허용되지 않은 실습 명령 → commands.md를 확인하세요')
    env = dict(os.environ, PYTHONIOENCODING='utf-8', PYTHONUTF8='1', PYTHONDONTWRITEBYTECODE='1')
    result = subprocess.run([sys.executable, *words[1:]], cwd=root, env=env,
                            capture_output=True, text=True, encoding='utf-8', timeout=60)
    if result.returncode:
        raise ValueError(command + '\n' + result.stdout + result.stderr)
    return result.stdout


def execute_chapter(root, chapter, show=True):
    outputs = {}
    for command in commands(root, chapter):
        output = run_command(root, command)
        outputs[command] = {'stdout': output, 'returncode': 0}
        if show:
            print('$ ' + command, flush=True)
            print(output, end='', flush=True)
    return outputs


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('--all', action='store_true', help='처음부터 모든 장 실행')
    group.add_argument('--chapter', choices=CHAPTERS, help='현재 상태에서 한 장만 실행')
    args = parser.parse_args()
    root = Path(__file__).resolve().parents[1]
    if args.all:
        reset(root)
    try:
        for chapter in CHAPTERS if args.all else (args.chapter,):
            execute_chapter(root, chapter)
            print(run_command(root, 'python course.py check ' + chapter), end='', flush=True)
    except ValueError as error:
        print('✖ 막힘: ' + str(error))
        return 1
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
