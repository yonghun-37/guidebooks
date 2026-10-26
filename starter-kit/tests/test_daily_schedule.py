"""날짜별 생성과 실제 등록 없는 예약 명령의 계약."""
from datetime import date
from pathlib import Path
import shlex
import subprocess
import sys

import pytest

import daily
import schedule_setup


def test_daily_uses_local_today_and_kit_root_from_other_cwd(tmp_path, monkeypatch):
    kit = tmp_path / "kit with spaces"
    kit.mkdir()
    (kit / "config.yaml").write_text("selected")
    monkeypatch.setattr(daily, "ROOT", kit)
    monkeypatch.chdir(tmp_path)
    class Today(date):
        @classmethod
        def today(cls):
            return cls(2026, 10, 27)
    monkeypatch.setattr(daily, "date", Today)
    calls = []
    monkeypatch.setattr(daily.run_pipeline, "run", lambda *a, **kw: calls.append((a, kw)))
    output = daily.generate()
    assert output == kit / "output/daily/2026-10-27"
    assert calls == [((output,), {"config_path": kit / "config.yaml", "feeds": None,
                                  "offline": True, "allow_api": False})]


def test_daily_date_feed_and_config_paths_are_relative_to_kit(tmp_path, monkeypatch):
    monkeypatch.setattr(daily, "ROOT", tmp_path)
    calls = []
    monkeypatch.setattr(daily.run_pipeline, "run", lambda *a, **kw: calls.append((a, kw)))
    output = daily.generate("2026-10-28", "my config.yaml", ["my feed.xml"], "custom daily")
    assert output == tmp_path / "custom daily/2026-10-28"
    assert calls[0][1]["config_path"] == tmp_path / "my config.yaml"
    assert calls[0][1]["feeds"] == [str(tmp_path / "my feed.xml")]


def test_daily_default_config_snapshot_and_no_approve_publish(tmp_path, monkeypatch):
    monkeypatch.setattr(daily, "ROOT", tmp_path)
    calls = []
    monkeypatch.setattr(daily.run_pipeline, "run", lambda *a, **kw: calls.append(kw))
    def forbidden(*a, **kw):
        pytest.fail("예약 생성이 승인 또는 게시를 호출함")
    monkeypatch.setattr(daily.run_pipeline, "approve", forbidden)
    monkeypatch.setattr(daily.run_pipeline, "publish", forbidden)
    daily.generate("2026-10-26")
    assert calls[0]["config_path"] == tmp_path / "config.example.yaml"


def test_daily_refuses_existing_day_before_any_work(tmp_path, monkeypatch):
    monkeypatch.setattr(daily, "ROOT", tmp_path)
    output = tmp_path / "output/daily/2026-10-26"
    output.mkdir(parents=True)
    sentinel = output / "copy.json"
    sentinel.write_text("keep")
    monkeypatch.setattr(daily.run_pipeline, "run", lambda *a, **kw: pytest.fail("기존 날짜 실행"))
    with pytest.raises(ValueError, match="--date"):
        daily.generate("2026-10-26")
    assert sentinel.read_text() == "keep"


@pytest.mark.parametrize("value", ["2026-02-30", "2026-1-2", "../../bad", "2026-10-26\n"])
def test_daily_rejects_bad_dates(value):
    with pytest.raises(ValueError, match="YYYY-MM-DD"):
        daily.generate(value)


def test_daily_preserves_failure_and_cli_log(tmp_path, monkeypatch):
    def failed(*a, **kw):
        raise ValueError("생성 실패 테스트")
    monkeypatch.setattr(daily.run_pipeline, "run", failed)
    monkeypatch.setattr(sys, "argv", ["daily.py", "--date", "2026-10-26", "--log", str(tmp_path / "logs/daily.log")])
    with pytest.raises(SystemExit) as error:
        daily.main()
    assert error.value.code == 1
    assert "생성 실패 테스트" in (tmp_path / "logs/daily.log").read_text()


