너는 ai-insta 프로젝트의 작업자(Codex)다. AGENTS.md, .agents/skills/guidebook-pipeline·guidebook-research·guidebook-writing, docs/STYLE-GUIDE.md, **docs/DESIGN-blog.md(이번 책 설계)**, docs/DESIGN.md 12절(AI 제작 핵심 모듈), 참고용으로 research/ai-production.md·research/ai-models-pricing.md·research-shorts/BRIEFING.md(형식 참고)를 읽어라.
이번 작업은 **Phase B2. 블로그 수익화 편: 학습자 질문 목록과 자료조사**다. site/, site-shorts/, starter-kit/, shorts-kit/, research/, research-shorts/는 **수정하지 마라**. 새 파일만 research-blog/와 docs/에 만든다. commit하지 마라. 자료조사가 이 책에서 가장 중요하다: 폭넓게, 2026년 10월 현재 기준으로, 공식 출처 우선.

## 1. 학습자 질문 먼저
docs/learner-questions-blog.md: 이론 1~13장, 실습 0~10 각각 초보자가 실제로 가장 궁금해할 질문 5개. 웹 검색으로 초보 블로거가 실제로 묻는 질문(네이버 지식iN, 블로그 커뮤니티, 검색 자동완성, 애드센스/애드포스트 도움말 커뮤니티 등)을 참고하고 출처 예시를 남긴다.

## 2. Hermes 조사
RUN=/home/yonghun/project/hermes-research/output/blog-research-20261026 (queries/, raw/ 준비됨). guidebook-research Skill 명령(`-s guidebook-research --max-turns 40`), 최대 4개 병렬, **총 32회 이하**. Codex 웹 검색·직접 열람으로 보완. 반드시 포함:
- **플랫폼**(한국, 2026-10 현재): 네이버 블로그, 티스토리, 워드프레스(.com/설치형+호스팅 비용), 구글 블로거, (참고) 브런치 — 개설 비용, 광고 가능 종류, 자체 광고 정책(티스토리 자체 광고·수익 배분 변화 등), 도메인, 예약 발행, 이전 가능성, 장단점.
- **수익**: 네이버 애드포스트(신청 조건·지급 기준·수익 구조), 구글 애드센스(승인 조건·흔한 거절 사유·지급 기준·한국 RPM/CPC 신뢰할 만한 공개 자료·2024년 노출 기준 지급 전환 등 변경), 카카오 애드핏, 네이버 쇼핑커넥트/브랜드커넥트, 쿠팡 파트너스(수수료율·최소 지급·대가성 문구), 기타 제휴(링크프라이스 등), 체험단·협찬 구조, 내 상품(전자책 등). "하루 방문자 N명이면 한 달 얼마"를 계산할 근거(페이지뷰/방문, RPM 범위)와 과장 사례 구분.
- **검색(SEO)**: 네이버 검색의 블로그 품질 판단(공식 설명된 C-Rank, D.I.A.(+) 등), 저품질·누락 관련 네이버 공식 안내, 네이버 서치어드바이저, 네이버의 AI 생성 글에 대한 공식 입장·정책; Google 검색 센터의 AI 생성 콘텐츠 안내, 스팸 정책(대량 생성 콘텐츠 남용 scaled content abuse, 사이트 평판 악용), 유용한 콘텐츠 기준, AI 개요(AI Overviews)·AI 모드가 블로그 유입에 미친 영향 자료, Search Console 등록.
- **AI 글쓰기·제작 도구(작업별 실제 서비스)**: 리서치·초안(ChatGPT, Gemini, Claude, Perplexity, 뤼튼 등 한국 서비스, 네이버 블로그 자체 AI 기능이 있다면 그 이름과 범위), 교정·맞춤법, 이미지·썸네일(ChatGPT 이미지, Gemini, Canva, 미리캔버스, Firefly 등), 키워드 도구(네이버 검색광고 키워드 도구, 네이버 데이터랩, Google Trends, Keyword Planner, 유료 도구는 이름만) — 무료 한도, 가격(원화/달러, 날짜), 한국어 품질, 상업 이용, 블로그 이용 시 표시 의무. research/ai-production.md·ai-models-pricing.md에 있는 것은 재사용하고 블로그 관점 차이만 추가.
- **AI 글 제작 과정(워크플로)**: 공식 가이드(Google의 AI 콘텐츠 안내, OpenAI/Anthropic/Google의 프롬프트 가이드)와 신뢰할 만한 튜토리얼에서 정보 글·후기 글·경험 글을 AI로 만드는 실제 단계, 사람이 반드시 해야 하는 일(경험·사실 확인), 흔한 실수, 소요 시간.
- **자동화·API**: 티스토리 Open API 현황(종료 여부·날짜), 네이버 블로그 글쓰기 API 현황, Blogger API v3 posts.insert(OAuth·할당량), WordPress REST API + 애플리케이션 비밀번호, 각 플랫폼 예약 발행 기능, 자동 발행 시 정책 위험.
- **정책·법**: 공정거래위원회 추천·보증 등에 관한 표시·광고 심사지침(2024 개정 포함, 표시 위치·문구), 쿠팡 파트너스 문구 의무, 저작권(이미지·뉴스 인용·AI 생성물), 애드센스 프로그램 정책(무효 클릭·콘텐츠 정책), 네이버 블로그 운영정책.
- **세금**: 애드센스·애드포스트·제휴 수입의 한국 세금 처리(종합소득세, 사업자 등록 필요 여부 기준, 미국 세금 정보 제출) — 국세청 등 공식 출처.
- **오늘 기준 절차(메뉴 이름, 한국어 UI)**: 네이버 블로그 개설·스마트에디터로 글쓰기·발행(PC/모바일), 티스토리 개설·글쓰기·발행, 애드포스트 신청, 애드센스 신청, 쿠팡 파트너스 가입, 서치어드바이저·Search Console 등록. 화면 JS 렌더링으로 확인이 어려우면 "보통 이런 이름" + 공식 도움말 링크로 남긴다.
- **한국 사례**: 블로그 수익 공개 사례(유형·기간·금액, 신뢰도 구분).

## 3. 산출물
Hermes 원응답 품질 점검(403·빈 응답 세기, exit 0 ≠ 성공), 공식 출처 15개 이상 직접 확인.
- research-blog/<topic>.md(주제별 노트), research-blog/SOURCES.md(번호 B###), research-blog/FACT-SHEET.md(ID 접두어 BL-), research-blog/QUESTION-MAP.md(학습자 질문 → 근거 사실), research-blog/BRIEFING.md(쇼츠 편 BRIEFING과 같은 형식 + "인스타·쇼츠 편과 다른 점"), research-blog/ai-production-blog.md(작업별 추천 도구 표, **"처음엔 이것 하나"**, 무료로 끝까지 가는 조합 1개·월 1~3만 원 조합 1개, 레시피 B1~B3의 단계·입력·출력·시간·비용, 프롬프트 공식과 예시, 흔한 실수, 상충·미확인).
- 결과 docs/results/phase-B2.md(질의 품질표 포함). 조사 결과로 DESIGN-blog.md 목차·키트 조정이 필요하면 여기에 제안(설계서는 Claude가 고친다). 특히 **API 자동 발행이 실제로 가능한 플랫폼**과 **실습 7의 기본 플랫폼 추천**을 결론으로 적는다.
- `python3 scripts/notify.py "✅ [블로그 편 조사 완료] ..." research-blog/BRIEFING.md`로 한국어 보고.
