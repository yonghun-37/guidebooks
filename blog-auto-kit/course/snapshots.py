"""장 시작 상태를 고정 ZIP으로 저장하고 앞 장까지 복원한다."""
import shutil
import sqlite3
import zipfile
from pathlib import PurePosixPath
from core.state import Store


def reset(root):
    for name in ('private', 'output'):
        path = root / name
        if path.exists():
            shutil.rmtree(path)
    (root / 'config.toml').unlink(missing_ok=True)


def save_start(root, destination):
    store = Store(root)
    with store.connect() as db:
        sql = ('\n'.join(db.iterdump()) + '\n').encode('utf-8')
    items = {'database.sql': sql}
    for directory in ('private', 'output'):
        for path in sorted((root / directory).rglob('*')):
            if path.is_file() and path.name != 'state.sqlite3':
                items[path.relative_to(root).as_posix()] = path.read_bytes()
    destination.parent.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(destination, 'w') as archive:
        for name, data in sorted(items.items()):
            info = zipfile.ZipInfo(name, (1980, 1, 1, 0, 0, 0))
            info.create_system = 3
            info.external_attr = 0o100600 << 16
            archive.writestr(info, data)


def restore_start(root, chapter):
    source = root / 'course/states' / (chapter + '.zip')
    if not source.exists():
        raise ValueError('장 시작 상태 없음 → course/build_expected.py로 생성하세요')
    with zipfile.ZipFile(source) as archive:
        data = {name: archive.read(name) for name in archive.namelist()}
    for name in data:
        parts = PurePosixPath(name).parts
        if name != 'database.sql' and (not parts or parts[0] not in ('output', 'private')
                or '..' in parts or '\\' in name):
            raise ValueError('시작 상태 경로 오류 → 원본 키트를 다시 복사하세요')
    reset(root)
    store = Store(root)
    store.path.unlink()
    with sqlite3.connect(store.path) as db:
        db.executescript(data.pop('database.sql').decode('utf-8'))
    for name, value in data.items():
        path = root / name
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(value)
