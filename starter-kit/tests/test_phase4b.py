import copy
import io
import json
import math
from pathlib import Path
import struct
import subprocess
import sys
import types
import wave

from PIL import Image, ImageChops, ImageDraw
import pytest
import yaml

from audio import prepare_audio
from common import ROOT, load_config, read_json, save_json
from fetch_news import fetch
from make_reel import ffmpeg_exe, make_reel
from render_cards import THEMES, font, plain, render_cards, text_box
from review import approve, prepare_review, require_approval
from run_pipeline import render, run
from write_copy import build_prompt, generate_copy, validate_copy, write_copy


@pytest.fixture
def config():
    return load_config()


@pytest.fixture
def news(config):
    return fetch(config["rss"])


@pytest.fixture
def draft(news, config):
    return write_copy(news, config)


def config_file(tmp_path, config, mode="offline"):
    config = copy.deepcopy(config)
    config["llm"]["mode"] = mode
    path = tmp_path / "config.yaml"
    path.write_text(yaml.safe_dump(config, allow_unicode=True), encoding="utf-8")
    return path


@pytest.mark.parametrize("template", ["cards", "reel-script", "caption"])
def test_prompt_contract_and_no_overwrite(template, draft, config, news, tmp_path):
    output = tmp_path / "copy.json"
    save_json(output, draft)
    before = output.read_bytes()
    assert generate_copy(news, config, output, mode="prompt", template=template) is None
    assert output.read_bytes() == before
    prompt = (tmp_path / "prompt.md").read_text(encoding="utf-8")
    for rule in ("사실 추가 금지", "출처 유지", "과장 금지", '"scenes"', '"synthetic": true'):
        assert rule in prompt
    assert all(a["link"] in prompt for a in news["articles"])
    assert validate_copy(read_json(output), news) == draft


def test_prompt_pipeline_wait_validate_then_render(config, draft, tmp_path, monkeypatch):
    output = tmp_path / "web-chat"
    run(output, config_file(tmp_path, config, "prompt"))
    assert (output / "prompt.md").exists()
    assert not (output / "copy.json").exists()
    assert not (output / "REVIEW.md").exists()
    # 웹 채팅에서 받은 전체 JSON을 붙여 넣는 과정을 재현한다.
    save_json(output / "copy.json", draft)
    validate_copy(read_json(output / "copy.json"), read_json(output / "news.json"))
    calls = []
    monkeypatch.setattr("run_pipeline.render_cards", lambda *args: calls.append("cards") or [])
    monkeypatch.setattr("run_pipeline.make_reel", lambda *args: calls.append("reel"))
    monkeypatch.setattr("run_pipeline.prepare_review", lambda *args: calls.append("review"))
    render(output)
    assert calls == ["cards", "reel", "review"]


@pytest.mark.parametrize("mutation", [
    lambda c: c.update(synthetic="false"),
    lambda c: c.update(is_ai_generated=0),
    lambda c: c.update(account_name=""),
    lambda c: c.update(scenes=[]),
    lambda c: c["scenes"][0].update(layout="other"),
    lambda c: c["scenes"][1].update(points=[]),
    lambda c: c["scenes"][1].update(points=["a"]*4),
    lambda c: c["scenes"][1].update(points=[{}]),
    lambda c: c["scenes"][1].update(subtitle=None),
    lambda c: c["scenes"][0].update(image={}),
    lambda c: c.update(label="실제 뉴스"),
    lambda c: c.update(caption="출처 삭제"),
    lambda c: c.update(synthetic=False),
    lambda c: [s.update(source="출처 삭제") for s in c["scenes"]],
])
def test_schema_rejects_invalid_or_source_lost(draft, news, mutation):
    mutation(draft)
    with pytest.raises(ValueError):
        validate_copy(draft, news)


def api_env(monkeypatch):
    monkeypatch.setenv("LLM_BASE_URL", "https://model.example.invalid/v1")
    monkeypatch.setenv("LLM_API_KEY", "SECRET_TEST_SENTINEL")
    monkeypatch.setenv("LLM_MODEL", "user-selected-model")


