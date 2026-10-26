import json
from urllib.error import HTTPError, URLError
import pytest
import publish
import render
import review
from common import save_json


@pytest.fixture
def output(tmp_path):
    draft = tmp_path / "input.md"
    draft.write_text("# 본인 관찰로 만든 생활 정보 글\n\n직접 적은 본문이에요.\n\n## 내 경험\n\n관찰한 일을 적었어요.\n\n## 다음 행동\n\n원문을 열어요.")
    out = render.render(draft, tmp_path / "output")
    path = out / "REVIEW.md"
    path.write_text(path.read_text().replace("- [ ]", "- [x]"))
    review.approve(out)
    return out


@pytest.fixture
def env_file(tmp_path, monkeypatch):
    for key in publish.ENV_KEYS:
        monkeypatch.delenv(key, raising=False)
    path = tmp_path / ".env"
    path.write_text("BLOGGER_BLOG_ID=123\nBLOGGER_ACCESS_TOKEN=SECRET_TOKEN\nWP_URL=https://owned.invalid-not-real.test\nWP_USER=writer\nWP_APP_PASSWORD=SECRET_PASSWORD\n")
    return path


def test_dry_run_never_reads_secrets_or_network(output, monkeypatch, capsys):
    def fail(*args, **kwargs):
        raise AssertionError("드라이런에서 인증/네트워크 접근")
    monkeypatch.setattr(publish, "settings", fail)
    monkeypatch.setattr(publish, "send", fail)
    for platform in ("blogger", "wordpress"):
        plan = publish.publish(output, platform)
        assert plan["mode"] == "dry-run" and plan["state"] == "draft"
        assert plan["authorization"] == "<REDACTED>"
        if platform == "blogger":
            assert "isDraft=true" in plan["endpoint"]
        else:
            assert plan["body"]["status"] == "draft"
    assert "SECRET" not in capsys.readouterr().out


@pytest.mark.parametrize("platform", ["naver", "tistory"])
def test_manual_platform(platform, output, monkeypatch):
    monkeypatch.setattr(publish, "settings", lambda *_: pytest.fail("인증 접근"))
    assert publish.publish(output, platform)["mode"] == "manual"
    with pytest.raises(ValueError, match="API 발행"):
        publish.publish(output, platform, live=True)


@pytest.mark.parametrize("platform", ["blogger", "wordpress"])
def test_mock_live_draft_and_no_repeat(platform, output, env_file, monkeypatch, capsys):
    calls = []
    def send(plan, authorization):
        calls.append((plan, authorization))
        return {"id": "999", "state": "draft", "mode": "live"}
    monkeypatch.setattr(publish, "send", send)
    result = publish.publish(output, platform, live=True, env_file=env_file)
    assert result["id"] == "999" and len(calls) == 1
    assert calls[0][0]["state"] == "draft"
    assert calls[0][1].startswith("Bearer " if platform == "blogger" else "Basic ")
    with pytest.raises(ValueError, match="시도 기록"):
        publish.publish(output, platform, live=True, env_file=env_file)
    assert len(calls) == 1
    logs = capsys.readouterr().out + (output / "LIVE_ATTEMPT.json").read_text()
    assert "SECRET" not in logs


def test_timeout_preserves_journal(output, env_file, monkeypatch):
    def fail(*args):
        raise ValueError("저장 상태를 확인하세요.")
    monkeypatch.setattr(publish, "send", fail)
    with pytest.raises(ValueError):
        publish.publish(output, "blogger", True, env_file)
    assert (output / "LIVE_ATTEMPT.json").is_file()
    with pytest.raises(ValueError, match="시도 기록"):
        publish.publish(output, "blogger", True, env_file)


def test_approval_required_and_stale_approval_blocked(output):
    (output / "editor.html").write_text("changed")
    with pytest.raises(ValueError, match="달라졌"):
        publish.publish(output, "blogger")
    (output / "APPROVED.json").unlink()
    with pytest.raises(ValueError, match="승인"):
        publish.publish(output, "blogger")


def test_missing_credentials_and_synthetic_refused(output, tmp_path, monkeypatch):
    for key in publish.ENV_KEYS:
        monkeypatch.delenv(key, raising=False)
    empty = tmp_path / ".env"
    empty.write_text("")
    with pytest.raises(ValueError, match="토큰"):
        publish.publish(output, "blogger", True, empty)
    from common import ROOT
    render.render(ROOT / "samples/article.md", output)
    path = output / "REVIEW.md"
    path.write_text(path.read_text().replace("- [ ]", "- [x]"))
    review.approve(output)
    with pytest.raises(ValueError, match="가상 연습용"):
        publish.publish(output, "blogger", True, empty)


