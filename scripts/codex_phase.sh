#!/usr/bin/env bash
# Run one Codex phase non-interactively: scripts/codex_phase.sh <name> <prompt-file>
set -uo pipefail
cd "$(dirname "$0")/.."
name=$1; prompt=$2
log=logs/codex-$name-$(date +%Y%m%d-%H%M%S)
python3 scripts/notify.py "▶️ [Codex 시작] $name"
codex exec -s workspace-write -c sandbox_workspace_write.network_access=true \
  --add-dir /home/yonghun/project/hermes-research/output/ai-insta-research-20261026 -C "$PWD" \
  -o "$log.last.md" - < "$prompt" > "$log.log" 2>&1
status=$?
if [ $status -ne 0 ]; then
  python3 scripts/notify.py "⚠️ [Codex 실패] $name (exit $status). 로그: $log.log — Claude Code가 확인합니다."
fi
echo "exit=$status log=$log.log last=$log.last.md"
exit $status
