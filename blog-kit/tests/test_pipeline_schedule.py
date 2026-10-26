from pathlib import Path
import subprocess
import sys
import pytest
import brief
import daily
import render
import review
import publish
from common import ROOT, load_config
from schedule_setup import instructions


def test_full_offline_pipeline(tmp_path):
    output = daily.run("2026-10-26", output_root=tmp_path)
    assert all((output / name).is_file() for name in ("brief.md", "materials.md", "draft.md", "daily-config.json"))
    assert not (output / "editor.html").exists()
    # 사람 작성 단계는 샘플 복사로 대체한다. 외부 서비스가 없어도 완주한다.
    (output / "draft.md").write_text((ROOT / "samples/article.md").read_text().replace("(support-check.svg)", "(https://example.invalid/image.svg)"))
    daily.run("2026-10-26", output_root=tmp_path, resume=True)
    assert (output / "report.md").is_file()
    assert not (output / "APPROVED.json").exists()
    review_path = output / "REVIEW.md"
    review_path.write_text(review_path.read_text().replace("- [ ]", "- [x]"))
    review.approve(output)
    assert publish.publish(output, "blogger")["state"] == "draft"
    with pytest.raises(ValueError, match="이미 있는 날짜"):
        daily.run("2026-10-26", output_root=tmp_path)


@pytest.mark.parametrize("kind", ["정보", "후기", "경험"])
def test_prompt_formulas_and_type_inputs(kind):
    config = load_config()
    config["article_type"] = kind
    result = brief.build(config, "나의 자료")
    for section in ("검색 의도", "개요", "초안", "사실 확인", "제목 3안", "요약·FAQ", "썸네일", "[과제]", "[독자]", "[내 자료/근거]", "[제약]", "[출력 형식]", "[검수 기준]"):
        assert section in result
    assert "나의 자료" in result and brief.INPUTS[kind] in result


@pytest.mark.parametrize("day", ["../../x", "2026-02-30", "2026-1-01", "2026-13-01"])
def test_bad_dates(day, tmp_path):
    with pytest.raises(ValueError):
        daily.run(day, output_root=tmp_path)


def test_resume_without_start(tmp_path):
    with pytest.raises(ValueError):
        daily.run("2026-10-26", output_root=tmp_path, resume=True)


@pytest.mark.parametrize("os_name", ["windows", "macos", "linux"])
def test_schedule_instructions_only(os_name, tmp_path):
    result = instructions(os_name, "20:30", config=str(ROOT / "config.example.json"), output_root=None if os_name == "windows" else tmp_path)
    assert "--live" not in result and "publish.py" not in result
    assert "daily.py" in result and "--resume" in result
    if os_name == "windows":
        assert "BlogBookDaily" in result and "/Delete" in result
    else:
        assert "30 20 * * *" in result and "crontab -l" in result


@pytest.mark.parametrize("kwargs", [{"time": "24:01"}, {"python": "relative/python"}, {"output_root": "bad\nargument"}])
def test_invalid_schedule_args(kwargs):
    values = {"os_name": "linux", "time": "20:30", **kwargs}
    with pytest.raises(ValueError):
        instructions(**values)


def test_cron_percent_and_windows_shell_metacharacters(tmp_path):
    assert r"\%" in instructions("macos", "09:00", output_root=tmp_path / "50% space")
    with pytest.raises(ValueError):
        instructions("windows", "09:00", output_root=tmp_path / "bad&path")


def test_cli_can_run_outside_kit_and_logs_duplicate(tmp_path):
    command = [sys.executable, str(ROOT / "daily.py"), "--date", "2026-10-26", "--output-root", str(tmp_path / "out"), "--log", str(tmp_path / "daily.log")]
    first = subprocess.run(command, cwd=tmp_path, capture_output=True, text=True)
    assert first.returncode == 0 and "작성 대기" in (tmp_path / "daily.log").read_text()
    second = subprocess.run(command, cwd=tmp_path, capture_output=True, text=True)
    assert second.returncode == 1 and "이미 있는 날짜" in (tmp_path / "daily.log").read_text()


@pytest.mark.parametrize("content", ['[]', 'null', '"wrong"'])
def test_non_object_config_reports_helpful_error(tmp_path, content):
    path = tmp_path / "config.json"
    path.write_text(content)
    with pytest.raises(ValueError, match="중괄호"):
        load_config(path)
