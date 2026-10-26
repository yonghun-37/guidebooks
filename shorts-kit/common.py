"""starter-kit의 JSON·해시·CLI 처리를 재사용한 독립 공통 모듈."""
from __future__ import annotations

import hashlib
import json
import math
from pathlib import Path
import sys

import yaml

ROOT = Path(__file__).resolve().parent


def read_json(path):
    return json.loads(Path(path).read_text(encoding="utf-8"))


def save_json(path, value):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_name(path.name + ".tmp")
    temporary.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    temporary.replace(path)


def digest(path):
    value = hashlib.sha256()
    with Path(path).open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            value.update(block)
    return value.hexdigest()


def number(value, low, high, label):
    if type(value) not in (int, float) or not math.isfinite(value) or not low <= value <= high:
        raise ValueError(f"{label}: {low}~{high} 안의 숫자를 입력하세요.")
    return value


def load_config(path=None):
    path = Path(path).resolve() if path else ROOT / "config.example.yaml"
    config = yaml.safe_load(path.read_text(encoding="utf-8"))
    if not isinstance(config, dict):
        raise ValueError("설정 파일은 YAML 객체여야 합니다.")
    def local(value):
        if not isinstance(value, str) or "://" in value:
            raise ValueError("설정에는 로컬 파일 경로만 입력하세요.")
        return str((path.parent / value).resolve())
    config["font"] = local(config["font"])
    if not Path(config["font"]).is_file():
        raise ValueError("font 파일이 없습니다.")
    if config["llm"]["mode"] not in ("offline", "prompt", "api"):
        raise ValueError("llm.mode는 offline/prompt/api여야 합니다.")
    video = config["video"]
    number(video["duration"], 1, 180, "duration [Y001]")
    if round(video["duration"] * 30) != video["duration"] * 30:
        raise ValueError("duration은 프레임에 맞게 정수 초로 입력하세요.")
    number(video["caption_size"], 24, 100, "caption_size (키트 허용값)")
    for key in ("caption_size", "safe_left", "safe_right", "safe_top", "safe_bottom"):
        if type(video[key]) is not int or video[key] < 0:
            raise ValueError(f"{key}는 음수가 아닌 정수여야 합니다.")
    if video["safe_left"] + video["safe_right"] > 720 or video["safe_top"] + video["safe_bottom"] > 1400:
        raise ValueError("안전 여백이 너무 큽니다. 가로·세로에 글자 공간을 남기세요.")
    number(video["music_gain"], 0, 1, "music_gain")
    for key in ("narration", "scenes_dir", "music"):
        if video.get(key):
            video[key] = local(video[key])
            if not Path(video[key]).exists():
                raise ValueError(f"{key} 파일 또는 폴더가 없습니다.")
    rights = config["rights"]
    if video.get("narration") and (not isinstance(rights.get("narration"), str) or not rights["narration"].strip()):
        raise ValueError("rights.narration에 화자·이용 동의를 적으세요.")
    if video.get("scenes_dir") and (not isinstance(rights.get("scenes"), str) or not rights["scenes"].strip()):
        raise ValueError("rights.scenes에 장면의 출처·사용 조건을 적으세요.")
    music = rights["music"]
    if video.get("music"):
        if music.get("confirmed") is not True or any(not isinstance(music.get(k), str) or not music[k].strip()
                                                      for k in ("source", "license", "evidence")):
            raise ValueError("음악 사용 전 confirmed·source·license·evidence를 확인하세요. [Y016]")
        music["evidence"] = local(music["evidence"])
        if not Path(music["evidence"]).is_file():
            raise ValueError("음악 이용 조건 증빙 파일이 없습니다.")
    return config


def cli(main):
    try:
        main()
    except (ValueError, OSError, KeyError, TypeError, yaml.YAMLError) as error:
        print(f"오류: {error}", file=sys.stderr)
        raise SystemExit(1)
