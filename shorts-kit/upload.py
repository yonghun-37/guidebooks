"""승인된 파일만 YouTube Data API v3로 보낸다. 기본값은 네트워크 없는 드라이런."""
import argparse
import hashlib
import json
from pathlib import Path
import re
import time
from urllib.parse import urlsplit

from common import ROOT, cli, digest, read_json, save_json
from render import probe
from review import require_approval
from write_script import validate

SCOPE = "https://www.googleapis.com/auth/youtube.upload"
ENDPOINT = "https://www.googleapis.com/upload/youtube/v3/videos?uploadType=resumable&part=snippet%2Cstatus"
CHUNK = 1024 * 1024  # 256 KiB 배수. 마지막 청크는 더 작을 수 있다.
QUOTA = "2026년 10월 조사 기준: videos.insert 업로드 버킷 1 unit/호출, 기본 100호출/일. 다른 엔드포인트는 별도입니다. 내 Cloud 할당량을 확인하세요. [Y037] [Y038] [Y088]"
LOCK = "공식 insert 문서는 미검증 프로젝트의 비공개 제한이 없다고 하나, 한국어 비공개 잠금 도움말은 제한을 설명해요. 먼저 private로 보내고 Studio의 실제 상태·제한을 확인하세요. 잠금은 public 변경만으로 해결되지 않아요. API 감사와 OAuth 앱 검증은 다른 절차예요. [Y037] [Y086] [Y040] [Y041]"


def private_json(path, value):
    # 토큰·세션은 임시 파일 단계부터 사용자만 읽을 수 있게 저장한다.
    import os
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_name(path.name + ".tmp")
    descriptor = os.open(temporary, os.O_WRONLY | os.O_CREAT | os.O_TRUNC, 0o600)
    with os.fdopen(descriptor, "w", encoding="utf-8") as stream:
        stream.write(json.dumps(value, ensure_ascii=False, indent=2) + "\n")
    temporary.chmod(0o600)
    temporary.replace(path)


def metadata(script):
    validate(script)
    for key in ("selfDeclaredMadeForKids", "containsSyntheticMedia"):
        if type(script.get(key)) is not bool:
            raise ValueError(f"{key}를 직접 판단해 true/false로 정하고 다시 검수하세요. [Y013] [Y014]")
    return {"snippet": {"title": script["title"], "description": script["description"] + "\n" + " ".join(script["hashtags"]), "categoryId": "22", "defaultLanguage": "ko"},
            "status": {key: script[key] for key in ("privacyStatus", "selfDeclaredMadeForKids", "containsSyntheticMedia")}}


def plan(output, body):
    size = (Path(output) / "short.mp4").stat().st_size
    return {"mode": "dry-run", "network_calls": 0, "metadata": body,
            "requests": [
                {"method": "POST", "url": ENDPOINT, "headers": {"Authorization": "Bearer <사용자 OAuth 토큰>", "Content-Type": "application/json; charset=UTF-8", "X-Upload-Content-Type": "video/mp4", "X-Upload-Content-Length": str(size)}, "body": body, "response": "Location: <개인 업로드 세션 주소>"},
                {"method": "PUT", "url": "<Location>", "headers": {"Content-Type": "video/mp4", "Content-Length": str(min(size, CHUNK)), "Content-Range": f"bytes 0-{min(size, CHUNK) - 1}/{size}"}, "body": "승인된 short.mp4의 청크. 308의 Range 다음부터 반복, 마지막 200/201의 id/status 저장"},
                {"when": "중단 후 재실행 또는 일시적 오류", "method": "PUT", "url": "<같은 Location>", "headers": {"Content-Length": "0", "Content-Range": f"bytes */{size}"}, "body": "없음. 서버 Range를 읽고 남은 청크만 전송"}],
            "fields": {"privacyStatus": "명시한 공개 범위. 키트 기본 private [Y037]", "selfDeclaredMadeForKids": "의도한 시청자·주제·표현을 직접 판단 [Y014] [Y037]", "containsSyntheticMedia": "사실적 합성 등 공개 요건을 직접 판단. 대본·자막 보조만 사용한 경우와 구분 [Y013] [Y037]", "shorts": "isShorts는 보내지 않음. 파일 비율·길이로 분류 [Y001]"},
            "quota": QUOTA, "private_lock": LOCK, "after_upload": "API 완료와 공개·쇼츠 분류·권리 검토 완료는 다릅니다. Studio에서 처리·Shorts·제한사항·공개 상태를 직접 확인하세요. [Y032]"}


