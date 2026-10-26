# B6 — BlogBook 통합

2026-10-26. **통합·로컬 게이트 완료, B7 독립 검토·Claude Code 검수 대기**. 기존 결과 문서 관례를 Level 2 기능 기록으로 이어 썼다. 실제 서비스 가입·발행·심사·정산·API live·결제·commit/push·배포를 수행한 기록은 아니다.

## 요구·전략·완료 범위

- [x] B3/B3k·B4a/b/c·B5 결과와 requests/glossary, 설계·문체·연구 근거 대조
- [x] 이론 1~13·실험실(14)·용어집(15), 실습 0~10·E2E, 부록 3개의 공통 상태를 **완성**으로 연결
- [x] 표지의 정적 목차와 공통 동적 목차·선행 장·이전/다음·본문 참조를 실제 파일로 통합
- [x] 프롬프트·모델/사용처/비용·실험실·용어집·출처, 표지 질문별 경로·키트 샘플/ZIP 구현
- [x] 정적·문체·3폭×2테마·링크·키보드·Python 3.11 키트 검사와 화면 직접 확인
- [x] 현재 상태·서가 블로그 상태·근거 노트 갱신

기존 정적 HTML/CSS/바닐라 JS와 iframe 재사용 방식을 유지했다. 새 실행 의존성·아키텍처 변경이 없어 ADR은 추가하지 않았다. `common.js`, `practice.js`, `book.css`, `lab.js`는 요청상 변경이 필요 없고 현재 도구·저장·테마를 그대로 지원했다. 통합 상태와 표시 번호는 `book.js`, 새 부록의 반응형 조판은 `blog.css`에 반영했다.

## 구현 결과

| 대상 | 결과 |
|---|---|
| `site-blog/assets/book.js`·본문 | 모든 장·실습·부록 완성, 실제 파일·학습 결과·실습 시간, 실습 번호 표시. 기존 준비중 링크를 실제 본문으로 교체. 저장된 `pending.html?chapter=…` 옛 주소에서도 완성 본문으로 이동 가능 |
| `index.html` | **블로그 수익화 입문서**, 실습 시작, AI 도구 지도·글쓰기 레시피·비용·프롬프트 진입. 방문자 1천 명/플랫폼/AI 글의 세 질문 경로, JS 없는 전체 30항목 목차 |
| `prompts.html` | **18개** 복사 블록. 6장 정보·후기·여행의 준비/초안·교정, 실습 4의 자료표/개요/초안·실습 5의 삽화/이미지 기록, 10~13장 반복/분석/정책/계획 요청문. 작업별 좋은/나쁜 요청 비교와 원본 링크 |
| `ai-models.html` | **13개 작업 카드**. 글·교정·이미지·썸네일·키워드·분석, 앱/구독·API·편집기 내장 기능, 구독/크레딧/종량제, 무료·저비용 조합·권리 확인. 무료 0원, 월 10편 가정의 디자인 구독 배분 1,490원, 총 입력 12,000·출력 6,000토큰 가정의 Luna US$0.0042·Sol US$0.084 사용분을 실제 결제와 구분 |
| `lab.html`·`catalog.js` | **13개 장 도구 전부** 원본 `?embed=<id>`로 재사용. 계산·도구 HTML 사본 없음. 원본 링크·전체 직접 목록·선택 URL·높이/테마 연동 |
| `glossary.html`·본문 | 요청을 중복 ID로 병합한 **43개 용어**, **38개 첫 본문 링크**와 data-term 일치. 인증 토큰과 AI 사용량 토큰 분리. 검색·본문 예시 복귀 |
| `credits.html` | 실제 각주 링크에서 모은 **B 출처 149개**만 수록. 원문·기관·날짜·인용한 장의 왕복 링크, 가상 인물·AI 삽화 3장·실제 요청문·글꼴·저장 안내 |
| `samples/blog-kit/` | 원본 키트의 글·그림·검사 리포트·README·**ZIP 32파일 / 55,102 bytes** 동봉. 미리보기에 아이콘 메타만 추가. 실제 키트 코드는 변경하지 않음. 실습 10과 표지에서 로컬 ZIP/README 제공 |

