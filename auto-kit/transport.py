"""작은 HTTP 경계. 리디렉션과 HTTP 디버그 로그를 사용하지 않는다."""
import time
from urllib.parse import urlsplit
import requests

class RemoteError(ValueError):
    def __init__(self, status=0, code=None, subcode=None):
        self.status, self.code, self.subcode = status, code, subcode
        super().__init__(f'외부 API 오류 HTTP {status}. 인증·한도·계정 상태를 확인하세요. 응답 전문은 보관하지 않습니다.')

class Deferred(ValueError):
    pass

class Uncertain(ValueError):
    pass

def https_url(url, hosts=None):
    parsed = urlsplit(url)
    if parsed.scheme != 'https' or not parsed.hostname or parsed.username or parsed.password or parsed.fragment or parsed.port not in (None, 443) or (hosts and parsed.hostname not in hosts):
        raise ValueError('인증 정보를 포함하지 않은 허용된 HTTPS 주소를 사용하세요.')
    return url

class HTTP:
    def __init__(self, session=None):
        self.session = session or requests.Session()

    def request(self, method, url, **kwargs):
        https_url(url)
        try:
            return self.session.request(method, url, timeout=60, allow_redirects=False, **kwargs)
        except (requests.RequestException, OSError):
            raise RemoteError() from None

    def json(self, method, url, **kwargs):
        response = self.request(method, url, **kwargs)
        try:
            value = response.json()
        except (ValueError, TypeError):
            raise RemoteError(response.status_code) from None
        if not 200 <= response.status_code < 300 or 'error' in value:
            err = value.get('error', {})
            if not isinstance(err, dict):
                err = {}
            raise RemoteError(response.status_code, err.get('code'), err.get('error_subcode'))
        return value

def read_retry(http, url, *, sleep=time.sleep, **kwargs):
    for attempt in range(3):
        try:
            return http.json('GET', url, **kwargs)
        except RemoteError as error:
            if error.status not in (0, 429, 500, 502, 503, 504) or attempt == 2:
                raise
            sleep(2 ** attempt)
