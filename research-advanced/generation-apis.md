# 생성 API 선택·구조화 출력·가격·지출 관리

- Hermes 원응답: `/home/yonghun/project/hermes-research/output/advanced-research-20261026/raw/05-llm-structured-budgets.md` · SHA256 `539561e83f22893a6262f91531dda27e3b4d1712aadd790e00e7ae6db2d21666` · exit 0.
- Hermes 원응답: `/home/yonghun/project/hermes-research/output/advanced-research-20261026/raw/06-image-video-api.md` · SHA256 `5e7119ec1c09bfc4e7848cc5de06a0d2c1bf8db90254c8d9ea3ad6e5bc0ee860` · exit 0.
- Hermes 원응답: `/home/yonghun/project/hermes-research/output/advanced-research-20261026/raw/07-tts-korean.md` · SHA256 `aac88dd1dff3ca299a180acb1385850710858590740a6bbd6fb80fa1c3d40de2` · exit 0.
- 실행·실패 구분: [provenance.json](provenance.json). 핵심 주장은 Codex 직접 열람/기존 근거와 대조했다.

2026년 10월 조사 기준. 모델 전수표는 기존 `research/ai-models-pricing.md`를 재사용한다. 아래는 파이프라인에서 실제 고를 후보와 신규 운영 공백이다. 한국어 품질 비교 생성·청취는 하지 않았다.

## LLM과 JSON 스키마

| 공급자 | 기능·요청 이름 | 저비용/표준 후보·기본 종량 단가(입력/출력 100만 토큰) | 무료·주의 |
|---|---|---|---|
| OpenAI | Structured Outputs. Responses `text.format={type:"json_schema",name,schema,strict:true}`; Chat Completions `response_format` | `gpt-6-luna` $0.10/$0.50, `gpt-6.1-sol` $2/$10 | 고정 무료 지급을 전제하지 않음. ChatGPT 구독과 API 별도 |
| Gemini | Structured output. `response_mime_type="application/json"`와 `response_json_schema`(SDK Pydantic은 `response_schema` 등 예제 대조) | 신규 접근 후보 `gemini-3.5-flash-lite` $0.30/$2.50. `gemini-3.8-flash` 입력$0.75·출력$3.75(2026-12-31까지 프로모션, 2027 재확인) | 지원 모델 Free Tier·프로젝트 rate limit 존재. 무료 데이터 이용 조건과 유료 조건 구별 |
| Anthropic | Structured outputs `output_config.format={type:"json_schema",schema}`; 도구는 `strict:true` | Claude Haiku5.5 $0.10/$0.50(입력10만 토큰 이하), Sonnet5.5 $2/$10 | 일회성 체험/구독 크레딧은 상시 무료 등급과 다름 |

