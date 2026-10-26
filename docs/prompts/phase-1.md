너는 ai-insta 프로젝트의 작업자(Codex)다. 먼저 AGENTS.md, docs/DESIGN.md, docs/PLAN.md를 읽어라.
이번 작업은 docs/PLAN.md의 **Phase 1. 자료조사 (Hermes)** 만이다.

절차:
1. `$RUN=/home/yonghun/project/hermes-research/output/ai-insta-research-20261026` 아래 queries/, raw/ 를 만든다.
2. PLAN.md의 12개 주제별로 Hermes 질의 파일을 작성한다. DESIGN.md 5절 "반드시 다룰 사실 영역"을 빠짐없이 덮도록 구체적인 질문 목록을 넣고, PLAN.md "Hermes 호출법"의 공통 요구(한국어, 출처 URL+게시일, 공식 우선, 미확인 표시, 한국 가용성, 2026-10 기준)를 모든 질의에 넣는다. 오늘은 2026-10-26이다.
3. Hermes를 PLAN.md 방법대로 실행한다(최대 4개 병렬, 총 16회 이하). 각 실행의 시작/종료 시각, exit code, 바이트 수를 $RUN/runs.jsonl 에 기록한다.
4. 원응답을 읽고 research/<topic>.md, research/SOURCES.md, research/FACT-SHEET.md 를 PLAN.md 형식대로 작성한다. 핵심 공식 출처 최소 5개(특히 Graph API 게시 한도·요건, 수익화 자격, AI 라벨 정책, 추천보증 심사지침)는 직접 curl 등으로 열어 확인 결과를 표시한다.
5. 응답이 빈약한 주제는 보충 질의를 한도 안에서 실행한다. 그래도 부족하면 FACT-SHEET에 "미확인/추가 조사 필요"로 남긴다. 추측으로 채우지 않는다.
6. docs/results/phase-1.md(질의 수, 성공/실패, 주제별 출처 수, 확인 결과, 목차 조정 제안, 남은 공백)를 쓰고, docs/PROJECT_STATE.md를 갱신하고, git add/commit 한다(메시지: "Phase 1: research notes"). 이 저장소의 다른 Phase 파일(docs/reference-analysis.md, docs/results/phase-2.md)은 다른 작업자가 동시에 쓰고 있으니 commit에 포함하지 말고 건드리지 마라.
7. 마지막에 `python3 scripts/notify.py "✅ [Phase 1 완료] ..."` 로 5줄 이내 보고.

주의: hermes-research 저장소의 코드·config·runtime은 수정 금지. 컨테이너 재시작 금지. 유료 API 금지.
