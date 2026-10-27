# BX5 · BlogBook 심화편 통합과 클린룸 재현

2026-10-28. **A0~A12·E2E 14장 통합·본문↔키트 검사·클린룸 재현·로컬 게이트 완료.** 커밋·push·실계정 로그인·게시·결제는 하지 않았다. 다음은 BX6 초보자·정책 독립 검토와 Claude Code 검수다.

## 범위와 구현

기준은 `DESIGN-blog-advanced.md` 8절, `STYLE-GUIDE.md`, BX3/BX4a/BX4b 결과·requests·glossary, `research-blog-advanced/SOURCES.md`다. Level 2 통합으로 기존 설계·단계 기록을 이어 쓰며 새 ADR은 만들지 않았다. 시작 시 Git 변경은 없었다.

- [x] 장 데이터·표지·정적 목차의 14장을 모두 완성으로 표시하고 같은 트랙 안의 이전/다음과 용어·출처 링크를 연결했다. JS가 없어도 이전/다음이 남는다.
- [x] 용어 25개를 추가해 기존 43개와 합쳤다. 심화 본문 첫 사용에 기존/새 용어를 연결했다. 실제 심화 인용 BX 출처 89개를 확인 범위·인용 위치와 함께 credits에 등록했다. 실험실에 심화 도구 진입을 더했다.
- [x] 만드는 것과 확인할 점을 독립된 공통 절로 맞췄다. A10/A11 FAQ는 오류 절 안에서 보충한다. A1/A9의 동일 OS 명령과 OS 탭 안의 같은 앞뒤 명령을 공통 블록으로 꺼냈다. 서로 다른 가상환경·복사 명령만 OS 탭에 남겼다.
- [x] 키트 변경 뒤 `course/build_expected.py`로 expected와 장 시작 ZIP을 재생성하고 성공 stdout·코드 발췌·관찰 안내를 맞췄다.
- [x] 서가 카드·진행표·PROJECT_STATE를 갱신했다. 부록 생성기가 새 용어를 지우는 회귀를 발견해 통합된 심화 용어·출처·도구 구역을 보존하도록 고쳤다.

`book.css`·`common.js`에는 별도 수정이 필요한 요청이 없어 기존 기능을 유지했다. `advanced.css`는 공통 절의 간격과 용어 링크 표시를 보완했다. 배포 구조와 의존성은 바꾸지 않았다.

## 요청별 처리와 실제 경계

| 기존 요청 | 처리 결과 |
|---|---|
| BX 출처 등록·BS074/L107 오인 | check_site가 심화 SOURCES도 읽는다. 외부 URL 쿼리·코드 줄을 출처 번호로 세지 않는다. 미등록 출처 0. 회귀 fixture로 실제 오류→수정 후 통과 확인. |
| A1 맛보기와 expected 차이 | `run --sample`을 A1 기본 명령/예상 결과에 포함했다. 날짜 바꾸기 뒤에는 전체 복원 명령을 명시했다. |
| 진단 포트와 실제 mock 차이 | doctor도 127.0.0.1의 임시 포트를 검사한다. 8767 점유 중에도 진단이 통과하는 테스트를 추가했다. |
| 협찬 CSV 반납·비용 | `return_terms`·`costs` 열을 계약·정산 기록에서 내보낸다. A9 안내를 맞췄다. |
| A6 날짜·URL·공개 재조회 | status.json에 date/date_gmt/link를 보존한다. `status --sample info --advance-days 2`를 기본 명령·expected·본문에 추가했다. |
| A6 시작 상태 | A1 맛보기의 기존 예약 글을 이어받아 prepare가 future를 반환한다. 새 글은 draft, 같은 글은 기존 ID 재사용임을 본문에 명시했다. 공개 재조회 뒤 반복 발행의 실제 결과 publish도 안내에 맞췄다. 기존 재사용 동작을 바꾸지 않았다. |
| A8 등록부와 관계 정보 | 샘플의 program을 쿠팡(모의)로 통일하고 실제 생성되는 쿠팡 문구를 본문에 반영했다. 실제 프로그램 가입·승인과는 구분한다. |
| A11 가상 승인 예약 | cron/launchd/Windows/Actions 예시를 모두 `report`로 바꿨다. 예약 예시는 승인·발행을 실행하지 않는다. |
| A12 확인 기록 | 여섯 항목마다 확인자·근거 파일/주소·보류 이유/다음 확인일 칸을 생성한다. 원본 비교용 파일은 그대로 두고 개인 복사본에 기록하도록 안내한다. |
| 장 상태·공통 OS·용어·출처·서가 | 요청한 공통 파일에 통합했다. A1의 중간 장 준비 중 안내와 표지의 샘플 상태는 남아 있지 않다. |
| A4 실제 LLM CLI·프롬프트 산출물 | 기존 차이 안내를 유지했다. 고정 mock가 기본이며 전송 주입 어댑터를 실제 유료 CLI 연결로 표시하지 않는다. 신규 실연결 확장은 하지 않았다. |
| A10 실제 수집/재점수·A11 영속 상태/실알림 | 고정 지표/주입 어댑터·선택 운영 과제라는 기존 설명을 유지한다. OAuth 수집기·외부 상태 저장·실제 알림 수신을 구현 완료로 표시하지 않는다. |

