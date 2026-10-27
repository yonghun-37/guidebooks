# Phase BX6-repro · BlogBook 심화편 재현·가독성 독립 검토

**전체 결론: 조건부.** 본문의 Linux·mock 기본 명령은 처음부터 E2E까지 재현된다. A1~A12와 E2E의 최종 체크포인트 13개, E2E 여섯 시나리오가 통과했다. 다만 **A4에서 SQLite 비용 기록을 직접 확인하는 행동은 여는 방법이 없어 차단**됐다. 자동 검사 통과만으로 사람의 확인까지 완료했다고 판정하지 않았다.

학습자 질문 78개: **통과 70 / 부분 8 / 불통과 0**. 부분 판정도 직답 기준의 개선 대상이다. 발견은 **차단 1 / 혼란 6 / 사소 3**이다. 사이트·원본 키트·저장소 스크립트를 수정하지 않았고 commit하지 않았다.

## 검토 방법과 범위

- 검토일: 2026-10-28, Linux·Python 3.11.15. 파이썬 기초만 아는 육아휴직 중 부모 블로거의 역할로 읽었다. 실제 초보자 참가자의 사용자 시험은 아니다.
- 작업 지침·문체 기준만 확인한 뒤 `site-blog/advanced/00-start.html` → A1~A12 → `e2e.html`을 순서대로 읽었다. 설계·기존 결과·프로젝트 상태·기존 재현 스크립트·키트 README/구현은 해법으로 읽지 않았다. 78개 질문 문서는 첫 순차 실습을 끝낸 뒤 열었다.
- 사용자 지시에 따라 ZIP 다운로드는 하지 않고, 빈 임시 폴더에 저장소의 **blog-auto-kit 폴더만** 복사했다. 매 세션 새 `.venv`를 만들었다. 생성물 읽기와 본문이 지정한 설정·샘플 확인만 했다. A3의 코드 한 문장 변경은 본문에 실린 발췌 범위에서 임시 복사본에만 적용하고 원복했다.
- 본문이 선택 사항이라고 한 Docker·실서버·유료 API·실광고/제휴 신청·OS 예약 등록·외부 알림은 선택하지 않았다. 계정·결제 없이 끝내는 기본 경로의 검토이며 이 선택 과제의 성공을 주장하지 않는다. 법·정책의 최신 사실을 검증한 별도 연구도 아니다.
- 본문 밖 해결 명령을 추가하지 않았다. A4 비용 DB 조회는 SQL이나 DB 도구를 추측해 실행하지 않고 미완료로 남겼다. 오류 실험의 입력·복구는 아래에 따로 구분했다.
- 기록용 실행기는 `/tmp`에만 뒀고, 명령·현재 폴더·시각·종료 코드·표준 출력/오류를 남겼다. 편집기·파일 탐색기의 동작은 복사/문자열 편집/이동으로 대행했다. 브라우저 촬영 도구 설치는 검토 장비 준비이며 키트의 설치 요건이 아니다. 검토 도구의 초기 import·브라우저 경로/버튼 선택 오류는 학습 경로 발견에 포함하지 않았다.
- **시간은 명령의 실제 누적 실행 초**다. 장을 읽는 시간·편집기 조작 시간·초보자의 예상 학습 시간으로 환산하지 않았다. 읽기/수동 조작의 장별 시간은 따로 계측하지 않았다. 순차 실습 명령 146회에 13.033초, 준비/재실행/의도한 실패 포함. `chapter-timing.json`의 시작/끝 시각은 초 단위여서 짧은 장의 경과가 0초로 보일 수 있으므로 아래에는 더 정밀한 누적 실행 초를 썼다.

증거: [순차 실습 터미널·수동 확인](phase-BX6-repro/sequential.txt) · [명령별 원기록](phase-BX6-repro/sequential.jsonl) · [전체 실행 집계](phase-BX6-repro/run-summary.json) · [장별 실행 시간](phase-BX6-repro/chapter-timing.json).

## 장별 실행·체크포인트·가독성

점수: 5 = 설명 없이도 다음 행동이 분명함, 4 = 스스로 이어 갈 수 있는 작은 걸림, 3 = 추측/재독이 필요하거나 일부 확인 미완료, 2 = 큰 우회 필요, 1 = 기본 경로 진행 불가. 점수는 명령 성공률과 별도로 매겼다.

