너는 ai-insta 프로젝트의 작업자(Codex)다. AGENTS.md, .agents/skills/guidebook-pipeline·guidebook-writing, docs/STYLE-GUIDE.md(6·7절 포함), docs/DESIGN-blog.md, docs/DESIGN.md 12절, docs/results/phase-B3·B3k·B4a·B4b·B4c·B5.md와 각 requests/glossary 파일, research-blog/(SOURCES·ai-production-blog), research/ai-models-pricing.md를 읽어라.
이번 작업은 **Phase B6. BlogBook 통합**이다. site-blog/ 공통 파일 수정 허용. 다른 책 폴더(site/, site-shorts/)와 auto-kit/은 다른 작업자가 수정 중이니 건드리지 마라. shelf/는 블로그 카드·진행 상태만. commit하지 마라.
1. requests 병합(book.js·book.css·common.js·practice.js 등). 이론 1~13장 + 실험실 + 용어집, 실습 0~10 + E2E 모두 '완성' 상태로. 이전/다음·표지 목차·본문 속 'N장/실습 N' 상호 참조 검사.
2. 부록: **프롬프트 모음**(prompts.html — 6장·실습 4·5의 복사용 프롬프트를 작업별로 모으고 좋은/나쁜 예), **AI 모델·사용처·비용 총정리**(ai-models.html — 블로그 작업 기준: 글·교정·이미지·키워드·분석 도구와 모델, 어디서 쓰나(앱·요금제·API·다른 도구 내장), 비용 체계(구독·크레딧·API 종량), 0원/저비용 조합, 글 1편당 비용 예 — research/ai-models-pricing.md와 research-blog 근거·날짜), 출처(credits.html, 실제 인용 B번호만)를 목차·표지에 연결.
3. 실험실(lab.html): 모든 장의 도구를 원본 재사용으로 모은다(scripts/build_appendices.py 방식, 필요하면 site-blog 인자 추가). 용어집: glossary 요청 병합, data-term 일치.
4. 표지: '블로그 수익화 입문서', 'AI로 무엇을 어떻게 쓰나'(도구 지도·레시피·비용 총정리) 진입, 실습편 시작 버튼, 질문별 짧은 경로(하루 1천 명이면 얼마? 어떤 플랫폼? AI 글 올려도 되나?), blog-kit 샘플 미리보기.
5. 전체 게이트: check_site(--site site-blog), style_lint, 1280/375/360px·라이트/다크·콘솔 오류·키보드, blog-kit pytest(Python 3.11). docs/results/phase-B6.md(+스크린샷), docs/PROJECT_STATE.md 갱신.
6. `python3 scripts/notify.py "✅ [B6 블로그 통합 완료] ..." <표지 스크린샷>`.
