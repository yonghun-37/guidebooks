# Phase V-insta — ReelsBook 시각자료 보강 결과

2026-10-26 완료. 기준은 수정된 `docs/STYLE-GUIDE.md` 6절과 [페이지별 계획](phase-V-insta-plan.md)이다. 그림의 개수 조건을 폐기하고 이해 효과로 선별했다. 이전 `phase-V-insta-before.md`의 최소 수량 표는 이번 작업에 적용하지 않는다.

## 구현

- 중단된 작업이 추가·포장한 206개 figure 중 유용한 **수수료·구독 조합·행동 비율 차트와 승인 흐름 4개**를 계승·개선했다. 나머지 202개는 삭제하거나 일반 내비게이션으로 되돌렸다. 기존 본문·내비·입력·퀴즈·43개 진행 키는 유지했다.
- 최종 38개 figure는 기존 결과 예시 8개(일부 반응형 개선), 위 4개, 계획에 따른 26개 추가·기존 표의 시각화로 구성된다. 이 숫자는 작업 목록이며 품질 조건이 아니다. 기획·로드맵·검수·E2E·용어집·실험실 등은 기존 도구·표·설명으로 충분해 그림을 더하지 않았다.
- 화면 위치 그림은 직접 그린 틀과 번호로 입력·결과·확인 위치를 설명한다. 실제 서비스의 배치·로고를 재현하지 않았다. 각 캡션에 설명용 위치·조사 기준월·관련 원문 각주를 달았다.
- `site/assets/figures.css`: figure·단계 띠·동일 크기 비교·파일 구조·차트·번호·두 테마. `site/assets/img/fig/screen-frame.svg`: 실제 화면 도식에서 공유하는 화면/번호 symbol. `book.css`에서 공통 CSS를 불러온다.
- 새 가격·정책·성과 수치를 만들지 않았다. 구독·수수료·API·표시·인사이트 그림은 본문과 동일한 출처를 캡션에 연결했다. 원래 가상 수치와 계산식을 유지했다. 카드 5장 역할과 레시피 선택은 기존 문장·표만으로 충분해 별도 그림을 추가하지 않았다.
- 기존 AI 삽화 `library-evening.webp`(109,058바이트), **AI 생성 예시** 고지와 바로 뒤의 사용 프롬프트는 유지했다. 새 AI 이미지는 생성하지 않았다. 의무 인물 삽화 27개(기준 시트 포함)와 쓰이지 않은 `paper-robot.webp`를 삭제했다. 삭제한 신규 파일은 총 28개다.

## 유지·개선한 그림

| 원래 자료 | 최종 처리 |
|---|---|
| 표지 지도·동봉 카드 PNG·릴스 MP4 | 기존 3개 figure와 캡션·재생 유지 |
| 8장 도서관 AI 삽화 | 기존 이미지·고지·프롬프트 유지 |
| 실습 0·4·5 파일 전달 SVG | 같은 입력·서비스·출력을 모바일에서 읽히는 HTML 단계 띠로 변경 |
| 실습 5 첫 확대 키프레임 | 0초 100%→끝 105%, 4초라는 연습값을 유지하고 축소되던 글자 개선 |
| 이전 그림 3-7 | 인정 구매 1건/20건 수수료 막대 유지·관련 각주만 남김 |
| 이전 그림 6-6 | 구독 구성 요소와 합계를 누적 막대로 개선 |
| 이전 그림 10-4 | 검수→승인→드라이런 흐름을 반응형으로 유지·원래 본문 흐름을 캡션으로 이동 |
| 이전 그림 12-7 | 가상 A/B의 비율뿐 아니라 행동 횟수도 나란히 비교 |

## 추가·기존 표를 시각화한 그림 목록

`site/` 기준이다. 유지·개선 항목과 구별한 세부 ID·캡션은 [전체 감사 기록](phase-V-insta/figure-audit.json)에 있다.

