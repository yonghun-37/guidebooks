# AI 도구 가격·무료량·한국어·상업 이용

작성: 2026-10-26, Codex 정리. **2026년 10월 조사 기준**(컷오프2026-10-26). Hermes 원응답과 별개인 편집본이며, 아래 사실의 확인 수준은 독립적으로 표시했다.

## 질의·원응답과 확인 범위

- 원응답: `/home/yonghun/project/hermes-research/output/ai-insta-research-20261026/raw/ai-tools-pricing.md`
- SHA256: `b279fbc6ec7feb4784a298c67fb7b0fd5bf45a276581d5b188d5d1ea34a52ae5`
- 원응답: `/home/yonghun/project/hermes-research/output/ai-insta-research-20261026/raw/ai-tools-pricing-supplement.md`
- SHA256: `5bf8cd694e89f7340f39e88714156aaa59e2f41cfa35ac45bb3de0da252ff52f`

초기 응답의 가격 주제는 일부 공식 본문을 얻었고, 다수 주제는 웹 중계 프록시403으로 근거를 얻지 못했다. 보충 질의도 실행별로 평가했다. exit0·URL 존재를 본문 확인으로 세지 않았다. Codex가 별도 경로로 읽은 근거는 SOURCES의 확인 범위와 [직접 확인 기록](verification-phase-1b.json)을 따른다.

## 핵심 사실(출처 각주)

- **PRICE-01 · 확인함; VAT·실결제 별도**: 타입캐스트 무료 플랜은 음성 생성·재생과 다운로드를 구분한다. 무료 다운로드는 최초 3000credits(약5분), Basic은 월9900원 또는 연106800원과 월30000credits(약60분)를 표시한다. Basic에는 상업 사용 가능 표시가 있고 기업·공공기관·에이전시는 Business 이용을 안내한다. [^S126]
- **PRICE-02 · 확인함**: ElevenLabs Free는 월10000credits를 제공하지만 상업 라이선스가 없다. 유료 구독 중 생성한 콘텐츠도 권리·법률·추가약관을 지켜야 하고 베타 서비스는 제외된다. 나중에 결제해도 무료 기간의 생성물에 상업 권리가 소급된다고 볼 수 없다. [^S124] [^S125]
- **PRICE-03 · 확인함; 계약·실측 별도**: Google Cloud TTS는 결제 활성화가 필요하고 무료량 초과분은 자동 과금된다. Standard/WaveNet과 Chirp3HD의 무료량·초과 단가는 다르다. 한국어 ko-KR 음성 목록은 확인했지만 실제 음질·개별 화자 권리·한국 청구는 검증하지 않았다. [^S101] [^S166]
- **PRICE-04 · 확인함; 문서 경로/모델별 구분**: OpenAI 공식 가격표는 Standard short-context gpt-6-luna의 100만토큰당 입력$0.10·출력$0.50을 표시한다. API 종량 가격이므로 웹 UI 구독료나 영상1편 원가와 다르다. Hermes가 다른 OpenAI 가격 경로에서 보고한 모델표는 동일 판본·모델인지 추가 대조가 필요하다. [^S163]
- **PRICE-05 · 확인함**: Gemini API는 일부 모델의 Free/Paid와 데이터 이용 표시를 구분한다. 지원국 목록에 한국이 있지만, 모든 모델·무료량·한국 결제·한국어 성능을 보장하는 목록은 아니다. [^S052] [^S165]
- **PRICE-06 · Phase1 직접 확인 근거 재사용**: Whisper는 MIT 라이선스의 음성인식·자막 도구이고 FFmpeg는 빌드별 LGPL/GPL 조건을 둔다. 로컬 실행기의 라이선스와 모델·음성·사진의 권리는 별도로 확인해야 한다. [^S088] [^S090]
- **PRICE-07 · 미확인/추가 조사 필요**: Vrew 가격 URL에서는 가격표 대신 제품 소개가 반환되었다. Vrew·CapCut·Canva의 최신 한국 구독료·무료 자막량과 도구 간 한국어 음질 순위는 확정하지 않는다. [^S127] [^S098] [^S100]

## 수치 표

