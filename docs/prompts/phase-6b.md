너는 ai-insta 프로젝트의 작업자(Codex)다. AGENTS.md, docs/DESIGN.md 8절, docs/results/phase-5d.md, docs/results/phase-6a-findings.md를 읽어라.
이번 작업은 **Phase 6b. 수정과 품질 게이트**다. commit하지 마라.

1. phase-6a-findings의 '차단'과 '혼란'은 모두 고치고, '사소'는 합리적인 범위에서 고친다. 고치지 않은 항목은 이유를 남긴다.
2. 검수자(Claude) 추가 지시: 3장·13장 장부 시뮬레이터에 수입·비용·잔액을 보여 주는 간단한 SVG 막대 그래프(텍스트 결과 유지)를 추가한다. 입력 칸이 많은 시뮬레이터는 모바일에서 2열/접기로 길이를 줄인다.
3. scripts/check_site.py를 만든다: 모든 HTML의 내부 링크·앵커, 2~14장 9블록, 각주 SOURCES 번호가 research/SOURCES.md에 존재, fact-pending 0개, data-term이 용어집에 존재, 퀴즈 데이터 구조, 이미지 alt, 파일 크기 합계. 실패 시 exit 1. 통과시킨다.
4. 브라우저 검사(1280/375/360px 가로 넘침·콘솔 오류·다크 모드)를 전 페이지에 다시 돌리고, 스타터 키트 테스트를 다시 통과시킨다.
5. DESIGN.md 8절 게이트별 통과/미통과 표를 docs/results/phase-6b.md에, docs/PROJECT_STATE.md를 최종 상태로 갱신한다. shelf/progress/index.html의 단계 상태도 최신으로 바꾼다.
6. `python3 scripts/notify.py "✅ [Phase 6b 완료] ..."`로 한국어 보고.
