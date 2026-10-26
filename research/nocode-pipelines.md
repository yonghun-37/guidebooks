# 노코드 파이프라인: 템플릿·승인·비용·실패 지점

작성: 2026-10-26, Codex 정리. **2026년 10월 조사 기준**(컷오프2026-10-26). Hermes 원응답과 별개인 편집본이며, 아래 사실의 확인 수준은 독립적으로 표시했다.

## 질의·원응답과 확인 범위

- 원응답: `/home/yonghun/project/hermes-research/output/ai-insta-research-20261026/raw/nocode-pipelines.md`
- SHA256: `7c83de4a5e71f16aa5a7167a55b1abe14ab1946888a9d8d1fbaab20fd17f1caa`
- 원응답: `/home/yonghun/project/hermes-research/output/ai-insta-research-20261026/raw/nocode-pipelines-supplement.md`
- SHA256: `d66a9c18fdb2c0447258ff55af44ce7859fcd0efeefa107d55218c65e97570b4`

초기 응답의 가격 주제는 일부 공식 본문을 얻었고, 다수 주제는 웹 중계 프록시403으로 근거를 얻지 못했다. 보충 질의도 실행별로 평가했다. exit0·URL 존재를 본문 확인으로 세지 않았다. Codex가 별도 경로로 읽은 근거는 SOURCES의 확인 범위와 [직접 확인 기록](verification-phase-1b.json)을 따른다.

## 핵심 사실(출처 각주)

- **NOCODE-01 · 확인함; 템플릿 설명만**: n8n 카탈로그의20222 템플릿은 인증폼→Gemini 초안→규칙 검사→Telegram 사람 승인→컨테이너 생성·상태 조회→Instagram 게시를 설명한다. 제작자 설명과 카탈로그 등록을 Codex의 실행 검증으로 읽으면 안 된다. [^S152]
- **NOCODE-02 · 확인함; 실행 미검증**: Make는 Google Sheets 새 행→Google Drive 파일→Instagram 사진 게시 템플릿을 공개한다. Zapier도 새 Sheets 행→Instagram 사진 게시 조합을 제공한다. 설명에 없는 RSS 수집·카드 렌더링·승인은 추가 설계가 필요하다. [^S153] [^S154]
- **NOCODE-03 · 확인함**: Zapier 공식 안내는 Business/Creator 계정과 연결된 Facebook 페이지·콘텐츠 권한·OAuth를 요구한다. Make의 Facebook Login 커넥터 안내는 Instagram Business와 연결 페이지의 관리 권한을 요구한다. API 자체 조건과 개별 커넥터 조건을 구분한다. [^S155] [^S156] [^S002]
- **NOCODE-04 · 확인함**: Make Free는 월1000credits이며 액션별 소모량과 일부 AI 기능의 가변 과금을 설명한다. n8n SUL은 자기 내부 사업·개인·비상업 사용 등의 제한을 두므로 소스 공개를 무제한 상용 재판매 허용으로 읽으면 안 된다. [^S044] [^S157]
- **NOCODE-05 · 기술조건 확인; 운영 절차는 제안**: 공개 미디어 URL·JPEG 입력·컨테이너 상태와 만료·권한·토큰은 게시 실패의 점검 항목이다. 중복 재시도 방지·승인 기록·시간대 기록은 운영 설계 제안이며 이번에 실행한 워크플로가 아니다. [^S001] [^S004] [^S030] [^S152]

## 수치 표

| 항목 | 값/산식 | 판정 |
| --- | --- | --- |
| Make Free | 월1000credits | 전체게시횟수아님 [^S044] |
| 교육용 월30개·6액션/개 | 180credits | 단순가정·정기조회/재시도/렌더링/LLM비용제외 [^S044] |
| 교육용 월60개·6액션/개 | 360credits | 실제비용/무료충족보장아님 [^S044] |
| n8n | 실행/서버·라이선스별도 | 외부API/호스팅별도 [^S157] [^S041] |

## 한국 가용성

한국 계정 연결·결제·AI/광고 라벨·음원·알림 게시의 실제 동작은 시험하지 않았다. 글로벌 커넥터 문서의 요건만 확인했다. [^S156] [^S155]

## 불확실·상충

템플릿의 무료 사용은 외부 LLM·렌더링·호스팅까지 무료라는 뜻이 아니다. 같은 도구의 다른 로그인 커넥터에까지 요건을 확대하지 않는다. API100/50 한도 충돌은 미해결이다. [^S152] [^S001] [^S003]

## 교과서 반영 포인트(장 번호)

편집 제안: 입력→초안→승인→렌더링→호스팅→예약→게시 상태 확인→결과 기록을 분리한다. 지원하지 않는 표시·음원은 사람이 최종 확인하는 경로를 검토한다. 이번에는 구현하지 않았다. [^S152] [^S001]

## 실제 템플릿 세 개의 범위

