"""검수 대상 목록과 승인 시점 파일 해시를 보존한다."""
from datetime import datetime, timezone
from pathlib import Path

from common import digest, read_json, save_json


def prepare_review(output):
    output = Path(output)
    copy = read_json(output / "copy.json")
    files = ["news.json", "copy.json", "config.json", "reel.mp4", "reel-info.json", "subtitles.srt", "frames.txt"]
    for i in range(1, len(copy["scenes"]) + 1):
        files += [f"cards/card-{i:02d}.png", f"cards/card-{i:02d}.jpg", f"frames/scene-{i:02d}.png",
                  f"frames/scene-{i:02d}-caption.png", f"frames/scene-{i:02d}.mp4"]
    files += read_json(output / "reel-info.json")["audio_files"]
    for name in ("APPROVED.json", "dry-run.json"):
        (output / name).unlink(missing_ok=True)
    (output / "REVIEW.md").write_text(f"""# 게시 전 사람 검수

상태: 검수 대기. 이 파일을 읽고 아래 여섯 칸을 `[x]`로 바꾸어 저장한 뒤 approve 명령을 실행하세요.
{copy['label']}

- [ ] news.json의 원출처·날짜·인명·수치·조건을 copy.json 및 카드와 대조했습니다. 합성 피드는 실제 뉴스가 아님을 확인했습니다.
- [ ] cards/의 모든 PNG와 게시용 JPEG를 열어 글자 잘림·출처·한글을 확인했습니다.
- [ ] reel.mp4를 끝까지 재생해 장면 전환·줌/팬·자막 등장·진행 막대·시간 및 음성/무음을 확인했습니다. 움직임만으로 수익화 적격이 보장되지 않음을 확인했습니다.
- [ ] 입력 자료·폰트·사진·음원 등의 이용 권리를 확인했습니다. AI 정보·광고 표시의 필요 여부를 검토하고 copy.json의 is_ai_generated를 확인했습니다.
- [ ] 직접 녹음한 내레이션·사용자 제공 배경음악의 이용 권리와 라이선스를 확인했습니다. TTS 사용 시 엔진·모델·화자 동의·출력물의 이용 조건도 확인했습니다. 미사용 항목은 해당 없음으로 검토했습니다.
- [ ] 아래 캡션을 확인했고 이 결과물의 드라이런 게시를 승인합니다.

## 캡션 (실제 전송 값은 copy.json)

{copy['caption']}

## 다음 명령

starter-kit 폴더의 터미널에서 실행:
`python run_pipeline.py approve "{output.as_posix()}"`

이 명령은 승인 기록 후 드라이런 요청을 출력합니다. 실제 게시하지 않습니다.
문안 수정은 copy.json 편집 → `python run_pipeline.py render "{output.as_posix()}"` → 다시 검수 순서입니다.
이 문서에 캡션만 고쳐 적으면 전송 값은 바뀌지 않습니다.
""", encoding="utf-8")
    save_json(output / "manifest.json", {"files": {name: digest(output / name) for name in files}})


def check_files(output, expected):
    for name, checksum in expected.items():
        path = output / name
        if not path.resolve().is_relative_to(output.resolve()) or not path.is_file() or digest(path) != checksum:
            raise ValueError(f"검수 대상이 바뀌었거나 없습니다: {name}. render 후 다시 검수·승인하세요.")


def approve(output):
    output = Path(output)
    expected = read_json(output / "manifest.json")["files"]
    check_files(output, expected)
    review = (output / "REVIEW.md").read_text(encoding="utf-8")
    if review.count("- [x]") != 6 or "- [ ]" in review:
        raise ValueError("REVIEW.md의 검수 여섯 칸을 [x]로 바꾸어 저장한 뒤 승인하세요.")
    expected.update({"manifest.json": digest(output / "manifest.json"), "REVIEW.md": digest(output / "REVIEW.md")})
    save_json(output / "APPROVED.json", {"approved_at": datetime.now(timezone.utc).isoformat(), "files": expected})


def require_approval(output):
    output = Path(output)
    if not (output / "APPROVED.json").is_file():
        raise ValueError("검수 대기 중입니다. REVIEW.md 확인 후 run_pipeline.py approve 명령이 필요합니다.")
    check_files(output, read_json(output / "APPROVED.json")["files"])
