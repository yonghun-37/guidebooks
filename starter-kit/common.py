"""공통 파일 처리. 실행 경로와 무관하게 동봉 자산을 찾는다."""
from __future__ import annotations

import hashlib
import json
from pathlib import Path
import sys

import yaml

ROOT = Path(__file__).resolve().parent


def read_json(path):
    return json.loads(Path(path).read_text(encoding="utf-8"))


def save_json(path, value):
    Path(path).parent.mkdir(parents=True, exist_ok=True)
    Path(path).write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def load_config(path=None):
    path = Path(path).resolve() if path else ROOT / "config.example.yaml"
    config = yaml.safe_load(path.read_text(encoding="utf-8"))
    config["font"] = str((path.parent / config["font"]).resolve())
    config["rss"] = [str((path.parent / p).resolve()) if not p.startswith(("https://", "http://")) else p
                     for p in config["rss"]]
    if config["llm"]["mode"] not in ("offline", "prompt", "api"):
        raise ValueError("llm.mode는 offline/prompt/api여야 합니다.")
    if config["reel"]["tts"] not in ("silent", "plugin"):
        raise ValueError("reel.tts는 silent/plugin이어야 합니다.")
    theme = config.get("theme", "forest")
    from render_cards import THEMES
    if theme not in THEMES:
        raise ValueError("theme은 forest/ink/coral이어야 합니다.")
    config["colors"] = {**THEMES[theme], **config.get("colors", {})}
    config["asset_root"] = str(path.parent)
    for key in ("narration", "music"):
        if config["reel"].get(key):
            config["reel"][key] = str((path.parent / config["reel"][key]).resolve())
    if not 15 <= float(config["reel"]["duration"]) <= 30:
        raise ValueError("릴스 duration은 15~30초로 설정하세요.")
    if not isinstance(config["publish"]["is_ai_generated"], bool):
        raise ValueError("publish.is_ai_generated는 true 또는 false여야 합니다.")
    return config


def digest(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def cli(main):
    try:
        main()
    except (ValueError, OSError, KeyError, yaml.YAMLError) as error:
        print(f"오류: {error}", file=sys.stderr)
        raise SystemExit(1)
