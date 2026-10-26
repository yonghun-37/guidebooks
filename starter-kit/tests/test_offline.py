from pathlib import Path
import socket

import imageio_ffmpeg
from PIL import Image
import pytest

from common import ROOT, load_config, read_json
from fetch_news import fetch
from make_reel import ffmpeg_exe
import publish
from review import approve, require_approval
from run_pipeline import run


@pytest.fixture(scope="module")
def generated(tmp_path_factory):
    output = tmp_path_factory.mktemp("offline") / "2026-10-26"
    # 모듈 fixture 실행 시에도 네트워크 차단이 적용되도록 명시한다.
    with pytest.MonkeyPatch.context() as patch:
        def blocked(*args, **kwargs):
            raise AssertionError("생성 중 외부 네트워크 요청 발생")
        patch.setattr(socket.socket, "connect", blocked)
        patch.setattr(socket, "create_connection", blocked)
        run(output, offline=True)
    return output


def checked_review(output):
    path = output / "REVIEW.md"
    path.write_text(path.read_text(encoding="utf-8").replace("- [ ]", "- [x]"), encoding="utf-8")


def test_offline_end_to_end_waits_then_approves_and_dry_runs(generated, monkeypatch, capsys):
    output = generated
    assert (output / "REVIEW.md").exists()
    assert not (output / "APPROVED.json").exists()
    assert not (output / "dry-run.json").exists()
    assert read_json(output / "news.json")["synthetic"] is True
    with pytest.raises(ValueError, match="검수 대기"):
        publish.publish(output)
    with pytest.raises(ValueError, match="여섯 칸"):
        approve(output)
    checked_review(output)
    approve(output)
    # 토큰이 환경에 있어도 --live가 없으면 요청하지 않는다. 출력에도 토큰이 없어야 한다.
    monkeypatch.setenv("IG_ACCESS_TOKEN", "SECRET_TEST_SENTINEL")
    plan = publish.publish(output)
    stdout = capsys.readouterr().out
    assert "SECRET_TEST_SENTINEL" not in stdout
    assert "Bearer <REDACTED>" in stdout
    assert "컨테이너 생성" in stdout and "상태 확인" in stdout and "게시" in stdout
    assert plan == read_json(output / "dry-run.json")
    steps = plan["requests"]
    assert len(steps) == 16  # 자식 5개의 생성·확인 + 부모 및 릴스 각 3단계
    assert all(s["endpoint"].startswith("https://graph.instagram.com/") for s in steps)
    for index, step in enumerate(steps):
        if step["step"] == "게시":
            assert steps[index - 2]["step"] == "컨테이너 생성"
            assert steps[index - 1]["params"] == {"fields": "status_code"}
            assert steps[index - 1]["until"] == "FINISHED"
            assert "creation_id" in step["params"]
    assert steps[10]["params"]["media_type"] == "CAROUSEL"
    assert "{CHILD_1}" in steps[10]["params"]["children"]
    assert steps[13]["params"]["media_type"] == "REELS"
    assert steps[0]["params"]["image_url"].endswith(".jpg")
    assert steps[13]["params"]["video_url"].endswith("reel.mp4")


def test_card_pixels_and_jpeg(generated):
    cards = sorted((generated / "cards").glob("*.png"))
    assert len(cards) == 5
    for path in cards:
        with Image.open(path) as image:
            assert image.size == (1080, 1350)
            assert image.format == "PNG"
            assert len(image.getcolors(maxcolors=1_000_000)) > 100
        with Image.open(path.with_suffix(".jpg")) as image:
            assert image.size == (1080, 1350) and image.format == "JPEG"


def test_actual_reel_dimensions_duration_codec_and_decode(generated):
    # 생성 시 적은 JSON 대신 실제 MP4를 디코딩하여 검사한다.
    reader = imageio_ffmpeg.read_frames(str(generated / "reel.mp4"), pix_fmt="rgb24")
    try:
        metadata = next(reader)
        assert metadata["size"] == (1080, 1920)
        assert 15 <= metadata["duration"] <= 30
        assert abs(metadata["duration"] - 20) < 0.1
        assert metadata["fps"] == 24
        assert "h264" in metadata["codec"]
        assert metadata["audio_codec"] == "aac"
        frame = next(reader)
        assert len(frame) == 1080 * 1920 * 3
    finally:
        reader.close()
    count, seconds = imageio_ffmpeg.count_frames_and_secs(str(generated / "reel.mp4"))
    assert count == 480 and 19.9 <= seconds <= 20.1
    srt = (generated / "subtitles.srt").read_text(encoding="utf-8")
    assert "00:00:00,000 --> 00:00:04,000" in srt
    assert "00:00:16,000 --> 00:00:20,000" in srt


