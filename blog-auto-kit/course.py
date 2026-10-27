"""A1부터 A12까지 시작 상태 복원과 성공 여부를 확인한다."""
import argparse
import sys
from pathlib import Path

if sys.version_info < (3, 11):
    raise SystemExit('✖ 막힘: Python 3.11 이상 필요 → python3.11 course.py로 실행하세요')

from core.terminal import capture_command
from course.steps import CHAPTERS
from course.snapshots import reset, restore_start
from course.artifacts import check_chapter
from course.doctor import doctor

ROOT = Path(__file__).resolve().parent


def execute(args):
    try:
        if args.action == 'doctor':
            doctor(ROOT, args.today)
        elif args.action == 'reset':
            reset(ROOT)
            print('✔ 통과: 실습 상태 초기화 · .env 보존')
        elif args.action == 'start':
            restore_start(ROOT, args.chapter)
            print('✔ 통과: ' + args.chapter + ' 시작 상태 복원')
        else:
            check_chapter(ROOT, args.chapter)
        return 0
    except (ValueError, OSError, KeyError) as error:
        print('✖ 막힘: ' + str(error))
        return 1


def main():
    parser = argparse.ArgumentParser(description='장별 시작 상태와 예상 결과 확인')
    commands = parser.add_subparsers(dest='action', required=True)
    for name in ('doctor', 'start', 'check', 'reset'):
        sub = commands.add_parser(name)
        if name in ('start', 'check'):
            sub.add_argument('chapter', choices=CHAPTERS)
        sub.add_argument('--today', default='2026-10-27', help='고정 기준일')
    args = parser.parse_args()
    if args.action == 'doctor':
        label = 'python course.py ' + ' '.join(sys.argv[1:])
        return capture_command(ROOT, label, lambda: execute(args))
    return execute(args)


if __name__ == '__main__':
    raise SystemExit(main())
