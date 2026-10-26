# AI 문안·대본·이미지: 무료 경로와 이용 권리

작성: 2026-10-26, Codex 정리. **2026년 10월 조사 기준**(컷오프: 2026-10-26). Hermes 원응답과 별개인 편집본이다.

- 원응답: `/home/yonghun/project/hermes-research/output/ai-insta-research-20261026/raw/ai-text-image-tools.md`
- SHA256: `fea123dba42e7c55f72f24282a892c299c498f1edc67045fea1b0481b473bbc4`

## 핵심 사실(출처 각주)

- **AI-01 · Hermes 근거**: 무료 웹 UI, 제한된 API 무료 할당, 유료 API, 로컬 추론은 별개 경로다. ChatGPT 무료 도구에도 개별 사용 제한이 있고 Gemini API Free는 일부 모델 대상이다. 웹 무료가 API 무료 또는 무제한을 뜻하지 않는다. [^S049] [^S051] [^S052]
- **AI-02 · Hermes 근거**: Qwen3-8B 공식 모델 저장소는 Apache-2.0를, llama.cpp 실행기는 MIT를 표시한다. 모델 가중치와 실행기 라이선스를 각각 확인해야 하며 특정 PC에서의 실행 성공·한국어 뉴스 정확도는 검증하지 않았다. [^S053] [^S054] [^S055]
- **AI-03 · Hermes 근거**: FLUX.1-schnell 모델 카드는 Apache-2.0와 상업 목적 이용 경로를 안내한다. FLUX.1-dev의 모델 사용 제한 및 출력물 조건은 다르므로 같은 브랜드의 라이선스를 일괄 적용하면 안 된다. [^S058] [^S059]
- **AI-04 · Hermes 근거**: Firefly의 과거 FAQ는 비베타 생성물 상업 이용을 안내하고 Adobe 가이드라인은 제3자 권리 침해를 금지한다. 상업 이용 허락은 입력 자료·초상·상표·저작권 문제나 비침해 보장과 별개다. [^S056] [^S057] [^S060]
- **AI-05 · Hermes 근거**: FLUX.1-schnell 모델 카드는 사실 정보를 제공하는 용도로 의도되지 않았다고 설명한다. 생성 삽화를 실제 사건의 증거 사진으로 제시할 근거가 되지 않는다. [^S058]
- **AI-06 · 미확인/추가 조사 필요**: ChatGPT 지원국 목록에 한국이 있다는 Hermes 확인은 한국어 요약 정확도·모든 이미지 기능·API 지역 지원을 입증하지 않는다. Gemini·Firefly·Midjourney의 한국 기능/결제/무료 할당도 이번 조사로 모두 확정하지 못했다. [^S050] [^S052] [^S056] [^S060]
- **AI-07 · 미확인/추가 조사 필요**: 한국어 뉴스 요약의 환각률이나 특정 프롬프트의 오류 감소율을 입증하는 자료를 확보하지 못했다. 출처·인명·날짜·수치·부정과 조건의 원문 대조는 교육용 검수 절차이며 오류 제거 보장이 아니다. [^S053] [^S010]

## 수치 표

| 항목 | 값·적용 범위 | 판정·출처 |
| --- | --- | --- |
| ChatGPT 무료 생성 횟수 | 구체 횟수·갱신 주기 미확인 | 제한 존재만 확인 [^S049] |
| 로컬 실행기·모델 | llama.cpp MIT, Qwen3-8B Apache-2.0 | 각 저장소의 버전 고정/전문 재확인 필요 [^S054] [^S055] |
| FLUX.1-schnell | Apache-2.0 명칭 확인 | 가중치 권리와 출력물·제3자 권리는 별개 [^S058] |
| 한국 무료량·API 단가·RAM/VRAM | 확정값 미채택 | 무료량·현장 실행·동적 가격 검증 부족 [^S052] [^S053] |

## 한국 가용성

- 한국 지원국 확인과 특정 기능 제공·상업 이용·한국어 품질을 나눠 기록한다. [^S050]
- 로컬 경로의 공개 문서·라이선스는 확인되었지만 국내 PC 다운로드·설치·생성은 수행하지 않았다. [^S053] [^S058]

## 불확실·상충

- Firefly FAQ는 과거 문서이고 제휴 모델·베타·플랜별 조건이 다를 수 있다. 무료량·원화 가격을 확정하지 않는다. [^S056]
- FLUX.1-dev는 모델 운영의 비상업 제한과 출력물 이용 조항을 분리해야 한다. 출력물 조항 전문은 미확인이다. [^S059]
- OpenAI 결과물 소유·상업 이용 조항 뒤쪽과 Midjourney 플랜별 권리·기업 조건은 확보하지 못했다. 상업적으로 자유롭다는 결론을 쓰지 않는다. [^S051] [^S060]

## 교과서 반영 포인트(장 번호)

- 6장: API 키 없는 규칙 기반 후보 추출+수동 재작성 경로를 기본으로 설명한다. 도구 설치·실행은 후속 Phase 범위다.
- 5~6장: 각 사실에 원출처 URL·게시일·사건일·원문 위치를 연결하고 인명·단위·조건·부정을 사람이 대조한다.
- 6~7장: 생성 삽화와 실제 보도 사진을 구별하고 한국어 제목·수치·출처는 편집 단계에서 넣는다.

