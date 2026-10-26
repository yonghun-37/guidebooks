너는 ai-insta 프로젝트의 작업자(Codex)다. AGENTS.md, .agents/skills/guidebook-pipeline·guidebook-research·guidebook-writing, docs/STYLE-GUIDE.md, **docs/DESIGN-shorts.md**, docs/reference-analysis-books.md 8절을 읽어라.
이번 작업은 **Phase Y2. 유튜브 쇼츠 편: 학습자 질문 목록과 자료조사**다. 인스타 편 파일(site/, starter-kit/, research/의 기존 파일)은 다른 작업자가 수정 중이니 **건드리지 마라**. 새 파일만 research-shorts/와 docs/에 만든다. commit하지 마라.

1. **학습자 질문 먼저**: docs/learner-questions-shorts.md에 이론 1~14장, 실습 0~10 각각 초보자가 실제로 가장 궁금해할 질문 5개. 웹 검색으로 초보 유튜버들이 실제로 묻는 질문(커뮤니티·검색 자동완성·유튜브 도움말 커뮤니티 등)을 참고하고 출처 예시를 남긴다.
2. **Hermes 조사**: RUN=/home/yonghun/project/hermes-research/output/shorts-research-20261026 (queries/, raw/). guidebook-research Skill 명령(-s guidebook-research, --max-turns 40), 최대 4개 병렬, **총 28회 이하**. 위 질문에 답할 재료를 모은다. 반드시 포함:
   - 쇼츠 사양(최대 3분, 9:16, 해상도·프레임 권장, 업로드 시 쇼츠 판정 조건), 쇼츠 피드 노출 원리 공식 설명
   - 수익: YPP 자격(팬 펀딩 단계와 광고 수익 단계의 구독자·시청 기준), 쇼츠 광고 수익 공유 구조(크리에이터 풀 45%), 한국 기준 대략적 RPM 공개 자료(신뢰 출처만), 쇼핑 제휴 등 한국 가용성
   - 정책: 재사용 콘텐츠·반복 콘텐츠 수익화 제한, AI 생성·변형 콘텐츠 표시(변경/합성 콘텐츠 공개) 기준, 아동용 설정, 커뮤니티 가이드, 저작권(Content ID, 오디오 라이브러리, 쇼츠 음악 사용 조건), 2025~2026 변경
   - 제작 도구: 무료 편집(CapCut 데스크톱/모바일, DaVinci Resolve, YouTube Create, Clipchamp 등)의 한국 가용·가격·워터마크·상업 이용 조건, TTS·음성(한국어), 자동 자막, AI 영상 생성(Veo의 쇼츠 통합 등, 한국 가용·표시 의무), 무료 영상·음악 소재 라이선스(YouTube 오디오 라이브러리, Pexels, Pixabay 등)
   - 제작 기술: 첫 3초 훅, 컷 길이, 자막 크기·위치, 시청 지속률 관련 공식 크리에이터 가이드(YouTube Creators, Creator Academy 후속)
   - 업로드 절차(오늘 기준): YouTube Studio PC 업로드와 모바일 앱 쇼츠 업로드의 단계별 메뉴 이름(한국어 UI), 제목·설명·해시태그, 공개 범위·예약, AI 표시 체크 위치, 쇼츠 썸네일/표지 선택
   - API: YouTube Data API v3 videos.insert 할당량 비용, 기본 일일 할당량, 2020-07-28 이후 생성된 미검증 API 프로젝트 업로드의 비공개 잠금 정책과 감사(audit) 절차, OAuth 동의 화면 테스트 사용자, 쇼츠로 인식시키는 조건
   - 분석 지표: 쇼츠의 조회수 집계 변경(2025-03 조회수 정의 변경 등), 시청함/스와이프 비율, 평균 시청 지속률
   - 한국 사례: 쇼츠로 성장한 한국 채널 유형과 공개 수익 사례(과장 구분)
3. Hermes 원응답 품질 점검(403 등), 공식 출처 10개 이상 직접 확인. 산출물: research-shorts/<topic>.md, research-shorts/SOURCES.md(번호 Y###), research-shorts/FACT-SHEET.md(ID 접두어 YT-), research-shorts/BRIEFING.md(인스타 편 BRIEFING과 같은 8절 + "인스타 편과 다른 점"), 결과 docs/results/phase-Y2.md.
4. 조사 결과로 DESIGN-shorts.md 목차 조정이 필요하면 docs/results/phase-Y2.md에 제안(설계서는 Claude가 고친다).
5. `python3 scripts/notify.py "✅ [쇼츠 편 조사 완료] ..." research-shorts/BRIEFING.md`로 한국어 보고.
