# 계정 준비·보안·인증 구독과 새 계정 속설

작성: 2026-10-26, Codex 정리. **2026년 10월 조사 기준**(컷오프2026-10-26). Hermes 원응답과 별개인 편집본이며, 아래 사실의 확인 수준은 독립적으로 표시했다.

## 질의·원응답과 확인 범위

- 원응답: `/home/yonghun/project/hermes-research/output/ai-insta-research-20261026/raw/account-setup-security.md`
- SHA256: `366f395bc9aaf03d3f92f20fefa26a47e2950dc970877a5c32b4b2b2f33e9957`
- 원응답: `/home/yonghun/project/hermes-research/output/ai-insta-research-20261026/raw/account-setup-security-supplement.md`
- SHA256: `83a4b1c7714209e21209c7fd13a7dbd3cf615a3d2d558d62808e90770a75b5ce`

초기 응답의 가격 주제는 일부 공식 본문을 얻었고, 다수 주제는 웹 중계 프록시403으로 근거를 얻지 못했다. 보충 질의도 실행별로 평가했다. exit0·URL 존재를 본문 확인으로 세지 않았다. Codex가 별도 경로로 읽은 근거는 SOURCES의 확인 범위와 [직접 확인 기록](verification-phase-1b.json)을 따른다.

## 핵심 사실(출처 각주)

- **SEC-01 · 확인함; 과거 보안 원칙**: Instagram의 Security Checkup 발표는2FA·로그인 활동·복구 연락처·의심 요청 점검을 권고한다. 2021년 문서의 설정 경로가2026년 한국 앱 화면과 같다고 보장하지 않는다. [^S130]
- **SEC-02 · 확인함; 현행 개별 자격 별도**: 한국 Meta Verified 출시 발표는19세 이상 개인·크리에이터, 신분증·프로필·활동 요건·2FA와 점진 배포를 설명한다. 인증과 직접 수익화 자격·노출 보장은 같은 개념이 아니다. [^S158]
- **SEC-03 · 확인함**: 프로페셔널 계정의 유형과 Facebook 페이지 연결 필요 여부는 API·커넥터별로 다르다. Instagram Login의 페이지 불필요 조건을 Zapier·Make의 Facebook 연결 커넥터에 확대하면 안 된다. [^S002] [^S155] [^S156]
- **SEC-04 · 미확인/추가 조사 필요**: 새 계정 N일 숙성·하루 N회 활동의 안전선이나 유료 인증의 항소·추천 보장에 관한 공식 수치 근거는 확보하지 못했다. 현재 한국 앱의 최소 가입 연령·전환 시 인사이트 보존 기간·복구 기한도 추가 확인이 필요하다. [^S130] [^S158] [^S116] [^S117]

## 수치 표

| 항목 | 확인 범위 | 한계 |
| --- | --- | --- |
| MetaVerified한국출시자격 | 2023발표19세이상·ID·2FA | 현행계정/사업자상품별도 [^S158] |
| 2023발표가격 | 단일앱프로필22000원/월·두프로필35900원/월 | 과거모바일발표가·현행가격채택금지 [^S158] |
| 신규계정안전활동수/숙성일 | 미확인 | 숫자정답없음 [^S130] |

## 한국 가용성

한국 출시 발표를 읽었지만 현행 개인/기업 상품·계정별 가격·본인인증·실제 복구를 시험하지 않았다. [^S158]

## 불확실·상충

일반 Instagram의 최소 가입 연령과 Meta Verified 구독 연령은 다르다. 복구 URL의 존재와 실제 항소 성공도 구분한다. 복구업자의 보장 문구를 공식 절차의 증거로 사용하지 않는다. [^S158] [^S117] [^S130]

## 교과서 반영 포인트(장 번호)

편집 제안: 인증앱2FA·백업코드 보관·연락처 최신화·최소 권한 OAuth·시크릿 비공개를 점검한다. 비밀번호·토큰을 공개 저장소나 강의 자료에 넣지 않는다. [^S130] [^S030]

[^S130]: [Keeping Instagram Safe and Secure](https://about.fb.com/news/2021/07/keeping-instagram-safe-and-secure/) · Meta Newsroom · 게시·갱신: 2021-07-13 · 접근: 2026-10-26 · A · 확인함. 전체 확인 범위: [SOURCES.md](SOURCES.md#s130).

[^S158]: [Meta Verified 글로벌 확대 도입](https://about.fb.com/ko/news/2023/12/meta-verified/) · Meta 한국 뉴스룸 · 게시·갱신: 2023-12-01 · 접근: 2026-10-26 · A · 확인함. 전체 확인 범위: [SOURCES.md](SOURCES.md#s158).

[^S002]: [Instagram API with Instagram Login](https://developers.facebook.com/documentation/instagram-platform/instagram-api-with-instagram-login) · Meta for Developers · 게시·갱신: 2025-01-21 갱신 · 접근: 2026-10-26 · A · Phase1 기록 참조. 전체 확인 범위: [SOURCES.md](SOURCES.md#s002).

[^S155]: [How to get started with Instagram for Business on Zapier](https://help.zapier.com/hc/en-us/articles/8496101110541-How-to-get-started-with-Instagram-for-Business-on-Zapier) · Zapier · 게시·갱신: 갱신2026-01-21 · 접근: 2026-10-26 · A · 확인함. 전체 확인 범위: [SOURCES.md](SOURCES.md#s155).

[^S156]: [Instagram for Business(Facebook login)](https://apps.make.com/instagram-business) · Make Apps Documentation · 게시·갱신: 게시·갱신일 미상 · 접근: 2026-10-26 · A · 확인함. 전체 확인 범위: [SOURCES.md](SOURCES.md#s156).

[^S116]: [계정 비활성화 도움말(확인 대상)](https://help.instagram.com/366993040048856) · Instagram Help Center · 게시·갱신: 날짜 미상 · 접근: 2026-10-26 · A · Phase1 기록 참조. 전체 확인 범위: [SOURCES.md](SOURCES.md#s116).

[^S117]: [Instagram 해킹 복구 경로(확인 대상)](https://www.instagram.com/hacked/) · Instagram · 게시·갱신: 날짜 미상 · 접근: 2026-10-26 · A · Phase1 기록 참조. 전체 확인 범위: [SOURCES.md](SOURCES.md#s117).

[^S030]: [Business Login for Instagram](https://developers.facebook.com/documentation/instagram-platform/instagram-api-with-instagram-login/business-login) · Meta for Developers · 게시·갱신: 2026-03-13 갱신 · 접근: 2026-10-26 · A · Phase1 기록 참조. 전체 확인 범위: [SOURCES.md](SOURCES.md#s030).
