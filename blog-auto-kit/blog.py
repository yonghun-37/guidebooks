"""장별 실습을 하나의 한국어 명령으로 실행한다."""
import sys
from pathlib import Path

if sys.version_info < (3, 11):
    raise SystemExit('✖ 막힘: Python 3.11 이상 필요 → python3.11 blog.py로 실행하세요')

from core.actions import content_action, monetize_action, operations_action
from core.cli import make_parser
from core.clock import checked_today
from core.config import load_config
from core.files import write_json
from core.state import Store
from core.terminal import capture_command
from core.publish_actions import gate_action, wordpress_action

ROOT = Path(__file__).resolve().parent


def sample_run(root, store, config, args):
    from core.demo import run_demo
    run_demo(root, store, config, args.today, args.sample)


def execute(args):
    try:
        path = ROOT / (args.config or ('config.toml' if (ROOT / 'config.toml').exists()
                                     else 'config.example.toml'))
        config, store = load_config(path), Store(ROOT)
        args.today = checked_today(args.today or config.get('clock', {}).get('today', '2026-10-27'))
        if args.command in ('topics', 'draft'):
            content_action(ROOT, store, config, args)
        elif args.command == 'gate':
            gate_action(ROOT, store, args)
        elif args.command in ('publish', 'status'):
            wordpress_action(ROOT, store, config, args)
        elif args.command == 'run':
            if any((args.ops, args.restore, args.audit, args.scenarios)):
                operations_action(ROOT, store, args)
            else:
                sample_run(ROOT, store, config, args)
        else:
            monetize_action(ROOT, store, config, args)
        write_json(ROOT / 'output/state.json', store.snapshot())
        return 0
    except (ValueError, OSError, KeyError) as error:
        message = str(error)
        if isinstance(error, OSError):
            message = '파일·연결을 열 수 없음 → doctor와 서버 주소를 확인하세요'
        print('✖ 막힘: ' + message)
        return 1


def main():
    args = make_parser().parse_args()
    label = 'python blog.py ' + ' '.join(sys.argv[1:])
    return capture_command(ROOT, label, lambda: execute(args))


if __name__ == '__main__':
    raise SystemExit(main())
