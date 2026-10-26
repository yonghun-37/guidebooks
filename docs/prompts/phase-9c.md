너는 ai-insta 프로젝트의 작업자(Codex)다. 먼저 AGENTS.md, **docs/STYLE-GUIDE.md(확정 기준, 최우선)**, docs/chapter-template-v2.html, site/drafts/ 3장 샘플 A·B·C, docs/learner-questions.md, research/FACT-SHEET.md, research/SOURCES.md, docs/results/phase-1c.md(재조사로 새로 확인된 사실·메뉴 이름), research/r2-*.md, docs/results/phase-9-0.md를 읽어라.
이번 작업은 **Phase 9c. 개편: 이론편 10~14장** 이다. 사용자가 3장 샘플의 품질 향상을 확인하고 "A 뼈대 + B 질문 답변 + C 단계표" 방식으로 인스타 편 전체를 다시 점검·개선하라고 지시했다.

해야 할 일:
1. 담당 범위의 각 페이지를 STYLE-GUIDE 5절 채점표로 먼저 채점해 docs/results/phase-9c-before.md에 적는다(엄격하게).
2. STYLE-GUIDE 2~4절대로 다시 쓴다. 학습자 질문 5개(learner-questions.md)에 직답하지 못하는 부분부터 고친다. 1c 재조사로 확인된 새 사실·숫자·메뉴 이름을 반영한다(FACT-SHEET 근거, 출처 각주 유지). 근거 없는 숫자를 만들지 않는다.
3. 시뮬레이터는 학습자 질문에 답하는 것만 남기고 결과를 "숫자 하나 + 해석 한 문장"으로 단순화한다. 불필요한 시뮬레이터 JS는 장에서 연결만 끊고 파일은 남긴다(실험실이 참조할 수 있음).

4. 다른 작업자가 동시에 다른 범위를 고친다. **담당 범위 파일과 그 전용 JS/이미지만 수정**한다. book.css/common.js/book.js 수정이 꼭 필요하면 docs/results/phase-9c-requests.md에 diff로 남긴다.
5. scripts/style_lint.py 통과(금지어·내부 용어 0, 단서 표현 장당 2회 이하, 이론편은 기준선 대비 70% 이하 분량), 1280/375px 가로 넘침·콘솔 오류 0, 내부 링크 정상, 퀴즈 정답이 새 본문과 일치. 실습편 명령은 실제 실행으로 재확인.
6. 다시 채점해 docs/results/phase-9c.md에 전/후 점수표, 바뀐 점, 남은 문제, 스크린샷(docs/results/phase-9c/)을 남긴다. commit하지 마라.
7. `python3 scripts/notify.py "✅ [Phase 9c 개편 완료] ..." <대표 스크린샷>`로 한국어 보고.
