"""TOML 설정과 비밀 파일을 읽고 줄 번호와 수정 방법을 알려 준다."""
import re
import tomllib
from pathlib import Path
from urllib.parse import urlsplit
from core.clock import checked_today


def error_at(text, key, reason, fix):
    line = next((i for i, row in enumerate(text.splitlines(), 1)
                 if re.match(r'\s*' + re.escape(key) + r'\s*=', row)), 1)
    raise ValueError(f'설정 {line}줄 {key}: {reason} → {fix}로 고치세요')


def load_config(path):
    text = Path(path).read_text(encoding='utf-8')
    try:
        config = tomllib.loads(text)
    except tomllib.TOMLDecodeError as error:
        match = re.search(r'line (\d+)', str(error))
        line = match.group(1) if match else '1'
        raise ValueError(f'설정 {line}줄: TOML 문법 오류 → 따옴표·대괄호를 고치세요') from error
    validate_config(config, text)
    return config


def validate_config(config, text):
    wp = config.get('wordpress', {})
    url = wp.get('url', 'http://127.0.0.1:8767')
    if not isinstance(url, str) or urlsplit(url).scheme not in ('http', 'https'):
        error_at(text, 'url', '주소 문자열이 아님', 'url="http://127.0.0.1:8767"')
    if wp.get('mode', 'mock') not in ('mock', 'local', 'live'):
        error_at(text, 'mode', 'mock/local/live만 가능', 'mode="mock"')
    mode = config.get('publishing', {}).get('mode', 'approval')
    if mode not in ('approval', 'auto'):
        error_at(text, 'mode', '유예·거부 검증 전 사후 확인 불가', 'mode="approval"')
    for key, default in (('daily_limit', 2), ('ad_after_h2', 2)):
        value = config.get('publishing', {}).get(key, config.get('ads', {}).get(key, default))
        if type(value) is not int or value < 1:
            error_at(text, key, '양의 정수가 필요함', f'{key}=2')
    try:
        checked_today(config.get('clock', {}).get('today', '2026-10-27'))
    except (TypeError, ValueError):
        error_at(text, 'today', '날짜 형식 오류', 'today="2026-10-27"')


def read_secrets(root):
    path = Path(root) / '.env'
    if not path.exists():
        return {}
    pairs = [line.split('=', 1) for line in path.read_text(encoding='utf-8').splitlines()
             if line.strip() and not line.lstrip().startswith('#') and '=' in line]
    return {key.strip(): value.strip() for key, value in pairs}
