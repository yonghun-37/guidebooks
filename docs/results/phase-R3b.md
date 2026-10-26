# Phase R3b. AI 모델 × 사용처 × 비용 체계 총정리

기준·접근일: **2026-10-26**. 담당: Codex(정리·교차 확인), Hermes(공식 자료 조사). **연구 완료·Claude Code 검수 대기**. 문헌 조사이며 한국 계정 가입·결제·API 호출·생성 품질·게시를 시험한 결과가 아니다.

## 완료한 내용과 산출물

- [공통 모델·사용처·가격 노트](../../research/ai-models-pricing.md): 모델·버전·상태·모델 미공개 기능 **274행**, 구독·번들 **24종**, 제작물3종×무료/저비용/고품질 설정 **9시나리오**, 계산식·원화 환산·상충/미확인 목록. 274개가 모두 서로 다른 현행 기반모델이라는 뜻은 아니다.
- [인스타 출처](../../research/SOURCES.md): S400~586 중 실제 인용한 **151개** 추가(중간 번호 공백 있음). [인스타 사실표](../../research/FACT-SHEET.md): AIM-001~076 추가.
- [쇼츠 출처](../../research-shorts/SOURCES.md): 동일 끝번호 Y400~586 중151개. [쇼츠 사실표](../../research-shorts/FACT-SHEET.md): YT-AIM-001~076 추가. 쇼츠의 생성 길이/청구 길이·한국 생성 제한·음원 반출·오디오/표시 조건과 공통 노트를 연결했다.
- [확인 메타데이터](phase-R3b-verification.json): 공식 URL·기관·접근일·확인 범위·HTTP 상태/해시·Hermes 실행/질의/원응답 해시. 원응답 전문·개인 환경·인증정보는 포함하지 않는다.

| 범주 | 행수 |
|---|---|
| 텍스트 LLM | 70 |
| 이미지 | 75 |
| 영상 | 63 |
| 음성·전사 | 35 |
| 음악 | 25 |
| 편집 앱 내장 AI | 6 |

주요 현행 모델과 요청된 이전 세대를 정리하되 날짜별 모든 스냅샷·튜닝 파생·임베딩/보안/생명과학 전용 전체 카탈로그까지 포함한다고 주장하지 않는다. 미공개 엔진에는 가상 모델명을 붙이지 않았다.

## 중요한 확인과 R3 보완

1. **서비스보다 모델·정확 버전을 먼저 정리했다.** ChatGPT Free GPT-5.6 Luna/유료 GPT-6, Claude5.5/Fable5.1, Gemini4 Argon/3.8, GPT Image2.5, Nano Banana2.1, Midjourney8.2, FLUX3, Kling4, HailuoH3, Seedance2.5, Elevenv4, Sunov6 등 현재 공식 자료에 나온 세대를 이전 버전과 분리했다.
2. **종료 문서를 가격표보다 우선했다.** Veo3.1 Gemini Developer Preview10/22 종료와 Cloud/Flow의 현행 경로를 분리했다. Imagen 생성endpoint·Sora·DALL·E·RunwayGen3·Suno구형모델의 잔존 가격/문서가 현행 제공의 증거가 되지 않도록 했다. Sonar는 지원 종료 뒤 동기/스트림 전환과 비동기 미지원을 구별한다. OpenAI TTS2027-01-06은 미래 종료 예정으로 기록했다.
3. **한도와 단위를 분리했다.** Claude Max의 명시된 API 크레딧 예외, ElevenCreative 웹과API 포함 문자, Flow영상과FlowMusic, Typecast다운로드와API문자, Vrew공용풀을 구별했다. VertexVeo의`/1 count`는 초당 환산을 확정하지 않았다.
4. **한국 지원과 한국어 지원을 구별했다.** YouTube Create 일반편집 한국지원과 Omni생성 한국미제공을 분리했다. Claude11/12 시행 정책을 소급하지 않고3/16 도움말로 한국 지원을 확인했다. HCX003/DASH001의 컨텍스트·입력·출력도 각각 바로잡았다.
5. **성공본 사용분과 실제 현금 지출을 분리했다.** 카드 저비용 약₩95.45, 해설 저비용 약₩101.66, AI영상 저비용 약₩2,777은 공개된 가정의 사용분이다. 신규 구독·최소 충전·세금·재생성을 별도로 설명한다. 고품질은 선택 설정의 명칭이며 품질 순위 실측이 아니다. 환율은9/30 Wise 과거 약1351을 반올림한 예산환율1350이고10/26 공적 종가가 아니다.
6. **무료 상업 제작을 무조건 약속하지 않았다.** Flow 무료 접근·PikaStarter상업권·Nano Banana원형종료일 등 공식 상충, Udio 반출 중단, Suno 다운로드 한도, 내부모델/국내 단가 미확인을 남겼다. 음원은 쇼츠에서 권리 확인한 YouTube 보관함, 인스타 예시에서는 생략한다.

