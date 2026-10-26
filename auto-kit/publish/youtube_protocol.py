"""shorts-kit/upload.py에서 재사용한 재개 프로토콜. 세션은 private 상태에 둔다."""
import hashlib
import json
from pathlib import Path
import re
import time
from urllib.parse import urlsplit
from common import digest, read_json
from transport import Uncertain
ENDPOINT = "https://www.googleapis.com/upload/youtube/v3/videos?uploadType=resumable&part=snippet%2Cstatus"
CHUNK = 1024 * 1024
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
        if not state.get("uri"):
            raise Uncertain("업로드 세션 시작 결과 불명. 새 insert 없이 Studio에서 확인하세요.")
        uri = valid_session(state["uri"])
        query = True
    else:
        if (output / "upload-result.json").exists():
            raise ValueError("완료 기록이 있습니다. 중복 업로드하지 않았습니다.")
        private_json(state_path, {"identity": identity, "phase": "starting"})
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
