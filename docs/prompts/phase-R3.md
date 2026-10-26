너는 ai-insta 프로젝트의 작업자(Codex)다. AGENTS.md, .agents/skills/guidebook-research·guidebook-pipeline, **docs/DESIGN.md 12절(AI 제작 핵심 모듈)**, docs/DESIGN-shorts.md, research/ai-tools-pricing.md·ai-text-image-tools.md·ai-video-voice-tools.md, research-shorts/07-editors.md·08-voice-captions.md·09-ai-video.md를 읽어라.
이번 작업은 **Phase R3. AI 제작 도구와 제작 과정 집중 조사(두 책 공통)** 다. 사용자 지적: "정확히 어떤 서비스·TOOL을 이용하고 어떤 과정으로 AI 콘텐츠를 만드는지가 가장 중요한데 빠져 있다." site/, site-shorts/, starter-kit/, shorts-kit/는 다른 작업자가 수정 중이니 건드리지 마라. commit하지 마라.

Hermes RUN=/home/yonghun/project/hermes-research/output/ai-production-research-20261026 (queries/, raw/ 준비됨), `-s guidebook-research`, `--max-turns 40`, 최대 4개 병렬, **총 30회 이하**. Codex 웹 검색으로 보완. 모든 결과는 **2026년 10월 현재** 기준.

조사 항목(작업별로 실제 서비스 이름을 구체적으로):
1. 리서치·팩트체크·요약: ChatGPT, Claude, Gemini, Perplexity, 네이버 클로바X/큐(Cue:) 등 — 무료 등급 한도, 한국어 품질, 웹 검색·출처 표시, 뉴스 요약에 쓰는 법.
2. 이미지 생성: ChatGPT 이미지 생성, Gemini(이미지 생성/편집), Midjourney, Ideogram(글자 렌더링), Adobe Firefly(상업 안전), Canva AI, 미리캔버스 AI 등 — 무료 한도, 가격, 한국어 글자 렌더링 품질, 상업 이용, 9:16/4:5 비율 지정법, 캐릭터·스타일 일관성 기능.
3. 카드뉴스 디자인 템플릿: Canva, 미리캔버스, 망고보드 등 — 무료 템플릿·대량 제작(Bulk create)·한국어 폰트 라이선스·AI 기능.
4. 영상 편집·자동 자막: CapCut(PC/모바일, 한국 가용·무료 범위·템플릿·자동 자막·워터마크·상업 이용), Vrew(한국어 자동 자막·AI 목소리·무료 한도), YouTube Create, DaVinci Resolve, Clipchamp.
5. AI 영상 생성: Google Veo(Gemini 앱·Flow·YouTube Shorts 통합), OpenAI Sora, Kling, Runway, Hailuo(MiniMax), Pika, Luma 등 — 한국에서 사용 가능 여부, 무료 크레딧, 가격, 최대 길이·해상도·세로 비율, 음성 포함 여부, 워터마크, 상업 이용, AI 표시(SynthID 등).
6. AI 음성: 타입캐스트, ElevenLabs, 클로바더빙, Vrew AI 목소리, CapCut TTS — 한국어 자연스러움, 무료 한도, 상업 이용·표시 조건.
7. AI 음악: Suno, Udio, YouTube 오디오 보관함·Dream Track 등 — 상업 이용·인스타/유튜브 사용 조건, Content ID 위험.
8. **제작 과정(워크플로)**: 공식 프롬프트 가이드(Google Veo 프롬프트 가이드, OpenAI 이미지/Sora 가이드, Midjourney 문서, Runway 가이드), 한국·해외의 "AI 카드뉴스 만들기", "얼굴 없는 AI 쇼츠 만들기", "AI 영상 생성 쇼츠" 실제 제작 과정을 공개한 신뢰할 만한 튜토리얼(공식 블로그·크리에이터 교육 자료 우선)에서 공통 단계와 도구 조합, 소요 시간, 흔한 실수.
9. 플랫폼 표시: 각 도구 결과물을 인스타·유튜브에 올릴 때 AI 표시가 필요한 경우(C2PA/SynthID 자동 감지 포함).

산출물:
- research/ai-production.md: ① 작업별 추천 도구 표(서비스, 잘하는 것, 무료 한도, 가격 원화/달러, 한국어, 한국 가용, 상업 이용, AI 표시) ② **"처음엔 이것 하나"** 추천과 이유 ③ 무료로 끝까지 가는 조합 1개, 월 1~3만 원 조합 1개(인스타/쇼츠 각각) ④ 레시피별 단계(입력·출력·도구·소요 시간·비용) — 인스타 4종(뉴스카드, 카드→모션 릴스, 얼굴 없는 해설 릴스, AI 영상 생성 릴스), 쇼츠 3종(직접 촬영+AI 편집, 얼굴 없는 해설, AI 영상 생성) ⑤ 프롬프트 작성 공식과 검증된 예시(이미지·영상·대본) ⑥ 흔한 실수와 품질 기준 ⑦ 상충·미확인.
- research/SOURCES.md에 S300번대, FACT-SHEET에 AIP-* 사실 추가(인스타 편용). research-shorts/SOURCES.md·FACT-SHEET.md에도 쇼츠 관련 항목을 Y300번대·YT-AIP-*로 추가.
- docs/results/phase-R3.md(질의 품질표 포함). 공식 출처 12개 이상 직접 확인.
- `python3 scripts/notify.py "✅ [R3 AI 제작 조사 완료] ..." research/ai-production.md`로 한국어 보고(처음엔 이것 하나 추천을 요약).
