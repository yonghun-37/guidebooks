너는 ai-insta 프로젝트의 작업자(Codex)다. AGENTS.md, docs/DESIGN.md 10절, docs/PLAN.md("Hermes 호출법", "Phase 7"), research/FACT-SHEET.md, research/graph-api-publishing.md, research/account-setup-security.md, research/scheduling-automation-tools.md를 읽어라.
이번 작업은 **Phase 7r. 실습편용 '오늘 기준 절차' 재조사**만이다. site/와 starter-kit/은 다른 작업자가 수정 중이니 건드리지 마라. commit하지 마라.

목표: 초보자가 2026-10-26 오늘 실제로 따라 해서 게시까지 끝낼 수 있는 **단계별 절차**(버튼·메뉴 이름, 순서, 조건, 흔한 오류)를 공식 근거로 확보한다.

1. PLAN.md Phase 7r의 항목을 질의 8회 이하(재시도 포함)로 나눠 Hermes에 묻는다. 질의마다 "단계별 절차를 번호로, 각 단계의 버튼/메뉴 이름(한국어 UI와 영어 UI 모두 가능하면), 공식 도움말 URL과 갱신일, 2025~2026년에 바뀐 점, 확인 못 한 단계는 미확인"을 요구한다. 질의 파일·원응답은 $RUN/queries/practice-*.txt, $RUN/raw/practice-*.md.
2. 특히 확인할 것: (a) 개발 모드 앱에서 앱 역할(테스터 등)이 있는 본인 계정으로 앱 검수 없이 콘텐츠 게시가 가능한지 (b) 현재 Graph API 버전 (c) 이미지 게시에 공개 URL이 필수인지, 릴스·이미지의 재개 가능 업로드(rupload) 지원 범위 (d) 초보자가 쓸 수 있는 무료 공개 URL 호스팅(예: GitHub Pages/저장소 raw, 클라우드 스토리지 무료 등급)과 주의점 (e) 장기 토큰 수명과 갱신 (f) 앱에서 AI 정보·유료 파트너십 라벨 켜는 위치 (g) 캐러셀에 이미지+동영상 혼합 가능 여부와 앱/API 차이.
3. 공식 문서 최소 6개를 직접 열어 확인 표시한다.
4. research/practice-instagram.md(실습 1~10에 대응하는 절차 노트: 각 단계, 근거 번호, 확인 수준, 화면이 다를 때 대처)를 쓰고, SOURCES.md·FACT-SHEET.md에 새 항목(사실 ID 접두어 PRAC-)을 추가한다. 상충은 상충으로 표시한다.
5. docs/results/phase-7r.md를 쓰고 `python3 scripts/notify.py "✅ [Phase 7r 완료] ..."`로 한국어 보고.
