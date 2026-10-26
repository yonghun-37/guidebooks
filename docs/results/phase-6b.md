# Phase 6b — 수정과 품질 게이트

2026-10-26. 사용자 지시·DESIGN 1절의 Claude 결정·8절 게이트와 Phase 6a F01~F15를 구현 기준으로 삼는다. Level 2 작업이며 기존 단계 결과 문서 관례에 맞춰 계획과 결과를 이 문서에 보존한다. commit·push·실제 OS 예약 등록·계정 로그인·실제 게시는 하지 않는다.

## 구현 계획

- [x] F01: `starter-kit/daily.py`는 키트 루트 기준 날짜별 폴더에 기존 생성 함수를 호출하고 검수 대기에서 종료한다. 같은 날짜 재실행은 기존 폴더를 덮어쓰지 않는다. `schedule_setup.py`는 작업 폴더에 의존하지 않는 Python·스크립트·설정 경로로 Windows schtasks/macOS·Linux cron 명령과 확인·해제 안내만 생성한다. 공백 경로·날짜·실패·게시 미호출을 모킹 시험한다.
- [x] F02~F09·F14~F15: 실습 0~9와 E2E의 장수·실제 자료 분기·파일 저장·Python 선택·음성·토큰·호스팅·계정 이름·검수 범위·총 소요 시간을 실제 코드에 맞춘다. 실습 9는 예약→수동 실행→다음 날 폴더→승인→게시로 연결한다.
- [x] F10~F13 및 추가 지시: 14장 날짜별 계획·주간 점검표, 첫 용어 풀이·해시 링크·장 메타를 보완한다. 3·13장 SVG 장부, 모바일 입력 압축, 8장 장면 미리보기를 확대한다. 9·14장과 실습 예약을 연결한다.
- [x] 기존 `scripts/check_site.py`에 9블록·SOURCES 참조·fact-pending·용어·퀴즈·alt·파일 합계를 추가하고 실패 fixture로 검증한다.
- [x] 전체 HTML의 1280/375/360px·라이트/다크·콘솔·도구 회귀, 키트 전체 시험·깨끗한 복사본 오프라인 실행·문체 검사를 실행한다.
- [x] 게이트 표·항목별 해결 결과·검증 한계·최신 PROJECT_STATE·진행 페이지를 갱신하고 Discord에 보고한다.

## 구현 선택

새 생성 파이프라인·무인 게시 기능은 만들지 않고 기존 `run_pipeline.run()`과 사람 승인을 재사용한다. 스케줄러는 등록 스크립트를 실행하는 대신 사람이 확인할 명령을 출력한다. 실습의 기존 체크 키는 보존하며 필요한 새 필수 단계는 원본과 E2E에 함께 반영한다. 외부 도구 안내는 기존 research 근거와 공식 문서로 확인한다.

## 구현 결과와 검수 항목

F01~F15 모두 수정했다. 미수정 항목은 없다. 실제 OS 등록·다음 날 대기·계정 게시의 미실행은 사용자 지정 검증 범위이며, 성공한 것으로 표시하지 않는다. [6a 원본 판정](phase-6a-findings.md)은 역사적 검토 기록으로 보존한다.

