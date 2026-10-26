# 예약·자동화 도구: 무료 범위·비용·책임

작성: 2026-10-26, Codex 정리. **2026년 10월 조사 기준**(컷오프: 2026-10-26). Hermes 원응답과 별개인 편집본이다.

- 원응답: `/home/yonghun/project/hermes-research/output/ai-insta-research-20261026/raw/scheduling-automation-tools.md`
- SHA256: `13428bdee80137851efb53a58a71c960a63ce41acbf05e229fc78fc1474870e7`

## 핵심 사실(출처 각주)

- **AUTO-01 · 미확인/추가 조사 필요**: Instagram 앱 예약과 Business Suite 예약은 대상·미디어·제약을 별도 확인해야 한다. 공식 도움말 검색 요약은 앱 예약을 공개 계정·30일 전·하루 25개로 표시했지만 한국 적용과 변경 시점은 미확인이다. [^S037] [^S039]
- **AUTO-02 · 미확인/추가 조사 필요**: Business Suite 접속 조건과 Facebook Login API의 페이지 연결 조건을 동일하게 가르치면 안 된다. 도움말 검색 요약에는 페이지 미연결 Instagram 프로페셔널 계정 접근 경로도 있다. [^S038] [^S033]
- **AUTO-03 · Hermes 근거**: n8n의 self-hosted는 배포 방식이며 Community와 유료 Business 에디션을 구분해야 한다. 내부 자동화와 고객에게 유료 플랫폼 접근권을 제공하는 서비스의 라이선스 조건도 다르다. [^S041] [^S042] [^S043]
- **AUTO-04 · Hermes 근거**: Make credits, Zapier task, n8n workflow executions, Buffer 채널/대기열, Later Social Set/게시량은 다른 과금 단위다. 무료 처리량과 미디어 호스팅·운영비를 나눠 비교해야 한다. [^S044] [^S045] [^S041] [^S046] [^S048] [^S001]
- **AUTO-05 · Hermes 근거**: Buffer Free의 3채널·채널당 10개는 검색 요약상 동시 대기 예약 수이며 월 게시 수가 아니다. Later의 14일은 유료 상품 체험이며 영구 무료 플랜의 근거로 쓰지 않는다. [^S046] [^S047] [^S048]
- **AUTO-06 · 미확인/추가 조사 필요**: n8n·Make·Zapier·Buffer·Later의 현행 Instagram Login/Facebook Login별 커넥터, 미디어·음원·AI/광고 라벨별 직접/알림 게시 지원표는 초기 조사에서 충분히 확보하지 못했다. [^S041] [^S044] [^S045] [^S046] [^S048]

## 수치 표

| 항목 | 값·적용 범위 | 판정·출처 |
| --- | --- | --- |
| Meta 앱 예약 | 검색 요약: 30일 전·하루 25개 | 한국 적용/현행 전문 재확인 [^S037] |
| n8n Cloud Starter | €20/월, 연간 결제 표기 | 포함 실행량·월 결제가는 미확인 [^S041] |
| Make Free | 월 1000 credits·최소 15분 간격 | Hermes 원문 일부; 유료 시작가 미확인 [^S044] |
| Zapier Professional | 가격 $19.99/월부터라는 표기 | 통화 코드·결제 주기·무료 task 미확인 [^S045] |
| Buffer | Free 3채널·대기열 10개/채널; Essentials $5 연결제 월 환산 또는 월결제 $6/채널 | 검색 요약만·통화 코드 미확인 [^S046] |
| Later | 14일 체험; Growth USD 37.50/월 연간 결제 화면 | Starter 시작가·영구 무료 플랜 미확인 [^S048] |

## 한국 가용성

- 글로벌 가격·도움말을 조사했으며 한국 가입·결제·음원·라벨 제공을 실계정으로 검증하지 않았다. 미확인은 비지원 단정과 다르다.
- n8n 자체 호스팅도 한국 전용 제한·제공 조건을 확인하지 못했다. 서버·저장소·유지보수 비용은 별도 산정 항목이다.

## 불확실·상충

- Business Suite의 Instagram별 예약 기간·총량, 도구별 로그인 방식·AI/광고 라벨·음원 지원이 남아 있다.
- 무료/최저 유료 비교표에서 금액 미추출을 임의의 업계 가격으로 채우지 않는다. 모든 가격은 결제 주기·통화·과금 단위와 함께 재확인한다.
- API 게시 한도 100건만 인용한 초기 도구 응답은 API 노트의 100/50 공식 문서 충돌을 함께 봐야 한다. [^S001] [^S003]
- Python+cron/Windows 작업 스케줄러는 비교 설계안이다. 이번 단계에서 구현·실행 문법을 검증하지 않았다.

## 교과서 반영 포인트(장 번호)

- 9~10장: 직접 게시와 사람이 알림을 받고 마무리하는 게시를 구분한다.
- 9~10장: 콘텐츠 ID·승인 상태·예약 시각과 시간대·컨테이너/게시 ID를 남기는 최소 흐름을 제안한다.
- 10장: 호스팅/권한/라벨을 별도 점검하고 가격표를 무료 자동 게시 보장으로 표현하지 않는다.

추가 확인 자료(접근 실패·검색만 확인한 후보 포함): [^S040]

