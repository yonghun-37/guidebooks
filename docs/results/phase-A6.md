# A6. 심화편 독립 검토 수정 + 최종 게이트

2026-10-26 · Codex. 입력은 [A5r 발견 사항](phase-A5r-findings.md)·[채점표](phase-A5r-scorecard.md)다. **차단 4·혼란 10·사소 2, 총 16건을 코드·본문·질문표·견본에 반영했고 로컬 최종 게이트를 통과했다.** 실계정 구축 성공·사람의 청취 감수 완료를 뜻하지 않는다.

## 발견별 처리

| 발견 | 처리와 남는 동작 | 검증·근거 |
|---|---|---|
| F01 차단 · 공개 호스팅 | 인스타 A5에 무료 교육용 Pages 계정→별도 public 저장소→media 브랜치→Pages 배포→대상 repo Contents 쓰기 PAT→`.env`→완성 hosting JSON→doctor→공개 파일 열기 절차·화면 도식. R2는 bucket/endpoint/공개 URL/키 대응과 결제·운영 조건을 별도 안내. README·연결 안내도 같은 경로 | [호스팅 실습](../../site/advanced/05-publish.html#hosting-pages), A162~164. doctor가 호스팅 필드·키 존재를 검사하는 회귀 및 기존 Pages/R2 어댑터 모킹 통과. 원격 업로드 미실행 |
| F02 차단 · TTS 키 | Cloud 프로젝트·결제 연결·API 활성화·standard key·API/IP 제한·`.env`·doctor·짧은 WAV 시험을 OAuth/Gemini와 구분. 직접 그린 화면 위치 그림과 모델 설정. 인스타 선택 음성은 쇼츠 절로 연결 | [발급](../../site-shorts/advanced/02-credentials.html#google-tts)·[WAV 시험](../../site-shorts/advanced/03-generation.html#tts-test). A165/166/171/172. 실제 어댑터 요청/헤더와 대조, 실제 키 발급·합성 호출 미실행 |
| F03 차단 · 인코딩 | 쇼츠 A3/A5/A6 등 JSON 읽기에 `encoding='utf-8-sig'`. 키트 `inspect`는 `read_json` 사용 | 비 UTF-8 기본 인코딩·UTF-8 stdout 환경에서 한국어 JSON 조회 회귀, 본문 명령 재현 |
| F04 차단 · 잘못된 결과 선택 | 쇼츠 A0부터 `private/shorts-demo`와 실제 RUN_ID를 끝까지 연결. glob 첫 파일 선택 제거. 키트 `inspect ID --flow ... --artifact ...`가 지정 ID의 flow까지 확인 | README 같은 상태에서 두 흐름 생성→쇼츠 문안/계획 조회 성공. 잘못된 flow 거절 회귀. 게시 결과는 DB에서 읽고 YouTube 내부 `status`도 JSON으로 출력 |
| F05 혼란 · 옛 오류 | 재개 시 현재 reason/failed_step 제거, 새 실패면 새 이유 기록. 과거 실패 이벤트 유지. 두 책 성공 안내 동기화 | 없는 폰트→실패→파일 복구→같은 ID dry_run, 원문·대본 바이트 유지·옛 오류 없음·실패 이벤트 보존 회귀 |
| F06 혼란 · 예외 종결 | 두 책 A6·README에 시험 민감어→실제 exception→이유 확인→approve 거절→원인 수정·새 실행 재검사→옛 미게시 ID reject→report 예외0. DB 삭제 없이 기록 보존. uncertain은 별도 조회/대조 | 두 흐름 실제 CLI와 pytest로 종결 재현. 의도된 exception exit2·approve exit1을 정상 단계와 구분 |
| F07 혼란 · 사후 확인 시계 | 두 플랫폼 모두 **실행 시작부터** 기본 2시간. created_at과 정확히 같은 시각 기준으로 publish_at 계산. 인스타 09:17 시작→11:17 예정 도식·본문·키트 안내 통일 | 두 흐름 제작 3분 경과 후 예정시각=시작+2시간, 남은 검토=1시간57분 회귀. tick 지연을 별도 설명 |
| F08 혼란 · 메신저 | Discord 서버 Integrations→webhook/channel/URL→`.env`→게시 없는 시험 알림. Telegram BotFather→개인 메시지→from/chat 숫자 ID→허용자 설정. 화면 도식·수신자 역할·최대25초 1회 수신·PowerShell/Bash 반복 루프·다음 tick/resume 발행 설명 | A167/168·기존 A067. 알림/ID조회 코드 모킹·구문 대조. PowerShell 문제였던 JSON 리터럴을 `json.dumps`로 교체. 실제 메신저 전송 미실행 |
| F09 혼란 · 토큰 우선순위 | private 토큰>환경변수>`.env` 우선순위 명시. `python -m ops.tokens import-instagram --config config.json`으로 새 환경 자격을 실제 private 저장 위치에 적용. 예약 중지·Secrets/외부 상태 동기화 순서 | 가짜 만료 private 토큰/새 환경 토큰으로 재현→명시적 적용 후 새 토큰 사용·0600·값 미출력. 잘못된 새 시각은 기존 파일 유지 |
| F10 혼란 · 소재 수 | 보유 소재 2~5개를 파일명 순서로 고르고 그 개수를 LLM 요청·스키마 장면 수에 고정. 다른 수가 오면 대본 단계에서 예산 내 재시도, 계속 실패면 렌더/TTS 전에 중단. mock도 같은 개수로 구성 | 2·3·5개 소재 대본/렌더 일치 및 5장면 잘못된 응답→3장면 재시도 회귀. 두 책 새 설명과 일치 |
| F11 혼란 · 전자동 기준 | 공통 교육 권장값: 승인제 10편 중9편 통과→사후 확인 다음10편 모두 통과·잘못 공개/거부/실행 오류0·미해결 예외0→사용자 수동 auto 전환. 두 책 표·그림·FAQ·E2E·README 통일 | 본문/도식 대조. 자동 승격·플랫폼 안전 보장으로 설명하지 않음 |
| F12 혼란 · 질문 대응 | 질문표 A6를 플랫폼별 관문 5문항, A7을 운영 핵심/노코드 선택 질문으로 정리. 인스타 A6 FAQ 교체·A8 views/engagedViews/평균시청시간 직답·상대 책 연결 | [질문표](../learner-questions-advanced.md), 인스타 A6/A8·쇼츠 A6 본문 대조. 질문마다 답/예/행동이 있는지 확인 |
| F13 혼란 · 무료 매일 운영 | 무료 Gemini 한국어 글 생성은 소규모로 시도 가능하나 매일 성공·전체0원 보장 아님을 직답. Flash-Lite Free Tier·프로젝트 active RPM/TPM/RPD·무료 데이터 이용·민감정보 제외·1편 검수·소진 대안 연결. TTS/영상 별도, 무료 잔량은 키트 비용 예약에서 차감하지 않음 | A028/169/170, [연결 근거](../../research-advanced/a6-connections.md). 고정 RPD 수치를 만들지 않음. 결제 미연결 LLM 확인을 결제 연결 TTS의 강제 상한으로 확대하지 않음 |
| F14 혼란 · 완성 목표 | 기존 신호음 기능 샘플 유지. 별도 편집 견본에 인스타 생활정보 카드4장·한국어 낭독 쇼츠38.667초·장면/자막8개·원고·재현 스크립트·권리 기록. 양쪽 A4에서 실제 웹 파일 열기/재생 | [완성 견본](../../auto-kit/samples/editorial/README.md). 프레임·전체 디코딩·자막·음량·ASR 대조, Python3.11 깨끗한 복사본 재생성. **사람의 녹음·최종 감수로 가장하지 않으며 사람 청취 미실행** |
| F15 사소 · 모바일 비용 | 쇼츠 차트 폭/글자 배치 조정, 같은 핵심 금액을 HTML 텍스트에도 제공. 일부 개요 도식 모바일 글자 보강 | 360/375/1280 양테마 검사, 비용 극단값·금액 HTML 표시/글자 크기 확인 |
| F16 사소 · 표기 | 두 책 어색한 목적격 조사 수정. RUN_ID는 문자 그대로 복사하는 값이 아니라 실제 12자리 ID라고 설명 | 원고 대조·문체 검사 통과 |

## 코드 검토와 구현 범위

`auto-kit/docs/plan.md`의 기존 feature 기록을 이어 쓴 Level 2 수정이다. 구조·배포·기본 의존성을 바꾸지 않아 ADR을 만들지 않았다. 주 작업자는 키트·README·연구·질문표·통합 문서, 별도 작업자는 각 책 HTML/전용 자산과 견본을 소유했다. 공통 CSS/JS·서가·입문편은 변경하지 않았다. 쇼츠 `advanced.css/js`만 해당 책 심화편 숫자 표시를 위해 수정했다.

독립 코드 리뷰에서 새 `inspect result`가 없는 result.json을 읽는 문제, 실제 YouTube 응답의 내부 status를 실행 상태로 오인하는 문제, PowerShell JSON 따옴표 문제를 찾았다. 모두 수정했다. 두 코드 결함은 각각 실패 회귀를 확인한 뒤 통과시켰고 가짜 YouTube 결과 CLI도 독립 재현했다. 추가 미해결 Critical/Important는 검토 범위에서 발견되지 않았다. 최종 리뷰는 실계정 실행의 대체 증거가 아니다.

추가 공식 근거는 `research-advanced/SOURCES.md` A162~174와 FACT-SHEET ADV-085~089, `a6-connections.md`에 남겼다. 기존 A1 조사를 보완하는 직접 열람이며 새 Hermes 질의는 실행하지 않았다. TTS의 API 키 지원은 **서비스 자체의 v1 Discovery parameters.key**와 Cloud REST 헤더 문서로 함께 대조했다. 음성 모델 원문 라이선스는 동봉 사본과 바이트 일치를 확인했다.

## 최종 게이트

| 게이트 | 실행 결과 | 영구 기록 |
|---|---|---|
| Python3.11 설치·pytest | 원본을 `/tmp/ai-insta-a6-gate/auto-kit`에 복사(.venv/private/.env/cache 제외), Python **3.11.15** 새 venv, README 바이너리 설치 명령 성공. 최종 전체 **93 passed**, 실제 외부 연결은 pytest fixture가 차단 | [pytest](phase-A6/pytest.txt), [회귀](../../auto-kit/tests/test_a6_regressions.py) |
| README 명령 재현 | 새 venv의 Python으로 `tests/check_readme.py` 실행, 추가 깨끗한 복사본에서 **31개 명령**·로컬 링크110개 오류0. run/승인/재개/거부/혼합 상태 조회/예외 생성·종결/보고·예약 생성 포함. live 명령은 실행하지 않음 | [재현 도구](../../auto-kit/tests/check_readme.py)·[실제 출력](../../auto-kit/docs/verification/commands.json) |
| 두 책 실습 변화 | 인스타/쇼츠 담당자가 별도 임시 복사본에서 변경 명령·실제 예외 종결·시계·비 UTF-8을 확인. ROOT 회귀/README로 핵심 동작을 재확인 | 발견별 표와 테스트, 임시 실행 경로 `/tmp/a6-insta-verify`, `/tmp/shorts-a6-review` |
| 문체 | 심화편 **22/22 통과**, 금지어/내부 용어0. 신규 실습 원고라 개편 전 이론 축약 기준선은 적용하지 않음 | [문체 JSON](phase-A6/style-lint.json) |
| 사이트 정적 | `check_site --site site`, `--site site-shorts` 각각 **errors=[]**. 사이트 전체 51/49 HTML·상대 링크·앵커·그림 캡션 검사 | [ReelsBook](phase-A6/check-site.json)·[ShortsBook](phase-A6/check-shorts.json) |
| 브라우저 | Chromium 심화22페이지×1280/375/360×라이트/다크=**132화면**. 가로 넘침·깨진 이미지·SVG 텍스트 경계·콘솔/페이지/내부HTTP 오류0. 배포 구조의 내부 링크/앵커 **608개** 오류0 | [재현 스크립트](phase-A6/verify-browser.mjs)·[화면/상호작용 JSON](phase-A6/browser.json), 같은 폴더의 대표 모바일 양테마 PNG |
| 키보드·미디어 | OS 탭/퀴즈/체크 저장·삭제를 키보드로 조작, 비용 극단값·관문 실패·외부 상태 없는 실행 선택, 기존/편집 영상 실제 재생 등 **18개 확인 통과** | browser.json interactions |
| 완성 견본 | 동봉 음성으로 Python3.11/Pillow13 복사본에서 카드/MP4 재생성. 최종원본 H.264/AAC·1080×1920·38.667초·−16.25LUFS. 8문장 로컬 ASR와 대본 대응, 4카드/8프레임 검토·웹 복사 해시·전체디코딩 통과 | [견본 측정](../../auto-kit/samples/editorial/verification.json)·[생성기](../../auto-kit/examples/build_editorial.py) |

브라우저는 실제 Pages 경로처럼 `/reels/`·`/shorts/`를 제공하는 로컬 서버에서 확인했다. 외부 웹폰트는 차단/대체했으며 자체 페이지의 오류와 구분했다. 원고 변경 후 최종 정적·문체·132화면을 다시 실행했다. 독립 리뷰 후 코드 변경 뒤 전체 pytest를 다시 실행했다. `git diff --check` 오류0이다.

## 남은 확인과 인계

- Windows/macOS 실기기·PowerShell 자체 실행·OS 예약 등록/다음날 동작은 미실행이다. 공통 Python 명령과 예약 파일 생성만 검증했다.
- 신규 유료 키·결제·실계정 로그인/게시·TTS/LLM 실생성·Pages/R2 원격 업로드·실제 메신저 전달은 수행하지 않았다. 사용자 환경의 키 발급·권한·첫 private/시험 게시·공개 URL·청구 대조는 별도다.
- 완성 견본은 사람이 다듬을 목표를 보여 주는 Codex 편집·로컬 합성음 예다. **사람의 최종 청취와 게시 적합성 감수는 남아 있다.** 자연스러운 호흡·강조를 기계 역전사만으로 확인했다고 주장하지 않는다.
- `docs/PROJECT_STATE.md`·키트 feature 기록·질문표를 갱신했다. commit/push하지 않았다. Claude Code 최종 검수·커밋·배포가 남아 있다.
- 완료 보고: `python3 scripts/notify.py "✅ [A6 심화편 수정·게이트 완료] ..."` 실행, Discord HTTP 200으로 전송 확인. 토큰 출력 없음.
