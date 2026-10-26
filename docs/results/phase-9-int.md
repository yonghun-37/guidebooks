# Phase 9-int · 개편 통합

상태: **개편 통합·작성자 검증 완료, Claude Code 검수 대기.** Claude Code 검수·독립 초보자 검수는 별도다. 기준은 [STYLE-GUIDE](../STYLE-GUIDE.md), [공통 부품](phase-9-0.md), [9a](phase-9a.md)·[9b](phase-9b.md)·[9c](phase-9c.md)·[9d](phase-9d.md)와 각 통합 요청이다. 기존 결과 문서 관례를 재사용하며 새 specs·ADR은 만들지 않았다.

## 요구사항과 결과

- [x] 9a~9d 요청을 검토해 공통 장 데이터와 부록을 통합했다.
- [x] 바뀐 이론 제목·결과물, 실습 11개 결과물·예상 시간을 `book.js`와 표지 목차에 맞췄다. 기존 예상 시간 숫자는 보존하고 이론 표시만 `약 N분`으로 정리했다.
- [x] `scripts/build_appendices.py`로 실험실·용어집·출처를 재생성했다. 원고를 덮어쓰는 옛 실습 생성기는 실행 차단했다.
- [x] 비교 샘플을 보존하고 상단에 **“선택 완료: A 뼈대 + B·C, 3장에 반영됨”** 안내와 현재 3장 링크를 넣었다.
- [x] 최종 브라우저·배포 경로 검사와 결과 기록을 완료했다.
- [x] 진행 현황과 PROJECT_STATE를 현재 원고 기준으로 갱신했다. 다음 작업은 인터랙션 고도화 예정이며 이번 작업에서 선행 구현하지 않았다.
- [x] 지정된 통합 완료 알림을 전송했다(HTTP 200).

## 통합 판단과 일반화한 해법

| 요청·차이 | 적용과 이유 |
| --- | --- |
| 9a의 `querySelector` 정규식 추가, 9b의 목록 수동 diff, 9c의 새/제거 도구 | **현재 HTML의 `data-block=figure/simulator`를 읽어 목록을 생성**한다. 외부 모듈·인라인 JS·정적 연습을 같은 방식으로 다루므로 코드 연결 방식에 의존하지 않는다. 제목은 실제 축 이름 또는 도구 제목을 따른다. 9b의 제안 제목과 현재 원고가 다른 경우 현재 HTML을 채택했다. |
| 3·4장의 옛 요약과 새 저장하지 않는 도구 | 실험실 카드를 구매 수수료 계산·기획 점검 바로가기로 바꿨다. 옛 저장값을 새 계산 결과로 읽지 않는다. 14장 변경 입력만 요약에 전달한다. 삭제 버튼은 이전 3·4장 기록도 지운다. |
| 14장의 이전 자동 일정 결과와 현재 시간 계산 | 입력 ID는 같아 이전 저장 결과가 섞일 수 있다. 공통 저장 형식을 2판으로 올리고 1판 입력 읽기를 유지했다. 원본 도구를 열면 **기존 입력으로 현재 결과를 재계산해 저장**한다. 실험실은 이전 결과를 숨기고 14장에서 확인하도록 안내한다. 문자열 모양으로 신구 결과를 추측하지 않는다. 이 변경은 기존 입력·현재 계산·공통 저장 API를 재사용하며 별도 변환 계산기를 만들지 않는다. |
| 과거 용어 인계의 31개와 현재 본문 | 현재 이론·실습 일반 텍스트에 쓰인 말만 24개 남겼다. `프롬프트→지시문`, `브랜디드 콘텐츠→협찬`으로 표시 이름을 바꾸되 기존 용어 ID를 유지한다. 현금 잔액 등 없어진 말은 제거했다. 첫 설명 자리 24곳에 `data-term`·설명·용어집 앵커를 함께 생성하며 코드·기존 링크·각주·제목은 건드리지 않는다. |
| 보존용 옛 각주와 실제 본문 인용 | 각주에 등장하는 모든 S번호 대신 **본문에서 참조하는 각주 항목의 S번호**를 수집했다. 현재 출처 98개와 해당 본문 각주로 가는 역링크를 생성했다. 원고의 옛 앵커는 그대로 보존한다. 출처 페이지에는 연구 작업자·단계·사실 ID를 다시 노출하지 않는다. |
| 9d의 이전 실습 생성기 | 직접 관리하는 현재 HTML을 원본으로 삼고 `build_practice.py` 진입점에서 설명과 함께 종료한다. 재실행해 개편 원고나 확인표가 덮어써지는 것을 막는다. |
| 공통 CSS·FAQ·OS 탭 | 요청서 모두 CSS·기존 FAQ·탭 동작 변경이 필요 없었다. `book.css`·`practice.js`를 유지하고 기존 기능을 통합 검증한다. `common.js` 변경은 위 저장 결과 갱신에 한정한다. |

실험실 **29개**는 축 그림 14개·계산/점검 도구 12개·정적 연습 2개·한 달 요약 1개다. 이를 모두 시뮬레이터로 부르던 표지·현황 문구도 **그림·계산·연습·요약**으로 맞췄다. 목록 주소는 현재 블록을 가리키며 기존 장/도구 앵커는 제거하지 않았다.

전 페이지 문체 검사를 위해 비교 샘플의 내부 단계명과 반복 면책도 짧게 고쳤다. 구성·계산 도구·선택 기록은 유지했다. 표지 `1장부터`가 검사기의 `장부`와 겹치는 경우는 자연스러운 `첫 장 읽기`로 바꿨다. 검사 기준이나 기준선을 완화하지 않았다.

