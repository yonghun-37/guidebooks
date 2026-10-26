import json
from pathlib import Path
import shutil

import pytest
import yaml

from common import ROOT, load_config, read_json, save_json
import daily
from render import ffmpeg, probe
from review import CHECKS, approve, require_approval
from run_pipeline import run, render_output
from schedule_setup import instructions
import upload
import write_script


@pytest.fixture(scope="module")
def rendered(tmp_path_factory):
    folder = tmp_path_factory.mktemp("shorts") / "first"
    run(folder, offline=True)
    return folder


@pytest.fixture
def output(rendered, tmp_path):
    folder = tmp_path / "working"
    shutil.copytree(rendered, folder)
    return folder


def mark_and_approve(output):
    script = read_json(output / "script.json")
    script["selfDeclaredMadeForKids"] = False
    script["containsSyntheticMedia"] = False
    save_json(output / "script.json", script)
    from review import prepare_review
    prepare_review(output)
    path = output / "REVIEW.md"
    path.write_text(path.read_text().replace("- [ ]", "- [x]"), encoding="utf-8")
    approve(output)


def test_offline_full_output(rendered):
    info = probe(rendered / "short.mp4")
    assert info == {"duration": 36.0, "video_codec": "h264", "size": [1080, 1920], "fps": 30.0, "audio_codec": "aac"}
    srt = (rendered / "subtitles.srt").read_text()
    assert "00:00:00,000 --> 00:00:12,000" in srt
    assert "00:00:24,000 --> 00:00:36,000" in srt
    assert "자주 쓰는 물건" in srt
    assert not (rendered / "APPROVED.json").exists()
    # 실제 전체 디코딩으로 프레임 손상과 오디오 누락을 확인한다.
    ffmpeg(["-i", str(rendered / "short.mp4"), "-f", "null", "-"])
    # 자막 검정 배경·흰 글자가 실제 영상에 구워졌는지 프레임에서 확인한다.
    from PIL import Image
    frame = rendered / "decoded.png"
    ffmpeg(["-ss", "1", "-i", str(rendered / "short.mp4"), "-frames:v", "1", str(frame)])
    with Image.open(frame) as image:
        crop = image.crop((90, 1398, 900, 1500)).convert("L")
        assert crop.getextrema()[0] < 30 and crop.getextrema()[1] > 220
    frame.unlink()


def test_approval_requires_checks_and_decisions(output):
    with pytest.raises(ValueError, match="여섯 칸"):
        approve(output)
    p = output / "REVIEW.md"
    p.write_text(p.read_text().replace("- [ ]", "- [x]"), encoding="utf-8")
    with pytest.raises(ValueError, match="null"):
        approve(output)
    mark_and_approve(output)
    require_approval(output)
    (output / "subtitles.srt").write_text("변경", encoding="utf-8")
    with pytest.raises(ValueError, match="바뀌"):
        require_approval(output)


def test_dry_run_needs_no_credentials_and_no_network(output):
    mark_and_approve(output)
    result = upload.upload(output)
    assert result["network_calls"] == 0
    assert result["metadata"]["status"] == {"privacyStatus": "private", "selfDeclaredMadeForKids": False, "containsSyntheticMedia": False}
    assert [r["method"] for r in result["requests"]] == ["POST", "PUT", "PUT"]
    assert "isShorts" not in result["metadata"]
    assert "[Y037]" in result["quota"] and "[Y086]" in result["private_lock"]
    assert not (output / "upload-session.json").exists()
    with pytest.raises(ValueError, match="모두 필요"):
        upload.upload(output, live=True, client_path=output / "missing", token_path=output / "missing-token")


def test_failed_rerender_invalidates_old_approval(output):
    mark_and_approve(output)
    (output / "script.json").write_text("{}", encoding="utf-8")
    with pytest.raises(ValueError):
        render_output(output)
    assert not (output / "APPROVED.json").exists()
    with pytest.raises(ValueError, match="REVIEW"):
        require_approval(output)


