"""승인 요청 알림을 기본 드라이런으로 기록한다."""
import json
from pathlib import Path
from urllib.parse import urlsplit


def _valid_url(url):
    """허용된 HTTPS 알림 엔드포인트인지 확인한다."""
    parsed = urlsplit(url)
    return (parsed.scheme == 'https' and parsed.hostname in ('discord.com', 'discordapp.com', 'api.telegram.org')
            and parsed.username is None and parsed.password is None and parsed.port in (None, 443)
            and not parsed.fragment and not parsed.query)


def notify(root, event, today, live=False, transport=None, secrets=None) -> dict:
    """드라이런 기록 또는 명시적 전송 함수로 알림을 처리한다."""
    if not isinstance(event, str) or not event or any(c not in 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789_-' for c in event):
        raise ValueError('알림 이벤트는 영문 식별자로 입력하세요')
    record = {'event': event, 'today': today, 'live': bool(live)}
    if live:
        url = (secrets or {}).get('url', '')
        if not _valid_url(url) or transport is None:
            raise ValueError('허용된 HTTPS 주소와 전송 함수가 필요합니다')
        message = f'{today}: {event}'
        if urlsplit(url).hostname == 'api.telegram.org':
            chat_id = (secrets or {}).get('chat_id')
            if not chat_id:
                raise ValueError('텔레그램 대화 ID가 필요합니다')
            body = {'chat_id': chat_id, 'text': message}
        else:
            body = {'content': message}
        transport(url, body)
    output = Path(root) / 'output/notifications.json'
    output.parent.mkdir(parents=True, exist_ok=True)
    previous = json.loads(output.read_text(encoding='utf-8')) if output.exists() else []
    previous.append(record)
    output.write_text(json.dumps(previous, ensure_ascii=False, indent=2) + '\n', encoding='utf-8', newline='\n')
    return record
