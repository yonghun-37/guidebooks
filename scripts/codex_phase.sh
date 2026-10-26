#!/usr/bin/env bash
# Run one Codex phase non-interactively: scripts/codex_phase.sh <name> <prompt-file>
# Retries up to 3 times when the model reports "at capacity".
set -uo pipefail
cd "$(dirname "$0")/.."
name=$1; prompt=$2
python3 scripts/notify.py "▶️ [Codex 시작] $name"
for attempt in 1 2 3 4; do
  log=logs/codex-$name-$(date +%Y%m%d-%H%M%S)
  codex --search exec -s workspace-write -c sandbox_workspace_write.network_access=true \
    -c 'mcp_servers.rea.default_tools_approval_mode="approve"' -c 'service_tier="fast"' \
    --add-dir "${HERMES_RUN:-/home/yonghun/project/hermes-research/output/ai-insta-research-20261026}" -C "$PWD" \
    -o "$log.last.md" - < "$prompt" > "$log.log" 2>&1
  status=$?
  if [ $status -ne 0 ] && grep -q "at capacity" "$log.log" && [ $attempt -lt 4 ]; then
    python3 scripts/notify.py "⏳ [Codex 재시도] $name: 모델 용량 초과, $((attempt*120))초 뒤 다시 시작합니다."
    sleep $((attempt*120)); continue
  fi
  break
done
if [ $status -ne 0 ]; then
  python3 scripts/notify.py "⚠️ [Codex 실패] $name (exit $status). 로그: $log.log — Claude Code가 확인합니다."
fi
echo "exit=$status log=$log.log last=$log.last.md"
exit $status
