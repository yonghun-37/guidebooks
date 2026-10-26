"""사람 검수표의 완료 표시와 파일 해시로 승인을 기록한다."""
import argparse
from datetime import datetime, timezone
from hashlib import sha256
from common import cli, kit_path, read_json, save_json

ITEMS = {
    "facts": "숫자·정책·날짜·출처를 원문과 직접 대조하고 점검 리포트의 각 항목을 검토했어요.",
    "experience": "내 경험이 실제 메모와 같고 가짜 체험·성과·개인정보가 없어요.",
    "rights": "사진·삽화·인용의 이용 조건과 AI 사용·표시 범위를 기록했어요.",
    "disclosure": "제휴·제품 제공·원고료 등 실제 관계와 첫 문단의 표시를 확인했어요.",
    "preview": "모바일 미리보기와 이미지·링크를 열어 보고 최종 초안 저장을 승인해요."
}


def digest(path):
    return sha256(path.read_bytes()).hexdigest()


def template():
    return "# 사람이 확인할 검수표\n\n파일을 직접 열어 확인한 뒤 [ ]를 [x]로 바꾸세요.\n\n" + "\n".join(f"- [ ] {key}: {text}" for key, text in ITEMS.items()) + "\n\n## 작업 메모\n\n출처·내 경험·이미지 권리·AI 사용 범위·제공 관계·발행 후 공개 URL을 여기에 기록하세요.\n"


def fingerprints(output):
    metadata = read_json(output / "render.json")
    if not metadata.get("files"):
        raise ValueError("render.py로 HTML을 먼저 만드세요.")
    for name, expected in metadata["files"].items():
        if digest(output / name) != expected:
            raise ValueError("변환 뒤 파일이 달라졌어요. render.py로 다시 만들고 검수하세요.")
    names = [*metadata["files"], "render.json", "REVIEW.md"]
    return {name: digest(output / name) for name in names}


def approve(output):
    output = kit_path(output)
    text = (output / "REVIEW.md").read_text(encoding="utf-8")
    lines = text.splitlines()
    for key, description in ITEMS.items():
        if f"- [x] {key}: {description}" not in lines and f"- [X] {key}: {description}" not in lines:
            raise ValueError("REVIEW.md의 모든 항목을 직접 확인하고 [x]로 저장하세요.")
    values = fingerprints(output)
    save_json(output / "APPROVED.json", {"approved_at": datetime.now(timezone.utc).isoformat(), "files": values})
    print("사람 승인 기록 완료. publish.py는 기본 드라이런입니다.")


def require_approval(output):
    if not (output / "APPROVED.json").is_file():
        raise ValueError("REVIEW.md를 검수하고 review.py --approve로 승인하세요.")
    approved = read_json(output / "APPROVED.json")
    if approved.get("files") != fingerprints(output):
        raise ValueError("승인 뒤 파일이 달라졌어요. 다시 변환·검수·승인하세요.")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("output")
    parser.add_argument("--approve", action="store_true", required=True)
    approve(parser.parse_args().output)


if __name__ == "__main__":
    cli(main)
