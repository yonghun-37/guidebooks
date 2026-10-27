"""글·실행·협찬·링크·비용 상태를 SQLite 한 파일에 저장한다."""
import json
import sqlite3
from pathlib import Path
from core.files import json_text

TABLES = ('posts', 'runs', 'sponsors', 'links', 'costs')


class Store:
    def __init__(self, root):
        self.path = Path(root) / 'private/state.sqlite3'
        self.path.parent.mkdir(parents=True, exist_ok=True)
        with self.connect() as db:
            for name in TABLES:
                db.execute(f'CREATE TABLE IF NOT EXISTS {name} '
                           '(key TEXT PRIMARY KEY, value TEXT NOT NULL)')

    def connect(self):
        return sqlite3.connect(self.path, timeout=5)

    def table(self, table):
        if table not in TABLES:
            raise ValueError('상태 표 이름 오류 → core/state.py의 TABLES를 확인하세요')
        return table

    def put(self, table, key, value):
        with self.connect() as db:
            db.execute(f'INSERT OR REPLACE INTO {self.table(table)} VALUES (?, ?)',
                       (key, json_text(value)))

    def get(self, table, key, default=None):
        with self.connect() as db:
            row = db.execute(f'SELECT value FROM {self.table(table)} WHERE key=?',
                             (key,)).fetchone()
        return json.loads(row[0]) if row else default

    def all(self, table):
        with self.connect() as db:
            rows = db.execute(f'SELECT value FROM {self.table(table)} ORDER BY key').fetchall()
        return [json.loads(row[0]) for row in rows]

    def claim(self, key, record):
        with self.connect() as db:
            result = db.execute('INSERT OR IGNORE INTO runs VALUES (?, ?)',
                                (key, json_text(record)))
        return result.rowcount == 1

    def snapshot(self):
        return {name: self.all(name) for name in TABLES}