| 제공처 | 출발→도착 | 사람 승인 | 채택 전 확인 |
| --- | --- | --- | --- |
| n8n20222 | 폼·Gemini→Telegram→Graph API | 명시 | 제작자기여템플릿·외부비용·권한 [^S152] |
| Make Sheets/Drive | 새행·이미지→사진게시 | 설명상없음 | 승인·렌더링추가필요 [^S153] |
| Zapier Sheets | 새행→사진게시 | 설명상없음 | OAuth·페이지·게시권한 [^S154] [^S155] |

[^S152]: [Create human-approved Instagram posts with Gemini, Telegram, and Instagram](https://n8n.io/workflows/20222-create-human-approved-instagram-posts-with-gemini-telegram-and-instagram/) · n8n 카탈로그 / Buğra Şıkel 작성 · 게시·갱신: 절대날짜미상;표시20일전 · 접근: 2026-10-26 · A · 확인함. 전체 확인 범위: [SOURCES.md](SOURCES.md#s152).

[^S153]: [Instagram for Business(Facebook Login)·Google Sheets templates](https://www.make.com/integrations/instagram-business/google-sheets) · Make · 게시·갱신: 게시·갱신일 미상 · 접근: 2026-10-26 · A · 확인함. 전체 확인 범위: [SOURCES.md](SOURCES.md#s153).

[^S154]: [Google Sheets·Instagram for Business Integration](https://zapier.com/apps/google-sheets/integrations/instagram-for-business) · Zapier · 게시·갱신: 게시·갱신일 미상 · 접근: 2026-10-26 · A · 확인함. 전체 확인 범위: [SOURCES.md](SOURCES.md#s154).

[^S155]: [How to get started with Instagram for Business on Zapier](https://help.zapier.com/hc/en-us/articles/8496101110541-How-to-get-started-with-Instagram-for-Business-on-Zapier) · Zapier · 게시·갱신: 갱신2026-01-21 · 접근: 2026-10-26 · A · 확인함. 전체 확인 범위: [SOURCES.md](SOURCES.md#s155).

[^S156]: [Instagram for Business(Facebook login)](https://apps.make.com/instagram-business) · Make Apps Documentation · 게시·갱신: 게시·갱신일 미상 · 접근: 2026-10-26 · A · 확인함. 전체 확인 범위: [SOURCES.md](SOURCES.md#s156).

[^S002]: [Instagram API with Instagram Login](https://developers.facebook.com/documentation/instagram-platform/instagram-api-with-instagram-login) · Meta for Developers · 게시·갱신: 2025-01-21 갱신 · 접근: 2026-10-26 · A · Phase1 기록 참조. 전체 확인 범위: [SOURCES.md](SOURCES.md#s002).

[^S044]: [Make Pricing](https://www.make.com/en/pricing) · Make · 게시·갱신: 게시·갱신일미상 · 접근: 2026-10-26 · A · 확인함. 전체 확인 범위: [SOURCES.md](SOURCES.md#s044).

[^S157]: [n8n LICENSE / Sustainable Use License](https://raw.githubusercontent.com/n8n-io/n8n/master/LICENSE.md) · n8n 공식 저장소 · 게시·갱신: 파일갱신일미상;SUL1.0 · 접근: 2026-10-26 · A · 확인함. 전체 확인 범위: [SOURCES.md](SOURCES.md#s157).

[^S001]: [Content Publishing](https://developers.facebook.com/documentation/instagram-platform/content-publishing) · Meta for Developers · 게시·갱신: 2026-10-20 갱신 · 접근: 2026-10-26 · A · Phase1 기록 참조. 전체 확인 범위: [SOURCES.md](SOURCES.md#s001).

[^S004]: [IG User Media](https://developers.facebook.com/documentation/instagram-platform/instagram-graph-api/reference/ig-user/media) · Meta for Developers · 게시·갱신: 2026-09-28 갱신 · 접근: 2026-10-26 · A · Phase1 기록 참조. 전체 확인 범위: [SOURCES.md](SOURCES.md#s004).

[^S030]: [Business Login for Instagram](https://developers.facebook.com/documentation/instagram-platform/instagram-api-with-instagram-login/business-login) · Meta for Developers · 게시·갱신: 2026-03-13 갱신 · 접근: 2026-10-26 · A · Phase1 기록 참조. 전체 확인 범위: [SOURCES.md](SOURCES.md#s030).

[^S041]: [n8n Plans and Pricing](https://n8n.io/pricing/) · n8n · 게시·갱신: 날짜 미상 · 접근: 2026-10-26 · A · Phase1 기록 참조. 전체 확인 범위: [SOURCES.md](SOURCES.md#s041).

[^S003]: [IG User content_publishing_limit](https://developers.facebook.com/documentation/instagram-platform/instagram-graph-api/reference/ig-user/content_publishing_limit) · Meta for Developers · 게시·갱신: 2024-07-23 갱신 · 접근: 2026-10-26 · A · Phase1 기록 참조. 전체 확인 범위: [SOURCES.md](SOURCES.md#s003).
