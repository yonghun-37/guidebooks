# BX3 · BlogBook 심화편 뼈대와 A1·A9 샘플

A1 작업 환경과 A9 협찬 본문, 전용 장 틀·스타일·협찬 상태 도구를 구현했다. A0~A12+E2E의 14개 장 경로를 연결했고, A1·A9만 `완성`, 나머지는 `준비 중`이다. **집필·실행·화면 검증은 완료했으며, 원본 check_site는 심화 출처 미등록 때문에 통합 담당자의 수정이 남았다.** 커밋·push는 하지 않았다.

## 범위와 결정

- 담당 파일: `site-blog/advanced/*.html`, `assets/advanced.css`, `assets/advanced.js`. 세 번째 트랙 연결에 필요한 `assets/book.js`, 표지 `index.html`만 함께 변경했다.
- 이론·실습의 HTML·공통 CSS/JS, 키트·research·서가·PROJECT_STATE·검사기는 수정하지 않았다. 작업 시작 당시 tracked 변경은 없었으며, 작업 중 등장한 다른 작업자의 `docs/prompts/phase-BX4a.md`, `phase-BX4b.md`도 보존했다.
- 문체는 STYLE-GUIDE, 장 형식은 DESIGN-blog-advanced 1.2절, 정책 충돌은 8절을 우선했다. 건강 규칙은 DESIGN-baby 8절을 읽고 수면 협찬 거절에 적용했다. 외부 관리자·광고·제휴 화면을 캡처하지 않았다.
- A1은 고정 날짜·시드·기본 mock, 진단과 임시 서버의 포트 차이, 가상환경, 기본 검사→맛보기→날짜 변경→복원을 설명한다. Docker는 선택 준비 안내이며 현재 mock 결과와 구별했다.
- A9는 가상 포근담요 거절, 도담 분류·리콜·권리 검토, AI 불허→사람 작성, 첫머리 표시, 광고주 확인→최종 사람 승인, 서버 공개 재조회, 보고·정산·현물 기록을 잇는다. 세금·육아휴직급여 신고 판단은 공식 안내와 상담 경로로 안내했다.
- 코드 발췌는 실제 키트의 doctor.py 17줄, ledger.py의 transition 22줄이다. 원본과 바이트 대조했고 읽는 법 표·파일:줄 링크를 넣었다.
- 협찬 도구는 키트 상태 이름·허용 경로를 사용한다. 필수 확인 항목, 수락·거절·자료 보류·복귀·재작성·예약·정산을 연습한다. 외부 전송은 없고 `blogbook:advanced:sponsor:v1`에 상태·가상 문의 종류·이력만 저장한다. 저장 차단·손상 저장값도 처리한다.
- book.js는 `data-advanced`를 읽고 트랙별로 현재 장을 찾는다. 다른 트랙의 `00-start`·`10-automation`·`e2e` 같은 slug가 충돌하지 않는다. 정적 표지 목차·장 이동 링크도 남겨 JS 없이 읽을 수 있다.

## 검증 결과

| 검사 | 실제 결과 | 증거 |
|---|---|---|
| style_lint · 새 심화편 | 14/14 통과, 금지어·내부 용어·단서 표현 0 | [보고서](phase-BX3/style-lint.json) |
| style_lint · site-blog 전체 | 48/48 통과 | [보고서](phase-BX3/style-lint-site.json) |
| check_site 원본 | **exit 1, 출처 등록 관련 22건**. 기존 36 HTML 검사 오류는 0이었으며 추가 오류는 새 장의 BX 출처와 URL 쿼리 BS074뿐 | [원본 검사](phase-BX3/check-site.json) |
| 동일 검사 함수 + 임시 합산 출처 목록 | 오류 0. 저장소 파일은 변경하지 않고 임시 루트의 SOURCES만 합침 | [합산 결과](phase-BX3/check-site-combined-registry.json) |
| 42페이지 × 3폭 × 2테마 | 가로 넘침 0, JS 예외·콘솔 오류 0. 기존 이론 13장·실습 페이지도 포함 | [브라우저 결과](phase-BX3/browser.json) |
| 동적 링크·트랙 충돌 | 900회 링크·앵커 대조, 오류 0. theory/practice/advanced의 같은 slug 분리 확인 | [최종 결과](phase-BX3/browser-final.json) |
| 키보드 | OS 탭 방향키/Home, 협찬 13회 상태 이동을 체크박스 Space·버튼 Enter로 완주 | [브라우저 결과](phase-BX3/browser.json) |
| 저장 | 새로고침 복원, 거절, 자료 보류·해결 복귀, 저장 접근 차단 시 계속 작동, 비정상 단계 저장값 초기화 통과 | [브라우저 결과](phase-BX3/browser.json) |
| JS 끄기 | 14개 심화 장·표지의 본문·정적 링크·두 OS 명령 읽기, 360px 넘침 0 | [브라우저 결과](phase-BX3/browser.json) |
| 명령·코드·출력 | 새 복사본+새 venv, Linux 본문 명령 22블록 실행. A1·A9 expected terminal 전체·각 stdout·체크포인트·발췌 일치 | [읽는 순서](phase-BX3/reading-order.json), [출력 대조](phase-BX3/commands.json) |
| 수정 뒤 재승인 복구 | 수정 원문→HTML 재생성→초안 준비→가상 광고주 재확인→새 해시 승인 통과 | [복구 기록](phase-BX3/recovery.json) |
| JS 구문 | book.js·advanced.js의 `node --check` 통과 | 명령 실행 확인 |

