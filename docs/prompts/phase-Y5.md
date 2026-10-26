너는 ai-insta 프로젝트의 작업자(Codex)다. AGENTS.md, .agents/skills/guidebook-pipeline·guidebook-writing, docs/STYLE-GUIDE.md, docs/DESIGN-shorts.md, docs/DESIGN.md 12절, docs/results/phase-Y4a·Y4b·Y4c·Y4k·Y4p·Y4ai.md와 각 requests/glossary 파일을 읽어라.
이번 작업은 **Phase Y5. ShortsBook 통합**이다. site-shorts/ 공통 파일 수정 허용. **site/, shelf/는 다른 작업자가 수정 중이니 건드리지 마라.** commit하지 마라.
1. requests 병합(book.js·book.css·common.js·practice.js). 새 장 'AI 도구 지도'(02b-ai-tools.html)를 3장으로 넣고 이후 번호를 하나씩 미룬다(파일 slug 유지, book.js 번호·제목·이전/다음·표지 목차·본문/퀴즈 속 'N장' 상호 참조 모두 갱신). 이론 1~15장 + 실험실 + 용어집, 실습 0~10 + E2E 모두 '완성' 상태로.
2. 부록: 프롬프트 모음(prompts.html), AI 모델·사용처·비용 총정리(ai-models.html), 출처(credits.html, 실제 인용 Y번호만)를 목차·표지에 연결.
3. 실험실(lab.html): 모든 장의 도구를 원본 재사용으로 모은다(ReelsBook의 scripts/build_appendices.py 방식 참고, 필요하면 site-shorts용 인자 추가). 용어집(glossary.html): glossary 요청 병합, data-term 일치.
4. 표지: '영상 제작에 집중한 쇼츠 입문서', 'AI로 무엇을 어떻게 만드나'(도구 지도·레시피·비용 총정리) 진입, 실습편 시작 버튼, 질문별 짧은 경로, shorts-kit 샘플 미리보기.
5. 전체 게이트: check_site(site-shorts), style_lint, 1280/375/360px·다크·콘솔 오류·키보드, shorts-kit pytest. docs/results/phase-Y5.md(+스크린샷).
6. `python3 scripts/notify.py "✅ [Y5 쇼츠 통합 완료] ..." <표지 스크린샷>`.
