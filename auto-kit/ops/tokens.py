"""키를 출력하지 않고 갱신한다. 네트워크는 live에서 호출자가 명시한다."""
import json
from datetime import timedelta
from common import kit_path, secrets, read_json, save_json, now, timestamp
from transport import HTTP

def import_instagram(config):
    """재인증한 환경 자격을 명시적으로 적용. 원격 호출·비밀 출력 없음."""
    values = secrets()
    token = {'access_token': values.get('IG_ACCESS_TOKEN'),
             'issued_at': values.get('IG_TOKEN_ISSUED_AT'),
             'expires_at': values.get('IG_TOKEN_EXPIRES_AT')}
    if not all(token.values()):
        raise ValueError('새 IG_ACCESS_TOKEN·IG_TOKEN_ISSUED_AT·IG_TOKEN_EXPIRES_AT을 환경/.env에 모두 넣으세요.')
    issued, expiry = timestamp(token['issued_at']), timestamp(token['expires_at'])
    if not issued <= now() < expiry or expiry <= issued:
        raise ValueError('새 토큰의 발급·만료 시각을 확인하세요. 만료되었거나 미래 발급인 값은 적용하지 않습니다.')
    save_json(kit_path(config['ops']['instagram_token_file']), token)

def instagram_token(config, *, refresh=False, http=None):
    path = kit_path(config['ops']['instagram_token_file'])
    values = secrets()
    token = read_json(path) if path.exists() else {'access_token': values.get('IG_ACCESS_TOKEN'), 'expires_at': values.get('IG_TOKEN_EXPIRES_AT'), 'issued_at': values.get('IG_TOKEN_ISSUED_AT')}
    if not token.get('access_token') or not token.get('expires_at') or not token.get('issued_at'):
        raise ValueError('Instagram 토큰·발급일·만료일이 필요합니다. doctor 안내를 확인하세요.')
    expiry, issued = timestamp(token['expires_at']), timestamp(token['issued_at'])
    if expiry <= now():
        raise ValueError('Instagram 토큰 만료. 본인 계정으로 재인증하세요.')
    if refresh and expiry - now() < timedelta(days=config['ops']['token_warning_days']) and now() - issued >= timedelta(hours=24):
        # 이 엔드포인트는 공식 access_token 쿼리를 요구한다. HTTP 로그를 켜지 않는다.
        raw = (http or HTTP()).json('GET', 'https://graph.instagram.com/refresh_access_token', params={'grant_type': 'ig_refresh_token', 'access_token': token['access_token']})
        if not raw.get('access_token') or not isinstance(raw.get('expires_in'), int):
            raise ValueError('Instagram 갱신 응답 확인 실패. 재인증이 필요합니다.')
        token = {'access_token': raw['access_token'], 'issued_at': now().isoformat(), 'expires_at': (now() + timedelta(seconds=raw['expires_in'])).isoformat()}
        save_json(path, token)
    return token

UPLOAD_SCOPE = 'https://www.googleapis.com/auth/youtube.upload'
ANALYTICS_SCOPE = 'https://www.googleapis.com/auth/yt-analytics.readonly'
CHANNEL_SCOPE = 'https://www.googleapis.com/auth/youtube.readonly'

def google_session(config, *, analytics=False):
    token_path = kit_path(config['ops']['google_token_file'])
    client_path = kit_path(config['ops']['google_client_file'])
    if not token_path.is_file() or not client_path.is_file():
        raise ValueError('Google 사용자 OAuth 파일이 없습니다. python oauth_setup.py를 실행하세요.')
    try:
        client, token = read_json(client_path)['installed'], read_json(token_path)
        scopes = token.get('scopes', [])
        scopes = scopes.split() if isinstance(scopes, str) else scopes
        scope = ANALYTICS_SCOPE if analytics else UPLOAD_SCOPE
        if token['client_id'] != client['client_id'] or token['client_secret'] != client['client_secret'] or token['token_uri'] != 'https://oauth2.googleapis.com/token' or scope not in scopes:
            raise ValueError()
        if CHANNEL_SCOPE not in scopes:
            raise ValueError('실제 채널 확인 권한 필요')
        if (config['mode'] == 'post_review' or config['youtube'].get('publishAt')) and 'https://www.googleapis.com/auth/youtube.force-ssl' not in scopes:
            raise ValueError('예약 취소 권한 필요')
        from google.oauth2.credentials import Credentials
        from google.auth.transport.requests import AuthorizedSession, Request
        credentials = Credentials.from_authorized_user_info(token, scopes=scopes)
        if not credentials.valid:
            credentials.refresh(Request())
            updated = json.loads(credentials.to_json())
            if token.get('granted_at'): updated['granted_at'] = token['granted_at']
            save_json(token_path, updated)
        return AuthorizedSession(credentials)
    except ImportError:
        raise ValueError('python -m pip install --only-binary=:all: -r requirements-live.txt를 실행하세요.') from None
    except Exception:
        raise ValueError('OAuth 파일·scope·만료를 확인하고 필요하면 재동의하세요. Testing 모드는 7일 만료 조건을 확인하세요.') from None

def main():
    import argparse
    from common import load_config
    parser = argparse.ArgumentParser(description='재인증한 토큰을 비공개 저장 위치에 적용합니다. 값은 출력하지 않습니다.')
    parser.add_argument('command', choices=['import-instagram'])
    parser.add_argument('--config')
    args = parser.parse_args()
    config = load_config(kit_path(args.config) if args.config else None)
    import_instagram(config)
    print('Instagram 새 토큰 적용 완료. 비밀 값은 출력하지 않습니다.')

if __name__ == '__main__':
    from common import cli
    cli(main)
