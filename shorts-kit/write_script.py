"""오프라인 예제 / 웹 채팅 붙여넣기 / 명시적으로 요청한 API 대본."""
import json
import os
from pathlib import Path
import re
from urllib.error import HTTPError, URLError
from urllib.parse import urlsplit
from urllib.request import HTTPRedirectHandler, Request, build_opener

from common import ROOT, number, save_json


class NoRedirect(HTTPRedirectHandler):
    def redirect_request(self, *args, **kwargs):
        return None


urlopen = build_opener(NoRedirect()).open


def example(duration):
    # 가상 사례, 초 단위는 이 키트의 학습용 배분이다.
    texts = [
        ("책상에서 하나만 바꿔요", "어디부터 정리할지 막막한가요? 오늘은 책상 위에서 자주 쓰는 물건 하나만 골라 볼게요.", "자주 쓰는 물건 하나를 골라요"),
        ("손이 닿는 곳으로", "그 물건을 편하게 꺼낼 수 있는 곳으로 옮겨 보세요. 나머지는 잠시 그대로 두고 손을 뻗어 봐요.", "편하게 꺼낼 곳으로 옮겨요"),
        ("바뀐 점을 보여 줘요", "옮기기 전과 후를 같은 자리에서 찍어 비교해 보세요. 쓰기 편해졌다면 그 자리를 기억해 두세요.", "바꾸기 전과 후를 찍어 봐요"),
    ]
    total_frames = round(duration * 30)
    boundaries = [round(i * total_frames / 3) for i in range(4)]
    return {"label": "가상 사례 · 도윤의 책상 정리 연습", "hooks": ["무엇부터 정리할까요?", "물건 하나만 옮겨 봤어요", "자주 쓰는 물건을 골라 보세요"],
            "title": "책상에서 물건 하나만 옮겨 보기", "description": "직접 해 보는 책상 정리 연습이에요. 가상 사례예요.",
            "hashtags": ["#책상정리", "#직접만들기"],
            "privacyStatus": "private", "selfDeclaredMadeForKids": None, "containsSyntheticMedia": None,
            "scenes": [{"title": title, "narration": voice, "subtitle": caption,
                        "duration": (boundaries[i + 1] - boundaries[i]) / 30}
                       for i, (title, voice, caption) in enumerate(texts)]}


def validate(script):
    if not isinstance(script, dict):
        raise ValueError("script.json은 JSON 객체여야 합니다.")
    for key in ("label", "title", "description"):
        if not isinstance(script.get(key), str) or not script[key].strip():
            raise ValueError(f"{key}에 글을 입력하세요.")
    if len(script["title"]) > 100 or any(c in script["title"] for c in "<>\n\r"):
        raise ValueError("title은 줄바꿈·꺾쇠 없이 100자 이내로 적으세요. [Y032]")
    tags = script.get("hashtags")
    if not isinstance(tags, list) or any(not isinstance(t, str) or not re.fullmatch(r"#[\w가-힣]+", t) for t in tags):
        raise ValueError("hashtags는 #낱말 문자열 배열이어야 합니다.")
    if len((script["description"] + "\n" + " ".join(tags)).encode("utf-8")) > 5000 or any(c in script["description"] for c in "<>"):
        raise ValueError("설명·해시태그가 너무 길거나 꺾쇠가 있습니다. 키트는 UTF-8 5000바이트 이내로 제한합니다. [Y037]")
    hooks = script.get("hooks")
    if not isinstance(hooks, list) or len(hooks) != 3 or any(not isinstance(h, str) or not h.strip() for h in hooks):
        raise ValueError("hooks에 첫 문장 세 가지를 적으세요.")
    if script.get("privacyStatus") not in ("private", "unlisted", "public"):
        raise ValueError("privacyStatus는 private/unlisted/public 중 하나입니다.")
    for key in ("selfDeclaredMadeForKids", "containsSyntheticMedia"):
        if script.get(key) is not None and type(script[key]) is not bool:
            raise ValueError(f"{key}는 null/true/false 중 하나입니다.")
    scenes = script.get("scenes")
    if not isinstance(scenes, list) or not 1 <= len(scenes) <= 30:
        raise ValueError("scenes는 장면 1~30개의 배열이어야 합니다. (키트 제한)")
    total = 0
    for scene in scenes:
        if not isinstance(scene, dict):
            raise ValueError("장면은 JSON 객체여야 합니다.")
        for key in ("title", "narration", "subtitle"):
            if not isinstance(scene.get(key), str) or not scene[key].strip():
                raise ValueError(f"장면의 {key}를 적으세요.")
        value = number(scene.get("duration"), 1 / 30, 180, "장면 duration")
        if abs(value * 30 - round(value * 30)) > 1e-6:
            raise ValueError("장면 duration은 1/30초 프레임에 맞춰 입력하세요.")
        total += round(value * 30)
    if not 1 <= total <= 180 * 30:
        raise ValueError("전체 영상은 최대 3분입니다. [Y001]")
    return script


def build_prompt(config):
    guides = [(ROOT / "prompts" / f"{name}.md").read_text(encoding="utf-8") for name in ("hooks", "script", "metadata")]
    return "\n\n".join(guides) + "\n\nJSON 예제(가상):\n" + json.dumps(example(config["video"]["duration"]), ensure_ascii=False, indent=2)


def generate(config, output, mode=None, allow_api=False):
    output = Path(output)
    mode = mode or config["llm"]["mode"]
    if mode == "prompt":
        (output / "prompt.md").write_text(build_prompt(config), encoding="utf-8")
        print(f"prompt.md를 웹 채팅에 붙여 넣고 답변을 {output / 'script.json'}에 저장하세요.")
        return None
    if mode == "offline":
        script = example(config["video"]["duration"])
    elif mode == "api":
        if not allow_api:
            raise ValueError("API 호출은 --allow-api를 직접 지정해야 합니다.")
        base, key, model = (os.getenv(k, "") for k in ("LLM_BASE_URL", "LLM_API_KEY", "LLM_MODEL"))
        parsed = urlsplit(base)
        if parsed.scheme != "https" or not parsed.hostname or parsed.username or parsed.password or parsed.query or parsed.fragment or not key or not model:
            raise ValueError("LLM_BASE_URL(HTTPS /v1)·LLM_API_KEY·LLM_MODEL을 환경변수에 설정하세요.")
        request = Request(base.rstrip("/") + "/chat/completions", method="POST",
                          headers={"Authorization": "Bearer " + key, "Content-Type": "application/json"},
                          data=json.dumps({"model": model, "messages": [{"role": "user", "content": build_prompt(config)}]}).encode())
        try:
            with urlopen(request, timeout=60) as response:
                choice = json.load(response)["choices"][0]
            if choice["finish_reason"] != "stop":
                raise ValueError("응답 미완료")
            script = json.loads(choice["message"]["content"])
        except (HTTPError, URLError, OSError, KeyError, IndexError, TypeError, ValueError):
            raise ValueError("API 응답 실패. 연결·모델·권한·JSON 형식을 확인하세요. 인증 값은 출력하지 않습니다.") from None
    else:
        raise ValueError("mode는 offline/prompt/api 중 하나입니다.")
    save_json(output / "script.json", validate(script))
    return script