| 페이지 | 최종 그림 |
|---|---|
| `ai-models.html` | `visual-card-cost` |
| `chapters/01-map.html` | `visual-human-check` |
| `chapters/02-formats.html` | `visual-aspect-ratios` |
| `chapters/03-revenue.html` | `visual-affiliate` |
| `chapters/05-sources.html` | `visual-rights-branch` |
| `chapters/05b-ai-tools.html` | `visual-tool-handoff`, `visual-budget` |
| `chapters/06-writing.html` | `visual-summary-compare` |
| `chapters/07-cards.html` | `기존 결과 예시`, `visual-card-compare` |
| `chapters/08-reels.html` | `visual-crop-compare` |
| `chapters/09-pipeline.html` | `visual-pipeline-files`, `visual-approval` |
| `chapters/10-publishing.html` | `visual-api-sequence`, `visual-two-clocks` |
| `chapters/11-analytics.html` | `visual-count-ratio` |
| `chapters/12-safety.html` | `visual-ad-disclosure` |
| `chapters/14-plan.html` | `visual-move-task` |
| `index.html` | `기존 결과 예시`, `기존 결과 예시`, `기존 결과 예시` |
| `practice/00-start.html` | `visual-file-handoff` |
| `practice/01-account.html` | `visual-account-screen`, `visual-security-screen` |
| `practice/02-setup.html` | `visual-kit-folders`, `visual-kit-result` |
| `practice/03-copy.html` | `visual-chat-screen` |
| `practice/04-cards.html` | `visual-canvas-screen`, `visual-file-handoff`, `visual-download-screen` |
| `practice/05-reel.html` | `visual-keyframes`, `visual-file-handoff`, `visual-timeline-screen` |
| `practice/07-publish.html` | `visual-gallery-screen`, `visual-publish-screen` |
| `practice/08-api.html` | `visual-hosting-boundary` |
| `practice/09-schedule.html` | `visual-daily-folders` |
| `practice/10-insights.html` | `visual-insights-screen` |

## 제거한 이전 그림 목록

아래 ID는 중단 작업의 번호다. 일반 내비를 감싼 figure는 포장만 없애고 원래 링크를 보존했다. 전 장·전 실습의 인물 그림, 제목을 되풀이한 흐름도, 매 단계에 반복한 범용 화면, 결과 목록을 다시 적은 그림, 본문만으로 충분한 비교를 제거했다. 각 캡션·처리 이유와 삭제 자산의 전체 경로는 감사 기록을 따른다.

| 페이지 | 제거 또는 figure 포장 해제한 이전 ID |
|---|---|
| `ai-models.html` | 모델-1 |
| `chapters/01-map.html` | 1-1, 1-2, 1-3, 1-4, 1-5, 1-6, 1-7, 1-8 |
| `chapters/02-formats.html` | 2-1, 2-2, 2-3, 2-4, 2-5, 2-6, 2-7, 2-8 |
| `chapters/03-revenue.html` | 3-1, 3-2, 3-3, 3-4, 3-5, 3-6, 3-8 |
| `chapters/04-niche.html` | 4-1, 4-2, 4-3, 4-4, 4-5, 4-6, 4-7, 4-8 |
| `chapters/05-sources.html` | 5-1, 5-2, 5-3, 5-4, 5-5, 5-6, 5-7 |
| `chapters/05b-ai-tools.html` | 6-1, 6-2, 6-3, 6-4, 6-5, 6-7 |
| `chapters/06-writing.html` | 7-1, 7-2, 7-3, 7-4, 7-5, 7-6, 7-7 |
| `chapters/07-cards.html` | 8-1, 8-2, 8-3, 8-4, 8-5, 8-7, 8-8 |
| `chapters/08-reels.html` | 9-1, 9-2, 9-3, 9-4, 9-5, 9-6, 9-7 |
| `chapters/09-pipeline.html` | 10-1, 10-2, 10-3, 10-5, 10-6, 10-7 |
| `chapters/10-publishing.html` | 11-1, 11-2, 11-3, 11-4, 11-5, 11-6, 11-7, 11-8 |
| `chapters/11-analytics.html` | 12-1, 12-2, 12-3, 12-4, 12-5, 12-6, 12-8 |
| `chapters/12-safety.html` | 13-1, 13-2, 13-3, 13-4, 13-5, 13-6, 13-7, 13-8, 13-9 |
| `chapters/13-roadmap.html` | 14-1, 14-2, 14-3, 14-4, 14-5, 14-6, 14-7, 14-8 |
| `chapters/14-plan.html` | 15-1, 15-2, 15-3, 15-4, 15-5, 15-6, 15-7 |
| `credits.html` | 출처-1 |
| `glossary.html` | 용어-1 |
| `index.html` | 표지-1 |
| `lab.html` | 실험-1 |
| `practice/00-start.html` | 실습0-1, 실습0-2, 실습0-3, 실습0-5, 실습0-6 |
| `practice/01-account.html` | 실습1-1, 실습1-2, 실습1-3, 실습1-4, 실습1-5, 실습1-6, 실습1-7 |
| `practice/02-setup.html` | 실습2-1, 실습2-2, 실습2-3, 실습2-4, 실습2-5, 실습2-6, 실습2-7 |
| `practice/03-copy.html` | 실습3-1, 실습3-2, 실습3-3, 실습3-4, 실습3-5, 실습3-6, 실습3-7, 실습3-8, 실습3-9, 실습3-10, 실습3-11 |
| `practice/04-cards.html` | 실습4-1, 실습4-2, 실습4-3, 실습4-4, 실습4-6, 실습4-7, 실습4-8, 실습4-9, 실습4-10 |
| `practice/05-reel.html` | 실습5-1, 실습5-2, 실습5-3, 실습5-4, 실습5-7, 실습5-8, 실습5-9, 실습5-10, 실습5-11 |
| `practice/06-review.html` | 실습6-1, 실습6-2, 실습6-3, 실습6-4, 실습6-5, 실습6-6 |
| `practice/07-publish.html` | 실습7-1, 실습7-2, 실습7-3, 실습7-4, 실습7-5, 실습7-6, 실습7-7, 실습7-8 |
| `practice/08-api.html` | 실습8-1, 실습8-2, 실습8-3, 실습8-4, 실습8-5, 실습8-6, 실습8-7 |
| `practice/09-schedule.html` | 실습9-1, 실습9-2, 실습9-3, 실습9-4, 실습9-5, 실습9-6, 실습9-7, 실습9-8 |
| `practice/10-insights.html` | 실습10-1, 실습10-2, 실습10-3, 실습10-4, 실습10-5, 실습10-6 |
| `practice/e2e.html` | 전체-1, 전체-2, 전체-3 |
| `prompts.html` | 요청-1 |

