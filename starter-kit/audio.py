"""사용자 제공 음원과 명시적으로 선택한 TTS 플러그만 사용한다."""
import importlib
from pathlib import Path
import shutil


def prepare_audio(copy, config, output):
    settings = config["reel"]
    narration = settings.get("narration")
    if settings["tts"] == "plugin":
        if narration:
            raise ValueError("직접 녹음 narration과 TTS plugin 중 하나만 선택하세요.")
        target = settings.get("tts_plugin") or ""
        if target.count(":") != 1:
            raise ValueError("tts_plugin은 사용자모듈:함수 형식이어야 합니다.")
        module, function = target.split(":")
        narration = Path(output) / "audio" / "narration.wav"
        narration.parent.mkdir(parents=True, exist_ok=True)
        narration.unlink(missing_ok=True)  # 이전 실행의 음성을 새 합성 결과로 오인하지 않는다.
        try:
            backend = getattr(importlib.import_module(module), function)
            backend(text="\n".join(s["subtitle"].replace("**", "") for s in copy["scenes"]),
                    output_path=narration)
        except Exception:
            raise ValueError("TTS 플러그 실행 실패. 모듈·함수·설정과 라이선스를 확인하세요.") from None
        if not narration.is_file():
            raise ValueError("TTS 플러그가 output_path에 WAV를 생성하지 않았습니다.")
    elif settings["tts"] != "silent":
        raise ValueError("reel.tts는 silent/plugin이어야 합니다.")
    result = {}
    for kind, source in (("narration", narration), ("music", settings.get("music"))):
        if not source:
            continue
        source = Path(source)
        if source.suffix.lower() not in (".mp3", ".wav") or not source.is_file():
            raise ValueError(f"{kind}: 사용자 제공 mp3/wav 파일을 확인하세요.")
        target = Path(output) / "audio" / (kind + source.suffix.lower())
        target.parent.mkdir(parents=True, exist_ok=True)
        if source.resolve() != target.resolve():
            shutil.copyfile(source, target)
        result[kind] = target
    return result