[A025](SOURCES.md#a025) [A026](SOURCES.md#a026) [A028](SOURCES.md#a028) [A029](SOURCES.md#a029) [A032](SOURCES.md#a032) [A033](SOURCES.md#a033). Anthropic 현행 API 문서 버전은 `2026-10-21`이며 예제 SDK/API 버전과 섞지 않는다. [A123](SOURCES.md#a123)

선택 모델 카드의 Structured outputs 지원과 API 접근 상태를 호출 전에 확인한다. 스키마 준수는 사실 정확성·출처 진위·길이의 읽기 쉬움까지 보장하지 않는다. 각 공급자의 JSON Schema 지원 부분집합을 사용한다. OpenAI는 모든 필드 required·필요한 nullable·`additionalProperties:false` 등을 확인하고, 거절·출력 잘림을 정상 콘텐츠와 분리한다. 파싱 실패를 자동 게시로 우회하지 않는다. Gemini 2.5 가격표가 남아 있어도 신규 계정 접근 제한·종료 일정을 확인한다. [A026](SOURCES.md#a026) [A029](SOURCES.md#a029) [A033](SOURCES.md#a033) [A077](SOURCES.md#a077)

**추천(편집 제안):** 기존 키트의 JSON 출력 규칙을 기준으로 저비용 `gpt-6-luna` 한 공급자부터 배운다. 무료 연습은 `mock` 또는 지원되는 Gemini 무료 모델을 고른다. 한국어 원문·숫자 검수는 사람에게 남기고, 고품질 예산 비교에는 `gpt-6.1-sol`을 쓴다. 공급자 3개를 처음부터 모두 구현해야 한다는 뜻이 아니다.

## 이미지·영상: 종료 모델을 새 실습에 넣지 않기

| API | 현재 확인·가격 | 제약·권장 |
|---|---|---|
| OpenAI Images | 현재 새 통합 가이드는 GPT Image2.5 Sunburst/Flare 권장. 이미지 토큰 입$8/출$30/100만, 텍스트 입력$5. 기존 `gpt-image-2` 비교표: 1024² low$0.006·medium$0.053·high$0.211 **출력만** | 입력 프롬프트·참조 이미지 추가 과금. 2.5는 전용 계산기로 크기·품질 견적; 2의 가격을 2.5에 적용 금지 |
| Gemini 이미지 | `gemini-nano-banana-2.1`, 신규1K 출력 약$0.0336/장(1120 image tokens), 입력 별도; 3.1 Flash Image 등 모델별 가격 다름 | 무료 이미지 API를 기본 전제하지 않음. 로고·한글 문안은 로컬 렌더 |
| Imagen | Gemini API Imagen4는 2026-08-17 종료 기록 | 남은 가격표를 현행 서비스로 안내하지 않음. Cloud 쪽 별도 모델 수명 확인 |
| Gemini API Veo | 3.1 Preview 세 ID가 2026-10-22 종료 | 신규 API 호출 예제 제외. `gemini-omni-1.1-flash` 또는 별도 Cloud GA로 이동 |
| Gemini Omni Flash | 유료만. 입력$1.50/100만, 출력 텍스트$9·영상$17.50/100만 토큰 | 영상 초당 고정값으로 임의 환산 금지; 해상도/길이/생성 결과의 과금 토큰 확인 |
| Runway Dev | $0.01/credit. `gen4_turbo`5credits/초=$0.05/초, `gen4.5`12=$0.12/초, `veo3.1_fast` 오디오15=$0.15/초·무음10=$0.10/초 | Runway 앱 구독 크레딧과 Dev 프로젝트 별도. 최소충전·세금·실패 과금은 현재 포털에서 확인 |

[A025](SOURCES.md#a025) [A035](SOURCES.md#a035) [A101](SOURCES.md#a101) [A028](SOURCES.md#a028) [A102](SOURCES.md#a102) [A077](SOURCES.md#a077) [A036](SOURCES.md#a036) [A037](SOURCES.md#a037).

`gpt-image-1`은 2026-10-23 종료 안내가 있다. `gpt-image-1-mini`·1.5도 모델 상태를 확인하고 저렴하다는 이유만으로 신규 기본값에 고정하지 않는다. [A035](SOURCES.md#a035) [A100](SOURCES.md#a100)

**추천:** 기본 쇼츠는 이미지/보유 소재+ffmpeg로 조립한다. 생성 영상은 5~10초 선택 샷으로 시작한다. Runway에서 판매하는 Veo는 Google Developer API의 종료된 Preview와 판매 경로가 다르므로 ‘Veo 전체 종료’라고 쓰지 않는다. 추가 후보 Luma Ray3.2의 공식 API 표는 SDR T2V/I2V 5초에 540p$0.15·720p$0.30·1080p$1.20, 10초에$0.45/$0.90/$3.60을 제시한다. HDR/EXR는 배수 과금이다. 앱 크레딧과 분리하고 한국 카드 승인·실제 API 이용은 미검증으로 둔다. [A129](SOURCES.md#a129)

## 한국어 TTS

아래 600자는 **비용 가정**이다. 한국어600자가 정확히60초라는 음성 측정 결과가 아니다. 실제 길이는 생성한 파일로 측정한다.

| API·후보 | 한국어·가격·무료량 | 600자×30편 비용 가정 |
|---|---|---|
| Google Cloud WaveNet | `ko-KR` 지원. 월400만자 무료 후 $4/100만자 | 무료량 남으면$0; 전부 유료면$0.072 |
| Google Cloud Chirp3 HD | `ko-KR-Chirp3-HD-*` 지원. 월100만자 무료 후 $30/100만자 | 무료량 남으면$0; 전부 유료면$0.54 |
| OpenAI `gpt-4o-mini-tts` | 한국어 지원. 텍스트 입$0.60/100만·오디오 출$12/100만; 과거 분당 견적과 실제 토큰 과금을 구별 | 현재 API 토큰으로 계산. **2027-01-06 종료 예정**이라 신규 기본 경로 제외 |
| ElevenAPI Flash/Turbo / v3 | 한국어 지원 모델을 선택. Flash/Turbo $0.04/천자, v3 $0.08/천자. Free/PAYG·Starter 정상$6/월, 모델별 포함문자량 | 단순 사용가치$0.72/$1.44. Starter를 고르면 소량 사용해도 실제 정기지출$6. Free 비상업/상업 조건 별도 |
| Typecast API | SSFM3.0·한국어 지원. Free월15k credits·비상업·출처 표시. Lite$15/월·200k, 초과$0.09/천자; 1자1credit | 18k자는 Free량도 초과. 수익용은 유료 권리 확인 후 Lite 실제$15/월. 포함량 배분$1.35를 실제 결제액이라고 쓰지 않음 |

[A038](SOURCES.md#a038) [A039](SOURCES.md#a039) [A040](SOURCES.md#a040) [A121](SOURCES.md#a121) [A100](SOURCES.md#a100) [A041](SOURCES.md#a041) [A042](SOURCES.md#a042) [A113](SOURCES.md#a113) [A114](SOURCES.md#a114).

Google 무료량에도 결제 활성화·다른 프로젝트 합산 사용·요청 quota 조건을 확인한다. OpenAI 음성은 AI 음성임을 사용자에게 명확히 알리라는 API 안내가 있다. Typecast Studio 요금과 API 요금은 별도다. Typecast 유료 초과는 Lite100k당$9·Plus1.25M당$100 자동 추가 청구이므로 ‘월15달러면 끝’이라고 쓰지 않는다. 30k라고 남은 구형 검색 발췌보다 현재 가격표15k를 우선한다.

## 지출 상한·알림 설정 위치

| 공급자 | 설정 위치·강제 중지 | 남은 확인/운영 제안 |
|---|---|---|
| OpenAI | Organization limits 또는 Project settings → Limits → Spend → Edit spend limit → Monthly spend limit → **Enforce a hard limit** → Save. Spend alerts 별도 | 2026-07-22 도입. 강제 한도 도달시429·전파 지연으로 소액 초과 가능. 알림만 설정한 상태와 구별 [A081](SOURCES.md#a081)[A082](SOURCES.md#a082) |
| Gemini API | AI Studio → Spend → Monthly spend cap → Edit spend cap. Billing의 Prepay/Auto-reload·Monthly auto-charge limit | 프로젝트 cap은 실험 기능·약10분 과금지연; 장기 작업 초과 가능. 신규 Prepay 최소$5, 자동충전 한도는 수동충전 제외. 계정 tier cap도 별도 [A030](SOURCES.md#a030) |
| Google Cloud TTS/GCS/Cloud 생성 | Cloud Billing → Budgets & alerts → Create budget → 대상/임계치/수신자 | **예산 알림만으로 서비스 정지 안 됨**. API quota는 요금 상한과 다름. Gemini AI Studio cap이 Cloud 전체를 막지 않음 [A031](SOURCES.md#a031) |
| Anthropic 직접 API | Claude Console → Billing 조직 월상한; Workspaces → 대상 → Spend limits에서 workspace 상한·알림 | 조직 서비스 한도 안에서 더 낮게 설정. **Default Workspace는 spend limit 설정 불가**이므로 별도 workspace 사용. AWS/Cloud 판매 경로는 결제·제어가 다름 [A034](SOURCES.md#a034)[A115](SOURCES.md#a115) |
| Runway Dev | 개발자 포털의 프로젝트 Credits/Billing·충전/사용량 확인 | 선불·자동충전 설정을 확인. 초보가 지정할 강제 월상한/메일알림의 정확한 공통 UI는 미확인. 자동충전 끄기+로컬 호출예산 제안 [A037](SOURCES.md#a037)[A134](SOURCES.md#a134) |
| ElevenAPI | ElevenLabs → Subscription/Usage·API key 설정과 credit/character 사용한도 확인 | API 달러결제·Creative 구독 잔량 구분. 현재 계정에서 초과사용·auto top-up·key cap 제공 범위 확인; 구형 초과크레딧 메뉴를 그대로 복사 금지 [A041](SOURCES.md#a041)[A133](SOURCES.md#a133) |
| Typecast API | API Dashboard의 사용량·요금제 | 공개 가격표에 사용자 지정 hard cap/예산 메일 경로 미기재. 무료 소진과 유료 자동 초과청구를 구분; 지원센터에 초과차단 가능 여부 확인 [A113](SOURCES.md#a113)[A114](SOURCES.md#a114) |

위 표의 약식 출처 A번호는 [SOURCES](SOURCES.md)에 연결된다. ‘설정 가능’과 ‘정확한 한국 콘솔 위치 확인’을 구분했다. 본인 계정의 메뉴·권한·카드 결제는 시험하지 않았다.

**코드 예산 설계 제안:** 요청 전에 최대입력/출력·이미지수·영상초수·남은 월예산을 확인해 예상최대비를 예약하고, 응답의 실제 usage를 기록한다. 유료생성은 재시도 횟수도 비용에 포함한다. 여러 실행기가 같은 예산을 쓰면 원자적으로 잔액을 차감해야 한다. 이 단계에서 구현한 기능은 아니다.

## 한국 가용성·반영

OpenAI·Gemini·Anthropic 공식 지원지역에 한국이 있다. 이는 국내 데이터 보관·모든 모델/기능·국내 카드 승인까지 보장하지 않는다. [A135](SOURCES.md#a135) [A136](SOURCES.md#a136) [A152](SOURCES.md#a152). Google `ko-KR` 음성·Typecast 한국어 지원과 한국어 발음 품질의 실측 순위도 구분한다. 신규 유료 키·결제·생성을 하지 않았다. A2/A3/A4에 반영한다.
