"""Instagram Login 게시 예제. 기본은 네트워크 없는 드라이런이다."""
import argparse
import json
import os
from pathlib import Path
import re
import time
from urllib.error import HTTPError, URLError
from urllib.parse import urlencode, urlparse
from urllib.request import Request, urlopen

from common import ROOT, cli, read_json, save_json
from review import require_approval


def request_plan(output, *, version="v26.0", user_id="<IG_USER_ID>", public_base_url="https://example.invalid/output"):
    copy = read_json(Path(output) / "copy.json")
    base = f"https://graph.instagram.com/{version}"
    urls = public_base_url.rstrip("/")
    steps = []

    def create(name, params):
        steps.append({"step": "컨테이너 생성", "method": "POST", "endpoint": f"{base}/{user_id}/media",
                      "params": params, "save_as": name})
        steps.append({"step": "상태 확인", "method": "GET", "endpoint": f"{base}/{{{name}}}",
                      "params": {"fields": "status_code"}, "until": "FINISHED"})

    def publish(name):
        steps.append({"step": "게시", "method": "POST", "endpoint": f"{base}/{user_id}/media_publish",
                      "params": {"creation_id": "{" + name + "}"}, "save_as": name + "_MEDIA"})

    for i in range(1, len(copy["scenes"]) + 1):
        create(f"CHILD_{i}", {"image_url": f"{urls}/cards/card-{i:02d}.jpg", "is_carousel_item": "true"})
    create("CAROUSEL", {"media_type": "CAROUSEL", "children": ",".join("{CHILD_" + str(i) + "}" for i in range(1, len(copy["scenes"]) + 1)),
                        "caption": copy["caption"], "is_ai_generated": str(copy["is_ai_generated"]).lower()})
    publish("CAROUSEL")
    create("REEL", {"media_type": "REELS", "video_url": f"{urls}/reel.mp4", "caption": copy["caption"],
                    "is_ai_generated": str(copy["is_ai_generated"]).lower()})
    publish("REEL")
    return {"mode": "dry-run", "login": "Instagram Login", "authorization": "Bearer <REDACTED>", "requests": steps}


def api_request(method, endpoint, params, token):
    data = urlencode(params).encode()
    request = Request(endpoint + ("?" + data.decode() if method == "GET" else ""),
                      data=data if method == "POST" else None, method=method,
                      headers={"Authorization": "Bearer " + token})
    try:
        with urlopen(request, timeout=30) as response:
            result = json.load(response)
    except HTTPError as error:
        # 요청 헤더·응답 전문·토큰은 로그에 쓰지 않는다.
        raise ValueError(f"Meta API HTTP {error.code}. 자동 재시도하지 않습니다. 앱 대시보드에서 확인하세요.") from None
    except (URLError, TimeoutError, json.JSONDecodeError):
        raise ValueError("Meta API 응답을 확인하지 못했습니다. 재게시 전 대시보드에서 상태를 확인하세요.") from None
    if "error" in result:
        raise ValueError("Meta API 오류 응답입니다. 앱 대시보드에서 확인하세요.")
    return result