def test_api_is_explicit_and_mocked(monkeypatch, config, news, draft, tmp_path, capsys):
    api_env(monkeypatch)
    output = tmp_path / "copy.json"
    with pytest.raises(ValueError, match="--allow-api"):
        generate_copy(news, config, output, mode="api")
    calls = []
    def mocked(request, timeout):
        calls.append(request)
        assert request.full_url == "https://model.example.invalid/v1/chat/completions"
        assert request.get_header("Authorization") == "Bearer SECRET_TEST_SENTINEL"
        body = json.loads(request.data)
        assert body["model"] == "user-selected-model"
        assert body["messages"][0]["role"] == "user"
        assert "사실 추가 금지" in body["messages"][0]["content"]
        assert timeout == 60
        return io.StringIO(json.dumps({"choices": [{"finish_reason": "stop", "message": {"content": json.dumps(draft)}}]}))
    monkeypatch.setattr("write_copy.urlopen", mocked)
    generate_copy(news, config, output, mode="api", allow_api=True)
    assert len(calls) == 1 and read_json(output) == draft
    assert "SECRET_TEST_SENTINEL" not in output.read_text() + capsys.readouterr().out


@pytest.mark.parametrize("response", [
    {"choices": []},
    {"choices": [{"finish_reason": "length", "message": {"content": "{}"}}]},
    {"choices": [{"finish_reason": "stop", "message": {"content": "bad json SECRET_TEST_SENTINEL"}}]},
    {"choices": [{"finish_reason": "stop", "message": {"content": "{}"}}]},
])
def test_api_invalid_response_preserves_existing(monkeypatch, config, news, tmp_path, response):
    api_env(monkeypatch)
    output = tmp_path / "copy.json"
    output.write_text("prior", encoding="utf-8")
    monkeypatch.setattr("write_copy.urlopen", lambda *a, **k: io.StringIO(json.dumps(response)))
    with pytest.raises(ValueError) as error:
        generate_copy(news, config, output, mode="api", allow_api=True)
    assert "SECRET_TEST_SENTINEL" not in str(error.value)
    assert output.read_text() == "prior"


def test_api_network_error_redacted_and_no_redirect(monkeypatch, config, news, tmp_path):
    from urllib.error import URLError
    from write_copy import NoRedirect
    api_env(monkeypatch)
    def failed(*args, **kwargs):
        raise URLError("SECRET_TEST_SENTINEL")
    monkeypatch.setattr("write_copy.urlopen", failed)
    with pytest.raises(ValueError) as error:
        generate_copy(news, config, tmp_path / "copy.json", mode="api", allow_api=True)
    assert "SECRET_TEST_SENTINEL" not in str(error.value)
    assert NoRedirect().redirect_request(None, None, None, None, None, None) is None


@pytest.mark.parametrize("bad_url", ["http://model.invalid/v1", "https://name:secret@model.invalid/v1", "https://model.invalid/v1?key=secret"])
def test_api_rejects_unsafe_endpoint(monkeypatch, config, news, tmp_path, bad_url):
    api_env(monkeypatch)
    monkeypatch.setenv("LLM_BASE_URL", bad_url)
    with pytest.raises(ValueError, match="환경변수"):
        generate_copy(news, config, tmp_path / "copy.json", mode="api", allow_api=True)


@pytest.mark.parametrize("mode,tts", [("api", "silent"), ("offline", "plugin")])
def test_offline_pipeline_rejects_external_backends(tmp_path, config, mode, tts):
    config["reel"]["tts"] = tts
    with pytest.raises(ValueError, match="오프라인"):
        run(tmp_path / "blocked", config_file(tmp_path, config, mode), offline=True, allow_api=True)
    assert not (tmp_path / "blocked").exists()


