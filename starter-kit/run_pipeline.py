"""소재 → 문안 → 카드 → 릴스 → 사람 승인 → 드라이런 게시."""
import argparse
from datetime import datetime
from pathlib import Path
import sys

from common import ROOT, cli, load_config, read_json, save_json
from fetch_news import fetch
from make_reel import make_reel
from publish import publish
from render_cards import render_cards
from review import approve, prepare_review
from write_copy import generate_copy, validate_copy


def render(output):
    output = Path(output).resolve()
    config = read_json(output / "config.json")
    # 재생성 시작 즉시 기존 승인을 무효화한다. 렌더링 실패 때도 게시를 허용하지 않는다.
    (output / "APPROVED.json").unlink(missing_ok=True)
    copy = validate_copy(read_json(output / "copy.json"), read_json(output / "news.json"))
    cards = render_cards(copy, config, output / "cards")
    make_reel(copy, config, cards, output)
    prepare_review(output)
    print(f"검수 대기: {output / 'REVIEW.md'}")


def run(output, config_path=None, feeds=None, offline=True, allow_api=False):
    output = Path(output).resolve()
    config = load_config(config_path)
    if offline and (config["llm"]["mode"] == "api" or config["reel"]["tts"] == "plugin"):
        raise ValueError("오프라인 실행에서는 LLM API와 TTS 플러그를 사용할 수 없습니다.")
    news = fetch(feeds or config["rss"], offline=offline)
    output.mkdir(parents=True, exist_ok=False)
    save_json(output / "config.json", config)
    save_json(output / "news.json", news)
    copy = generate_copy(news, config, output / "copy.json", allow_api=allow_api)
    if copy is None:
        print(f"문안 대기: 답변 JSON 저장·검증 후 python run_pipeline.py render {output}")
        return output
    render(output)
    return output


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    commands = parser.add_subparsers(dest="command", required=True)
    create = commands.add_parser("run", help="생성 후 검수 대기에서 종료")
    create.add_argument("--config")
    create.add_argument("--output", type=Path, default=ROOT / "output" / datetime.now().strftime("%Y-%m-%d"))
    create.add_argument("--feed", action="append")
    network = create.add_mutually_exclusive_group()
    network.add_argument("--offline", action="store_true", help="기본값. 외부 요청 금지")
    network.add_argument("--online", action="store_true", help="RSS URL 및 설정에서 선택한 TTS 허용. LLM API는 --allow-api도 필요")
    create.add_argument("--allow-api", action="store_true", help="llm.mode=api일 때만 LLM 호출 명시 허용")
    for command in ("render", "approve"):
        sub = commands.add_parser(command)
        sub.add_argument("output", type=Path)
    argv = sys.argv[1:]
    if not argv or argv[0].startswith("-"):
        argv.insert(0, "run")
    args = parser.parse_args(argv)
    if args.command == "run":
        run(args.output, args.config, args.feed, offline=not args.online, allow_api=args.allow_api)
    elif args.command == "render":
        render(args.output)
    else:
        approve(args.output)
        publish(args.output)  # 승인 명령은 언제나 드라이런. live 옵션을 받지 않는다.


if __name__ == "__main__":
    cli(main)
