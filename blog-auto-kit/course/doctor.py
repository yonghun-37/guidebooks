"""Python·필수 폴더·포트·쓰기 권한·고정 시계를 검사한다."""
import socket
import sys
import tempfile
from core.clock import checked_today, SEED


def doctor(root, today='2026-10-27'):
    if sys.version_info < (3, 11):
        raise ValueError('Python 버전 낮음 → Python 3.11 이상으로 실행하세요')
    for name in ('core', 'content', 'providers', 'gates', 'wordpress', 'monetize',
                 'analytics', 'ops', 'course', 'samples'):
        if not (root / name).is_dir():
            raise ValueError(name + ' 폴더 없음 → 키트를 빈 폴더에 다시 복사하세요')
    with tempfile.TemporaryFile(dir=root) as stream:
        stream.write(b'check')
    try:
        with socket.socket() as sock:
            sock.bind(('127.0.0.1', 8767))
    except OSError as error:
        raise ValueError('포트 8767 사용 중 → 해당 mock 서버를 종료하고 doctor를 실행하세요') from error
    checked_today(today)
    print('✔ 통과: Python 3.11 이상 · 폴더 · 쓰기 권한 · 포트 8767')
    print(f'✔ 통과: 고정 시계 {today} · 시드 {SEED}')
