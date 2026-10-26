"""공통 파일·설정·오류 처리. 실행 의존성은 표준 라이브러리뿐이다."""
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parent
PLATFORMS = ("naver", "tistory", "blogger", "wordpress")
TYPES = ("정보", "후기", "경험")


def kit_path(value):
    path = Path(value).expanduser()
    return (path if path.is_absolute() else ROOT / path).resolve()


def read_json(path):
    value = json.loads(Path(path).read_text(encoding="utf-8-sig"))
    if not isinstance(value, dict):
        raise ValueError("JSON의 맨 바깥은 중괄호로 감싼 객체여야 해요.")
    return value


def save_text(path, value):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(value, encoding="utf-8")


def save_json(path, value):
    save_text(path, json.dumps(value, ensure_ascii=False, indent=2) + "\n")


def load_config(path=None):
    source = kit_path(path) if path else ROOT / ("config.json" if (ROOT / "config.json").is_file() else "config.example.json")
    config = read_json(source)
    if config.get("platform") not in PLATFORMS or config.get("article_type") not in TYPES:
        raise ValueError("config의 platform 또는 article_type을 확인하세요.")
    for name in ("keyword", "blog_name", "reader"):
        if not isinstance(config.get(name), str) or not config[name].strip():
            raise ValueError(f"config의 {name}에 내용을 적으세요.")
    rules = config.get("rules", {})
    if not isinstance(rules, dict):
        raise ValueError("rules는 중괄호로 감싼 설정 객체여야 해요.")
    for name in ("title_min", "title_max", "body_min", "body_max", "h2_min", "repeat_min"):
        if type(rules.get(name)) is not int or rules[name] < 1:
            raise ValueError(f"rules.{name}은 양의 정수여야 합니다.")
    if rules["title_min"] > rules["title_max"] or rules["body_min"] > rules["body_max"]:
        raise ValueError("최솟값은 최댓값보다 클 수 없습니다.")
    for name in ("affiliate_markers", "cliches"):
        if not isinstance(rules.get(name), list) or any(not isinstance(v, str) or not v.strip() for v in rules[name]):
            raise ValueError(f"rules.{name}은 비어 있지 않은 문자열 목록이어야 합니다.")
    if not isinstance(rules.get("experience_heading"), str) or not rules["experience_heading"].strip():
        raise ValueError("rules.experience_heading에 소제목을 적으세요.")
    return config


def cli(main):
    try:
        main()
    except (ValueError, OSError, KeyError, TypeError) as error:
        # 인증/HTTP 오류는 publish.py에서 별도 처리한다. 파일 경로·외부 오류 전문도 출력하지 않는다.
        message = str(error) if isinstance(error, ValueError) and not isinstance(error, json.JSONDecodeError) else "파일·JSON 형식·접근 권한을 확인하세요."
        print(f"오류: {message}", file=sys.stderr)
        raise SystemExit(1) from None
