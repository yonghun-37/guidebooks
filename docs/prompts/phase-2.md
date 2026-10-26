너는 ai-insta 프로젝트의 작업자(Codex)다. 먼저 AGENTS.md, docs/DESIGN.md, docs/PLAN.md를 읽어라.
이번 작업은 docs/PLAN.md의 **Phase 2. 참고 사이트 분석 (REA)** 만이다.

1. 너에게 연결된 MCP 서버 `rea`(Reverse Engineer Anything)의 도구 목록을 확인하고, 웹사이트/프런트엔드 분석에 쓸 수 있는 도구로 https://art.euiyun.com/color/ 를 분석한다. 표지, 1장(chapters/overview.html), 본문 장 2개 이상, 실험실(chapters/lab.html), 용어집을 본다. REA로 불가능한 부분은 이유를 적고 curl/Node/Playwright 등으로 보완한다. 임시 다운로드는 저장소 밖(`mktemp -d`)에 둔다.
2. PLAN.md Phase 2의 "파악할 것"을 모두 조사해 docs/reference-analysis.md 를 쓴다. 각 패턴마다: 관찰 내용(근거 URL/선택자), ReelsBook 적용 방안, 따라 하지 않을 점. 장 내부 블록 순서, 시뮬레이터 상호작용 방식(드래그/슬라이더/토글, 흑백 보기 같은 보조 토글, '무너뜨리기' 같은 극단값 체험), 퀴즈 UI, 진행 표시, 다크 모드, 모바일 처리, 폰트·여백 수치를 구체적으로 적는다.
3. 원 사이트의 문장·이미지·코드를 저장소에 복사하지 않는다. 짧은 구조 설명과 수치만 기록한다.
4. docs/results/phase-2.md 에 사용한 REA 도구, 성공/실패, 핵심 결론 10줄을 쓴다.
5. git commit 하지 마라(다른 작업자가 동시에 커밋한다). docs/PROJECT_STATE.md도 건드리지 마라.
6. 마지막에 `python3 scripts/notify.py "✅ [Phase 2 완료] ..."` 로 5줄 이내 보고.