| 장 | 실제 결과와 성공 예시 대조 / 체크포인트 | 누적 실행(초) | 가독성 | 이유 |
|---|---|---:|---:|---|
| [A0](../../site-blog/advanced/00-start.html#checkpoint) | 수입 0원·mock 비용 0원/월 표시, 운영계획 네 칸 작성. check A0 없음. | — | 4/5 | 역할·위험별 승인·비용 계산은 분명하다. LLM 등 약어가 앞선다. |
| [A1](../../site-blog/advanced/01-environment.html#checkpoint) | doctor·mock 연결·맛보기 출력 일치. 날짜 변경 후 예약 10/29, 기본 복원 후 check 통과. | 0.94 | 4/5 | 폴더/가상환경 안내가 좋다. 포트·시드 설명과 잘못된 폴더 오류가 부족하다. |
| [A2](../../site-blog/advanced/02-wordpress.html#checkpoint) | pages 네 경로 일치. 문의 전송 미연결, 이메일 변경 두 파일 반영. check 통과. | 0.36 | 4/5 | 로컬 파일과 게시를 잘 구별한다. 서버 기능표의 낯선 약어가 부담이다. |
| [A3](../../site-blog/advanced/03-topics.html#checkpoint) | 여섯 갈래·기준일·제목 변경 반영. 원문 코드 원복 후 check 통과. | 0.33 | 4/5 | 출처·자료 형식·경험 분리가 명확하다. JSON 속성명이 한꺼번에 많다. |
| [A4](../../site-blog/advanced/04-drafts.html#checkpoint) | 세 초안의 경험/작성자 빈 문자열·사진 빈 배열 확인. 예산 0에서도 생성. check 통과, costs 직접 확인은 차단. | 0.63 | 3/5 | 초안/경험 설명은 쉽지만 비용 DB를 여는 행동이 빠져 있다. |
| [A5](../../site-blog/advanced/05-gates.html#checkpoint) | info pass, play review와 이유/행동 일치. risk_flags를 비워도 review. check 통과. | 0.55 | 4/5 | 관문과 사람 승인을 구별하기 쉽다. 코드의 긴 return은 재독 필요. |
| [A6](../../site-blog/advanced/06-publish.html#checkpoint) | 기본 승인 해시 3a9c0b7dbafb 일치. id=1 future→publish. 수정 뒤 거부·재준비·새 승인도 재현. check 통과. | 1.73 | 3/5 | 실습은 되지만 마지막 문장이 앞서 확인한 공개 상태와 충돌한다. |
| [A7](../../site-blog/advanced/07-ads.html#checkpoint) | 광고 파일 다섯 경로·0.12/0.00/0.00 일치. 소제목 위치 변경 확인. check 통과. 0의 오류 문구만 예시와 다름. | 0.47 | 4/5 | 심사/자리표시 구분이 좋다. 광고 관련 약어가 몰려 나온다. |
| [A8](../../site-blog/advanced/08-affiliate.html#checkpoint) | CSV의 날짜·가격 미표시·쿠팡(모의), 첫 문구·sponsored·관문 pass 일치. 날짜 변경/복원 후 check 통과. | 0.62 | 5/5 | 실행→파일 확인→모바일 비교→복원이 구체적이다. |
| [A9](../../site-blog/advanced/09-sponsorship.html#checkpoint) | id=2 draft→future→publish, 승인 f62525058efb, declined/settled, 현물/현금 분리 일치. 자동 모드 승인 거부도 일치. check 통과. | 1.76 | 4/5 | 계약부터 정산까지 이어진다. 내 문의를 직접 기록하는 방법은 따로 찾게 된다. |
| [A10](../../site-blog/advanced/10-analytics.html#checkpoint) | 보고서 120·20·6점과 날짜 변경 일치. 갱신 목록 기본값은 없음. check 통과. | 0.43 | 4/5 | 지표·수입 상태 구별은 좋다. 고칠 글을 목록에서 직접 고르는 경험은 약하다. |
| [A11](../../site-blog/advanced/11-operations.html#checkpoint) | 알림 live=false·예약 파일·ZIP 확인. DB와 mock 폴더를 밖으로 이동한 뒤 재생성. 10/29 설정이 백업의 10/28로 복원. check 통과. | 0.65 | 4/5 | 실제 이동·복구 지시가 좋다. 예약 파일 인수 설명은 생성물과 어긋난다. |
| [A12](../../site-blog/advanced/12-policy.html#checkpoint) | 여섯 미체크 항목 생성, auto 설정도 미체크 유지. 개인 사본에 보류 메모. check 통과. | 0.5 | 4/5 | 확인 목록 생성과 실제 승인을 잘 구별한다. 한 장의 정책·세금 분량은 길다. |
| [E2E](../../site-blog/advanced/e2e.html#checkpoint) | 여섯 passed=true 및 evidence 문장 일치. 설정 날짜를 바꿔도 고정 증거 유지. check 통과. | 1.77 | 5/5 | 기본/선택 경로와 거절·보류의 성공 기준이 분명하다. |

본문의 `data-expected`가 붙은 성공 출력 블록은 **30/30개**가 순차 실행의 동일 명령 출력과 정확히 일치했다. start/check·추가 성공 예시도 터미널 기록과 대조했다. 이 30개 대조는 오류 예시나 수동 행동까지 자동 검증한 수가 아니다. [대조 목록](phase-BX6-repro/expected-output-audit.json) 참조. A7의 0 입력 오류 차이는 아래 발견 F03에 남겼다.

## 코드 읽기·그림·낯선 말

코드 이해 판정은 **본문에 실린 발췌와 줄별 설명으로 기능을 한 문장으로 설명할 수 있는지**다. 원본 구현과 대조한 코드 정확성 판정은 아니다. 그림은 직접 렌더링한 스크린샷을 보고 평가했다.

| 장 | 내가 이해한 코드의 뜻 · 자체 판정 | 그림이 도운 점 |
|---|---|---|
| A0 | 설정에서 기본 사람 승인제와 하루 발행 상한을 정한다. **통과**. | 전체 순서와 다음 장 링크를 함께 보여 줘 돌아갈 곳을 찾기 쉽다. |
| A1 | Python 버전·필수 폴더·파일 쓰기·임시 포트를 검사한 뒤 고정 날짜를 출력한다. **통과**, 시드 뜻은 별도 설명 필요. | 키트→가상환경→진단→파일, output/private 폴더 그림이 파일 찾기에 도움 된다. |
| A2 | 설정의 이메일과 보유기간으로 문의/처리방침의 문장을 만든다. **통과**. | 세 연결 경로와 비밀번호 발급 위치가 mock에는 관리자 화면이 없다는 것을 알려 준다. |
| A3 | 날짜를 넣어 여섯 주제와 대상 월령의 목록을 돌려준다. **통과**. | 주제와 위험 등급을 나눠 놀이 제목만으로 승인을 생략하지 않게 한다. |
| A4 | 샘플을 복사하면서 날짜를 넣고 경험·작성자·사진을 비워 초안을 돌려준다. **통과**. | AI 허용 판단을 생성 앞에 두는 순서가 명료하다. DB 여는 법은 그림에도 없다. |
| A5 | 위험 표시·건강 내용·상업 관계·경험·사진·갱신 중 하나라도 해당하면 사람 승인이 필요하다. **부분**: 목적은 이해하나 긴 return의 각 조건을 독립적으로 설명하기 어렵다. | 단순 상자 그림보다 네 샘플의 7단계 판정 도구가 pass/review/block 차이를 확실하게 보여 준다. |
| A6 | 준비 때 저장한 원고·분류·미디어와 서버 결과를 다시 비교해 달라지면 멈춘다. **통과**, 보조함수 내부는 발췌 밖. | 요청마다 받은 ID를 다음 요청에 잇는 흐름이 중복 생성 방지 이해에 도움 된다. 기본 출력은 그림의 draft가 아니라 기존 future다. |
| A7 | 설정한 소제목 뒤에 광고 자리표시를 넣고 판매자 정보와 가상 지표 파일을 만든다. **통과**. | 좋은/나쁜 광고 배치 비교가 오클릭과 가림을 글보다 빨리 설명한다. |
| A8 | 원고의 관계 정보에서 표시 문구를 골라 앞에 붙이고 등록된 링크에 sponsored를 넣는다. **통과**. | 모바일에서 링크 옆만/첫머리를 바꾸면 부족한 표시가 무엇인지 바로 보인다. |
| A9 | 허용한 다음 상태와 필수 기록·승인 해시를 확인한 뒤 상태와 이력을 저장한다. **통과**, 중첩 이력 접근은 재독했다. | 도담 정산·포근담요 거절·자료 부족 보류를 직접 옮기는 도구가 긴 영어 상태표를 풀어 준다. |
| A10 | GA4에 기간·날짜/페이지·네 지표·남은 할당량을 요청하고 상태와 시간대를 꺼낸다. **통과**. | 지표와 보고서 네 구역은 유용하다. 갱신 대상은 실제 생성 보고서에서는 없음이라 그림의 행동을 바로 체험하지 못했다. |
| A11 | 백업을 임시 공간에 준비한 뒤 mock 파일·설정·상태 DB를 교체한다. **통과**, 검증/되돌리기 세부는 보조함수 밖이라 줄별 설명에 의존. | 하루/한 주 구분은 실행과 사람 검토를 분리해 준다. 파일 이동 전후 폴더 그림이 있으면 더 쉽겠다. |
| A12 | 여섯 확인 항목에 빈 확인자·근거·보류 칸을 써서 점검표를 만든다. **통과**. | 확인 안 된 항목은 보류로 돌아가는 흐름이 미체크 파일의 의미를 설명한다. |
| E2E | 시나리오마다 새 폴더에 샘플을 복사해 검사 함수를 실행하고 증거를 JSON으로 저장한다. **통과**: 함수가 예외 없이 끝난 뒤 passed=true를 쓰는 흐름으로 읽었다. | 세 경로 그림과 진행표가 mock 완주를 실계정 성과로 읽는 혼동을 줄인다. |

| 장 | 헷갈린 원문 / 설명 없이 먼저 나온 말 |
|---|---|
| A0 | “LLM은 호출당 입력·출력 토큰과 각 단가를 계산하고” — LLM·토큰이 정의보다 먼저 나온다. 토큰 설명은 A4에 있다. |
| A1 | “고정 시계 2026-10-27 · 시드 37” — 시드의 뜻이 없다. HTTP·REST·포트·바이트도 초반 밀도가 높다. REST는 A2에서 뒤늦게 풀어 준다. |
| A2 | “WAF 제한은요?” — WAF, SSH·FTP, Authorization 헤더를 호스팅 문의 전에 이해하기 어렵다. OAuth와 REST 정의는 있다. |
| A3 | “url·official·country·checked_on·age_range·license·claims를 나눠요.” — JSON 키의 한국어 뜻 일부를 샘플에서 추측했다. 스키마·JSON·CSV의 정의는 있다. |
| A4 | “costs의 mock 비용 0 기록을 확인하세요.” — DB를 어떻게 열지 모른다. micro_usd의 단위·settled의 뜻도 바로 풀어 주지 않는다. |
| A5 | “return bool(flagged or is_health(doc) or …)” — 긴 조건을 따라가다 놓쳤다. pass/review/block·EXIF·human_resolvable 설명은 도움이 됐다. |
| A6 | “공개 완료로 표시하지 마세요.” — 바로 앞 명령으로 mock publish를 확인했는데 어디에 무엇을 표시하지 말라는지 모호하다. slug·UTC·GET/POST 뜻도 즉시 설명되지 않는다. |
| A7 | “0으로 바꾸면 광고 위치는 1 이상이어야 합니다라는 오류가 나요.” — 실제는 설정 행/필드명을 포함한 다른 문구다. TFAT·TFCD·TFUA의 차이도 이름만으로 알기 어렵다. |
| A8 | “등록부는 쿠팡인데 첫 문구는 광고 관계” / “모의 예제는 정상이에요.” — 기본 원고는 쿠팡 지정 문구라는 앞 설명과 맞춰 읽기 어렵다. CSV·딥링크·sponsored 설명은 충분하다. |
| A9 | “대장에 declined, 사유 영아 수면 안전 충돌, 회신 기록을 남겨요.” — demo의 CSV에는 상태 세 칼럼만 보여 내 사유·기한·중간 이력을 어디에 적는지 찾게 된다. 미디어킷·전이의 정의는 있다. |
| A10 | “기준일 지난 금액·날짜 글” — 보고서는 없음이다. scope는 한국어 풀이가 없다. 서비스 계정·세션·transport 설명은 도움이 된다. |
| A11 | “생성 파일의 run --sample은 가상 승인 시연을 포함해요.” — 실제 생성 파일은 이미 report다. SQL 덤프·crontab·LaunchAgents·artifact 같은 말은 설명이 짧거나 없다(일부는 선택 과제). |
| A12 | 큰 실행 혼동은 없었다. YMYL·E-E-A-T·EXIF는 같은 자리에서 풀어 준다. 다만 소득세·부가세·휴직급여를 한 번에 읽는 분량이 길어 재독했다. |
| E2E | 큰 실행 혼동은 없었다. “생성 응답 유실 후 슬러그 조회 복구”의 슬러그는 앞 장에서 뜻을 못 배웠다. passed/evidence는 결과 파일과 직접 대조할 수 있다. |

그림 증거: [A0~A3](phase-BX6-repro/figures-0.png) · [A4~A7](phase-BX6-repro/figures-4.png) · [A8~A11](phase-BX6-repro/figures-8.png) · [A12·E2E](phase-BX6-repro/figures-12.png). 각 원본은 같은 폴더의 `장-이름-overview-1280.png`다. 일부 긴 요소 캡처에는 고정 메뉴가 중간에 들어가므로 실제 뷰포트도 별도 촬영했다.

## 중간 장에서 시작

각 행은 **빈 새 폴더 → 키트 폴더만 복사 → 별도 새 가상환경 → 해당 start**로 시작했다. 해당 장의 본 실습·바꿔 보기·복원·check를 수행했고, 남은 장도 E2E까지 이어서 수행했다. 앞 장의 실행 파일을 다른 실습 폴더에서 가져오지 않았다. `start`가 제공한 앞 장 스냅샷은 학습자가 직접 실습했다는 기록으로 세지 않았다.

| 새 시작 | 실제 통과한 장 | 새 시작 장의 관찰 | 명령 수 / 누적 실행 초 | 증거 |
|---|---|---|---|---|
| A5 | A5~A12·E2E | info pass/play review, risk_flags 삭제 후에도 review. A5 check 통과. | 106 / 11.526 | [mid-A5.txt](phase-BX6-repro/mid-A5.txt) |
| A9 | A9~A12·E2E | 도담 id=2, 동일 승인 해시, 정산 settled. 자동 모드에서도 승인 없는 발행 거부. | 59 / 8.514 | [mid-A9.txt](phase-BX6-repro/mid-A9.txt) |
| A11 | A11~A12·E2E | DB·mock 폴더를 키트 밖으로 이동하고 복원. 설정 날짜 복원과 A11 check 통과. | 28 / 5.903 | [mid-A11.txt](phase-BX6-repro/mid-A11.txt) |

A5부터의 재현에는 A6 수정 뒤 재승인 거부·A7 위치 0 오류·A9 승인 누락이라는 본문상 의도한 종료 코드 1이 있었다. A9부터는 승인 누락 1회, A11부터는 비정상 종료가 없었다. 이 예상 거부를 재현 실패로 세지 않았다.

## 일부러 실수한 결과

각 오류 실험도 다른 새 폴더와 새 가상환경에서 했다.

| 종류 | 내가 한 실수와 실제 오류 | 본문으로 한 복구 | 판정·증거 |
|---|---|---|---|
| 다른 폴더 | 키트 부모 폴더에서 `python course.py doctor`. `python: can't open file '…/course.py': [Errno 2] No such file or directory`, exit 2. | A1의 폴더 이동 안내로 blog.py/course.py 보이는 자리로 이동 → pwd/ls → start A1 → doctor. | 복구됨. **A1 오류 표 자체에는 이 오류가 없다.** A1 앞 설명으로는 해결 가능하고 동일 문구의 표는 A12에 있다. [기록](phase-BX6-repro/mistake-folder.txt). |
| 장 건너뛰기 | A1의 진단·연결까지만 한 뒤 A2~A7과 A8 start를 건너뛰고 affiliate 생성. `✖ 막힘: 초안 없음 → python blog.py draft --sample affiliate`, exit 1. | A8 흔한 오류의 해당 행대로 start A8 → affiliate → gate → check A8. | 표만으로 복구, check 통과. [기록](phase-BX6-repro/mistake-skip-chapter.txt). 올바르게 start A8부터 시작하는 중간 진입은 오류가 아니라 정상임도 구별했다. |
| 설정 오타 | A10 today를 `2026/10/28`로 저장. `✖ 막힘: 설정 3줄 today: 날짜 형식 오류 → today="2026-10-27"로 고치세요`, exit 1. | A10 흔한 오류 표대로 YYYY-MM-DD, 오류가 제시한 기본 날짜로 수정 → report → check A10. | 오류 문구/행동이 일치하고 check 통과. [기록](phase-BX6-repro/mistake-config.txt). |

추가로 A9에서 공개 재조회 단계를 건너뛰고 정산했다. `공개 상태 확인 전 → status --sample sponsor --advance-days 2를 실행하세요`로 거부됐고 A9 표의 두 명령을 실행해 check A9까지 복구했다. [추가 기록](phase-BX6-repro/mistake-skip.txt).

## 발견 목록

차단 = 본문만으로 요구 행동을 끝낼 수 없음. 혼란 = 경로는 진행되나 뜻·다음 행동을 추측/재독함. 사소 = 진행을 막지 않는 예시/표현 불일치. 아래 제안은 문서 검토 의견이며 이번 작업에서 적용하지 않았다.

| ID·분류 | 장·위치 | 원문 | 실제 관찰·영향 | 제안 |
|---|---|---|---|---|
| F01 **차단** | A4 #experience·#checkpoint | “costs의 mock 비용 0 기록을 확인하세요.” | state.sqlite3가 비용 기록이라는 것만 안다. 열 프로그램·조회법·성공 예시가 없어 **비용 직접 확인은 중단**. check A4는 통과. [터미널 기록](phase-BX6-repro/sequential.txt). | 키 노출 없이 costs만 읽는 복사 가능한 명령과 `micro_usd=0 / settled` 출력 예를 본문에 추가한다. 추측한 해결은 SQLite 읽기 도구/명령이지만 실행하지 않았다. |
| F02 **혼란** | A6 #checkpoint | “post_id=1의 draft → 승인 → future와 status.json의 예약 정보를 확인하세요. 공개 완료로 표시하지 마세요.” | 체크포인트 명령에는 advance-days 2가 있고 실제 마지막 파일은 id=1 publish다. 준비 시작도 draft가 아니라 기존 future다. 앞 본문은 이를 설명하는데 마지막 문장이 되돌린다. | “기본 시작은 기존 future 재사용 → 최종 승인 → 예약 유지 → mock publish 확인. 실제 블로그 공개 성공으로 표시하지 않아요.”처럼 경로를 명시한다. |
| F03 사소 | A7 #change | “0으로 바꾸면 광고 위치는 1 이상이어야 합니다라는 오류가 나요.” | 실제는 `설정 24줄 ad_after_h2: 양의 정수가 필요함 → ad_after_h2=2로 고치세요`. 오류 자체가 복구를 안내해 진행은 된다. | 키트가 출력한 설정 검증 문구로 예시를 교체한다. |
| F04 **혼란** | A11 #schedule | “run·--sample 인수 대신 report 하나를 써요.” / “생성 파일의 run --sample은 가상 승인 시연을 포함해요.” | 생성한 cron.txt·launchd.plist·windows.txt는 모두 이미 report다. 바꿀 인수를 찾지 못한다. 선택 과제이므로 OS 등록은 하지 않았다. | 현재 생성물은 report라고 설명하고 run --sample 주의는 직접 실행하는 별도 예에만 붙인다. |
| F05 **혼란** | A1 #errors | 표의 폴더 오류는 “core 폴더 없음 → 키트를 빈 폴더에 다시 복사하세요” | 다른 폴더에서 치면 core 검사 전에 Python의 can't open file이 난다. A1 앞 폴더 안내를 다시 읽어 해결했지만 해당 오류 표로 바로 찾지는 못했다. | A12의 can't open file 행을 A1에도 두고 cd·pwd·ls 예를 연결한다. |
| F06 **혼란** | A9 #review·#media-kit | “대장에 declined, 사유 영아 수면 안전 충돌, 회신 기록을 남겨요.” | demo 뒤 ledger.csv에는 id/content_id/state만 보인다. 내 사유·기한·수정 요청·중간 이력을 적는 사용 위치가 불분명하다. mock 정산은 재현된다. | 이번 CLI는 가상 거래 자동 시연이라고 바로 명시하고, 실제 거래용 개인 메모의 칸과 한 행 예를 본문에 준다. 기능 확장 요청이 아니다. |
| F07 **혼란** | A0 #cost, A1 #steps/#read, A2 #server | “LLM”, “시드 37”, “WAF 제한은요?” | 파이썬 기초로 뜻을 알기 어렵고 정의가 뒤에 나오거나 없다. A7 TFAT/TFCD/TFUA, A10 scope, A11 선택 과제 용어도 같은 문제다. | 처음 나온 자리에서 한 문장 풀이를 주고 실습 필수 용어와 선택 연결 용어를 구분한다. 장별 목록은 위 표 참조. |
| F08 **혼란** | A5 #read | `return bool(flagged or is_health(doc) or …)` | 사람 승인을 강제한다는 목적은 알지만 매우 긴 한 줄과 영어 키를 차례로 읽기 어렵다. 줄별 설명도 해당 조건을 한꺼번에 묶는다. | 본문 발췌를 조건별 줄바꿈하고 대표 조건 두 개의 뜻을 구체 예로 푼다. 키트 리팩터링은 필요하지 않다. |
| F09 사소 | A8 #errors | “등록부는 쿠팡인데 첫 문구는 광고 관계” / “모의 예제는 정상이에요.” | 실제 기본 HTML과 앞 설명은 쿠팡 지정 문구로 일치한다. 불일치를 정상으로 읽게 하는 오류 표가 혼동을 남긴다. | 기본 정상 예는 지정 문구라고 맞추고 실제 불일치면 관계 정보와 등록부를 대조하게 한다. |
| F10 사소 | A10 #steps | “갱신할 글과 다음 글감 하나를 골라요.” / 그림의 “기준일 지난 금액·날짜 글” | 기본 보고서의 갱신 목록은 없음. 본문은 목록 밖도 검토하라 하므로 진행 가능하지만 목록에서 고르는 체험은 없다. [보고서 화면](phase-BX6-repro/artifact-analytics-weekly.png). | 없음일 때 본문의 부모급여 글을 직접 확인하는 예를 바로 붙이거나, 기한 지난 고정 샘플을 별도 예로 보여 준다. |

## 78개 학습자 질문의 직답 판정

관련 절/FAQ의 시작 근처에서 질문에 결론을 주고 예·수치 또는 구체 확인 방법과 행동으로 이어지는지를 봤다. 한 장의 맨 첫 문장에 6문항 모두 답해야 한다는 뜻은 아니다. 복합 질문의 답 일부가 멀리 흩어지거나 “확인하세요”만 남으면 부분이다. 각 인용은 해당 HTML 절 안에 실제 존재하는지 대조했다. **정책 사실의 법적 정확성을 이 점수로 보증하지 않는다.**

| 질문 | 판정 | 위치·직답 원문 | 판정 이유 |
|---|---|---|---|
| **A0-Q1** 아기 낮잠 시간에만 작업할 수 있는데 어디까지 코드가 하고 무엇을 제가 확인하나요? | 통과 | [00-start.html#answer](../../site-blog/advanced/00-start.html#answer) · “코드는 자료 정리·초안·검사·발행 요청을 맡고, 사람은 경험·사진·건강·계약과 최종 승인을 맡아요.” | 역할과 낮잠 시간의 작은 끝점을 바로 제시한다. |
| **A0-Q2** 건강 글과 그림책 목록을 같은 방식으로 자동 발행해도 되나요? | 통과 | [00-start.html#automation](../../site-blog/advanced/00-start.html#automation) · “건강 글과 그림책 목록은 같은 방식으로 자동 발행하지 않아요.” | 유형별 표에서 승인 수준을 고를 수 있다. |
| **A0-Q3** 로컬 실습만 끝내도 광고·제휴·협찬 흐름을 배울 수 있나요? | 통과 | [00-start.html#answer](../../site-blog/advanced/00-start.html#answer) · “로컬 실습으로 광고·제휴·협찬 흐름을 배우고 실제 연결은 준비 뒤에 해요.” | 서버 구매 질문에 곧바로 아니요라고 답한다. |
| **A0-Q4** 한 달 호스팅·도메인·AI 비용은 각각 얼마이고 무료로 어디까지 되나요? | 통과 | [00-start.html#cost](../../site-blog/advanced/00-start.html#cost) · “mock는 외부 서비스 추가요금 0으로 완주할 수 있어요.” | 가격 예·갱신비·월 계산식과 견적 확인 행동을 잇는다. |
| **A0-Q5** 글이 몇 편 있어야 광고를 신청하고 제휴·협찬은 언제 붙이나요? | 통과 | [00-start.html#income](../../site-blog/advanced/00-start.html#income) · “광고 신청에 공통으로 정해진 최소 글 수·방문자 기준은 없어요.” | 학습 순서와 프로그램별 독립 준비를 바로 구별한다. |
| **A0-Q6** 조회수가 아직 적어도 수익 계산기를 써 볼 수 있고 무엇을 직접 입력하나요? | 통과 | [00-start.html#income](../../site-blog/advanced/00-start.html#income) · “조회수가 적어도 계산할 수 있고, 모르는 값은 빈칸으로 남겨도 돼요.” | 직접 채울 여섯 입력과 빈칸/0의 차이를 바로 보여 준다. |
| **A1-Q1** 파이썬 기초만 아는데 가상환경은 왜 만들고 어느 폴더에서 명령을 치나요? | 통과 | [01-environment.html#start](../../site-blog/advanced/01-environment.html#start) · “명령은 blog.py와 course.py가 보이는 키트 폴더에서 입력해요.” | 가상환경의 뜻·OS별 준비·전체 폴더 이동을 제시한다. |
| **A1-Q2** 책과 내 컴퓨터 결과가 다를 때 파이썬 버전·실행 폴더·설정 중 무엇부터 보나요? | 통과 | [01-environment.html#steps](../../site-blog/advanced/01-environment.html#steps) · “먼저 Python 버전 → 현재 폴더 → 기본 설정 순서로 보세요.” | 진단 순서가 첫 문장이고 doctor를 실행할 수 있다. |
| **A1-Q3** Windows PowerShell에서 책 명령이 안 되면 macOS 명령과 무엇이 다른가요? | 통과 | [01-environment.html#start](../../site-blog/advanced/01-environment.html#start) · “PowerShell에서 활성화가 차단되면 이후 명령의 python을” | OS 탭과 Python 직접 실행 대안이 있다. |
| **A1-Q4** Docker가 설치되지 않아도 mock 서버로 모든 장을 끝낼 수 있나요? | 통과 | [01-environment.html#change](../../site-blog/advanced/01-environment.html#change) · “Docker 없이도 mock으로 모든 장을 마칠 수 있어요.” | 선택 상자 첫 문장이 답이고 현재 경로를 유지할 수 있다. |
| **A1-Q5** 포트가 이미 사용 중이거나 서버에 연결되지 않는다고 나오면 어떻게 하나요? | 부분 | [01-environment.html#errors](../../site-blog/advanced/01-environment.html#errors) · “서버 연결 오류가 나면 먼저 python course.py doctor를 실행해요.” | 연결/권한 진단은 있으나 사용 중인 고정 포트와 임시 포트의 차이·포트 충돌의 다음 행동은 없다. |
| **A1-Q6** 실습을 꼬이게 했는데 제 실제 글을 지우지 않고 그 장부터 다시 시작하나요? | 통과 | [01-environment.html#answer](../../site-blog/advanced/01-environment.html#answer) · “별도 연습 폴더를 쓰세요.” | 이 문구는 대화에 있음. 복원 대상·보관·실운영 금지와 start 예가 본문에 있다. |
| **A2-Q1** 이미 네이버 블로그가 있는데 왜 코드 실습은 설치형 WordPress로 하나요? | 통과 | [02-wordpress.html#server](../../site-blog/advanced/02-wordpress.html#server) · “설치형 WordPress는 글·사진·분류를 REST API로 다룰 수 있어” | 기존 블로그는 유지하고 별도 실습하는 이유를 바로 답한다. |
| **A2-Q2** WordPress.com 유료 요금제와 설치형 호스팅은 API·플러그인·광고에서 어떻게 다른가요? | 부분 | [02-wordpress.html#server](../../site-blog/advanced/02-wordpress.html#server) · “WordPress.com은 요금제별 플러그인·광고 허용과 서비스 전용 인증을 확인하고,” | 인증 경로는 대비되지만 플러그인·광고의 실제 차이는 지원팀 질문으로 남는다. 첫머리에 기능 비교 결론이 부족하다. |
| **A2-Q3** 월 요금이 싼 호스팅을 고를 때 HTTPS·백업·복구·도메인 갱신비는 어디서 보나요? | 통과 | [02-wordpress.html#server](../../site-blog/advanced/02-wordpress.html#server) · “싼 호스팅은 가격보다 필요한 기능부터 진단하세요.” | 바로 아래 표의 업체 질문으로 HTTPS·복구·갱신 총액을 확인한다. |
| **A2-Q4** 애플리케이션 비밀번호 메뉴가 없거나 401·403이면 누구에게 무엇을 물어보나요? | 통과 | [02-wordpress.html#password](../../site-blog/advanced/02-wordpress.html#password) · “앱 비밀번호는 사용자 프로필에서 만들고 본래 로그인 비밀번호와 구별해요.” | 메뉴 없을 때 진단 순서와 401/403별 호스팅 문의 정보가 있다. |
| **A2-Q5** 로컬 Docker WordPress는 어떤 버전과 이미지 태그로 맞추고 실제 서버로 어떻게 옮기나요? | 부분 | [02-wordpress.html#password](../../site-blog/advanced/02-wordpress.html#password) · “Docker는 키트의 로컬 설치 안내로 준비해요.” | 태그·DB/uploads 원칙은 있지만 실제 이전 조작은 본문 밖 설치 안내와 A11 선택 과제에 나뉘어 있다. |
| **A2-Q6** 소개·문의·광고 정책·개인정보처리방침에는 무엇을 쓰고 문의자의 정보는 얼마나 받나요? | 통과 | [02-wordpress.html#pages](../../site-blog/advanced/02-wordpress.html#pages) · “페이지 묶음은 내 컴퓨터의 HTML 파일로 만들어져요.” | 네 파일별 의무/권장·연락처·이메일과 문의 내용만 수집하는 범위를 표로 제시한다. |
| **A3-Q1** 제가 키워 본 월령 밖의 글은 쓰면 안 되고 경험과 자료 정리는 어떻게 나누나요? | 통과 | [03-topics.html#answer](../../site-blog/advanced/03-topics.html#answer) · “내 경험 밖의 월령도 공식 자료를 정리할 수 있어요.” | 자료와 경험 칸 분리라는 행동을 다음 문장에 준다. |
| **A3-Q2** 부모급여·아동수당 글의 금액이 바뀌면 어느 공식 자료로 고치나요? | 통과 | [03-topics.html#schema](../../site-blog/advanced/03-topics.html#schema) · “부모급여·아동수당 금액이 바뀌면 관할 기관의 원문으로 갱신해요.” | 기관·시행일·지역·메모 갱신이 이어진다. |
| **A3-Q3** 어린이집·육아지원센터·예방접종 일정은 무료 API나 파일로 받을 수 있나요? | 통과 | [03-topics.html#data](../../site-blog/advanced/03-topics.html#data) · “어린이집 기관 정보와 복지서비스는 무료 공개 API로 찾을 수 있어요.” | CSV·주소록·API와 공개 접종 일정 파일의 역할을 구별한다. |
| **A3-Q4** 공공누리 자료는 출처만 쓰면 상업 블로그에 사진까지 옮겨도 되나요? | 통과 | [03-topics.html#data](../../site-blog/advanced/03-topics.html#data) · “공공누리는 유형마다 상업 이용과 변경 허용이 달라요.” | 사진까지 복사하면 안 되는 이유와 유형별 표·기록 행동이 있다. |
| **A3-Q5** 터미타임 같은 놀이 글도 건강·안전 글로 보고 매번 승인해야 하나요? | 통과 | [03-topics.html#topics](../../site-blog/advanced/03-topics.html#topics) · “터미타임 글은 놀이로 분류해도 건강·안전 글로 검토해요.” | 바로 다음에 play는 항상 사람 승인이라고 답한다. |
| **A3-Q6** 같은 주제를 월령만 바꿔 여러 편 만들면 중복이나 검색 스팸이 되나요? | 통과 | [03-topics.html#change](../../site-blog/advanced/03-topics.html#change) · “월령만 바꾼 비슷한 글을 늘리는 방법은 피하세요.” | 추가 가치가 없으면 기존 글 수정이라는 행동까지 제시한다. |
| **A4-Q1** ChatGPT 구독이 있는데 API 비용도 포함되고 무료 키가 꼭 필요한가요? | 통과 | [04-drafts.html#answer](../../site-blog/advanced/04-drafts.html#answer) · “유료 API 키 없이 mock 초안을 만들 수 있어요.” | 구독과 API 비용은 별도라고 바로 답한다. |
| **A4-Q2** JSON 초안은 일반 답변과 무엇이 다르고 구조화 출력의 정확한 기능 이름은 뭔가요? | 통과 | [04-drafts.html#draft](../../site-blog/advanced/04-drafts.html#draft) · “일반 답변과 JSON 초안의 차이는 검사할 칸이 정해져 있다는 점이에요.” | Structured Outputs와 text.format 예를 이어 준다. |
| **A4-Q3** AI가 제가 써 봤다거나 아기가 좋아했다는 경험을 지어내지 않게 하려면요? | 통과 | [04-drafts.html#experience](../../site-blog/advanced/04-drafts.html#experience) · ““직접 써 봤다”는 문장은 사람이 겪은 내용을 직접 넣어야 해요.” | 날짜·조건·좋고 나쁜 점, human 표시와 빈칸 행동이 있다. |
| **A4-Q4** 입력·출력 토큰으로 한 편과 한 달 비용은 어떻게 계산하나요? | 통과 | [04-drafts.html#experience](../../site-blog/advanced/04-drafts.html#experience) · “한 편의 토큰 비용은 입력 비용과 출력 비용을 더해요.” | 토큰 정의·편당 식·30회 계산 예가 있다. |
| **A4-Q5** 모델 이름이 책과 다르거나 종료됐다고 하면 어디서 현재 모델을 확인하나요? | 통과 | [04-drafts.html#experience](../../site-blog/advanced/04-drafts.html#experience) · “모델 이름이 없거나 종료 오류가 나면 공급자의 모델 목록·지원 종료 안내에서 현재 ID와 종료일을 확인하세요.” | 확인 위치와 가격/구조화 출력 대조를 준다. |
| **A4-Q6** 지출 한도와 알림을 어디서 설정하고 재시도까지 합쳐 과금을 막을 수 있나요? | 부분 | [04-drafts.html#experience](../../site-blog/advanced/04-drafts.html#experience) · “지출 알림과 강제 한도를 함께 확인하세요.” | 어디서 설정하는지인 메뉴 위치는 뒤 확인할 점에 떨어져 있고 비용 예약 기록을 읽는 절차도 없다. |
| **A5-Q1** 관문 통과라고 뜨면 발열·수면 글도 바로 공개해도 되나요? | 통과 | [05-gates.html#answer](../../site-blog/advanced/05-gates.html#answer) · “관문 통과는 자동 검사 결과예요.” | 건강 글 등은 최종 사람 승인 후 발행한다고 바로 답한다. |
| **A5-Q2** 아기 얼굴을 가렸는데 이름·생일·어린이집·사진 위치정보도 검사하나요? | 통과 | [05-gates.html#review](../../site-blog/advanced/05-gates.html#review) · “얼굴을 가렸어도 실명·정확한 생일·어린이집·병원·생활 위치와 사진 메타데이터를 확인해요.” | EXIF 뜻과 제거 뒤 재확인, 배경은 사람 확인이라고 구별한다. |
| **A5-Q3** 약 이름·용량·집에서 지켜보라는 문장을 발견하면 코드는 어떤 상태로 멈추나요? | 통과 | [05-gates.html#review](../../site-blog/advanced/05-gates.html#review) · “약 이름·용량이나 “집에서 지켜봐도 된다”는 판정이 있으면 차단해요.” | 문장 제거와 근거/월령 재검사를 바로 지시한다. |
| **A5-Q4** 협찬 표시가 글 맨 끝이나 더보기 안에 있으면 왜 막나요? | 통과 | [05-gates.html#review](../../site-blog/advanced/05-gates.html#review) · “협찬 표시를 글 끝이나 더보기 안에만 두면 첫부분에서 관계를 알아볼 수 없어 막혀요.” | 첫 문장에 이유, 이어서 올바른 위치를 준다. |
| **A5-Q5** KC 번호나 광고 심의 자료가 없는 제품 글은 보류인가요 거절인가요? | 통과 | [05-gates.html#decision](../../site-blog/advanced/05-gates.html#decision) · “법적 금지, 프로젝트 거절, 자료 보류는 해결 방법이 달라요.” | 품목별 예와 자료 요청/재검사로 단일 KC 판정을 피하게 한다. |
| **A5-Q6** 중복 글이나 근거 없는 효능 표현을 걸러도 제가 추가로 확인할 것은 뭔가요? | 통과 | [05-gates.html#review](../../site-blog/advanced/05-gates.html#review) · “중복·효능 표현 검사를 통과해도 원문 사실과 사진 맥락은 사람이 확인해요.” | 유사문서·숫자·허가 밖 효능·경험을 다시 읽게 한다. |
| **A6-Q1** 파이썬에서 WordPress 초안·글·이미지·카테고리·태그를 어떤 순서로 올리나요? | 통과 | [06-publish.html#answer](../../site-blog/advanced/06-publish.html#answer) · “분류·이미지 ID 준비 → 서버 초안 → 최종본 승인 → 예약 → 서버 상태 재조회 순서예요.” | 순서와 요청 ID 그림이 일치한다. |
| **A6-Q2** 초안은 성공했는데 이미지 업로드는 실패하면 글을 다시 만들어야 하나요? | 통과 | [06-publish.html#prepare](../../site-blog/advanced/06-publish.html#prepare) · “이미지 업로드에 실패해도 이미 만든 글을 새로 생성하지 마세요.” | 기존 글 번호를 보존하고 목록/기록부터 조회하게 한다. |
| **A6-Q3** 예약 status=future와 한국 시간은 어떻게 맞추고 정각에 꼭 올라가나요? | 통과 | [06-publish.html#schedule](../../site-blog/advanced/06-publish.html#schedule) · “실제 예약은 정각 공개를 보장하지 않아요.” | 한국 시간대·date/date_gmt·WP-Cron·publish 재조회를 제시한다. |
| **A6-Q4** 요청이 시간 초과돼 다시 누르면 글이 두 번 올라가지 않게 어떻게 하나요? | 통과 | [06-publish.html#answer](../../site-blog/advanced/06-publish.html#answer) · “시간 초과 때는 새 글을 만들기 전에 기존 결과부터 조회해요.” | 오류 표가 post_id/slug로 조회하고 POST 반복 금지를 잇는다. |
| **A6-Q5** 승인 뒤 문구나 사진을 고쳤으면 이전 승인으로 예약 발행해도 되나요? | 통과 | [06-publish.html#approve](../../site-blog/advanced/06-publish.html#approve) · “사람 승인은 지금 준비한 최종본에만 유효해요.” | 변경 실습에서 거부를 확인하고 prepare→재승인을 실행한다. |
| **A6-Q6** Blogger는 API 키만 있으면 쓰나요 OAuth·쿼터·애드센스 연결은 어떻게 다른가요? | 부분 | [06-publish.html#errors](../../site-blog/advanced/06-publish.html#errors) · “Blogger 글쓰기는 API 키만으로 되지 않아요.” | OAuth·초안/예약·광고 연결은 구별하나 쿼터 확인은 끝 확인할 점으로 넘기며 구체 확인 항목/단위가 없다. |
| **A7-Q1** 애드센스는 글 수·방문자·블로그 나이·도메인에 공식 최소 조건이 있나요? | 통과 | [07-ads.html#answer](../../site-blog/advanced/07-ads.html#answer) · “애드센스는 글 개수를 채워 받는 광고가 아니에요.” | 글 수/방문자/운영일 공통 숫자가 없고 HTML 관리권을 확인하게 한다. |
| **A7-Q2** 광고 승인 거절 사유가 가치가 낮은 콘텐츠라면 무엇부터 고치고 어디서 이유를 보나요? | 통과 | [07-ads.html#steps](../../site-blog/advanced/07-ads.html#steps) · “가치가 낮다는 거절을 받으면 기존 사이트의 거절 사유부터 읽어요.” | 메일·사이트/정책센터와 그림책 글을 고치는 예가 있다. |
| **A7-Q3** 개인정보처리방침 말고 소개·문의 페이지도 공식 필수 조건인가요? | 통과 | [07-ads.html#summary](../../site-blog/advanced/07-ads.html#summary) · “개인정보 고지 의무와 운영 권장 페이지를 구별해요.” | FAQ 바로 다음에 소개/문의는 권장이라고 답하고 A2 재검토를 지시한다. |
| **A7-Q4** 광고는 몇 개까지 어디에 붙이고 버튼 옆·화면을 덮는 위치는 왜 위험한가요? | 통과 | [07-ads.html#steps](../../site-blog/advanced/07-ads.html#steps) · “안전한 광고 개수 하나가 정해져 있지는 않아요.” | 오클릭·가림 금지와 위치 그림·설정 실습이 있다. |
| **A7-Q5** 부모가 읽는 육아 글과 아동 대상 글은 다르고 맞춤 광고·동의 배너는 어떻게 정하나요? | 통과 | [07-ads.html#steps](../../site-blog/advanced/07-ads.html#steps) · “부모가 읽는 육아 글이라는 이유만으로 아동 대상 사이트가 되지는 않아요.” | 이용자/정보 수집 판단·아동 처리·지역별 CMP를 따로 보게 한다. |
| **A7-Q6** ads.txt·민감한 광고 차단·수익 보고 API를 붙이고 애드핏 등 다른 광고도 쓸 수 있나요? | 통과 | [07-ads.html#summary](../../site-blog/advanced/07-ads.html#summary) · “각각 준비와 확인 경로가 있어요.” | FAQ와 본문에서 계정 행·차단 메뉴·OAuth·AdFit 문의를 각각 제시한다. |
| **A8-Q1** 쿠팡 파트너스 가입·최종 승인과 Open API 키 발급은 같은 조건인가요? | 통과 | [08-affiliate.html#answer](../../site-blog/advanced/08-affiliate.html#answer) · “가입, 최종 채널 심사, API 이용 자격을 따로 확인하세요.” | 이어지는 단계표에 15만 원은 최종 검토 시작 기준이라고 구별한다. |
| **A8-Q2** API 실적 요건·호출 한도를 못 채우면 검색·딥링크 대신 수동 링크로 연습하나요? | 통과 | [08-affiliate.html#answer](../../site-blog/advanced/08-affiliate.html#answer) · “API 키가 없어도 등록부·관계 표시·링크 검사를 끝낼 수 있어요.” | 수동 링크·가격 미표시·mock 명령을 그대로 실행할 수 있다. |
| **A8-Q3** 쿠팡 의무 대가성 문구는 정확히 무엇이고 제목·첫머리·사진 중 어디에 넣나요? | 통과 | [08-affiliate.html#steps](../../site-blog/advanced/08-affiliate.html#steps) · “블로그의 관계 표시는 제목 또는 첫 부분에서 쉽게 보여야 해요.” | 정확한 쿠팡 문구·사진 재사용·모바일 위치 실습을 준다. |
| **A8-Q4** 가격을 API에서 가져와 계속 표시하거나 AI로 상품 후기를 자동 생성해도 되나요? | 통과 | [08-affiliate.html#steps](../../site-blog/advanced/08-affiliate.html#steps) · “실제 가격은 기본 글에 표시하지 않아요.” | 가격 이용 조건 확인과 직접 사용하지 않은 AI 후기 금지를 바로 잇는다. |
| **A8-Q5** 분유·젖병·아기 화장품·체온계·영양제 링크는 일반 완구 링크와 뭐가 다른가요? | 통과 | [08-affiliate.html#steps](../../site-blog/advanced/08-affiliate.html#steps) · “KC 번호 하나로 모든 아기 제품을 검사하지 않아요.” | 품목별 법적 금지/프로젝트 거절/자료 보류와 다음 행동을 표로 준다. |
| **A8-Q6** 쇼핑커넥트·브랜드커넥트 링크를 제 설치형 블로그에도 쓸 수 있고 제한은 어디서 보나요? | 통과 | [08-affiliate.html#summary](../../site-blog/advanced/08-affiliate.html#summary) · “내 등록 매체와 캠페인의 외부 게시 허용부터 확인해요.” | WordPress 전체 허용으로 읽지 말고 약관과 지정 채널을 확인하게 한다. |
| **A9-Q1** 육아 블로그 협찬 제안이 왔을 때 제공품·원고료·작성 기한·반납 중 무엇을 먼저 묻나요? | 통과 | [09-sponsorship.html#review](../../site-blog/advanced/09-sponsorship.html#review) · “제공품·원고료·작성 기한·반납 조건을 한 번에 받아 적어요.” | 계약 질문 일곱 개와 서면 보관 행동이 있다. |
| **A9-Q2** 방문자가 많지 않은데 미디어킷에는 어떤 실제 지표와 글 예시를 넣나요? | 부분 | [09-sponsorship.html#media-kit](../../site-blog/advanced/09-sponsorship.html#media-kit) · “모의 미디어킷을 만든 뒤 실제 지표로 바꿀 칸을 확인해요.” | 지표/기간/대표글은 언급하지만 어떤 대표글을 고를지의 구체 예가 없고 첫 답도 모의 파일 안내다. |
| **A9-Q3** 지원→선정→배송→작성→수정 요청→발행→정산을 대장에 어떻게 기록하나요? | 부분 | [09-sponsorship.html#overview](../../site-blog/advanced/09-sponsorship.html#overview) · “각 상태는 증빙을 남겨야 넘어가요.” | 상태 그림과 demo 자동 기록은 있지만 내 문의의 중간 상태·수정 요청을 직접 대장에 기록하는 사용 절차는 없다. |
| **A9-Q4** 좋은 말만 쓰라거나 광고 표시를 빼 달라거나 아이 얼굴 사진을 달라면 거절하나요? | 통과 | [09-sponsorship.html#write](../../site-blog/advanced/09-sponsorship.html#write) · “광고주가 표시 삭제·거짓 후기·의학 효능 추가를 요구하면 진행하지 않아요.” | 아이 얼굴 강제·긍정 평가만 허용도 거절한다고 바로 잇는다. |
| **A9-Q5** 아기 낮잠 이불·베개 협찬은 안전 수면 원칙에 안 맞으면 왜 거절하고 대안은 뭔가요? | 통과 | [09-sponsorship.html#review](../../site-blog/advanced/09-sponsorship.html#review) · “영아가 자는 자리에 느슨한 이불을 두도록 홍보하는 제안은 거절해요.” | 안전 원칙·거절 회신·그림책 정리 대안이 이어진다. |
| **A9-Q6** 제품만 받고 돈을 안 받았어도 세금 기록이 필요하고 계약의 2차 사용권은 어떻게 정하나요? | 부분 | [09-sponsorship.html#report](../../site-blog/advanced/09-sponsorship.html#report) · “물건만 받아도 세금 검토용 기록을 남겨요.” | 현물 기록은 직답하지만 2차 사용권의 매체·기간·편집·비용 질문은 앞 계약 목록에 떨어져 있다. |
| **A10-Q1** GA4 방문자·조회수와 Search Console 클릭·노출은 왜 서로 다른가요? | 통과 | [10-analytics.html#answer](../../site-blog/advanced/10-analytics.html#answer) · “방문·검색·수익은 다른 숫자예요.” | 도구별 표와 가상 120/20 예로 같은 수로 맞추지 않게 한다. |
| **A10-Q2** GA4 Data API에서 무료 할당량과 정확한 지표 이름은 무엇인가요? | 통과 | [10-analytics.html#errors](../../site-blog/advanced/10-analytics.html#errors) · “표준 GA4 Core의 속성당 하루 한도는 200,000토큰이에요.” | FAQ가 정확한 네 지표와 잔여량 확인까지 바로 준다. |
| **A10-Q3** Search Console 데이터가 어제 날짜에 비어 있으면 실패인가요 지연인가요? | 통과 | [10-analytics.html#steps](../../site-blog/advanced/10-analytics.html#steps) · “어제 데이터가 비었다면 지연부터 확인하세요.” | 보통 2~3일·시간대·필터/날짜 조회 순서가 있다. |
| **A10-Q4** 서비스 계정과 OAuth 중 어느 것을 써야 하고 사이트 권한도 따로 줘야 하나요? | 통과 | [10-analytics.html#steps](../../site-blog/advanced/10-analytics.html#steps) · “먼저 화면에서 같은 기간의 보고서를 읽은 뒤 API 수집을 붙이세요.” | 선택 표가 소유 자료/타인 자료와 별도 사이트 권한, AdSense 사용자 OAuth를 구별한다. |
| **A10-Q5** 애드센스·제휴 예상 수입과 확정·입금액을 한 보고서에서 어떻게 구분하나요? | 통과 | [10-analytics.html#steps](../../site-blog/advanced/10-analytics.html#steps) · “예상액·확정액·입금액을 따로 적고 더하지 마세요.” | 같은 거래의 세 칸 예와 증빙 기록 행동을 준다. |
| **A10-Q6** WordPress 통계 플러그인만 써도 되고 어떤 글부터 고칠지 기준은 뭔가요? | 통과 | [10-analytics.html#errors](../../site-blog/advanced/10-analytics.html#errors) · “네. 이번 주 고칠 글을 고를 수 있으면 시작할 수 있어요.” | FAQ에서 오래된 제도 글의 출처·기준일 확인을 바로 지시한다. |
| **A11-Q1** 제 노트북이 꺼져 있어도 cron·작업 스케줄러·GitHub Actions가 돌아가나요? | 통과 | [11-operations.html#answer](../../site-blog/advanced/11-operations.html#answer) · “노트북이 꺼지면 그 안의 예약 작업도 멈춰요.” | 늘 켜진 실행 장소와 Actions 외부 상태 준비를 준다. |
| **A11-Q2** 매일 실행이 늦거나 실패하면 어디서 로그를 보고 알림을 받나요? | 통과 | [11-operations.html#steps](../../site-blog/advanced/11-operations.html#steps) · “실행 로그와 알림 기록을 함께 보세요.” | 로그 위치 표와 아직 연결하지 않은 실패/실전송의 경계를 명시한다. |
| **A11-Q3** 승인 알림을 못 보고 지나가도 건강·협찬 글이 자동 공개되나요? | 통과 | [11-operations.html#steps](../../site-blog/advanced/11-operations.html#steps) · “미응답이면 그대로 대기해요.” | 고위험 글 최종 사람 승인과 수정 뒤 재승인을 바로 잇는다. |
| **A11-Q4** 코드·사진·데이터베이스·비밀키는 무엇을 백업하고 복구 성공을 어떻게 확인하나요? | 통과 | [11-operations.html#steps](../../site-blog/advanced/11-operations.html#steps) · “ZIP이 있다는 것보다 되살릴 수 있다는 것이 중요해요.” | 자료별 백업 표·밖으로 이동·복원·check 행동이 있다. |
| **A11-Q5** API 비밀번호가 노출되면 어떤 순서로 폐기·재발급하고 로그에서 지우나요? | 통과 | [11-operations.html#steps](../../site-blog/advanced/11-operations.html#steps) · “실행 중단 → 노출 키 폐기 → 새 키 발급 → 로컬 설정 교체 → 읽기 검증 순서예요.” | 로그·백업·공개 기록 점검과 값 비공개까지 구체 순서로 준다. |
| **A11-Q6** 같은 작업이 겹치거나 한도에 걸리면 무한 재시도와 중복 과금을 어떻게 막나요? | 통과 | [11-operations.html#steps](../../site-blog/advanced/11-operations.html#steps) · “새로 만들기 요청을 반복하기 전에 기존 글 ID를 조회하세요.” | 공유 상태 잠금·상한·최대 3회 예·CLI 미제공 경계를 준다. |
| **A12-Q1** AI로 초안을 쓰는 것과 구글이 금지한 대량 생성·사이트 평판 악용은 어떻게 다른가요? | 통과 | [12-policy.html#search](../../site-blog/advanced/12-policy.html#search) · “AI로 초안을 쓸 수 있어요.” | 다음 문장과 사례표가 가치 없는 대량 생성/평판 악용을 구별한다. |
| **A12-Q2** 육아 정보는 모두 YMYL인가요 건강·지원금 글에는 어떤 근거와 작성자 정보를 두나요? | 통과 | [12-policy.html#search](../../site-blog/advanced/12-policy.html#search) · “모든 육아 글을 같은 의학 조언으로 보지는 않아요.” | YMYL/E-E-A-T 정의·근거/기준일/작성자 예가 바로 있다. |
| **A12-Q3** 아이 사진을 부모가 올릴 때 동의·초상권·EXIF·삭제 요청은 어떻게 다루나요? | 통과 | [12-policy.html#privacy](../../site-blog/advanced/12-policy.html#privacy) · “부모 동의를 모든 공개에 대한 허락으로 쓰지 마세요.” | 촬영/인터넷 허락 구별·기본 비공개·EXIF·삭제 처리까지 이어진다. |
| **A12-Q4** 공정위 최신 지침에서 제품 제공·원고료·제휴 수수료 표시는 어떻게 다르나요? | 통과 | [12-policy.html#disclosure](../../site-blog/advanced/12-policy.html#disclosure) · “물품·원고료·제휴 수수료는 실제 받은 관계대로 밝혀요.” | 관계별 표시 문장과 위치·모바일 확인 행동이 있다. |
| **A12-Q5** 협찬 물품·원고료·광고료는 사업소득인가요 기타소득인가요 언제 사업자등록·종합소득세를 확인하나요? | 통과 | [12-policy.html#tax](../../site-blog/advanced/12-policy.html#tax) · “협찬이라는 이름만으로 사업소득·기타소득을 결정하지 않아요.” | 반복성/고용·등록 20일·다음 해 5월·현물/비용 기록과 문의 행동이 있다. |
| **A12-Q6** 출시 전에 저작권·영유아 제품 규제·세금에서 미확인인 항목은 어떻게 보류하고 확인하나요? | 통과 | [12-policy.html#answer](../../site-blog/advanced/12-policy.html#answer) · “답이 없는 글이나 광고 연결을 보류하고, 해결된 항목만 다음 단계로 옮겨요.” | 단계 ⑤와 확인할 점이 자료·담당자·기한·문의처를 제시한다. |

판정 집계: [78행 구조화 원기록](phase-BX6-repro/question-review.json). 부분 8개는 A1-Q5, A2-Q2·Q5, A4-Q6, A6-Q6, A9-Q2·Q3·Q6이다.

## 브라우저와 증거 보관

- Chromium으로 14개 장을 1280px/360px에서 확인했다. 두 폭 모두 문서 전체 가로 넘침은 0이었다. 1280px 로드의 pageerror도 0이었다. 표·코드 내부의 의도한 가로 스크롤까지 없다는 뜻은 아니다. 375px·다크 모드·실물 Windows/macOS 실행은 이번 독립 재현 범위에 포함하지 않았다.
- A0 수입/비용 0 가정 버튼과 계획 파일 받기, A1 Linux 탭, A5 네 샘플의 7단계 검사, A8 링크 옆만→첫머리 복원, A9 도담 settled·포근담요 declined·자료 부족 on_hold를 직접 조작했다. A9 다음 상태 버튼은 필요한 기록 체크를 해야 켜졌다.
- E2E의 mock 8칸만 체크하고 선택 경로 16칸은 비웠다. 여섯 시나리오 메모를 쓰고 새로고침 뒤 유지됨을 확인했다. 비용 DB 확인의 미완료는 별도 메모에 남겼다. 체크는 자가 기록이고 자동 성공 증거가 아니라는 본문 설명에 동의한다.
- `artifact-*` 화면은 별도 새 가상환경의 `artifact-recheck` 세션에서 본문 명령으로 다시 생성한 직후 브라우저로 연 스크린샷이다. 초기 촬영은 E2E start가 복원한 파일이었으므로 최종 증거는 직접 생성한 화면으로 교체했다. 최초 순차 실습의 값·편집·상태 변화는 `sequential.txt/jsonl`, 브라우저 재확인은 `artifact-recheck.txt`와 `artifact-observations.json`에 남겼다.

| 증거 | 내용 |
|---|---|
| [artifact-recheck.txt](phase-BX6-repro/artifact-recheck.txt), [artifact-observations.json](phase-BX6-repro/artifact-observations.json) | 본문 명령으로 다시 생성한 12개 파일의 브라우저 열람 |
| [browser-observations.json](phase-BX6-repro/browser-observations.json), [browser-interactions.json](phase-BX6-repro/browser-interactions.json) | 페이지·넘침·오류·도구 조작 결과 |
| [A0-plan.txt](phase-BX6-repro/A0-plan.txt), [A0-downloaded-plan.txt](phase-BX6-repro/A0-downloaded-plan.txt) | 직접 채운 네 칸과 브라우저 다운로드 결과 |
| [A12-personal-checklist.txt](phase-BX6-repro/A12-personal-checklist.txt) | 원본 밖 복사본에 실제 자료 미확보 보류 기록 |
| [E2E-learner-notes.txt](phase-BX6-repro/E2E-learner-notes.txt), [e2e-progress-observation.json](phase-BX6-repro/e2e-progress-observation.json) | 여섯 증거와 mock/선택 경로 구별 |
| [A5 판정 도구](phase-BX6-repro/05-gates-simulator.png), [A9 상태 도구](phase-BX6-repro/09-sponsorship-simulator.png) | 고정 샘플의 판정·보류 화면 |
| [A5 모바일 코드](phase-BX6-repro/05-gates-read-360-viewport.png), [A9 모바일](phase-BX6-repro/09-sponsorship-overview-360-viewport.png), [A11 모바일](phase-BX6-repro/11-operations-overview-360-viewport.png) | 작은 화면의 실제 뷰포트 |
| [순차 실습 위치](phase-BX6-repro/sequential-meta.json), `mid-*-meta.json`, `mistake-*-meta.json` | 각 임시 복사본 경로. 가상환경/DB/비밀 파일은 저장소에 넣지 않음 |

## 최종 판단과 남은 일

**본문만으로 재현: 조건부.** mock 명령·파일 생성·승인 거부·공개 재조회·정산·복구·E2E는 재현됐다. A4 비용 확인 절차가 보강돼야 사람이 직접 확인하는 체크포인트까지 닫을 수 있다. A6의 마지막 상태 설명과 A11의 예약 인수 안내도 실제 출력에 맞춰야 한다. 나머지 부분 직답·용어·오류 표 개선은 위 발견 및 질문별 행에 남겼다.

이번 산출물은 이 보고서와 `docs/results/phase-BX6-repro/`의 증거뿐이다. PROJECT_STATE·설계·본문·키트·스크립트 수정이나 commit은 하지 않았다. 전체 테스트 스위트나 기존 재현 스크립트를 실행한 결과로 바꿔 주장하지 않는다. 후속 수정·재검토는 담당 단계에서 할 일로 남긴다.