def execute_live(output, plan, token):
    journal = Path(output) / "LIVE_ATTEMPT.json"
    # 응답이 끊긴 경우 이미 게시됐을 수 있으므로 같은 폴더에서 자동 재실행하지 않는다.
    with journal.open("x", encoding="utf-8") as file:
        json.dump({"status": "started", "completed": []}, file)
    values, completed = {}, []

    def substitute(value):
        for name, replacement in values.items():
            value = value.replace("{" + name + "}", replacement)
        return value

    for step in plan["requests"]:
        endpoint = substitute(step["endpoint"])
        params = {key: substitute(value) for key, value in step["params"].items()}
        for attempt in range(5 if step["method"] == "GET" else 1):
            result = api_request(step["method"], endpoint, params, token)
            if step["method"] != "GET" or result.get("status_code") == "FINISHED":
                break
            if result.get("status_code") in ("ERROR", "EXPIRED"):
                raise ValueError("컨테이너 처리 실패 또는 만료. LIVE_ATTEMPT.json과 대시보드를 확인하세요.")
            if attempt == 4:
                raise ValueError("컨테이너 처리 시간 초과. 상태를 확인한 뒤 수동으로 재개해야 합니다.")
            time.sleep(60)
        if "save_as" in step:
            identifier = str(result.get("id", ""))
            if not identifier.isdigit():
                raise ValueError("Meta 응답에 유효한 ID가 없습니다. 대시보드에서 확인하세요.")
            values[step["save_as"]] = identifier
        completed.append({"step": step["step"], "save_as": step.get("save_as"), "id": result.get("id"), "status_code": result.get("status_code")})
        save_json(journal, {"status": "in_progress", "completed": completed})
    save_json(journal, {"status": "finished", "completed": completed})
    return {"mode": "live", "completed": completed}


def settings():
    """고정된 키트 .env만 읽는다. 셸 확장·실행 없이 환경변수가 우선한다."""
    values = {}
    path = ROOT / ".env"
    if path.is_file():
        for line in path.read_text(encoding="utf-8-sig").splitlines():
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            key, separator, value = line.partition("=")
            if not separator or key.strip() not in ("IG_ACCESS_TOKEN", "IG_USER_ID", "IG_API_VERSION"):
                raise ValueError(".env는 IG_ACCESS_TOKEN/IG_USER_ID/IG_API_VERSION=값 형식만 사용하세요. 값은 출력하지 않습니다.")
            values[key.strip()] = value.strip().strip("\"'")
    for key in ("IG_ACCESS_TOKEN", "IG_USER_ID", "IG_API_VERSION"):
        if key in os.environ:
            values[key] = os.environ[key].strip()
    values.setdefault("IG_API_VERSION", "v26.0")
    return values


def publish(output, *, live=False, public_base_url=None):
    output = Path(output)
    require_approval(output)
    config = settings()
    version = config["IG_API_VERSION"]
    if not re.fullmatch(r"v\d+\.\d+", version):
        raise ValueError("IG_API_VERSION은 v숫자.숫자 형식이어야 합니다.")
    if not live:
        plan = request_plan(output, version=version, **({"public_base_url": public_base_url} if public_base_url else {}))
        save_json(output / "dry-run.json", plan)
        print(json.dumps(plan, ensure_ascii=False, indent=2))
        return plan
    token = config.get("IG_ACCESS_TOKEN", "")
    user_id = config.get("IG_USER_ID", "")
    if not token or not user_id.isdigit() or not re.fullmatch(r"v\d+\.\d+", version):
        raise ValueError("--live에는 IG_ACCESS_TOKEN, 숫자 IG_USER_ID, IG_API_VERSION(v숫자.숫자)이 모두 필요합니다.")
    url = urlparse(public_base_url or "")
    if url.scheme != "https" or not url.hostname or url.hostname.endswith(".invalid") or url.username or url.password or url.query or url.fragment:
        raise ValueError("--live에는 자격증명·쿼리 없는 공개 HTTPS --base-url이 필요합니다.")
    if read_json(output / "copy.json")["synthetic"]:
        raise ValueError("동봉 합성 데이터는 live 게시할 수 없습니다. 드라이런으로 연습하세요.")
    return execute_live(output, request_plan(output, version=version, user_id=user_id, public_base_url=public_base_url), token)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("output", type=Path)
    parser.add_argument("--live", action="store_true")
    parser.add_argument("--base-url", "--public-base-url", dest="public_base_url", help="cards/와 reel.mp4가 있는 공개 HTTPS 폴더 URL")
    args = parser.parse_args()
    result = publish(args.output, live=args.live, public_base_url=args.public_base_url)
    if args.live:
        print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    cli(main)