[^S049]: [ChatGPT Free Tier FAQ](https://help.openai.com/en/articles/9275245-using-chatgpt-s-free-tier-faq) · OpenAI Help Center · 게시·갱신: 절대 날짜 미상; Hermes 관찰시 상대 갱신 20일 전 · 접근: 2026-10-26 · A · Hermes 원문; 도구별 제한 존재, 구체 무료 횟수 미확인. 전체 메타데이터: [SOURCES.md](SOURCES.md#s049).

[^S051]: [Terms of Use](https://openai.com/policies/terms-of-use/) · OpenAI · 게시·갱신: 시행 2026-01-01 · 접근: 2026-10-26 · A · Hermes 앞부분; API 별도 계약, 결과물 권리 조항은 미확인. 전체 메타데이터: [SOURCES.md](SOURCES.md#s051).

[^S052]: [Gemini Developer API Pricing](https://ai.google.dev/gemini-api/docs/pricing) · Google AI for Developers · 게시·갱신: 날짜 미상 · 접근: 2026-10-26 · A · Hermes Free/Paid 본문; 모델별 무료량·한국 제공은 미확인. 전체 메타데이터: [SOURCES.md](SOURCES.md#s052).

[^S053]: [Qwen3-8B Model Card](https://huggingface.co/Qwen/Qwen3-8B) · Qwen · 게시·갱신: 날짜 미상 · 접근: 2026-10-26 · A · Hermes 모델 카드 일부; 로컬 경로 확인 보고, 국내 실행·한국어 정확도 미검증. 전체 메타데이터: [SOURCES.md](SOURCES.md#s053).

[^S054]: [Qwen3-8B LICENSE](https://huggingface.co/Qwen/Qwen3-8B/blob/main/LICENSE) · Qwen · 게시·갱신: 파일 갱신일 미상; 라이선스 명칭 Apache-2.0 · 접근: 2026-10-26 · A · Hermes LICENSE 앞부분; 버전 고정 전문 검토 미완료. 전체 메타데이터: [SOURCES.md](SOURCES.md#s054).

[^S055]: [llama.cpp Repository](https://github.com/ggml-org/llama.cpp) · ggml-org · 게시·갱신: 날짜 미상 · 접근: 2026-10-26 · A · Hermes README 일부; MIT·로컬 CPU/GPU·양자화 안내 확인 보고. 전체 메타데이터: [SOURCES.md](SOURCES.md#s055).

[^S058]: [FLUX.1-schnell Model Card](https://huggingface.co/black-forest-labs/FLUX.1-schnell) · Black Forest Labs · 게시·갱신: 날짜 미상 · 접근: 2026-10-26 · A · Hermes 모델 카드 일부; Apache-2.0·상업 목적·사실 정보 비의도 확인 보고. 전체 메타데이터: [SOURCES.md](SOURCES.md#s058).

[^S059]: [FLUX.1-dev LICENSE.md](https://huggingface.co/black-forest-labs/FLUX.1-dev/blob/main/LICENSE.md) · Black Forest Labs · 게시·갱신: 날짜 미상 · 접근: 2026-10-26 · A · Hermes 모델 제한 원문 일부, 출력물 상업 이용 조항은 검색 요약만. 전체 메타데이터: [SOURCES.md](SOURCES.md#s059).

[^S056]: [Adobe Firefly FAQ](https://helpx.adobe.com/firefly/get-set-up/learn-the-basics/adobe-firefly-faq.html) · Adobe · 게시·갱신: 게시 메타데이터 2025-06-26 / 본문 갱신 2025-08-20 · 접근: 2026-10-26 · A · Hermes 과거 FAQ 일부; 비베타 상업 이용, 2026 모든 모델 현행 적용 미확인. 전체 메타데이터: [SOURCES.md](SOURCES.md#s056).

[^S057]: [Adobe Generative AI User Guidelines](https://www.adobe.com/legal/licenses-terms/adobe-gen-ai-user-guidelines.html) · Adobe · 게시·갱신: 갱신 2026-05-15 · 접근: 2026-10-26 · A · Hermes 본문 일부; 제3자 권리 침해 금지 확인 보고. 전체 메타데이터: [SOURCES.md](SOURCES.md#s057).

[^S060]: [Midjourney Terms of Service](https://docs.midjourney.com/hc/en-us/articles/32083055291277-Terms-of-Service) · Midjourney · 게시·갱신: 시행 2026-05-27 · 접근: 2026-10-26 · A · Hermes 앞부분; 비침해 보장 부인 확인 보고, 플랜별 상업 이용은 미확인. 전체 메타데이터: [SOURCES.md](SOURCES.md#s060).

[^S050]: [ChatGPT Supported Countries](https://help.openai.com/en/articles/7947663-chatgpt-supported-countries) · OpenAI Help Center · 게시·갱신: 절대 날짜 미상; Hermes 관찰시 상대 갱신 4일 전 · 접근: 2026-10-26 · A · Hermes 원문에서 South Korea 확인 보고; API/모든 기능 지원국과 별개. 전체 메타데이터: [SOURCES.md](SOURCES.md#s050).

[^S010]: [저작권법(현행 본문)](https://www.law.go.kr/LSW/lsInfoR.do?lsiSeq=283335&chrClsCd=010202&efYd=20260811) · 국가법령정보센터 / 문화체육관광부 · 게시·갱신: 2026-02-10 개정 / 현행판 시행 2026-08-11 · 접근: 2026-10-26 · A · Codex curl 본문 확인; 제7조제5호·제28조·제35조의5·제37조 확인. 전체 메타데이터: [SOURCES.md](SOURCES.md#s010).
