"""Phase 7w: 실제 네트워크 없이 URL/설정/승인/부분 실패 계약 검증."""
import io
import json
from pathlib import Path
from urllib.error import HTTPError, URLError

import pytest

from common import digest, read_json, save_json
import publish
import prepare_hosting


@pytest.fixture
def approved(tmp_path):
    output = tmp_path / "reviewed"
    output.mkdir()
    save_json(output / "copy.json", {"scenes": [{}, {}], "caption": "검수된 문안", "is_ai_generated": True, "synthetic": False})
    (output / "cards").mkdir()
    for name in ["cards/card-01.jpg", "cards/card-02.jpg", "reel.mp4"]:
        (output / name).write_bytes(b"approved media")
    # 승인에 없는 파일은 공개 폴더에서 제외되어야 한다.
    (output / ".env").write_text("PRIVATE_TEST_VALUE")
    (output / "cards/extra.jpg").write_bytes(b"unreviewed")
    save_json(output / "APPROVED.json", {"files": {str(p.relative_to(output)): digest(p) for p in output.rglob("*") if p.is_file() and p.name != ".env" and p.name != "extra.jpg"}})
    return output


@pytest.fixture(autouse=True)
def isolated_settings(tmp_path, monkeypatch):
    monkeypatch.setattr(publish, "ROOT", tmp_path)
    for key in ("IG_ACCESS_TOKEN", "IG_USER_ID", "IG_API_VERSION"):
        monkeypatch.delenv(key, raising=False)


def test_hosting_only_approved_media(approved, tmp_path, capsys):
    destination = tmp_path / "public"
    names = prepare_hosting.prepare(approved, destination)
    assert sorted(str(p.relative_to(destination)) for p in destination.rglob("*") if p.is_file()) == sorted(names)
    for name in names:
        assert digest(destination / name) == digest(approved / name)
    text = capsys.readouterr().out
    assert "PRIVATE_TEST_VALUE" not in text
    assert "Upload files" in text and "--base-url" in text and "/cards/card-01.jpg" in text
    with pytest.raises(FileExistsError):
        prepare_hosting.prepare(approved, destination)
    with pytest.raises(ValueError, match="바깥"):
        prepare_hosting.prepare(approved, approved / "public")


def test_hosting_rejects_changed_and_oversize(approved, tmp_path):
    path = approved / "reel.mp4"
    path.write_bytes(b"changed")
    with pytest.raises(ValueError, match="검수 대상"):
        prepare_hosting.prepare(approved, tmp_path / "changed")
    with path.open("wb") as file:
        file.truncate(25 * 1024 * 1024 + 1)
    approval = read_json(approved / "APPROVED.json")
    approval["files"]["reel.mp4"] = digest(path)
    save_json(approved / "APPROVED.json", approval)
    with pytest.raises(ValueError, match="25MiB"):
        prepare_hosting.prepare(approved, tmp_path / "large")
    assert not (tmp_path / "large").exists()


def test_env_precedence_version_and_secret_redaction(approved, tmp_path, monkeypatch, capsys):
    (tmp_path / ".env").write_text('IG_ACCESS_TOKEN="SECRET_SENTINEL"\nIG_USER_ID=123\nIG_API_VERSION=v27.0\n')
    monkeypatch.setenv("IG_API_VERSION", "v26.0")
    plan = publish.publish(approved)
    assert all("/v26.0/" in step["endpoint"] for step in plan["requests"])
    assert "SECRET_SENTINEL" not in capsys.readouterr().out
    monkeypatch.delenv("IG_API_VERSION")
    assert publish.settings()["IG_API_VERSION"] == "v27.0"
    (tmp_path / ".env").write_text("UNKNOWN=secret\n")
    with pytest.raises(ValueError, match="값은 출력하지"):
        publish.settings()


def test_api_request_url_headers_and_errors(monkeypatch):
    captured = []
    def fake(request, timeout):
        captured.append(request)
        return io.StringIO('{"id":"123"}')
    monkeypatch.setattr(publish, "urlopen", fake)
    assert publish.api_request("POST", "https://graph.instagram.com/v26.0/1/media", {"caption": "한글"}, "SECRET") == {"id": "123"}
    assert captured[-1].get_header("Authorization") == "Bearer SECRET"
    assert b"caption=" in captured[-1].data
    publish.api_request("GET", "https://graph.instagram.com/v26.0/2", {"fields": "status_code"}, "SECRET")
    assert captured[-1].data is None and captured[-1].full_url.endswith("?fields=status_code")
    for error in (HTTPError("url", 401, "SECRET", {}, None), URLError("SECRET"), TimeoutError("SECRET")):
        def fail(*args, **kwargs):
            raise error
        monkeypatch.setattr(publish, "urlopen", fail)
        with pytest.raises(ValueError) as caught:
            publish.api_request("GET", "https://graph.instagram.com/", {}, "SECRET")
        assert "SECRET" not in str(caught.value)
    for body in ('bad json', '{"error":{"message":"SECRET"}}'):
        monkeypatch.setattr(publish, "urlopen", lambda *a, **k: io.StringIO(body))
        with pytest.raises(ValueError) as caught:
            publish.api_request("GET", "https://graph.instagram.com/", {}, "SECRET")
        assert "SECRET" not in str(caught.value)