@pytest.mark.parametrize("os_name", ["linux", "macos"])
def test_cron_round_trips_space_quote_and_percent_paths(tmp_path, monkeypatch, os_name):
    kit = tmp_path / "kit with space's 10%"
    monkeypatch.setattr(daily, "ROOT", kit)
    monkeypatch.setattr(schedule_setup, "ROOT", kit)
    text = schedule_setup.instructions(os_name, "09:05", "/opt/python space/bin/python", "my config.yaml", ["feed 100%.xml"], "my output")
    line = next(line for line in text.splitlines() if line.startswith("5 9 * * * "))
    args = shlex.split(line.split(" ", 5)[5].replace(r"\%", "%"))
    assert args[:2] == ["/opt/python space/bin/python", str(kit / "daily.py")]
    assert args[args.index("--config") + 1] == str(kit / "my config.yaml")
    assert args[args.index("--feed") + 1] == str(kit / "feed 100%.xml")
    assert args[args.index("--log") + 1] == str(kit / "my output/daily.log")
    assert r"10\%" in line
    assert "crontab -l" in text and "crontab -e" in text
    assert "삭제" in text and "검수" in text


def test_windows_nested_quoting_and_lifecycle_without_registration(tmp_path, monkeypatch):
    monkeypatch.setattr(schedule_setup, "ROOT", tmp_path / "kit with spaces")
    monkeypatch.setattr(daily, "ROOT", tmp_path / "kit with spaces")
    def forbidden(*a, **kw):
        pytest.fail("예약 명령 생성 중 subprocess 실행")
    monkeypatch.setattr(subprocess, "run", forbidden)
    monkeypatch.setattr(subprocess, "Popen", forbidden)
    text = schedule_setup.instructions("windows", "23:59", r"C:\Program Files\Python311\python.exe", "my config.yaml")
    create = next(line for line in text.splitlines() if line.startswith("schtasks /Create"))
    assert '/SC DAILY /ST 23:59 /TN ReelsBookDaily /TR ' in create
    assert r'\"C:\Program Files\Python311\python.exe\"' in create
    assert r'\"' + str(tmp_path / "kit with spaces/daily.py") + r'\"' in create
    assert "--log" in create
    assert 'schtasks /Query /TN ReelsBookDaily /V /FO LIST' in text
    assert 'schtasks /Delete /TN ReelsBookDaily' in text
    assert "/F" not in create  # 이미 있는 작업을 덮어쓰지 않는다.
    assert "PowerShell" in text and "cmd.exe" in text


@pytest.mark.parametrize("time", ["24:00", "12:60", "9:00", "09:00\nsurprise", ""])
def test_schedule_rejects_invalid_time(time):
    with pytest.raises(ValueError, match="HH:MM"):
        schedule_setup.instructions("linux", time, "/usr/bin/python3")


@pytest.mark.parametrize("kwargs", [
    {"python": "python"}, {"config": "config\nattack.yaml"},
    {"feeds": ["feed\rattack.xml"]}, {"output_root": "bad\x00path"},
    {"os_name": "other"},
])
def test_schedule_rejects_unsafe_inputs(kwargs):
    params = {"os_name": "linux", "time": "09:00", "python": "/usr/bin/python3"}
    params.update(kwargs)
    with pytest.raises(ValueError):
        schedule_setup.instructions(**params)


@pytest.mark.parametrize("path", [r"C:\bad%PATH%\python.exe", r"C:\bad!x\python.exe", r'C:\bad"quote\python.exe'])
def test_windows_rejects_cmd_expansion_characters(path):
    with pytest.raises(ValueError):
        schedule_setup.instructions("windows", "09:00", path)


def test_schedule_cli_prints_only_and_freezes_default_config(tmp_path, monkeypatch, capsys):
    monkeypatch.setattr(daily, "ROOT", tmp_path)
    monkeypatch.setattr(schedule_setup, "ROOT", tmp_path)
    monkeypatch.setattr(sys, "argv", ["schedule_setup.py", "--os", "linux", "--time", "09:00"])
    schedule_setup.main()
    stdout = capsys.readouterr().out
    assert str(tmp_path / "config.example.yaml") in stdout
    assert "--offline" not in stdout  # daily는 언제나 오프라인이며 옵션으로 해제할 수 없다.
    assert list(tmp_path.iterdir()) == []


