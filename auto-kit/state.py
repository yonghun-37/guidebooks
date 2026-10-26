"""SQLite 영속 상태·비용 예약·실행 잠금. 비용 단위는 micro-USD."""
from contextlib import contextmanager
from datetime import datetime, timezone
import json
import math
import os
from pathlib import Path
import sqlite3
from common import now, canonical

class BudgetExceeded(ValueError):
    pass

class Busy(ValueError):
    pass

class Store:
    def __init__(self, root):
        self.root = Path(root).resolve()
        self.root.mkdir(parents=True, exist_ok=True)
        self.root.chmod(0o700)
        self.path = self.root / 'state.sqlite'
        self.db = sqlite3.connect(self.path, timeout=30, isolation_level=None)
        self.path.chmod(0o600)
        self.db.row_factory = sqlite3.Row
        self.db.executescript('''
        PRAGMA journal_mode=WAL;
        CREATE TABLE IF NOT EXISTS runs(id TEXT PRIMARY KEY, flow TEXT, status TEXT, data TEXT, updated TEXT);
        CREATE TABLE IF NOT EXISTS calls(id INTEGER PRIMARY KEY, run_id TEXT, kind TEXT, reserved INTEGER, actual INTEGER, usage TEXT, created TEXT);
        CREATE TABLE IF NOT EXISTS claims(flow TEXT, account TEXT, hash TEXT, lane TEXT, run_id TEXT, PRIMARY KEY(flow,account,hash,lane));
        CREATE TABLE IF NOT EXISTS metrics(run_id TEXT, metric TEXT, value REAL, unit TEXT, day TEXT, collected TEXT, PRIMARY KEY(run_id,metric,day));
        CREATE TABLE IF NOT EXISTS events(id INTEGER PRIMARY KEY, run_id TEXT, step TEXT, status TEXT, created TEXT);
        CREATE TABLE IF NOT EXISTS kv(key TEXT PRIMARY KEY, value TEXT);
        ''')

    @contextmanager
    def lock(self):
        """OS가 프로세스 종료 때 해제한다. 같은 저장소의 두 실행은 겹치지 않는다."""
        with (self.root / 'runner.lock').open('a+b') as stream:
            try:
                if os.name == 'nt':
                    import msvcrt
                    stream.write(b'0'); stream.flush(); stream.seek(0)
                    msvcrt.locking(stream.fileno(), msvcrt.LK_NBLCK, 1)
                else:
                    import fcntl
                    fcntl.flock(stream, fcntl.LOCK_EX | fcntl.LOCK_NB)
            except OSError:
                raise Busy('다른 실행이 진행 중입니다. 다음 예약에서 다시 실행하세요.') from None
            try:
                yield
            finally:
                if os.name == 'nt':
                    stream.seek(0); msvcrt.locking(stream.fileno(), msvcrt.LK_UNLCK, 1)
                else:
                    fcntl.flock(stream, fcntl.LOCK_UN)

    def save(self, run):
        self.db.execute('INSERT OR REPLACE INTO runs VALUES(?,?,?,?,?)', (run['id'], run['flow'], run['status'], canonical(run), now().isoformat()))

    def get(self, identifier):
        row = self.db.execute('SELECT data FROM runs WHERE id=?', (identifier,)).fetchone()
        if not row:
            raise ValueError('실행 ID가 없습니다. status 명령으로 확인하세요.')
        return json.loads(row[0])

    def runs(self):
        return [json.loads(r[0]) for r in self.db.execute('SELECT data FROM runs ORDER BY updated DESC')]

    def event(self, run_id, step, status):
        # 로그에는 내용·URL·예외 전문·인증 값을 넣지 않는다.
        self.db.execute('INSERT INTO events(run_id,step,status,created) VALUES(?,?,?,?)', (run_id, step, status, now().isoformat()))
        with (self.root / 'execution.log').open('a', encoding='utf-8') as stream:
            stream.write(canonical({'id': run_id, 'step': step, 'status': status, 'at': now().isoformat()}) + '\n')

    def reserve(self, run_id, kind, amount, *, daily, monthly):
        units = math.ceil(amount * 1000000)
        if units < 0 or not math.isfinite(amount):
            raise ValueError('비용 견적을 확인하세요.')
        day = now().date().isoformat()
        self.db.execute('BEGIN IMMEDIATE')
        try:
            rows = self.db.execute('SELECT COALESCE(actual,reserved),created FROM calls WHERE created>=?', (day[:7],)).fetchall()
            month_spend = sum(r[0] for r in rows)
            day_spend = sum(r[0] for r in rows if r[1].startswith(day))
            envelope = self.db.execute("SELECT id,reserved,created FROM calls WHERE run_id=? AND kind='run:maximum' AND actual IS NULL",(run_id,)).fetchone() if kind != 'run:maximum' else None
            day_credit = units if envelope and envelope['created'].startswith(day) else 0
            month_credit = units if envelope and envelope['created'].startswith(day[:7]) else 0
            if day_spend + units - day_credit > int(daily * 1e6) or month_spend + units - month_credit > int(monthly * 1e6):
                raise BudgetExceeded('일/월 비용 상한에 도달했습니다. 생성 중단·비용 장부를 확인하세요.')
            if envelope:
                if units > envelope['reserved']:
                    raise BudgetExceeded('실행 예상 최대비/재시도 예산을 넘었습니다. 추가 생성을 중단합니다.')
                self.db.execute('UPDATE calls SET reserved=reserved-? WHERE id=?',(units,envelope['id']))
            cur = self.db.execute('INSERT INTO calls(run_id,kind,reserved,usage,created) VALUES(?,?,?,?,?)', (run_id, kind, units, '{}', now().isoformat()))
            self.db.execute('COMMIT')
            return cur.lastrowid
        except BaseException:
            self.db.execute('ROLLBACK')
            raise

    def settle(self, ticket, amount, usage):
        if not isinstance(amount, (int, float)) or not math.isfinite(amount) or amount < 0:
            raise ValueError('실제 비용이 올바르지 않아 예약액을 유지합니다.')
        units = math.ceil(amount * 1e6)
        self.db.execute('BEGIN IMMEDIATE')
        try:
            row = self.db.execute('SELECT reserved,actual,run_id,kind FROM calls WHERE id=?', (ticket,)).fetchone()
            if row['actual'] is not None:
                raise ValueError('이미 정산한 비용 호출입니다.')
            self.db.execute('UPDATE calls SET actual=?,usage=? WHERE id=?', (units, canonical(usage), ticket))
            if row['kind'] != 'run:maximum' and units <= row['reserved']:
                self.db.execute("UPDATE calls SET reserved=reserved+? WHERE run_id=? AND kind='run:maximum' AND actual IS NULL",(row['reserved']-units,row['run_id']))
            self.db.execute('COMMIT')
        except BaseException:
            self.db.execute('ROLLBACK');raise
        if units > row[0]:
            raise BudgetExceeded('실제 사용비가 예약액을 넘었습니다. 추가 호출을 중지하고 가격표·usage를 확인하세요.')

    def finish_budget(self, run_id):
        row=self.db.execute("SELECT id FROM calls WHERE run_id=? AND kind='run:maximum' AND actual IS NULL",(run_id,)).fetchone()
        if row:self.settle(row['id'],0,{'released_unused_envelope':True})

    def calls(self):
        return [dict(r) for r in self.db.execute('SELECT * FROM calls')]

    def spend(self):
        rows = self.calls()
        day, month = now().date().isoformat(), now().strftime('%Y-%m')
        cost = lambda r: (r['actual'] if r['actual'] is not None else r['reserved']) / 1e6
        return {'total': sum(map(cost, rows)), 'day': sum(cost(r) for r in rows if r['created'].startswith(day)), 'month': sum(cost(r) for r in rows if r['created'].startswith(month)), 'pending': sum(r['reserved'] / 1e6 for r in rows if r['actual'] is None)}

    def claim(self, run, fingerprint):
        account = run['target']['account']
        lane = 'live' if run['live'] else 'dry'
        row = self.db.execute('SELECT run_id FROM claims WHERE flow=? AND account=? AND hash=? AND lane=?', (run['flow'], account, fingerprint, lane)).fetchone()
        if row and row[0] != run['id']:
            raise ValueError('같은 콘텐츠의 게시/시도 기록이 있습니다. 중복 게시를 차단했습니다.')
        self.db.execute('INSERT OR IGNORE INTO claims VALUES(?,?,?,?,?)', (run['flow'], account, fingerprint, lane, run['id']))

    def kv(self, key, value=None):
        if value is not None:
            self.db.execute('INSERT OR REPLACE INTO kv VALUES(?,?)', (key, canonical(value)))
        row = self.db.execute('SELECT value FROM kv WHERE key=?', (key,)).fetchone()
        return json.loads(row[0]) if row else None