| 항목 | 수정과 재검증 |
| --- | --- |
| F01 차단 | `daily.py`가 `output/daily/YYYY-MM-DD`에 생성하고 검수 대기에서 종료한다. 중복 날짜는 덮어쓰지 않는다. `schedule_setup.py`가 Windows schtasks·macOS/Linux cron 등록/확인/수동 실행/해제 명령을 출력한다. 실습 9를 등록→수동 실행→다음 날 폴더→검수·승인→앱 또는 선택 API 게시로 재작성하고 9·14장/E2E에 연결했다. 실제 등록 전에는 체크하지 않도록 했다. |
| F02 혼란 | 동봉 3개 기사=5장, 기사 1개=3장으로 구별하고 생성된 모든 카드의 검수·전송으로 통일했다. 깨끗한 복사본의 두 입력에서 재현했다. |
| F03 혼란 | 실습 3 첫머리에서 합성 연습/내 자료를 선택하고 E2E에 `3:real-source` 필수 분기를 넣었다. 합성 자료를 오늘 게시할 자료로 간주하지 않는다. |
| F04 혼란 | 메모장 모든 파일·UTF-8·실제 확장자, TextEdit 일반 텍스트·인코딩·스마트 따옴표·.txt 추가 설정과 `.json.txt`/`.xml.txt` 복구를 안내했다. |
| F05 혼란 | 낮은 python3와 설치한 python3.11을 구별하고 버전별 실행 파일로 venv를 만드는 예를 추가했다. |
| F06 혼란 | Windows/macOS의 본인 녹음→구간 자르기→WAV 내보내기 한 경로와 지원하지 않는 M4A의 동봉 FFmpeg 변환을 안내했다. 실패하면 기본 무음을 유지한다. 변환 명령을 실행했다. |
| F07 혼란 | `token_check.py`가 getpass로 토큰을 숨겨 받고 본인 ID/계정 이름만 읽는다. 리다이렉트·숨김 입력 불가·HTTP 오류·민감 값 출력은 차단한다. 실습은 user_id→IG_USER_ID, 발급 응답 expires_in→만료 메모를 구분하며 OAuth·scope도 풀어 쓴다. 실제 요청은 모킹했다. |
| F08 혼란 | GitHub 가입/로그인→새 공개 저장소 이름→README 초기화→기본 branch 확인을 업로드 앞에 붙였다. 공식 절차 근거를 보존했다. |
| F09 혼란 | 기획 이름→config.yaml account_name→새 생성, 소개→앱 프로필을 연결했다. 독립 코드 검토에서 추가 발견한 prompt 명령의 기본 이름 복귀도 수정했다. 내 자료용 `--config config.yaml`을 양 OS에 명시했고 프롬프트 이름 RED→GREEN을 확인했다. |
| F10 혼란 | 14장 숫자를 ‘시간 예산’으로 먼저 설명하고 첫날부터 30행의 날짜별 할 일·완료 칸·복사용 텍스트·주간 점검 5칸을 만든다. 날짜/활동일 변경과 빈칸, 체크 유지를 검사했다. 화면 체크는 저장되지 않으므로 내 메모로 옮기도록 안내한다. |
| F11 혼란 | WCAG·OFL·px·fps·MIME·scope 첫 사용 풀이와 용어집 항목을 보완했다. 용어집은 30개가 됐다. |
| F12 사소 | 모든 이론 장의 공통 메타를 복구했다. 예상 시간은 읽기·메모이며 연결 실습 시간은 별도라고 명시했다. |
| F13 사소 | 해시태그의 ‘해시’를 파일 해시 첫 사용으로 오인하지 않게 생성기를 수정했다. 용어집은 실제 설명인 실습 6 `#approve`로 연결한다. |
| F14 혼란 | 카드만 게시해도 키트가 영상까지 만들므로 승인 전 영상 검수도 필요하다고 경로·카드·검수·E2E에 명시했다. |
| F15 혼란 | 기본 실습 0~7 합계 195분(3시간 15분), 중단 지점과 내 자료 재생성·전송·인증 대기를 별도로 표시했다. 한 시간 완료를 보장하지 않는다. |
| 추가: SVG | 3·13장 수입·비용·잔액 SVG와 텍스트 결과를 함께 제공한다. 3장은 비용에 환불·공제를 합치며 적자는 0선 왼쪽, 빈칸은 그림 숨김이다. 13장은 필요한 건수를 모두 유료 납품한 가상 계산이다. |
| 추가: 모바일·8장 | 수치 입력은 모바일에서도 2열로 표시하고 기존 접기 입력을 유지했다. 타임라인 화면은 기존 72×112에서 모바일 150×약267, 데스크톱 200×약356으로 확대했다. 실습의 같은 도구에도 적용한다. |

## 구현 선택과 검토 중 수정

