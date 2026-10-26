import pytest
from common import read_json, save_json
import upload

URI = "https://www.googleapis.com/upload/youtube/v3/videos?upload_id=mock"
BODY = {"snippet": {"title": "예제"}, "status": {"privacyStatus": "private", "selfDeclaredMadeForKids": False, "containsSyntheticMedia": True}}

class Response:
    def __init__(self, code, headers=None, value=None):
        self.status_code, self.headers, self.value = code, headers or {}, value
    def json(self):
        return self.value

class Session:
    def __init__(self, responses):
        self.responses = iter(responses)
        self.calls = []
    def request(self, method, url, **kwargs):
        self.calls.append((method, url, kwargs))
        response = next(self.responses)
        if isinstance(response, Exception):
            raise response
        return response

def started():
    return Response(200, {"Location": URI})

def done():
    return Response(201, value={"id": "mock-video", "status": {"privacyStatus": "private"}})

@pytest.fixture
def media(tmp_path, monkeypatch):
    (tmp_path / "short.mp4").write_bytes(b"abcdefghijkl")
    monkeypatch.setattr(upload, "CHUNK", 4)
    return tmp_path

def test_chunk_sequence_and_idempotent_completion(media):
    session = Session([started(), Response(308, {"Range": "bytes=0-3"}), Response(308, {"Range": "bytes=0-7"}), done()])
    result = upload.resumable(media, BODY, session)
    assert result["id"] == "mock-video"
    assert [call[2].get("headers", {}).get("Content-Range") for call in session.calls] == [None, "bytes 0-3/12", "bytes 4-7/12", "bytes 8-11/12"]
    assert b"".join(c[2]["data"] for c in session.calls[1:]) == b"abcdefghijkl"
    assert all(call[2]["allow_redirects"] is False for call in session.calls)
    again = Session([])
    assert upload.resumable(media, BODY, again) == result and not again.calls

def test_network_failure_queries_server_received_bytes(media):
    session = Session([started(), OSError("secret-session-url"), Response(308, {"Range": "bytes=0-3"}), Response(308, {"Range": "bytes=0-7"}), done()])
    waits = []
    upload.resumable(media, BODY, session, sleep=waits.append)
    assert session.calls[2][2]["headers"]["Content-Range"] == "bytes */12"
    assert session.calls[3][2]["data"] == b"efgh" and waits == [2]

def test_cross_process_resume_uses_server_not_cached_offset(media):
    first = Session([started(), Response(308, {"Range": "bytes=0-3"}), Response(403)])
    with pytest.raises(ValueError, match="HTTP 403"):
        upload.resumable(media, BODY, first)
    assert read_json(media / "upload-session.json")["offset"] == 4
    second = Session([Response(308, {"Range": "bytes=0-7"}), done()])
    upload.resumable(media, BODY, second)
    assert second.calls[0][0] == "PUT" and second.calls[0][2]["data"] == b""
    assert second.calls[1][2]["data"] == b"ijkl"

def test_lost_final_response_recovered_by_query(media):
    session = Session([started(), Response(503), done()])
    assert upload.resumable(media, BODY, session, sleep=lambda _: None)["id"] == "mock-video"
    assert session.calls[-1][2]["headers"]["Content-Range"] == "bytes */12"

def test_changed_media_cannot_resume(media):
    with pytest.raises(ValueError):
        upload.resumable(media, BODY, Session([started(), Response(403)]))
    (media / "short.mp4").write_bytes(b"different")
    with pytest.raises(ValueError, match="달라졌"):
        upload.resumable(media, BODY, Session([]))

def test_retries_are_bounded_and_sanitized(media):
    session = Session([started(), *[OSError("SECRET") for _ in range(5)]])
    with pytest.raises(ValueError, match="일시적") as error:
        upload.resumable(media, BODY, session, sleep=lambda _: None)
    assert "SECRET" not in str(error.value) and (media / "upload-session.json").exists()

def test_expired_session_does_not_start_duplicate(media):
    with pytest.raises(ValueError, match="만료"):
        upload.resumable(media, BODY, Session([started(), Response(410)]))

@pytest.mark.parametrize("response", [Response(308, {"Range": "bad"}), Response(308, {"Range": "bytes=0-999"}), Response(201, value={}), Response(302, {"Location": "https://example.invalid"})])
def test_malformed_or_redirect_response(media, response):
    with pytest.raises(ValueError):
        upload.resumable(media, BODY, Session([started(), response]))

def test_stalled_progress_stops(media):
    with pytest.raises(ValueError, match="진행이 멈췄"):
        upload.resumable(media, BODY, Session([started(), *[Response(308) for _ in range(5)]]))

@pytest.mark.parametrize("uri", ["http://www.googleapis.com/upload/youtube/v3/videos", "https://evil.example/upload/youtube/v3/videos", "https://www.googleapis.com@evil.example/upload/youtube/v3/videos", "https://www.googleapis.com:444/upload/youtube/v3/videos"])
def test_session_destination_validation(uri):
    with pytest.raises(ValueError):
        upload.valid_session(uri)

def test_oauth_files_must_match(tmp_path):
    client, token = tmp_path / "client.json", tmp_path / "token.json"
    save_json(client, {"installed": {"client_id": "one", "client_secret": "placeholder"}})
    save_json(token, {"client_id": "other", "client_secret": "placeholder", "token_uri": "https://oauth2.googleapis.com/token"})
    with pytest.raises(ValueError, match="OAuth 파일") as error:
        upload.authorized_session(client, token)
    assert "placeholder" not in str(error.value)