수아·태오의 가상 블로그 ‘퇴근 후 생활 정보’와 지원 제도 글·실사용 생활 가전 후기·당일치기 여행을 유지했다. 새 이미지 생성은 하지 않았다. 도구/과금 흐름과 좋은/나쁜 비교는 HTML figure·figcaption, 두 테마 CSS로 표현했다.

## 재생성과 근거

`python3 scripts/build_appendices.py --site site-blog`는 새 `scripts/build_appendices_blog.py`를 실행한다. 원고에서 도구·프롬프트를 읽고, B4a/b/c·B5 용어 요청을 병합하며, 실제 인용 링크만 출처로 모으고, 허용한 공개 키트 파일만 ZIP으로 만든다. 모델 부록은 작성된 HTML을 유지하면서 용어·출처를 통합한다. 반복 실행 후 사이트 파일의 바이트 동일성을 테스트했다.

공유 `TermLinks`에 site/label 선택 인자를 추가했고 기본 동작과 다른 책 생성기의 기존 전역 경로 사용도 유지했다. 테스트는 임시 복사본에서 실행하므로 다른 책을 재생성하지 않았다.

- B5 직접 확인 인계 **B208~B210**: 네이버·카카오 2단계 인증, 공식 ChatGPT 웹 대화 안내를 등록하고 실습 1·2 각주로 연결했다. 공개 원문을 다시 열었고 로그인 후 설정은 실행하지 않았다.
- **B211/B212**: 공통 `research/ai-models-pricing.md`의 S400/S408을 블로그 B번호로 연결하고 공식 OpenAI/Gemini API 가격 원문을 다시 확인했다. Claude·Gemini 한국 구독표도 대조했다. API를 호출하지 않았다.
- 미리캔버스 14,900원은 기존 B2/B4b 직접 확인의 일반 가이드 값이다. B6 재열람의 동적 페이지 텍스트에서는 숫자가 재현되지 않아 새 독립 가격 확인으로 세지 않았다. 결제창의 개인/좌석·월납/연납·세금 확인을 한 상자에 안내한다.
- 업데이트: `research-blog/SOURCES.md`, `FACT-SHEET.md` BL-UI-14·BL-AI-14, `QUESTION-MAP.md` P01-5/P02-1, 네이버/티스토리 UI·AI 제작 노트. Hermes 추가 질의 없이 기존 조사와 공식 공개 문서 재확인으로 통합했다.

## 실행한 검증

| 검사 | 실제 결과·기록 |
|---|---|
| `python3 scripts/check_site.py --site site-blog --output docs/results/phase-B6/check-site.json` | **오류 0**. 서가 포함 36 HTML·내부 참조 2,147개, 이론 13·퀴즈 39·원본 도구 13·실습 체크 15키·용어 링크 38개. [JSON](phase-B6/check-site.json) |
| `python3 scripts/style_lint.py --site site-blog --output docs/results/phase-B6/style-lint.json` | **34/34 통과**, 금지어·내부 용어·반복 단서 0. 신규 원고라 이전 70% 축약 기준선은 미적용. [JSON](phase-B6/style-lint.json) |
| `/tmp/blogbook-b6-py311/bin/python -m pytest scripts/tests -q` | **41 passed**, 블로그 부록 원본 일치·출처/용어 병합·재생성 동일성·ZIP 공개 파일 5개 새 검사 포함. [출력](phase-B6/scripts-tests.txt) |
| Python **3.11.15**, pytest 8.4.2: `-m pytest blog-kit/tests -ra` | **97 passed**. 같은 Python으로 동봉 ZIP을 새 임시 경로에 풀어 **97 passed** 재확인. [원본](phase-B6/blog-kit-py311.txt)·[동봉본](phase-B6/distribution-py311.txt)·[환경](phase-B6/environment.json)·[ZIP 해시/구성](phase-B6/kit-distribution.json) |
| `node docs/results/phase-B6/verify-browser.mjs` | Chromium **34페이지 × 1280/375/360px × 라이트/다크**, **3,699개 확인**. 내부 링크/앵커 **826개**, 숫자가 붙은 장/실습 참조 **478개**, 이전/다음 순서 일치. 가로 넘침·콘솔·페이지·내부 HTTP 오류 **0**. [JSON](phase-B6/browser-check.json)·[번호 참조](phase-B6/numbered-references.json) |
| `node docs/results/phase-B6/verify-final.mjs` | 최종 옛 주소→완성 본문, 실험실 선택 주소 복원과 13개 원본 도구의 실제 키보드 입력 **19개 통과**, 오류0. [JSON](phase-B6/final-browser-check.json) |
| 구문·차이 확인 | `node --check` book.js/lab.js, 변경 범위 `git diff --check` 통과. `blog-kit/`·`auto-kit/` tracked diff 없음 |

