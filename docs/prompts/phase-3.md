너는 ai-insta 프로젝트의 작업자(Codex)다. AGENTS.md, docs/DESIGN.md, docs/PLAN.md, docs/reference-analysis.md, research/FACT-SHEET.md(있으면)를 읽어라.
주의: 자료조사(Phase 1/1b)가 다른 작업자에 의해 동시에 진행 중이다. research/, docs/PROJECT_STATE.md, docs/PLAN.md는 수정하지 마라. 1장의 정책·수치 문장은 FACT-SHEET에 해당 사실 ID가 있을 때만 쓰고, 없으면 `<span class="fact-pending">[출처 확인 대기]</span>` 표시로 남겨라(나중에 채운다).
이번 작업은 docs/PLAN.md의 **Phase 3. 뼈대와 디자인 시스템, 1장** 만이다.

1. DESIGN.md 7절 구조로 site/를 만든다. book.js는 하나의 장 데이터(번호, slug, 부, 제목, 결과물, 소요시간, 난이도, 상태: 준비중/완성)에서 표지 목차, 장 상단 메타, 사이드/하단 내비, 이전·다음 링크를 그린다. 아직 없는 장은 "준비 중"으로 표시하되 링크가 깨지지 않게 한다.
2. 공통 기능: 9단계 블록 스타일, 용어 툴팁(용어집 링크), 각주/출처 표시, 코드 복사 버튼, 결과물 체크리스트(localStorage try/catch), 퀴즈 엔진(데이터 속성 기반, 즉시 채점·해설), 다크 모드(시스템 따름 + 토글), "교육용 가정 모형" 배지, 시뮬레이터 공통 래퍼(키보드 조작, 결과 텍스트 출력).
3. docs/chapter-template.html: 9단계 블록이 모두 들어간 장 템플릿(주석으로 작성 규칙 포함).
4. index.html 표지와 1장(chapters/01-map.html "계정 하나가 돈이 되기까지")을 완성한다. 1장 시뮬레이터: 파이프라인 지도(소재→문안→카드/릴스→검수→게시→분석→수익, 각 블록 클릭 시 설명·관련 장 링크·필요한 도구·하린의 시간 예산 표시) + 주당 투입 시간 슬라이더로 30일 동안 만들 수 있는 게시물 수를 보여 주는 교육용 계산. 1장 사실 주장은 FACT-SHEET 사실 ID와 SOURCES 번호를 각주로 단다. 하린·정 선배 서사를 시작한다.
5. 정적 서버로 띄워 Playwright(또는 사용 가능한 헤드리스 브라우저)로 데스크톱 1280px·모바일 375px 스크린샷을 docs/results/phase-3/에 저장하고, 가로 스크롤 여부와 콘솔 오류를 확인한다. 브라우저 설치가 샌드박스에서 막히면 이유를 기록하고 HTML 검증만 한다.
6. docs/results/phase-3.md 작성, git commit("Phase 3: site skeleton and chapter 1") — `git add site docs/chapter-template.html docs/results/phase-3.md docs/results/phase-3 docs/reference-analysis.md docs/results/phase-2.md` 처럼 이 단계 파일만 명시해서 add 한다. index.lock 충돌 시 잠시 후 재시도한다, notify로 보고(스크린샷 1~2장 첨부: `python3 scripts/notify.py "메시지" 파일1 파일2`).
