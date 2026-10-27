너는 ai-insta 프로젝트의 작업자(Codex)다. AGENTS.md, .agents/skills/guidebook-writing·guidebook-pipeline, **docs/STYLE-GUIDE.md(최우선 문체)**, **docs/DESIGN-blog-advanced.md 전체(8절 우선)**, docs/DESIGN-baby.md 8절, docs/learner-questions-blog-advanced.md, research-blog-advanced/(BRIEFING·FACT-SHEET·SOURCES·노트), **docs/results/phase-BX3.md의 "장 틀 사용법"과 샘플 완성본 site-blog/advanced/01-environment.html·09-sponsorship.html(이 형식을 그대로 따른다)**, docs/results/phase-BX3k.md, blog-auto-kit/(course/commands.md, course/expected/ — 실제로 실행해 본다)를 읽어라.

이번 작업은 **Phase BX4a. BlogBook 심화편 집필: A0, A2~A6 (A1은 샘플 완성본 — 필요하면 다듬기만)**이다. 담당 파일: site-blog/advanced/의 00-start, 02-wordpress, 03-topics, 04-drafts, 05-gates, 06-publish (.html)와 그 장 전용 assets(site-blog/assets/advanced-<장>.css/js, assets/img/advanced/<장>-*). 공통 파일(book.js, book.css, common.js, advanced.css/js, index, glossary, credits)과 다른 장·키트·research는 수정하지 마라 — 필요한 변경은 docs/results/phase-BX4a-requests.md에, 새 용어는 phase-BX4a-glossary.md에. 병렬로 다른 작업자가 나머지 장을 쓴다. commit하지 마라.

## 원칙 (사용자 핵심 요구: 재현 가능 + 가독성)
- **명령이 두 OS에서 똑같으면 탭을 만들지 말고 "Windows·macOS·Linux 공통" 블록 하나로** 보인다(탭은 실제로 다를 때만: 가상환경 만들기·활성화·파일 복사 등). 같은 내용 반복은 가독성을 해친다.
- 장 하나 = 결과물 하나. 샘플 장과 같은 순서(먼저 답 → 만드는 것 → 한눈에 보기 → 시작 상태 확인 → 단계 → 코드 읽기 → 바꿔 보기 → 흔한 오류 → 체크포인트 → 확인할 점 → 정리).
- 모든 명령은 course/commands.md 그대로, "이렇게 보이면 성공"은 course/expected/의 실제 출력에서 그대로. 키트를 고치지 말고 다르면 requests에 적는다.
- 코드 발췌 25줄 이하 + "읽는 법" 표. 학습자 질문(해당 장 6개)에 본문이 첫 문장에서 직답하는지 결과 문서에 자체 점검표.
- 사양·조건·가격·법 조항은 [BX###] 각주, 2026년 10월 조사 기준, 근거 없는 숫자·기대 수익 금지, 내부 ID 본문 금지. 건강 정보는 DESIGN-baby 8절. 브랜드·광고주는 가상.
- 관리자·광고·제휴 화면 캡처 금지, 직접 그린 위치 그림. 시각자료는 STYLE-GUIDE 6절(필요한 곳에 적극적으로, 개수 채우기 금지), 라이트/다크.

## 장별 필수 내용
A0: 시스템 전체 그림(단계 클릭→장), 글 유형별 자동화 수준 표(DESIGN 1.1), 수익 구조 계산기(내 숫자 입력, 평균 기본값 금지), 월 비용 계산기(호스팅·도메인 갱신비·LLM). A2: mock/로컬 Docker/실호스팅 성공 화면 구분, 저가 호스팅 진단 과제(플러그인·SSH·REST 인증), 애플리케이션 비밀번호 발급 위치 그림, 필수 페이지(의무/권장 구분). A3: 주제 지도 그림, 글 유형 4종 스키마, 공공자료 3종 구분·공공누리·기준일. A4: AI 허용 확인 → 초안 → 경험 슬롯, 비용 기록. A5: 관문 판정 흐름 그림 + '관문 판정 따라가기' 도구(샘플 4편), 법적 금지/프로젝트 거절/자료 보류. A6: REST 요청·응답 순서 그림(비밀 가림), 중복 잠금·시간 초과 후 조회·재승인·공개 상태 재확인.

## 검증
style_lint, scripts/check_site.py(site-blog), 1280/375/360px × 라이트/다크, 콘솔 오류 0, 키보드, JS 없이 본문 읽기. 본문 명령을 빈 폴더 복사본에서 실행해 성공 문구 대조표. 결과 docs/results/phase-BX4a.md(+스크린샷 docs/results/phase-BX4a/). `python3 scripts/notify.py "✅ [BX4a 완료] ..."`로 한국어 보고.
