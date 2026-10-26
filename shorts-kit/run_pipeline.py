"""대본→영상→사람 검수. 기본 실행은 오프라인 초안 생성이다."""
import argparse
import yaml
from pathlib import Path

from common import ROOT, cli, load_config, read_json, save_json
from render import render
from review import approve, invalidate, prepare_review
from write_script import generate, validate


def render_output(output, config_path=None):
    output = Path(output).resolve()
    if (output / "upload-session.json").exists() or (output / "upload-result.json").exists():
        raise ValueError("업로드 기록이 있는 폴더입니다. 새 폴더에서 새 영상을 만드세요. 기존 전송 상태를 보존합니다.")
    # 실패한 재생성을 이전 승인으로 업로드할 수 없게 먼저 무효화한다.
    invalidate(output)
    config = load_config(config_path or output / "config.yaml")
    script = validate(read_json(output / "script.json"))
    (output / "config.yaml").write_text(yaml.safe_dump(config, allow_unicode=True, sort_keys=False), encoding="utf-8")
    save_json(output / "config.json", config)
    render(script, config, output)
    prepare_review(output)
    print(f"영상 생성 완료: {output / 'short.mp4'}\n검수 대기: {output / 'REVIEW.md'}\n미리보기: {output / 'preview.html'}")
    return output


def run(output, config_path=None, offline=False, allow_api=False, mode=None):
    config_path = Path(config_path or ROOT / "config.example.yaml").resolve()
    config = load_config(config_path)
    if offline:
        mode, allow_api = "offline", False
    output = Path(output).resolve()
    output.mkdir(parents=True, exist_ok=False)
    # 재렌더 시에도 원래 설정 기준 상대 경로가 유지되도록 절대 경로로 저장한다.
    (output / "config.yaml").write_text(yaml.safe_dump(config, allow_unicode=True, sort_keys=False), encoding="utf-8")
    script = generate(config, output, mode, allow_api)
    if script is not None:
        return render_output(output)
    return output


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest="command", required=True)
    new = sub.add_parser("run", help="새 폴더에 초안 생성")
    new.add_argument("--output", type=Path, default=ROOT / "output" / "first")
    new.add_argument("--config")
    new.add_argument("--mode", choices=("offline", "prompt", "api"))
    new.add_argument("--allow-api", action="store_true")
    for command in ("render", "validate", "approve"):
        part = sub.add_parser(command)
        part.add_argument("output", type=Path)
        if command == "render":
            part.add_argument("--config", help="지정한 설정으로 다시 출력")
    args = parser.parse_args()
    if args.command == "run":
        run(args.output, args.config, mode=args.mode, allow_api=args.allow_api)
    elif args.command == "render":
        render_output(args.output, args.config)
    elif args.command == "validate":
        validate(read_json(args.output / "script.json"))
        print("대본 형식 확인 완료. 사실·권리·자막 시점은 직접 검수하세요.")
    else:
        approve(args.output)
        from upload import upload
        upload(args.output)
        print("승인 기록·드라이런 완료. 실제 전송하지 않았습니다.")


if __name__ == "__main__":
    cli(main)
