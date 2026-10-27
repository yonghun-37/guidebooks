"""개인정보나 비밀 대신 고정 날짜와 사건 이름만 기록한다."""
from core.files import write_json, read_json


def record_event(root, event, content_id, today):
    path = root / 'private/events.json'
    rows = read_json(path) if path.exists() else []
    rows.append({'date': today, 'event': event, 'content_id': content_id})
    write_json(path, rows)
