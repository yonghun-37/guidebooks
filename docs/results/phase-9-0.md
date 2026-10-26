# Phase 9-0 · 개편용 공통 부품과 자동 검사기

상태: 구현·작성자 검증 완료, Claude Code 검수 대기. 기준은 [확정 STYLE-GUIDE](../STYLE-GUIDE.md) 2·3·5절이다. 장 본문 개편은 아직 진행하지 않았다.

## 범위와 구현

- `site/assets/book.css`: 샘플 A의 카드·흐름·고정 항목, B의 굵은 직답, C의 단계표를 공통 부품으로 승격했다. 기존 클래스는 유지했고 새 클래스는 기존 본문과 겹치지 않는다. 기존 색상 변수를 사용하므로 다크 모드·인쇄 색상이 이어진다.
- `site/assets/sim/common.js`: 축 카드의 절 이동 후 키보드 초점을 옮긴다. FAQ 내부의 직접 링크를 펼치고, 인쇄할 때 FAQ를 모두 열었다가 원래 상태로 복원한다. 기존 `ReelsSim` API·저장 동작은 유지했다. 요청의 `common.js`는 저장소에서 이 경로에 있으며 `site/assets/common.js`를 중복 생성하지 않았다.
- [이론 장 v2 템플릿](../chapter-template-v2.html): 모든 부품, 축 3개, 단계표, FAQ 5개, 정리 3줄, 퀴즈 3개와 작동하는 예시 도구를 담았다. 작성 규칙·출처·복사 경로·검수 기준은 주석에 요약했다. 공개 사례는 작성 자리이며 출처를 지어 넣지 않았다. 실제 장에 복사할 때 장별 질문·사례·근거로 교체한다.
- `scripts/style_lint.py`: 표준 라이브러리만 쓰는 CLI. 위반 문구별 횟수·원문 행 번호·주변 문장, 본문 글자 수, 기준선 비율, 기준별 통과 여부를 JSON으로 출력한다. 회귀 검사는 `scripts/tests/test_style_lint.py`다.

기존 9개 `data-block`과 절 ID를 유지한다. v2에서는 `story` 블록을 FAQ로 쓰고 인물 대화는 `question`에 둔다. 단계표는 `case` 블록 끝에 둔다. 이후 장을 개편할 때 기존 절의 앵커도 보존해야 한다. `book.js`는 수정하지 않았고 기존 목차·메타·퀴즈 엔진을 재사용한다.

## 부품 계약

| 용도 | 마크업 |
|---|---|
| 먼저 답부터 | `.answer-box` 안 `.direct-answer > strong` |
| 한눈에 보기 | `nav.axis-grid[data-axis-nav] > a.axis-card[href="#절ID"]` |
| 축 설명 | `article.axis-block[id] > h3`와 `dl.axis-rows` |
| 고정 줄 | `dl.axis-rows > div` 안 `dt + dd`, 정의 → 흐름 → 얼마 → 조건 → 언제 → 지금 할 일 |
| 흐름·강조 숫자 | `.axis-flow`, `.key-number` |
| 지금 할 일 | 고정 줄의 마지막 `div.axis-action` |
| 확인할 점 | 축 끝 `aside.check-points[data-check-points]`와 제목 `확인할 점` |
| 단계표 | `table.stage-table` + `caption`, 열/행 제목의 `scope` |
| 접는 FAQ | `.chapter-faq` 안 `details > summary + .faq-answer`; 답 첫 줄은 `.direct-answer > strong` |
| 핵심 정리 | `ul.key-takeaways`의 세 항목 |

카드 링크와 FAQ는 네이티브 HTML로 동작한다. 자바스크립트를 꺼도 이동·열고 닫기가 가능하다. 인쇄는 CSS의 `::details-content`와 JS 인쇄 이벤트로 지원한다.

## 검사 범위와 기준선

- `main` 안의 학습자 텍스트를 읽는다. `main`이 없으면 `body`를 사용하고 둘 다 없으면 오류다. 장 머리·그림 설명·코드·접힌 FAQ·OS 탭·퀴즈 보기는 포함한다. 선택 가능한 항목도 학습자가 읽을 내용으로 센다.
- 스크립트·스타일·템플릿·주석·HTML 속성, 출처 각주(`source-notes`, `footnotes` 등)·참조 번호, 책 내비게이션은 제외한다. 본문 축 카드 내비게이션은 포함한다. `hidden`은 제외하되 OS 탭 패널은 포함한다. JS가 나중에 생성한 결과·속성 속 퀴즈 해설은 집계하지 않는다.
- 글자 수는 **유니코드 공백을 제외한 문자 수**다. 들여쓰기·줄바꿈으로 비율이 달라지지 않는다. 본문 금지어·내부 용어는 “확인할 점” 안에서도 검사한다.
- “미확인/단정할 수 없/별개”는 별도 집계한다. `check-points`·`data-check-points`·샘플의 `draft-check`, 또는 첫 라벨이 정확히 “확인할 점”인 상자만 단서 표현의 예외다. 본문에 그 말을 언급하는 것만으로 예외가 되지 않는다. 상자 밖 합계는 장당 2회까지 허용한다.
- 사실 ID는 `PRAC-`·`API-`·`META-`를 포함한 현재 사실표의 ID 계열과 `R2-` 계열을 검사한다. 일반 표기 `API`, `UTF-8`, `ISO-8601`은 금지하지 않는다.
- [baseline.json](phase-9/baseline.json)은 이론 14개·실습 11개 **총 25개**의 원본 SHA256과 글자 수를 보존한다. 추출 규칙 식별자는 `learner-main-non-whitespace-v1`이다. 다음 개편에서 이 파일을 재생성하지 않는다.
- `--baseline`을 주면 모든 파일의 비율을 보고하고 **이론편만 70% 이하**인지 검사한다. 누락·잘못된 집계 방식의 기준선은 오류다. `--write-baseline`은 기존 파일을 덮어쓰지 않는다.
- 종료 코드: `0` 문체 검사 통과, `1` 기준 위반, `2` 입력·기준선 오류. 위반이 있어도 보고서는 저장한다. 직답의 정확성·출처의 충분성·학습자 질문 충족은 자동 판정하지 않는다.