실행 환경: Linux, Python 3.11.15, 새 venv, 실행 패키지 설치 없음. 시스템 python3은 3.10.12여서 본문처럼 python3.11로 새 환경을 만들었다. Windows PowerShell 명령은 표기와 경로를 검토했으며 Windows·macOS 실기기는 실행하지 않았다. 이번 단계의 Docker 실행·실호스팅 발행·계정 로그인·유료 호출·실제 광고주 회신·세금 신고는 하지 않았다. Docker 선행 실행 사실은 [BX3k 결과](phase-BX3k.md)에 있다. Python 코드는 변경하지 않아 전체 pytest를 재실행하지 않았다.

## 본문 명령 대조표

기본 A1과 A9는 `course/expected/<장>/terminal.txt` 전체 및 `outputs.json`의 stdout과 **문자열 그대로** 일치했다. 이 출력만 본문의 “이렇게 보이면 성공”에 썼다. expected에 없는 보조 출력은 본문에서 “실행 결과” 또는 “예상한 막힘”으로 구별하고 실제 실행 로그와 대조했다. Linux 셸 준비는 본문의 명령 블록을 읽는 순서대로 실행했다.

| 본문 명령 | 실제 확인 | 대조 기준·결과 |
|---|---|---|
| `python3.11 --version`, `python --version` | Python 3.11.15 | 설치된 인터프리터·새 venv 확인 |
| `pwd`, `ls` | 새 복사본 경로와 blog.py/course.py 표시 | 키트 폴더 확인 |
| `python3.11 -m venv .venv`, `source .venv/bin/activate` | 새 환경 생성·이후 python을 해당 환경으로 실행 | Linux 실제 성공 |
| `python course.py start A1` | `✔ 통과: A1 시작 상태 복원` | 실제 stdout 일치 |
| `python course.py doctor` | Python·폴더·쓰기 권한·포트 8767, 고정 날짜·시드 | A1 expected 일치 |
| `python blog.py status --mock` | mock REST 연결 / output/status.json | A1 expected 일치 |
| `python course.py check A1` | A1 산출물·상태·터미널 출력 일치 | 기본 실행과 최종 복원 후 모두 통과 |
| `python blog.py run --sample` | mock 초안→가상 사람 승인 시연→예약 1, 글 HTML·주간 HTML | 실제 stdout 일치. A1 expected에는 없는 보조 맛보기 |
| `cp config.example.toml config.toml` | 설정 복사 | Linux 실제 성공 |
| 날짜 한 줄 변경 후 `python blog.py run --sample` | 예약 10월 28일 09시→29일 09시 | state.json의 실제 date 대조 |
| `python course.py reset` | 실습 상태 초기화·.env 보존 | 실제 stdout, 이후 A1 시작/재실행/check 통과 |
| `python course.py start A9` | `✔ 통과: A9 시작 상태 복원` | 실제 stdout 일치 |
| `python blog.py sponsor demo` | 미디어킷·보고서·세금 CSV·대장 CSV | A9 expected 일치. 도담 brand_review, 포근담요 declined |
| `python blog.py draft --sample sponsor --human-notes` | 사람 경험 칸이 있는 초안 생성 | A9 expected 일치 |
| `python blog.py publish --sample sponsor --prepare` | post_id=2 · draft | A9 expected 일치 |
| `python blog.py gate --sample sponsor --approve 서윤` | 사람 승인 · f62525058efb | A9 expected 일치 |
| `python blog.py publish --sample sponsor` | post_id=2 · future | A9 expected 일치 |
| `python blog.py status --sample sponsor --advance-days 2` | 서버 상태 재조회 | A9 expected 일치, status.json의 publish 확인 |
| `python blog.py sponsor settle` | 보고·정산 파일 생성 | A9 expected 일치, 대장 declined/settled 확인 |
| `python course.py check A9` | A9 산출물·상태·터미널 출력 일치 | 기본 완주 및 바꿔 보기 복원 후 통과 |
| publishing mode 한 줄 auto 변경 후 `publish --sample sponsor` | `✖ 막힘: 사람 승인 대기 → blog.py gate --approve 검토자명을 실행하세요` | 의도한 exit 1, 실제 문구 일치 |
| 공개 확인 전 `python blog.py sponsor settle` | `✖ 막힘: 공개 상태 확인 전 → status --sample sponsor --advance-days 2를 실행하세요` | 의도한 exit 1, 실제 문구 일치 |
| `python blog.py sponsor review` → `gate --sample sponsor --approve 서윤` | 수정된 mock 원고 준비 후 광고주 확인·새 승인 fc29bae7ffff | 본문 오류 복구 경로 실제 성공 |
| `.venv/bin/python course.py doctor` | 새 venv 인터프리터의 진단 성공 | 활성화 대체 경로와 같은 인터프리터로 직접 실행 |

