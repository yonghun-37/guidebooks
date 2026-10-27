"""월 비용 예약과 확정을 마이크로달러로 기록한다."""
import json
from decimal import Decimal, ROUND_CEILING


def _micro(amount):
    """달러 값을 마이크로달러로 올림한다."""
    value = Decimal(str(amount))
    if not value.is_finite() or value < 0:
        raise ValueError('비용은 0 이상의 유한값이어야 합니다')
    return int((value * 1000000).to_integral_value(rounding=ROUND_CEILING))


def _encode(row):
    """상태 저장소와 같은 JSON 형식으로 직렬화한다."""
    return json.dumps(row, ensure_ascii=False, sort_keys=True, indent=2) + '\n'


def reserve_cost(store, run_id, amount, today, monthly_cap):
    """쓰기 잠금 안에서 중복과 월 상한을 원자적으로 확인한다."""
    reserved, cap = _micro(amount), _micro(monthly_cap)
    with store.connect() as db:
        db.execute('BEGIN IMMEDIATE')
        if db.execute('SELECT 1 FROM costs WHERE key = ?', (run_id,)).fetchone():
            raise ValueError('이미 예약된 실행입니다')
        rows = [json.loads(row[0]) for row in db.execute('SELECT value FROM costs')]
        total = sum(row['micro_usd'] for row in rows if row['date'][:7] == today[:7])
        if total + reserved > cap:
            raise ValueError('월 비용 상한 초과')
        row = {'run_id': run_id, 'date': today, 'micro_usd': reserved, 'status': 'reserved'}
        db.execute('INSERT INTO costs (key, value) VALUES (?, ?)', (run_id, _encode(row)))
    return row


def settle_cost(store, run_id, amount, today):
    """예약한 실행의 실제 비용을 원자적으로 확정한다."""
    cost = _micro(amount)
    with store.connect() as db:
        db.execute('BEGIN IMMEDIATE')
        saved = db.execute('SELECT value FROM costs WHERE key = ?', (run_id,)).fetchone()
        if not saved or json.loads(saved[0])['status'] != 'reserved':
            raise ValueError('확정 가능한 예약이 없습니다')
        row = dict(json.loads(saved[0]), micro_usd=cost, status='settled', settled_at=today)
        db.execute('UPDATE costs SET value = ? WHERE key = ?', (_encode(row), run_id))
    return row
