"""기본 드라이런. Blogger·설치형 WordPress에만 사람이 승인한 초안을 저장한다."""
import argparse
import base64
import json
import os
import re
from urllib.error import HTTPError, URLError
from urllib.parse import urlsplit
from urllib.request import HTTPRedirectHandler, Request, build_opener

from common import ROOT, cli, kit_path, read_json, save_json
from review import require_approval

ENV_KEYS = ("BLOGGER_BLOG_ID", "BLOGGER_ACCESS_TOKEN", "BLOGGER_TOKEN_FILE", "WP_URL", "WP_USER", "WP_APP_PASSWORD")


class NoRedirect(HTTPRedirectHandler):
    def redirect_request(self, req, fp, code, msg, headers, newurl):
        return None


def settings(env_file=None):
    values = {}
    path = kit_path(env_file) if env_file else ROOT / ".env"
    if not path.is_file():
        raise ValueError("live에는 사용자가 직접 준비한 .env 파일이 필요해요. .env.example을 복사해 채우세요.")
    for line in path.read_text(encoding="utf-8-sig").splitlines():
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        key, sep, value = line.partition("=")
        if not sep or key.strip() not in ENV_KEYS:
            raise ValueError(".env에는 .env.example의 항목만 KEY=값 형식으로 적으세요. 값은 표시하지 않아요.")
        values[key.strip()] = value.strip().strip("\"'")
    for key in ENV_KEYS:
        if key in os.environ:
            values[key] = os.environ[key].strip()
    return values


def wordpress_base(url, live=False):
    try:
        parsed = urlsplit(url)
        valid = (parsed.scheme == "https" and parsed.hostname and not parsed.username and not parsed.password
                 and not parsed.query and not parsed.fragment and parsed.port in (None, 443)
                 and not any(ord(c) < 33 or ord(c) == 127 for c in url) and "\\" not in url)
    except ValueError:
        valid = False
    if not valid:
        raise ValueError("WP_URL은 인증 정보·쿼리 없는 HTTPS 사이트 주소로 적으세요.")
    if parsed.hostname == "wordpress.com" or parsed.hostname.endswith(".wordpress.com") or parsed.hostname == "public-api.wordpress.com":
        raise ValueError("WordPress.com은 별도 OAuth 방식이에요. 이 키트는 설치형 WordPress만 지원해요.")
    if live and parsed.hostname.endswith(".invalid"):
        raise ValueError("WP_URL을 본인이 관리하는 설치형 사이트 주소로 바꾸세요.")
    return url.rstrip("/")


def request_plan(output, platform, *, blog_id=None, wp_url=None):
    metadata = read_json(output / "render.json")
    content = (output / "editor.html").read_text(encoding="utf-8")
    body = {"title": metadata["title"], "content": content}
    if platform == "blogger":
        if blog_id is not None and not re.fullmatch(r"[0-9]+", blog_id):
            raise ValueError("Blogger 블로그 ID에는 숫자만 입력하세요.")
        endpoint = f"https://www.googleapis.com/blogger/v3/blogs/{blog_id or '<BLOG_ID>'}/posts?isDraft=true"
    elif platform == "wordpress":
        endpoint = wordpress_base(wp_url or "https://example.invalid") + "/wp-json/wp/v2/posts"
        body["status"] = "draft"
    else:
        raise ValueError("API 대상은 blogger/wordpress예요.")
    return {"mode": "dry-run", "platform": platform, "method": "POST", "endpoint": endpoint,
            "authorization": "<REDACTED>", "body": body, "state": "draft"}


def credentials(platform, config):
    if platform == "blogger":
        token = config.get("BLOGGER_ACCESS_TOKEN", "")
        if config.get("BLOGGER_TOKEN_FILE"):
            # 파일의 리프레시 토큰이나 클라이언트 비밀 정보는 표시하지 않는다.
            value = read_json(kit_path(config["BLOGGER_TOKEN_FILE"]))
            token = value.get("access_token") or value.get("token") or ""
        if not isinstance(token, str) or not token.strip() or not re.fullmatch(r"[0-9]+", config.get("BLOGGER_BLOG_ID", "")):
            raise ValueError("--live에는 본인의 Blogger OAuth 액세스 토큰과 숫자 블로그 ID가 필요해요.")
        authorization = "Bearer " + token
    else:
        wordpress_base(config.get("WP_URL", ""), live=True)
        user, password = config.get("WP_USER", ""), config.get("WP_APP_PASSWORD", "")
        if not user or not password or ":" in user:
            raise ValueError("--live에는 WP_USER와 WP_APP_PASSWORD가 필요해요. 주 비밀번호는 쓰지 마세요.")
        authorization = "Basic " + base64.b64encode(f"{user}:{password}".encode()).decode()
    if any(ord(c) < 32 or ord(c) == 127 for c in authorization):
        raise ValueError("인증 정보의 형식을 확인하세요.")
    return authorization


