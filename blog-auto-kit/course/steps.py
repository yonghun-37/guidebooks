"""교과서와 재현 검사가 같은 명령 표를 읽게 한다."""
import re
from pathlib import Path

CHAPTERS = tuple('A' + str(i) for i in range(1, 13)) + ('E2E',)


def commands(root, chapter):
    if chapter not in CHAPTERS:
        raise ValueError('장 번호 오류 → A1~A12 또는 E2E를 입력하세요')
    rows = []
    for line in (Path(root) / 'course/commands.md').read_text(encoding='utf-8').splitlines():
        match = re.fullmatch(r'\| (A\d+|E2E) \| `([^`]+)` \| `([^`]+)` \|', line)
        if match and match[1] == chapter:
            if match[2] != match[3]:
                raise ValueError('운영체제 명령 불일치 → commands.md를 확인하세요')
            rows.append(match[2])
    if not rows:
        raise ValueError('장별 명령 없음 → course/commands.md를 확인하세요')
    return rows