def test_daily_rejects_url_feed_instead_of_making_it_a_local_path(monkeypatch):
    monkeypatch.setattr(daily.run_pipeline, "run", lambda *a, **kw: pytest.fail("URL을 로컬 경로로 바꿈"))
    with pytest.raises(ValueError, match="로컬"):
        daily.generate("2099-01-01", feeds=["https://example.invalid/feed.xml"])


def test_schedule_rejects_url_feed_in_offline_task():
    with pytest.raises(ValueError, match="로컬"):
        schedule_setup.instructions("linux", "09:00", "/usr/bin/python3", feeds=["https://example.invalid/feed.xml"])


def test_windows_python_requires_drive_or_unc_absolute_path():
    with pytest.raises(ValueError, match="절대 경로"):
        schedule_setup.instructions("windows", "09:00", r"\Python311\python.exe")


@pytest.fixture
def windows_paths(monkeypatch):
    from pathlib import PureWindowsPath
    kit = PureWindowsPath(r"C:\Users\Harin\Desktop\guidebooks-main\starter-kit")
    monkeypatch.setattr(schedule_setup, "ROOT", kit)
    def resolve(path):
        path = PureWindowsPath(path)
        return path if path.is_absolute() else kit / path
    monkeypatch.setattr(schedule_setup, "kit_path", resolve)
    monkeypatch.setattr(schedule_setup, "default_config", lambda: kit / "config.example.yaml")
    calls = []
    original = schedule_setup.list2cmdline
    def capture(args):
        calls.append(list(args))
        return original(args)
    monkeypatch.setattr(schedule_setup, "list2cmdline", capture)
    return kit, calls


def test_windows_desktop_command_is_compact_and_kit_relative(windows_paths):
    kit, calls = windows_paths
    executable = str(kit / ".venv/Scripts/python.exe")
    schedule_setup.instructions("windows", "09:00", executable, feeds=["fixtures/feed.xml"])
    args = calls[0]
    assert args[:2] == [executable, str(kit / "daily.py")]
    assert args[args.index("--config") + 1] == "config.example.yaml"
    assert args[args.index("--feed") + 1] == r"fixtures\feed.xml"
    assert args[args.index("--log") + 1] == r"output\daily\daily.log"
    assert "--output-root" not in args
    assert len(calls[1][-1]) <= 261


def test_windows_internal_custom_output_is_kit_relative(windows_paths):
    kit, calls = windows_paths
    schedule_setup.instructions("windows", "09:00", r"C:\Python311\python.exe",
                                config="my config.yaml", output_root="drafts")
    args = calls[0]
    assert args[args.index("--config") + 1] == "my config.yaml"
    assert args[args.index("--output-root") + 1] == "drafts"
    assert args[args.index("--log") + 1] == r"drafts\daily.log"


def test_windows_external_paths_stay_absolute(windows_paths):
    kit, calls = windows_paths
    schedule_setup.instructions("windows", "09:00", r"C:\Python311\python.exe",
                                config=r"D:\private\config.yaml", feeds=[r"D:\feeds\news.xml"], output_root=r"D:\drafts")
    args = calls[0]
    assert args[args.index("--config") + 1] == r"D:\private\config.yaml"
    assert args[args.index("--feed") + 1] == r"D:\feeds\news.xml"
    assert args[args.index("--output-root") + 1] == r"D:\drafts"
    assert args[args.index("--log") + 1] == r"D:\drafts\daily.log"


@pytest.mark.parametrize("kind", ["python", "external_config"])
def test_windows_long_command_is_rejected_with_relocation_help(windows_paths, kind):
    kit, calls = windows_paths
    kwargs = {"python": r"C:\Python311\python.exe"}
    if kind == "python":
        kwargs["python"] = "C:\\" + "long directory " * 25 + "python.exe"
    else:
        kwargs["config"] = "D:\\" + "long directory " * 25 + "config.yaml"
    with pytest.raises(ValueError, match=r"261.*C:\\reels.*재생성"):
        schedule_setup.instructions("windows", "09:00", **kwargs)
    assert not any(args[0] == "schtasks" for args in calls)
