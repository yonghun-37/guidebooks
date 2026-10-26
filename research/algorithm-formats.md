# 추천 시스템·포맷·오리지널 콘텐츠

작성: 2026-10-26, Codex 정리. **2026년 10월 조사 기준**(컷오프: 2026-10-26). Hermes 원응답과 별개인 편집본이다.

- 원응답: `/home/yonghun/project/hermes-research/output/ai-insta-research-20261026/raw/algorithm-formats.md`
- SHA256: `bdb613b7cbfef7a8c3137f2014e6ec651368367723f038dd10f2eac3b9054da5`

## 핵심 사실(출처 각주)

- **ALG-01 · Hermes 근거**: Instagram은 2023년 공식 설명에서 Feed·Stories·Explore·Reels가 영역별 처리·예측을 사용한다고 밝혔다. 좋아요·저장·공유·시청 등 공개 신호를 고정 수치 가중치나 성공 공식으로 환산할 근거는 확인되지 않았다. [^S061]
- **ALG-02 · Hermes 근거**: 공개 계정의 추천 자격이 실제 추천 노출을 보장하지는 않는다. Account Status의 추천·삭제·기능 제한 상태와 콘텐츠 성과를 구분해서 확인해야 한다. [^S062] [^S063]
- **ALG-03 · Hermes 근거**: 2024년 공식 발표는 추천 영역에서 동일 콘텐츠의 복제본 대신 원본을 우선하고 비독창 콘텐츠 집계 계정을 제한하는 방향을 설명했다. 상당한 변경의 예외는 추천 보장·저작권 허락과 별개다. [^S064] [^S065]
- **ALG-04 · Hermes 근거**: 단순 클립 연결·워터마크 추가만으로 실질적 편집이 인정되는 것은 아니다. 공식 과거 설명에는 워터마크·저해상도·텍스트 중심 릴스의 가시성 감소 설명이 있으나 2026 로고별 집행 강도는 미확인이다. [^S061] [^S064] [^S065]
- **ALG-05 · Hermes 근거**: 직접 제작·게시 도움말의 릴스 최대20분, 3분 초과 추천 경고와 API의 3초~15분 수용 규격은 서로 다른 범위다. 촬영·가져오기·웹·한국 계정별 완전한 지원표는 미확인이다. [^S066] [^S004]
- **ALG-06 · Hermes 근거**: 직접 게시 이미지 도움말은 1.91:1~3:4를, API 레퍼런스는 4:5~1.91:1을 안내한다. 앱 지원을 API까지 확대해 해석하지 않는다. [^S069] [^S004]
- **ALG-07 · 불일치**: 직접 게시 캐러셀은 Hermes가 읽은 도움말에서 최대20개다. API는 Codex가 직접 읽은 게시 가이드도 최대20개이며, 초기 Hermes의 API10개 검색 발췌는 충돌 자료로 보존한다. [^S068] [^S001] [^S004]
- **ALG-08 · 미확인/추가 조사 필요**: AI 음성·필터·배경 변경만으로 독창성이 인정되거나 추천 제한을 면제한다는 근거와 AI 사용 자체가 일괄 추천 제한된다는 인과 근거는 확보하지 못했다. [^S064] [^S065]

## 수치 표

| 항목 | 값·적용 범위 | 판정·출처 |
| --- | --- | --- |
| 직접 게시 릴스 | 도움말 최대20분·3분초과 추천 경고 | Hermes 원문; 한국 계정별·영문 문맥 미확인 [^S066] |
| 앱 릴스 규격 | 1.91:1~9:16·최소720픽셀·30FPS | 720을 가로폭으로 임의 해석하지 않음 [^S067] |
| API 릴스 규격 | 3초~15분·23~60FPS·최대300MB | Codex 본문 확인 [^S004] |
| 캐러셀 | 앱 도움말20개; API 게시 가이드20개 | 초기 API10개 발췌 교정 [^S068] [^S001] |
| 이미지 비율 | 직접 게시 1.91:1~3:4 / API 4:5~1.91:1 | 경로 차이를 구분 [^S069] [^S004] |
| 추천 가중치·성장 임계값 | 공개된 확정 수치 미확인 | 시뮬레이터는 교육용 가정 [^S061] |

## 한국 가용성

- 한국어 도움말 열람은 한국 모든 계정의 실제 촬영·업로드·추천 동작 확인과 다르다. 일부 기능의 계정별 제공 차이는 남아 있다. [^S066]
- 글로벌 API 규격은 확인했지만 한국 계정 승인·게시를 수행하지 않았다.

## 불확실·상충

- 2025년 watch time/likes/sends 설명은 최초 공식 게시물의 전체 문맥·날짜를 확보하지 못해 “2026 공식 3대 지표”로 확정하지 않았다.
- 2025-01-18 3분 지원 발표는 과거 자료이고 현행 최대 길이·전체 한국 배포 시점을 입증하지 않는다. [^S070]
- 집계 계정의 과거 30일/10회 숫자를 현재 안전 임계값으로 사용하지 않는다. 오리지널 대체 예외와 저작권 허락도 구분한다.
- API 규격 표의 출처를 직접 게시 표에 혼합하지 않는다. 가이드 최대20개와 남은10개 검색 발췌의 불일치는 API 노트에 보존한다.

## 교과서 반영 포인트(장 번호)

