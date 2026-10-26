# 공식 API 게시: 로그인 경로·요건·한도·절차

작성: 2026-10-26, Codex 정리. **2026년 10월 조사 기준**(컷오프: 2026-10-26). Hermes 원응답과 별개인 편집본이다.

- 원응답: `/home/yonghun/project/hermes-research/output/ai-insta-research-20261026/raw/graph-api-publishing.md`
- SHA256: `b8f98f43d4eaea3bbdf36155858dfc2ef2d27d4c6bf75983e8460cc49dd3da03`

## 핵심 사실(출처 각주)

- **API-01 · 확인함**: Instagram Login은 Business/Creator 프로페셔널 계정을 대상으로 하며 Facebook 페이지 연결이 필요 없다. 호스트는 graph.instagram.com, 게시 권한은 instagram_business_basic·instagram_business_content_publish다. [^S002] [^S001]
- **API-02 · 확인함**: Facebook Login은 Facebook 페이지와 연결된 프로페셔널 계정을 대상으로 한다. 게시 가이드의 호스트는 graph.facebook.com, 권한은 instagram_basic·instagram_content_publish·pages_read_engagement이며 페이지 탐색 권한과 별도다. 개인 계정은 지원하지 않는다. [^S033] [^S029] [^S001]
- **API-03 · 확인함**: 자기 소유·관리 계정의 Standard Access와 다른 비즈니스 계정에 제공하는 Advanced Access는 구분된다. 외부 사용자 대상 Advanced Access에는 앱 검수가 필요하며 Overview는 Business Verification도 요구한다. [^S031] [^S030] [^S033]
- **API-04 · 불일치**: 공식 게시 가이드의 일반 한도는 이동 24시간 100건이나 같은 문서 캐러셀 절과 한도 레퍼런스는 50건을 적고 있다. 캐러셀은 한 건으로 계산된다. 계정별 실효 한도와 변경 시행일은 미확인이다. [^S001] [^S003]
- **API-05 · 불일치**: Codex가 읽은 2026-10-20 갱신 게시 가이드는 API 캐러셀 최대 20개를 명시한다. Hermes 초기 응답의 검색 발췌 2~10개와 불일치한다. 앱 발표의 장수와 API 문서를 구분하고 현행 원문을 우선한다. [^S001] [^S036]
- **API-06 · 확인함**: API 이미지 형식은 JPEG이며 미디어 레퍼런스는 최대 8MB, 비율 4:5~1.91:1, 너비 320~1440px를 적고 있다. PNG 학습 산출물을 그대로 API 입력으로 가정하면 안 된다. [^S001] [^S004]
- **API-07 · 확인함**: 릴스 API 레퍼런스는 MOV/MP4, H.264/HEVC, 23~60fps, 3초~15분, 최대 300MB와 9:16 권장 등을 명시한다. 앱에서의 촬영 상한·추천 길이와 다른 범위다. [^S004]
- **API-08 · 확인함**: 게시 흐름은 media 컨테이너 생성, status_code 처리 상태 확인, media_publish 발행이다. URL 가져오기 방식은 Meta가 읽을 수 있는 공개 미디어 URL이 필요하다. Facebook Login 재개 업로드 경로는 rupload.facebook.com이다. [^S001]
- **API-09 · 확인함**: 미발행 컨테이너는 24시간 후 만료되며 계정당 24시간 400개 생성 제한이 문서에 있다. 생성 제한·게시물 발행 한도·일반 API 호출 제한은 다른 단위다. [^S004] [^S001] [^S035]
- **API-10 · 확인함**: Instagram Login 장기 사용자 토큰은 60일 유효하며 발급 후 24시간 이상 지났고 아직 유효한 토큰을 갱신할 수 있다. 앱 시크릿이 포함된 교환 요청은 서버에서 수행한다. 모든 토큰이 영구라는 설명은 부정확하다. [^S030] [^S034]
- **API-11 · 확인함**: 구 business_* scope의 사용 중단일은 2025-01-27이다. 현행 Instagram Login 게시 scope는 instagram_business_content_publish이며 문서 갱신일을 기능 도입일로 바꾸면 안 된다. [^S002] [^S030]
- **API-12 · 확인함**: 2026-06-22 변경 이력과 현재 게시 가이드는 is_ai_generated=true로 게시 시 AI 자기공개를 지원한다고 설명한다. 캐러셀은 부모 컨테이너에만 설정하며 양쪽 로그인에서 제공된다. [^S032] [^S001]
- **API-13 · 확인함**: 현재 게시 가이드는 is_paid_partnership·branded_content_sponsor_ids를 이용한 파트너십 라벨을 Facebook Login에 제공한다고 적고 있다. Instagram Login에 같은 지원을 가정하면 안 된다. [^S001] [^S032]
- **API-14 · 확인함**: 2026-09-28 갱신 Overview는 Unified Login·Instagram Login·Facebook Login 세 구성을 비교하며 새 통합에는 Unified Login을 권장한다. Unified는 Facebook 페이지 없이 연결할 수 있으나 비즈니스 포트폴리오 등 별도 요건이 있다. 도입 시행일과 한국 실사용은 미확인이다. [^S033]