## 검사기

`scripts/check_site.py`에서 수량 minimum·shortages·집계 반환값·`--fig-warn`을 제거했다. 캡션·의미 있는 img alt·SVG의 접근 가능한 이름과 기존 구조·링크·각주·퀴즈·진행 검사를 유지했다. site-blog의 배포/출처 경로 지원을 유지했다.

좌표·크롭용 중첩 SVG는 이름 있는 바깥 그림의 일부로 검사하며 독립 `role="img"`에는 자체 이름을 요구한다. 쇼츠의 `API480` 같은 제품 표기를 출처로 오인하지 않도록 기존 Y 출처 패턴을 유지했다. 블로그 사이트는 아직 없어 임시 fixture로 지원을 검증했다.

## 검증 결과

- `style_lint`: 고정 기준선 25파일 + 기타 본편/부록 8파일 **모두 통과**. 기준선은 바꾸지 않았다. 금지어·내부 용어 0. 기존 본문을 줄여 그림 자리를 만들지 않고 기존 정보를 재배치·캡션 중복을 줄였다.
- `check_site(site)`: 40 HTML(서가 포함), 내부 참조 3,430개·도구 31개·진행 키 43개·퀴즈 57문항, **오류 0**. `check_site(site-shorts)`: 검사 당시 38 HTML(서가 포함), **오류 0**. 쇼츠 원고는 수정하지 않았다.
- 기존 검사기 회귀 **29 tests 통과**. 추가 검증 **90항목 통과**: 수량 무관 통과·빈 캡션/alt/SVG 이름 거부·중첩 SVG·site-blog·기존 인터랙션 속성·기존 HTML 앵커 보존. 교체한 SVG 내부 title/desc ID는 새 구조에 맞췄다.
- Chromium: **ReelsBook 전체 38 HTML × 1280/375/360px × 라이트/다크**, 접힌 내용 펼치기·그림 경계·글자 크기/잘림·이미지 로드·퀴즈 키보드/초기화 **1,176항목 통과**. 가로 넘침·콘솔·페이지·로컬 HTTP 오류 **0**. 새 공통 그림은 본문/그림 글자 약 14px 이상을 확인했다(각주 제외).
- 카드 비교의 모바일 폭 넘침과 AI 도구 띠의 작은 글자를 수정하고 전체 화면 검사를 재실행했다. 대표 화면은 직접 열어 라이트/다크·크롭·타임라인·파일 선택·카드 비교를 확인했다.
- 자동 스크린샷 56장과 카드 비교 수동 확인 1장을 [검증 폴더](phase-V-insta/)에 보관했다. [모바일 카드 비교](phase-V-insta/card-compare-360-light.png), [데스크톱 다크 타임라인](phase-V-insta/site-practice-05-reel-visual-timeline-screen-1280-dark.png).
- 키트·기존 research·STYLE-GUIDE의 시작 시점 파일 해시가 그대로임을 확인했다. 다른 작업자가 진행 중인 쇼츠·심화/블로그 자료는 덮어쓰지 않았다. commit/push·결제·실계정 로그인/게시를 하지 않았다.

## 재현과 남은 확인

재현 명령은 [commands.md](phase-V-insta/commands.md), 결과는 `check-site.json`, `check-shorts.json`, `style-*.json`, `static-regression.json`, `browser-check.json`, `script-tests.txt`에 있다. 검증 코드는 같은 폴더의 `verify-static.py`, `verify-browser.mjs`다. 브라우저 코드는 이 환경의 기존 Playwright·Chromium을 사용한다.

로컬 제작·렌더링 검증을 마쳤다. Claude Code의 최종 검수·커밋·배포는 남아 있다. 실제 서비스 화면·Windows/macOS·휴대폰 계정 조작 검증은 이번 작업 범위에 포함하지 않았다.
