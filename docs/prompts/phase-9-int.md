너는 ai-insta 프로젝트의 작업자(Codex)다. AGENTS.md, .agents/skills/guidebook-pipeline·guidebook-writing, docs/STYLE-GUIDE.md, docs/results/phase-9-0.md, phase-9a~9d.md와 각 `-requests.md`를 읽어라.
이번 작업은 **Phase 9-int. 개편 통합**이다. 다른 작업자는 없다. commit하지 마라.
1. 9a~9d requests를 검토해 book.css/common.js/book.js/practice.js에 병합한다. 충돌은 더 일반적인 해법을 택하고 이유를 기록한다.
2. 장 제목·결과물·시간이 바뀐 경우 book.js 장 데이터와 표지·목차를 맞춘다. 15장 실험실(scripts/build_appendices.py 재실행), 16장 용어집(용어 삭제·이름 변경 반영, data-term 일치), 출처 페이지(실제 인용 출처만)를 재생성한다.
3. site/drafts/는 개편이 반영됐으므로 비교 페이지 상단에 "선택 완료: A 뼈대 + B·C, 3장에 반영됨" 안내를 넣고 유지한다.
4. 전체 검증: style_lint 전 페이지, 내부 링크·앵커, 1280/375/360px 가로 넘침·콘솔 오류, 퀴즈·FAQ·탭·체크리스트 키보드, 스타터 키트 테스트. shelf/progress/index.html 상태 갱신(문체 개편 완료, 인터랙션 고도화 예정), docs/PROJECT_STATE.md 갱신.
5. docs/results/phase-9-int.md, `python3 scripts/notify.py "✅ [Phase 9 통합 완료] ..."`.
