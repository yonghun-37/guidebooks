# API 완전 자동화 심화편 조사 브리핑

**2026년 10월 조사 기준 · 2026-10-26 확인.** 결론: **키 없이 mock로 완주 → 로컬에서 생성/렌더·사람 승인 → 본인 계정의 소량 private/시험 게시 → 지속 상태·예산·일정 운영** 순서가 적합하다. 이번 단계는 문서 조사이며 구현·실계정 성공 검증을 하지 않았다. [기존 근거 재사용표](00-scope-reuse.md), [학습자 질문50개](../docs/learner-questions-advanced.md), [사실표](FACT-SHEET.md), [출처](SOURCES.md)를 함께 본다.

## ① 인스타 자동화 결론

**신규 서비스의 공식 권장은 Unified Login, 기존 본인 계정 학습 키트는 Instagram Login 유지**다. Unified는 비즈니스 포트폴리오가 필요하며, Instagram Login은 Facebook 페이지가 필요 없다. Facebook Login은 연결 페이지가 필요하다. 세 경로의 토큰·호스트·scope를 섞지 않는다. [A001](SOURCES.md#a001) [A084](SOURCES.md#a084)

준비물:

1. 본인 Business/Creator 프로페셔널 계정과 복구 가능한 로그인 수단.
2. Meta 개발자 계정·Business 앱·Instagram 제품, 앱 역할/테스터 연결·수락.
3. Instagram Login의 `instagram_business_basic`, `instagram_business_content_publish`; 분석 때 insights scope 추가.
4. 사용자 ID·토큰·만료일을 비공개 저장. 생성기 토큰60일, OAuth 단기1시간→장기60일; 발급24시간 후·만료 전에 갱신.
5. JPEG/MP4와 Meta가 읽을 공개 URL, 사람 승인·완료 ID·실패 알림.

본인 소유·관리 계정의 Standard Access는 공식 검수 표에서 App Review 불필요다. 외부 고객 계정 Advanced는 검수·Business Verification 대상이다. 생성 가이드의 앱 공개/live data 검수 요구와의 범위 차이를 보존하고, 개발 모드 테스트의 실제 가시성을 사용자 확인 항목으로 둔다. [A004](SOURCES.md#a004) [A111](SOURCES.md#a111) [A083](SOURCES.md#a083) [A005](SOURCES.md#a005)

게시: `media` 컨테이너 생성 → `status_code=FINISHED` → `media_publish`. 캐러셀 부모만 발행한다. 이미지 JPEG≤8MB·4:5~1.91:1; 릴스 MOV/MP4·H.264/HEVC·AAC·3초~15분·≤300MB. Story의 계정·길이는 별도다. [A006](SOURCES.md#a006) [A007](SOURCES.md#a007)

한도: 공식 일반100/이동24시간과 캐러셀/레퍼런스50이 **상충**한다. `content_publishing_limit?fields=quota_usage,config`로 계정값을 읽는다. 교육은 하루1건, 방어적 상한50 이하·실제 계정값 우선. 조회 실패시100을 기본값으로 넣지 않는다. [A008](SOURCES.md#a008)

공개 URL: 첫 비민감 교육용 JPEG는 별도 Pages, 일상 운영은 과금 조건을 확인한 R2 Standard/GCS를 선택한다. `r2.dev`는 개발용이다. Facebook Login for Business의 영상 resumable은 로컬 바이너리로 공개 영상 URL을 대체하지만 **Instagram Login 지원으로 확대하지 않는다**. [A047](SOURCES.md#a047) [A048](SOURCES.md#a048) [A049](SOURCES.md#a049) [A142](SOURCES.md#a142)

AI는 `is_ai_generated`(캐러셀 부모), 협찬은 Facebook Login의 별도 파라미터. 음악은 **Audio API가 존재**하고 Facebook/Unified의 릴스에 허용 오디오를 붙일 수 있지만 Instagram Login은 미지원이다. [A006](SOURCES.md#a006) [A125](SOURCES.md#a125). 상세: [계정·토큰](instagram-auth.md), [게시·분석](instagram-publishing.md).

## ② 쇼츠 자동화 결론

**OAuth Desktop app+본인 브라우저 동의 후 로컬 refresh token을 비공개 보관**한다. External Testing7일 만료는 매일 운영의 핵심 장애다. 장기 운영 전 Production/개인 사용 예외·scope 검증 요건을 확인하고 새로 동의한다. OAuth 검증과 YouTube API 감사는 구분한다. [A017](SOURCES.md#a017) [A018](SOURCES.md#a018)

| 항목 | 조사 결론 |
|---|---|
| 기본 업로드 할당량 | videos.insert 전용100회/일·1unit/호출 → 한 편1insert라면 **이론상100편/일** |
| 다른 호출 | search100회/일 별도·나머지10,000units/일; 실패도 차감·채널 업로드 제한 별도 |
| 감사 전 | 현행 insert의 비공개 제한 없음 문장과 한국어 잠금 도움말 상충. 첫 private 전송 후 Studio·메일 확인 |
| 잠김/감사 후 | 잠김은 public 설정 반복으로 해제하지 않음. API 감사/공식 업로드 선택; 감사 승인 범위·추가 quota는 각각 확인 |
| 감사 신청 | 공식 Audit and Quota Extension Form. 프로젝트·사용 사례·시연·정책 준수 자료; 보장 처리일 미확인 |
| 재개 | Location 세션+PUT, 308 Range 다음부터; 마지막 외256KiB 배수. 공개 영상 URL 불필요 |
| Shorts/AI | 일반 채널 정사각/세로≤3분; `isShorts` 업로드 필드 없음. `status.containsSyntheticMedia` 지원 |
| 예약·썸네일 | `publishAt`은 private·미공개 이력 조건. API thumbnail 상한50MB·현재 PC Studio Shorts 파일 업로드 안내 |

[A012](SOURCES.md#a012) [A013](SOURCES.md#a013) [A014](SOURCES.md#a014) [A015](SOURCES.md#a015) [A016](SOURCES.md#a016) [A019](SOURCES.md#a019) [A020](SOURCES.md#a020) [A022](SOURCES.md#a022) [A124](SOURCES.md#a124).

분석은 별도 readonly/monetary scope와 `reports.query`. `views`·`engagedViews`·시청시간·구독·수익을 분모/단위와 함께 수집한다. Instagram 지표는 최대48시간 지연, YouTube는 요청한 모든 지표가 준비된 마지막 날짜까지만 반환하므로 오늘 빈 값은0과 구분한다. [A023](SOURCES.md#a023) [A024](SOURCES.md#a024) [A109](SOURCES.md#a109). 상세: [YouTube API](youtube-api.md).

## ③ 생성 API 추천·편당/월 비용

**최소 유료 조합:** GPT-6 Luna 구조화 문안+보유소재/로컬 카드+Google WaveNet+ffmpeg. 무료 시작은 mock 또는 지원되는 Gemini 무료 텍스트 모델+본인 소재. **고품질 목표 비교안:** GPT-6.1 Sol+AI 이미지+Chirp3 HD. 이는 실측 품질 순위가 아니다.

가정: 플랫폼별 하루1편×30일, LLM 입력3천/출력1천tokens, 카드5장 중AI배경1개, 쇼츠600자/AI장면6장. 이미지는 Gemini NanoBanana2.1 1K($0.0336+텍스트입력100tokens$0.00015)를 사용한다. 추론·검색·참조입력 등 추가 과금이 없는 가정이며 모델/해상도를 바꾸면 재견적한다. [A025](SOURCES.md#a025) [A028](SOURCES.md#a028) [A038](SOURCES.md#a038)

| 조합 | 편당(음성 무료 소진 후) | 월30편 | 음성 무료량이 남은 월30편 |
|---|---:|---:|---:|
| 인스타 저비용 | $0.00080 | $0.02400 | $0.02400 |
| 인스타 고품질 목표 | $0.04975 | $1.49250 | $1.49250 |
| 쇼츠 저비용 | $0.00320 | $0.09600 | $0.02400 |
| 쇼츠 고품질 목표 | $0.23650 | $7.09500 | $6.55500 |
| **두 플랫폼 저비용** | **$0.00400/일** | **$0.12000** | **$0.04800** |
| **두 플랫폼 고품질 목표** | **$0.28625/일** | **$8.58750** | **$8.04750** |

생성비에만20% 추가 생성 허용량을 주면 고품질 월$10.305. 실제 청구·성공률 예측이 아니다. 세금·환율수수료·고정구독·최소충전·호스팅/전기·추가추론/도구는 별도다. Typecast Lite를 선택하면 사용분 계산이 작아도 실제$15/월, ElevenAPI Starter면 정상$6/월이다. 영상10초를 Runway gen4_turbo로 생성하면 추가$0.50/편·월$15이며 전량60초는월$90이다. [A113](SOURCES.md#a113) [A041](SOURCES.md#a041) [A037](SOURCES.md#a037)

종료 주의: Gemini API Imagen4 종료(8/17), Veo3.1 Preview 종료(10/22), OpenAI GPT Image1 종료(10/23), Speech API 기존 TTS 종료 예정(2027-01-06). 새 실습은 현재 모델/지원 판매 경로를 명시한다. [A077](SOURCES.md#a077) [A036](SOURCES.md#a036) [A100](SOURCES.md#a100)

지출 관리: OpenAI의 **Enforce a hard limit**, Gemini AI Studio의 project spend cap/Prepay, Anthropic 조직/workspace spend limit을 확인한다. Google Cloud **budget alert만으로 중지되지 않는다**. 상한 전파지연·재시도비를 고려해 로컬 요청 예산도 둔다. [A081](SOURCES.md#a081) [A030](SOURCES.md#a030) [A031](SOURCES.md#a031) [A115](SOURCES.md#a115). 상세: [생성 API](generation-apis.md), [비용 산식](costs.md), [계산 데이터](cost-model.json).

## ④ 실행 방식 추천

| 선택 | 추천 시점 | 꼭 가르칠 것 |
|---|---|---|
| 로컬 | 첫 완주·실패 복구 | Python/ffmpeg 절대경로·cwd·스케줄러 사용자·절전·상태파일 |
| GitHub Actions | PC를 계속 켤 수 없고 짧은 일일작업 | 기본5분·timezone 지원·지연/누락·60일 비활성·Secrets·외부 상태 |
| n8n | 승인/여러 서비스 연결을 화면으로 관리 | Community 라이선스·서버 관리·API 별도비용·HTTP 게시·자격증명 |

공개 표준runner 무료, 비공개 GitHub Free월2천분·artifact500MB. n8n Cloud Starter연€240(월환산€20), Make Free1천credits/월·15분·작은파일제한, Zapier Free100tasks/월. 단위를 게시편수로 바꾸지 않는다. [A044](SOURCES.md#a044) [A045](SOURCES.md#a045) [A055](SOURCES.md#a055) [A131](SOURCES.md#a131) [A062](SOURCES.md#a062). 상세: [호스팅·실행](execution-hosting.md), [노코드](nocode.md).

## ⑤ 승인 방식 추천

로컬 승인 파일 → Telegram inline button+long polling → 필요할 때 Discord app interactions 순서다. Discord incoming webhook은 알림만으로 시작한다. 링크 버튼과 승인 callback은 다르다. Discord interaction은3초 ACK·HTTP 서명, Telegram은 사용자/채팅·callback·중복 update 검증이 필요하다. 생성 해시·문안·계정·공개범위·AI표시·예약시각을 승인에 묶고 수정되면 재승인한다. [A065](SOURCES.md#a065) [A067](SOURCES.md#a067) [A144](SOURCES.md#a144) [A145](SOURCES.md#a145). 상세: [승인·보안](approval-security.md).

## ⑥ 위험과 회피

- 응답 유실·중복: 컨테이너/세션/게시 ID 기록, 동일 상태 조회 후 재개. 모르는 상태를 미게시로 단정하지 않음.
- 비용: 키만 지키는 것으로 부족. 강제 상한·알림·최대 생성 수/초수·재시도 예산을 함께 설정.
- 콘텐츠: 사실·원본·권리 검수와 독창적 해설. API 사용은 스팸/재사용 정책 면제 아님.
- AI 표시: 사실적 합성 공개를 판정하고 실제 필드를 전송. 표시 자체와 콘텐츠 위반을 구분.
- 키 유출: 실행 중지→폐기/회전→사용·청구 점검→Secrets 교체→필요한 이력 정리. 파일 삭제만으로 해결하지 않음.

2025-07-15 YouTube 변경은 반복/대량생산 정책 명확화이며 AI 전면금지가 아니다. 2025년 가짜 예고편 채널 종료와2026년 대변인이 확인한 일부 AI 채널 스팸 제재는 자동화의 실무 위험 사례다. 공식 API라는 이유의 인스타 도달 차이는 근거 미확보; YouTube AI 공개 자체는 도달/수익자격을 제한하지 않는다는 공식 안내가 있다. [A070](SOURCES.md#a070) [A071](SOURCES.md#a071) [A128](SOURCES.md#a128) [A161](SOURCES.md#a161) [A075](SOURCES.md#a075). 상세: [정책](policy-safety.md), [실제 구조·실패](cases-operations.md).

## ⑦ 상충·미확인과 직접 확인법

| 남은 항목 | 사용자가 확인할 방법 |
|---|---|
| 인스타50/100·config 예제 불일치 | 본인 token으로 limit 읽고 버전·필드·반환한도 기록. 실패시 임의100 적용 금지 |
| 본인 Standard와 공개/live data 검수 문구 | Dashboard 역할·Access Level·앱 모드·검수 가이드 대조, 본인 시험 게시와 일반 시청 가시성 확인 |
| Creator Story·Unified/Audio 준비 조건 | 해당 로그인별 권한/포트폴리오·페이지 요건과 실제 메뉴/반환을 확인 |
| 미검증 YouTube 비공개 잠금 | private1개 전송 후 Studio 제한·메일·API status, 필요시 감사팀 문의 |
| 감사 처리 기간·결과 | 공식 양식 후속메일; 확정 완료일을 일정에 약속하지 않음 |
| 한국 결제·UI·TTS 자연스러움 | 본인 계정 결제 통화/초과옵션·지원 지역 확인, 발음표본 미리듣기. 이번 실결제/청취 없음 |
| Runway/Typecast 등의 hard cap·알림 | 계정 Billing/Usage와 지원센터에 초과중지/예산알림 제공 여부 확인. 공개 문서에 없는 메뉴를 만들지 않음 |
| 신규/종료 모델·노코드 필드·분석 조합 | 현재 모델 목록·deprecations·모듈 advanced fields·insights 지원표에서 재확인 |
| 신뢰도/빈본문 | SOURCES 확인 수준·verification.json·질의 품질표를 확인. HTTP200 제목만은 본문 확인으로 세지 않음 |

설계서는 수정하지 않았다. [A1 결과와 설계 조정 제안](../docs/results/phase-A1.md)을 Claude 검수에 넘긴다. 실계정 게시·한국 카드 승인·음성 품질·일정 정시성은 이번 완료 범위 밖의 사용자 확인 항목이다.
