"""기존 키트의 파일 해시 검수와 승인 방식을 쇼츠에 적용한다."""
from datetime import datetime, timezone
from pathlib import Path

from common import digest, read_json, save_json
from write_script import validate

CHECKS = [
    "대본의 사실·이름·수치와 원출처를 대조했어요. 가상 예제는 실제 사례로 소개하지 않아요.",
    "short.mp4를 끝까지 재생해 장면 순서·화질·크롭·자막 잘림을 확인했어요.",
    "녹음·무음과 음악을 직접 듣고 말의 시작·끝과 자막 시점을 확인했어요.",
    "장면·화자·음악의 사용권과 표시문구를 확인했어요. 음악 증빙과 설명도 대조했어요.",
    "script.json의 제목·설명·해시태그·공개 범위·아동용·AI 공개 여부를 직접 결정했어요.",
    "이 파일들의 드라이런 요청을 승인해요. 실제 전송은 별도 --live 명령을 실행할 때 해요.",
]


def invalidate(output):
    for name in ("APPROVED.json", "dry-run.json"):
        (Path(output) / name).unlink(missing_ok=True)


def required_files(output):
    output = Path(output)
    files = ["script.json", "config.yaml", "config.json", "short.mp4", "video-info.json", "subtitles.srt", "frames.txt", "preview.html"]
    info = read_json(output / "video-info.json")
    files += list(info.get("audio", {}).values()) if "silent" not in info["audio"] else []
    files += info["rights_files"]
    files += [p.relative_to(output).as_posix() for p in sorted((output / "frames").iterdir()) if p.is_file()]
    return files


def check_files(output, expected):
    output = Path(output).resolve()
    for name, checksum in expected.items():
        path = output / name
        if not path.resolve().is_relative_to(output) or not path.is_file() or digest(path) != checksum:
            raise ValueError(f"검수 대상이 바뀌었습니다: {name}. render 후 다시 승인하세요.")


def prepare_review(output):
    output = Path(output)
    invalidate(output)
    script = validate(read_json(output / "script.json"))
    (output / "REVIEW.md").write_text("# 게시 전 검수\n\n" + script["label"] + "\n\n"
        + "preview.html을 열어 영상을 끝까지 확인한 뒤 아래 칸을 `[x]`로 바꾸어 저장하세요.\n\n"
        + "\n".join("- [ ] " + text for text in CHECKS)
        + "\n\n실제 전송 값은 script.json이에요. 이 문서만 바꾸면 전송 값은 바뀌지 않아요.\n"
        + "수정: script.json과 설정 편집 → render → 다시 검수 → approve.\n"
        + f'승인: `python run_pipeline.py approve "{output.as_posix()}"`\n', encoding="utf-8")
    files = required_files(output)
    save_json(output / "manifest.json", {"files": {name: digest(output / name) for name in files}})


def approve(output):
    output = Path(output)
    expected = read_json(output / "manifest.json")["files"]
    if set(expected) != set(required_files(output)):
        raise ValueError("검수 파일 목록이 다릅니다. render 후 다시 검수하세요.")
    check_files(output, expected)
    review = (output / "REVIEW.md").read_text(encoding="utf-8")
    if any("- [x] " + check not in review for check in CHECKS) or "- [ ]" in review:
        raise ValueError("REVIEW.md의 여섯 칸을 직접 확인하고 [x]로 바꾸어 저장하세요.")
    script = validate(read_json(output / "script.json"))
    if any(type(script.get(key)) is not bool for key in ("selfDeclaredMadeForKids", "containsSyntheticMedia")):
        raise ValueError("아동용·AI 공개 여부가 null입니다. script.json에 true/false를 정한 뒤 render·검수하세요. [Y013] [Y014]")
    expected.update({"manifest.json": digest(output / "manifest.json"), "REVIEW.md": digest(output / "REVIEW.md")})
    save_json(output / "APPROVED.json", {"approved_at": datetime.now(timezone.utc).isoformat(), "files": expected})


def require_approval(output):
    output = Path(output)
    if not (output / "APPROVED.json").is_file():
        raise ValueError("REVIEW.md 확인 후 python run_pipeline.py approve 폴더 명령을 실행하세요.")
    files = read_json(output / "APPROVED.json")["files"]
    if set(files) != set(required_files(output)) | {"manifest.json", "REVIEW.md"}:
        raise ValueError("승인 파일 목록이 다릅니다. 다시 검수하세요.")
    check_files(output, files)
