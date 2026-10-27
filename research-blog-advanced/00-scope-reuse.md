# 조사 범위와 재사용

2026-10-27 · 한국 · Phase BX2. 조사 문서이며 후속 키트/원고 구현 완료를 뜻하지 않는다.

| 먼저 읽은 기존 근거 | 이번 재사용 | 이번 공백 조사 |
|---|---|---|
| research-blog/01-platforms.md, 07-api-automation.md | 플랫폼 구분·네이버/티스토리 종료·Blogger OAuth | WordPress 7.1.3·Docker 태그·세부 REST·호스팅 제한 재확인 |
| research-blog/02-ads-revenue.md, 03-affiliate-products.md, 08-policy-copyright.md, 09-tax.md | 광고/제휴 구조·표시 원칙·계속 반복 소득·등록/신고 | 현행 AdSense/AdFit·쿠팡 API 공백·2026 공정위·현물과 부가세 |
| research-blog/05-google-seo-ai.md, 06-keywords-analytics.md | AI 자체와 스팸 구별·측정 정의 | GA4/GSC API 수치·현재 정책·네이버 원문 |
| research-advanced/costs.md, generation-apis.md, execution-hosting.md, approval-security.md | LLM 계산식·구조화 출력·cron/작업 스케줄러·알림·Actions·키/상태 보관 | 가격/종료표·현재 지출 한도 메뉴만 갱신 확인 |
| research-baby/04-sleep.md, 08-fever-emergency.md, 11-vaccines.md, 14-benefits.md, 17-home-products.md, BRIEFING.md, FACT-SHEET.md | 공식 건강/제도 근거·예방접종·안전 수면·응급 경로 | 제품 광고 규제·공공데이터 허락·아이 사생활 |

기존 숫자를 현재 숫자로 무검증 승격하지 않는다. 기존 출처만 재사용한 건은 신규 공식 원문 직접 열람 수에서 뺀다. 원응답은 RUN 외부 보관이며 저장소에는 경로와 SHA256만 남긴다.

## 설계와 법의 경계

설계 1.1·6절과 BabyBook 8절은 이 프로젝트의 보호 수준이다. 법이 모든 부모 사진 공개를 금지하거나 모든 하루 2편 발행을 금지한다는 뜻이 아니다. 관문은 위법 여부를 확정하지 않고 `block/review/pass`와 다음 행동을 반환한다. 미확인 자료는 기본 허용으로 처리하지 않는다.