## 수행 범위와 변경 소유권

AGENTS.md·guidebook-pipeline/research Skill·DESIGN12절·PLAN Hermes 호출법·지정 R3 노트/결과와 관련 출처를 읽었다. OpenAI 부분에는 openai-docs Skill과 공식 문서를 적용했다. 일반 PLAN보다 이번 사용자 지시의 **RUN·총24회 이하·최대4개·40turns**를 우선했다.

이번 작업에서 쓴 저장소 파일은 위 연구5개와 결과/메타데이터2개, 합계7개뿐이다. site/·site-shorts/·starter-kit/·shorts-kit/·서가·배포·설계서는 수정하지 않았다. 작업 중 다른 작업자의 사이트 변경/커밋이 관찰됐으며 되돌리지 않았다. PROJECT_STATE는pipeline의 통합 작업자 소유 규칙에 따라 이 결과를 인계해 갱신하도록 남겼다. Codex는commit/push를 실행하지 않았다.

Hermes 저장소에서는 사용자 허용 RUN의`queries/r3b-*`·`raw/r3b-*`만 만들었다. 코드·config·runtime·Skill·컨테이너 기동/재시작은 변경하지 않았다. 유료 API·새 키·결제·실계정 로그인/게시를 하지 않았다.

<a id="hermes-실행-기록"></a>
## Hermes 실행 기록과 품질 판정

**12/24회**, 재시도0회, 실제 최대동시4개. 각 호출은`-s guidebook-research --max-turns 40 --provider openai-codex -t web`이며900초 제한을 뒀다. 질의별 원응답의 근거 URL·오류/누락 고지·숫자를 읽고 판정했다. 모든exit0이지만 그것만으로 성공으로 세지 않았다.

근거 없이 끝난 **전면 실패0/12(0%)**, 가격 추출/지역/약관 등 **부분 제약12/12(100%)**다. Codex 웹 검색과 공식 페이지 직접 열람으로 보완했고, 해결하지 못한 공백은 미확인으로 유지했다. 아래 숫자는 대소문자 무시 **문자열 언급 횟수**이며 실제 HTTP 오류 횟수/실패율이 아니다. “403 없음”도 언급1회가 될 수 있다.

시각은2026-10-26 **UTC**(한국시각+9시간), 바이트/해시는 원응답 파일 실측이다.