def test_mocked_live_polling_two_posts_and_no_retry(approved, monkeypatch):
    monkeypatch.setenv("IG_ACCESS_TOKEN", "SECRET")
    monkeypatch.setenv("IG_USER_ID", "123")
    calls, sleeps = [], []
    def fake(method, endpoint, params, token):
        calls.append((method, endpoint, params))
        assert token == "SECRET" and "{" not in endpoint
        if method == "GET":
            return {"status_code": "IN_PROGRESS" if len(calls) == 2 else "FINISHED"}
        return {"id": str(100 + len(calls))}
    monkeypatch.setattr(publish, "api_request", fake)
    monkeypatch.setattr(publish.time, "sleep", sleeps.append)
    result = publish.publish(approved, live=True, public_base_url="https://test.example/lesson")
    assert result["mode"] == "live" and sleeps == [60]
    assert len([c for c in calls if c[1].endswith("/media_publish")]) == 2
    assert calls[0][2]["image_url"] == "https://test.example/lesson/cards/card-01.jpg"
    assert next(c for c in calls if "video_url" in c[2])[2]["video_url"] == "https://test.example/lesson/reel.mp4"
    assert read_json(approved / "LIVE_ATTEMPT.json")["status"] == "finished"
    assert "SECRET" not in (approved / "LIVE_ATTEMPT.json").read_text()
    before = len(calls)
    with pytest.raises(FileExistsError):
        publish.publish(approved, live=True, public_base_url="https://test.example/lesson")
    assert len(calls) == before


@pytest.mark.parametrize("state", ["ERROR", "EXPIRED", "IN_PROGRESS", "network"])
def test_partial_failure_keeps_journal(approved, monkeypatch, state):
    count = 0
    def fake(method, *args):
        nonlocal count
        count += 1
        if method == "POST":
            return {"id": "123"}
        if state == "network":
            raise ValueError("응답 유실")
        return {"status_code": state}
    monkeypatch.setattr(publish, "api_request", fake)
    monkeypatch.setattr(publish.time, "sleep", lambda _: None)
    with pytest.raises(ValueError):
        publish.execute_live(approved, publish.request_plan(approved), "SECRET")
    assert (approved / "LIVE_ATTEMPT.json").exists()
    assert count == (6 if state == "IN_PROGRESS" else 2)


def test_live_guards_before_network(approved, monkeypatch):
    with pytest.raises(ValueError, match="IG_ACCESS_TOKEN"):
        publish.publish(approved, live=True, public_base_url="https://test.example")
    monkeypatch.setenv("IG_ACCESS_TOKEN", "SECRET")
    monkeypatch.setenv("IG_USER_ID", "123")
    for url in ("http://test.example", "https://u:p@test.example", "https://test.example/?token=x", "https://example.invalid"):
        with pytest.raises(ValueError, match="HTTPS"):
            publish.publish(approved, live=True, public_base_url=url)
    # Re-sign only the test fixture to exercise the synthetic guard.
    copy = read_json(approved / "copy.json")
    copy["synthetic"] = True
    save_json(approved / "copy.json", copy)
    approval = read_json(approved / "APPROVED.json")
    approval["files"]["copy.json"] = digest(approved / "copy.json")
    save_json(approved / "APPROVED.json", approval)
    with pytest.raises(ValueError, match="합성"):
        publish.publish(approved, live=True, public_base_url="https://test.example")
    assert not (approved / "LIVE_ATTEMPT.json").exists()


@pytest.mark.parametrize("flag", ["--base-url", "--public-base-url"])
def test_cli_url_alias_dryrun(approved, monkeypatch, capsys, flag):
    monkeypatch.setattr("sys.argv", ["publish.py", str(approved), flag, "https://test.example/lesson"])
    publish.main()
    assert "https://test.example/lesson/cards/card-01.jpg" in capsys.readouterr().out
