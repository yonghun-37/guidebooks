"""실제 인증 없이 본인 계정 확인과 토큰 비노출을 검증한다."""
import io
import json
from urllib.error import HTTPError, URLError
import warnings
from getpass import GetPassWarning

import pytest

import token_check


def test_private_prompt_and_read_only_request(monkeypatch, capsys):
    secret = "SECRET_TEST_SENTINEL"
    calls = []
    monkeypatch.setattr(token_check, "getpass", lambda prompt: secret)
    def response(request, timeout):
        calls.append(request)
        assert request.method == "GET" and request.data is None
        assert request.full_url == "https://graph.instagram.com/v26.0/me?fields=user_id,username"
        assert request.get_header("Authorization") == "Bearer " + secret
        assert timeout == 30
        return io.StringIO(json.dumps({"user_id": "123456", "username": "harin.demo", "access_token": secret}))
    monkeypatch.setattr(token_check, "urlopen", response)
    token_check.main()
    captured = capsys.readouterr()
    assert captured.out == "user_id: 123456\nusername: harin.demo\n"
    assert secret not in captured.out + captured.err
    assert len(calls) == 1


@pytest.mark.parametrize("response", ["not json SECRET_TEST_SENTINEL", "[]", "null", "{\"error\":\"SECRET_TEST_SENTINEL\"}",
                                    '{"user_id":"123", "username":"SECRET_TEST_SENTINEL\\nattack"}'])
def test_bad_response_never_echoes_body(response, monkeypatch):
    monkeypatch.setattr(token_check, "urlopen", lambda *a, **kw: io.StringIO(response))
    with pytest.raises(ValueError) as error:
        token_check.check("SECRET_TEST_SENTINEL")
    assert "SECRET_TEST_SENTINEL" not in str(error.value)


@pytest.mark.parametrize("error", [URLError("SECRET_TEST_SENTINEL"), TimeoutError("SECRET_TEST_SENTINEL"),
                                   HTTPError("https://example.invalid", 401, "SECRET_TEST_SENTINEL", {}, io.BytesIO(b"SECRET_TEST_SENTINEL"))])
def test_network_failures_do_not_echo_token_or_error_body(error, monkeypatch):
    def failed(*a, **kw):
        raise error
    monkeypatch.setattr(token_check, "urlopen", failed)
    with pytest.raises(ValueError) as caught:
        token_check.check("SECRET_TEST_SENTINEL")
    assert "SECRET_TEST_SENTINEL" not in str(caught.value)


@pytest.mark.parametrize("token", ["", " ", "secret\nattack", "secret\x00attack"])
def test_bad_tokens_are_rejected_before_network(token, monkeypatch):
    monkeypatch.setattr(token_check, "urlopen", lambda *a, **kw: pytest.fail("잘못된 토큰으로 요청"))
    with pytest.raises(ValueError):
        token_check.check(token)


def test_no_echo_fallback_and_cancelled_prompt(monkeypatch):
    def fallback(prompt):
        warnings.warn("unsafe fallback", GetPassWarning)
        pytest.fail("숨김 입력 실패 후 읽기를 계속함")
    monkeypatch.setattr(token_check, "getpass", fallback)
    with pytest.raises(ValueError, match="숨김"):
        token_check.main()
    monkeypatch.setattr(token_check, "getpass", lambda prompt: (_ for _ in ()).throw(EOFError()))
    with pytest.raises(ValueError, match="취소"):
        token_check.main()


def test_cross_host_redirect_is_never_followed():
    assert token_check.NoRedirect().redirect_request(None, None, 302, "", {}, "https://other.invalid") is None