| 질의(파일 앞에r3b-) | 시작 UTC | 종료 UTC | exit | 바이트 | 403/timeout/blocked/검색실패 언급 | 고유URL수 |
|---|---|---|---|---|---|---|
| 01-openai | 04:54:25 | 04:59:24 | 0 | 35,996 | 0/0/0/0 | 44 |
| 02-llm | 04:54:25 | 04:59:05 | 0 | 30,827 | 0/0/0/0 | 58 |
| 03-search-korea | 04:54:25 | 05:00:11 | 0 | 27,635 | 0/0/0/0 | 46 |
| 04-google-image-video | 04:54:25 | 04:59:53 | 0 | 33,853 | 1/0/0/0 | 51 |
| 05-image-design | 04:59:05 | 05:06:41 | 0 | 48,996 | 1/0/0/0 | 61 |
| 06-flux-sd | 04:59:24 | 05:04:15 | 0 | 28,411 | 0/0/0/0 | 43 |
| 07-kling-runway | 04:59:53 | 05:05:42 | 0 | 35,812 | 1/0/0/0 | 46 |
| 08-video-other | 05:00:11 | 05:03:57 | 0 | 30,491 | 0/0/0/0 | 46 |
| 09-voice-global | 05:03:57 | 05:09:05 | 0 | 32,416 | 0/0/0/0 | 46 |
| 10-voice-korea | 05:04:15 | 05:09:27 | 0 | 28,437 | 0/0/0/0 | 35 |
| 11-music | 05:05:42 | 05:10:57 | 0 | 31,221 | 0/0/0/0 | 47 |
| 12-editors-fx | 05:06:41 | 05:12:19 | 0 | 30,349 | 2/0/0/0 | 44 |

원응답: `/home/yonghun/project/hermes-research/output/ai-production-research-20261026/raw/r3b-<질의>.md`. 질의: 같은RUN의`queries/r3b-<질의>.txt`. 원응답은 수정하지 않았다. 질의 해시도 JSON에 보존했다.

| 원응답 파일 | SHA256 |
|---|---|
| `r3b-01-openai.md` | `d8e1bef9f8a9ccb8df0f8fb5196f78011edc4a6ef66d7c3198a4022bae0935a9` |
| `r3b-02-llm.md` | `60ca46b41cde34468339877617d7fc85237e80c4378cfc79d450d8c54fed2da5` |
| `r3b-03-search-korea.md` | `8d40a9224a8f87b3efa3eea8718059f81e587d7d76c054d4a4a1179ea09a2951` |
| `r3b-04-google-image-video.md` | `7f52ed02b57d559b6bc5d8e39786e8eb71de993b2826647c5dfc447bdbd7b388` |
| `r3b-05-image-design.md` | `06df920e26bddf8e13e03fec78ac1a31701f719ed5dd0469d7430d14ff5d0069` |
| `r3b-06-flux-sd.md` | `3f52a913c5c6cef19819c779803e25c4562e9e83a84e868a5796df504b2523bd` |
| `r3b-07-kling-runway.md` | `ca0570453de2687c659b171d75100a28e5b7b6c89176c0d81c43b6950459fd36` |
| `r3b-08-video-other.md` | `b11862ab203a0a997803431ab639cc359926447479e42e6b8a5beb8d9dafb07f` |
| `r3b-09-voice-global.md` | `6461809446259e29cb905247b275303ce61a246ec01e16c48fbdced978b485a2` |
| `r3b-10-voice-korea.md` | `51e906586b76b1f427868a3bba1ff7c2195c8dfe6787e22968ca4bc8db143927` |
| `r3b-11-music.md` | `e3ad99368c0a404d98d22974487fffed499ec08fee4a8d7c25f6677adc36ec90` |
| `r3b-12-editors-fx.md` | `276e7e2e813264f4af9074add1e382966150f348bc0e1faed6ca0df7be0be893` |

## Codex 공식 가격·요금 페이지 직접 확인

등록151개 중 **91개는 명시된 범위의 본문을 Codex 웹 또는HTTP로 직접 확인**했다. 로그인 셸·일반 메뉴로 이동한 모델URL·숫자가 빈 동적 요금표는 전체 검증으로 세지 않는다. 직접 본문을 읽었어도 그 페이지의 모든 가격·지역·모델을 검증했다는 뜻은 아니며 개별 범위/공백은 출처표와JSON에 적었다. 나머지는 Hermes 근거 또는 독립 확인 미완료/부분이다.

아래 **서로 다른 공식 가격/요금 URL29개**를 직접 열어 가격·단위·포함량의 적힌 범위를 확인했다(요구15개 이상 충족). 동적 금액이 없는 항목은 그 공백도 명시한다. 같은 가격표의 여러 모델을 여러 페이지로 중복 세지 않았다.