수동 편집 뒤의 체크포인트는 모든 실행 장에서 **start → 해당 장의 기본 명령 전체 → check**로 통일했다. 재현 중 expected JSON의 정렬된 키 순서를 명령 순서로 쓴 오류가 드러나 commands.md 순서로 고쳤고, 검사기에 체크포인트 순서 회귀 검사를 추가했다.

## 14장 가독성 점검표

✓는 해당 절이 같은 순서로 있고 실제 내용을 확인했다는 뜻이다. 단계는 여러 주제 절로 나뉠 수 있다. 코드 수치는 실제 발췌 줄 수이며 바로 아래 읽는 법 표가 있다. 원본·설정 복원에 필요한 명령 반복은 남기고, 같은 OS 명령·샘플 시기 안내·오래된 관찰 설명은 정리했다.

| 장 | 먼저 답 | 만드는 것 | 한눈 | 시작 | 단계 | 코드·표 | 바꿔 보기 | 오류 | 체크 | 확인 | 정리 |
|---|---|---|---|---|---|---|---|---|---|---|---|
| A0 | ✓ | ✓ | ✓ | ✓ | ✓ | 3줄·✓ | ✓ | ✓ | ✓ | ✓ | ✓ |
| A1 | ✓ | ✓ | ✓ | ✓ | ✓ | 17줄·✓ | ✓ | ✓ | ✓ | ✓ | ✓ |
| A2 | ✓ | ✓ | ✓ | ✓ | ✓ | 13줄·✓ | ✓ | ✓ | ✓ | ✓ | ✓ |
| A3 | ✓ | ✓ | ✓ | ✓ | ✓ | 9줄·✓ | ✓ | ✓ | ✓ | ✓ | ✓ |
| A4 | ✓ | ✓ | ✓ | ✓ | ✓ | 5줄·✓ | ✓ | ✓ | ✓ | ✓ | ✓ |
| A5 | ✓ | ✓ | ✓ | ✓ | ✓ | 7줄·✓ | ✓ | ✓ | ✓ | ✓ | ✓ |
| A6 | ✓ | ✓ | ✓ | ✓ | ✓ | 14줄·✓ | ✓ | ✓ | ✓ | ✓ | ✓ |
| A7 | ✓ | ✓ | ✓ | ✓ | ✓ | 17줄·✓ | ✓ | ✓ | ✓ | ✓ | ✓ |
| A8 | ✓ | ✓ | ✓ | ✓ | ✓ | 17줄·✓ | ✓ | ✓ | ✓ | ✓ | ✓ |
| A9 | ✓ | ✓ | ✓ | ✓ | ✓ | 22줄·✓ | ✓ | ✓ | ✓ | ✓ | ✓ |
| A10 | ✓ | ✓ | ✓ | ✓ | ✓ | 14줄·✓ | ✓ | ✓ | ✓ | ✓ | ✓ |
| A11 | ✓ | ✓ | ✓ | ✓ | ✓ | 10줄·✓ | ✓ | ✓ | ✓ | ✓ | ✓ |
| A12 | ✓ | ✓ | ✓ | ✓ | ✓ | 8줄·✓ | ✓ | ✓ | ✓ | ✓ | ✓ |
| E2E | ✓ | ✓ | ✓ | ✓ | ✓ | 11줄·✓ | ✓ | ✓ | ✓ | ✓ | ✓ |

