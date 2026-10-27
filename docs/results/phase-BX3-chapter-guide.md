# BlogBook 심화편 장 틀 사용법

대상: 남은 A0·A2~A8·A10~A12·E2E 집필자. 최우선 문체는 `docs/STYLE-GUIDE.md`, 설계 충돌은 `DESIGN-blog-advanced.md` 8절을 따른다. 공통 파일 변경이 필요하면 집필 작업자가 직접 고치지 말고 통합 요청에 남긴다.

1. **파일과 외곽**: `site-blog/advanced/01-environment.html`을 형식 참고로 삼는다. 자리 페이지 파일명을 유지하고 `body data-advanced`를 book.js의 slug와 일치시킨다. 완성 후 `data-manuscript="complete"`로 바꾸고 통합 담당자에게 장 상태 `완성`을 요청한다. `book.css → advanced.css`, `book.js → common.js → advanced.js`를 로드한다. 전용 CSS는 기존 색 변수로 두 테마를 지원한다.
2. **장 순서**: 먼저 답부터 → 만드는 파일·완료 조건 → 한눈에 보기 → 시작 상태 확인 → 단계 → 코드 읽기 → 바꿔 보기 → 흔한 오류 → 체크포인트 → 확인할 점 상자 하나 → 정리. 각 절은 `.chapter-block[id]`와 `<h2>`를 가진다. 장 머리 기준월은 한 번만 쓴다. 대화는 서윤 질문·태오 직답으로 1~2회만 넣는다. 예시는 「봄이랑 크는 집」을 이어 쓴다.
3. **시작과 명령**: `course.py start A번호`가 output/private/config.toml을 교체한다는 안내를 먼저 쓴다. 명령은 키트 폴더의 활성 venv에서 실행한다. `.os-tabs[data-os-tabs]` 안의 `[data-os=windows/unix]` 버튼과 `[data-os-panel=windows/unix]` 두 section을 복제한다. JS는 탭·키보드·복사를 붙이고, JS가 없으면 두 명령이 모두 읽힌다. 명령 code에는 `data-run="windows"` / `"unix"`를 붙이면 대조하기 쉽다.
4. **성공 문구**: `blog-auto-kit/course/commands.md`의 순서로 빈 복사본에서 실행한다. `course/expected/장/outputs.json`의 stdout을 `<samp data-expected="A번호|python …">`에 그대로 넣는다. expected에 없는 보조 실행은 실제 stdout을 확인해 “실행 결과”로 구분하고 결과 문서에 한계를 적는다. `check`는 장 명령이 끝난 뒤 실행한다. 기본 경로와 바꿔 보기 경로를 섞어 checkpoint 실패를 방치하지 않는다.
5. **코드**: 실제 키트 발췌는 한 번에 25줄 이하. `data-source="파일:시작줄:끝줄"`와 외부 GitHub `blob/main/blog-auto-kit/파일#L줄` 링크를 붙인다. 바로 아래 “읽는 법” 표는 원본 줄 번호 → 하는 일이다. 내부 사이트 링크는 상대 경로만 쓴다. 키트가 다르면 수정하지 말고 요청 문서에 남긴다.
6. **그림과 정책**: 흐름·상태·폴더·요청/응답은 의미 있는 그림으로 보여 준다. `<figure>`·`<figcaption>`·접근 가능한 이름을 갖춘다. 화면은 직접 그린 위치 그림, “보통 이런 이름”·공식 링크·버전 차이 안내를 쓴다. mock / Docker 로컬 / 실제 호스팅의 성공 증거를 섞지 않는다. 정책·조건은 [BX###] 각주와 장 끝 `.source-notes`에서 공식 원문으로 연결한다. 본문에는 사실표 ID·작업 단계 이름을 쓰지 않는다.
7. **안전과 저장**: 건강·협찬·제휴·아이 정보·기존 글 갱신은 항상 사람 승인이다. 광고주 확인과 최종 승인을 나눈다. 계약 AI 허용을 먼저 확인하고, false는 사람 작성·unknown은 보류한다. 법적 금지 / 프로젝트 거절 / 자료 보류를 구별한다. 도구는 기본 본문을 정적 HTML로 남기고 `blogbook:` 저장키, 읽기·쓰기 try/catch, 상태 알림, 네이티브 키보드 조작을 쓴다.

마지막으로 style_lint, check_site, 본문 명령 대조, 1280/375/360 × 라이트/다크·키보드·JS 꺼짐을 검증한다. 현재 check_site의 BX 출처 등록 문제는 [통합 요청](phase-BX3-requests.md)을 확인한다. 결과 문서에는 학습자 질문별 **직답·예·할 일**과 미실행 환경을 남긴다.