[^S037]: [How to create and manage scheduled posts and Reels on Instagram](https://help.instagram.com/439971288310029) · Instagram Help Center · 게시·갱신: 날짜 미상 · 접근: 2026-10-26 · A · Hermes 검색 요약만; 30일·공개 계정 문구, 한국 적용·변경일 미확인. 전체 메타데이터: [SOURCES.md](SOURCES.md#s037).

[^S039]: [Schedule Facebook and Instagram Content on Meta Business Suite](https://www.facebook.com/business/help/609176706604372) · Meta Business Help Center · 게시·갱신: 날짜 미상 · 접근: 2026-10-26 · A · Hermes 검색 요약만; Instagram별 예약 기간·라벨 지원 미확인. 전체 메타데이터: [SOURCES.md](SOURCES.md#s039).

[^S038]: [Connect your Instagram account to Meta Business Suite](https://www.facebook.com/business/help/428687951269163) · Meta Business Help Center · 게시·갱신: 날짜 미상 · 접근: 2026-10-26 · A · Hermes 검색 요약만; 페이지 미연결 프로페셔널 계정 접근 경로 보고. 전체 메타데이터: [SOURCES.md](SOURCES.md#s038).

[^S033]: [Instagram Platform Overview](https://developers.facebook.com/docs/instagram-platform/overview) · Meta for Developers · 게시·갱신: 2026-09-28 갱신 · 접근: 2026-10-26 · A · Codex curl 본문 확인; 세 로그인 구성·페이지 연결·Advanced Access와 Business Verification 확인. 전체 메타데이터: [SOURCES.md](SOURCES.md#s033).

[^S041]: [n8n Plans and Pricing](https://n8n.io/pricing/) · n8n · 게시·갱신: 날짜 미상 · 접근: 2026-10-26 · A · Hermes 가격 원문 일부; 포함 실행량·월 결제가 미확인. 전체 메타데이터: [SOURCES.md](SOURCES.md#s041).

[^S042]: [n8n Community License](https://docs.n8n.io/n8n-community-license) · n8n · 게시·갱신: 날짜 미상 · 접근: 2026-10-26 · A · Hermes 검색 요약만; 상업 서비스 최종 허용 범위는 전문 재확인 필요. 전체 메타데이터: [SOURCES.md](SOURCES.md#s042).

[^S043]: [n8n Community License FAQ](https://docs.n8n.io/n8n-community-license/community-license/license-faq) · n8n · 게시·갱신: 날짜 미상 · 접근: 2026-10-26 · A · Hermes 검색 요약만; 내부 자동화와 고객 플랫폼 접근 판매 구분. 전체 메타데이터: [SOURCES.md](SOURCES.md#s043).

[^S044]: [Make Pricing](https://www.make.com/en/pricing) · Make · 게시·갱신: 날짜 미상 · 접근: 2026-10-26 · A · Hermes 원문 일부; Free 1000 credits·15분 확인 보고, 유료 가격 추출 실패. 전체 메타데이터: [SOURCES.md](SOURCES.md#s044).

[^S045]: [Zapier Plans and Pricing](https://zapier.com/pricing) · Zapier · 게시·갱신: 날짜 미상 · 접근: 2026-10-26 · A · Hermes 원문 일부; USD 여부·결제 주기·무료 task 한도 미확인. 전체 메타데이터: [SOURCES.md](SOURCES.md#s045).

[^S046]: [Buffer Pricing](https://buffer.com/pricing) · Buffer · 게시·갱신: 날짜 미상; 검색 문구상 마지막 가격 변경 2025-11 · 접근: 2026-10-26 · A · Hermes 검색 요약만; 무료 대기열과 월 처리량을 구분해야 함. 전체 메타데이터: [SOURCES.md](SOURCES.md#s046).

[^S048]: [Later Pricing Plans](https://later.com/pricing/) · Later · 게시·갱신: 날짜 미상 · 접근: 2026-10-26 · A · Hermes 원문 일부; 무료 체험·Auto Publish 설명, Starter 시작가 미확인. 전체 메타데이터: [SOURCES.md](SOURCES.md#s048).

[^S001]: [Content Publishing](https://developers.facebook.com/documentation/instagram-platform/content-publishing) · Meta for Developers · 게시·갱신: 2026-10-20 갱신 · 접근: 2026-10-26 · A · Codex curl 본문 확인; 한도 설명 100/50 내부 충돌, 캐러셀 20개·JPEG·게시 절차 확인. 전체 메타데이터: [SOURCES.md](SOURCES.md#s001).

[^S047]: [How many posts can I schedule in advance?](https://support.buffer.com/articles/how-many-posts-can-i-schedule-in-advance-Kmy2IEecqm) · Buffer · 게시·갱신: 날짜 미상 · 접근: 2026-10-26 · A · Hermes 검색 요약만. 전체 메타데이터: [SOURCES.md](SOURCES.md#s047).

[^S003]: [IG User content_publishing_limit](https://developers.facebook.com/documentation/instagram-platform/instagram-graph-api/reference/ig-user/content_publishing_limit) · Meta for Developers · 게시·갱신: 2024-07-23 갱신 · 접근: 2026-10-26 · A · Codex curl 본문 확인; quota_total=50·86400초 예시가 게시 가이드 100과 충돌. 전체 메타데이터: [SOURCES.md](SOURCES.md#s003).

[^S040]: [Create a post in Meta Business Suite on desktop](https://www.facebook.com/business/help/942827662903020) · Meta Business Help Center · 게시·갱신: 날짜 미상 · 접근: 2026-10-26 · A · Hermes 검색 요약만; 10장 문구는 도구 기능이며 API 전체 한도로 사용 금지. 전체 메타데이터: [SOURCES.md](SOURCES.md#s040).