@pytest.mark.parametrize("theme", list(THEMES))
def test_templates_themes_highlight_and_image_slot(config, draft, tmp_path, theme):
    config["colors"] = THEMES[theme]
    draft["scenes"] = [draft["scenes"][0], draft["scenes"][1], draft["scenes"][-1]]
    draft["scenes"][1]["points"] = ["**첫 번째** 요점", "두 번째 요점", "세 번째 요점"]
    supplied = tmp_path / "my-image.png"
    Image.new("RGB", (50, 100), "#DB7EFA").save(supplied)
    draft["scenes"][0]["image"] = str(supplied)
    paths = render_cards(draft, config, tmp_path / theme)
    with Image.open(paths[0]) as cover, Image.open(paths[1]) as body, Image.open(paths[2]) as closing:
        assert cover.getpixel((100, 900)) == (219, 126, 250)
        assert cover.getpixel((0, 0)) != closing.getpixel((0, 0))
        assert len(body.crop((70, 730, 1000, 1160)).getcolors(1_000_000)) > 100
        # ** 마킹은 별표로 남지 않고 실제 강조색 픽셀을 만든다.
        accent = tuple(bytes.fromhex(config["colors"]["accent"][1:]))
        assert accent in dict((color, n) for n, color in cover.crop((60, 270, 1010, 600)).getcolors(1_000_000))
    assert plain("**강조**") == "강조"


def test_text_overflow_and_missing_image_fail(config, draft, tmp_path):
    draw = ImageDraw.Draw(Image.new("RGB", (100, 100)))
    with pytest.raises(ValueError, match="영역"):
        text_box(draw, "아주 긴 문장"*1000, (0, 0, 50, 40), config, 44, "white")
    draft["scenes"][0]["image"] = "missing-local-photo.png"
    with pytest.raises(OSError):
        render_cards(draft, config, tmp_path / "missing")
    draft["scenes"][0]["image"] = "https://example.invalid/photo.png"
    with pytest.raises(ValueError, match="로컬"):
        render_cards(draft, config, tmp_path / "remote")


def wav_file(path):
    with wave.open(str(path), "wb") as out:
        out.setparams((1, 2, 16000, 0, "NONE", "not compressed"))
        out.writeframes(b"".join(struct.pack("<h", round(5000*math.sin(2*math.pi*440*i/16000))) for i in range(32000)))
    return path


