너는 ai-insta 프로젝트의 작업자(Codex)다. AGENTS.md, .agents/skills/guidebook-research, docs/DESIGN.md 12절, **research/ai-production.md(R3 결과)**, docs/results/phase-R3.md를 읽어라.
이번 작업은 **Phase R3b. AI 모델 × 사용처 × 비용 체계 총정리**다. 사용자 요청(원문): "어떤 모델을 어디서 사용할 수 있는지, 비용 체계는 어떻게 되는지 싹다 정리해줘." site/·site-shorts/·키트는 건드리지 마라. commit하지 마라.

Hermes RUN=/home/yonghun/project/hermes-research/output/ai-production-research-20261026 (queries/r3b-*, raw/r3b-*), `-s guidebook-research`, `--max-turns 40`, 최대 4개 병렬, **총 24회 이하**. Codex 웹 검색과 공식 가격 페이지 직접 열람으로 반드시 교차 확인한다. 2026-10-26 기준.

정리 단위는 **모델**이다(서비스 이름만으로 끝내지 않는다). 범주별로 2026년 10월 현재 주요 모델을 빠짐없이:
- 텍스트(LLM): OpenAI GPT 계열(ChatGPT 앱의 무료/Plus/Pro에서 쓰는 모델과 API 모델), Anthropic Claude 계열, Google Gemini 계열, Perplexity, 네이버 HyperCLOVA X 등.
- 이미지: OpenAI 이미지 모델(ChatGPT·API), Google 이미지 모델(Gemini 앱·AI Studio·Vertex·Whisk 등), Midjourney 버전, Ideogram, Adobe Firefly 모델, FLUX, Stable Diffusion 계열, Canva·미리캔버스 내장 모델.
- 영상: Google Veo 버전(Gemini 앱·Flow·YouTube Shorts/Create·Vertex AI·Gemini API), OpenAI Sora 버전(앱·ChatGPT·API), Kling 버전, Runway Gen 버전, Hailuo/MiniMax, Pika, Luma, Seedance 등.
- 음성: ElevenLabs 모델, 타입캐스트, 클로바더빙/클로바 보이스, OpenAI TTS, Google TTS/Gemini TTS.
- 음악: Suno 버전, Udio, Google Lyria(어디서), YouTube 오디오 보관함(무료).
- 편집 앱 내장 AI: CapCut(어떤 생성 모델·자동 자막), Vrew, YouTube Create.

모델마다 표 한 줄: 모델명·버전 / 만든 회사 / **어디서 쓸 수 있나**(앱·웹 서비스, 포함 요금제, API·플랫폼, 다른 도구 내장) / **한국에서 사용 가능?** / **비용 체계**(무료 한도 · 구독 요금제별 포함량 · 크레딧 단가 · API 종량 요금 예: 이미지 1장당, 영상 1초당, 100만 토큰당, 음성 1천 자당) / 출력 규격(최대 길이·해상도·세로 비율·음성 포함) / 상업 이용 조건 / 워터마크·AI 표시(SynthID·C2PA) / 확인일·출처.
그리고:
- **비용 체계 해설**: 구독형·크레딧형·종량형(API)·번들형(다른 구독에 포함)의 차이와, 같은 모델이 사용처마다 가격·한도가 다른 이유. 원화 환산 예(환율 기준일 명시).
- **실전 비용 시나리오**: 뉴스카드 1세트, 30초 해설 릴스 1편, 8초×4클립 AI 영상 쇼츠 1편을 무료 조합·저비용 조합·고품질 조합으로 만들 때 대략 비용(계산식 공개).
- 상충·미확인 목록.

산출물: research/ai-models-pricing.md(위 표 전체 + 해설 + 시나리오), research/SOURCES.md·FACT-SHEET.md(AIM-*) 보강, research-shorts에 쇼츠 관련 항목 반영, docs/results/phase-R3b.md. 공식 가격/요금 페이지 15개 이상 직접 확인.
마지막에 `python3 scripts/notify.py "✅ [R3b AI 모델·사용처·비용 총정리 완료] ..." research/ai-models-pricing.md`로 한국어 보고.