@pytest.mark.parametrize("name", ["copy.json", "cards/card-01.png", "reel.mp4", "REVIEW.md", "manifest.json"])
def test_approval_rejects_changed_assets(generated, name):
    # 테스트 순서와 무관하게 승인된 기준을 만든다.
    checked_review(generated)
    approve(generated)
    path = generated / name
    original = path.read_bytes()
    try:
        path.write_bytes(original + b" ")
        with pytest.raises(ValueError, match="검수 대상"):
            require_approval(generated)
    finally:
        path.write_bytes(original)


def test_offline_rejects_remote_feed():
    with pytest.raises(ValueError, match="오프라인"):
        fetch(["https://example.invalid/news.xml"], offline=True)


def test_broken_empty_and_unsafe_feed(tmp_path):
    path = tmp_path / "feed.xml"
    for xml in ("<rss>", "<rss><channel/></rss>", '<!DOCTYPE rss [<!ENTITY x "x">]><rss/>'):
        path.write_text(xml, encoding="utf-8")
        with pytest.raises(ValueError):
            fetch([str(path)])


def test_system_ffmpeg_missing_uses_pip_binary(monkeypatch):
    monkeypatch.setattr("make_reel.shutil.which", lambda name: None)
    assert Path(ffmpeg_exe()).is_file()
    assert ".venv" in ffmpeg_exe()


def test_existing_output_not_overwritten(generated):
    before = (generated / "reel.mp4").read_bytes()
    with pytest.raises(FileExistsError):
        run(generated)
    assert (generated / "reel.mp4").read_bytes() == before


def test_failed_rerender_revokes_approval(generated, tmp_path, monkeypatch):
    import shutil
    import run_pipeline
    output = tmp_path / "rerender"
    shutil.copytree(generated, output)
    checked_review(output)
    approve(output)

    def failed(*args, **kwargs):
        raise ValueError("렌더링 실패 테스트")
    monkeypatch.setattr(run_pipeline, "render_cards", failed)
    with pytest.raises(ValueError, match="렌더링 실패 테스트"):
        run_pipeline.render(output)
    with pytest.raises(ValueError, match="검수 대기"):
        require_approval(output)


def test_approve_command_prints_dry_run(generated, monkeypatch, capsys):
    import run_pipeline
    checked_review(generated)
    monkeypatch.setattr("sys.argv", ["run_pipeline.py", "approve", str(generated)])
    run_pipeline.main()
    assert '"mode": "dry-run"' in capsys.readouterr().out


def test_bundled_samples_size_and_dimensions():
    samples = ROOT / "samples"
    assert sum(p.stat().st_size for p in samples.rglob("*") if p.is_file()) <= 10_000_000
    assert len(list(samples.glob("card-*.png"))) == 5
    for path in samples.glob("card-*.png"):
        with Image.open(path) as image:
            assert image.size == (1080, 1350)
    reader = imageio_ffmpeg.read_frames(str(samples / "reel.mp4"))
    try:
        metadata = next(reader)
        assert metadata["size"] == (1080, 1920) and 15 <= metadata["duration"] <= 30
    finally:
        reader.close()


def test_config_rejects_unsupported_voice_and_bad_duration(tmp_path):
    import yaml
    original = yaml.safe_load((ROOT / "config.example.yaml").read_text(encoding="utf-8"))
    original["reel"]["tts"] = "unknown-cloud"
    path = tmp_path / "config.yaml"
    path.write_text(yaml.safe_dump(original), encoding="utf-8")
    with pytest.raises(ValueError, match="silent"):
        load_config(path)
    original["reel"] = {"tts": "silent", "duration": 100}
    path.write_text(yaml.safe_dump(original), encoding="utf-8")
    with pytest.raises(ValueError, match="15~30"):
        load_config(path)