def audio_rms(path, start=0.3):
    pcm = subprocess.run([ffmpeg_exe(), "-v", "error", "-ss", str(start), "-i", str(path), "-t", "0.5",
                          "-map", "0:a", "-f", "s16le", "-ac", "1", "-ar", "8000", "pipe:1"],
                         capture_output=True, check=True).stdout
    values = struct.unpack("<" + "h"*(len(pcm)//2), pcm)
    return math.sqrt(sum(v*v for v in values)/len(values))


@pytest.mark.parametrize("kind", ["narration", "music", "mixed", "plugin"])
def test_real_audio_paths_mix_and_review_manifest(config, draft, tmp_path, monkeypatch, kind):
    source = wav_file(tmp_path / "voice.wav")
    draft["scenes"] = [draft["scenes"][0], draft["scenes"][1], draft["scenes"][-1]]
    config["reel"]["duration"] = 15
    output = tmp_path / kind
    output.mkdir()
    if kind in ("narration", "mixed"):
        # MP3 사용자 입력도 실제 디코딩한다.
        mp3 = tmp_path / "voice.mp3"
        subprocess.run([ffmpeg_exe(), "-v", "error", "-i", str(source), "-y", str(mp3)], check=True)
        config["reel"]["narration"] = str(mp3)
    if kind in ("music", "mixed"):
        config["reel"]["music"] = str(source)
    if kind == "plugin":
        module = types.ModuleType("test_voice_backend")
        calls = []
        def synthesize(*, text, output_path):
            calls.append(text)
            output_path.write_bytes(source.read_bytes())
        module.synthesize = synthesize
        monkeypatch.setitem(sys.modules, module.__name__, module)
        config["reel"].update(tts="plugin", tts_plugin="test_voice_backend:synthesize")
    cards = render_cards(draft, config, output / "cards")
    reel = make_reel(draft, config, cards, output)
    assert audio_rms(reel) > 100
    assert audio_rms(reel, start=10) < 2  # 짧은 음원의 나머지는 무음으로 채운다
    info = read_json(output / "reel-info.json")
    assert "silent" not in info["audio"]
    if kind == "mixed":
        assert info["audio"] == ["narration", "music"]
    if kind == "plugin":
        assert calls == ["\n".join(plain(s["subtitle"]) for s in draft["scenes"])]
    save_json(output / "copy.json", draft)
    save_json(output / "news.json", {"synthetic": True})
    save_json(output / "config.json", config)
    prepare_review(output)
    manifest = read_json(output / "manifest.json")["files"]
    assert all(name in manifest for name in info["audio_files"])
    review = output / "REVIEW.md"
    assert review.read_text().count("- [ ]") == 6
    assert "라이선스" in review.read_text()
    review.write_text(review.read_text().replace("- [ ]", "- [x]"))
    approve(output)
    require_approval(output)
    audio_path = output / info["audio_files"][0]
    audio_path.write_bytes(b"changed")
    with pytest.raises(ValueError, match="검수 대상"):
        require_approval(output)


def test_audio_missing_unsupported_and_plugin_failures(config, draft, tmp_path, monkeypatch):
    config["reel"]["narration"] = str(tmp_path / "absent.mp3")
    with pytest.raises(ValueError, match="mp3/wav"):
        prepare_audio(draft, config, tmp_path)
    config["reel"].update(tts="plugin", tts_plugin="bad", narration=None)
    with pytest.raises(ValueError, match="형식"):
        prepare_audio(draft, config, tmp_path)
    module = types.ModuleType("empty_voice")
    module.synthesize = lambda **kwargs: None
    monkeypatch.setitem(sys.modules, "empty_voice", module)
    config["reel"]["tts_plugin"] = "empty_voice:synthesize"
    (tmp_path / "audio").mkdir(exist_ok=True)
    (tmp_path / "audio" / "narration.wav").write_bytes(b"stale audio")
    with pytest.raises(ValueError, match="생성하지"):
        prepare_audio(draft, config, tmp_path)
    config["reel"]["tts_plugin"] = "nonexistent_voice:synthesize"
    with pytest.raises(ValueError, match="실행 실패"):
        prepare_audio(draft, config, tmp_path)
    config["reel"]["narration"] = "user.wav"
    with pytest.raises(ValueError, match="하나만"):
        prepare_audio(draft, config, tmp_path)


def video_frame(path, second):
    raw = subprocess.run([ffmpeg_exe(), "-v", "error", "-ss", str(second), "-i", str(path), "-frames:v", "1",
                          "-f", "rawvideo", "-pix_fmt", "rgb24", "pipe:1"], capture_output=True, check=True).stdout
    return Image.frombytes("RGB", (1080, 1920), raw)


def test_bundled_video_has_real_motion_and_silent_audio():
    path = ROOT / "samples" / "reel.mp4"
    early, later = video_frame(path, 0.25), video_frame(path, 2)
    assert ImageChops.difference(early.crop((80, 200, 1000, 1350)), later.crop((80, 200, 1000, 1350))).getbbox()
    assert ImageChops.difference(early.crop((90, 1450, 990, 1710)), later.crop((90, 1450, 990, 1710))).getbbox()
    assert ImageChops.difference(early.crop((90, 1810, 990, 1818)), later.crop((90, 1810, 990, 1818))).getbbox()
    boundary = video_frame(path, 4)
    assert sum(boundary.resize((1, 1)).getpixel((0, 0))) < sum(later.resize((1, 1)).getpixel((0, 0))) / 3
    assert audio_rms(path) < 2
