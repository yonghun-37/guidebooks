# Phase BX7b — 승인된 틀과 검증 데이터만 자동 발행

2026-10-28. **구현·로컬 게이트 완료, Claude Code 검수 대기.** 실계정·유료 호출·commit/push는 하지 않았다. `docs/DESIGN-blog-advanced.md`는 읽기만 했다. 요청한 변경 범위를 따라 PROJECT_STATE·설계·다른 책은 수정하지 않고 이 결과 기록을 현재 작업의 인계 문서로 남긴다.

## 문제·요구와 완료한 계획

BX7은 자유 문장을 단어 목록으로 검사한 뒤 신규 info/play 글을 자동 허용했다. Claude 우회 10개를 그대로 옮겨 실행하면 **5개 실패·5개 통과**였다([수정 전](phase-BX7b/red-bypass.txt)). 단어를 늘리는 대신 자동 허용의 입력 범위를 닫았다.

- [x] Claude 10개 우회를 `tests/test_bx7b_claude_bypass.py`로 옮김. 각 반례에서 정상 서버 초안을 먼저 만든 뒤 변경·예약을 시도해 실제 글 한 개가 draft로 남는지 확인
- [x] 글 틀·닫힌 JSON Schema 승인과 해시 변경 무효화
- [x] 발행 직전 데이터·현재 설정·본문/HTML 바이트·전체 문서 재검사
- [x] 본문·HTML URL 추출, 상업 표시 관문·미허용 도메인 사람 검토 연결
- [x] 가상 도서관 주제 틀·명시적 승인 명령·자동 예약 시연
- [x] A0/A3/A5/A6/A11/A12/E2E 및 영향받은 장의 명령·출력·발췌 동기화
- [x] 전체 게이트·3폭×2테마 브라우저 검사·결과 기록

## 구현과 결정

- `content/templates/library.md`와 `library.schema.json`을 `blog.py template approve library --by 서윤`으로 승인한다. 기존 SQLite `runs`에 검토자·날짜·두 파일의 SHA-256을 보관한다. 별도 DB·외부 서비스·런타임 의존성은 추가하지 않았다. 템플릿이나 데이터 규칙이 한 바이트라도 달라지면 이전 기록은 유효한 승인으로 사용되지 않는다.
- `content/template_schema.py`는 **제한된 JSON Schema 부분집합**만 지원한다. 필수 칸만 있는 닫힌 객체, 길이 제한이 있는 문자열 열거값, 범위가 있는 정수를 받는다. 자유 문자열·중첩·미지원 규칙은 승인 단계부터 거절한다. 샘플의 주제·읽기 대상·자료 구분·기관 URL은 모두 열거값이다. 정수와 불리언도 구별한다. 일반 JSON Schema 전체를 구현했다고 주장하지 않는다.
- `content/templates.py`가 틀과 데이터로 원문·HTML·제목·설명·출처 메모를 만든다. `gates/risk.py::may_auto_publish`는 단어 탐지를 허용 근거에서 제거했다. 신규 확인·설정 허용 유형·모든 관문 pass와 함께 현재 틀 승인, 데이터 검증, 원문/HTML의 UTF-8 바이트 일치 및 문서 전체 동등성을 요구한다. 임의 필드·작성 경로·경험·사진·자유 문장이 섞이면 자동 대상이 아니다.
- `automation.T1`이 틀 증명이 없는 글을 사람 검토 보고서와 대기열에 남긴다. 건강·식별·상업 단어 검사는 기존 차단/자료 보류와 보조 검토 표시로 유지한다. 법적 금지·자료 보류는 글별 승인으로 풀리지 않는다. 갱신·원격 변조·미디어·응급 공통 문구의 기존 보호도 유지한다.
- `gates/links.py`는 마크다운 링크·이미지·참조 정의, 일반 URL, HTML href/src/srcset/formaction 등에서 URL을 모은다. 알려진 제휴·쇼핑 도메인은 경제관계 검사에 연결하고 사람 검토를 요구한다. 정확한 기관 호스트 허용 목록 밖 주소·상대 URL·다른 스킴도 사람 검토다. 쇼핑 도메인을 허용 목록에 넣어도 자동 허용하지 않는다. 알려지지 않은 쇼핑 주소도 기본 미허용 도메인으로 사람에게 간다.
- `--config`로 고른 경로를 생성·관문·준비·승인·발행까지 전달하고 준비 기록에도 남긴다. 발행 때 그 파일을 다시 읽는다. 기본 설정 파일로 몰래 돌아가거나 초안 저장 때 읽은 도메인 목록만 재사용하지 않는다.
- 기본 `run --sample`도 자유 문장의 승인을 대신 만들지 않는다. A1에 `draft → publish --prepare → 초안을 읽고 gate --approve → run --sample`을 넣었다. A3는 틀 승인 명령과 실제 해시 출력, A6는 별도 복사본의 auto 예약·틀 변경 거부를 설명한다. `run --sample library`는 틀 승인을 만들거나 글별 승인을 위조하지 않는다([실행 증거](phase-BX7b/template-demo.txt)).
- 도서관 샘플은 기관의 실제 선정 목록을 수집한 결과가 아닌 **가상 편집 목록**임을 원문과 본문에 표시한다. 건강 문장·사진·경험은 없다. 기관 검색 주소와 고정 칸만 채운다.
- A5의 브라우저 도구도 `inspect_document` 결과로 갱신했다. 요청 범위 안의 `site-blog/advanced/05-gates.js`를 사용한다. info가 자유 문장이라 사람 검토로 가는 것을 보여 주며 단어 검사를 자동 허가로 설명하지 않는다. 공용 assets 파일은 변경하지 않았다.

