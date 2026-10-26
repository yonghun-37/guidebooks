너는 ai-insta 프로젝트의 작업자(Codex)다. AGENTS.md, .agents/skills/guidebook-writing·guidebook-pipeline, **docs/STYLE-GUIDE.md(특히 6절 시각자료 기준 — 이번 작업의 기준)**, docs/DESIGN.md, 그리고 site 전체(assets와 모든 chapters/·practice/·부록 페이지)를 읽어라.
사용자 지시(원문): "전반적으로 교과서에 시각자료좀 많이 넣어". 이번 작업은 **Phase V-insta. ReelsBook(인스타) 시각자료 보강** 이다. 담당: `site/` 전체(공통 파일 포함 이 작업자만 수정), 그리고 scripts/check_site.py(이 작업자만 수정). 다른 책 폴더·키트·research·docs/STYLE-GUIDE.md는 수정하지 마라. 다른 작업자가 research-blog/·research-advanced/를 만들고 있다. commit하지 마라.

1. 먼저 페이지별 현재 그림 수와 STYLE-GUIDE 6.1 최소 기준 대비 부족분 표를 docs/results/phase-V-insta-before.md에 만든다.
2. 공통 그림 컴포넌트(figure 스타일, 그림 번호, 화면 위치 그림용 SVG 틀·번호 동그라미·강조, 단계 띠, 좋은/나쁜 비교 2칸, 차트 기본 스타일, 라이트/다크 변수)를 assets에 만든다. 재사용 가능한 SVG는 `assets/img/fig/`.
3. 인물 기준 시트: 하린·정 선배(ReelsBook), 그리고 다른 책이 같은 방식을 쓰도록 기준 시트 만드는 법을 docs/results/phase-V-insta.md에 기록의 같은 그림체 기준 이미지(이미지 생성 기능)를 만들고 `assets/img/characters/`에 저장, 이를 기준으로 장 머리 대화 삽화를 만든다(장마다 1장, WebP 400KB 이하, "AI 생성 삽화" 표시는 크레딧 페이지에 일괄).
4. 모든 이론 장·실습 장·E2E·부록·표지에 6.1 기준만큼 **내용을 전달하는** 그림을 추가한다. 본문 숫자(수익·비용·조건·한도)는 차트로, 흐름은 도식으로, 앱 조작 단계는 직접 그린 화면 위치 그림으로, AI 제작 레시피는 단계 띠와 AI 생성 예시(입력 프롬프트 → 결과)로. 본문 근거와 같은 숫자만 쓰고 캡션에 출처 각주. 서비스 화면 캡처·로고 따라 그리기 금지. 기존 인터랙션·본문 내용은 유지(그림을 가리키는 문장 정도만 추가).
5. scripts/check_site.py에 STYLE-GUIDE 6.1 그림 최소 기준 검사(페이지 종류별: chapters/ 6, practice/ 단계 수의 절반 이상, advanced/ 5)와 figure의 figcaption·img alt 누락 검사를 추가하되 `--site site-shorts`·`--site site-blog`에도 동작하게 하고, 기준 미달은 오류가 아닌 경고 옵션(`--fig-warn`)도 둔다.
6. 검증: style_lint, check_site(site, 새 그림 기준 포함), 1280/375/360px × 라이트/다크(그림 글자 가독·가로 넘침 없음), 콘솔 오류, 페이지 이미지 합계 1.5MB 이하. 스크린샷(대표 이론 장·실습 장·심화와 무관한 페이지 각 3폭) docs/results/phase-V-insta/.
7. 결과 docs/results/phase-V-insta.md(페이지별 그림 수 전후 표, 이미지 용량 합계), `python3 scripts/notify.py "🖼️ [V-insta 완료] ..." <대표 스크린샷 2장>`.