def valid_session(url):
    parsed = urlsplit(url)
    if parsed.scheme != "https" or parsed.hostname not in ("www.googleapis.com", "youtube.googleapis.com") or parsed.port not in (None, 443) or parsed.username or parsed.password or parsed.fragment or not parsed.path.startswith("/upload/youtube/v3/videos"):
        raise ValueError("업로드 세션 주소가 올바르지 않습니다. 개인 세션 파일을 외부에 공유하지 마세요.")
    return url


def resumable(output, body, session, sleep=time.sleep):
    """네트워크 객체를 주입해 프로토콜을 실제 전송 없이 검증한다."""
    output = Path(output)
    media = output / "short.mp4"
    size = media.stat().st_size
    identity = {"sha256": digest(media), "metadata_sha256": hashlib.sha256(json.dumps(body, sort_keys=True).encode()).hexdigest(), "size": size}
    state_path = output / "upload-session.json"
    def request(method, url, **kwargs):
        try:
            return session.request(method, url, timeout=60, allow_redirects=False, **kwargs)
        except OSError:
            return None  # 실제 응답/인증/세션 URL을 로그로 노출하지 않는다.
    if state_path.exists():
        state = read_json(state_path)
        if state["identity"] != identity:
            raise ValueError("재개 대상 영상·메타데이터가 달라졌습니다. 원래 파일로 재개하거나 새 폴더를 쓰세요.")
        if state.get("result"):
            return state["result"]
        uri = valid_session(state["uri"])
        query = True
    else:
        if (output / "upload-result.json").exists():
            raise ValueError("완료 기록이 있습니다. 중복 업로드하지 않았습니다.")
        response = request("POST", ENDPOINT, json=body, headers={"X-Upload-Content-Type": "video/mp4", "X-Upload-Content-Length": str(size)})
        if response is None or response.status_code not in (200, 201) or not response.headers.get("Location"):
            raise ValueError("업로드 세션 시작 실패. 계정·API 활성화·할당량을 확인하세요. 인증 값은 출력하지 않습니다.")
        uri = valid_session(response.headers["Location"])
        state = {"identity": identity, "uri": uri, "offset": 0}
        private_json(state_path, state)
        query = False
    offset, failures, stalls = 0, 0, 0
    with media.open("rb") as stream:
        while True:
            if query:
                response = request("PUT", uri, data=b"", headers={"Content-Length": "0", "Content-Range": f"bytes */{size}"})
            else:
                stream.seek(offset)
                block = stream.read(CHUNK)
                if not block:
                    raise ValueError("서버 완료 응답이 없습니다. 같은 폴더로 다시 실행해 상태를 조회하세요.")
                response = request("PUT", uri, data=block, headers={"Content-Type": "video/mp4", "Content-Length": str(len(block)), "Content-Range": f"bytes {offset}-{offset + len(block) - 1}/{size}"})
            if response is None or response.status_code in (429, 500, 502, 503, 504):
                failures += 1
                if failures > 4:
                    raise ValueError("일시적 업로드 오류가 계속됩니다. 같은 폴더로 재실행하면 서버 위치부터 재개해요.")
                sleep(min(2 ** failures, 16))
                query = True
                continue
            if response.status_code in (200, 201):
                try:
                    data = response.json()
                    video_id = data["id"]
                    if not isinstance(video_id, str) or not re.fullmatch(r"[A-Za-z0-9_-]+", video_id):
                        raise ValueError("잘못된 영상 ID")
                    result = {"id": video_id, "url": "https://www.youtube.com/watch?v=" + video_id, "status": data.get("status", {}), "requested_status": body["status"], "note": "전송 완료. Studio에서 처리·공개 상태·쇼츠 분류·제한사항을 확인하세요. [Y032]"}
                except (ValueError, KeyError, TypeError):
                    raise ValueError("완료 응답을 읽지 못했습니다. 같은 폴더로 상태를 조회하고 Studio에서도 확인하세요.") from None
                state["result"] = result
                private_json(state_path, state)
                private_json(output / "upload-result.json", result)
                return result
            if response.status_code == 308:
                match = re.fullmatch(r"bytes=0-(\d+)", response.headers.get("Range", ""))
                if response.headers.get("Range") and not match:
                    raise ValueError("서버 Range 응답이 올바르지 않습니다. 상태를 확인하세요.")
                next_offset = int(match[1]) + 1 if match else 0
                if not 0 <= next_offset <= size:
                    raise ValueError("서버 재개 위치가 파일 크기를 넘습니다.")
                stalls = stalls + 1 if next_offset == offset else 0
                if stalls > 4:
                    raise ValueError("업로드 진행이 멈췄습니다. 네트워크 확인 후 같은 폴더로 재실행하세요.")
                offset = next_offset
                state["offset"] = offset
                private_json(state_path, state)
                query = offset == size
                continue
            if response.status_code in (404, 410):
                raise ValueError("업로드 세션이 만료됐습니다. Studio에서 중복 영상 여부를 확인한 뒤 새 폴더에서 시작하세요.")
            raise ValueError(f"업로드 실패 HTTP {response.status_code}. 권한·할당량·파일 조건을 확인하세요. 같은 폴더의 세션은 보존했어요.")