## 회귀와 독립 검토 반영

새 시험은 `tests/test_bx7b_{claude_bypass,templates,links,lifecycle}.py` **60개**다. 승인된 틀의 무승인 future, 승인 없음, 틀/스키마 한 글자 변경, 허용 밖 값/URL/긴 문자열/타입/추가 칸, 원문·HTML·제목·설명 편집, 경험·사진·LLM 경로, 예약 후 틀 변경 시 재실행에서 회수, 명시적 글별 승인 후 예약을 검사했다. BX6·BX7 반례와 나머지 키트 시험을 포함한 전체는 305개다. 과거 자유 문장의 자동 허용 양성 시험 두 개는 새 요구대로 승인 대기로 바꿨다.

읽기 전용 독립 코드 검토가 찾은 항목은 모두 수정했다.

| 발견 | 처리·증거 |
|---|---|
| 선택한 `--config` 대신 기본 도메인 목록 사용 | 선택 경로를 전 단계에 전달하고 발행 직전 재로딩. [수정 전 실패](phase-BX7b/red-custom-config.txt), 선택 설정/준비 후 설정 변경 회귀 통과 |
| 기본 mock 시연의 자유 문장 자동 승인 기록 | 가상 승인 생성 제거, A1 직접 승인 명령 추가. [수정 전 실패](phase-BX7b/red-demo.txt), 무승인 draft·직접 승인 뒤 future 확인 |
| 참조 링크·formaction 추출 누락 | URL 추출에 포함, 상대 주소도 검토 보고서에 표시 |
| 정수 enum에서 `1 == True`로 잘못 통과 | 정수 열거값의 실제 타입·범위 검사. 위 URL 두 건과 함께 [수정 전 실패](phase-BX7b/red-review-edges.txt) 후 통과 |

이 검토는 코드 검토이며 Claude의 최종 검수·의료/법률 재심사·실서비스 검증을 대신하지 않는다.

## 최종 게이트

| 게이트 | 결과·증거 |
|---|---|
| 예상 출력 재생성·`build_expected.py --check` | 13개 장 출력/시작 ZIP 일치. [생성](phase-BX7b/build-expected.txt), [대조](phase-BX7b/build-check.txt), 최종 클린룸에서도 확인 |
| `check_blog_advanced.py --check` | **14장·명령35·출력35·발췌14·불일치0**. [대조](phase-BX7b/alignment.txt) |
| 전체 키트 pytest | **305 passed**. [출력](phase-BX7b/pytest.txt). [새 회귀만](phase-BX7b/green-bx7b.txt) 60 passed |
| 검사기 pytest | **63 passed**. [출력](phase-BX7b/scripts-tests.txt) |
| `repro_blog_advanced.sh` | **통과1·실패0**. Python 3.11.15 새 venv·키트 복사본, 전 장·7시나리오·expected·305 tests 통과. [전체 기록](phase-BX7b/repro.txt) |
| 문체 | 심화14장 통과, 금지/내부 용어·단서 위반0. [결과](phase-BX7b/style-lint.json) |
| 네 책 `check_site` | Reels51·Shorts49·Blog50·Baby35 HTML, 오류 각각0. [Reels](phase-BX7b/check-site.json), [Shorts](phase-BX7b/check-site-shorts.json), [Blog](phase-BX7b/check-site-blog.json), [Baby](phase-BX7b/check-site-baby.json) |
| 브라우저 | **102화면**(심화14장·목차2경로·출처 ×1280/375/360×라이트/다크), 무JS34·도구/저장48 검사. 가로 넘침·콘솔·페이지·로컬HTTP 오류0. A3 승인 출력·A6 펼친 자동 시연도 확인. [결과·입력 지문](phase-BX7b/browser.json), [실행](phase-BX7b/browser-stdout.txt), [스크립트](phase-BX7b/verify-browser.cjs), 같은 폴더 PNG |
| 변경 경계·일관성 | `git diff --check` 통과, 지정 범위 밖 변경 없음. 브라우저 최종 입력 해시 재대조 일치. 설계·다른 책·공용 assets·다른 키트·Git 기록 미변경 |

## 남은 확인

- Claude Code의 최종 검수·커밋·배포가 남았다. 이 작업은 공개 배포를 수행하지 않았다.
- 틀 승인과 글별 승인 명령은 사람이 검토했다는 기록이다. 검토자의 실제 독해·자료의 진실·사진 내용·권리·계약을 코드가 증명하지 않는다. 자동 작업이 승인 명령을 대신 실행하지 않도록 운영한다.
- 틀·규칙 변경은 다음 준비/발행 경로에서 재검사한다. 파일 변경 자체를 감시해 원격 예약을 즉시 취소하는 상주 작업은 없다. DB만 복구해도 현재 파일 해시가 달라지면 자동 허용하지 않는다. 틀·데이터 파일도 코드와 함께 별도 버전 보관한다.
- Windows/macOS 실기기·Python3.12·실 WordPress·OS 예약 등록·기관 자료 실수집·실발행·유료 공급자는 실행하지 않았다. HTTP 시험과 브라우저 검사는 로컬 mock/Chromium 기준이다. 외부 정책·세무·API의 기존 보류를 해소했다고 주장하지 않는다.

완료 알림: 요청된 `scripts/notify.py` 디스코드 전송 성공(HTTP 200).
