"""날짜별 생성의 OS 예약 등록·확인·삭제 안내만 출력한다. 등록은 실행하지 않는다."""
import argparse
from pathlib import Path, PureWindowsPath
import re
import shlex
from subprocess import list2cmdline
import sys

from common import ROOT, cli
from daily import default_config, kit_path


def instructions(os_name, time, python=None, config=None, output_root=None):
    if os_name not in ("windows", "macos", "linux"):
        raise ValueError("--os는 windows/macos/linux 중 하나여야 합니다.")
    if not re.fullmatch(r"(?:[01]\d|2[0-3]):[0-5]\d", time):
        raise ValueError("--time은 00:00~23:59의 HH:MM 형식이어야 합니다.")
    python = python or sys.executable
    values = [python, config, output_root]
    if any(any(ord(char) < 32 or ord(char) == 127 for char in str(value)) for value in values if value is not None):
        raise ValueError("명령 인자에 줄바꿈·제어 문자를 넣을 수 없습니다.")
    if not Path(python).is_absolute() and not (os_name == "windows" and PureWindowsPath(python).is_absolute()):
        raise ValueError("--python에는 가상환경 Python 실행 파일의 절대 경로를 입력하세요.")
    output = kit_path(output_root or ROOT / "output" / "daily")
    config_path = kit_path(config) if config else default_config()
    heading = ("안내만 생성했습니다. 아래 등록 명령은 직접 확인한 뒤 실행하세요.\n"
               "컴퓨터의 현지 시간 기준이며 컴퓨터가 켜져 있어야 합니다. 생성 후 검수 대기에서 멈춥니다.\n"
               f"로그: {output / 'daily.log'}\n"
               "기존 날짜 폴더는 덮어쓰지 않습니다. 로그의 오류와 날짜별 REVIEW.md를 확인하세요.\n")
    if os_name == "windows":
        def compact(path):
            # daily.py가 키트 기준으로 해석하므로 작업 스케줄러의 cwd와 무관하다.
            try:
                return str(path.relative_to(ROOT))
            except ValueError:
                return str(path)
        args = [str(python), str(ROOT / "daily.py"), "--config", compact(config_path)]
        if output != kit_path(ROOT / "output" / "daily"):
            args.extend(["--output-root", compact(output)])
        args.extend(["--log", compact(output / "daily.log")])
        # cmd.exe의 환경변수 확장·메타 문자 해석은 list2cmdline이 방어하지 않는다.
        if any(any(char in argument for char in '%!"&|<>^') for argument in args):
            raise ValueError('Windows 경로에는 % ! " & | < > ^를 사용할 수 없습니다. 다른 폴더로 옮겨 다시 만드세요.')
        task = list2cmdline(args)
        # 이 키트에서는 보수적인 상한을 적용하고 짧은 명령만 안내한다.
        if len(task) > 261:
            raise ValueError("Windows예약 명령이 키트의 보수적인 261문자 상한을 넘었습니다. "
                             r"키트를 C:\shorts 같은 짧은 경로로 옮기고 Python·외부 파일 경로도 짧게 한 뒤 안내를 재생성하세요.")
        create = list2cmdline(["schtasks", "/Create", "/SC", "DAILY", "/ST", time,
                              "/TN", "ShortsBookDaily", "/TR", task])
        return (heading + "PowerShell에서 cmd.exe를 입력해 명령 프롬프트로 바꾼 뒤 아래 명령을 실행하세요.\n"
                "등록 (같은 이름의 기존 작업은 자동 교체하지 않습니다):\n" + create + "\n"
                "확인:\nschtasks /Query /TN ShortsBookDaily /V /FO LIST\n"
                "수동 실행 (오늘 폴더가 이미 있으면 중복 오류가 정상입니다):\nschtasks /Run /TN ShortsBookDaily\n"
                "삭제:\nschtasks /Delete /TN ShortsBookDaily\n")
    args = [str(python), str(ROOT / "daily.py"), "--config", str(config_path),
            "--output-root", str(output), "--log", str(output / "daily.log")]
    hour, minute = map(int, time.split(":"))
    # cron은 셸 인용 내부에서도 %를 먼저 해석하므로 셸 인용 후 이스케이프한다.
    command = shlex.join(args).replace("%", r"\%")
    return (heading + "등록: crontab -e 를 열고 아래 한 줄만 추가해 저장하세요.\n"
            f"{minute} {hour} * * * {command}\n"
            "확인:\ncrontab -l\n"
            "수동 실행 (터미널에 붙여넣기):\n" + shlex.join(args) + "\n"
            "삭제: crontab -e 를 열어 위 ShortsBook daily.py 실행 줄만 지우고 저장하세요.\n"
            "다른 예약은 유지하세요. macOS에서 권한 오류가 나면 시스템 설정의 개인정보 보호에서 터미널 권한을 확인하세요.\n")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--os", choices=("windows", "macos", "linux"), required=True)
    parser.add_argument("--time", required=True, help="현지 시각 HH:MM")
    parser.add_argument("--python", default=sys.executable, help="가상환경 Python 절대 경로. 기본: 현재 실행 파일")
    parser.add_argument("--config")
    parser.add_argument("--output-root")
    args = parser.parse_args()
    print(instructions(args.os, args.time, args.python, args.config, args.output_root))


if __name__ == "__main__":
    cli(main)
