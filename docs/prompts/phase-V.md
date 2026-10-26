너는 ai-insta 프로젝트의 작업자(Codex)다. AGENTS.md, .agents/skills/guidebook-writing·guidebook-pipeline, **docs/STYLE-GUIDE.md(특히 6절 시각자료 기준 — 이번 작업의 기준, 방금 수정됨)**, __DESIGN__, 그리고 __BOOKDIR__ 전체를 읽어라.
사용자 지시(원문): "억지로 이미지를 늘릴 필요는 없고 시각자료가 있으면 좋은 내용은 적극적으로 활용하라." 이번 작업은 **Phase __PHASE__. __BOOK__ 시각자료 보강(재시작)** 이다.

**중요: 이전 작업자가 "페이지마다 최소 개수" 기준으로 작업하다 중단됐다.** `git diff -- __BOOKDIR__ __EXTRA_PATHS__`와 새로 생긴 파일(`git status --short`)을 먼저 검토하라. 6.1에 해당하는 좋은 그림은 살리고, 개수를 채우려는 그림·본문 반복 그림·장마다 의무로 넣은 장식/인물 삽화는 제거한다. 쓰지 않게 된 이미지 파일도 지운다.

담당: `__BOOKDIR__/` 전체(공통 파일 포함 이 작업자만 수정)__EXTRA__. 다른 책 폴더·키트·research·docs/STYLE-GUIDE.md는 수정하지 마라. commit하지 마라.

1. 페이지마다 "그림이 있으면 훨씬 잘 이해될 내용"을 STYLE-GUIDE 6.1 표 기준으로 찾아 목록을 docs/results/phase-__PHASE__-plan.md에 적는다(페이지, 내용, 그림 종류, 이유). 그 목록대로만 만든다.
2. 공통 그림 컴포넌트(figure 스타일, 화면 위치 그림용 SVG 틀·번호 동그라미, 단계 띠, 2칸 비교, 차트 기본 스타일, 라이트/다크)를 assets에 정리한다.
3. 그림 숫자는 본문과 같은 근거, 캡션에 출처 각주. 서비스 화면 캡처·로고 따라 그리기 금지. 기존 인터랙션·본문 내용은 유지(그림을 가리키는 문장 정도만 추가). AI 생성 예시는 프롬프트와 함께 "AI 생성 예시" 표시.
4. __CHECK__
5. 검증: style_lint, check_site(__BOOKDIR__), 1280/375/360px × 라이트/다크(그림 글자 가독·가로 넘침 없음), 콘솔 오류. 스크린샷 docs/results/phase-__PHASE__/.
6. 결과 docs/results/phase-__PHASE__.md(추가·유지·제거한 그림 목록), `python3 scripts/notify.py "🖼️ [__PHASE__ 완료] ..." <대표 스크린샷 2장>`.
