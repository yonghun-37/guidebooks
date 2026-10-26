# Phase 7w — 인스타 실습편과 두 트랙

2026-10-26. Level 2 작업. 기존 Phase 결과 문서 관례를 재사용한다. 요구사항은 DESIGN 10·10.1과 사용자 Phase 7w 지시다. commit·push·실계정 로그인·게시·유료 API는 수행하지 않는다.

## 요구사항과 구현 계획

- [x] 기존 URL을 보존하면서 이론/실습 두 트랙과 표지 진입점을 만든다.
- [x] 실습 0~10·E2E 체크리스트, 공통 단계/OS 탭, 자체 SVG를 구현한다.
- [x] PRAC/API 근거와 미확인 앱 메뉴를 구분하고 7v 확인 목록을 남긴다.
- [x] 키트 버전 설정·로컬 .env·공개 미디어 준비 도우미·호환 CLI를 구현한다.
- [x] 이론 작업실의 조작 안내를 실습 링크로 옮긴다.
- [x] 전체 키트 시험, 깨끗한 복사본 실습 2~6, 브라우저 3개 폭·저장/키보드/링크를 검증한다.
- [x] 실제 결과·현황·진행 페이지·첨부 알림을 갱신한다.

## 구현 판단

실습의 외부 절차·수치는 `research/practice-instagram.md`와 `FACT-SHEET.md`의 확인 범위를 따른다. 계정 수·이메일 별칭·한국 앱 버튼 등 근거 공백을 사실로 보완하지 않는다. 사이트는 정적 HTML과 기존 공통 JS를 사용하며 단계 문안에서 E2E 목록을 생성해 누락을 방지한다. 새 프레임워크·의존성·ADR은 필요하지 않다. live 검증은 네트워크 모킹으로 한정한다.

## 구현 결과

계획의 일곱 항목을 완료했다. 실행 시 빌드나 새 라이브러리는 필요하지 않다.