A1은 OS 탭 2곳, A9는 복사 명령 탭 1곳만 남았다. 25줄 초과 발췌 0, 읽는 법 표 누락 0, 같은 OS 명령 블록 0이다. 가상 인물 서윤·태오와 「봄이랑 크는 집」을 유지했다. 세부 구조·줄 수는 [readability.json](phase-BX5/readability.json)에 있다.

## 자동 검사와 클린룸

`python3 scripts/check_blog_advanced.py --check`는 쓰기 없이 게이트로 쓴다. HTML의 data-run/data-course를 읽어 장별 명령·순서를 commands.md와 비교한다. 기본 구역에 다른 장 명령을 끼우거나 표시를 떼어도 실패한다. 준비·복원·바꿔 보기의 명령도 허용 목록과 대조하고, 성공 samp는 expected stdout, data-source 파일:시작줄:끝줄은 실제 키트 코드와 비교한다. 코드 25줄·읽는 법 표·OS 중복도 검사한다.

- [대조 결과](phase-BX5/alignment.txt): **14장·기본 명령30·성공 출력30·발췌14, 불일치0**.
- [HTML 추출 JSON](phase-BX5/extracted-commands.json): 기본·선택·바꿔 보기·OS를 구분한 전체 명령 블록. `--extract 경로`로 다시 만든다.
- [기존 클린룸](phase-BX5/repro.txt): `bash scripts/repro_blog_advanced.sh`. 새 복사본·새 venv에서 전체 장 실행/check, expected 재생성 동일성, 전체 pytest를 검사한다.
- [기본 HTML 재현](phase-BX5/html-cleanroom.txt): `python3.11 scripts/check_blog_advanced.py --check --replay`. 추출한 시작·기본·check **56명령**을 별도의 빈 복사본·새 venv에서 실행하고 stdout도 비교한다. A0는 계획 장으로 실행 명령이 없다.
- [전체 읽는 순서](phase-BX5/reading-order.txt)·[각 stdout](phase-BX5/reading-order.json): `python3.11 docs/results/phase-BX5/verify-reading.py`. 추출 JSON의 Unix/공통 명령과 본문에 적힌 수동 편집을 함께 따라 **138명령**, 의도한 차단2회, 실행 장13개 체크포인트를 통과했다. 원본 코드·설정을 되돌리는 행동도 포함했다.

### 기존 재현 스크립트 원문 끝부분

```text
✔ 통과: A12 예상 출력 생성
✔ 통과: E2E 예상 출력 생성
✔ 통과: 예상 출력과 장 시작 상태 일치
........................................................................ [ 58%]
....................................................                     [100%]
124 passed in 6.98s
재현 결과: 통과 1 / 실패 0
```

### HTML 기본 명령 재현 원문 끝부분

```text
✔ 통과: mock_normal
✔ 통과: regulated_refusal
✔ 통과: missing_data
✔ 통과: reapproval
✔ 통과: timeout_no_duplicate
✔ 통과: backup_restore
$ python course.py check E2E
✔ 통과: E2E 산출물·상태·터미널 출력 일치
HTML 추출 명령 클린룸: 56개 성공 / 불일치 0
```

### 바꿔 보기 포함 원문 끝부분

```text
✔ 통과: regulated_refusal
✔ 통과: missing_data
✔ 통과: reapproval
✔ 통과: timeout_no_duplicate
✔ 통과: backup_restore
$ python course.py check E2E
✔ 통과: E2E 산출물·상태·터미널 출력 일치
E2E 읽는 순서·변경 후 복원 통과
전체 읽는 순서: 138 명령 / 예상한 차단 2 / 체크포인트 13장 통과
```

## 최종 게이트