- 기본 파이프라인·라이브 게시 검수 규칙은 재사용했다. 일일 생성은 오프라인 고정이며 로컬 피드를 매번 읽는다. 새 뉴스 수집·웹 채팅 응답·검수·게시를 무인 실행하지 않는다. `llm.mode=prompt`를 선택한 설정은 문안 대기에서 멈추므로 실습 9는 offline/silent를 지정한다.
- cron은 절대 경로와 셸 인용·퍼센트 이스케이프를 쓴다. Windows는 긴 `/TR` 우려를 줄이기 위해 Python/daily.py는 절대 경로, 키트 내부 config/feed/log/output은 키트 기준 상대 경로를 사용한다. 외부 파일은 절대 경로다. 261자 초과 명령은 **키트가 보수적으로 거절**하며 짧은 폴더로 옮겨 재생성하도록 한다. 이 수치를 Windows 전체 명령 한도의 실증값으로 주장하지 않는다. 근거·한계는 [예약 노트](../../research/phase-6b-scheduling.md)에 남겼다.
- 별도 코드 검토자는 키트 111개·스크립트 23개·UI 48개를 재실행하고 실습의 설정 누락 F09를 찾아냈다. 이후 프롬프트 설정을 보완했고 최종 키트 116개·UI 55개는 작성자가 재실행했다. Claude Code의 최종 검수는 남아 있다.
- 14장 체크를 누르면 표가 다시 만들어져 체크가 지워지던 문제는 실패 재현 뒤 달력 입력 3개만 표를 다시 그리도록 고쳤다.
- 초기 브라우저 404는 저장소 원본 서버에 배포 전용 `progress/samples`가 없어서 생겼다. Actions와 같은 책장 루트·`reels/`·샘플 구조를 임시 폴더에 만들고 다시 검사했다. 사이트 오류를 검사에서 제외한 것이 아니다.
- 8장 확대 요청에 맞춰 기존 도구 회귀 검사의 결과 위치 제한을 해당 도구만 740px→950px로 조정했다. 다른 도구는 740px를 유지한다. 확대된 화면과 접힌 입력의 키보드 조작·가로 넘침을 함께 검사했다.

## DESIGN 8절 품질 게이트

| 게이트 | 판정 | 실제 증거·한계 |
| --- | --- | --- |
| 모든 내부 링크·앵커 유효 | **통과** | 정적 37 HTML·내부 참조 1,373개 오류 0. 브라우저가 만든 링크 625개도 파일·앵커 검사 통과. [정적](phase-6b/static-check.json), [브라우저](phase-6b/browser-check.json) |
| 2~14장 9단계 블록 | **통과** | 13장 모두 누락·중복·순서 오류 0. `check_site.py`가 검사한다. |
| 정책·수치 각주·연구 출처 | **통과 — 문서 근거 기준** | S259~270 절차 근거 추가, 등록 출처 총270개·현재 인용109개. S번호·용어·fact-pending 검사 통과. 기존 6a 질문/수치 검토와 신규 절차 근거를 대조했다. 모든 정책의 현행 계정 적용을 새로 실증했다는 뜻은 아니다. |
| 1280/375px 가로 스크롤 없음 | **통과** | 360px도 추가. 37페이지×3폭×라이트/다크, 접기 전후 포함 총2,140검사·가로 넘침·콘솔/페이지 오류 0. [모바일](phase-6b/reel-360-dark.png), [375](phase-6b/reel-375-dark.png), [데스크톱](phase-6b/reel-1280-dark.png) |
| 키트 오프라인 전체 실행·샘플 재생성 | **통과** | 최종 116 tests 통과. 새 복사본·새 .venv에서 생성/문안/렌더/승인/드라이런/호스팅/음성 변환·예약 명령 실행. PNG5·MP4·SRT·JSON2의 기존 샘플과 SHA256 일치. [키트 시험](phase-6b/kit-tests.txt), [명령](phase-6b/commands.md), [샘플](phase-6b/sample-regeneration.json) |
| 퀴즈 정답·해설과 본문 일치 | **통과** | 6a의 독립 의미 검토에서 7/7인 원고의 이론42·실습12=54문항을 유지했다. 변경된 예약 문답도 실제 단계와 대조했고 전 문항 정답/오답/해설/초기화 동작을 다시 조작했다. DOM 데이터 구조 오류는 자동 검사한다. |
| 독립 초보자 검토와 막힘 수정 | **통과 — 발견 항목 수정·재검증** | 별도 6a에서 찾은 F01~15 전부 수정. 깨끗한 복사본 명령, UI·정적 회귀 및 별도 코드 검토로 확인했다. F01은 Claude의 변경된 성공 기준을 적용한다. 실제 계정 게시·OS 예약 등록·다음 날 실동작을 성공으로 표시하지 않는다. |

## 추가 자동 검사와 검증 결과

