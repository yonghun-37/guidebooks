너는 ai-insta 프로젝트의 작업자(Codex)다. 먼저 다음을 읽어라.
- AGENTS.md, .agents/skills/guidebook-pipeline·guidebook-writing, docs/STYLE-GUIDE.md
- **docs/DESIGN-baby.md**: 8절 건강 정보 안전 규칙과 11절 N2 반영 결정이 최우선이다.
- docs/learner-questions-baby.md
- research-baby/: BRIEFING, FACT-SHEET, SOURCES, QUESTION-MAP, 주제 노트
- docs/results/phase-N3.md
- **완성 샘플 site-baby/chapters/07-hospital.html과 site-baby/practice/07-apply.html**: 이 두 쪽의 틀·문체·컴포넌트를 그대로 따른다.

## 공통 규칙
- **동시에 다른 작업자들이 site-baby의 다른 쪽을 쓴다.** 내가 맡은 파일과, 그 장 전용 css/js(`assets/chNN.*` 또는 `assets/pNN.*`)만 만들고 고친다.
  - 공용 자산은 수정하지 않는다: book.js, catalog.js, common.js, baby.css, book.css, emergency-data.js, glossary.js, lab.js, index.html.
  - 공용 자산에 필요한 변경(장 상태 '완료' 전환, 용어, 실험실 등록 등)은 결과 문서의 "통합 요청" 절에 적는다. 다음 통합 단계가 반영한다.
- 응급 신호는 emergency-data.js의 공통 컴포넌트를 불러 쓴다. 문구를 복사해 박아 넣지 않는다.
- 근거:
  - 건강·제도 주장은 FACT-SHEET 근거와 [N###] 각주를 단다.
  - `확인` 상태만 단정형으로 쓴다. `상충`은 "국내/국외 차이" 상자에 두 근거를 모두 쓴다. `미확인`은 확인 방법만 쓴다.
  - 약 이름·용량, 브랜드 이름, 사실 ID, 내부 용어는 본문에 쓰지 않는다.
  - 장 머리에 "2026년 10월 조사 기준"을 한 번 쓴다.
- 이론 장은 STYLE-GUIDE 2절 틀을 따른다: 먼저 답부터 → 한눈에 보기 → 축별 설명(같은 틀 반복) → 해 보기 → 실제 사례(가상 가족 장면) → 작업실 노트 → FAQ 5개(learner-questions-baby의 해당 장 질문) → 핵심 3줄 + 퀴즈.
- 실습 쪽은 STYLE-GUIDE 4절 단계 틀을 따른다. 처음에 "이 실습이 끝나면 내 손에 있는 것", 끝에 "다음 실습"을 둔다.
- 시각자료(STYLE-GUIDE 6절, DESIGN-baby 6절):
  - 손 동작·순서·비교·달력·흐름은 직접 그린 선화 SVG로 적극적으로 그린다.
  - 사람·아기는 단순하지만 알아볼 수 있게 그린다. 아기 동작을 보여 주는 그림에는 아기가 보여야 한다. 예: 겨드랑이 체온은 어른 혼자 그린 그림이 아니라 아기 겨드랑이에 체온계를 댄 그림.
  - 실제 사진·로고·캡처는 쓰지 않는다. 장식으로 개수를 채우지 않는다.
- 예시: 봄이 가족의 실제 날짜 흐름을 따른다(퇴원 0일 → 1주 → 2~5주 검진 → 1개월 → 2개월 접종 → 백일). 장마다 그 시기의 장면으로 시작한다.
- 검증:
  - scripts/style_lint.py로 내 파일을 검사한다.
  - `python3 scripts/check_site.py --site site-baby`를 실행한다. 다른 작업자 파일의 오류는 무시하고 기록만 한다.
  - 내 쪽을 375px·1280px, 라이트·다크로 스크린샷을 찍는다.
- commit하지 않는다. 마지막에 결과 문서를 쓰고 `python3 scripts/notify.py "📝 [육아 편 <단계>] ..."`로 한국어 보고한다.

## 이번 작업: Phase N5 — 실습편 0~6·8~10 + E2E + 인쇄 부록
맡은 파일만 만든다.
실습 7(`practice/07-apply.html`)은 N3에서 완성됐다. 나머지를 같은 틀로 쓴다. 실습은 "~해요/~하세요" 친근체를 쓰고, 모유/분유·온라인/방문 같은 탭을 필요한 곳에 쓴다.
- 0 `practice/00-start.html` 시작 전에: 출산 전·퇴원 날 준비물(꼭 필요한 것 / 나중에 사도 되는 것, 브랜드 금지), 연락처 카드 작성(7장 컴포넌트 재사용), "화면·제도는 바뀔 수 있어요" 한 번.
- 1 `practice/01-home.html` 집에 오는 날: 카시트 장착 확인, 안전한 잠자리 세팅 점검(그림 체크).
- 2 `practice/02-diaper.html` 기저귀 갈기(단계 선화) + 변 확인과 이상 변 연락 연습(자체 색표 금지).
- 3 `practice/03-feeding.html` 먹이기: 모유 수유 자세·물리기 / 분유 타기·젖병 세척·소독 / 트림 (탭, 단계 선화).
- 4 `practice/04-sleep.html` 재우기: 잠자리 비우기·등 대고 재우기·뒤집기 시도 확인·밤 수유 동선. 속싸개 묶기는 필수 과제가 아니다.
- 5 `practice/05-bath.html` 목욕과 배꼽 관리: 부분 씻기 기본, 통목욕 시점은 퇴원 안내·소아과 확인.
- 6 `practice/06-emergency.html` 응급 신호 연습: 5사례(발열 / 호흡·의식 / 회백색 변 / 초록 구토 / 먹지 못함) → 연락처 → 의료진에게 말할 문장 만들기. 체온 재기 실습(아기 겨드랑이 그림). "집에서 지켜봐도 됨" 판정은 없다.
- 8 `practice/08-checkups.html` 접종·검진 일정 만들기와 첫 예약: 경로 선택 달력, 병원 전화 예약 대본, 예약 기록.
- 9 `practice/09-records.html` 1주 기록: 수유·수면·기저귀 기록기(버튼 기록, 오늘 요약, localStorage만, CSV 내려받기), 종이 기록지 인쇄, 기록으로 진료 때 말하는 법.
- 10 `practice/10-play.html` (선택) 깨어 있을 때 놀기: 터미타임·눈 맞춤·말 걸기, 백일 준비(사진·기념은 짧게).
- E2E `practice/e2e.html`: 실습 0→10 체크리스트, 주차별 할 일 달력, 총 소요 시간(대략).
- 인쇄 부록 `print/`:
  - weekly-checklist.html: 0~15주 주차별 체크리스트
  - log-sheet.html: 수유·수면·기저귀 기록지 1주
  - parent-crisis.html: 부모 위기 연락 카드(109, 1577-0199, 119·112, 아이사랑 1644-7373)
  - print/emergency.html 하단에 부모 위기 번호 한 줄 추가(이 파일은 네가 수정해도 된다)
  - 모두 A4 한 쪽, 흑백 구분.
결과 문서: docs/results/phase-N5.md