브라우저는 목차 Enter/Escape·초점 복귀, 실험실 13원본의 세 폭/두 테마·가로 넘침·테마·초점, 18개 프롬프트 Enter 복사와 내용, 용어 검색/앵커/tooltip Escape, 실습↔E2E 진행·주소 복원, 저장/클립보드 차단 대안, JS 없는 목차·본문·부록, 동봉 샘플 로딩을 검사했다. 링크 숫자는 JS가 만든 메뉴·선행 장·이전/다음·출처 복귀까지 포함한다. 본문의 일반 문장에 있는 장/실습 참조도 읽어 주제와 번호를 대조했다.

초기 검사에서 샘플의 기본 favicon 요청 404를 고쳤다. 지연 로딩 이미지는 실제 로딩 후 판정하도록 검증 코드를 수정했다. 문체 검사에서 표지의 ‘1장부터’가 ‘장부’로 잡힌 문구와 출처 메타의 내부 작업명도 독자용 표현으로 정리했다. 최종 수치는 수정 후의 결과다.

재현은 저장소 루트에서 `python3 -m http.server 8636 --bind 127.0.0.1` 후 위 두 브라우저 코드를 실행한다. 기존 Playwright/Chromium 설치 경로를 사용하며 새 Python 가상환경의 개발 테스트 패키지만 `/tmp`에 설치했다. 운영 의존성은 늘리지 않았다.

## 화면과 남은 확인

대표 화면을 실제 이미지로 열어 모바일 글자·여백·다크 대비·비용 예·프롬프트·샘플을 점검했다.

- [표지 1280 라이트](phase-B6/index-1280-light.png) · [375 라이트 전체](phase-B6/cover-full-375-light.png) · [360 다크](phase-B6/index-360-dark.png)
- [AI 제작·질문별 진입](phase-B6/index-ai-start-1280-light.png) · [키트 미리보기](phase-B6/index-kit-sample-1280-light.png)
- [글 1편 비용 · 375 라이트](phase-B6/ai-models-per-article-375-light.png) · [후기 프롬프트 · 360 다크](phase-B6/prompts-review-360-dark.png) · [실험실 계획 도구 · 360 다크](phase-B6/lab-plan-360-dark.png)

B7 초보자 독립 검토, Claude Code 최종 검수·커밋·배포가 남아 있다. 현재 사이트의 ‘완성’은 원고·도구·통합 구현 상태다. Windows/macOS 실기기, 실제 계정 가입·모델 실행·발행·검색/광고 신청·심사·정산, OAuth 발급/갱신·live·OS 예약 등록은 검증하지 않았다.

수정 범위는 `site-blog/`, 부록 생성기/검사, 블로그 연구·결과·현재 상태와 `shelf/` 블로그 카드·진행 상태다. `site/`·`site-shorts/`·`auto-kit/` 및 병렬 작업자의 변경을 편집하거나 되돌리지 않았다. 공통 문서는 블로그 항목만 갱신했다.

완료 알림: `python3 scripts/notify.py`로 위 요약 5줄과 표지 1280 라이트 스크린샷을 디스코드에 첨부 전송했고 **HTTP 200**을 확인했다.
