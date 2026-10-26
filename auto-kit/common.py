"""키트 경로·비공개 파일·설정. 비밀 값은 오류 문자열에 넣지 않는다."""
import hashlib
import json
import os
from pathlib import Path
from datetime import datetime, timezone

ROOT = Path(__file__).resolve().parent

def now():
    return datetime.now(timezone.utc)

def local_now():
    return datetime.now().astimezone()

def canonical(value):
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(',', ':'))

def digest(path):
    h = hashlib.sha256()
    with Path(path).open('rb') as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b''):
            h.update(block)
    return h.hexdigest()

def hashed(value):
    return hashlib.sha256(canonical(value).encode()).hexdigest()

def read_json(path):
    return json.loads(Path(path).read_text(encoding='utf-8-sig'))

def save_json(path, value):
    """shorts-kit/upload.py private_json을 복사·일반화. 임시 파일부터 0600."""
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    temp = path.with_name(path.name + '.tmp')
    fd = os.open(temp, os.O_WRONLY | os.O_CREAT | os.O_TRUNC, 0o600)
    with os.fdopen(fd, 'w', encoding='utf-8') as stream:
        stream.write(json.dumps(value, ensure_ascii=False, indent=2) + '\n')
    temp.chmod(0o600)
    temp.replace(path)

def load_config(path=None):
    config = read_json(path or ROOT / 'config.example.json')
    if config['mode'] not in ('auto', 'post_review', 'approval'):
        raise ValueError('mode는 auto/post_review/approval 중 하나여야 합니다.')
    for key in ('daily_usd', 'monthly_usd'):
        value = config['budget'][key]
        if not isinstance(value, (int, float)) or not 0 < value < 100000:
            raise ValueError('일/월 비용 상한은 0보다 큰 유한한 숫자여야 합니다.')
    return config

def secrets():
    values = {}
    path = ROOT / '.env'
    if path.exists():
        for line in path.read_text(encoding='utf-8-sig').splitlines():
            line = line.strip()
            if not line or line.startswith('#'):
                continue
            key, sep, value = line.partition('=')
            if not sep or not key.strip().replace('_', '').isalnum():
                raise ValueError('.env는 이름=값 형식으로 작성하세요. 값은 출력하지 않습니다.')
            values[key.strip()] = value.strip().strip('"\'')
    values.update(os.environ)
    return values

def kit_path(value):
    path = Path(value).expanduser()
    return path.resolve() if path.is_absolute() else (ROOT / path).resolve()

def timestamp(value):
    try:
        result = datetime.fromisoformat(value.replace('Z', '+00:00'))
        if result.tzinfo is None:
            raise ValueError()
        return result.astimezone(timezone.utc)
    except (ValueError, TypeError, AttributeError):
        raise ValueError('예약·만료 시각에는 UTC 오프셋이 있는 ISO8601 값을 넣으세요.') from None

def cli(main):
    try:
        main()
    except (ValueError, OSError, KeyError) as error:
        # 예상 외 네트워크 예외/응답 전문의 traceback을 공개 로그로 내보내지 않는다.
        print('중단: ' + (str(error) if isinstance(error, ValueError) else '파일·설정 항목을 확인하세요.'))
        raise SystemExit(1) from None