- `scripts/check_site.py`: 모든 site/shelf HTML, 배포 경로를 따른 href/src/poster 및 도구 복습 링크, 중복 ID, 9블록, SOURCES, fact-pending, 용어, 퀴즈 DOM 계약, 이미지 alt, 배포 파일 합계를 검사한다. 실패 시 exit 1. 새로운 정적 검사 13개와 기존 문체 검사 10개, 합계 **23 tests** 통과. 결함 fixture로 실패를 먼저 확인했다. [시험](phase-6b/script-tests.txt)
- `style_lint`: 이론14+기타23=**37페이지 통과**, 금지어·내부 용어0, 이론 모두 고정 기준선의70% 이하. [이론](phase-6b/lint-theory.json), [기타](phase-6b/lint-other.json). 기준선은 변경하지 않았다.
- 기존 인터랙션 **883개**·경계 **15개**, 신규 UI **55개** 검사 통과. [도구](phase-6b/interaction/browser-check.json), [경계](phase-6b/interaction/edge-check.json), [UI](phase-6b/ui-check.json). 14장 날짜/체크·3장 음수/빈칸·13장 0가격·메타·6개 새 용어/해시 연결을 포함한다.
- 부록 재생성 전후 사이트 **90파일 SHA256 동일**, JS 전체 `node --check`·`git diff --check` 통과. [재생성](phase-6b/regeneration-check.json)
- 배포 합계 **4,075,418바이트 / 98파일**: site 2,498,524 + shelf 8,561 + 배포 샘플 1,568,333. `.github/workflows`가 배포하는 세 묶음 기준이며 저장소 전체 크기가 아니다. 용량 상한을 새로 정하지 않았다.
- [프롬프트 설정 회귀](phase-6b/prompt-config-regression.md), [일일 생성과 중복 보존](phase-6b/daily-e2e.txt). 원본35개의 진행 키를 보존하고 실제 자료·수동 확인·다음 날 확인3개를 더해 원본/E2E **38개**를 맞췄다.

## 재현

```bash
starter-kit/.venv/bin/python -m pytest -q starter-kit/tests
python3 -m unittest discover -s scripts/tests -q
python3 scripts/check_site.py --output docs/results/phase-6b/static-check.json
python3 scripts/style_lint.py site/chapters/[0-9][0-9]-*.html --baseline docs/results/phase-9/baseline.json
find site/assets -name '*.js' -print0 | xargs -0 -n1 node --check
git diff --check
```

브라우저는 기존 Playwright Core·Chromium1228을 사용했다. 신규 패키지는 추가하지 않았다. `verify.mjs`는 Actions와 같은 배포 폴더를 포트8587로 제공한다. 나머지 검사는 저장소 루트를 포트8586으로 제공한다. `/tmp/reelsbook-6b-host/`에 shelf 내용, 그 아래 reels/에 site 내용, progress/samples/에 키트 PNG/MP4를 복사하면 된다.

```bash
python3 -m http.server 8587 --bind 127.0.0.1 --directory /tmp/reelsbook-6b-host
# 별도 터미널에서 저장소 루트 서버도 시작
python3 -m http.server 8586 --bind 127.0.0.1
# 서버를 유지한 채 별도 터미널에서
node docs/results/phase-6b/verify.mjs
node docs/results/phase-6b/ui-check.mjs
SITE_URL=http://127.0.0.1:8586/ node docs/results/phase-6b/verify-interactions.mjs
SITE_URL=http://127.0.0.1:8586/ node docs/results/phase-6b/verify-interaction-edge.mjs
```

## 남은 확인·후속

- Claude Code 최종 검수·커밋·배포가 남아 있다. 이 작업은 commit·push를 하지 않았다.
- 실제 Windows/macOS·스케줄러 등록·다음 날 실행·잠자기/전원/권한 조건, 휴대폰 녹음·전송·앱 메뉴, 실제 토큰·게시·예약 발행은 미실행이다. 생성된 명령·모킹·Linux/Chromium 검증으로 한정한다.
- 자동 수집/토큰 갱신/호스팅/무인 게시를 추가하지 않았다. 피드의 새 자료·권리 갱신과 승인·게시는 사람이 맡는다. 정책·국가·계정별 가용성의 기존 확인 공백은 유지한다.
- 절차 근거는 [보완 노트](../../research/phase-6b-procedures.md)·[예약 노트](../../research/phase-6b-scheduling.md), 출처/사실표에 남겼다. 최종 현황·책장 단계 상태도 갱신했다.

Discord 보고: 요청한 `✅ [Phase 6b 완료]` 한국어 5줄을 `python3 scripts/notify.py`로 전송했다. **HTTP 200**, 메시지 ID `1564119415799419001`. 비밀 값은 출력·기록하지 않았다.