| 도구·용도 | 무료/비용 관찰값 | 권리·한국·조건 |
| --- | --- | --- |
| ChatGPT 웹·문안 | 무료UI의횟수/모델별최신량미확인 | Phase1국가확인과API구분 [^S049] [^S050] |
| OpenAI API·문안 | gpt-6-luna Standard short:입력$0.10/출력$0.50/100만토큰 | 문맥≤272K,도구/세금/한국청구별도·품질미실측 [^S163] |
| Gemini API·문안 | 일부모델Free·Paid,무료고정량미채택 | 한국지원목록·Free데이터이용별도 [^S052] [^S165] |
| FLUX.1-schnell·이미지 | 모델Apache2.0;장비/호스팅비별도 | Phase1후보,한국생성실증없음 [^S058] |
| Firefly·이미지 | 현행한국가격/무료량미확인 | 과거비베타상업FAQ를모든모델에확대금지 [^S056] |
| Canva·카드 | 현행한국구독료/AI한도미확인 | Free/Pro/Branded/음악조건별도 [^S100] |
| 타입캐스트·TTS | 무료최초3000credits약5분;Basic월9900원·연106800원 | 월30000credits약60분·상업가능;기업별도·VAT미확인 [^S126] |
| ElevenLabs·TTS | Free10000credits/월;Starter30000·월$6표시,11/1까지첫달$1프로모션 | 세금별도·통화코드별도미확인·Free상업불가 [^S124] [^S125] |
| Google TTS | Standard/WaveNet월400만문자후US$4/백만;Chirp3HD100만후US$30/백만 | 결제활성화필수·초과과금·ko-KR목록 [^S101] [^S166] |
| Vrew·자막/TTS | 최신가격·무료량미확인 | 가격URL본문이제품소개,성능/권리미검증 [^S127] |
| Whisper·자막 | MIT코드/모델·로컬장비비별도 | TTS아님·한국어오류율미실측 [^S088] |
| FFmpeg·편집 | 로컬도구·별도API종량없음 | 빌드/재배포·codec·소재권리별도 [^S090] |
| CapCut·편집 | 한국무료자막량/Pro가격미확인 | Commercial Sounds의Instagram반출별도 [^S098] |

모두2026-10-26관찰이며 갱신일 미상인 가격은 시행 시작일을 알 수 없다. 한국어 지명·숫자·영문약어·빠른 문장 표본의 직접 청취/오류율 평가를 하지 않아 “1위·자연스러움 점수”를 만들지 않았다.

## 한국 가용성

타입캐스트의 한국어 가격표, Gemini의 한국 지원 목록, Google의 ko-KR 음성 목록을 확인했다. 실제 결제·합성·워터마크·음질은 검증하지 않았다. [^S126] [^S165] [^S166]

## 불확실·상충

최초 지급과 월별 지급, 무료 체험과 상업 라이선스를 구분한다. ElevenLabs의 첫달 할인은 정상 월가격이 아니다. Hermes의 OpenAI 다른 URL 발췌는 모델·판본을 맞추기 전까지 같은 가격의 충돌로 확정하지 않는다. [^S124] [^S163]

## 교과서 반영 포인트(장 번호)

편집 제안: 직접 쓴 문안·직접 녹음/무음·로컬 자막과 렌더링을 기본 경로로 두고 TTS는 상업 권리를 확인한 뒤 선택한다. 한국어 품질 순위는 동일 문장과 평가 기준으로 실측할 때까지 제시하지 않는다. [^S126] [^S125] [^S088]

