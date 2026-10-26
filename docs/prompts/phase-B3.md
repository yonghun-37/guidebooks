너는 ai-insta 프로젝트의 작업자(Codex)다. AGENTS.md, .agents/skills/guidebook-pipeline·guidebook-writing, **docs/STYLE-GUIDE.md(최우선)**, **docs/DESIGN-blog.md**, docs/DESIGN.md 12절, docs/learner-questions-blog.md, research-blog/(BRIEFING·FACT-SHEET·SOURCES·QUESTION-MAP·ai-production-blog와 주제 노트), docs/results/phase-B2.md(설계 조정 제안), **docs/DESIGN-blog.md 11절(B2 반영 결정·예시 — 우선)**, docs/reference-analysis-books.md 8절을 읽어라. 그리고 가장 최근에 완성된 ShortsBook(site-shorts/)의 구조(assets/book.css·book.js·common.js·practice.js·catalog.js·glossary.js·lab.js, chapters/02-revenue.html, chapters/02b-ai-tools.html, practice/08-publish.html, prompts.html, ai-models.html)를 기준 구현으로 삼는다.
이번 작업은 **Phase B3. BlogBook 뼈대 + 샘플 2개** 다. 전체 집필은 하지 않는다. site/, site-shorts/, starter-kit/, shorts-kit/는 수정하지 마라(blog-kit/는 다른 작업자가 동시에 만든다 — 건드리지 마라). commit하지 마라.

1. 뼈대: `site-blog/`에 BlogBook을 만든다. ShortsBook 공통 자산을 복사해 재사용하되 책 이름("BlogBook: AI로 쓰는 블로그 수익화 입문"), 색 테마(블로그 편임을 알 수 있되 네이버·티스토리·구글 로고·브랜드 자산 복제 금지), 장 데이터(DESIGN-blog 4·5절 + B2 제안 중 타당한 것 반영, 상태 '준비중'), 인물(수아·태오)을 바꾼다. 쇼츠 전용 자산(영상 타임라인 등)은 가져오지 않는다. 표지(index.html)에 이론/실습 두 트랙과 "오늘 첫 글 발행까지: 실습편 시작" 버튼.
2. 배포: .github/workflows/pages.yml에 `cp -r site-blog _site/blog` 추가, shelf/index.html에 BlogBook 카드(경로 blog/), shelf/progress/index.html에 블로그 편 진행 상태 추가, README.md 표에 한 줄.
3. **샘플 A — (이론) 2장 "블로그는 무엇으로 돈을 버나"**: STYLE-GUIDE 2절 틀 그대로. 첫 질문 "하루 방문자 1천 명이면 한 달 얼마?"에 research-blog 근거로 직답(계산식 공개). 축: ① 광고(애드포스트/애드센스, 플랫폼별) ② 제휴(쿠팡 파트너스·쇼핑커넥트 등) ③ 협찬·체험단 ④ 내 상품. 축마다 정의 → 흐름 → 얼마 → 조건 → 언제부터 → 지금 할 일 + 확인할 점. 단계표: 개설 → 글 수·운영 기간·방문자 단계별로 신청 가능한 수익 장치. 해 보기: 방문자×페이지/방문×RPM 참고치 + 제휴 전환 계산기(가상·참고 표시, 내 값으로 바꿔 넣기).
4. **샘플 B — (실습) 7 "첫 글 실제로 발행하기"**: 네이버 블로그 / 티스토리 탭(B2 결론의 기본 플랫폼을 첫 탭), PC/모바일. 발행 설정(카테고리·공개 범위·태그·대가성 문구 위치·예약), 발행 후 모바일 확인, 주소 기록, 수정·삭제 방법. 앱 버튼 표준 안내 문구("버튼 이름은 앱 버전에 따라 조금 다를 수 있어요…"), 직접 그린 도식 SVG.
5. 샘플 인터랙션 1개 완성: A의 수익 계산기 또는 B의 "발행 전 체크 분기"(제휴 링크/협찬/AI 이미지/남의 사진 여부 → 필요한 표시·조치).
6. 모든 정책·수치는 research-blog FACT-SHEET 근거와 [B###] 각주. 근거 없는 숫자 금지. 사실 ID·내부 용어 본문 금지.
7. 검증: scripts/style_lint.py와 scripts/check_site.py를 site-blog에도 쓸 수 있게(인자 추가, 기존 동작 유지) 하고 실행, 1280/375/360px·라이트/다크·콘솔 오류·키보드. 스크린샷 docs/results/phase-B3/.
8. docs/results/phase-B3.md(인물 설정·결정 사항·공통 자산 목록), `python3 scripts/notify.py "📝 [블로그 편 샘플 준비] ..." <샘플 A 스크린샷>`.
- **시각자료**: docs/STYLE-GUIDE.md 6절 — 개수 기준 없음. 흐름·숫자·선택지 비교·화면 위치·결과 예시·구조처럼 그림이 더 잘 전달하는 내용은 적극적으로 그림으로, 장식·개수 채우기는 하지 않는다.
- **예시**: docs/STYLE-GUIDE.md 7절 — 실제로 사람들이 보고 읽을 만한 소재로 예시를 정해 장을 관통시킨다(설명용 인위적 소재 금지, 실존 브랜드·지어낸 성과 숫자 금지). 인스타·쇼츠 편의 새 예시(출근길 3분 생활 뉴스 / 자취생 10분 생존법)와 어울리게 한다.
