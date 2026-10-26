# Phase A4 결과 — ShortsBook API 완전 자동화 심화편

2026-10-26 · Codex. **A0~A9·통합 체크리스트 집필·구현과 오프라인/브라우저 검증 완료. Claude 검수 및 A5 독립 검토 대기.** 실계정 업로드·유료 생성·실기기 예약 성공을 뜻하지 않는다.

## 요구와 구현 방식

- 문제: 실습편의 한 편 제작에서 주제 선정→생성→자동 관문→게시→분석→다음 주제 반영까지 연결하는 코드 중심 학습 경로가 필요했다.
- 기준: AGENTS, pipeline·writing·OpenAI Docs 스킬, STYLE-GUIDE 최우선, DESIGN-advanced, 학습자 질문, 연구 브리핑·사실표·출처·노트, A1/A2 결과와 실제 auto-kit 코드·출력, 기존 쇼츠 공통 자산·실습 장·E2E를 대조했다.
- 정적 HTML·바닐라 JS·기존 색 변수/내비게이션을 재사용했다. 새 의존성·사이트 빌드·키트 변경은 없다. 단계 결과 문서를 기존 프로젝트의 기능 기록으로 사용한다.
- [x] 실제 mock 실행과 출력 대조
- [x] A0~A9·E2E 집필, 그림·계산·분기 도구 구현
- [x] 세 번째 트랙·용어·A 출처 통합
- [x] 문체·정적·브라우저·키보드·보존 검증과 결과 기록

## 변경한 내용

- [심화편 시작](../../site-shorts/advanced/00-overview.html): 11 HTML. 각 페이지에 만드는 결과·먼저 답·직접 그린 도식·실행 명령 Windows/macOS 탭·실제 mock 성공 표시·오류 표·편당/월 비용·확인할 점·FAQ 5개·퀴즈 3개를 넣었다.
- 예시: 가상 채널 「자취생 10분 생존법」의 「월급날 10분, 돈을 네 칸으로 나누기」를 원문→대본→영상→게시 요청→가상 지표까지 이어 썼다. 콘솔 캡처·실존 브랜드·성과 숫자를 만들지 않았다.
- A0: 클릭형 전체 파이프라인, 첫 권장 조합(Luna+보유 소재+WaveNet+ffmpeg), 가상 월 30편 생성비 $0.096. 무료량·세금·충전·고정비와 계산 가정을 분리했다.
- 운영 전환: 첫 1~2주 승인제, 최근 고유 실행 10편 중 9편 통과·미해결 예외 0건이면 사후 확인, 최근 20편 중 19편 통과·미해결/잘못 공개 0건이면 전자동을 고려한다. 플랫폼 규정이 아닌 제안 기준으로 표시하고, 산식·직접 설정 변경·오류 공개 시 복귀를 안내했다.
- A1~A4: 상태 전이/재개·폴더 구조, OAuth Testing 만료·키 저장·공급자/키트 비용 상한, 구조화 JSON·실제 스키마·TTS·이미지/영상 API·로컬/RSS 원문 입력, ffmpeg·대본 기반 자막·폰트/소재 권리를 다룬다.
- A5: Desktop OAuth·scope·실제 채널, private 시험·API 감사·상충하는 비공개 잠금 안내, 현행 granular quota와 로컬 cap, Location/308/Range 재개, 요청·응답 시퀀스·가린 토큰, publishAt·AI/아동용 필드·예약 취소를 안내한다.
- A6~A9: 관문별 통과/예외와 우회 금지, 로컬/Actions 선택·하루 타임라인·외부 암호화 상태/lease·승인/알림, Analytics의 단위·missing·현재 주제 점수 산식, 반복/재사용·AI 공개·권리·유출 중지/복구를 안내한다. 노코드는 A7 상자로만 다룬다.
- 시각자료 **18개**(SVG·비용 차트·실제 mock MP4). 장면 수·기간·비용을 장식 목적으로 늘리지 않았다. 계산기·관문 모드 분기·실행 방식 고르기는 네트워크를 호출하지 않는다.
- [완료 체크](../../site-shorts/advanced/e2e.html): mock·문서/설정·사용자 실계정 증거를 나누고 첫 자동 게시의 ID·주소·검사·비용·분석·다음 주제 기록 양식을 제공한다. 기존 실습편과 다른 `shortsbook:advanced:v1` 키로 진행을 보관한다.
- [전용 CSS](../../site-shorts/assets/advanced.css)·[JS](../../site-shorts/assets/advanced.js). 공통 변경은 `book.js`의 새 트랙/장/URL·현재 장 구분, 표지 연결, 용어 9개, 크레딧 A 출처 **53개**뿐이다. `book.css`·`practice.js`·`sim/common.js`는 변경하지 않았다.

