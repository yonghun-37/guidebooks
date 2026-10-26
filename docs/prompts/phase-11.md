너는 ai-insta 프로젝트의 작업자(Codex)다. AGENTS.md, .agents/skills/guidebook-writing·guidebook-pipeline, docs/STYLE-GUIDE.md, **docs/reference-analysis-books.md(6·7절 제안과 상위 5 명세)**, docs/results/phase-9*.md를 읽어라.
이번 작업은 **Phase 11. 인터랙션 고도화(P0 5개 + 접근성 조건)** 다. 개편(Phase 9)이 끝난 본문 위에 구현한다. commit하지 마라.

구현 범위:
- R01 3장 돈의 네 갈래 조작형 흐름, R02 7장·실습4 실제 문안 카드 편집기(실시간 줄바꿈·잘림 미리보기), R03 8장·실습5 재생 가능한 릴스 타임라인(장면·자막·음성 트랙, 재생 헤드, 구간 반복, 프레임 정지), R04 10장·실습8 게시 단계 시뮬레이션(요청 성공과 게시 완료 구별, 실패 주입), R05 12장·실습6 상황별 검수 분기(증거 먼저 고르기).
- 모든 P0의 수용 조건 R17: 드래그·그림 조작마다 숫자 입력/버튼 대안, 현재 상태 문장(aria-live), 선택 상태 속성.
- 여력이 있으면 S 난이도 P1: R07 표지 질문별 짧은 경로, R09 카드 수정 전후·작게 보기, R10 자막 실패→복구 프리셋, R15 퀴즈 오답→관련 도구 프리셋 링크.

규칙: 참고 사이트의 코드·문장·이미지를 복사하지 않고 패턴만 새로 구현. 빌드 없는 바닐라 JS. 결과는 STYLE-GUIDE대로 "숫자 하나 + 해석 한 문장". 모바일 360px에서 입력·결과·해석이 한 화면 높이 안에 가깝게 배치. 기존 장 본문 문체를 바꾸지 말 것(필요한 연결 문장만). 15장 실험실에 새 도구가 노출되게 갱신.
검증: 각 도구의 키보드만 조작, 360/375/1280px, 콘솔 오류 0, prefers-reduced-motion 시 애니메이션 축소, style_lint·check_site 통과. 결과 docs/results/phase-11.md + 도구별 GIF 대신 전/후 스크린샷 docs/results/phase-11/.
마지막에 `python3 scripts/notify.py "✅ [Phase 11 인터랙션 고도화 완료] ..." <대표 스크린샷>`.
