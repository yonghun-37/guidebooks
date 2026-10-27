#!/usr/bin/env bash
# 빈 폴더의 새 가상환경에서 틀 승인 명령·7종 시나리오·자유 문장 우회 회귀를 재현한다.
set -Eeuo pipefail
REPRO_ROOT=$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")/.." && pwd)
python3 "$REPRO_ROOT/scripts/check_blog_advanced.py" --check
REPRO_TMP=$(mktemp -d)
REPRO_PASSED=0
REPRO_FAILED=0
REPRO_CURRENT="준비"
finish_repro() {
  local result=$?
  if [ "$result" -ne 0 ]; then
    REPRO_FAILED=$((REPRO_FAILED + 1))
    printf '✖ 막힘: %s 재현 실패\n' "$REPRO_CURRENT"
  fi
  rm -rf -- "$REPRO_TMP"
  printf '재현 결과: 통과 %s / 실패 %s\n' "$REPRO_PASSED" "$REPRO_FAILED"
}
trap finish_repro EXIT
REPRO_PYTHONS=()
for candidate in python3.11 python3.12; do
  if command -v "$candidate" >/dev/null 2>&1; then
    REPRO_PYTHONS+=("$(command -v "$candidate")")
  fi
done
if [ "${#REPRO_PYTHONS[@]}" -eq 0 ]; then
  REPRO_PYTHONS+=("$(command -v python3)")
fi
for interpreter in "${REPRO_PYTHONS[@]}"; do
  REPRO_CURRENT=$($interpreter -c 'import sys; assert sys.version_info >= (3,11); print("Python "+sys.version.split()[0])')
  printf '%s 클린룸 시작\n' "$REPRO_CURRENT"
  REPRO_COPY="$REPRO_TMP/kit-$REPRO_PASSED"
  "$interpreter" - "$REPRO_ROOT/blog-auto-kit" "$REPRO_COPY" <<'PY'
import shutil
import sys
shutil.copytree(sys.argv[1], sys.argv[2], ignore=shutil.ignore_patterns(
    '.env', '.venv', 'private', 'output', 'config.toml', '__pycache__', '.pytest_cache'))
PY
  "$interpreter" -m venv "$REPRO_COPY/.venv"
  REPRO_PY="$REPRO_COPY/.venv/bin/python"
  "$REPRO_PY" -m pip install -q --disable-pip-version-check --no-cache-dir -r "$REPRO_COPY/requirements-dev.lock"
  (
    cd -- "$REPRO_COPY"
    export PYTHONIOENCODING=utf-8 PYTHONUTF8=1 PYTHONDONTWRITEBYTECODE=1 PYTHONNOUSERSITE=1
    "$REPRO_PY" course/execute.py --all
    "$REPRO_PY" course/build_expected.py --check
    # 전체 pytest에 Claude 우회 10개와 승인 틀·데이터·렌더 경계 회귀가 포함된다.
    "$REPRO_PY" -m pytest -q
  )
  REPRO_PASSED=$((REPRO_PASSED + 1))
done
