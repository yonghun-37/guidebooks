# 발행 경로와 WordPress REST

2026-10-27 · 한국 · 2026년 10월 조사 기준. 신규 과금·가입·실계정 게시를 실행하지 않았다.

**같은 실습은 mock에서 끝내고, 선택적으로 Docker WordPress와 실제 HTTPS 호스팅으로 옮긴다.**

## 원응답과 재사용

기존 근거 재사용 범위: [00-scope-reuse.md](00-scope-reuse.md). 원응답 전문은 외부 RUN에만 보관한다.

| 원응답 경로 | SHA256 |
|---|---|
| `/home/yonghun/project/hermes-research/output/blog-advanced-research-20261027/raw/01-wordpress-api.md` | `6e02472bd267e738a9895e3fd37a38c07c43b9a37c371cc2c1973f8f88a5ac54` |

## 핵심 사실·수치·한국 가용성

| 동작 | 공식 경로·필드 | 사람/오류 처리 |
|---|---|---|
| 초안 생성 | POST /wp-json/wp/v2/posts, status=draft | 응답 id 저장; POST 타임아웃은 서버 조회 후 재개 |
| 이미지 | POST /wp-json/wp/v2/media → id → featured_media | 원본/변환본 EXIF 확인; 실패 시 이미 성공한 글 재생성 금지 |
| 카테고리·태그 | /categories, /tags 생성/조회 → ID 배열 | 이름이 아닌 ID 연결; 같은 항목 재사용 |
| 예약 | future + 미래 date 또는 date_gmt | Asia/Seoul과 UTC를 혼합하지 않음; WP-Cron 지연 확인 |
| 승인 뒤 수정 | 최종 HTML·미디어·관계표시·설정의 해시 | 해시가 바뀌면 승인 무효·다시 검수 |

REST 스키마는 중복 방지 키를 자동 제공하지 않는다. SQLite의 로컬 content_id/서버 post_id와 상태를 먼저 보존하는 것은 키트 제안이다. 예약 API 성공과 공개 완료를 따로 출력한다. [BX004](SOURCES.md#bx004) [BX005](SOURCES.md#bx005) [BX127](SOURCES.md#bx127)

애플리케이션 비밀번호는 WordPress 5.6부터다. 실제 운영은 HTTPS·작성 권한·Authorization 전달이 전제다. 메뉴가 없으면 사이트 HTTPS 인식/보안 플러그인/WAF/호스팅 지원을 차례로 확인한다. 비밀번호 값을 로그나 문의글에 붙이지 않는다. localhost 예외는 로컬 실습에서만 다루고 공인 HTTP 서버에 확대하지 않는다. [BX003](SOURCES.md#bx003)

WordPress.com은 OAuth와 public-api.wordpress.com 경로를 구별한다. 10-28 현행 플러그인 도움말과 가격 페이지는 유료 Personal의 설치를 안내하며 과거 상충을 재현하지 못했다. 선택한 플랜의 플러그인·외부 광고 코드·WordAds 조건을 각각 확인한다. Free의 플랫폼 광고를 내 수입으로 계산하지 않는다.

Blogger는 API key의 공개 읽기와 OAuth 쓰기를 구별한다. OAuth scope는 https://www.googleapis.com/auth/blogger, posts.insert의 isDraft=true와 posts.publish의 publishDate를 쓴다. 현재 요청 쿼터는 본인 프로젝트 콘솔에서 확인한다. Blogger 관리의 수익 메뉴에서 AdSense를 연결하며 글쓰기 권한이 광고 승인까지 주지는 않는다. [BX011](SOURCES.md#bx011) [BX012](SOURCES.md#bx012) [BX095](SOURCES.md#bx095)

## 불확실·상충과 권장 결론

- [BXF-006](FACT-SHEET.md#bxf-006) · **확인**: 현재 유료 플랜의 플러그인 안내를 확인했다. 과거 가격 FAQ 상충은 현재 결론에서 철회하고 선택 플랜의 코드 삽입·광고·REST·복구를 구매 전에 확인한다.
- [BXF-008](FACT-SHEET.md#bxf-008) · **미확인**: Blogger 현행 프로젝트 요청 할당량은 인증된 콘솔 확인 대상이다. 검색에 남은 하루 10000회를 보편적 현재값으로 채택하지 않는다. 글 생성/스팸 제한과 요청 쿼터도 다르다.

## 교과서·키트 반영

A1·A2·A6: doctor에 Python/실행 폴더/포트/모드/서버 버전/시간대만 출력하고 비밀을 숨긴다. 책과 결과가 다르면 이 순서로 비교한다.

## 연결 사실

[BXF-001](FACT-SHEET.md#bxf-001) · [BXF-002](FACT-SHEET.md#bxf-002) · [BXF-003](FACT-SHEET.md#bxf-003) · [BXF-004](FACT-SHEET.md#bxf-004) · [BXF-005](FACT-SHEET.md#bxf-005) · [BXF-006](FACT-SHEET.md#bxf-006) · [BXF-007](FACT-SHEET.md#bxf-007) · [BXF-008](FACT-SHEET.md#bxf-008) · [BXF-009](FACT-SHEET.md#bxf-009) · [BXF-010](FACT-SHEET.md#bxf-010) · [BXF-098](FACT-SHEET.md#bxf-098)