def test_manifest_cannot_omit_video(output):
    mark_and_approve(output)
    approved = read_json(output / "APPROVED.json")
    del approved["files"]["short.mp4"]
    save_json(output / "APPROVED.json", approved)
    with pytest.raises(ValueError, match="목록"):
        require_approval(output)


@pytest.mark.parametrize("key,value", [("selfDeclaredMadeForKids", "false"), ("containsSyntheticMedia", 0), ("privacyStatus", "friends"), ("hooks", []), ("hashtags", ["#two words"]), ("scenes", []), ("title", "<제목>"), ("description", "가" * 2000)])
def test_script_input_validation(key, value):
    script = write_script.example(36)
    script[key] = value
    with pytest.raises(ValueError):
        write_script.validate(script)


def test_duration_boundaries():
    write_script.validate(write_script.example(180))
    with pytest.raises(ValueError, match="최대 3분"):
        write_script.validate(write_script.example(181))
    script = write_script.example(36)
    script["scenes"][0]["duration"] = float("nan")
    with pytest.raises(ValueError):
        write_script.validate(script)


def test_prompt_paste_and_api_gate(tmp_path):
    config = load_config()
    write_script.generate(config, tmp_path, "prompt")
    text = (tmp_path / "prompt.md").read_text()
    assert "질문형·결과 먼저·행동 제안형" in text
    assert "hashtags" in text and "narration" in text
    assert not (tmp_path / "script.json").exists()
    with pytest.raises(ValueError, match="allow-api"):
        write_script.generate(config, tmp_path, "api")
    config["llm"]["mode"] = "api"
    with pytest.raises(ValueError, match="LLM_BASE_URL"):
        write_script.generate(config, tmp_path, "api", True)


def test_api_response_mock(monkeypatch, tmp_path):
    import io
    script = write_script.example(36)
    for k, value in {"LLM_BASE_URL": "https://example.invalid/v1", "LLM_API_KEY": "test-placeholder", "LLM_MODEL": "user-model"}.items():
        monkeypatch.setenv(k, value)
    def response(request, timeout):
        assert request.full_url == "https://example.invalid/v1/chat/completions"
        assert timeout == 60
        return io.StringIO(json.dumps({"choices": [{"finish_reason": "stop", "message": {"content": json.dumps(script)}}]}))
    monkeypatch.setattr(write_script, "urlopen", response)
    assert write_script.generate(load_config(), tmp_path, "api", True) == script


def test_api_error_hides_secrets(monkeypatch, tmp_path):
    monkeypatch.setenv("LLM_BASE_URL", "https://example.invalid/v1")
    monkeypatch.setenv("LLM_API_KEY", "do-not-print-this")
    monkeypatch.setenv("LLM_MODEL", "test")
    def fail(*args, **kwargs):
        raise OSError("do-not-print-this")
    monkeypatch.setattr(write_script, "urlopen", fail)
    with pytest.raises(ValueError) as error:
        write_script.generate(load_config(), tmp_path, "api", True)
    assert "do-not-print-this" not in str(error.value)


def test_missing_audio_and_unlicensed_music(tmp_path):
    config = yaml.safe_load((ROOT / "config.example.yaml").read_text())
    config["font"] = str(ROOT / "assets/fonts/NotoSansKR.ttf")
    config["video"]["narration"] = "missing.wav"
    path = tmp_path / "config.yaml"
    path.write_text(yaml.safe_dump(config))
    with pytest.raises(ValueError, match="narration"):
        load_config(path)
    config["video"]["narration"] = None
    config["video"]["music"] = "music.wav"
    (tmp_path / "music.wav").write_bytes(b"test")
    path.write_text(yaml.safe_dump(config))
    with pytest.raises(ValueError, match="음악 사용 전"):
        load_config(path)


