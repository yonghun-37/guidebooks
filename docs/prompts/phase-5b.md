# Phase 5b 집필: 6, 7, 8, 9장

담당: 6, 7, 8, 9장. 파일 slug 제안: 06-ai-writing, 07-cards, 08-reels, 09-pipeline (스타터 키트의 write_copy prompt/api 모드, render_cards 템플릿·테마, make_reel 내레이션·음악, run_pipeline 검수 흐름을 실제 실행하며 따라 하게 한다). 장 번호·제목·결과물은 site/assets/book.js의 장 데이터와 docs/DESIGN.md 5절·9절을 따른다(slug가 book.js와 다르면 book.js의 slug를 따른다).
우선 읽을 조사 노트: ai-text-image-tools, ai-tools-pricing, content-craft, ai-video-voice-tools, music-assets-licensing, nocode-pipelines, ai-labeling-policy.

## 공통 지시 (Phase 5 집필)

너는 ai-insta 프로젝트의 작업자(Codex)다. 먼저 AGENTS.md, docs/DESIGN.md(특히 3·4·5절), docs/chapter-template.html, site/chapters/01-map.html(완성 예시), site/assets/book.js, site/assets/book.css, site/assets/sim/common.js, research/BRIEFING.md, research/FACT-SHEET.md, starter-kit/README.md를 읽어라. 담당 장과 관련된 research/<topic>.md도 읽는다.

집필 원칙:
- 독자는 코딩·마케팅 경험이 없는 직장인 초보자다. 짧은 문장, 쉬운 말, 용어는 처음 나올 때 풀어 쓰고 `data-term`으로 용어집에 연결한다.
- 9단계 블록을 모두 갖춘다. 장 상단에 결과물·소요 시간·난이도·선행 장.
- 모든 정책·수치·법률·가격 문장은 FACT-SHEET 사실 ID에 근거하고 SOURCES 번호 각주를 단다. "2026년 10월 조사 기준"을 명시한다. 상충·미확인 사실은 그 사실 자체를 독자에게 알려 준다(예: "공식 문서 안에서도 50건/100건으로 다르게 적혀 있다"). 근거 없는 수치·성공 보장·과장 금지.
- 작업실 노트는 번호 단계마다 소요 시간·준비물·기대 결과·흔한 오류를 적고, 스타터 키트 명령은 starter-kit/.venv로 **실제 실행해 확인한 것만** 쓴다. Windows/macOS 차이는 짧게 병기한다.
- 시뮬레이터는 장마다 1~2개, site/assets/sim/<이름>.js로 구현한다. 공통 래퍼를 쓰고, 키보드 조작·텍스트 결과·"교육용 가정 모형" 배지와 가정값 공개. 극단값에서 무엇이 깨지는지 보여 주는 "무너뜨리기" 프리셋을 하나 이상 넣는다.
- 하린·정 선배 서사를 장마다 이어 간다. 이전 장의 결과물을 다음 장에서 이어 쓰도록 연결한다.
- 실제 사례 블록: research에 근거가 있는 공개 사례·공식 예시만 출처와 함께 쓴다. 없으면 "사례 유형 분석"으로 가상임을 밝힌다.
- 퀴즈 3~5문항, 해설은 본문 근거 절을 가리킨다.
- 참고 사이트 문장·코드 복사 금지.

충돌 방지(다른 작업자가 동시에 다른 장을 쓴다):
- 담당 장의 HTML, 담당 장의 시뮬레이터 JS, 필요 시 site/assets/img/ch<번호>-*.{svg,png}만 새로 만든다.
- **site/assets/book.js, book.css, common.js, glossary.html, credits.html, index.html은 수정하지 마라.** 필요한 변경(장 상태를 완성으로, 새 공통 CSS, 공통 JS 개선)은 docs/results/phase-5b-requests.md에 정확한 diff 제안으로 적는다. 장 전용 스타일이 꼭 필요하면 장 HTML 안의 <style>을 최소로 쓴다.
- 새 용어는 docs/results/phase-5b-glossary.md에 "용어 | 쉬운 설명 | 처음 나온 장 | 관련 사실 ID" 표로 적는다.
- commit하지 마라.

검증: 정적 서버 + 기존 Chromium/Playwright로 담당 장의 1280px·375px 가로 넘침, 콘솔 오류, 내부 링크, 9블록 존재, 퀴즈 동작, 시뮬레이터 키보드 조작을 확인하고 스크린샷 2장을 docs/results/phase-5b/에 저장한다. 결과는 docs/results/phase-5b.md에. 마지막에 `python3 scripts/notify.py "✅ [Phase 5b 완료] ..." <스크린샷1>`로 한국어 5줄 보고.
