너는 ai-insta 프로젝트의 작업자(Codex)다. AGENTS.md, **docs/STYLE-GUIDE.md(확정 기준, 최우선)**, site/drafts/(3장 샘플 A·B·C와 drafts.css/js), site/assets/book.css·book.js·common.js, docs/chapter-template.html을 읽어라.
이번 작업은 **Phase 9-0. 개편용 공통 부품과 자동 검사기**다. 장 본문은 아직 고치지 않는다. commit하지 마라.

1. STYLE-GUIDE 2절의 장 틀에 필요한 공통 컴포넌트를 book.css/common.js에 추가한다: 먼저 답부터(직답 상자), 한눈에 보기(축 카드 그리드, 클릭 시 절 이동), 축 블록(정의/흐름/얼마/조건/언제/지금 할 일 고정 줄), 확인할 점 상자, 단계표, 자주 묻는 질문(접기 가능한 Q&A, 굵은 직답), 핵심 정리. drafts.css의 좋은 시각 요소를 공통으로 승격한다. 기존 장이 깨지지 않게 기존 클래스는 유지한다.
2. docs/chapter-template-v2.html: 위 틀을 모두 담은 이론 장 템플릿(주석으로 STYLE-GUIDE 규칙 요약).
3. scripts/style_lint.py: 지정 HTML의 학습자 본문 텍스트(스크립트·각주 속성 제외)에서 STYLE-GUIDE 3절 금지어·내부 용어(7r, 7v, Phase, PRAC-, API-, META- 등 사실 ID 본문 노출, Hermes, 원응답, 키트 계약, 실측 아님, 탐색 후보 등)와 '확인할 점' 상자 밖 단서 표현(미확인/단정할 수 없/별개) 횟수, 본문 글자 수를 보고한다. `--baseline` 옵션으로 개편 전 글자 수 대비 비율을 계산한다. 개편 전 기준선을 docs/results/phase-9/baseline.json에 저장한다(1~14장, 실습 0~10).
4. 현재 상태로 style_lint를 전 장에 돌린 결과를 docs/results/phase-9/lint-before.json으로 저장한다.
5. docs/results/phase-9-0.md 작성. notify는 하지 않는다(다음 단계가 이어진다).