## 수치 표

| 항목 | 값·적용 범위 | 판정·출처 |
| --- | --- | --- |
| 발행 한도 | 100건/이동 24시간과 50건/24시간 혼재 | 불일치; 실효값 미확인 [^S001] [^S003] |
| 캐러셀 | 직접 읽은 게시 가이드 최대 20개 | 초기 Hermes 10개 검색 발췌와 불일치 [^S001] |
| 이미지 | JPEG·최대 8MB·4:5~1.91:1·320~1440px 너비 | Codex 본문 확인 [^S004] |
| 릴스 | 3초~15분·23~60fps·최대 300MB·9:16 권장 | API 규격이며 앱 추천 상한과 별개 [^S004] |
| 컨테이너 | 미발행 24시간 만료·24시간 400개 생성 | 게시물 50/100건과 다른 제한 [^S004] |
| IG 장기 토큰 | 60일, 발급 24시간 이후·만료 전 갱신 | Instagram Login에 한정 [^S030] |

## 한국 가용성

- 공식 글로벌 문서의 프로페셔널 계정 요건을 조사했다. 한국 실제 계정의 로그인·권한·검수·게시 성공은 수행하지 않아 미확인이다.
- 한국 지원/비지원 전용 국가 목록은 확보하지 못했으며, 공개 API 문서만으로 모든 한국 계정의 즉시 사용을 보장하지 않는다.

## 불확실·상충

- 100/50, config와 예제 rate_limit_settings 필드명, 조건부 ads_management/ads_read 표현이 공식 자료에서 혼재한다. 실호출로 검증하지 않았다. [^S003] [^S001]
- 스토리는 Facebook Login 소개에서 Business 한정이다. Instagram Login Creator 스토리 허용 범위는 미확인이다. [^S029]
- API 자체 미래 예약 매개변수와 범용 idempotency key는 확인하지 못했다. 예약 큐·상태표·중복 방지는 교과서 운영 설계 제안으로 설명한다.
- 현재 Overview는 새 통합에 Unified Login을 권장하지만 초기 Hermes 응답은 주로 두 기존 경로를 다뤘다. 세부 온보딩·사업체 요건·한국 실사용은 보충 검증 대상으로 두며 구현 경로를 이 단계에서 확정하지 않는다. [^S033]

## 교과서 반영 포인트(장 번호)

- 7·10장: 학습용 PNG와 게시용 JPEG 변환을 구분하는 설계 보완이 필요하다.
- 9~10장: 컨테이너·발행·일반 호출 한도를 분리하고 한도 숫자는 고정 정답으로 가르치지 않는다.
- 10장: Instagram Login과 Facebook Login 비교표에 페이지 연결·권한·파트너십 라벨 차이를 둔다.
- 10·12장: AI 자기공개 파라미터를 게시 전 검수 항목과 연결하고 실제 로그인 없는 드라이런을 유지한다.

