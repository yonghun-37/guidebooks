"""실습 산출물의 상대 경로와 SHA-256을 비교한다."""
from core.files import read_json
from core.hashes import digest


def manifest(root):
    paths = list((root / 'output').rglob('*')) if (root / 'output').exists() else []
    paths += list((root / 'private/mock-wp').rglob('*')) if (root / 'private/mock-wp').exists() else []
    events = root / 'private/events.json'
    if events.exists():
        paths.append(events)
    return {path.relative_to(root).as_posix(): digest(path.read_bytes())
            for path in sorted(paths) if path.is_file()}


def differences(expected, actual):
    return [(name, '누락' if name not in actual else '추가' if name not in expected else '내용 변경')
            for name in sorted(expected.keys() | actual.keys()) if expected.get(name) != actual.get(name)]


def check_chapter(root, chapter):
    expected = root / 'course/expected' / chapter
    if not (expected / 'hashes.json').exists():
        raise ValueError('예상 출력 없음 → course/build_expected.py로 생성하세요')
    changes = differences(read_json(expected / 'hashes.json'), manifest(root))
    if changes:
        name, reason = changes[0]
        raise ValueError(f'{chapter} {name}: {reason} ({len(changes)}개 차이)\n'
                         f'→ python course.py start {chapter} 후 그 장 명령을 다시 실행하세요')
    compare_terminal(root, chapter, expected)
    compare_state(root, expected)
    print(f'✔ 통과: {chapter} 산출물·상태·터미널 출력 일치')


def compare_terminal(root, chapter, expected):
    from course.steps import commands
    current = read_json(root / 'private/terminal.json')
    outputs = read_json(expected / 'outputs.json')
    for command in commands(root, chapter):
        if current.get(command) != outputs[command]:
            raise ValueError(f'{chapter} 명령 출력이 다름: {command}\n'
                             f'→ python course/execute.py --chapter {chapter}로 다시 실행하세요')


def compare_state(root, expected):
    from core.state import Store
    if Store(root).snapshot() != read_json(expected / 'state.json'):
        raise ValueError('SQLite 상태가 예상과 다름 → course.py start로 복원하고 다시 실행하세요')