- **두 트랙:** `site/assets/book.js`에 기존 이론 1~14장·실험실·용어집·출처와 새 실습 0~10을 분리했다. 표지·목차·사이드바·상단에 트랙을 표시하고 이전/다음은 같은 트랙 안에서 이동한다. 기존 `ReelsBook.chapters`·byNumber와 URL·앵커를 유지했다. 표지에 주요 실습 시작 버튼·E2E 링크·각 트랙 수를 넣었다.
- **실습 원고:** `site/practice/00-start.html`부터 `10-insights.html`, `e2e.html`을 추가했다. 총 35단계가 동일한 여섯 요소와 OS 탭을 갖춘다. 실습 1의 테스트 계정 A/B·+별칭 확인 팁·필수 상자 3개, 실습 2의 터미널/Python/pip 기초, 실습 3의 웹 채팅/직접 편집과 실제 로컬 피드 전환, 실습 7의 원본 전송·앱 게시 후보·주소 기록을 포함한다. 실습 8·9는 선택 심화이고 24시간·7일은 교재 관찰 시점으로 구분했다.
- **공통 동작:** `practice.js`는 방향키/Home/End/Tab/Enter로 조작하는 OS 탭과 공유 진행 상태·게시물 주소·초기화를 담당한다. `book.css`의 공통 단계 클래스를 사용한다. 읽기 금지·쓰기 용량 부족·손상 데이터에서도 체크와 입력을 유지하고 미저장을 알린다. JS가 없으면 두 OS 본문과 다음 실습 링크를 읽을 수 있다. 브라우저를 바꾸거나 저장을 차단한 뒤 이동하면 기록이 이어진다고 보장하지 않는다.
- **원고와 근거:** `scripts/build_practice.py`가 정적 본문·같은 단계의 E2E·자체 SVG 12개·[7v 확인 목록](phase-7w-verify-list.md)을 생성한다. Instagram 메뉴 미확인 블록 **18개** 모두 `data-verify="app-menu"`, 지정 문구, 공식 도움말, 확인일을 갖는다. 공개 폴더 그림은 자체 휴대폰 틀·번호·강조로 그렸고 실제 화면·브랜드 아이콘을 복제하지 않았다. 그림의 위치는 설명용임을 명시했다.
- **키트:** `publish.py` 기본 버전 v26.0·`.env`/환경변수 설정·`--base-url`을 추가하고 기존 `--public-base-url`을 유지했다. 환경변수가 우선하며 `.env.example`과 Git 제외 규칙을 제공한다. Instagram Login 이미지·영상 모두 공개 URL, 장기 토큰 60일·갱신 조건을 README와 실습에 반영했다. `prepare_hosting.py --dest`는 승인 해시를 확인한 JPEG/MP4만 **새 폴더**로 복사하며 GitHub 웹 업로드/Pages/URL 규칙을 안내한다. 토큰·설정·검수표는 복사하지 않고 25MiB 초과·승인 변경·기존 대상 폴더를 거부한다. 실제 업로드는 하지 않는다.
- **전송과 실패:** 기존 승인·파일 변경 검출·합성 자료 live 거부·시도 기록의 중복 방지를 유지했다. 컨테이너 확인은 60초 간격 최대 5회로 근거 노트의 분당 확인 권고에 맞췄다. live는 캐러셀+릴스 **2개 게시 시도**이며 API 광고 라벨·자동 갱신·예약/호스팅 서비스는 추가하지 않았다. 모든 API 호출 시험은 모킹이다.
- **이론·부록·현황:** 이론 5~10장의 작업실은 기획·판단과 실습 링크로 정리하고 다른 이론 장에도 관련 실습을 연결했다. 이론 1장에 바로 가기 안내를 넣었다. SRT의 정의는 이론 원리 절에 남겨 용어집 최초 장과 실험실 절 재사용을 유지했다. 부록 생성기는 실습 인용도 집계해 **147개 출처**를 노출한다. `docs/PROJECT_STATE.md`와 `shelf/progress/index.html`은 7r/7w/조건부 7v를 구분한다.

## 근거 공백과 계획 조정

- 계정 전환 수 상한·계정별 가입 인증 조건·이메일 +별칭 수락, 프로페셔널 공개 전환·보관/삭제의 세부 절차는 7r에 충분한 근거가 없다. 사용자 요청 항목을 빼는 대신 **확인 필요/탐색 후보**로 설명하고 수치나 성공을 만들어 쓰지 않았다. S180 전환 도움말을 가입·삭제 절차의 근거로 전용하지 않았다.
- 개발자 대시보드의 문서상 흐름과 현재 한국 Instagram 앱 메뉴를 구분했다. Standard Access 검수 면제와 개발 모드의 일반 공개도 구분한다. 필요한 라벨을 확인하지 못하면 보류하는 경로를 둔다.
- 실습 명령은 첫 합성 연습에 `output/first-post`를 계속 쓰도록 통일했다. 실제 자료는 독자가 확인한 로컬 RSS로 새 `output/my-news`를 만들고 이후 경로를 바꾸도록 안내한다. 웹 채팅을 사용하지 않는 직접 편집 경로도 완주 가능하다.
- 기존 Phase 결과 기록과 생성 스크립트 관례를 재사용했다. 새 specs/ADR·프레임워크·외부 패키지·자동 스케줄러는 만들지 않았다.

## 검증 결과

Linux / Python 3.11.15 / 기존 Playwright Core·Chromium 1228에서 수행했다. 외부 폰트는 빈 CSS로 모킹해 시스템 폰트 대체 표시를 검사했다. 실제 Meta/LLM 네트워크·로그인·게시 요청은 보내지 않았다.