[^S002]: [Instagram API with Instagram Login](https://developers.facebook.com/documentation/instagram-platform/instagram-api-with-instagram-login) · Meta for Developers · 게시·갱신: 2025-01-21 갱신 · 접근: 2026-10-26 · A · Codex curl 본문 확인; 프로페셔널 계정·페이지 불필요·scope 변경일 확인. 전체 메타데이터: [SOURCES.md](SOURCES.md#s002).

[^S001]: [Content Publishing](https://developers.facebook.com/documentation/instagram-platform/content-publishing) · Meta for Developers · 게시·갱신: 2026-10-20 갱신 · 접근: 2026-10-26 · A · Codex curl 본문 확인; 한도 설명 100/50 내부 충돌, 캐러셀 20개·JPEG·게시 절차 확인. 전체 메타데이터: [SOURCES.md](SOURCES.md#s001).

[^S033]: [Instagram Platform Overview](https://developers.facebook.com/docs/instagram-platform/overview) · Meta for Developers · 게시·갱신: 2026-09-28 갱신 · 접근: 2026-10-26 · A · Codex curl 본문 확인; 세 로그인 구성·페이지 연결·Advanced Access와 Business Verification 확인. 전체 메타데이터: [SOURCES.md](SOURCES.md#s033).

[^S029]: [Instagram API with Facebook Login](https://developers.facebook.com/documentation/instagram-platform/instagram-api-with-facebook-login) · Meta for Developers · 게시·갱신: 2025-03-03 갱신 · 접근: 2026-10-26 · A · Codex curl 본문 확인; Business/Creator·개인 계정 미지원·스토리 Business 한정 확인. 전체 메타데이터: [SOURCES.md](SOURCES.md#s029).

[^S031]: [App Review for Instagram API](https://developers.facebook.com/documentation/instagram-platform/app-review) · Meta for Developers · 게시·갱신: 2026-06-30 갱신 · 접근: 2026-10-26 · A · Codex curl 본문 확인; 소유/관리 계정 Standard와 타 비즈니스 Advanced·검수 구분 확인. 전체 메타데이터: [SOURCES.md](SOURCES.md#s031).

[^S030]: [Business Login for Instagram](https://developers.facebook.com/documentation/instagram-platform/instagram-api-with-instagram-login/business-login) · Meta for Developers · 게시·갱신: 2026-03-13 갱신 · 접근: 2026-10-26 · A · Codex curl 본문 확인; 장기 60일·24시간 지난 유효 토큰 갱신·앱 시크릿 서버 보관 확인. 전체 메타데이터: [SOURCES.md](SOURCES.md#s030).

[^S003]: [IG User content_publishing_limit](https://developers.facebook.com/documentation/instagram-platform/instagram-graph-api/reference/ig-user/content_publishing_limit) · Meta for Developers · 게시·갱신: 2024-07-23 갱신 · 접근: 2026-10-26 · A · Codex curl 본문 확인; quota_total=50·86400초 예시가 게시 가이드 100과 충돌. 전체 메타데이터: [SOURCES.md](SOURCES.md#s003).

[^S036]: [Instagram Platform Error Codes](https://developers.facebook.com/documentation/instagram-platform/instagram-graph-api/reference/error-codes) · Meta for Developers · 게시·갱신: 날짜 미상 · 접근: 2026-10-26 · A · Hermes 검색 요약만; 캐러셀 10개 발췌는 Codex가 읽은 게시 가이드 20개와 충돌. 전체 메타데이터: [SOURCES.md](SOURCES.md#s036).

[^S004]: [IG User Media](https://developers.facebook.com/documentation/instagram-platform/instagram-graph-api/reference/ig-user/media) · Meta for Developers · 게시·갱신: 2026-09-28 갱신 · 접근: 2026-10-26 · A · Codex curl 본문 확인; JPEG 8MB·이미지 비율·릴스 3초~15분·23~60fps·300MB 확인. 전체 메타데이터: [SOURCES.md](SOURCES.md#s004).

[^S035]: [Graph API Rate Limits](https://developers.facebook.com/docs/graph-api/overview/rate-limiting/) · Meta for Developers · 게시·갱신: 날짜 미상 · 접근: 2026-10-26 · A · Hermes 검색 요약만; 산식 구성별 현행 적용 미확인. 전체 메타데이터: [SOURCES.md](SOURCES.md#s035).

[^S034]: [Long-Lived Access Tokens](https://developers.facebook.com/docs/facebook-login/guides/access-tokens/get-long-lived/) · Meta for Developers · 게시·갱신: 날짜 미상 · 접근: 2026-10-26 · A · Hermes 검색 요약만; Page 토큰 발급 경로별 수명 미확인. 전체 메타데이터: [SOURCES.md](SOURCES.md#s034).

[^S032]: [Instagram Platform Changelog](https://developers.facebook.com/documentation/instagram-platform/changelog) · Meta for Developers · 게시·갱신: 최종 표시 2026-10-20; 항목별 날짜 별도 · 접근: 2026-10-26 · A · Codex curl 본문 확인; 2026-06-22 AI info 파라미터와 파트너십 라벨 항목 확인. 전체 메타데이터: [SOURCES.md](SOURCES.md#s032).