def send(plan, authorization):
    request = Request(plan["endpoint"], data=json.dumps(plan["body"], ensure_ascii=False).encode(),
                      headers={"Content-Type": "application/json; charset=utf-8", "Authorization": authorization}, method="POST")
    try:
        # 리다이렉트 대상에 인증 정보 전송·POST 재전송을 금지한다.
        with build_opener(NoRedirect()).open(request, timeout=30) as response:
            if response.status not in (200, 201):
                raise ValueError("API 응답을 확인하지 못했어요. 관리 화면에서 중복·저장 상태를 확인하세요.")
            result = json.load(response)
    except HTTPError as error:
        raise ValueError(f"API HTTP {error.code}. 자동 재시도하지 않아요. 관리 화면의 저장 상태·권한을 확인하세요.") from None
    except (URLError, OSError, ValueError):
        raise ValueError("API 응답을 확인하지 못했어요. 재전송 전 관리 화면에서 저장 상태를 확인하세요.") from None
    if not isinstance(result, dict) or isinstance(result.get("id"), bool) or not re.fullmatch(r"[0-9]+", str(result.get("id", ""))):
        raise ValueError("API 글 ID를 확인하지 못했어요. 관리 화면에서 저장 상태를 확인하세요.")
    if (plan["platform"] == "wordpress" and result.get("status") != "draft") or (plan["platform"] == "blogger" and result.get("status") not in (None, "DRAFT")):
        raise ValueError("응답이 초안 상태가 아니에요. 관리 화면을 확인하세요.")
    return {"id": str(result["id"]), "state": "draft", "mode": "live"}


def publish(output, platform, live=False, env_file=None, blog_id=None, wp_url=None):
    output = kit_path(output)
    if platform in ("naver", "tistory"):
        if live:
            raise ValueError("이 플랫폼은 API 발행을 지원하지 않아요. editor.html을 편집기에 옮기세요.")
        message = "편집기에 붙여 넣기: preview.html을 브라우저에서 열어 내용을 복사하세요. 제목·사진·서식·링크를 편집기에서 확인하고 직접 발행하세요."
        print(message)
        return {"mode": "manual", "message": message}
    require_approval(output)
    if not live:
        # .env·환경변수·인증 파일에 접근하지 않는다.
        plan = request_plan(output, platform, blog_id=blog_id, wp_url=wp_url)
        save_json(output / "dry-run.json", plan)
        print(json.dumps(plan, ensure_ascii=False, indent=2))
        return plan
    if read_json(output / "render.json").get("synthetic"):
        raise ValueError("동봉 가상 연습용 글은 live 저장할 수 없어요. 본인 자료로 새 글을 만드세요.")
    config = settings(env_file)
    authorization = credentials(platform, config)
    plan = request_plan(output, platform, blog_id=config.get("BLOGGER_BLOG_ID") if platform == "blogger" else None,
                        wp_url=config.get("WP_URL") if platform == "wordpress" else None)
    # 로컬 이미지 자동 업로드는 지원하지 않는다. HTTPS 이미지로 바꾸고 다시 검수한다.
    from html.parser import HTMLParser
    class Images(HTMLParser):
        def handle_starttag(self, tag, attrs):
            if tag == "img" and urlsplit(dict(attrs).get("src", "")).scheme != "https":
                raise ValueError("API 초안의 이미지는 본인이 권리를 확인한 HTTPS 주소여야 해요. 로컬 이미지는 편집기에서 직접 올리세요.")
    Images().feed(plan["body"]["content"])
    journal = output / "LIVE_ATTEMPT.json"
    try:
        with journal.open("x", encoding="utf-8") as stream:
            json.dump({"state": "started", "platform": platform}, stream)
    except FileExistsError:
        raise ValueError("live 시도 기록이 있어 재전송을 멈췄어요. 서버 글 목록과 LIVE_ATTEMPT.json을 직접 확인하세요.") from None
    result = send(plan, authorization)
    save_json(journal, result)
    print("초안 저장 완료. 게시 관리 화면에서 글 ID와 공개 상태를 확인하세요.")
    return result


def main():
    from common import PLATFORMS
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("output")
    parser.add_argument("--platform", choices=PLATFORMS, default="blogger")
    parser.add_argument("--live", action="store_true")
    parser.add_argument("--env-file", help="사용자가 직접 준비한 .env 경로")
    parser.add_argument("--blog-id", help="드라이런 대상 숫자 ID. live는 .env 값을 사용")
    parser.add_argument("--wp-url", help="드라이런 대상 HTTPS 사이트. live는 .env 값을 사용")
    args = parser.parse_args()
    publish(args.output, args.platform, args.live, args.env_file, args.blog_id, args.wp_url)


if __name__ == "__main__":
    cli(main)
