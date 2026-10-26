# A6 연결 절차와 무료 운영 답변 보완

2026년 10월 조사 기준. A5r F01/F02/F08/F13에 대한 **Codex 공식 문서 직접 열람** 보충이다. 기존 A1 조사 결과를 재사용했으며 새 Hermes 질의는 실행하지 않았다. 실계정 생성·자격 발급·TTS API 호출·원격 업로드는 수행하지 않았다.

## 공개 파일 호스팅

교육용 무료 경로는 GitHub Free의 **public 별도 저장소**다. Pages에 entry 파일을 만들고 Settings → Pages → Deploy from a branch에서 `media`/root를 선택한다. 키트는 Contents API에 파일을 쓰므로 해당 저장소만 선택한 fine-grained PAT의 Contents 쓰기 권한을 사용한다. URL에는 repo 경로까지 넣는다. [A162](SOURCES.md#a162) [A163](SOURCES.md#a163) [A164](SOURCES.md#a164)

Pages에는 상업 호스팅 제한과 저장/전송/build soft limit가 있다. ‘인스타 자동화 사업의 영구 무료 CDN’으로 확대하지 않는다. R2는 별도 계정·결제 활성화, S3 endpoint·Access Key ID·Secret이 필요하다. 공개 파일용 bucket과 private 상태용 bucket을 분리하고 운영 공개 URL은 사용자 도메인·요금을 확인한다. r2.dev는 개발용이다. [A047](SOURCES.md#a047) [A048](SOURCES.md#a048) [A049](SOURCES.md#a049) [R2 인증](https://developers.cloudflare.com/r2/api/tokens/)

`doctor --live --flow insta`는 로컬 설정·키 존재 확인이다. 발행 한도 조회는 `--check-remote`, 공개 파일의 비인증 GET/MIME/SHA256 검증은 host 단계다. 이것은 키트 코드 확인이며 외부 서비스 사실과 구별한다.

## 권장 TTS 발급

Cloud TTS 프로젝트는 결제 연결과 API 활성화가 필요하다. Cloud Console Credentials에서 standard API key를 만들고 Cloud Text-to-Speech API만 허용한다. 고정 서버 IP가 있다면 IP 제한도 적용한다. 키는 `.env`의 `GOOGLE_TTS_API_KEY`다. 키트의 REST 어댑터는 `x-goog-api-key` 헤더로 보낸다. Gemini AI Studio 키·YouTube 사용자 OAuth 파일과 발급/권한을 구분한다. [A165](SOURCES.md#a165) [A166](SOURCES.md#a166) [A171](SOURCES.md#a171) [A172](SOURCES.md#a172)

TTS의 인증 가이드는 ADC/OAuth를 주로 설명하지만, 공식 v1 Discovery의 parameters.key는 OAuth 토큰이 없으면 API 키가 필요하다고 명시한다. 서비스별 API 키 지원은 이 메타데이터로, 헤더 방식은 Cloud 공통 REST 문서로 대조했다. 프로젝트 정책에 따라 키가 제한되면 사용자는 API 활성화·키의 API/IP 제한을 확인해야 한다. 실제 키의 성공 응답을 확인한 기록은 아니다. WaveNet 무료량/초과 단가는 기존 [A038](SOURCES.md#a038)에 근거한다.

## 메신저 자격과 운영

Discord는 Server Settings → Integrations에서 webhook을 만들고 수신 채널을 선택한 뒤 URL을 복사한다. Telegram은 공식 BotFather의 `/newbot`으로 발급하며, 봇에 개인 메시지를 보낸 뒤 `getUpdates`의 message.from.id·message.chat.id를 읽는다. [A167](SOURCES.md#a167) [A168](SOURCES.md#a168) [A067](SOURCES.md#a067)

키트의 polling은 최대 25초 1회다. Discord는 알림 전용이고, Telegram 승인 수신은 사용자가 켠 터미널/별도 반복 수신 프로세스가 맡는다. OS 예약 생성기는 tick만 호출한다. 수신 후 approve가 기록되어도 게시 실행은 다음 tick/resume의 몫이다. 같은 상태 DB에 수신자를 겹쳐 실행하지 않는다. 이는 코드 확인이다.

## 무료로 매일 한국어 콘텐츠를 만들 수 있나

**소규모 한국어 글 생성은 무료 등급으로 시도할 수 있지만, 매일 무인 성공·전체 구성 0원을 보장할 수 없다.** 가격표의 `gemini-3.5-flash-lite`는 무료 입력/출력 항목이 있다. AI Studio의 해당 프로젝트 active rate limits에서 RPM·TPM·RPD를 직접 확인한다. 한도는 키별이 아닌 프로젝트별이며 일 요청 수는 Pacific 자정에 갱신된다. 고정 RPD 수치를 전 사용자에게 안내하지 않는다. [A028](SOURCES.md#a028) [A169](SOURCES.md#a169)

한국에서 unpaid Gemini 입력·응답은 제품 개선에 사용될 수 있고 사람이 검토할 수 있다. 개인정보·기밀은 넣지 않는다. 유료 프로젝트의 데이터 조건은 다르다. 무료 모델 제공 여부·한도 부족·변경/중단에 대응하려면 대기 후 재개 또는 예산을 정한 유료 모델을 선택한다. 한국어 지원과 발음·사실 정확성은 구분해 한 편을 직접 검수한다. [A170](SOURCES.md#a170) [A135](SOURCES.md#a135)

카드는 무료 LLM+로컬 템플릿+조건에 맞는 교육용 Pages로 API 청구 0원 구성을 시도할 수 있다. 쇼츠는 TTS 무료량이 남아 있거나 새 대본을 직접 녹음하는 경우 로컬 렌더 비용 외 청구를 줄인다. 녹음은 매일 새 작업이므로 무인 경로가 아니다. 이미지/영상 생성 API는 무료라고 전제하지 않는다. 키트는 무료 잔량을 모르므로 **유료 단가로 보수적으로 비용 예약**한다. [A038](SOURCES.md#a038) [A047](SOURCES.md#a047)

## 반영·한계

두 책 A2/A3/A5/A7과 키트 README에 설정값 대응·도식·사용자 확인 위치를 넣는다. 검증은 문서와 오프라인 모킹까지다. 현행 콘솔의 개인 권한·결제 성공·TTS 품질·공개 URL은 독자가 자신의 환경에서 확인한다.

## 편집 견본의 음성 근거

완성 쇼츠 견본은 로컬 Supertonic 3의 기본 한국어 음색으로 생성했다. SDK는 MIT, 모델은 OpenRAIL-M이며 출력 관련 조항과 사용 제한을 구분했다. 라이선스 원문 15007 bytes를 직접 받아 동봉 사본과 일치함을 확인했다. 공식 SDK는 보관소로 이전되어 지원이 끝났으므로 신규 무인 운영 공급자로 권장하지 않는다. 키트 기본 의존성을 늘리지 않고 WAV와 재현 스크립트를 동봉했다. [A173](SOURCES.md#a173) [A174](SOURCES.md#a174)

원고 편집·실제 프레임·기계 역전사 검증은 [견본 기록](../auto-kit/samples/editorial/README.md)에 있다. 사람이 녹음하거나 사람이 청취 감수를 완료한 견본이라고 표시하지 않는다.