def authorized_session(client_path, token_path):
    if not Path(client_path).is_file() or not Path(token_path).is_file():
        raise ValueError("--live에는 사용자 client_secret.json과 token.json이 모두 필요합니다. README의 OAuth 준비를 따라 하세요.")
    try:
        client, token = read_json(client_path)["installed"], read_json(token_path)
        if client["client_id"] != token["client_id"] or client["client_secret"] != token["client_secret"] or token["token_uri"] != "https://oauth2.googleapis.com/token":
            raise ValueError("OAuth 파일 불일치")
        scopes = token.get("scopes", [])
        scopes = scopes.split() if isinstance(scopes, str) else scopes
        if SCOPE not in scopes:
            raise ValueError("업로드 권한 없음")
    except (ValueError, OSError, KeyError, TypeError):
        raise ValueError("OAuth 파일·권한·만료 상태를 확인하세요. [Y042]") from None
    try:
        from google.oauth2.credentials import Credentials
        from google.auth.transport.requests import AuthorizedSession, Request
    except ImportError:
        raise ValueError("선택 설치: python -m pip install -r requirements-live.txt") from None
    try:
        credentials = Credentials.from_authorized_user_info(token, scopes=[SCOPE])
        if not credentials.valid:
            credentials.refresh(Request())
            private_json(token_path, json.loads(credentials.to_json()))
        return AuthorizedSession(credentials)
    except Exception:
        raise ValueError("OAuth 파일·권한·만료 상태를 확인하세요. 본인 테스트 사용자로 인증을 다시 준비하세요. [Y042]") from None


def upload(output, live=False, client_path=None, token_path=None):
    output = Path(output).resolve()
    require_approval(output)
    body = metadata(read_json(output / "script.json"))
    info = probe(output / "short.mp4")
    if info["size"] != [1080, 1920] or info["fps"] != 30 or info["video_codec"] != "h264" or info["audio_codec"] != "aac" or not 0 < info["duration"] <= 180:
        raise ValueError("영상 규격을 다시 확인하세요. 최대 3분입니다. [Y001]")
    if not live:
        value = plan(output, body)
        save_json(output / "dry-run.json", value)
        print(json.dumps(value, ensure_ascii=False, indent=2))
        return value
    session = authorized_session(client_path or ROOT / "private" / "client_secret.json", token_path or ROOT / "private" / "token.json")
    try:
        from google.auth.exceptions import GoogleAuthError
        try:
            result = resumable(output, body, session)
        except GoogleAuthError:
            raise ValueError("업로드 중 OAuth 인증이 만료됐습니다. 본인 테스트 계정으로 다시 인증하세요. [Y042]") from None
    finally:
        session.close()
    print(json.dumps(result, ensure_ascii=False, indent=2))
    print(LOCK)
    return result


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("output", type=Path)
    parser.add_argument("--live", action="store_true")
    parser.add_argument("--client-secret", type=Path)
    parser.add_argument("--token", type=Path)
    args = parser.parse_args()
    upload(args.output, args.live, args.client_secret, args.token)


if __name__ == "__main__":
    cli(main)
