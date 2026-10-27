# GA4·Search Console·광고 보고 API

2026-10-27 · 한국 · 2026년 10월 조사 기준. 신규 과금·가입·실계정 게시를 실행하지 않았다.

**주간 보고서는 지표 정의·날짜·통화·확정 여부를 함께 저장해야 비교할 수 있다.**

## 원응답과 재사용

기존 근거 재사용 범위: [00-scope-reuse.md](00-scope-reuse.md). 원응답 전문은 외부 RUN에만 보관한다.

| 원응답 경로 | SHA256 |
|---|---|
| `/home/yonghun/project/hermes-research/output/blog-advanced-research-20261027/raw/13-measurement-api.md` | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` |
| `/home/yonghun/project/hermes-research/output/blog-advanced-research-20261027/raw/13-measurement-api-retry.md` | `075536ffd85b8f4d28d2ca37268b4af08cc4279af9c25a47172c96179c70acbc` |

## 핵심 사실·수치·한국 가용성

| API | 정확한 항목 | 한도/주의 |
|---|---|---|
| GA4 Data API v1 | activeUsers, sessions, screenPageViews, engagementRate; date/pagePath | 표준 Core: 일200000/시간40000/프로젝트·속성·시간14000 토큰, 동시10; 요청수와 다름 |
| Search Console query | clicks, impressions, ctr, position; dimensions/date | rowLimit1~25000·기본1000; 상위행·일/검색유형50K; 전체검색어 보장 아님 |
| GSC 검색분석 | 사이트/사용자1200QPM, 프로젝트40000QPM/30000000QPD | 별도 load quota; URL검사 한도와 구별 |
| AdSense Management v2 | GET reports:generate, metrics/dimensions, readonly OAuth | JSON최대100000행/CSV1000000행; 추정수입·확정지급 별도 |

[BX057](SOURCES.md#bx057) [BX058](SOURCES.md#bx058) [BX059](SOURCES.md#bx059) [BX060](SOURCES.md#bx060) [BX116](SOURCES.md#bx116) [BX063](SOURCES.md#bx063)

GA4 할당량은 Standard 속성 기준이며 360과 다르다. returnPropertyQuota=true로 상태를 받고429/500/503을 분리한다. 행 수·차원·필터가 토큰 비용을 바꾼다. 무료로 시작할 수 있는 표준 속성/API 할당량을 유료360 구독 보장과 혼동하지 않는다.

GSC는 통상2~3일 후 데이터가 생기고 날짜는PT 기준이다. final/all/hourly_all과 incomplete 메타데이터를 보존한다. 최근 빈 결과는 지연과0을 구별하고, 최근일을 재조회한다. GA4 속성 시간대와 GSC PT, 광고 보고 통화를 억지로 맞춰 합산하지 않는다.

서비스 계정/사용자 OAuth 모두 인증 후 GA4 속성권한이 필요하다. GSC도 사이트 소유자/사용자권한을 부여해야 한다. 본인 AdSense에는 사용자 OAuth readonly를 안내한다. 키트 기본은 mock CSV이며 실제 서비스계정 키/토큰을 커밋하지 않는다. Google Site Kit은 WordPress에서 GA4/GSC/AdSense를 연결하는 공식 대안이다. Jetpack의 현재 가격/상업 조건을 별도 확인한다. [BX062](SOURCES.md#bx062) [BX110](SOURCES.md#bx110) [BX109](SOURCES.md#bx109)

## 불확실·상충과 권장 결론

문서상 지원·규정 확인과 특정 계정/제품/거래의 성공을 구별한다. 실제 계정 조건·제품 모델·계약이 정해지면 같은 공식 원문에서 확인일과 적용 범위를 갱신한다.

## 교과서·키트 반영

A10: 다음 글 점수는 학습용 규칙이다. 수익 예측모델로 부르지 않고 검색어의 실제 질문·갱신 필요 글을 먼저 개선한다.

## 연결 사실

[BXF-068](FACT-SHEET.md#bxf-068) · [BXF-069](FACT-SHEET.md#bxf-069) · [BXF-070](FACT-SHEET.md#bxf-070) · [BXF-071](FACT-SHEET.md#bxf-071) · [BXF-072](FACT-SHEET.md#bxf-072) · [BXF-073](FACT-SHEET.md#bxf-073) · [BXF-074](FACT-SHEET.md#bxf-074) · [BXF-075](FACT-SHEET.md#bxf-075)