| 범위 | 실제 결과 | 증거 |
| --- | --- | --- |
| 키트 기존+신규 전체 시험 | **67 passed in 29.83s**, 실제 네트워크 차단·API 성공/오류/유실·5회 대기·시도 기록·토큰 비노출·.env 우선순위·호스팅 파일 제한·CLI 호환 | `starter-kit/tests/`, 신규 `test_publishing.py` 12개 포함 |
| 깨끗한 임시 키트/새 venv | 설치 후 실습 2~6 명령·호스팅 준비·본인 로컬 피드 계약을 실제 실행, **12개 명령+출력/해시 기록** 통과. 설치 이후 네트워크 차단 | [walkthrough-check.json](phase-7w/walkthrough-check.json), [재현 스크립트](phase-7w/walkthrough.py) |
| 전체 31 HTML × 1280/375/360px | **2,147개 검사**, 가로 넘침·콘솔/페이지 오류 0, 런타임 링크 733개 유효 | [browser-check.json](phase-7w/browser-check.json), [검사기](phase-7w/verify.mjs) |
| 배포 하위 경로·트랙 이동·현황·file:// | **85개 검사**, 오류 0. `/reels/` 트랙별 다음 이동·상대 경로, 현황 3개 폭, 수정 이론 작업실 3개 폭, file 탭·이동·다크 화면 | [edge-check.json](phase-7w/edge-check.json), [검사기](phase-7w/edge-check.mjs) |
| 정적 링크/앵커·공통 구조·출처 | **1,188개** 내부 링크/자산, 35단계/E2E·18개 메뉴 목록 일치, 기존 HTML의 앵커 보존, 오류 0 | [static-check.json](phase-7w/static-check.json), [검사기](phase-7w/check.py) |
| 재생성·구문·공백 | 생성/연결 원고 **43개** SHA256 재실행 전후 동일, 전체 assets JS `node --check`·`git diff --check` 통과 | [build-check.json](phase-7w/build-check.json) |

깨끗한 복사본에서는 README의 venv·pip 설치 → 실습 2 첫 생성 → 실습 3 prompt.md 생성/기존 초안 직접 편집/구조 검증 → 실습 4·5 render 두 번 → 검수 fixture 체크 → approve → publish 드라이런을 실행했다. 본문 성공 기준의 `검수 대기`, `구조 검증 OK`, `mode: dry-run`, PNG/JPEG 5장·MP4·승인 기록을 대조했다. 추가 도우미의 `공개 준비 완료: 6개 JPEG/MP4`와 로컬 RSS 새 폴더 경로도 확인했다. 검증 fixture의 자동 체크는 테스트 내부 처리이며 독자에게 자동 검수 명령을 제공하지 않는다. 웹 채팅 호출·실제 기사 권리 판단·본인 녹음 음질 검증은 하지 않았다.

브라우저에서는 모든 실습 탭의 방향키/Home/End/Tab과 체크의 Space, 새로고침 복원·E2E↔실습 공유·주소 복원/삭제를 실제 조작했다. 읽기/쓰기 금지·QuotaExceededError·잘못된 저장 구조에서도 입력·탭·체크가 동작함을 확인했다. JS 비활성 시 양쪽 OS 본문과 다음 링크가 남는다.

검증 중 검사기가 `data-fact-id`를 기존 `id`로 잘못 인식해 앵커 제거를 보고한 것을 정확한 속성 검사로 수정했다. file 탭 검사도 복사 버튼 대신 실제 탭을 선택하도록 고쳤다. 현황 샘플 404는 임시 호스트가 CI의 샘플 복사를 재현하지 않은 검사 환경 문제였다. 실제 `.github/workflows/pages.yml` 조립과 같이 임시 폴더에 샘플을 복사한 뒤 오류 없이 통과했다. 사이트의 오류를 무시하는 예외는 넣지 않았다. 최종 검토에서 이론 체크 문구의 중복을 제거하고 실제 기획 결과에 맞췄다.

## 재현

저장소 루트에서:

