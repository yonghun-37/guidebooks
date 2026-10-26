너는 ai-insta 프로젝트의 작업자(Codex)다. AGENTS.md, .agents/skills/guidebook-writing·guidebook-pipeline, docs/STYLE-GUIDE.md, docs/DESIGN.md 12절, docs/results/phase-R-shorts-findings.md를 읽어라.
이번 작업은 **ShortsBook 검토 반영과 최종 게이트**다. site-shorts/와 shorts-kit/만 수정한다(다른 책 파일은 다른 작업자가 수정 중). commit하지 마라.
1. 차단·혼란은 모두, 사소는 합리적 범위에서 고친다. 고치지 않은 항목은 이유를 남긴다.
2. 최종 게이트: check_site(site-shorts), style_lint, 1280/375/360px·다크·콘솔 오류·키보드, shorts-kit 테스트. 결과 docs/results/phase-F-shorts.md(게이트 표 + 항목별 해결).
3. `python3 scripts/notify.py "✅ [ShortsBook 최종 수정 완료] ..."`.
