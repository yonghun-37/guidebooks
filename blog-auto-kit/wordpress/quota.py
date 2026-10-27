"""서로 다른 실행도 같은 날짜의 예약 상한을 원자적으로 지킨다."""
import json
from core.files import json_text


def reserve_slot(store, destination, content_id, today, limit, content_digest=None):
    prefix = 'quota:' + destination + ':' + today + ':'
    key = prefix + content_id
    with store.connect() as db:
        db.execute('BEGIN IMMEDIATE')
        content_key = 'content:' + destination + ':' + (content_digest or content_id)
        saved = db.execute('SELECT value FROM runs WHERE key=?', (content_key,)).fetchone()
        if saved and json.loads(saved[0])['owner'] != content_id:
            raise ValueError('같은 내용의 예약이 이미 있음 → 기존 post_id를 확인하세요')
        if not saved:
            db.execute('INSERT INTO runs VALUES (?, ?)',
                       (content_key, json_text({'id': content_key, 'owner': content_id})))
        rows = db.execute('SELECT key FROM runs').fetchall()
        keys = [row[0] for row in rows if row[0].startswith(prefix)]
        if key in keys:
            return
        if len(keys) >= limit:
            raise ValueError('하루 발행 상한 도달 → 다음 날짜에 다시 확인하세요')
        db.execute('INSERT INTO runs VALUES (?, ?)',
                   (key, json_text({'id': key, 'state': 'reserved', 'date': today})))
