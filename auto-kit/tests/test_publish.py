from pathlib import Path
import pytest
from common import load_config, read_json
from publish.instagram import Instagram, request_plan
from publish.youtube import metadata, resumable
from transport import Deferred, Uncertain, RemoteError

class Response:
    def __init__(self, status=200, data=None, headers=None):
        self.status_code, self.data, self.headers = status, data or {}, headers or {}
    def json(self): return self.data

class FakeHTTP:
    def __init__(self, values): self.values, self.calls = list(values), []
    def json(self, method, url, **kwargs):
        self.calls.append((method, url, kwargs))
        value = self.values.pop(0)
        if isinstance(value, Exception): raise value
        return value

def quota(used=0, total=10):
    return {'data': [{'quota_usage': used, 'config': {'quota_total': total, 'quota_duration': 86400}}]}

def test_instagram_poll_and_parent_only(tmp_path):
    http = FakeHTTP([quota(), {'id': '1'}, {'status_code': 'IN_PROGRESS'}, {'status_code': 'FINISHED'}, {'id': '2'}, {'status_code': 'FINISHED'}, {'id': '3'}, {'status_code': 'FINISHED'}, quota(), {'id': '99'}])
    ig = Instagram(http, token='secret', account='123', sleep=lambda _: None)
    result = ig.publish(['https://example.org/a.jpg', 'https://example.org/b.jpg'], {'caption': '문안', 'is_ai_generated': True}, tmp_path / 'ig.json')
    assert result['id'] == '99'
    assert len([c for c in http.calls if c[1].endswith('/media_publish')]) == 1
    creates = [c[2]['data'] for c in http.calls if c[0] == 'POST' and c[1].endswith('/media')]
    assert 'is_ai_generated' not in creates[0]
    assert creates[-1]['is_ai_generated'] == 'true'
    assert 'secret' not in (tmp_path / 'ig.json').read_text()

def test_instagram_limit_fail_closed(tmp_path):
    for value in [quota(10), {}, RemoteError(403)]:
        ig = Instagram(FakeHTTP([value]), token='secret', account='123', sleep=lambda _: None)
        with pytest.raises(Deferred):
            ig.publish(['https://example.org/a.jpg'], {'caption': '문안', 'is_ai_generated': True}, tmp_path / 'ig.json')

def test_instagram_unknown_publish_no_repost(tmp_path):
    http = FakeHTTP([quota(), {'id': '1'}, {'status_code': 'FINISHED'}, quota(), RemoteError()])
    ig = Instagram(http, token='secret', account='123', sleep=lambda _: None)
    with pytest.raises(Uncertain):
        ig.publish(['https://example.org/a.jpg'], {'caption': '문안', 'is_ai_generated': True}, tmp_path / 'ig.json')
    ig.http = FakeHTTP([{'status_code': 'PUBLISHED'}])
    with pytest.raises(Uncertain):
        ig.publish(['https://example.org/a.jpg'], {'caption': '문안', 'is_ai_generated': True}, tmp_path / 'ig.json')
    assert all(c[0] == 'GET' for c in ig.http.calls)

def test_youtube_status_and_dry_plan():
    cfg = load_config()['youtube']
    body = metadata({'title': '가상', 'caption': '설명'}, cfg)
    assert body['status']['privacyStatus'] == 'private'
    assert body['status']['containsSyntheticMedia'] is True
    assert 'isShorts' not in body['status']
    cfg['publishAt'] = '2000-01-01T00:00:00Z'
    with pytest.raises(ValueError): metadata({'title': '가상', 'caption': '설명'}, cfg)

def test_youtube_308_and_saved_session(tmp_path):
    (tmp_path / 'short.mp4').write_bytes(b'x' * (1024 * 1024 + 19))
    class Session:
        def __init__(self): self.calls = []; self.responses = [Response(headers={'Location': 'https://www.googleapis.com/upload/youtube/v3/videos?upload_id=fake'}), Response(308, headers={'Range': 'bytes=0-1048575'}), Response(201, {'id': 'abc_123', 'status': {'privacyStatus': 'private'}})]
        def request(self, method, url, **kwargs): self.calls.append((method, kwargs)); return self.responses.pop(0)
    session = Session()
    result = resumable(tmp_path, {'status': {'privacyStatus': 'private'}}, session, sleep=lambda _: None)
    assert result['id'] == 'abc_123'
    assert session.calls[-1][1]['headers']['Content-Range'] == 'bytes 1048576-1048594/1048595'
    assert resumable(tmp_path, {'status': {'privacyStatus': 'private'}}, session)['id'] == 'abc_123'
    assert len(session.calls) == 3

def test_instagram_error_poll(tmp_path):
    http = FakeHTTP([quota(), {'id': '1'}, {'status_code': 'ERROR'}])
    with pytest.raises(ValueError):
        Instagram(http, token='x', account='123').publish(['https://example.org/a.jpg'], {'caption': '문안', 'is_ai_generated': False}, tmp_path / 'ig.json')
