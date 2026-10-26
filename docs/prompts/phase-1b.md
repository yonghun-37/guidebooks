너는 ai-insta 프로젝트의 작업자(Codex)다. AGENTS.md, docs/DESIGN.md, docs/PLAN.md(특히 "Hermes 호출법"과 "Phase 1b")를 읽고, Phase 1 산출물(research/*.md, docs/results/phase-1.md)을 먼저 검토하라.
이번 작업은 **Phase 1b. 확장 자료조사** 만이다. 사용자가 자료조사를 가장 중요하게 여기므로 폭과 근거 품질을 최우선으로 한다.

1. Phase 1의 공백(미확인 항목, 출처가 약한 주장, 한국 가용성 미확인)을 목록화해 `gap-fill` 질의에 넣는다.
2. 주제 13~26의 질의 파일을 $RUN/queries/에 쓰고(Phase 1 공통 요구 포함), Hermes를 최대 4개 병렬로 실행한다. 총 28회 이하, `--max-turns 40`. runs.jsonl에 계속 기록한다.
3. 원응답 품질을 확인한다: 출처 URL이 없거나 공식 출처가 부족한 주제는 더 좁은 보충 질의를 한도 안에서 실행한다.
4. research/<topic>.md 추가, SOURCES.md·FACT-SHEET.md 확장. 새 핵심 공식 출처 5개 이상을 직접 열어 확인 표시한다. 상충하는 정보는 양쪽 출처와 함께 "상충"으로 표시한다.
5. research/BRIEFING.md 를 PLAN.md Phase 1b 형식대로 작성한다. 초보자가 읽어도 이해되는 한국어로, 과장 없이, 모든 주장에 출처 번호.
6. docs/results/phase-1b.md, docs/PROJECT_STATE.md 갱신, git commit("Phase 1b: extended research and briefing"). docs/reference-analysis.md·docs/results/phase-2.md는 건드리지 말고 commit에 넣지 마라.
7. `python3 scripts/notify.py "✅ [Phase 1b 완료] ..." research/BRIEFING.md` 로 5줄 이내 한국어 보고(BRIEFING 첨부).