```bash
python3 scripts/build_practice.py
python3 scripts/build_appendices.py
starter-kit/.venv/bin/python -m pytest -q starter-kit/tests
python3 docs/results/phase-7w/walkthrough.py
python3 docs/results/phase-7w/check.py
find site/assets -name '*.js' -print0 | xargs -0 -n1 node --check
git diff --check
```

브라우저 검사 서버를 별도 터미널에서 실행한다.

```bash
python3 -m http.server 8517 --bind 127.0.0.1 --directory site
```

```bash
node docs/results/phase-7w/verify.mjs
```

추가 경로 검사는 `/tmp/ai-insta-7w-host/reels`를 이 저장소의 `site/`에 연결한 뒤 아래 서버를 실행한다. 검사기 자체가 Pages workflow에 맞춰 현황 HTML·샘플을 임시 폴더에 조립한다.

```bash
python3 -m http.server 8518 --bind 127.0.0.1 --directory /tmp/ai-insta-7w-host
```

```bash
node docs/results/phase-7w/edge-check.mjs
```

브라우저 검사기는 기존 `/tmp/ai-insta-phase3-browser/node_modules/playwright-core/index.mjs`와 `/home/yonghun/.cache/ms-playwright/chromium-1228/chrome-linux64/chrome`을 사용한다. 다른 환경에서는 해당 경로를 맞춘다. 깨끗한 복사본은 기존 키트 Python 3.11 실행 파일을 사용하며 `WALKTHROUGH_PYTHON`으로 바꿀 수 있다. 설치할 때 인터넷이 필요하다.

## 화면 증거

- 표지: [1280](phase-7w/index-1280.png) · [375](phase-7w/index-375.png) · [360](phase-7w/index-360.png)
- 실습 7 상단: [1280](phase-7w/practice-07-publish-1280.png) · [375](phase-7w/practice-07-publish-375.png) · [360](phase-7w/practice-07-publish-360.png)
- 실습 7 공통 단계·미확인 메뉴: [게시 단계](phase-7w/practice-07-publish-step-1280.png) · [다크 라벨 단계](phase-7w/practice-07-publish-labels-dark.png). 요소 캡처에는 고정 헤더의 겹침을 피하려고 헤더만 숨겼다.
- E2E 전체: [1280](phase-7w/practice-e2e-1280.png) · [375](phase-7w/practice-e2e-375.png) · [360](phase-7w/practice-e2e-360.png)
- 모바일: [계정](phase-7w/practice-01-account-375.png) · [설치](phase-7w/practice-02-setup-375.png) · [API](phase-7w/practice-08-api-375.png)

## 남은 확인과 작업 범위

**Claude Code 검수와 조건부 7v가 남아 있다.** [미확인 목록](phase-7w-verify-list.md)의 한국 앱 메뉴·필수 라벨 적용·예약/인사이트·개발 모드 일반 공개는 실제 계정 제공 시 확인한다. Windows/macOS 설치·실제 기기 전송·실제 토큰 발급/갱신·게시·예약·다른 브라우저/보조기기·독립 초보자 완주를 검증하지 않았다. Phase 6의 독립 품질 검토나 ShortsBook을 미리 수행하지 않았다.

초기 Git 상태는 깨끗했다. 작업 중 별도로 나타난 `scripts/codex_phase.sh` 변경과 `docs/prompts/phase-8s.md`는 수정·되돌리지 않았다. 연구 원고와 Hermes 저장소는 변경하지 않았다. 토큰·개인 .env·원응답 전문을 저장소에 넣지 않았고 commit·push를 시도하지 않았다.

## 완료 보고

`python3 scripts/notify.py`로 위 결과와 남은 7v/검수 범위를 한국어 5줄로 보고하고 실습 7의 공통 단계 스크린샷을 첨부했다. **HTTP 200**, 메시지 ID `1564089194018508964`. 인증 값은 출력하거나 저장하지 않았다.
