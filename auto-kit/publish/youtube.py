"""YouTube private 기본값·예약·재개 업로드와 할당량 연기."""
from pathlib import Path
from common import now, timestamp, read_json
from transport import Deferred, RemoteError
from .youtube_protocol import resumable, ENDPOINT

def channel_id(session):
    try:
        response = session.request('GET', 'https://www.googleapis.com/youtube/v3/channels', params={'part': 'id', 'mine': 'true'}, timeout=60, allow_redirects=False)
        if response.status_code != 200: raise ValueError()
        items = response.json()['items']
        if len(items) != 1 or not isinstance(items[0]['id'], str): raise ValueError()
        return items[0]['id']
    except Exception:
        raise ValueError('현재 OAuth의 실제 YouTube 채널을 확인하지 못했습니다. youtube.readonly 권한과 선택 채널을 확인하세요.') from None

def metadata(draft, target, *, resuming=False):
    for field in ('selfDeclaredMadeForKids', 'containsSyntheticMedia'):
        if type(target.get(field)) is not bool:
            raise ValueError('아동용·AI 표시를 true/false로 결정하세요.')
    status = {k: target[k] for k in ('privacyStatus', 'selfDeclaredMadeForKids', 'containsSyntheticMedia')}
    if status['privacyStatus'] not in ('private', 'public', 'unlisted'):
        raise ValueError('YouTube 공개 범위를 확인하세요.')
    if target.get('publishAt'):
        if status['privacyStatus'] != 'private' or (timestamp(target['publishAt']) <= now() and not resuming):
            raise ValueError('publishAt은 미래 시각·private여야 합니다. 공개 이력도 확인하세요.')
        status['publishAt'] = target['publishAt']
    return {'snippet': {'title': draft['title'][:100], 'description': draft['caption'], 'categoryId': '22', 'defaultLanguage': 'ko'}, 'status': status}

def request_plan(media, body):
    size = Path(media).stat().st_size
    return {'mode': 'dry-run', 'network_calls': 0, 'metadata': body, 'requests': [
        {'method': 'POST', 'url': ENDPOINT, 'headers': {'Authorization': 'Bearer <REDACTED>', 'X-Upload-Content-Length': str(size), 'X-Upload-Content-Type': 'video/mp4'}, 'json': body},
        {'method': 'PUT', 'url': '<saved Location>', 'headers': {'Content-Range': f'bytes 0-{size-1}/{size}'}, 'note': '마지막 외 256KiB 배수 청크. 308 Range 다음부터 재개'},
        {'method': 'PUT', 'url': '<same Location>', 'headers': {'Content-Length': '0', 'Content-Range': f'bytes */{size}'}, 'note': '응답 유실·재시작 때 서버 상태 조회'}]}

class QuotaSession:
    def __init__(self, session): self.session = session
    def request(self, method, url, **kwargs):
        try:
            response = self.session.request(method, url, **kwargs)
        except Exception:
            # google-auth와 requests의 예외가 토큰·세션 URL을 출력하지 않게 경계를 닫는다.
            raise OSError('업로드 연결 실패') from None
        if response.status_code in (403, 429):
            try:
                reasons = {e['reason'] for e in response.json().get('error', {}).get('errors', [])}
            except (ValueError, KeyError, TypeError):
                reasons = set()
            if response.status_code == 429 or reasons & {'quotaExceeded', 'uploadLimitExceeded', 'rateLimitExceeded', 'dailyLimitExceeded'}:
                raise Deferred('YouTube 할당량/채널 업로드 제한으로 연기합니다.')
        return response

def publish(output, body, session):
    path = Path(output) / 'upload-session.json'
    try:
        return resumable(output, body, QuotaSession(session))
    except Deferred:
        if path.exists() and read_json(path).get('phase') == 'starting':
            path.unlink()  # 명백한 할당량 거절 응답. 업로드 세션은 만들어지지 않았다.
        raise

def cancel(video_id, session):
    response = session.request('DELETE', 'https://www.googleapis.com/youtube/v3/videos', params={'id': video_id}, timeout=60, allow_redirects=False)
    if response.status_code != 204:
        raise ValueError('예약 영상 삭제를 확인하지 못했습니다. scheduled 상태를 유지합니다.')
