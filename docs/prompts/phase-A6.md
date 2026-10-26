너는 ai-insta 프로젝트의 작업자(Codex)다. AGENTS.md, .agents/skills/guidebook-writing·guidebook-pipeline, docs/STYLE-GUIDE.md(6·7절 포함), docs/DESIGN-advanced.md, **docs/results/phase-A5r-findings.md·phase-A5r-scorecard.md(이번 작업의 입력)**, research-advanced/, auto-kit/, site/advanced/, site-shorts/advanced/를 읽어라.
이번 작업은 **Phase A6. 심화편 독립 검토 수정 + 최종 게이트** 다. 담당: auto-kit/, site/advanced/와 그 전용 assets, site-shorts/advanced/와 그 전용 assets, research-advanced/(근거 추가 시), docs/learner-questions-advanced.md. commit하지 마라. 유료 키·실계정 사용 금지.

1. A5r의 16건(차단 4·혼란 10·사소 2)을 모두 고친다. 키트 결함(F03 인코딩, F04 결과 선택, F05 오류 잔존, F07 사후 확인 시작점, F09 토큰 우선순위, F10 장면 수)은 코드와 테스트로 고치고, 책 본문은 실제 출력과 일치시킨다. 특히:
   - F01: 인스타 공개 호스팅을 실제로 연결하는 끝까지의 절차(A1 결론의 무료 선택지, 계정 생성 → 버킷/저장소 → 키 → .env → doctor 확인 → 공개 URL 열어 보기) + 화면 위치 그림.
   - F02·F08: 권장 TTS 키와 디스코드/텔레그램 자격을 어디서 만들고 어디에 넣는지 단계별 + 화면 위치 그림, 수신 운영(누가 언제 무엇을 누르나).
   - F06: 예외 대기열에서 고친 항목을 재검사·완료하는 실습.
   - F11: 전자동 전환 기준을 두 책·키트에서 하나로 통일.
   - F13: "무료 모델로 매일 가능한가"에 근거 있는 직답(무료 등급 한도·조건·대안).
   - F14: 게시할 만한 완성 견본 — mock이 아닌 '사람이 다듬은 완성 예'를 키트 샘플로(인스타 카드 세트, 쇼츠 1편), STYLE-GUIDE 7절 예시.
2. 게이트: auto-kit pytest(Python 3.11, 깨끗한 복사본에서 README 명령 재현), style_lint, check_site(site, site-shorts), 1280/375/360 × 라이트/다크·콘솔·키보드.
3. 결과 docs/results/phase-A6.md(발견별 처리 표), docs/PROJECT_STATE.md 갱신, `python3 scripts/notify.py "✅ [A6 심화편 수정·게이트 완료] ..."`.
