# BX3k · blog-auto-kit 구현 결과

완료: 2026-10-27. 지정한 `blog-auto-kit/`, `scripts/repro_blog_advanced.sh`, 이 문서만 작성했다. 기존 키트는 읽기만 했으며 커밋·push·실계정 로그인·유료 키 사용·외부 블로그 발행은 하지 않았다. `docs/prompts/phase-BX3k.md` 변경과 동시 작업의 `docs/prompts/phase-BX3.md`는 보존했다. 명시한 범위에 따라 PROJECT_STATE와 다른 문서는 수정하지 않았다.

## 구현·검증 결과

- [x] 표준 라이브러리만으로 mock LLM→관문→서버 초안→해시 승인→예약→공개 재조회. 실행 의존성 lock은 불필요하며 pytest와 전이 의존성만 dev lock에 고정했다.
- [x] 고정 날짜·시드, SQLite 상태, 최종 원고/로컬·원격 사진/분류/협찬 자료 해시, 날짜별 예약 상한과 내용 해시 잠금. 결과 불명 시 조회하며 생성 POST를 반복하지 않는다.
- [x] 건강·협찬·제휴·아이 사진/경험·갱신의 사람 승인 강제. 관문은 법적 금지/프로젝트 거절/자료 보류를 구분한다. 원고·출처 수치·최종 HTML·EXIF·표시·근접 중복을 검사한다.
- [x] 문의 항목에 맞춘 처리방침과 미연결 양식, 광고·제휴·협찬 대장/미디어킷/보고/세금 CSV, 모의 지표와 분석 API 요청 어댑터, 알림 드라이런·예약 생성·백업 복구.
- [x] A1~A12+E2E의 명령·시작 ZIP·예상 출력·해시/논리 상태, 독립 시작 검사, 6종 시나리오를 pytest와 repro 양쪽에 연결했다.
- [x] 독립 검토에서 발견한 준비 후 사진 변경, 서버 원고 변경, 협찬 재승인 복귀, 계약 해시 누락, 근접 중복 경로 누락을 수정했다. 예약 후 불일치는 승인 취소·초안 회수로 처리하며 회수 확인 실패는 unknown 보류로 기록한다.

검증: `bash scripts/repro_blog_advanced.sh` **exit 0**, Python **3.11.15**, **119 passed**. 별도 전체 pytest도 **119 passed in 7.07s**. `course/build_expected.py --check` 바이트 비교와 전 장 독립 시작 검사가 포함됐다. Python 3.12는 이 컴퓨터에 없어 미실행이다. Windows·macOS 실기기 검증은 미실행이며, PowerShell 명령 표기와 파일 LF는 검사했다.

## 장별 명령·예상 출력·집필 인계

정확한 복사 대상은 `course/commands.md`이다. 모든 행은 `python blog.py` 또는 `python course.py`로 시작한다. 아래 발췌는 시작 줄에서 **25줄 이하**를 골라 쓰고 장 전체 출력은 `course/expected/<장>/terminal.txt`에서 가져온다. 실제 승인 해시는 해당 expected 파일을 그대로 따른다.

