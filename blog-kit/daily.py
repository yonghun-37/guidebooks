"""매일 프롬프트를 만들고 사람 작성을 기다린다. --resume은 검사·HTML 변환까지 한다."""
import argparse
from contextlib import redirect_stderr, redirect_stdout
from datetime import date, datetime
import re

import brief
import render
from common import ROOT, cli, kit_path, load_config, read_json, save_json, save_text


def default_config():
    return ROOT / ("config.json" if (ROOT / "config.json").is_file() else "config.example.json")


def run(day=None, config=None, output_root=None, resume=False, affiliate=False):
    day = day or date.today().isoformat()
    if not re.fullmatch(r"\d{4}-\d{2}-\d{2}", day):
        raise ValueError("--date는 YYYY-MM-DD 형식의 실제 날짜여야 해요.")
    try:
        date.fromisoformat(day)
    except ValueError:
        raise ValueError("--date는 실제 날짜여야 해요.") from None
    output = kit_path(output_root or ROOT / "output" / "daily") / day
    if resume:
        if not (output / "daily-config.json").is_file():
            raise ValueError("먼저 같은 날짜로 daily.py를 실행해 프롬프트를 만드세요.")
        render.render(output / "draft.md", output, read_json(output / "daily-config.json"), affiliate)
        return output
    settings = load_config(config)
    try:
        output.mkdir(parents=True, exist_ok=False)
    except FileExistsError:
        raise ValueError("이미 있는 날짜 폴더예요. 본문 작성 뒤 --resume으로 이어 가거나 다른 날짜·출력 경로를 고르세요.") from None
    save_json(output / "daily-config.json", settings)
    save_text(output / "brief.md", brief.build(settings))
    save_text(output / "materials.md", "# 내 자료\n\n## 공식 출처\n제목 / URL / 확인일 / 적용 대상 / 실제 확인한 사실\n\n## 내 경험\n날짜 / 실제 행동 / 관찰 / 공개 가능한 사진\n\n## 권리·AI 사용·광고 관계\n파일 / 권리자 / 이용 조건 / 원문 주소 / 확인일\nAI 사용 범위 / 실제 제공·수수료 관계\n\n## 발행 뒤 기록\n공개 URL / 공개 상태 / 확인일 / 첫 유입·변경 메모\n")
    section = {"정보": "원문에서 확인할 내용", "후기": "사용 조건과 장단점", "경험": "내가 한 일과 달라진 점"}[settings["article_type"]]
    save_text(output / "draft.md", f"# {settings['keyword']}\n\n[직접 입력: 독자의 질문에 바로 답하는 문단]\n\n## {section}\n\n[직접 입력: 내 자료와 출처를 대조해 작성]\n\n## 내 경험\n\n[직접 입력: 실제 확인·관찰 메모. 경험을 꾸미지 마세요.]\n\n## 지금 할 일\n\n[직접 입력: 오늘 할 행동]\n")
    print(f"작성 대기: {output / 'draft.md'}")
    print("brief.md를 참고해 직접 쓰고 materials.md를 채우세요. 완료하면 같은 날짜로 --resume을 실행하세요.")
    return output


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--date")
    parser.add_argument("--config")
    parser.add_argument("--output-root")
    parser.add_argument("--resume", action="store_true")
    parser.add_argument("--affiliate", action="store_true")
    parser.add_argument("--log")
    args = parser.parse_args()
    def execute():
        run(args.date, args.config, args.output_root, args.resume, args.affiliate)
    if args.log:
        path = kit_path(args.log)
        path.parent.mkdir(parents=True, exist_ok=True)
        with path.open("a", encoding="utf-8", buffering=1) as stream, redirect_stdout(stream), redirect_stderr(stream):
            print(f"[{datetime.now().isoformat(timespec='seconds')}] 일일 작업 시작")
            cli(execute)
    else:
        execute()


if __name__ == "__main__":
    cli(main)
