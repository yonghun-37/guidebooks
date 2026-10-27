# 한국 사용자의 호스팅·도메인 비용

2026-10-27 · 한국 · 2026년 10월 조사 기준. 신규 과금·가입·실계정 게시를 실행하지 않았다.

**월 광고가보다 REST 지원·HTTPS·백업 복구·정상 갱신 총액을 먼저 비교한다.**

## 원응답과 재사용

기존 근거 재사용 범위: [00-scope-reuse.md](00-scope-reuse.md). 원응답 전문은 외부 RUN에만 보관한다.

| 원응답 경로 | SHA256 |
|---|---|
| `/home/yonghun/project/hermes-research/output/blog-advanced-research-20261027/raw/02-hosting-domains.md` | `7323abe67d4d8ce3a4d90f39bccff6da7d537c10fd9c1b027851422b9d7eacf8` |

## 핵심 사실·수치·한국 가용성

| 예시 | 확인한 가격 | HTTPS·백업·제약 |
|---|---|---|
| 카페24 워드프레스 블로그 스타트업 | 월500원+설치5000원, VAT포함 | SSL; 800MB/일1GB; 플러그인·SSH·FTP 제한은 현재 재확인 보류; 코드 삽입·REST/Application Passwords·백업/복원은 구매 전 서면 확인 |
| Hostinger Premium 공개 USD 상품 | 48개월 $119.52 선납=$2.49/월; 같은 기간 갱신 표시 $10.99/월 | 관리형 WordPress·SSL·주간백업; 한국 결제통화·세금·갱신총액 확인 |
| Google Cloud e2-micro Free Tier | 해당 미국 리전 월1대 상당; standard PD30GB-month·북미발 전송1GB | 설치/HTTPS/보안/백업을 직접 관리; 일반VM 외부IPv4 시간$0.005 별도 |
| Oracle Always Free | 상세 문서 A1 총2OCPU/12GB 예시; 별도 30일 trial과 구별 | 홈리전·가용성·유휴회수; 보안/HTTPS/복구 직접; 결제계정 현재 entitlement 확인 |

각 행은 별도 상품이다. 카페24의 managed_wordpress/wordpress-blog 가격과 설치비를 섞지 않는다. 카페24 페이지는 장기 선납 할인도 안내하므로 월500×12는 월납 단순 비교식이며 실제 연납 견적이 아니다. [BX015](SOURCES.md#bx015) [BX016](SOURCES.md#bx016) [BX017](SOURCES.md#bx017) [BX121](SOURCES.md#bx121) [BX130](SOURCES.md#bx130)

가비아 .com/.kr 첫해 이벤트는 각각19,800/16,500원(VAT포함). 10월 정가는24,000/21,000원(VAT별도), 11월1일부터25,000/22,000원(VAT별도)으로 신규·연장·이전 인상 예정이다. 할인 첫해와 2년차 갱신을 비용표에 별도 칸으로 둔다. [BX019](SOURCES.md#bx019) [BX120](SOURCES.md#bx120)

백업 구매 전 질문: DB와 wp-content/uploads를 함께 내려받는가, 보관 주기는 무엇인가, 내보내기/복구비가 있는가, 다른 서버에 복구 가능한가, 관리자가 잘못 지운 경우도 복구하는가. 무료 SSL이 백업을 의미하지 않는다. 키트는 별도 빈 WordPress에 DB/파일 복구 후 이미지와 글 ID를 대조하는 과제를 제공하도록 제안한다.

## 불확실·상충과 권장 결론

- [BXF-012](FACT-SHEET.md#bxf-012) · **일부 미확인**: 과거 미지원 문구를 이번에 재확인하지 못했다. 현재 제한/지원을 단정하지 않고 코드 삽입·플러그인·REST·복구를 구매 전에 문의한다.

## 교과서·키트 반영

A0·A2: 업체 추천 순위 대신 1년/갱신 총액과 구현 가능성 표를 쓴다. 실제 구매 전 auth·플러그인·백업 확인을 완료 기준에 넣는다.

## 연결 사실

[BXF-011](FACT-SHEET.md#bxf-011) · [BXF-012](FACT-SHEET.md#bxf-012) · [BXF-013](FACT-SHEET.md#bxf-013) · [BXF-014](FACT-SHEET.md#bxf-014) · [BXF-015](FACT-SHEET.md#bxf-015) · [BXF-016](FACT-SHEET.md#bxf-016) · [BXF-094](FACT-SHEET.md#bxf-094) · [BXF-095](FACT-SHEET.md#bxf-095) · [BXF-096](FACT-SHEET.md#bxf-096)

## 2026-10-28 재대조 반영

현재 플러그인 문서는 모든 WordPress.com 유료 플랜 설치를 안내한다. 과거 가격 FAQ 상충과 카페24 플러그인·SSH·FTP 미지원은 이번 재대조에서 확인되지 않아 현행 사실로 쓰지 않는다. 선택 플랜의 코드 삽입·광고·플러그인·REST·복구 지원을 구매 전에 확인한다. BXF-006·012의 최신 판정을 따른다.