## 검증

검증 환경은 Linux·Python 3.11·Chromium 1228이다. 외부 폰트 CSS는 빈 응답으로 대체했다.

| 검사 | 실제 결과 | 증거 |
| --- | --- | --- |
| 문체·분량 | 이론 14장+실습 11개 통과. 금지어·내부 용어·상자 밖 단서 각각 0. 모든 이론 46.0~68.3%, 합계 34,429/59,922자(57.5%) | [25페이지 검사](phase-9-int/lint-chapters.json) |
| 나머지 전 페이지 문체 | 부록·표지·대기 페이지·E2E·비교 10개, 책장·현황 2개 모두 통과 | [기타 10개](phase-9-int/lint-other.json) · [책장 2개](phase-9-int/lint-shelf.json) |
| 링크·자산·앵커 | 사이트 HTML 35개, 책장 배포 링크 포함 내부 참조 **1,290개**, 오류 0. 용어 24개/링크 24개 일치, 본문 각주 165개에서 실제 출처 98개 확인. 이론·실습 기존 앵커 1,146개와 35단계/E2E 키 보존 | [정적 결과](phase-9-int/static-check.json) |
| 재생성·보호 | 부록 반복 생성 시 모든 사이트 파일 해시 동일. 옛 실습 생성기는 종료 1로 차단하고 원고·메뉴 확인표 해시 보존 | 같은 정적 결과 |
| 브라우저·조작 | **35페이지×1280/375/360px, 2,022개 검사 통과**, 렌더링된 내부 링크 597개 유효. 가로 넘침·콘솔/페이지/로컬 HTTP 오류 0. FAQ·축 이동·퀴즈 정답/오답/초기화·OS 탭·체크리스트 키보드, 인쇄 복원·JS 끔·저장 차단·E2E 공유/초기화·28개 원본 임베드·옛 저장 입력 보존/결과 갱신 확인 | [브라우저 결과](phase-9-int/browser-check.json) |
| Pages 하위 경로 | GitHub Actions와 같은 파일 배치를 `/guidebooks/` 아래에 조립해 **469개 검사 통과**, 책장·현황·표지·실험실·실습을 세 폭에서 확인 | [배포 배치 결과](phase-9-int/deployed-check.json) · [현황 375px](phase-9-int/progress-375.png) |
| 검사기 테스트 | `python3 -m unittest discover -s scripts/tests -v` **10개 통과** | 실행 결과 |
| 스타터 키트 | `cd starter-kit` 후 `.venv/bin/python -m pytest -q` **67개 통과, 25.42초** | 실행 결과. 키트 코드는 수정하지 않음 |

최초 브라우저 실행의 프레임 대기 오류는 로딩 완료 조건을 검사기에 추가해 수정했다. 마지막에는 이전 판 저장값 회귀 검사까지 포함한 전체 검사를 다시 실행해 위 수치를 확인했다. 모바일 화면에서 표지·실험실·용어집·선택 안내의 줄바꿈과 여백을 직접 확인했다. [표지 375px](phase-9-int/cover-375.png) · [실험실 375px](phase-9-int/lab-375.png) · [용어집 375px](phase-9-int/glossary-375.png) · [비교 안내 375px](phase-9-int/drafts-375.png).

재현 명령(기준선을 재생성하지 않는다):

```sh
python3 scripts/build_appendices.py
python3 docs/results/phase-9-int/check.py
python3 scripts/style_lint.py site/chapters/[0-9][0-9]-*.html site/practice/[0-9][0-9]-*.html \
  --baseline docs/results/phase-9/baseline.json --output /tmp/phase9int-chapters.json
python3 scripts/style_lint.py site/*.html site/chapters/coming-soon.html site/practice/e2e.html site/drafts/*.html
python3 scripts/style_lint.py shelf/*.html shelf/progress/*.html
python3 -m unittest discover -s scripts/tests -v
(cd starter-kit && .venv/bin/python -m pytest -q)
# 별도 창: python3 -m http.server 8549 --bind 127.0.0.1
node docs/results/phase-9-int/verify.mjs
# 배포 배치 검사기에서 /tmp/phase9int-pages/guidebooks를 조립한다.
# 별도 창: python3 -m http.server 8550 --directory /tmp/phase9int-pages --bind 127.0.0.1
node docs/results/phase-9-int/deployed.mjs
```

## 남은 확인과 인계

실제 Instagram 계정의 로그인·가입·게시·예약·인사이트 조회·토큰 발급/갱신·지급, Windows/macOS·다른 브라우저·독립 초보자 따라 하기는 수행하지 않았다. 18개 앱 메뉴의 실제 기기 확인 속성·기존 연구 공백을 유지했다. 유료 API·결제·호스팅 업로드는 하지 않았다.

[PROJECT_STATE](../PROJECT_STATE.md)와 `shelf/progress/index.html`에 문체 개편 완료·인터랙션 고도화 예정을 반영했다. Claude Code 검수·독립 초보자 검수·조건부 실제 계정 검증이 남아 있다. 시작 시 Git 작업 상태는 깨끗했으며 다른 작업자는 없었다. 연구·키트·설계·배포 설정은 수정하지 않았다. commit·push·배포는 하지 않는다.

## 완료 알림

`python3 scripts/notify.py "✅ [Phase 9 통합 완료] ..."`로 한국어 4줄을 전송했다. **HTTP 200**, 메시지 ID `1564105335600455781`. 토큰을 출력하거나 기록하지 않았다. commit·push·배포하지 않았다.