@pytest.mark.parametrize("url", ["http://x.test", "https://u:p@x.test", "https://x.test?token=SECRET", "https://x.test#fragment", "https://x.test:8443", "https://name.wordpress.com", "https://wordpress.com", "https://x.test\n"])
def test_bad_wordpress_target(url):
    with pytest.raises(ValueError):
        publish.wordpress_base(url, live=True)


def test_env_precedence_and_token_file(env_file, tmp_path, monkeypatch):
    monkeypatch.setenv("BLOGGER_BLOG_ID", "456")
    values = publish.settings(env_file)
    assert values["BLOGGER_BLOG_ID"] == "456"
    token_file = tmp_path / "token.json"
    save_json(token_file, {"access_token": "FROM_FILE", "refresh_token": "NEVER_USED"})
    values["BLOGGER_TOKEN_FILE"] = str(token_file)
    assert publish.credentials("blogger", values) == "Bearer FROM_FILE"


class Response:
    def __init__(self, body, status=200):
        self.body, self.status = body, status
    def __enter__(self):
        return self
    def __exit__(self, *args):
        pass
    def read(self):
        return self.body


@pytest.mark.parametrize("platform, result", [("blogger", {"id": "42"}), ("wordpress", {"id": 42, "status": "draft"})])
def test_real_transport_mock_success(output, monkeypatch, platform, result):
    requests = []
    class Opener:
        def open(self, request, timeout):
            requests.append(request)
            return Response(json.dumps(result).encode())
    monkeypatch.setattr(publish, "build_opener", lambda *_: Opener())
    plan = publish.request_plan(output, platform)
    assert publish.send(plan, "Bearer SECRET")["id"] == "42"
    assert requests[0].method == "POST"
    assert requests[0].get_header("Authorization") == "Bearer SECRET"
    assert json.loads(requests[0].data)["title"] == plan["body"]["title"]


@pytest.mark.parametrize("response", [HTTPError("https://SECRET", 401, "SECRET", {}, None), HTTPError("https://SECRET", 302, "SECRET", {}, None), URLError("SECRET"), TimeoutError("SECRET"), Response(b"not JSON"), Response(b'{"id": "SECRET"}'), Response(b'{"id": 10, "status": "publish"}')])
def test_transport_failure_is_sanitized_no_retry(output, monkeypatch, response):
    calls = []
    class Opener:
        def open(self, *args, **kwargs):
            calls.append(1)
            if isinstance(response, Exception):
                raise response
            return response
    monkeypatch.setattr(publish, "build_opener", lambda *_: Opener())
    with pytest.raises(ValueError) as error:
        publish.send(publish.request_plan(output, "wordpress"), "Bearer SECRET")
    assert "SECRET" not in str(error.value) and len(calls) == 1


def test_redirects_disabled():
    assert publish.NoRedirect().redirect_request(None, None, 302, "", {}, "https://evil.test") is None


def test_local_image_live_blocked_before_journal(output, env_file):
    # 본인 글에 로컬 사진이 있을 때도 API 서버로 깨진 경로를 전송하지 않는다.
    source = output.parent / "local.md"
    (source.parent / "picture.svg").write_text('<svg xmlns="http://www.w3.org/2000/svg"/>')
    source.write_text("# 직접 쓴 글\n\n![내 사진](picture.svg)")
    render.render(source, output)
    path = output / "REVIEW.md"
    path.write_text(path.read_text().replace("- [ ]", "- [x]"))
    review.approve(output)
    with pytest.raises(ValueError, match="HTTPS"):
        publish.publish(output, "blogger", True, env_file)
    assert not (output / "LIVE_ATTEMPT.json").exists()


def test_live_requires_user_supplied_env_file(output, tmp_path, monkeypatch):
    monkeypatch.setenv("BLOGGER_ACCESS_TOKEN", "SECRET")
    monkeypatch.setenv("BLOGGER_BLOG_ID", "123")
    with pytest.raises(ValueError, match="직접 준비한 .env"):
        publish.publish(output, "blogger", True, tmp_path / "missing.env")
    assert not (output / "LIVE_ATTEMPT.json").exists()
