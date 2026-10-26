# 자동화 실패·추천/계정 제한·복구 공백

작성: 2026-10-26, Codex 정리. **2026년 10월 조사 기준**(컷오프: 2026-10-26). Hermes 원응답과 별개인 편집본이다.

- 원응답: `/home/yonghun/project/hermes-research/output/ai-insta-research-20261026/raw/risks-failures.md`
- SHA256: `c45afc49bf08422274d8c67ef59a2d8d974dddfa89d770163ec60f6475c33ca9`

## 핵심 사실(출처 각주)

- **RISK-01 · Hermes 근거**: AI 정보 라벨, 게시물 삭제, 추천 자격, 기능/계정 제한과 수익화 적격은 별도 질문이다. AI 표시를 했다는 이유로 기만·권리 침해 등이 모두 허용된다고 볼 수 없다. [^S007] [^S062] [^S012]
- **RISK-02 · Hermes 근거**: Account Status 도움말을 읽은 알고리즘 조사에서는 삭제·기능 제한·검토 요청·추천 상태 확인을 안내했다. 위험 조사 자체에서는 관련 도움말 접근이 실패했으므로 교차 주제의 확인 범위만 채택한다. [^S063] [^S062]
- **RISK-03 · 확인함**: 공식 API의 공개 미디어 URL·권한·페이지 PPA·컨테이너 처리/만료 요건을 충족하지 못하면 게시에 실패할 수 있다. 이는 문서상 기술 실패 조건이며 실제 창작자의 제재·수익 실패 사례와 다르다. [^S001] [^S004]
- **RISK-04 · 열 수 없음**: 이용약관의 무단 자동 접근·스크래핑 예외, 스팸/가짜 참여/반복 게시의 현행 상세 판정 기준은 원문을 충분히 확보하지 못했다. 안전한 하루 게시·팔로우·댓글 횟수를 제시할 근거도 없다. [^S112] [^S113]
- **RISK-05 · 미확인/추가 조사 필요**: 계정 비활성화 이의제기와 해킹 복구의 현재 화면·자격·처리 기간은 확인되지 않았다. 두 문제를 같은 절차로 합치거나 복구 성공·기간을 보장하지 않는다. [^S116] [^S117]
- **RISK-06 · 미확인/추가 조사 필요**: 2025~2026 대량 AI·재사용 Instagram 계정의 실제 제재 통지와 전후 도달·수익을 대조한 실패 사례는 확보하지 못했다. Facebook 발표나 개인 소문을 한국 Instagram 제재 증거로 대신하지 않는다. [^S113] [^S115]
- **RISK-07 · 미확인/추가 조사 필요**: Instagram의 개인정보·뉴스 허위정보 삭제/표시·지역 적용 세부는 미확인이다. 한국 저작권·개인정보 조문과 초상 관련 확인 범위는 법률 노트의 직접 검증 항목으로 별도 연결한다. [^S114] [^S115] [^S010] [^S078]

## 수치 표

| 항목 | 값·적용 범위 | 판정·출처 |
| --- | --- | --- |
| 안전한 하루 행동 횟수 | 미확인 | API 발행 한도와 별개 [^S113] [^S001] |
| 반복/대량 제재 임계값 | 미확인 | 과거 수치를 현행 안전선으로 쓰지 않음 [^S113] |
| 보장 복구 기간 | 미확인 | 현재 도움말·화면 미확보 [^S116] [^S117] |
| AI 도달·수익 감소율 | 검증값 없음 | 실제 인과·사례 원문 미확보 [^S115] |

## 한국 가용성

- 한국 계정의 제재·추천·복구 실험을 하지 않았다. 해외 Facebook 정책을 한국 Instagram 규칙으로 전용하지 않는다.
- 한국 법률 근거는 저작권·광고·AI 표시 노트에 분리했으며 이것이 플랫폼의 한국 집행을 검증했다는 뜻은 아니다.

## 불확실·상충

- 핵심 약관·스팸·개인정보·허위정보 본문 접근 실패가 남는다. 접근 실패는 해당 사이트 장애·한국 차단·정책 부재의 증거가 아니다.
- 허위정보 정책의 국가별 변화, 공식 통지·원본 지표가 있는 AI 실패 사례, 현재 이의제기 화면을 확보하지 못했다.
- 이 노트의 운영 통제 제안은 Meta 공식 드라이런 기능·범용 중복방지·계정 안전·복구 보장이 아니다.

## 교과서 반영 포인트(장 번호)

- 9~10장: 생성→근거/권리 장부→사람 승인→드라이런→공식 게시 후보의 흐름을 제안한다.
- 9~10장: 콘텐츠 ID·해시·승인 버전·대상 계정·컨테이너/게시 결과를 기록하고 응답 단절 시 기존 결과를 먼저 확인한다.
- 12장: 비밀번호·토큰을 프롬프트·공개 저장소·로그에 넣지 않는 운영 원칙과 권한/정책 오류 시 중단을 설명한다.
- 12~13장: 확인된 실제 실패 사례를 확보하기 전까지 가상 사건을 실제 사례로 제시하지 않는다.