## 실행·검증

| 검사 | 실제 결과·증거 |
|---|---|
| 깨끗한 키트 복사 | `/tmp/shorts-a4-auto-kit`에서 실행. 원본 키트 수정 없음. 기존 `/tmp/auto-kit-a2-venv` Python 3.11.15·설치된 의존성을 사용했다. [CLI 17회 기록](phase-A4/kit-commands.json) |
| mock 완주 | 실제 shorts auto → `dry_run`; approval → `waiting_approval` → approve → resume → `dry_run`; 반복 resume; post_review → `scheduled` → reject → `rejected`; 지표·보고·3 OS 예약 파일 생성·tick 하루 1회 확인 |
| 출력 | 실제 1080×1920·30fps·H.264/AAC·36.1초·-16.05 LUFS. `request-plan.json`: `dry-run`, `network_calls:0`, `Bearer <REDACTED>`. 실제 파일을 advanced/examples/에 MP4·SRT로 동봉 |
| 인쇄 명령 대조 | [본문 명령 6회(중복 OS 포함)](phase-A4/printed-command-check.json), [설정·로컬 RSS](phase-A4/config-rss-check.json), [관문 검사·실제 출력](phase-A4/gate-command-check.json). 숫자 관문 테스트 **4 passed** |
| 문체 | [style_lint](phase-A4/style-lint.json) **14/14 통과**(심화 11+공통 3), 금지어·내부 용어·상자 밖 단서 0. 새 트랙은 과거 축약 기준선 비교 대상 아님 |
| 정적 | [check_site](phase-A4/check-site.json) `--site site-shorts` 오류 0. 기존 검사기가 A 출처를 검사하지 않으므로 [심화 전용 검사](phase-A4/verify-content.py)로 등록·각주·URL·장 구조·범위 금지어를 별도 검사, [오류 0](phase-A4/content-check.json). FAQ 55·퀴즈 33 |
| 브라우저 | [재현 코드](phase-A4/verify-browser.mjs)·[결과](phase-A4/browser-check.json): **986개 확인**, 17페이지×3폭×2테마 **102개 조합**, 가로 넘침·SVG 글자 넘침·콘솔/페이지/내부 HTTP 오류 0, 동적 내부 링크 **283개** |
| 상호작용 | 비용 기본/이미지/초과/음수/공란/0/범위 밖, 관문 12조합, 실행 방식 분기, OS 탭 방향키/Home·복사·퀴즈 정답/오답/초기화, 메뉴 Enter/Escape, 테마 보존, 진행 교차 페이지 복원/삭제·기존 실습 보존, 저장 차단·JS 없는 읽기, 실제 MP4 메타데이터/재생 확인 |
| 추가 키보드·화면 | [집중 검사](phase-A4/focused-check.json): SVG 단계 링크 Enter 이동·네이티브 select 방향키 판정, API 시퀀스·파이프라인 3폭/2테마 캡처 |
| 변경 보존 | [보존 검사](phase-A4/content-check.json): 키트·research-advanced **1,996개 파일** 해시 유지. 쇼츠 공통 CSS·실습 JS·sim 공통 JS도 HEAD와 동일. 다른 작업자의 동시 수정은 회수/덮어쓰기하지 않음 |