- 2장: 화면별 공개 신호·추천 자격을 설명하고 가중치 체험에는 교육용 가정 배지를 붙인다.
- 7~8장: 1080×1350 4:5 카드·1080×1920 9:16 30FPS 릴스를 학습용 선택으로 제안한다. 성과 최적값으로 설명하지 않는다.
- 11~12장: 조회 감소를 곧바로 제재로 부르지 않고 Account Status·규격·편집 품질·성과를 나눠 점검한다.

[^S061]: [Instagram Ranking Explained](https://about.instagram.com/blog/announcements/instagram-ranking-explained) · Instagram / Adam Mosseri · 게시·갱신: 2023-05-31 게시 · 접근: 2026-10-26 · A · Hermes 도입 원문·영역별 상세는 검색 발췌; 2026 가중치 동일성 미확인. 전체 메타데이터: [SOURCES.md](SOURCES.md#s061).

[^S062]: [Recommendation eligibility on Instagram](https://www.facebook.com/help/instagram/653964212890722) · Instagram Help Center · 게시·갱신: 날짜 미상 · 접근: 2026-10-26 · A · Hermes 반환 원문; 추천 자격과 보장은 다르다는 설명 확인 보고. 전체 메타데이터: [SOURCES.md](SOURCES.md#s062).

[^S063]: [Check your Account Status on Instagram](https://www.facebook.com/help/instagram/338481628002750) · Instagram Help Center · 게시·갱신: 날짜 미상 · 접근: 2026-10-26 · A · Hermes 반환 원문; 삭제·기능 제한·검토 요청 확인 보고. 전체 메타데이터: [SOURCES.md](SOURCES.md#s063).

[^S064]: [Helping Creators Find New Audiences](https://creators.instagram.com/blog/recommendations-and-originality) · Instagram for Creators · 게시·갱신: 2024-04-30 게시 · 접근: 2026-10-26 · A · Hermes 도입·원본 대체·예외 원문, 집계 계정 일부는 검색 발췌; 2026 집행 세부 미확인. 전체 메타데이터: [SOURCES.md](SOURCES.md#s064).

[^S065]: [About original content on Instagram](https://help.instagram.com/1800814370401535/) · Instagram Help Center · 게시·갱신: 날짜 미상 · 접근: 2026-10-26 · A · Hermes 원문; 단순 이어붙이기·워터마크만 추가한 편집과 저작권 별도 판단 보고. 전체 메타데이터: [SOURCES.md](SOURCES.md#s065).

[^S066]: [Instagram에서 릴스 녹화하기](https://ko-kr.facebook.com/help/456185931138729) · Meta / Instagram Help Center · 게시·갱신: 날짜 미상 · 접근: 2026-10-26 · A · Hermes 한국어 원문; 최대20분·3분초과 추천 경고, 영문 대조·한국 계정별 실측 미확인. 전체 메타데이터: [SOURCES.md](SOURCES.md#s066).

[^S004]: [IG User Media](https://developers.facebook.com/documentation/instagram-platform/instagram-graph-api/reference/ig-user/media) · Meta for Developers · 게시·갱신: 2026-09-28 갱신 · 접근: 2026-10-26 · A · Codex curl 본문 확인; JPEG 8MB·이미지 비율·릴스 3초~15분·23~60fps·300MB 확인. 전체 메타데이터: [SOURCES.md](SOURCES.md#s004).

[^S069]: [Instagram에서 공유하는 사진의 이미지 해상도](https://www.facebook.com/help/instagram/1631821640426723?locale=ko_KR) · Instagram Help Center · 게시·갱신: 날짜 미상 · 접근: 2026-10-26 · A · Hermes 한국어 원문; 직접 게시 3:4·너비1080 관련, API 규격과 별개. 전체 메타데이터: [SOURCES.md](SOURCES.md#s069).

[^S068]: [Instagram에 사진이나 동영상이 여러 개 포함된 게시물 공유하기](https://www.facebook.com/help/instagram/269314186824048?locale=ko_KR) · Instagram Help Center · 게시·갱신: 날짜 미상 · 접근: 2026-10-26 · A · Hermes 한국어 원문; 직접 게시 최대20개·캐러셀 영상은 독립 릴스가 아님. 전체 메타데이터: [SOURCES.md](SOURCES.md#s068).

[^S001]: [Content Publishing](https://developers.facebook.com/documentation/instagram-platform/content-publishing) · Meta for Developers · 게시·갱신: 2026-10-20 갱신 · 접근: 2026-10-26 · A · Codex curl 본문 확인; 한도 설명 100/50 내부 충돌, 캐러셀 20개·JPEG·게시 절차 확인. 전체 메타데이터: [SOURCES.md](SOURCES.md#s001).

[^S067]: [Reel size and aspect ratios on Instagram](https://www.facebook.com/help/instagram/1038071743007909?locale=en_US) · Instagram Help Center · 게시·갱신: 날짜 미상 · 접근: 2026-10-26 · A · Hermes 원문; 앱 규격 720픽셀·30FPS·비율 확인 보고. 전체 메타데이터: [SOURCES.md](SOURCES.md#s067).

[^S070]: [We are now supporting reels up to three minutes long on Instagram](https://www.threads.com/@mosseri/post/DE-efFqyStv) · Adam Mosseri / Threads · 게시·갱신: 2025-01-18; 검색 표시 기준 · 접근: 2026-10-26 · A · Hermes 공식 계정 검색 요약만; 2026 최대 길이 근거로 사용 금지. 전체 메타데이터: [SOURCES.md](SOURCES.md#s070).
