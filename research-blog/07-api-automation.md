# 공식 API·예약·자동화의 실제 경계

2026-10-26 · **2026년 10월 조사 기준**. 공개 문서 조사이며 실계정 실행 결과는 아니다.

| Hermes 원응답(저장소 밖) | SHA256 |
|---|---|
| `/home/yonghun/project/hermes-research/output/blog-research-20261026/raw/16-api-automation.md` | `f90d71323aecce6612357c3a8064bd7a827c9cdd33da7d0124776dc37fa1fa98` |

확인 수준·게시일은 [출처표](SOURCES.md), 질문별 채택 상태는 [질문 연결표](QUESTION-MAP.md)를 따른다. 원응답은 근거 후보이며 직접 확인으로 보완했다.

## 핵심 사실

**공식 API 자동 발행 대상은 Blogger API v3와 WordPress REST API다.** 네이버 글쓰기 API는2020-05-06 종료 적용, 티스토리는2023-12-22 공지에2023년12월말~2024년2월말 순차 종료를 명시했다. 글쓰기 문서가 검색에 남아 있거나 검색 API가 살아 있다는 사실은 발행 가능 근거가 아니다. [B006](SOURCES.md#b006) [B007](SOURCES.md#b007) [B012](SOURCES.md#b012) [B010](SOURCES.md#b010)

| 플랫폼 | 공식 프로그램 발행 | 인증·권한 | 예약/검수 |
|---|---|---|---|
| 네이버 | 종료된 글쓰기 API로 신규 구현 불가 | 검색 API의 Client ID와 글쓰기 권한은 다름 | 공식 에디터 예약 가능 |
| 티스토리 | Open API 종료; 키트는 원고/HTML 내보내기까지만 | 종료 전 access_token 예제 재사용 금지 | 공식 에디터 예약 |
| Blogger | `POST /blogger/v3/blogs/{blogId}/posts` | OAuth2와 `https://www.googleapis.com/auth/blogger`; 소유 블로그 쓰기 권한. API key만으로 쓰기 불가 | `isDraft=true`로 초안, `posts.publish`의 `publishDate`로 예약 |
| 설치형 WordPress | `POST /wp-json/wp/v2/posts` | HTTPS+로그인명/애플리케이션 비밀번호, 해당 사용자 작성/발행 권한 | `status=draft` 기본; `future`와 미래 `date` 예약, 사이트 시간대 확인 |
| WordPress.com | `POST https://public-api.wordpress.com/wp/v2/sites/{site_id}/posts` | WordPress.com OAuth2 Bearer 토큰; 설치형 Basic 인증과 구별 | blog-kit 기본 지원 범위는 설치형으로 한정 제안 |
| 브런치 | 일반 이용자용 공개 글쓰기 API 근거 미확보 | 미확인 | 공식 예약은 지원 |

[B002](SOURCES.md#b002) [B012](SOURCES.md#b012) [B013](SOURCES.md#b013) [B010](SOURCES.md#b010) [B011](SOURCES.md#b011) [B144](SOURCES.md#b144) [B080](SOURCES.md#b080)

### Blogger의 최소 흐름

1. 학습자가 Google Cloud 프로젝트에 Blogger API를 켠다.
2. OAuth 동의화면·본인 테스트 사용자·데스크톱 클라이언트를 설정한다.
3. 사용자 브라우저 동의로 얻은 토큰을 로컬에 보관한다. API키만 넣는 방식으로 안내하지 않는다.
4. 미리보기·중복 확인 후 `isDraft=true`로 생성하고 반환된 `id/url`을 기록한다.
5. 사용자가 원하면 공식 UI 또는 publish 호출로 공개한다. 예약은 publishDate를 쓴다.

[B014](SOURCES.md#b014) [B012](SOURCES.md#b012) [B013](SOURCES.md#b013) OAuth 외부 테스트 상태·토큰 만료·검증 요구는 실제 프로젝트 화면에서 확인한다. 상용 공개 앱 검증과 개인 테스트 앱 실행을 같은 절차로 설명하지 않는다.

### WordPress의 최소 흐름

WordPress5.6(2020-12)부터 애플리케이션 비밀번호를 제공한다. 관리자에서 사용자→프로필→애플리케이션 비밀번호로 도구 전용 자격을 만든다. 주 비밀번호와 다르고 개별 폐기할 수 있으며 최초에만 보인다. HTTPS에서 Basic 인증으로 REST에 사용한다. 플러그인/WAF/호스팅이 기능을 막으면401/403 원인을 공식 가이드로 확인하고 우회 인증을 만들지 않는다. [B011](SOURCES.md#b011)

## 수치 표·할당량

| 항목 | 판정 |
|---|---|
| Blogger 프로젝트 요청 할당량 | 공식 콘솔의 해당 프로젝트 Quotas에서 확인; 검색되는1일1만 회를 무조건 고정 기본값으로 채택하지 않음 |
| Blogger 글 생성 제한 | API 요청 한도와 블로그 스팸/일 발행 제한은 별도. 무제한 자동발행 보장 없음 |
| WordPress | 보편 공통 ‘일 N개’ REST 한도 미확인. 서버/WAF/권한 제한에 따름 |
| 실제 호출 검증 | 이번 단계0회. 공개 글·인증 토큰 생성 안 함 |

[B146](SOURCES.md#b146) WordPress 예약은기본WP-Cron이 방문 요청에 의존해 늦어질 수 있으므로, 예약 등록과 정각공개 보장을 구분한다. [B145](SOURCES.md#b145)

위 첫 두 항목의 구체 프로젝트 숫자는 [미확인 목록](BRIEFING.md)에 남기며 키트 검증에서 콘솔 표시를 기록하게 한다.

## 한국 가용성

Blogger는 Google 사용자 동의, WordPress는 본인 관리 사이트가 전제다. 실제 한국 계정·호스팅에서 API 호출은 하지 않았다. ‘문서상 가능’과 ‘실게시 성공’을 구별한다.

## 불확실·상충과 권장 결론

기본 드라이런은 **네트워크 쓰기0회**로 요청 본문·대상·상태만 보여 준다. 별도 명시적 live 옵션에서도 우선 초안 저장을 권한다. 타임아웃 후 POST를 맹목 반복하면 중복 글이 생길 수 있으므로 저장된 post ID·서버 목록을 확인한다. 이는 정책 요구가 아닌 키트 구현 제안이다. API를 쓴다는 이유로 검색 스팸 정책이 면제되지 않는다. [B046](SOURCES.md#b046) [B032](SOURCES.md#b032)

## 교과서 반영 포인트

이론10·실습10 선택: 기본 커넥터 Blogger1개, 심화 설치형 WordPress. 첫 발행(실습7)은 공식 UI. 네이버/티스토리 버튼 자동조작·비공개 엔드포인트·로그인 우회는 대안으로 넣지 않는다. B3k 구현 시 할당량·토큰 저장·초안/공개 상태·중복 오류를 분리 검증한다.