전체 키트 pytest를 재실행한 결과로 보고하지 않는다. 이번 변경은 사이트 집필·전용 도구이며 관문 검증은 필요한 4개 테스트를 실제 실행했다. 설치 명령/OS 예약 생성은 Windows·macOS 실기기 성공과 구분한다. live 명령은 코드·공식 요건을 대조한 사용자 연결 절차이며 작업자가 실행하지 않았다.

대표 화면: [1280 라이트](phase-A4/representative-1280-light.png) · [375 라이트](phase-A4/representative-375-light.png) · [360 다크 전체 흐름](phase-A4/pipeline-360-dark.png) · [API 시퀀스](phase-A4/api-sequence-360-dark.png) · [비용 계산기](phase-A4/calculator-1280.png). 전체 장 라이트/다크 화면은 [검증 폴더](phase-A4/)에 있다.

## 근거·계획과 실제 구현 차이

- 연구 비용표의 600자·AI 이미지 6장은 견적 가정이다. 실제 키트 스키마는 2~5장면, 동봉 영상은 5장면·신호음이다. 원고에서 차이를 밝히고 스키마·키트를 변경하지 않았다.
- Analytics 기본 구현은 views·engagedViews·estimatedMinutesWatched다. 평균시청시간·수익은 공식 지표로 설명하되 기본 자동 수집으로 표시하지 않았다. 주제 선택은 현재 코드의 순서+카테고리 로그 평균 방식이다.
- 학습자 질문 원본 A6의 일정·알림·승인 질문은 설계 목차의 A7에서, 원본 A7의 노코드 질문은 A7 상자/FAQ에서 답한다. A6 본문/FAQ는 설계서의 자동 관문에 맞췄다. 인스타 질문은 쇼츠와 혼동하지 않도록 플랫폼 차이와 필요한 연결만 설명한다.
- 가격·핵심 규격은 research-advanced의 A 각주를 유지했다. 공식 [OpenAI 가격](https://developers.openai.com/api/docs/pricing), [insert](https://developers.google.com/youtube/v3/docs/videos/insert), [OAuth 만료](https://developers.google.com/identity/protocols/oauth2#expiration), [TTS 가격](https://cloud.google.com/text-to-speech/pricing), [재개 업로드](https://developers.google.com/youtube/v3/guides/using_resumable_upload_protocol), [Analytics query](https://developers.google.com/youtube/analytics/reference/reports/query), [Actions schedule](https://docs.github.com/en/actions/reference/workflows-and-actions/events-that-trigger-workflows#schedule)도 직접 대조했다. 연구 파일과 출처 번호는 바꾸지 않았다.

## 남은 확인·통합 요청

- A5 독립 초보 개발자 검토와 Claude 최종 검수·커밋·배포가 남아 있다. Codex는 commit/push하지 않았다.
- 사용자 본인 OAuth 발급/재동의·장기 만료 대응, 공급자 실청구·한국어 발음·실제 소재 권리, private/공개/예약 취소·잠금/감사·분석, OS 다음 날 실행·절전·Actions/R2 복구는 실계정/실기기에서 확인해야 한다. 신규 유료 키·결제·로그인·게시는 하지 않았다.
- `docs/PROJECT_STATE.md`·서가 진행표는 동시 작업자가 관리하고 있어 수정하지 않았다. 통합 담당자는 A4 작성·위 검증 완료와 A5/사용자 확인 미완료를 현재 상태에 반영하면 된다. `scripts/build_appendices.py`로 쇼츠 부록을 재생성할 때 수동 통합한 심화 용어·A 출처를 보존해야 한다.

완료 알림: 요청한 `scripts/notify.py`로 대표 1280px 스크린샷을 첨부해 전송했고 HTTP 200을 확인했다.
