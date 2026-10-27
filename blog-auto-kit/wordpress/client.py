"""mock와 설치형 WordPress에 같은 REST 요청을 보낸다."""
import base64
import json
from urllib.error import HTTPError
from urllib.parse import urlencode, urljoin, urlsplit
from urllib.request import Request, HTTPRedirectHandler, build_opener

MOCK_PASSWORD = 'abcd efgh ijkl mnop qrst uvwx'


class NoRedirect(HTTPRedirectHandler):
    def redirect_request(self, req, fp, code, msg, headers, newurl):
        return None


class WPError(ValueError):
    def __init__(self, body):
        self.body = body
        super().__init__('WordPress 요청 실패 → 주소·권한·애플리케이션 비밀번호를 확인하세요')


class Client:
    def __init__(self, base, username='mock-user', password=MOCK_PASSWORD, timeout=5,
                 destination='mock'):
        self.base = base.rstrip('/')
        self.destination = destination
        self.authorization = 'Basic ' + base64.b64encode(
            f'{username}:{password}'.encode('utf-8')).decode('ascii')
        self.timeout = timeout

    def request(self, method, route, data=None, headers=None):
        body = data if isinstance(data, bytes) else (
            json.dumps(data, ensure_ascii=False).encode('utf-8') if data is not None else None)
        values = {'Authorization': self.authorization, 'Content-Type': 'application/json'}
        values.update(headers or {})
        request = Request(self.base + '/wp-json/wp/v2/' + route, body, values, method=method)
        try:
            with build_opener(NoRedirect).open(request, timeout=self.timeout) as response:
                return json.load(response)
        except HTTPError as error:
            try:
                body = json.load(error)
            except ValueError:
                body = {'code': 'http_error', 'message': 'REST 응답 확인 필요',
                        'data': {'status': error.code}}
            raise WPError(body) from None

    def media_bytes(self, media_id):
        row = self.request('GET', f'media/{media_id}?context=edit')
        url = urljoin(self.base + '/', row['source_url'])
        origin, target = urlsplit(self.base), urlsplit(url)
        if (origin.scheme, origin.netloc) != (target.scheme, target.netloc):
            raise ValueError('외부 미디어 저장소 → 같은 서버의 원본 미디어로 연결하세요')
        request = Request(url, headers={'Authorization': self.authorization})
        try:
            with build_opener(NoRedirect).open(request, timeout=self.timeout) as response:
                return response.read()
        except HTTPError:
            raise ValueError('서버 사진 확인 실패 → 미디어를 다시 준비하세요') from None

    def find_slug(self, slug):
        query = urlencode({'slug': slug, 'status': 'draft,future,publish,pending,private',
                           'context': 'edit', 'per_page': 100})
        return self.request('GET', 'posts?' + query)

    def ensure_term(self, kind, name):
        rows = self.request('GET', kind + '?' + urlencode({'search': name, 'per_page': 100}))
        found = next((row for row in rows if row['name'] == name), None)
        if found:
            return found['id']
        try:
            return self.request('POST', kind, {'name': name})['id']
        except WPError as error:
            if error.body.get('code') == 'term_exists':
                return error.body['data']['term_id']
            raise

    def upload_media(self, data, filename, mime):
        return self.request('POST', 'media', data, {
            'Content-Type': mime,
            'Content-Disposition': 'attachment; filename="' + filename + '"'})