## 개편 전 결과

[lint-before.json](phase-9/lint-before.json)에 25개 파일의 상세 결과를 저장했다.

| 항목 | 현재 집계 |
|---|---:|
| 본문 글자 수 합계 | 92,324 |
| 금지어 | 138회 |
| 내부 용어 | 59회 |
| 상자 밖 단서 표현 | 104회 |
| 상자 안 단서 표현 | 0회 |
| 기준선 대비 비율 | 모든 장 100% |

현재 원고는 개편 전이므로 25개 모두 종합 기준을 통과하지 않는다. 이론편은 분량이 아직 100%이고 실습편에는 금지어·내부 용어가 남아 있다. 이 결과는 다음 개편의 출발점이며 이번 단계의 검사기 실행 실패를 의미하지 않는다. 본문을 수정해 수치를 줄이지 않았다.

## 실행과 검증

최초 스냅샷 생성(이미 실행했으므로 재실행하지 않는다):

```sh
python3 scripts/style_lint.py site/chapters/[0-9][0-9]-*.html site/practice/[0-9][0-9]-*.html \
  --write-baseline docs/results/phase-9/baseline.json --output /tmp/phase9-initial-lint.json
```

전체 검사·검사기 회귀 검사:

```sh
python3 scripts/style_lint.py site/chapters/[0-9][0-9]-*.html site/practice/[0-9][0-9]-*.html \
  --baseline docs/results/phase-9/baseline.json --output docs/results/phase-9/lint-before.json
python3 -m unittest discover -s scripts/tests -v
node --check site/assets/sim/common.js
```

- 전체 문체 검사는 예상대로 **종료 코드 1**이다. 위 집계와 비율 1.0을 확인했다. v2 템플릿 단독 문체 검사는 **종료 코드 0**이었다.
- 검사기 테스트 **10개 통과**. 추출 범위·인라인 태그로 나뉜 용어·상자 예외·용어 오탐·행 번호·공백 안정성·70% 경계·실습 분량 제외·CLI 종료 코드·기준선 덮어쓰기 금지를 확인했다.
- [정적 검사 결과](phase-9/static-check.json): 사이트 35개 HTML + 템플릿, 내부 링크·자산 **1,368개**, 중복 ID·없는 앵커 오류 **0**. 장·실습·샘플 **33개 파일의 작업 시작 대비 SHA256 변화 0**. 기준선 25개와 개편 전 보고서의 해시·글자 수 일치도 확인했다.
- [브라우저 검사 결과](phase-9/browser-check.json): 기존 학습 페이지·표지·부록·샘플과 템플릿 **35페이지 × 1280/375/360px**, **146개 검사 통과**. 가로 넘침·콘솔/페이지 오류 **0**. 카드 키보드 이동·초점, FAQ 열고 닫기·직접 링크·인쇄 후 상태 복원, JS 없는 카드/FAQ/FAQ 인쇄, 다크 모드, 예시 도구·극단값, 기존 퀴즈·목차 통합을 확인했다.
- 재현: 저장소 루트에서 `python3 -m http.server 8539 --bind 127.0.0.1`로 제공한 뒤 `node docs/results/phase-9/verify.mjs`. 브라우저 도구·Chromium은 기존 `/tmp/ai-insta-phase3-browser`·사용자 캐시를 사용한다. 외부 폰트는 빈 CSS로 대체해 검사했다. 실제 OS·다른 브라우저 검증은 수행하지 않았다.
- 시각 확인: [1280px](phase-9/template-1280.png), [375px](phase-9/template-375.png), [360px 다크](phase-9/template-dark-360.png), [360px 축 블록](phase-9/axis-360.png).

## 인계

[PROJECT_STATE.md](../PROJECT_STATE.md)에 공통 부품·기준선·검증 결과와 미완료 장 개편을 반영했다. 시작 시 존재하던 상태 문서 변경·`scripts/build_practice.py` 및 작업 중 나타난 다른 요청 파일은 보존했다. 설계 문서·장 본문·샘플·연구·키트·배포는 수정하지 않았다. 다음 단계는 이 템플릿과 확정 문체 기준으로 각 장을 개편하고 같은 기준선으로 검사하는 것이다. 완료 알림·커밋·푸시는 하지 않았다.
