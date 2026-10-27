"""SQLite 논리 덤프와 mock 자료를 결정적으로 백업하고 복원한다."""
import os
import shutil
import sqlite3
import tempfile
import zipfile
from pathlib import Path, PurePosixPath
from core.state import Store, TABLES


def _entries(root):
    """비밀 파일을 제외하고 백업할 데이터를 수집한다."""
    db = Store(root)
    with db.connect() as connection:
        dump = '\n'.join(connection.iterdump()) + '\n'
    items = {'state.sql': dump.encode('utf-8')}
    for name in ('config.example.toml', 'config.toml'):
        path = root / name
        if path.is_file() and not path.is_symlink():
            items[name] = path.read_bytes()
    directory = root / 'private/mock-wp'
    if directory.exists():
        for path in sorted(directory.rglob('*')):
            if path.is_symlink():
                raise ValueError('심볼릭 링크는 백업할 수 없습니다')
            if path.is_file() and not any('.env' in part for part in path.relative_to(directory).parts):
                items[path.relative_to(root).as_posix()] = path.read_bytes()
    if 'config.example.toml' not in items:
        raise ValueError('config.example.toml이 필요합니다')
    return items


def backup(root) -> Path:
    """고정 메타데이터의 ZIP 백업을 만든다."""
    root = Path(root); items = _entries(root)
    target = root / 'output/backups/blog.zip'
    target.parent.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(target, 'w', compression=zipfile.ZIP_STORED) as archive:
        for name, data in sorted(items.items()):
            info = zipfile.ZipInfo(name, (1980, 1, 1, 0, 0, 0))
            info.create_system = 3; info.external_attr = 0o100600 << 16
            archive.writestr(info, data)
    return target


def _read_archive(path):
    """경로와 필수 항목을 검증한 뒤 모든 데이터를 읽는다."""
    try:
        with zipfile.ZipFile(path) as archive:
            names = archive.namelist()
            if len(names) != len(set(names)) or len(names) > 10000:
                raise ValueError('중복되거나 지나치게 많은 백업 항목')
            if not {'state.sql', 'config.example.toml'} <= set(names):
                raise ValueError('필수 백업 항목 누락')
            items = {}
            for info in archive.infolist():
                name = info.filename; parts = PurePosixPath(name).parts
                allowed = name in ('state.sql', 'config.example.toml', 'config.toml') or name.startswith('private/mock-wp/')
                if not allowed or not parts or any(p in ('..', '.') for p in parts) or '\\' in name or any('.env' in part for part in parts) or info.is_dir() or info.file_size > 100_000_000:
                    raise ValueError('허용되지 않는 백업 경로')
                if (info.external_attr >> 16) & 0o170000 == 0o120000:
                    raise ValueError('심볼릭 링크는 복원할 수 없습니다')
                items[name] = archive.read(info)
            return items
    except (zipfile.BadZipFile, OSError, RuntimeError) as exc:
        raise ValueError('백업 파일이 손상되었습니다') from exc


def _stage(root, items, stage):
    """복원 전 임시 DB와 파일을 완성하고 검사한다."""
    database = stage / 'state.sqlite3'
    try:
        with sqlite3.connect(database) as db:
            db.set_authorizer(lambda action, *args: sqlite3.SQLITE_DENY if action in (sqlite3.SQLITE_ATTACH, sqlite3.SQLITE_DETACH) else sqlite3.SQLITE_OK)
            db.executescript(items['state.sql'].decode('utf-8'))
            names = {r[0] for r in db.execute("SELECT name FROM sqlite_master WHERE type='table'")}
            if not set(TABLES) <= names or db.execute('PRAGMA integrity_check').fetchone()[0] != 'ok':
                raise ValueError('상태 DB 구조가 올바르지 않습니다')
    except (sqlite3.Error, UnicodeError) as exc:
        raise ValueError('상태 DB 덤프가 손상되었습니다') from exc
    for name, data in items.items():
        if name != 'state.sql':
            path = stage / name; path.parent.mkdir(parents=True, exist_ok=True)
            path.write_bytes(data)
    (stage / 'private/mock-wp').mkdir(parents=True, exist_ok=True)


def _install(root, stage, names):
    """교체 전 원본을 보존하고 실패 시 모두 되돌린다."""
    saved = stage / 'old'; saved.mkdir(); completed = []
    try:
        for index, (source, target) in enumerate(names):
            target.parent.mkdir(parents=True, exist_ok=True)
            previous = saved / str(index)
            if target.exists():
                os.replace(target, previous)
            completed.append((target, previous))
            os.replace(source, target)
    except Exception:
        for target, previous in reversed(completed):
            if target.is_dir(): shutil.rmtree(target)
            elif target.exists(): target.unlink()
            if previous.exists(): os.replace(previous, target)
        raise


def restore(root, path) -> None:
    """백업을 검증한 뒤 기존 상태를 안전하게 교체한다."""
    root = Path(root); items = _read_archive(path)
    root.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory(prefix='.restore-', dir=root) as folder:
        stage = Path(folder); _stage(root, items, stage)
        pairs = [(stage / 'private/mock-wp', root / 'private/mock-wp')]
        pairs.extend((stage / name, root / name) for name in ('config.example.toml', 'config.toml') if name in items)
        pairs.append((stage / 'state.sqlite3', root / 'private/state.sqlite3'))
        _install(root, stage, pairs)
