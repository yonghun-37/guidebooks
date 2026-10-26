너는 ai-insta 프로젝트의 작업자(Codex)다. AGENTS.md, docs/DESIGN.md(특히 10절·10.1절), research/practice-instagram.md, research/FACT-SHEET.md(PRAC-*, API-*), docs/results/phase-7r.md, docs/results/phase-5d.md, site/assets/book.js, starter-kit/README.md를 읽어라.
이번 작업은 **Phase 7w. 인스타 실습편 집필과 구조 개편**이다. 다른 작업자는 없으므로 공통 파일 수정이 허용된다. commit하지 마라.

1. 구조 개편: book.js에 '이론편'(기존 1~14장, 15 실험실, 16 용어집, 출처)과 '실습편'(실습 0~10) 두 트랙을 만든다. 표지·목차·사이드바·장 상단에 `(이론)`/`(실습)` 표시. 표지에 "오늘 첫 게시까지: 실습편 시작" 주요 버튼과 "E2E 한눈에 보기" 링크를 추가한다. 기존 URL은 깨지지 않게 유지한다.
2. 실습 페이지: site/practice/00-start.html ~ 10-insights.html와 site/practice/e2e.html(전 단계 체크리스트, 진행 저장). DESIGN 10.1의 단계 틀(지금 하는 일/왜/따라 하기/이렇게 보이면 성공/이렇게 보이면?/Windows·macOS 탭)을 공통 컴포넌트(CSS 클래스 + 탭 JS)로 만든다. 실습 1에는 DESIGN 10절의 테스트 계정 만들기·상자 3개를 반드시 넣는다.
3. 근거: 절차·수치는 practice-instagram.md와 FACT-SHEET 근거만 쓴다. 7r에서 **앱 메뉴 이름이 미확인**인 단계는 메뉴 이름을 단정하지 말고 "앱 버전에 따라 이름이 다를 수 있음 — 보통 이런 이름" 형태와 공식 도움말 링크, 그리고 `data-verify="app-menu"` 속성을 붙여 나중에 사용자 실계정 확인(7v)으로 갱신할 수 있게 표시한다. 미확인 목록을 docs/results/phase-7w-verify-list.md로 만든다(실습/단계/확인할 화면/현재 문구).
4. 화면 그림: 인스타그램 실제 스크린샷 대신 직접 그린 도식형 SVG(휴대폰 틀, 버튼 위치 강조, 번호 표시)를 site/assets/img/practice/에 만든다. 브랜드 로고·아이콘을 복제하지 않는다.
5. 키트 live 경로 갱신(starter-kit/): Graph API 버전을 설정값으로(기본 v26.0, PRAC 근거), Instagram Login 경로는 이미지·동영상 모두 공개 URL 필요함을 반영. 초보자용 공개 URL 준비 도우미: `prepare_hosting.py`가 승인된 JPEG/MP4를 지정 폴더로 복사하고 GitHub Pages 웹 업로드(드래그 앤 드롭) 방법과 최종 URL 규칙을 안내, `publish.py --live --base-url <URL>`로 연결. 토큰은 starter-kit/.env(또는 환경변수)에서 읽고 .env.example 제공, 토큰 만료(60일)·갱신 안내. 모든 네트워크는 모킹 테스트로 검증하고 live 실행은 하지 않는다. 기존 테스트 포함 전부 통과.
6. 이론편 장의 작업실 노트 중 실제 계정·도구 조작 단계는 해당 실습으로 링크(중복 서술 줄이기). 이론편 1장에 "실습편으로 바로 가기" 안내.
7. 검증: 전 페이지 1280/375/360px 가로 넘침·콘솔 오류·내부 링크·탭/체크리스트 키보드 조작·진행 저장 실패 시 동작, 실습 2~6의 키트 명령은 깨끗한 임시 복사본에서 README대로 실제 실행해 출력이 본문의 "이렇게 보이면 성공"과 일치하는지 확인. 결과 docs/results/phase-7w.md(+스크린샷 docs/results/phase-7w/), docs/PROJECT_STATE.md, shelf/progress/index.html 상태 갱신.
8. `python3 scripts/notify.py "✅ [Phase 7w 완료] ..." <실습 7 스크린샷>`로 한국어 보고.
