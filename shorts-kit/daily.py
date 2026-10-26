"""매일 날짜별 초안을 만들고 사람 검수 대기에서 종료한다. 항상 오프라인이다."""
import argparse
from contextlib import redirect_stderr, redirect_stdout
from datetime import date, datetime
from pathlib import Path
import re

from common import ROOT, cli
import run_pipeline


def kit_path(path):
    """예약 작업의 현재 작업 폴더에 의존하지 않는다."""
    path = Path(path).expanduser()
    return (path if path.is_absolute() else ROOT / path).resolve()


def default_config():
    return ROOT / ("config.yaml" if (ROOT / "config.yaml").is_file() else "config.example.yaml")


def generate(day=None, config=None, output_root=None):
    day = day or date.today().isoformat()
    if not re.fullmatch(r"\d{4}-\d{2}-\d{2}", day):
        raise ValueError("--date는 YYYY-MM-DD 형식의 실제 날짜여야 합니다.")
    try:
        date.fromisoformat(day)
    except ValueError:
        raise ValueError("--date는 YYYY-MM-DD 형식의 실제 날짜여야 합니다.") from None
    output = kit_path(output_root or ROOT / "output" / "daily") / day
    if output.exists():
        raise ValueError(f"이미 있는 날짜 폴더입니다: {output}. 덮어쓰지 않았습니다. "
                         "REVIEW.md를 확인하거나 예행연습은 --date 다른날짜 또는 --output-root 다른폴더를 사용하세요.")
    config = kit_path(config) if config else default_config()
    try:
        run_pipeline.run(output, config_path=config, offline=True, allow_api=False)
    except FileExistsError:
        raise ValueError(f"날짜 폴더가 이미 생겼습니다: {output}. 검수 후 --date 또는 --output-root로 새 경로를 고르세요.") from None
    return output


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--date", help="예행연습 날짜 YYYY-MM-DD. 기본: 컴퓨터의 오늘 날짜")
    parser.add_argument("--config", help="기본: 키트 config.yaml이 있으면 사용, 없으면 config.example.yaml")
    parser.add_argument("--output-root", help="날짜 폴더를 담을 경로. 기본: 키트 output/daily")
    parser.add_argument("--log", help="예약 실행의 출력과 오류를 누적할 파일")
    args = parser.parse_args()
    def execute():
        generate(args.date, args.config, args.output_root)
    if args.log:
        log = kit_path(args.log)
        log.parent.mkdir(parents=True, exist_ok=True)
        with log.open("a", encoding="utf-8", buffering=1) as stream, redirect_stdout(stream), redirect_stderr(stream):
            print(f"\n[{datetime.now().isoformat(timespec='seconds')}] 날짜별 생성 시작")
            cli(execute)
    else:
        execute()


if __name__ == "__main__":
    cli(main)