| 검사 | 실제 결과·근거 |
|---|---|
| 심화 style_lint | 14/14, 금지어·내부 용어·단서 표현0. [JSON](phase-BX5/style-lint.json) |
| 정적 사이트·서가 | site-blog·site·site-shorts·site-baby 각각 오류0. check_site는 각 책과 서가를 함께 검사한다. [블로그](phase-BX5/check-site-blog.json)·[릴스](phase-BX5/check-site-reels.json)·[쇼츠](phase-BX5/check-site-shorts.json)·[육아](phase-BX5/check-site-baby.json) |
| 브라우저 | 14장+표지+목차 16경로 ×1280/375/360×라이트/다크 =96화면. 가로 넘침·콘솔/페이지/내부 HTTP 오류0. [기록](phase-BX5/browser.json) |
| 키보드·JS 없음·도구 | 모든 경로 skip 링크, OS 방향키/Home, 계산·다운로드, 관문4샘플, 협찬13상태, 표시·진행 저장/복원/초기화·차단/손상 저장값 등42회. JS 꺼짐32회에서 본문·정적 목차·이전/다음 읽기 통과. 위 기록 참조 |
| 최종 수정·공통 부록·서가 | A1/A6/A8/A9/A12·용어집/출처/실험실·서가/진행표10경로×6=60화면. 실제 배포 경로로 조립한 로컬 서버에서 넘침·콘솔0. [기록](phase-BX5/final-pages.json) |
| blog-auto-kit | 새 복사본 Python3.11.15·새 venv에서 **124 tests** 통과. expected·시작 ZIP 동일성 통과. repro.txt 참조 |
| 기존 키트 회귀 | starter-kit116·shorts-kit38·blog-kit97·auto-kit93, 모두 실제 실행 exit0. [환경·결과](phase-BX5/kit-regressions.json)·[쇼츠 원문](phase-BX5/shorts-kit-tests.txt). blog-kit은 기본 quiet로 개수 요약이 없어 [수집97개](phase-BX5/blog-kit-collection.txt)도 별도 확인했다. |
| 공용 Python 검사 | 61 passed, 17 subtests passed. 명령/출력/발췌/체크포인트 변조·출처 URL 오인·부록 재생성 보존 회귀 포함. [원문](phase-BX5/scripts-tests.txt) |
| 기타 | book.js·advanced.js node --check, 재현 셸 bash -n, git diff --check 통과 |

재현 가능한 브라우저 코드는 [verify-browser.cjs](phase-BX5/verify-browser.cjs)·[최종 페이지 확인](phase-BX5/verify-final-pages.cjs)에 있다. 첫 코드는 저장소 루트의 로컬 서버8855, 두 번째는 check_site.deployment_files와 같은 배포 매핑의 로컬 서버18856을 사용했다. 원본 도구·공통 자산은 배포 대상 파일을 연결해 확인했다.

## 최종 검토·대표 화면·남은 확인

최종 코드 검토에서 A6의 기존 예약 재사용/공개 상태와 A8의 제휴 문구 안내 불일치2건을 확인해 본문을 수정했다. 명령·출력 대조는 설명 문장의 뜻까지 검증하지 않으므로 실제 관찰 안내도 함께 읽었다. 이 검토는 BX6 독립 초보자·정책 검토를 대신하지 않는다.

- [A1 360 다크](phase-BX5/advanced-01-environment-html-360-dark.png)·[표지 목차](phase-BX5/index-html-contents-1280-light.png)
- [A6 기존 예약 재사용 설명](phase-BX5/06-publish-detail-360-dark.png)·[A8 실제 제휴 문구](phase-BX5/08-affiliate-detail-360-dark.png)·[A12 기록 코드](phase-BX5/12-policy-detail-360-dark.png)

Windows PowerShell/macOS 실기기, 이번 단계 Docker·실제 호스팅·OS 예약 등록/절전/다음날 실행, 실제 WordPress/GA4/GSC/광고·제휴 인증/수집/게시, 외부 알림 수신·실제 광고주 회신·세금 신고는 미실행이다. Docker 선행 검증은 BX3k 기록과 구별한다. 실제 LLM CLI·지표 수집·외부 영속 상태/알림은 선택 확장 과제로 남는다. 자동 통과·가상 사람 승인·실서비스 성공을 혼동하지 않는다.

문서 갱신: 이 결과와 PROJECT_STATE를 최신 상태로 반영했고 서가 BX 상태를 갱신했다. 연구 출처 내용·기존 다른 책/키트 구현은 변경하지 않았다. 공개 산출물에 토큰·개인 환경·Hermes 원응답을 넣지 않았다.

완료 알림: 지정한 `python3 scripts/notify.py`로 한국어 5줄 전송, exit0·HTTP200 확인. 커밋·push는 하지 않았다.
