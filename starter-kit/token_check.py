"""토큰을 숨겨 입력받아 본인 Instagram 계정 ID·이름만 읽는다. 게시하지 않는다."""
from getpass import GetPassWarning, getpass
import json
import re
from urllib.error import HTTPError, URLError
from urllib.request import HTTPRedirectHandler, Request, build_opener
import warnings

from common import cli


class NoRedirect(HTTPRedirectHandler):
    def redirect_request(self, req, fp, code, msg, headers, newurl):
        return None


# 인증 헤더를 다른 주소로 넘기는 리다이렉트를 따르지 않는다.
urlopen = build_opener(NoRedirect()).open


def check(token):
    if not token or any(ord(char) <= 32 or ord(char) >= 127 for char in token):
        raise ValueError("토큰을 공백·줄바꿈 없이 입력하세요. 값은 출력하지 않습니다.")
    request = Request("https://graph.instagram.com/v26.0/me?fields=user_id,username",
                      headers={"Authorization": "Bearer " + token}, method="GET")
    try:
        with urlopen(request, timeout=30) as response:
            result = json.load(response)
    except HTTPError as error:
        raise ValueError(f"계정 확인 HTTP {error.code}. 토큰·권한을 앱 대시보드에서 확인하세요.") from None
    except (URLError, OSError, json.JSONDecodeError, UnicodeError):
        raise ValueError("계정 확인 응답을 읽지 못했습니다. 연결과 앱 대시보드를 확인하세요.") from None
    if not isinstance(result, dict):
        raise ValueError("계정 확인 응답 형식이 잘못되었습니다. 앱 대시보드를 확인하세요.")
    user_id, username = str(result.get("user_id", "")), result.get("username", "")
    if ("error" in result or not re.fullmatch(r"[0-9]+", user_id) or not isinstance(username, str)
            or not re.fullmatch(r"[A-Za-z0-9_.]+", username) or token in user_id or token in username):
        raise ValueError("계정 ID·이름을 확인하지 못했습니다. 토큰·권한을 앱 대시보드에서 확인하세요.")
    return {"user_id": user_id, "username": username}


def main():
    try:
        with warnings.catch_warnings():
            warnings.simplefilter("error", GetPassWarning)
            token = getpass("Instagram 토큰 (화면에 표시되지 않음): ")
    except GetPassWarning:
        raise ValueError("숨김 입력을 지원하는 로컬 터미널에서 다시 실행하세요.") from None
    except (EOFError, KeyboardInterrupt):
        raise ValueError("토큰 입력을 취소했습니다.") from None
    result = check(token)
    print(f"user_id: {result['user_id']}\nusername: {result['username']}")


if __name__ == "__main__":
    cli(main)