[^S126]: [타입캐스트 플랜 안내](https://typecast.ai/kr/pricing) · 타입캐스트 · 게시·갱신: 게시·갱신일 미상;2026-10-26 관찰 · 접근: 2026-10-26 · A · 확인함. 전체 확인 범위: [SOURCES.md](SOURCES.md#s126).

[^S124]: [ElevenLabs Pricing](https://elevenlabs.io/pricing) · ElevenLabs · 게시·갱신: 게시·갱신일 미상;2026-10-26 월결제 화면 · 접근: 2026-10-26 · A · 확인함. 전체 확인 범위: [SOURCES.md](SOURCES.md#s124).

[^S125]: [Can I publish the content I generate on the platform?](https://help.elevenlabs.io/hc/en-us/articles/13313564601361-Can-I-publish-the-content-I-generate-on-the-platform) · ElevenLabs · 게시·갱신: 게시·갱신일 미상 · 접근: 2026-10-26 · A · 확인함. 전체 확인 범위: [SOURCES.md](SOURCES.md#s125).

[^S101]: [Text-to-Speech pricing](https://cloud.google.com/text-to-speech/pricing) · Google Cloud · 게시·갱신: 게시·갱신일 미상 · 접근: 2026-10-26 · A · 확인함. 전체 확인 범위: [SOURCES.md](SOURCES.md#s101).

[^S166]: [Supported voices and languages](https://cloud.google.com/text-to-speech/docs/voices) · Google Cloud · 게시·갱신: 게시·갱신일 미상 · 접근: 2026-10-26 · A · 확인함. 전체 확인 범위: [SOURCES.md](SOURCES.md#s166).

[^S163]: [OpenAI API Pricing](https://developers.openai.com/api/docs/pricing) · OpenAI 공식 문서 · 게시·갱신: 게시·갱신일 미상;2026-10-26관찰 · 접근: 2026-10-26 · A · 확인함. 전체 확인 범위: [SOURCES.md](SOURCES.md#s163).

[^S052]: [Gemini Developer API pricing](https://ai.google.dev/gemini-api/docs/pricing) · Google AI for Developers · 게시·갱신: 게시·갱신일 미상 · 접근: 2026-10-26 · A · 확인함. 전체 확인 범위: [SOURCES.md](SOURCES.md#s052).

[^S165]: [Available regions for Google AI Studio and Gemini API](https://ai.google.dev/gemini-api/docs/available-regions) · Google AI for Developers · 게시·갱신: 갱신2026-10-22UTC · 접근: 2026-10-26 · A · 확인함. 전체 확인 범위: [SOURCES.md](SOURCES.md#s165).

[^S088]: [Whisper README License](https://raw.githubusercontent.com/openai/whisper/main/README.md) · OpenAI / Whisper · 게시·갱신: 날짜 미상 · 접근: 2026-10-26 · A · Phase1 기록 참조. 전체 확인 범위: [SOURCES.md](SOURCES.md#s088).

[^S090]: [FFmpeg License and Legal Considerations](https://www.ffmpeg.org/legal.html) · FFmpeg · 게시·갱신: 날짜 미상 · 접근: 2026-10-26 · A · Phase1 기록 참조. 전체 확인 범위: [SOURCES.md](SOURCES.md#s090).

[^S127]: [Vrew 가격 경로 접근 결과](https://vrew.ai/ko/pricing) · Vrew / VoyagerX · 게시·갱신: 게시·갱신일 미상 · 접근: 2026-10-26 · A · 열 수 없음. 전체 확인 범위: [SOURCES.md](SOURCES.md#s127).

[^S098]: [CapCut Materials License Agreement](https://www.capcut.com/clause/material-license-agreement) · CapCut · 게시·갱신: 갱신2026-01-22 · 접근: 2026-10-26 · A · 확인함. 전체 확인 범위: [SOURCES.md](SOURCES.md#s098).

[^S100]: [Canva Content License Agreement](https://www.canva.com/policies/content-license-agreement/) · Canva · 게시·갱신: 게시·갱신일 미상 · 접근: 2026-10-26 · A · 확인함. 전체 확인 범위: [SOURCES.md](SOURCES.md#s100).

[^S049]: [ChatGPT Free Tier FAQ](https://help.openai.com/en/articles/9275245-using-chatgpt-s-free-tier-faq) · OpenAI Help Center · 게시·갱신: 절대 날짜 미상; Hermes 관찰시 상대 갱신 20일 전 · 접근: 2026-10-26 · A · Phase1 기록 참조. 전체 확인 범위: [SOURCES.md](SOURCES.md#s049).

[^S050]: [ChatGPT Supported Countries](https://help.openai.com/en/articles/7947663-chatgpt-supported-countries) · OpenAI Help Center · 게시·갱신: 절대 날짜 미상; Hermes 관찰시 상대 갱신 4일 전 · 접근: 2026-10-26 · A · Phase1 기록 참조. 전체 확인 범위: [SOURCES.md](SOURCES.md#s050).

[^S058]: [FLUX.1-schnell Model Card](https://huggingface.co/black-forest-labs/FLUX.1-schnell) · Black Forest Labs · 게시·갱신: 날짜 미상 · 접근: 2026-10-26 · A · Phase1 기록 참조. 전체 확인 범위: [SOURCES.md](SOURCES.md#s058).

[^S056]: [Adobe Firefly FAQ](https://helpx.adobe.com/firefly/get-set-up/learn-the-basics/adobe-firefly-faq.html) · Adobe · 게시·갱신: 게시 메타데이터 2025-06-26 / 본문 갱신 2025-08-20 · 접근: 2026-10-26 · A · Phase1 기록 참조. 전체 확인 범위: [SOURCES.md](SOURCES.md#s056).
