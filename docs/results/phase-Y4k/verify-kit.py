"""깨끗한 임시 복사본에서 README의 제작·승인·드라이런·예약 명령을 실행한다."""
import json
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile

ROOT = Path(__file__).resolve().parents[3]
REPORT = Path(__file__).parent
results = []
with tempfile.TemporaryDirectory(prefix="shorts-y4k-clean-") as temporary:
    kit = Path(temporary) / "초보자 쇼츠"
    shutil.copytree(ROOT / "shorts-kit", kit, ignore=shutil.ignore_patterns(".venv", "__pycache__", ".pytest_cache", "output", "private", "input"))
    def run(*args, cwd=None):
        value = subprocess.run([sys.executable, *map(str, args)], cwd=cwd or kit, capture_output=True, text=True, encoding="utf-8")
        results.append({"args": list(map(str, args)), "returncode": value.returncode, "stdout": value.stdout, "stderr": value.stderr})
        if value.returncode:
            raise AssertionError(results[-1])
    run("run_pipeline.py", "run", "--output", "output/first")
    run("run_pipeline.py", "run", "--mode", "prompt", "--output", "output/my-script")
    first, prompt = kit / "output/first", kit / "output/my-script"
    script = json.loads((first / "script.json").read_text())
    script["selfDeclaredMadeForKids"] = False
    script["containsSyntheticMedia"] = False
    (prompt / "script.json").write_text(json.dumps(script, ensure_ascii=False), encoding="utf-8")
    run("run_pipeline.py", "validate", "output/my-script")
    run("run_pipeline.py", "render", "output/my-script")
    review = prompt / "REVIEW.md"
    # 시험 복사본의 자체 생성 가상 미디어만 확인한다. 공개 샘플은 승인하지 않는다.
    review.write_text(review.read_text().replace("- [ ]", "- [x]"), encoding="utf-8")
    run("run_pipeline.py", "approve", "output/my-script")
    run("upload.py", "output/my-script")
    assert json.loads((prompt / "dry-run.json").read_text())["network_calls"] == 0
    assert not (prompt / "upload-session.json").exists()
    run(kit / "daily.py", "--date", "2026-10-26", "--output-root", "output/daily", cwd=Path(temporary))
    assert (kit / "output/daily/2026-10-26/REVIEW.md").is_file()
    run("schedule_setup.py", "--os", "windows", "--time", "09:30")
    run("schedule_setup.py", "--os", "macos", "--time", "09:30")
(REPORT / "clean-copy-check.json").write_text(json.dumps({"passed": True, "commands": results, "environment": "Linux, Python " + sys.version.split()[0], "native_os_test": False}, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
print(f"깨끗한 임시 복사본 명령 {len(results)}개 통과")