| 공식 페이지 | 직접 확인 범위 |
|---|---|
| [S400. OpenAI API 가격](https://developers.openai.com/api/docs/pricing) | Standard와Batch/Fast 분리·현행/잔존 GPT 입력/출력·이미지/음성요율 |
| [S405. Claude 가격](https://claude.com/pricing) | Claude 개인 플랜·Max API크레딧·현행/이전모델 단가 |
| [S406. Claude API 가격](https://platform.claude.com/docs/en/about-claude/pricing) | Claude API 단가·캐시·부가기능 |
| [S408. Gemini API 가격](https://ai.google.dev/gemini-api/docs/pricing) | Gemini 주력/이미지/TTS/음악 Standard·Batch 분리·원형Nano종료문구상충 |
| [S410. Vertex 생성 AI 가격](https://cloud.google.com/vertex-ai/generative-ai/pricing) | Cloud LLM·Imagen잔존가격·Veo/count단위·Omni초당토큰환산 |
| [S414. Midjourney 구독](https://docs.midjourney.com/hc/en-us/articles/27870484040333-Comparing-Midjourney-Plans) | Midjourney 월/연정가·GPU시간·추가GPU·상업매출조건 |
| [S416. Ideogram 가격](https://ideogram.ai/pricing) | Ideogram Plus/Pro/Team금액·월크레딧;모델별직접API상세는Hermes05 |
| [S418. Firefly 한국 가격](https://www.adobe.com/kr/products/firefly/plans.html) | 한국Firefly 월별4플랜VAT포함·월2000/4000/10000/50000 |
| [S420. FLUX 가격](https://bfl.ai/pricing) | BFL종량/가중치계약·계산기기본$0.048관찰;전체동적정가미추출 |
| [S421. Stability API 가격](https://platform.stability.ai/pricing) | Stability1cr=$0.01·최초25cr·SD3.5/Core/Ultra단가 |
| [S425. Flow 크레딧](https://support.google.com/flow/answer/16526234?hl=en) | Flow일50·플랜월추가·모델별회당차감·혼잡제한 |
| [S428. Runway API 요금](https://docs.dev.runwayml.com/guides/pricing/) | Runway Dev $0.01/cr·자체/제휴 모델초당·참조/전문출력추가료 |
| [S433. Pika 요금](https://pika.art/pricing) | Pika현행플랜/금액·팩비호환·Starter상업허용본문 |
| [S434. Luma 요금](https://lumalabs.ai/pricing) | Luma월/연·10K/40K/150K·Ray/제휴모델크레딧차감 |
| [S437. ElevenLabs 가격](https://elevenlabs.io/pricing) | ElevenCreative월정가/최초할인·크레딧·상업권 |
| [S439. Typecast 가격](https://typecast.ai/kr/pricing) | TypecastStudio월/연·5등급다운로드크레딧·기업조건 |
| [S440. Typecast API 가격](https://typecast.ai/pricing/api) | TypecastAPI Lite/Plus가격·월자수/초과/자동묶음·SSFM3.0 |
| [S443. Google TTS 가격](https://cloud.google.com/text-to-speech/pricing) | Google문자TTS무료량/천자환산·GeminiTTS토큰가격 |
| [S445. Suno 가격](https://suno.com/pricing) | Suno현행v6접근·연환산$8/$24·생성/다운로드한도;월납표미확보 |
| [S453. ChatGPT Plus 가격](https://help.openai.com/en/articles/6950777-what-is-chatgpt-plus) | Plus월$20·API별도 |
| [S454. ChatGPT Pro 가격](https://help.openai.com/en/articles/9793128-what-is-chatgpt-pro) | Pro100/200/500월액·10/29기존한도유예 |
| [S460. Runway 앱 가격 현행](https://runway.com/pricing) | Runway월/연·125최초·625/2250/9500·광고초수상충 |
| [S461. Perplexity API 현행 가격](https://docs.perplexity.ai/docs/getting-started/pricing) | Perplexity Agent/Orchestrator 모델과도구요금·레거시와분리 |
| [S495. Gemini 한국 구독가격](https://gemini.google/kr/subscriptions?hl=ko) | 한국Gemini구독Plus7500/Ultra119000·300000·Pro혜택;Pro금액빈판본존재 |
| [S511. Luma Agents API 가격](https://docs.agents.lumalabs.ai/guides/pricing/) | UNI1/Max2K장당·Ray3.2해상도별5/10초API가격·HDR제약 |
| [S512. Pika2.5 API 가격](https://dev.pika.art/models/pika/pika-2.5/text-to-video/pricing) | Pika2.5 T2V/I2V 초당·별도오디오요금 |
| [S535. Kling API 영상가격](https://kling.ai/document-api/pricing/base/video.md) | 직접Markdown:Kling2.5/2.6/3/O1·4API미리보기·4.0Preview dollar/Unit차이 |
| [S549. ElevenAPI 문자단가](https://elevenlabs.io/pricing/api) | ElevenAPI $0.08/$0.04천자·플랜포함문자·API는달러과금 |
| [S560. CapCut 공식 구독가격](https://www.capcut.com/pricing) | CapCut월Pro19.99/Ultra79·1200/8645·연표시179.99/900·프로모션초당값 |

## 검증 결과

- 문서 검사 통과: 274행의 필수9열·중복 모델명, 구독24종·시나리오9개, S/Y151개와 AIM/YT-AIM76개 각각의 고유성·대응, 신규 로컬 링크/출처 앵커, Markdown 표 열수를 확인했다.
- 공개 계산식16개를 Decimal로 검산했고, 원응답/질의12쌍의 바이트·SHA256·언급수와 실행시각으로 실제 최대동시4개를 확인했다. 가격 페이지29개는 서로 다른 공식 URL이며 직접 확인 범위를 보존했다.
- 기존 출처/사실표4개는 원래 바이트 접두부 해시가 그대로다. 신규 내용만 덧붙였으며 기존 R3 사실은 당시 기록을 보존하면서 최신 판정을 연결했다.
- 문서 링크·표·산술 검사는 앱 기능/음질/한국 계정/결제 테스트를 대신하지 않는다. 이번 연구 범위에서는 사이트·키트 테스트나 생성API 호출을 실행하지 않았다.
- 원응답 전문·토큰·환경 파일을 저장소에 넣지 않았다. 결과 JSON은 URL·날짜·확인 수준·해시·검증 요약만 담는다. 작업 파일의 `git diff --check`와 신규 파일을 포함한 끝 공백/비밀키 패턴 검사가 통과했다.

## 남은 확인과 통합 인계

- 한국 신규 계정에서 가격/세금·앱스토어·정확 모델 해금·생성직전 차감·무료 접근을 실증하지 않았다. NAVER 일부 원화 단가, Canva/미리캔버스 현재 결제창, Kling앱 신구플랜, Udio요금, Seedance일부API는 각 출처에 적힌 확인 수준을 유지한다.
- Gemini원형Nano종료일·VeoCloud count/해상도·PikaStarter상업권·Flow무료·Runway앱차감·Suno소급권리는 공통 노트6절의 권장 결론과 확인 위치를 따른다.
- R3 AIP-044(쇼츠YT-AIP-044)의 Veo3.1 Developer 사양은 종료된Preview의 기록으로 보존하고 R3b의 현행 경로로 보완했다. R3의 Kling Codex본문 미확인도 이번 API Markdown 확인 범위에서 보완했다.
- Claude Code는 이 연구와 기존 R3를 함께 검수하고 PROJECT_STATE·책별 집필 인계 상태를 갱신한다. 사이트·키트 원고 적용은 이번 요청 범위 밖이다. 실제 앱/생성/결제/음질/시간 측정은 수행하지 않았다.

## 단계 보고

지정된 `python3 scripts/notify.py` 명령으로 한국어5줄 보고와 `research/ai-models-pricing.md` 첨부를 전송했다. **HTTP200·exit0**을 확인했다. 보고에도 한국 실계정·동적 가격·상충 항목과 검수 대기를 명시했다.
