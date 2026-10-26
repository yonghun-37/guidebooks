# Instagram 로그인 경로·앱·권한·토큰

- Hermes 원응답: `/home/yonghun/project/hermes-research/output/advanced-research-20261026/raw/01-instagram-auth.md` · SHA256 `75af27a4e0b1459c0a79bcc9be4a99145e96490fde8825e51e6fc18931d5f923` · exit 0.
- 실행·실패 구분: [provenance.json](provenance.json). 핵심 주장은 Codex 직접 열람/기존 근거와 대조했다.

2026년 10월 조사 기준 · API 예시 v26.0. 기존 `research/graph-api-publishing.md`, `practice-instagram.md`를 재사용하고 현재 공식 본문으로 차이를 확인했다.

## 핵심 결론

**새 상용 통합의 공식 권장은 Unified Login이다. 본인 계정으로 배우는 기존 키트는 Instagram Login 경로를 유지할 수 있다.** 두 추천의 목적이 다르다. Unified는 비즈니스 포트폴리오가 필요하고, Instagram Login은 로그인 자체에서 페이지·포트폴리오를 요구하지 않는다. [A001](SOURCES.md#a001) [A084](SOURCES.md#a084)

| 항목 | Instagram Login | Facebook Login | Unified Login |
|---|---|---|---|
| 계정 | Business/Creator | Business/Creator | 프로페셔널 |
| Facebook 페이지 | 불필요 | 연결 필요 | 불필요 |
| 비즈니스 포트폴리오 | 로그인 흐름상 불필요 | 구성에 따라 | 필요 |
| 호출 호스트 | `graph.instagram.com` | `graph.facebook.com` | `graph.facebook.com` |
| 게시 기본 scope | `instagram_business_basic`, `instagram_business_content_publish` | `instagram_basic`, `instagram_content_publish`, `pages_read_engagement`; 페이지 탐색 권한은 별도 | `instagram_*` 계열; 기존 `instagram_business_*` 그대로 복사 금지 |
| 토큰 | Instagram User | Facebook User/Page | Business Integration System User(SUAT) |
| 선택 | 기존 키트·본인 계정 입문 | 기존 페이지 연결·협찬 라벨/재개 영상 업로드 | 신규 서비스·고객 온보딩 |

개인용 소비자 계정은 지원 대상이 아니다. Story는 Facebook Login 문서에서 Business 한정이다. Creator의 모든 로그인 경로에서 Story가 된다고 확대하지 않는다. [A002](SOURCES.md#a002) [A003](SOURCES.md#a003) [A084](SOURCES.md#a084)

## 본인 계정 준비물과 개발 모드

1. 본인 프로페셔널 계정·복구 수단, Meta 개발자 계정, Meta 앱을 준비한다.
2. 현행 생성 가이드는 `Other` 사용 사례 → `Business` 앱 유형 → Instagram 제품 추가를 설명한다. 화면에 통합형 Instagram 사용 사례가 보이면 해당 앱 가이드를 다시 대조한다.
3. 앱의 Instagram 설정에서 테스트할 계정을 추가하고 역할/초대를 수락한다. 역할 수락 위치는 현재 사용자 화면에서 확인한다.
4. 게시 기본 scope만 먼저 허용하고, 분석 단계에서 `instagram_business_manage_insights` 등을 추가한다. 메시지·광고 scope를 기본 필수로 넣지 않는다.
5. `Instagram > API setup with Instagram business login > Generate token`으로 본인 계정 토큰을 만들고 `/me`의 계정 ID를 확인한다. 실제 토큰은 비공개로 보관한다. [A083](SOURCES.md#a083) [A111](SOURCES.md#a111) [A110](SOURCES.md#a110)

**자기 소유·관리 비즈니스 계정만 쓰는 Standard Access는 App Review 불필요라고 공식 표에 명시되어 있다.** 다른 사업자의 계정을 받는 Advanced Access는 앱 검수·Business Verification 대상이다. 개발 모드에서 본인 역할 계정의 허용된 API 테스트와 앱을 일반인에게 공개하는 것은 구분한다. [A004](SOURCES.md#a004) [A001](SOURCES.md#a001)

> 확인할 점: 생성 가이드는 앱 공개 전에 검증된 비즈니스 연결과 검수를 요구하는 문구도 포함한다. 이를 근거로 본인 테스트에도 무조건 사업자 인증이 필요하다고 쓰거나, 반대로 검수 없이 외부 고객까지 받을 수 있다고 쓰지 않는다. App Dashboard의 역할·권한 Access Level·앱 모드·계정 연결 상태를 확인하고, 본인 테스트 게시의 일반 시청자 가시성은 사용자가 확인한다. 이번 조사에서는 로그인·게시하지 않았다. [A111](SOURCES.md#a111)

## 토큰 종류·수명·갱신

| 경로 | 문서값·운영 방법 |
|---|---|
| Instagram OAuth 단기 | 1시간. authorization code를 `api.instagram.com/oauth/access_token`에서 교환 |
| Instagram 장기 | 60일. 유효한 단기 토큰을 `graph.instagram.com/access_token`에서 `ig_exchange_token`으로 교환 |
| Dashboard 생성기 | 장기 60일 토큰이라고 Get Started가 명시 |
| Instagram 갱신 | `graph.instagram.com/refresh_access_token`, `grant_type=ig_refresh_token`; 발급 후 24시간 이상이고 아직 유효할 때 새 60일. 이미 만료됐으면 재인증 |
| Facebook User | 장기 User는 대체로 약 60일. Page 토큰은 발급 경로·권한·사용자 상태에 따라 다르므로 ‘영구’라고 안내하지 않음 |
| Unified SUAT | 구성할 때 만료를 선택. 포트폴리오 소속 토큰이며 로그인한 직원 퇴사에도 유지되는 설계. 60일 User 토큰 갱신 URL을 재사용하지 않음 |

Instagram 수명은 [A083](SOURCES.md#a083) [A005](SOURCES.md#a005), Facebook은 [A106](SOURCES.md#a106), Unified는 [A112](SOURCES.md#a112). 앱 시크릿을 쓰는 교환은 서버/로컬 비공개 프로세스에서 한다.

**편집 제안:** 만료일을 기록하고 만료 전에 주기 갱신·실패 알림을 둔다. ‘매월 갱신’은 여유를 둔 운영 예시이지 Meta의 의무 주기가 아니다. 토큰을 URL·로그·드라이런 JSON에 남기지 않는다.

## 한국 가용성·반영

글로벌 공식 개발자 문서의 한국 배제 조건은 이 범위에서 찾지 못했다. 한국 계정 생성·인증·권한 승인 성공을 보장하지 않는다. 장 A0/A2/A5: 로그인 비교표, 본인 테스트와 고객 서비스 분기, 만료 확인을 실습 성공 기준에 포함한다. Graph 버전은 코드처럼 v26.0을 명시하고 자동 ‘최신’ 별칭을 쓰지 않는다. [A122](SOURCES.md#a122)