def test_user_clip_photo_recording_music_and_split_captions(tmp_path):
    from PIL import Image
    assets = tmp_path / "inputs"
    assets.mkdir()
    Image.new("RGB", (640, 480), "#008060").save(assets / "02.jpg")
    ffmpeg(["-f", "lavfi", "-i", "color=c=navy:s=640x360:r=24", "-t", "0.5", "-an", "-c:v", "libx264", "-threads", "1", str(assets / "01.mp4")])
    ffmpeg(["-f", "lavfi", "-i", "sine=frequency=440:duration=2", str(tmp_path / "voice.wav")])
    ffmpeg(["-f", "lavfi", "-i", "sine=frequency=220:duration=1", str(tmp_path / "music.wav")])
    (tmp_path / "license.txt").write_text("자체 생성 시험 음원", encoding="utf-8")
    config = yaml.safe_load((ROOT / "config.example.yaml").read_text())
    config["font"] = str(ROOT / "assets/fonts/NotoSansKR.ttf")
    config["video"].update({"duration": 2, "narration": "voice.wav", "music": "music.wav", "scenes_dir": "inputs"})
    config["rights"].update({"scenes": "직접 생성 시험 영상·사진", "narration": "자체 생성 시험음", "music": {"confirmed": True, "source": "시험 코드", "license": "자체 생성", "evidence": "license.txt", "attribution": "자체 생성 음악"}})
    path = tmp_path / "config.yaml"
    path.write_text(yaml.safe_dump(config, allow_unicode=True))
    out = tmp_path / "mixed"
    out.mkdir()
    script = write_script.example(2)
    script["scenes"] = script["scenes"][:2]
    for scene in script["scenes"]:
        scene["duration"] = 1
        scene["subtitle"] = "자막을 여러 줄로 나누어 읽고 다음 문장이 나오는 시간을 직접 확인해 보세요."
    script["description"] += " 자체 생성 음악"
    save_json(out / "script.json", script)
    render_output(out, path)
    info = read_json(out / "video-info.json")
    assert len(info["sources"]) == 2 and set(info["audio"]) == {"narration", "music"}
    assert info["duration"] == 2
    assert (out / "subtitles.srt").read_text().count(" --> ") > 2
    result = __import__("subprocess").run([__import__("imageio_ffmpeg").get_ffmpeg_exe(), "-i", str(out / "short.mp4"), "-af", "volumedetect", "-f", "null", "-"], capture_output=True, text=True)
    assert "mean_volume: -inf" not in result.stderr and "mean_volume:" in result.stderr
    # 녹음을 영상보다 길게 잘라 숨기지 않는다.
    script["scenes"] = script["scenes"][:1]
    save_json(out / "script.json", script)
    with pytest.raises(ValueError, match="녹음이 영상보다"):
        render_output(out, path)


def test_daily_always_offline_duplicate_date_and_schedule(monkeypatch, tmp_path):
    calls = []
    def fake_run(output, **kwargs):
        calls.append(kwargs)
        output.mkdir(parents=True)
    monkeypatch.setattr(daily.run_pipeline, "run", fake_run)
    result = daily.generate("2026-10-26", output_root=tmp_path)
    assert calls[0]["offline"] and not calls[0]["allow_api"]
    with pytest.raises(ValueError, match="덮어쓰지"):
        daily.generate("2026-10-26", output_root=tmp_path)
    with pytest.raises(ValueError, match="실제 날짜"):
        daily.generate("2026-02-30", output_root=tmp_path)
    assert result.name == "2026-10-26"
    text = instructions("macos", "09:30", python="/tmp/test env/bin/python")
    assert "30 9 * * *" in text and "--live" not in text
    win = instructions("windows", "09:30", python=r"C:\s\.venv\Scripts\python.exe")
    assert "ShortsBookDaily" in win and "/Delete" in win
    for os_name, clock in [("windows", "24:00"), ("wrong", "09:30")]:
        with pytest.raises(ValueError):
            instructions(os_name, clock)


def test_published_sample_size_and_spec():
    samples = ROOT / "samples"
    assert sum(p.stat().st_size for p in samples.rglob("*") if p.is_file()) <= 10_000_000
    assert probe(samples / "short.mp4")["size"] == [1080, 1920]
    assert not (samples / "APPROVED.json").exists()
    write_script.validate(read_json(samples / "script.json"))
