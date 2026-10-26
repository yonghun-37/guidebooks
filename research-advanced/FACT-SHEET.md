# 심화편 사실표

2026년 10월 조사 기준 · 2026-10-26. ADV-는 연구 문서용이며 교과서 본문에 노출하지 않는다. `확인`은 문서 근거 확인이며 실계정 실행 성공이 아니다. 상충/미확인을 완료 사실로 바꾸지 않는다. 가격/무료량의 상세 조건은 주제 노트와 SOURCES를 따른다.

| ID | 주장 | 출처 | 장 | 판정 |
|---|---|---|---|---|
| ADV-001 | 새 통합의 Meta 권장은 Unified Login이며 비즈니스 포트폴리오가 필요하다. | [A001](SOURCES.md#a001) [A084](SOURCES.md#a084) | A0/A5 | 확인 |
| ADV-002 | Instagram Login은 페이지 불필요, Facebook Login은 연결 페이지 필요; Business/Creator 대상이다. | [A001](SOURCES.md#a001) [A002](SOURCES.md#a002) [A003](SOURCES.md#a003) | A0/A5 | 확인 |
| ADV-003 | Instagram Login 게시 기본 권한은 instagram_business_basic·instagram_business_content_publish다. | [A002](SOURCES.md#a002) [A005](SOURCES.md#a005) | A2/A5 | 확인 |
| ADV-004 | 본인 소유·관리 계정 Standard Access는 App Review 불필요라는 개발 시나리오 표가 있다. | [A004](SOURCES.md#a004) | A2/A5 | 조건부 확인 |
| ADV-005 | 외부 고객 계정 Advanced Access는 검수·Business Verification 대상이다. | [A001](SOURCES.md#a001) [A004](SOURCES.md#a004) | A2/A5 | 확인 |
| ADV-006 | 앱 생성 문서의 live data 검수·공개 요구와 Standard 예외의 적용 범위/실제 가시성은 추가 사용자 확인이다. | [A111](SOURCES.md#a111) [A004](SOURCES.md#a004) | A5 | 범위 상충/실기능 미검증 |
| ADV-007 | Instagram OAuth 단기1시간·장기/생성기60일이며 장기 갱신은 발급24시간 이후·만료 전이다. | [A083](SOURCES.md#a083) [A005](SOURCES.md#a005) | A2/A6 | 확인 |
| ADV-008 | Unified는 포트폴리오 소속 SUAT이며 만료는 로그인 구성에 따라 선택한다. | [A112](SOURCES.md#a112) | A2/A5 | 확인 |
| ADV-009 | 피드 이미지는 JPEG≤8MB·너비320~1440·4:5~1.91:1이다. | [A007](SOURCES.md#a007) | A4/A5 | 확인 |
| ADV-010 | 릴스 API는 MOV/MP4·H264/HEVC·AAC·23~60fps·3초~15분·≤300MB를 명시한다. | [A007](SOURCES.md#a007) | A4/A5 | 확인 |
| ADV-011 | Story 영상은3~60초·≤100MB이며 Facebook Login Story는 Business 한정이다. | [A007](SOURCES.md#a007) [A003](SOURCES.md#a003) | A4/A5 | 로그인 범위 한정 |
| ADV-012 | 게시 가이드 캐러셀 최대20개와 오류표2~10개 문구가 상충한다. | [A006](SOURCES.md#a006) [A009](SOURCES.md#a009) | A5 | 상충, 교육5장 제안 |
| ADV-013 | 게시 흐름은 media 컨테이너→상태 FINISHED→media_publish이며 컨테이너ID와 게시ID는 다르다. | [A006](SOURCES.md#a006) [A007](SOURCES.md#a007) | A1/A5 | 확인 |
| ADV-014 | URL 방식은 Meta가 인증 없이 읽을 수 있는 파일 URL이 필요하다. | [A006](SOURCES.md#a006) [A007](SOURCES.md#a007) | A5 | 확인 |
| ADV-015 | 영상 resumable은 Facebook Login for Business 경로에 명시되며 Instagram Login 지원으로 확대할 수 없다. | [A006](SOURCES.md#a006) [A142](SOURCES.md#a142) | A5 | 현재 지원 범위 확인 |
| ADV-016 | 미발행 컨테이너24시간 만료·계정당400개/24시간 생성과 발행 한도는 다른 단위다. | [A007](SOURCES.md#a007) | A1/A5 | 확인 |
| ADV-017 | 게시 한도 일반100/이동24시간과 캐러셀·limit reference50이 공식 문서에서 상충한다. | [A006](SOURCES.md#a006) [A008](SOURCES.md#a008) | A5 | 상충 미해결 |
| ADV-018 | limit의 quota_usage는 사용량, config의 quota_total·quota_duration은 총량/기간이며 예제 요청필드에 불일치가 있다. | [A008](SOURCES.md#a008) | A5/A6 | 문서스키마 확인·실응답 미검증 |
| ADV-019 | AI 공개 is_ai_generated는 양 기존 로그인 지원·캐러셀 부모만 설정한다. | [A006](SOURCES.md#a006) [A011](SOURCES.md#a011) | A5/A9 | 확인 |
| ADV-020 | 파트너십 is_paid_partnership·branded_content_sponsor_ids는 현재 가이드에서 Facebook Login 지원이다. | [A006](SOURCES.md#a006) | A5/A9 | 범위 확인 |
| ADV-021 | Audio API는 Facebook/Unified Reels 오디오 검색/부착을 지원하며 Instagram Login은 미지원이다. | [A125](SOURCES.md#a125) [A011](SOURCES.md#a011) | A5/A9 | 지원 확인·한국곡목 미검증 |
| ADV-022 | Audio API 소개의 Unified 지원과 Before You Start 페이지/User token 요건의 구체 조합은 재확인 대상이다. | [A125](SOURCES.md#a125) [A084](SOURCES.md#a084) | A5 | 준비 조건 공백 |
| ADV-023 | Meta 오류9007/2207027은 미디어 미준비,9004/2207052는URL가져오기,9/2207042는게시한도다. | [A009](SOURCES.md#a009) | A5/A6 | 확인 |
| ADV-024 | Instagram 지표는 계산 데이터가 최대48시간 지연될 수 있고 미지원/미준비 빈 데이터는0과 다르다. | [A085](SOURCES.md#a085) [A109](SOURCES.md#a109) [A110](SOURCES.md#a110) | A8 | 확인 |
| ADV-025 | Instagram views·reach·saved·shares와 릴스 watch time 등은 미디어별 지원표를 따라 요청한다. | [A109](SOURCES.md#a109) [A110](SOURCES.md#a110) | A8 | 확인 |
| ADV-026 | YouTube 개인 채널 자동화는 OAuth Desktop app·시스템 브라우저/loopback 동의를 사용한다. | [A017](SOURCES.md#a017) | A2/A5 | 확인 |
| ADV-027 | External Testing refresh token7일 만료의 기본프로필 예외는 youtube.upload에 적용되지 않는다. | [A018](SOURCES.md#a018) | A2/A6 | 조건부 확인 |
| ADV-028 | videos.insert는 전용1unit/호출·기본100회/일이며 search100회와 기타10000units는 별도 버킷이다. | [A012](SOURCES.md#a012) [A013](SOURCES.md#a013) [A079](SOURCES.md#a079) | A0/A5 | 현행 확인 |
| ADV-029 | 과거1600→2025-12-04약100→2026-06-01granular quota의 변경 이력이 있다. | [A014](SOURCES.md#a014) | A5 | 날짜 확인 |
| ADV-030 | 현재 insert 비공개 제한 없음과 잠금 도움말의 미검증 API 제한이 상충한다. | [A012](SOURCES.md#a012) [A014](SOURCES.md#a014) [A016](SOURCES.md#a016) | A5 | 상충 미해결 |
| ADV-031 | API 감사·할당량 증설과 OAuth 검증은 다른 절차; 공식 양식은 있으나 보장 처리일은 미확보다. | [A015](SOURCES.md#a015) [A088](SOURCES.md#a088) | A5 | 절차 확인·기간 미확인 |
| ADV-032 | YouTube resumable은 Location·308 Range·마지막 외256KiB 배수로 재개하며 공개URL은 불필요하다. | [A019](SOURCES.md#a019) | A1/A5 | 프로토콜 확인 |
| ADV-033 | publishAt은 private·기공개 이력 없음 조건이며 privacyStatus를 항상 명시하는 편집안을 권장한다. | [A020](SOURCES.md#a020) [A012](SOURCES.md#a012) | A5/A6 | 필드/조건 확인 |
| ADV-034 | selfDeclaredMadeForKids와 containsSyntheticMedia는 서로 다른 status Boolean이다. | [A020](SOURCES.md#a020) | A5/A9 | 확인 |
| ADV-035 | 일반 채널의2024-10-15이후 정사각/세로≤3분은Shorts; 음악 연결 채널은2025-12-08분기 예외가 있다. | [A022](SOURCES.md#a022) | A4/A5 | 조건부 확인 |
| ADV-036 | isShorts는 공식 업로드용 status 필드로 제시되지 않는다. | [A020](SOURCES.md#a020) [A012](SOURCES.md#a012) | A5 | 스키마 대조 |
| ADV-037 | thumbnails.set 최대50MB·약50units, 2026-09-14이력에서2→50MB변경 확인. | [A021](SOURCES.md#a021) [A014](SOURCES.md#a014) | A5 | 현행 확인 |
| ADV-038 | 현재 공식 도움말은 인증 계정의 PC Studio에서 Shorts 썸네일 파일업로드를 안내한다. | [A124](SOURCES.md#a124) | A5 | 문서 확인·UI미실측 |
| ADV-039 | Analytics views·engagedViews·시청시간·구독·추정수익은 단위/보고서 조합·scope를 확인해야 한다. | [A023](SOURCES.md#a023) [A024](SOURCES.md#a024) | A8 | 확인 |
| ADV-040 | Analytics 응답은 요청한 모든 지표가 준비된 마지막 날짜까지만 포함한다. | [A024](SOURCES.md#a024) | A8 | 확인 |
| ADV-041 | OpenAI 구조화출력은 Responses text.format/json_schema와 Chat response_format을 구별한다. | [A026](SOURCES.md#a026) | A3 | 확인 |
| ADV-042 | Gemini response_mime_type+response_json_schema와 Anthropic output_config.format/strict tool use는 이름·지원 schema가 다르다. | [A029](SOURCES.md#a029) [A033](SOURCES.md#a033) | A3 | 확인 |
| ADV-043 | 기본 LLM 단가 Luna입0.10/출0.50,Sol입2/출10달러/100만tokens다. | [A025](SOURCES.md#a025) | A2/A3 | 기본tier·단문 |
| ADV-044 | Gemini3.5FlashLite입0.30/출2.50,3.8Flash입0.75/출3.75는2026연말까지 표시가격이다. | [A028](SOURCES.md#a028) | A3 | 모델별 기간 한정 |
| ADV-045 | Claude Haiku5.5입0.10/출0.50는입력10만tokens이하,Sonnet5.5입2/출10달러다. | [A032](SOURCES.md#a032) | A3 | 조건부 확인 |
| ADV-046 | OpenAI는2026-07-22조직/프로젝트 hard spend limit 도입; 알림과별도·도달시429·소액전파지연가능이다. | [A081](SOURCES.md#a081) [A082](SOURCES.md#a082) | A2 | 현행 확인 |
| ADV-047 | Gemini AI Studio project spend cap은실험기능·약10분지연;Prepay최소5달러·자동충전월한도는수동충전제외다. | [A030](SOURCES.md#a030) | A2 | 조건부 확인 |
| ADV-048 | Cloud Billing budget alert는자동으로사용/과금을멈추지않는다. | [A031](SOURCES.md#a031) | A2/A6 | 확인 |
| ADV-049 | Claude Console조직Billing·workspace Spend limits에서상한과알림을관리한다(Default workspace설정불가). | [A034](SOURCES.md#a034) [A115](SOURCES.md#a115) | A2 | 직접API범위 |
| ADV-050 | NanoBanana2.1은1K출력0.0336달러·입력1.50달러/100만tokens이며추론/검색/참조입력추가과금은별도다. | [A028](SOURCES.md#a028) | A3 | 무료없음·추가출력조건 |
| ADV-051 | OpenAI Image2의1024²medium출력가격0.053달러는입력과별도이며2.5가격으로사용하면안된다. | [A035](SOURCES.md#a035) [A025](SOURCES.md#a025) | A3 | 모델/tier분리 |
| ADV-052 | GeminiAPI Imagen4는2026-08-17, Veo3.1Preview는2026-10-22종료안내다. | [A077](SOURCES.md#a077) [A036](SOURCES.md#a036) | A3 | 종료경로한정 |
| ADV-053 | OpenAI GPTImage1은2026-10-23종료,기존SpeechAPI TTS는2027-01-06종료예정이다. | [A100](SOURCES.md#a100) [A040](SOURCES.md#a040) | A3 | 완료/예정 구분 |
| ADV-054 | GoogleWaveNet월400만자무료후4달러/100만,Chirp3HD월100만자무료후30달러/100만;ko-KR음성지원이다. | [A038](SOURCES.md#a038) [A039](SOURCES.md#a039) | A2/A3 | 무료조건·결제확인 |
| ADV-055 | ElevenAPI Flash/Turbo0.04달러/천자·v3 0.08,Starter정상6달러/월은사용분과구독지출을분리한다. | [A041](SOURCES.md#a041) [A042](SOURCES.md#a042) | A3 | 실결제/품질 미검증 |
| ADV-056 | TypecastAPI Free15k/월비상업·Lite15달러/200k,초과100k당9달러자동추가청구;Studio와별도다. | [A113](SOURCES.md#a113) [A114](SOURCES.md#a114) | A2/A3 | 현행가격표 |
| ADV-057 | RunwayDev 1credit0.01달러·gen4_turbo5credit/초·gen4.5 12credit/초다. | [A037](SOURCES.md#a037) | A3 | 앱구독과별도 |
| ADV-058 | LumaRay3.2 SDR720p 10초0.90달러·1080p3.60달러이며HDR배수는별도다. | [A129](SOURCES.md#a129) | A3 | 한국카드미검증 |
| ADV-059 | Actions schedule최소5분·IANA timezone지원·default branch실행이다. | [A044](SOURCES.md#a044) | A6 | 현행확인 |
| ADV-060 | Actions schedule은지연/드롭가능·공개repo60일비활성시예약비활성화가능이다. | [A044](SOURCES.md#a044) | A6 | 확인 |
| ADV-061 | 표준public Actions무료·private GitHubFree월2000분/artifact500MB·큰runner는별도과금이다. | [A045](SOURCES.md#a045) | A6 | 조건부 확인 |
| ADV-062 | GitHubSecrets저장과인수/로그의노출방지는별도이며새runner작업파일을영속상태로가정하지않는다. | [A046](SOURCES.md#a046) [A155](SOURCES.md#a155) | A2/A6 | 문서+운영추론 |
| ADV-063 | Pages는사이트1GB·월100GBsoft·기본10build/시간soft와상업호스팅제한을명시한다. | [A047](SOURCES.md#a047) | A5/A6 | 교육/상용구분 |
| ADV-064 | R2Standard월10GB-month·A100만/B1000만·egress무료,초과과금·checkout조건이있다. | [A048](SOURCES.md#a048) [A099](SOURCES.md#a099) | A5/A6 | 조건부 확인 |
| ADV-065 | r2.dev는rate-limited개발용이며운영용무료CDN으로보장하지않는다. | [A049](SOURCES.md#a049) | A5/A6 | 확인 |
| ADV-066 | GCS Free는미국3개리전합산5GB·A5천/B5만·북미발egress100GB조건;서울리전무료저장으로확대금지다. | [A050](SOURCES.md#a050) | A5/A6 | 지역조건부 |
| ADV-067 | ffmpeg는공식소스/연결빌드·LGPL/GPL빌드조건을구별하며바이너리재배포의무를확인해야한다. | [A053](SOURCES.md#a053) [A054](SOURCES.md#a054) | A4 | 문서 확인 |
| ADV-068 | n8nCommunity의내부사업자동화무료와서버비무료/유료편집기재판매는다르다. | [A120](SOURCES.md#a120) [A150](SOURCES.md#a150) | A7 | 라이선스범위 |
| ADV-069 | n8nCloud연결제Starter20유로/2500실행·Pro50유로/10000실행표시이며월결제/한국통화는재확인이다. | [A055](SOURCES.md#a055) | A7 | 표시값 한정 |
| ADV-070 | MakeFree월1000credits·최소15분·작은파일/실행제한,Core9/Pro16달러표시는연결제선택값이다. | [A131](SOURCES.md#a131) | A7 | 조건부 확인 |
| ADV-071 | ZapierFree월100tasks·two-step,Professional연결제19.99달러부터·초과pay-per-task설정확인이다. | [A062](SOURCES.md#a062) | A7 | 조건부 확인 |
| ADV-072 | n8nYouTube업로드/OpenAI공식노드는확인했으나Instagram전용공식노드는미확인;HTTP/GraphAPI경로가있다. | [A056](SOURCES.md#a056) [A057](SOURCES.md#a057) [A058](SOURCES.md#a058) | A7 | 확인/미확인 구분 |
| ADV-073 | MakeFacebookLogin커넥터요건과Meta자체InstagramLogin요건은동일하지않다. | [A060](SOURCES.md#a060) [A002](SOURCES.md#a002) | A7 | 범위 구분 |
| ADV-074 | Discordlinkbutton은interaction을보내지않으며interactive custom_id승인은수신앱이필요하다. | [A066](SOURCES.md#a066) [A144](SOURCES.md#a144) | A6 | 확인 |
| ADV-075 | DiscordHTTP interaction은서명검증·3초응답,follow-up token15분을승인만료와구별한다. | [A065](SOURCES.md#a065) [A145](SOURCES.md#a145) | A6 | 확인 |
| ADV-076 | Telegraminlinebutton callback_query·answerCallbackQuery·getUpdates/webhook수신을지원하며일반소규모봇과유료broadcast는다르다. | [A067](SOURCES.md#a067) [A143](SOURCES.md#a143) | A6 | 확인 |
| ADV-077 | YouTube2025-07-15는반복/대량생산정책명확화와명칭변경이며reused content정책변경이아니다. | [A070](SOURCES.md#a070) | A9 | 변경범위 확인 |
| ADV-078 | YouTubeAI공개자체는시청대상이나수익화자격을제한하지않는다고공식도움말이설명한다. | [A071](SOURCES.md#a071) | A9 | 다른정책면제아님 |
| ADV-079 | InstagramAPI게시자체의도달차이를입증하는공식비교근거는확보하지못했다. | [A006](SOURCES.md#a006) | A9 | 조사공백, 부재입증아님 |
| ADV-080 | ScreenCulture/KHStudio종료는2025-12-18보도에서YouTube확인된반복위반사례다. | [A128](SOURCES.md#a128) | A9 | 언론B·AI자체금지로확대금지 |
| ADV-081 | 2026-01-28TheVerge는지목채널중11개스팸등제재를대변인확인으로보도;운영자삭제등과구분한다. | [A161](SOURCES.md#a161) | A9 | 언론B·전체연구목록제재아님 |
| ADV-082 | 노출된비밀은폐기/회전이우선이고파일삭제만으로git이력·fork·clone의비밀을회수할수없다. | [A075](SOURCES.md#a075) [A107](SOURCES.md#a107) [A108](SOURCES.md#a108) [A068](SOURCES.md#a068) | A2/A9 | 보안절차 확인 |
| ADV-083 | 가정된두플랫폼생성비는TTS무료소진후저비용월0.12달러·고품질목표월8.5875달러다. | [A025](SOURCES.md#a025) [A028](SOURCES.md#a028) [A038](SOURCES.md#a038) | A0/A2 | 가상계산·고정비/세금제외 |
| ADV-084 | 한국어지원·국가지역지원·특정카드결제승인·한국리전데이터보관은서로다르다. | [A135](SOURCES.md#a135) [A136](SOURCES.md#a136) [A152](SOURCES.md#a152) [A039](SOURCES.md#a039) [A114](SOURCES.md#a114) | A2/A3 | 지원목록·음성언어 확인, 실결제미검증 |

예산표의 계산 입력/제외 항목은 [cost-model.json](cost-model.json), 구현 제안과 외부 사실의 경계는 [재사용표](00-scope-reuse.md)에 있다.
