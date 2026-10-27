"""UTF-8과 고정 JSON 형식으로 파일을 읽고 쓴다."""
import json
from pathlib import Path


def json_text(value):
    return json.dumps(value, ensure_ascii=False, sort_keys=True, indent=2) + '\n'


def write_text(path, text):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(text.replace('\r\n', '\n').encode('utf-8'))


def write_json(path, value):
    write_text(path, json_text(value))


def read_json(path):
    return json.loads(Path(path).read_text(encoding='utf-8'))
