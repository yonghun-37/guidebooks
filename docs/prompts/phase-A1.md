너는 ai-insta 프로젝트의 작업자(Codex)다. AGENTS.md, .agents/skills/guidebook-pipeline·guidebook-research, docs/STYLE-GUIDE.md, **docs/DESIGN-advanced.md(이번 작업 설계)**, docs/DESIGN.md 12절, 그리고 이미 있는 근거 research/(api-*·practice-instagram·ai-production·ai-models-pricing 등 API·비용 관련 노트), research-shorts/(API·업로드 노트), starter-kit/publish.py, shorts-kit/upload.py를 읽어 **이미 조사된 것은 재사용하고 빈 곳만 조사**한다.
이번 작업은 **Phase A1. 심화편(API 완전 자동화) 자료조사** 다. 다른 작업자가 research-blog/, site*/, *-kit/을 수정 중이니 **새 폴더 research-advanced/와 docs/results/phase-A1*.md만** 만든다. 기존 research/·research-shorts/는 수정하지 마라. commit하지 마라.

Hermes RUN=/home/yonghun/project/hermes-research/output/advanced-research-20261026 (queries/, raw/ 준비됨), `-s guidebook-research --max-turns 40`, **동시에 최대 3개**(다른 조사 작업이 함께 돈다), **총 28회 이하**. Codex 웹 검색·공식 문서 직접 열람으로 보완. 모두 **2026년 10월 현재** 기준, 공식 개발자 문서 우선, 문서 날짜·버전 기록.

## 조사 항목
1. **Instagram 게시 API**: Instagram API with Instagram Login vs Facebook Login 차이와 지금 권장 경로, 필요한 계정 종류(프로페셔널: 비즈니스/크리에이터), Meta 앱 생성·사용 사례·권한(instagram_business_content_publish 등)·앱 검수/비즈니스 인증이 본인 계정 게시에 필요한지(개발 모드로 본인 계정만 쓰는 경우), 토큰 종류·수명·갱신, 컨테이너 생성→상태 확인→media_publish 흐름(이미지·캐러셀·릴스·스토리), 미디어 요건(형식·비율·길이·용량), **공개 URL 필요 여부**와 대안(resumable upload 지원 여부), 게시 한도(24시간 100 vs 50 상충 정리 — content_publishing_limit 엔드포인트), 오류 코드, 인사이트 API 지표와 지연. API로 AI 표시·음악·협찬 표시가 가능한지.
2. **YouTube Data API v3**: OAuth(데스크톱 앱), 동의 화면 테스트 모드의 토큰 만료(7일 등), videos.insert 할당량 비용과 기본 일일 할당량, 2020-07-28 이후 미검증 프로젝트 업로드 비공개 잠금과 감사 절차(신청서·소요), 재개 업로드, 쇼츠 판정, status 필드(privacyStatus·publishAt 예약·selfDeclaredMadeForKids·containsSyntheticMedia 등 AI 공개 필드 존재 여부와 이름), 썸네일 API 제약, YouTube Analytics API 지표.
3. **생성 API(가격·제한, 날짜)**: LLM(OpenAI·Gemini·Anthropic — 구조화 출력/JSON 스키마 기능 이름, 무료 등급 여부, 지출 한도 설정 방법), 이미지 생성 API(OpenAI 이미지, Gemini/Imagen 등), TTS API(Google Cloud TTS·OpenAI TTS·ElevenLabs·타입캐스트 API — 한국어), 영상 생성 API(Gemini API의 Veo, Runway API, 기타 한국에서 결제 가능한 것) — research/ai-models-pricing.md에 있으면 재사용. 각 API의 **지출 상한·예산 알림** 설정 위치.
4. **실행·호스팅**: GitHub Actions 예약 실행(cron 최소 간격·지연·공개 저장소 무료 분량·비공개 한도·비밀 저장 Secrets), Windows 작업 스케줄러·macOS launchd 기본, 인스타용 공개 이미지/영상 URL을 무료로 만드는 선택지(GitHub Pages 공개 저장소의 주의점, Cloudflare R2·Google Cloud Storage 등 무료 등급과 조건), ffmpeg 배포 방식.
5. **노코드 자동화**: n8n(셀프 호스팅 무료/클라우드 가격, Instagram·YouTube·OpenAI 노드 존재 여부), Make, Zapier — 가격·무료 분량·인스타/유튜브 게시 지원 여부, 한국 사용자 사례.
6. **승인 알림**: 디스코드 웹훅/봇, 텔레그램 봇 — 무료, 버튼(인터랙션) 승인 가능 여부와 간단한 대안.
7. **정책·안전**: Meta 플랫폼 약관·자동화 관련 커뮤니티 가이드(스팸·비진정성 행동), API 게시물의 도달 차이 여부(공식 언급이 있을 때만), YouTube 스팸·반복 콘텐츠·재사용 콘텐츠 수익화 정책과 AI 대량 생성 채널 사례(2025~2026 정책 변화), AI 표시 의무와 API로 하는 법, 토큰 유출 시 조치.
8. **실무 사례**: 공개된 자동화 파이프라인 사례(오픈소스 저장소, 공식 블로그) — 구조·비용·운영 문제, 실패 사례.

## 산출물
- research-advanced/<topic>.md, research-advanced/SOURCES.md(번호 A###), research-advanced/FACT-SHEET.md(ID ADV-), research-advanced/BRIEFING.md: ① 인스타 자동화 결론(권장 API 경로, 필요한 준비물 목록, 한도, 공개 URL 해법) ② 쇼츠 자동화 결론(감사 전/후 차이, 할당량으로 하루 몇 편) ③ 생성 API 추천 조합과 **편당·월 비용표**(인스타 카드 매일 1편, 쇼츠 매일 1편; 저비용/고품질) ④ 실행 방식 추천(로컬 vs GitHub Actions vs n8n) ⑤ 승인 방식 추천 ⑥ 위험과 회피 ⑦ 상충·미확인과 사용자가 직접 확인할 방법.
- docs/learner-questions-advanced.md: A0~A9 장마다 초보 개발자 질문 5개(실제 커뮤니티·개발자 포럼 질문 참고).
- 결과 docs/results/phase-A1.md(질의 품질표, 403·빈 응답 수), DESIGN-advanced.md 조정 제안(설계서는 Claude가 고친다).
- `python3 scripts/notify.py "✅ [심화편 조사 완료] ..." research-advanced/BRIEFING.md`로 한국어 보고.
