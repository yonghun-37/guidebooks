"""승인된 JPEG/MP4만 새 공개 폴더로 복사한다. 업로드·네트워크 호출 없음."""
import argparse
from pathlib import Path
import shutil

from common import cli, read_json
from review import require_approval


def prepare(output, destination):
    output, destination = Path(output).resolve(), Path(destination).resolve()
    require_approval(output)
    if destination.is_relative_to(output):
        raise ValueError("공개 폴더는 검수 출력 폴더 바깥의 새 폴더로 지정하세요.")
    files = [f"cards/card-{i:02d}.jpg" for i in range(1, len(read_json(output / "copy.json")["scenes"]) + 1)] + ["reel.mp4"]
    approved = read_json(output / "APPROVED.json")["files"]
    for name in files:
        if name not in approved:
            raise ValueError("승인 기록에 게시용 파일이 없습니다. 다시 검수하세요.")
        if (output / name).stat().st_size > 25 * 1024 * 1024:
            raise ValueError("GitHub 웹 업로드는 파일당 25MiB까지입니다. 파일 크기를 줄인 뒤 다시 검수하세요.")
    destination.mkdir(parents=True, exist_ok=False)
    for name in files:
        target = destination / name
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(output / name, target)
    print(f"공개 준비 완료: {len(files)}개 JPEG/MP4 → {destination}")
    print("작은 비민감 교육 실습용입니다. 합성 자료를 실제 뉴스로 게시하지 마세요.")
    print("1. 본인 GitHub의 별도 공개 저장소에서 Add file > Upload files를 엽니다.")
    print("2. 이 폴더 안 cards 폴더와 reel.mp4를 함께 드래그 앤 드롭하고 Commit changes로 저장합니다.")
    print("3. Settings > Pages > Build and deployment > Source: Deploy from a branch에서 branch와 /(root)를 선택합니다.")
    print("4. 배포 완료 후 로그인하지 않은 창에서 파일 자체가 열리는지 확인합니다.")
    print("기본 URL 규칙: https://사용자.github.io/저장소 (하위 폴더에 올렸다면 그 경로까지)")
    print("파일 URL: <기본 URL>/cards/card-01.jpg 및 <기본 URL>/reel.mp4")
    print(f'미리보기: python publish.py "{output}" --base-url "<기본 URL>"')
    print(f'실제 2개 게시 시도: python publish.py "{output}" --live --base-url "<기본 URL>"')
    print(".env·토큰·검수/설정 파일은 복사하지 않습니다. Pages 이용정책·Meta 파일 수신은 별도 확인하세요.")
    return files


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("output", type=Path)
    parser.add_argument("--dest", type=Path, required=True, help="새로 만들 공개 폴더")
    args = parser.parse_args()
    prepare(args.output, args.dest)


if __name__ == "__main__":
    cli(main)