[^S007]: [Our Approach to Labeling AI-Generated Content and Manipulated Media](https://about.fb.com/news/2024/04/metas-approach-to-labeling-ai-generated-content-and-manipulated-media/) · Meta Newsroom · 게시·갱신: 2024-04-05 게시 / 페이지 갱신 표시 2025-10-23; 라벨 관련 본문 갱신 2024-09-12 · 접근: 2026-10-26 · A · Codex curl 본문 확인; AI info 표시와 AI 편집 메뉴 이동을 확인. 과거 사실검증 운영 설명은 현행으로 채택하지 않음. 전체 메타데이터: [SOURCES.md](SOURCES.md#s007).

[^S062]: [Recommendation eligibility on Instagram](https://www.facebook.com/help/instagram/653964212890722) · Instagram Help Center · 게시·갱신: 날짜 미상 · 접근: 2026-10-26 · A · Hermes 반환 원문; 추천 자격과 보장은 다르다는 설명 확인 보고. 전체 메타데이터: [SOURCES.md](SOURCES.md#s062).

[^S012]: [Instagram Content Monetization Policies](https://help.instagram.com/2635536099905516) · Instagram Help Center · 게시·갱신: 날짜 미상 · 접근: 2026-10-26 · A · 열 수 없음: curl HTTP 200이나 제목 외 본문 없음; web 429. 수익화 포맷 제한 독립 확인 불가. 전체 메타데이터: [SOURCES.md](SOURCES.md#s012).

[^S063]: [Check your Account Status on Instagram](https://www.facebook.com/help/instagram/338481628002750) · Instagram Help Center · 게시·갱신: 날짜 미상 · 접근: 2026-10-26 · A · Hermes 반환 원문; 삭제·기능 제한·검토 요청 확인 보고. 전체 메타데이터: [SOURCES.md](SOURCES.md#s063).

[^S001]: [Content Publishing](https://developers.facebook.com/documentation/instagram-platform/content-publishing) · Meta for Developers · 게시·갱신: 2026-10-20 갱신 · 접근: 2026-10-26 · A · Codex curl 본문 확인; 한도 설명 100/50 내부 충돌, 캐러셀 20개·JPEG·게시 절차 확인. 전체 메타데이터: [SOURCES.md](SOURCES.md#s001).

[^S004]: [IG User Media](https://developers.facebook.com/documentation/instagram-platform/instagram-graph-api/reference/ig-user/media) · Meta for Developers · 게시·갱신: 2026-09-28 갱신 · 접근: 2026-10-26 · A · Codex curl 본문 확인; JPEG 8MB·이미지 비율·릴스 3초~15분·23~60fps·300MB 확인. 전체 메타데이터: [SOURCES.md](SOURCES.md#s004).

[^S112]: [Instagram 이용약관(확인 대상)](https://help.instagram.com/581066165581870) · Instagram / Meta · 게시·갱신: 날짜 미상 · 접근: 2026-10-26 · A · Hermes 접근 실패; Codex curl도 본문 미제공. 무단 자동 접근 예외·현행 조문 미확인. 전체 메타데이터: [SOURCES.md](SOURCES.md#s112).

[^S113]: [Spam(확인 대상)](https://transparency.meta.com/policies/community-standards/spam/) · Meta Transparency Center · 게시·갱신: 날짜 미상 · 접근: 2026-10-26 · A · Hermes 접근 실패; Codex curl HTTP200이나 본문 미제공. 판정 임계값 미확인. 전체 메타데이터: [SOURCES.md](SOURCES.md#s113).

[^S116]: [계정 비활성화 도움말(확인 대상)](https://help.instagram.com/366993040048856) · Instagram Help Center · 게시·갱신: 날짜 미상 · 접근: 2026-10-26 · A · Hermes 접근 실패; 현행 메뉴·처리 기간·이의제기 조건 미확인. 전체 메타데이터: [SOURCES.md](SOURCES.md#s116).

[^S117]: [Instagram 해킹 복구 경로(확인 대상)](https://www.instagram.com/hacked/) · Instagram · 게시·갱신: 날짜 미상 · 접근: 2026-10-26 · A · Hermes 접근 실패; 로그인/복구를 실제 수행하지 않았고 현재 화면 미확인. 전체 메타데이터: [SOURCES.md](SOURCES.md#s117).

[^S115]: [Misinformation(확인 대상)](https://transparency.meta.com/policies/community-standards/misinformation/) · Meta Transparency Center · 게시·갱신: 날짜 미상 · 접근: 2026-10-26 · A · Hermes 접근 실패; 한국 현행 삭제/표시/추천 제한 세부 미확인. 전체 메타데이터: [SOURCES.md](SOURCES.md#s115).

[^S114]: [Privacy Violations(확인 대상)](https://transparency.meta.com/policies/community-standards/privacy-violations/) · Meta Transparency Center · 게시·갱신: 날짜 미상 · 접근: 2026-10-26 · A · Hermes 접근 실패; Codex curl도 제목 외 본문 미제공. 전체 메타데이터: [SOURCES.md](SOURCES.md#s114).

[^S010]: [저작권법(현행 본문)](https://www.law.go.kr/LSW/lsInfoR.do?lsiSeq=283335&chrClsCd=010202&efYd=20260811) · 국가법령정보센터 / 문화체육관광부 · 게시·갱신: 2026-02-10 개정 / 현행판 시행 2026-08-11 · 접근: 2026-10-26 · A · Codex curl 본문 확인; 제7조제5호·제28조·제35조의5·제37조 확인. 전체 메타데이터: [SOURCES.md](SOURCES.md#s010).

[^S078]: [개인정보 보호법(현행 본문)](https://www.law.go.kr/LSW/lsInfoR.do?lsiSeq=283839&chrClsCd=010202&efYd=20260911) · 국가법령정보센터 / 개인정보보호위원회 · 게시·갱신: 2026-03-10 개정 / 시행2026-09-11 · 접근: 2026-10-26 · A · Codex curl 본문 제15조·16조·23조 확인; 공개 SNS 개별 재이용 적법성은 별도. 전체 메타데이터: [SOURCES.md](SOURCES.md#s078).