| 장 | 본문 명령·정확한 목록 위치 | 예상 출력/산출물 요약 | 발췌 후보(키트 기준 시작 줄) |
|---|---|---|---|
| A1 | `doctor / status --mock` · [명령 목록](../../blog-auto-kit/course/commands.md#L15) | Python·폴더·권한·포트·고정 시계 / REST 연결 | `course/doctor.py:8` |
| A2 | `pages` · [명령 목록](../../blog-auto-kit/course/commands.md#L17) | 4개 정적 페이지·최소 문의 항목 | `monetize/pages.py:6` |
| A3 | `topics` · [명령 목록](../../blog-auto-kit/course/commands.md#L18) | 월령·발달·제도·놀이·그림책 지도 | `content/topics.py:2` |
| A4 | `draft --sample info/play/affiliate` · [명령 목록](../../blog-auto-kit/course/commands.md#L19) | 3개 초안 / 경험·사진 빈 칸 / 비용 0 기록 | `providers/mock.py:5` |
| A5 | `gate --sample info/play` · [명령 목록](../../blog-auto-kit/course/commands.md#L22) | 정보 통과 / 터미타임 사람 검토 대기 | `gates/risk.py:5` |
| A6 | `publish --prepare → gate --approve → publish → status` · [명령 목록](../../blog-auto-kit/course/commands.md#L24) | post_id=1, draft→future / 최종본 승인 해시 | `wordpress/integrity.py:21` |
| A7 | `ads` · [명령 목록](../../blog-auto-kit/course/commands.md#L28) | 점검표·게시자 ID 자리표시·광고 위치·모의 지표 | `monetize/ads.py:8` |
| A8 | `affiliate → gate` · [명령 목록](../../blog-auto-kit/course/commands.md#L29) | 등록부 CSV·첫 문단 표시·실제 링크 sponsored | `monetize/affiliate.py:37` |
| A9 | `sponsor demo → 사람 작성·승인·예약·공개 확인 → sponsor settle` · [명령 목록](../../blog-auto-kit/course/commands.md#L31) | 포근담요 declined / 도담 settled / CSV·미디어킷 | `monetize/sponsor/states.py:2` |
| A10 | `report` · [명령 목록](../../blog-auto-kit/course/commands.md#L38) | 가상 주간 지표·시간대·갱신 대상 | `analytics/adapters.py:23` |
| A11 | `run --ops → run --restore` · [명령 목록](../../blog-auto-kit/course/commands.md#L39) | 드라이런 알림·예약 예시·ZIP·복구 | `ops/backup.py:33` |
| A12 | `run --audit` · [명령 목록](../../blog-auto-kit/course/commands.md#L41) | 출시·정책·현물·휴직급여 확인 목록 | `core/actions.py:58` |
| E2E | `run --scenarios` · [명령 목록](../../blog-auto-kit/course/commands.md#L42) | 6종 모두 통과 | `course/scenarios.py:17` |

## 파일 트리와 가독성

배포 파일 **167개**, 텍스트 **200줄 초과 0개**, 함수 **40줄 초과 0개**. 가장 긴 텍스트는 `tests/test_gates.py` 180줄, 가장 긴 함수는 `gates/products.py:product_checks` 38줄이다. 괄호는 실제 줄 수이며 PNG/JPEG/ZIP은 바이너리 바이트 수다. runtime `private/`, `output/`, 캐시는 제외했다.

```text
blog-auto-kit/
./:
  .gitignore(7줄) · README.md(35줄) · blog.py(61줄) · config.example.toml(25줄) · course.py(52줄) · pytest.ini(4줄) ·
  requirements-dev.lock(6줄)
analytics/:
  adapters.py(49줄) · report.py(33줄)
content/:
  affiliate.schema.json(26줄) · info.schema.json(26줄) · markdown.py(27줄) · play.schema.json(26줄) · samples.py(27줄) · schema.py(35줄) ·
  sponsor.schema.json(26줄) · topics.py(10줄)
core/:
  actions.py(83줄) · approval.py(46줄) · cli.py(53줄) · clock.py(16줄) · config.py(53줄) · demo.py(19줄) · files.py(21줄) · hashes.py(25줄) ·
  logs.py(9줄) · publish_actions.py(59줄) · sponsor_flow.py(84줄) · state.py(50줄) · terminal.py(17줄) · workflow.py(77줄)
course/:
  __init__.py(1줄) · artifacts.py(48줄) · build_expected.py(66줄) · commands.md(45줄) · doctor.py(24줄) · execute.py(57줄) ·
  scenario_cases.py(132줄) · scenarios.py(40줄) · snapshots.py(54줄) · steps.py(20줄)
course/expected/A1/:
  hashes.json(5줄) · outputs.json(10줄) · state.json(1줄) · terminal.txt(6줄)
course/expected/A10/:
  hashes.json(41줄) · outputs.json(6줄) · state.json(1줄) · terminal.txt(3줄)
course/expected/A11/:
  hashes.json(46줄) · outputs.json(10줄) · state.json(1줄) · terminal.txt(8줄)
course/expected/A12/:
  hashes.json(47줄) · outputs.json(6줄) · state.json(1줄) · terminal.txt(3줄)
course/expected/A2/:
  hashes.json(9줄) · outputs.json(6줄) · state.json(1줄) · terminal.txt(6줄)
course/expected/A3/:
  hashes.json(10줄) · outputs.json(6줄) · state.json(1줄) · terminal.txt(3줄)
course/expected/A4/:
  hashes.json(16줄) · outputs.json(14줄) · state.json(1줄) · terminal.txt(9줄)
course/expected/A5/:
  hashes.json(21줄) · outputs.json(10줄) · state.json(1줄) · terminal.txt(6줄)
course/expected/A6/:
  hashes.json(23줄) · outputs.json(18줄) · state.json(1줄) · terminal.txt(12줄)
course/expected/A7/:
  hashes.json(28줄) · outputs.json(6줄) · state.json(1줄) · terminal.txt(7줄)
course/expected/A8/:
  hashes.json(31줄) · outputs.json(10줄) · state.json(1줄) · terminal.txt(6줄)
course/expected/A9/:
  hashes.json(40줄) · outputs.json(30줄) · state.json(1줄) · terminal.txt(27줄)
course/expected/E2E/:
  hashes.json(48줄) · outputs.json(6줄) · state.json(1줄) · terminal.txt(7줄)
course/states/:
  A1.zip(471B·바이너리) · A10.zip(72787B·바이너리) · A11.zip(73601B·바이너리) · A12.zip(99401B·바이너리) · A2.zip(1454B·바이너리) · A3.zip(4335B·바이너리) ·
  A4.zip(5346B·바이너리) · A5.zip(17170B·바이너리) · A6.zip(19280B·바이너리) · A7.zip(33836B·바이너리) · A8.zip(35687B·바이너리) · A9.zip(37921B·바이너리) ·
  E2E.zip(100016B·바이너리)
gates/:
  body.py(30줄) · checks.py(90줄) · engine.py(58줄) · privacy_exif.py(37줄) · products.py(42줄) · risk.py(16줄) · sources.py(26줄)
monetize/:
  ads.py(34줄) · affiliate.py(78줄) · pages.py(32줄)
monetize/sponsor/:
  demo.py(75줄) · ledger.py(60줄) · states.py(20줄)
ops/:
  README.md(29줄) · backup.py(116줄) · docker-compose.yml(29줄) · github-actions.yml(19줄) · notifications.py(38줄) · scheduler.py(19줄)
providers/:
  costs.py(45줄) · mock.py(9줄) · openai_adapter.py(46줄)
samples/:
  affiliate.json(62줄) · affiliate.md(11줄) · books.png(546B·바이너리) · books.svg(1줄) · emergency.json(91줄) · fake-exif.jpg(673B·바이너리) ·
  info.json(55줄) · info.md(13줄) · make_images.py(59줄) · nap-blanket.json(9줄) · play.json(45줄) · play.md(7줄) · sponsor-human.txt(1줄) ·
  sponsor.json(62줄) · sponsor.md(9줄)
tests/:
  test_adapter_requests.py(24줄) · test_atomic_content.py(17줄) · test_content.py(28줄) · test_course.py(45줄) · test_gates.py(180줄) ·
  test_integrity.py(109줄) · test_integrity_recovery.py(72줄) · test_monetize.py(122줄) · test_operations.py(41줄) ·
  test_ops_extra.py(105줄) · test_pages_ads.py(26줄) · test_providers.py(58줄) · test_publication_safety.py(176줄) ·
  test_readability.py(32줄) · test_remote_media.py(33줄) · test_scenarios.py(27줄) · test_wordpress.py(50줄)
wordpress/:
  client.py(81줄) · integrity.py(34줄) · mock_data.py(50줄) · mock_server.py(139줄) · prepare.py(104줄) · publish.py(99줄) · quota.py(25줄)
scripts/repro_blog_advanced.sh(49줄)
```

## 클린룸 재현 결과 원문 끝 30줄

새 빈 폴더에 키트만 복사하고 새 venv/dev lock 설치 → commands.md 순서 실행 → 매 장 check → expected 재생성 비교 → 전체 pytest를 수행했다. mock 정상·규제 품목 거절·자료 보류·수정 재승인·응답 유실 중복 방지·백업 복구가 포함된다.

```text
$ python blog.py run --audit
✔ 통과: 출시 전 사람이 확인할 점검표
output/launch-checklist.txt
✔ 통과: A12 산출물·상태·터미널 출력 일치
$ python blog.py run --scenarios
✔ 통과: mock_normal
✔ 통과: regulated_refusal
✔ 통과: missing_data
✔ 통과: reapproval
✔ 통과: timeout_no_duplicate
✔ 통과: backup_restore
✔ 통과: E2E 산출물·상태·터미널 출력 일치
✔ 통과: A1 예상 출력 생성
✔ 통과: A2 예상 출력 생성
✔ 통과: A3 예상 출력 생성
✔ 통과: A4 예상 출력 생성
✔ 통과: A5 예상 출력 생성
✔ 통과: A6 예상 출력 생성
✔ 통과: A7 예상 출력 생성
✔ 통과: A8 예상 출력 생성
✔ 통과: A9 예상 출력 생성
✔ 통과: A10 예상 출력 생성
✔ 통과: A11 예상 출력 생성
✔ 통과: A12 예상 출력 생성
✔ 통과: E2E 예상 출력 생성
✔ 통과: 예상 출력과 장 시작 상태 일치
........................................................................ [ 60%]
...............................................                          [100%]
119 passed in 6.29s
재현 결과: 통과 1 / 실패 0
```

## Docker 실행 결과

실행했다. `127.0.0.1:8877`의 임시 WordPress만 사용했으며, JPEG/PNG 업로드·분류 자동 생성·앱 비밀번호 Basic 인증·401 오류 형식·draft→future→publish·공개 재조회를 같은 REST 클라이언트로 확인했다. 최종 코드의 원문·사진 바이트 무결성 검사→사람 승인→예약도 실제 컨테이너에서 통과했다. 잘못된 인증의 실제 응답은 `rest_forbidden_context`, `data.status=401`이었다. mock도 `code/message/data.status` 구조를 사용한다.

- WordPress **7.1.3**, PHP **8.3.36**, MariaDB **11.4.13**, 기본 플러그인 Akismet **5.7.2**·Hello Dolly **1.7.2**(추가 설치 없음).
- `wordpress:7.1.3-php8.3-apache` → `sha256:e5a724ec7ad9055f48b2941ac1b674b08e77ed60edb8937a6254fb89ec45ddf7`.
- `mariadb:11.4.13-noble` → `sha256:d1891ede5a559f1086f55053bb8cc1569b0298338c4d72d71725a7f74f6ba620`.
- 태그 근거: BRIEFING ③/BX001·BX002, DB 세부 버전은 이번 pull·실행으로 고정했다. 태그는 불변 digest와 다르므로 갱신 시 digest와 expected를 함께 검토한다.
- `docker compose ... -p bx3k-local down -v` 실행 완료. 해당 컨테이너·DB/WP 볼륨·네트워크가 남지 않았음을 확인했다. 실 WordPress의 DB·uploads를 새 환경으로 이전하는 복구는 미실행이며 ops 안내의 별도 과제다. 키트 SQLite+mock 미디어 복구는 6종 시나리오에서 실행했다.

## 결정·한계·근거 부족으로 구현하지 않은 것

- 설계 8절과 BRIEFING ④~⑥를 우선했다. 사후 확인 모드는 유예·거부 수신·지연 검증 전 제공하지 않는다. 낮은 위험만 선택 auto, 나머지는 항상 사람 승인이다.
- SQLite는 논리 SQL 덤프를 고정 ZIP에 넣는다. 엔진 버전에 따른 DB 파일 헤더 차이를 피해 바이트 재현성을 유지하며, 복원 시 새 SQLite DB를 만들고 검증한다. `.env`는 백업하지 않는다.
- 쿠팡 live API는 BXF-029/030의 현행 자격·쿼터·HMAC/가격 저장 근거가 부족해 서명·엔드포인트를 만들지 않았다. 수동 링크·mock 검색/딥링크와 명시적 live 차단만 제공한다.
- OpenAI Responses 구조화 출력(gpt-6-luna), GA4 Data API, GSC 어댑터는 전송 함수를 주입한 모킹 테스트만 했다. 실제 키·OAuth·유료 호출을 연결하지 않았다. 광고/제휴 숫자는 모의 값이며 예상·확정·실입금을 구분한다.
- 문의 폼은 전송 미연결이다. 처리방침은 실제 연락처·도구·위탁/국외 이전 등을 확정한 뒤 공개해야 한다. 아동 광고의 실제 코드 유형이 확인되기 전 TFAT 등 광고 코드는 임의로 만들지 않았다(BXF-023).
- 제품·출처·아이 정보 검사는 명시 데이터/패턴에 기반한다. 의료·법률 판단, 사진 배경의 사람 식별, 가상 제품 확인 자료의 실제 진위는 사람이 확인해야 한다. 최종 서버 원본은 같은 origin에서만 바이트 비교하며 별도 CDN/자동 변환은 연결 전 확인 대상이다.
- 장 집필·사이트 편집·배포는 다음 단계다. 이 단계의 다음 입력은 commands.md/expected와 위 발췌 표다. 기본 PNG는 실제 WordPress가 받는 형식이며 SVG 원본·표준 라이브러리 이미지 생성기도 제공했다.

알림: 사용자 지정 `python3 scripts/notify.py`로 한국어 5줄 완료 보고 전송 성공(exit 0).