오류 표의 `허용되지 않은 전이입니다`, `협찬 대장 승인 불일치`는 키트 함수의 실제 ValueError도 발생시켜 확인했다. PowerShell 전용 `py`, `Get-Location`, `Get-ChildItem`, `Activate.ps1`, `Copy-Item`, `.venv\\Scripts\\python.exe`는 Linux에서 실행할 수 없어 표기 검토만 했다.

## 학습자 질문 자체 점검

A1 여섯 질문 모두 **직답 + 예 + 지금 할 행동**이 본문에 있다. 이 표는 본문에 넣지 않았다.

| 질문 | 직답·예 | 본문에서 하는 일 | 판정 |
|---|---|---|---|
| A1-Q1 가상환경·실행 폴더 | 키트 전용 Python, blog.py/course.py가 보이는 폴더 | pwd/ls 또는 Get-Location/Get-ChildItem, venv 생성 | 충족 |
| A1-Q2 결과가 다를 때 확인 순서 | Python→현재 폴더→기본 설정 | doctor, 기본 mock 확인, 복원 후 check | 충족 |
| A1-Q3 PowerShell 차이 | py 런처·Scripts 경로·활성화, 차단 시 직접 python.exe | OS 탭과 활성화 대체 실행 | 충족 |
| A1-Q4 Docker 없이 완주 | 모든 장의 기본 경로는 mock | status --mock, sample, Docker는 선택 상자 | 충족 |
| A1-Q5 포트·연결 오류 | 진단 8767과 실제 임시 포트를 구별 | 내가 켠 서버 Ctrl+C, doctor, mock 설정 후 재실행 | 충족 |
| A1-Q6 꼬였을 때 복구 | 운영 폴더를 피해 별도 연습 폴더, 교체 대상 명시 | 보관 파일 복사→reset/start→명령 재실행→check | 충족 |

| 질문 | 직답·예·행동의 위치 | 판정 |
|---|---|---|
| A9-Q1 제안 조건 | 단계①: 제공품·현금·기한·반납을 함께 묻는 계약 질문 | 충족 |
| A9-Q2 작은 지표의 미디어킷 | 먼저 답부터·단계②: 실제 기간별 지표·주제·대표글, 모의 숫자 대체 | 충족 |
| A9-Q3 문의부터 정산 | 상태 그림·도구·명령②~⑤, 실제 대장 최종 상태 | 충족 |
| A9-Q4 표시 삭제·칭찬·아이 얼굴 요구 | 세 판정 표·단계③: 프로젝트 거절과 실제 표시/경험 기준 | 충족 |
| A9-Q5 수면 충돌 협찬 | 단계①: 포근담요 거절 사유·정중한 회신 예·그림책 소재 대안 | 충족 |
| A9-Q6 현물·2차 사용 | 계약 질문의 매체·기간·편집·비용, 단계⑤의 현물 기록·공식 상담 | 충족 |

## 인계와 남은 일

- [장 틀 사용법 한 쪽](phase-BX3-chapter-guide.md)
- [통합·키트 요청](phase-BX3-requests.md): BX 출처 검사 등록, A1 맛보기 expected 범위, 진단 포트, 세금 CSV 칸. 키트를 고치지 않고 차이를 기록했다.
- 남은 본문은 준비 중으로 유지했다. PROJECT_STATE·서가·배포 상태는 통합 담당자에게 넘긴다.
- 대표 화면: [A9 상태 그림](phase-BX3/a9-state-1280-light.png), [A1 데스크톱](phase-BX3/a1-1280-light.png), [A9 360px 다크](phase-BX3/a9-360-dark.png), [협찬 도구 375px](phase-BX3/tool-375-light.png). 캡처는 직접 구현한 교과서 화면만 포함한다.

완료 알림: 사용자 지정 `python3 scripts/notify.py`로 한국어 5줄 보고와 A9 상태 그림을 전송했다. exit 0, HTTP 200 확인.
