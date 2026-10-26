# 카드·릴스 편집 원칙과 성과 속설의 근거

작성: 2026-10-26, Codex 정리. **2026년 10월 조사 기준**(컷오프2026-10-26). Hermes 원응답과 별개인 편집본이며, 아래 사실의 확인 수준은 독립적으로 표시했다.

## 질의·원응답과 확인 범위

- 원응답: `/home/yonghun/project/hermes-research/output/ai-insta-research-20261026/raw/content-craft.md`
- SHA256: `07587909a5af2c9ce9c7c80efa5d33603fccd787a9f8406021478c5b23c978eb`
- 원응답: `/home/yonghun/project/hermes-research/output/ai-insta-research-20261026/raw/content-craft-supplement.md`
- SHA256: `3bad6c1fd58eee64bbef27b9b8d781bd1db266bdb25c8c5bd469a676aa6d7fbb`

초기 응답의 가격 주제는 일부 공식 본문을 얻었고, 다수 주제는 웹 중계 프록시403으로 근거를 얻지 못했다. 보충 질의도 실행별로 평가했다. exit0·URL 존재를 본문 확인으로 세지 않았다. Codex가 별도 경로로 읽은 근거는 SOURCES의 확인 범위와 [직접 확인 기록](verification-phase-1b.json)을 따른다.

## 핵심 사실(출처 각주)

- **CRAFT-01 · 확인함**: W3C WCAG2.2 해설은 일반 텍스트·문자 이미지의 최소 대비4.5:1, 큰 글자3:1과 예외를 설명한다. 이 값은 가독성 점검 근거이며 Instagram 추천 점수의 기준이 아니다. [^S121]
- **CRAFT-02 · 확인함**: 사전 녹화된 동기화 미디어의 자막은 대사뿐 아니라 이해에 필요한 화자·비음성 소리 정보를 포함한다는 WCAG 해설이 있다. 자막 제공과 자동 인식의 정확도는 별도다. [^S122]
- **CRAFT-03 · 확인함; 업계 자체 관찰연구**: Buffer2026-09-23 글은960만Instagram게시물을 분석하며 전체 연구는2024-01~2025-12,10플랫폼/20만이상계정/5200만게시물이다. 참여율중앙값과 현지시간정규화를 설명한다. Instagram표본계정수와 한국 뉴스계정 대표성은 별도 미확인이다. [^S151]
- **CRAFT-04 · 부분 확인; 고정 성공공식 미확인**: 첫3초·정답게시시각·해시태그 최적개수를 한국 초보자 계정의 고정 성공조건으로 정할 인과 근거는 이번에 확보하지 못했다. Meta Best Practices는 제작/참여/도달 등 계정별 학습 팁을 제공한다고 발표했다. [^S131] [^S151] [^S107]

## 수치 표

| 항목 | 값·분모 | 한계 |
| --- | --- | --- |
| 대비 | 일반4.5:1·큰글자3:1 | WCAG예외/큰글자정의확인,추천조건아님 [^S121] |
| 게시시간연구 | Instagram960만게시물·2024~2025 | Buffer고객선택편향·통제실험아님 [^S151] |
| 참여율 | (좋아요+댓글+공유+저장)/팔로워×100의중앙값 | 도달분모참여율과비교금지 [^S151] |
| 첫3초·최적해시태그 | 한국계정확정임계값미확인 | 실습설계와성과법칙구분 [^S131] |

## 한국 가용성

WCAG는 한국어 카드의 대비·자막 점검에 참고할 공개 표준이다. 게시시간 연구는 한국 시청자 전용 분석이 아니며 한국어 자동자막 실측도 하지 않았다. [^S121] [^S122] [^S151]

## 불확실·상충

광고 소재의 권고/성과를 일반 게시물 도달 상승률로 전환하지 않는다. Socialinsider의 컷오프 이후 분석기간 문제는 Phase1과 같이 보류한다. Buffer의 시간표도 개인 계정 정답으로 쓰지 않는다. [^S108] [^S151]

## 교과서 반영 포인트(장 번호)

편집 제안: 한 카드 한 주장→단위/조건→출처 순서로 쓰고 첫 화면에는 얻을 정보를 드러낸다. 자동자막의 고유명사·숫자·부정을 검수하고 게시 미리보기에서 가림을 점검한다. 여러 시간대를 같은 지표로 비교하는 기록을 제공한다. [^S121] [^S122] [^S131]

[^S121]: [Understanding SC 1.4.3 Contrast (Minimum)](https://www.w3.org/WAI/WCAG22/Understanding/contrast-minimum.html) · W3C WAI · 게시·갱신: 본문 갱신일 미상; WCAG2.2 해설 · 접근: 2026-10-26 · A · 확인함. 전체 확인 범위: [SOURCES.md](SOURCES.md#s121).

[^S122]: [Understanding SC 1.2.2 Captions (Prerecorded)](https://www.w3.org/WAI/WCAG22/Understanding/captions-prerecorded.html) · W3C WAI · 게시·갱신: 본문 갱신일 미상; WCAG2.2 해설 · 접근: 2026-10-26 · A · 확인함. 전체 확인 범위: [SOURCES.md](SOURCES.md#s122).

[^S151]: [Best Time to Post on Instagram:9.6M Posts](https://buffer.com/resources/when-is-the-best-time-to-post-on-instagram/) · Buffer · 게시·갱신: 2026-09-23 · 접근: 2026-10-26 · B · 확인함. 전체 확인 범위: [SOURCES.md](SOURCES.md#s151).

[^S131]: [Introducing Best Practices, an Education Hub for Creators on Instagram](https://about.fb.com/news/2024/10/best-practices-education-hub-creators-instagram/) · Meta Newsroom · 게시·갱신: 2024-10-01 게시·2024-09-30 병기 · 접근: 2026-10-26 · A · 확인함. 전체 확인 범위: [SOURCES.md](SOURCES.md#s131).

[^S107]: [How Often Should You Post on Instagram in 2026? What Data From 2 Million Posts Tells Us](https://buffer.com/resources/how-often-to-post-on-instagram/) · Buffer / Kirsti Lang · 게시·갱신: 표시 게시2025-08-13; 정확한 갱신일 미상 · 접근: 2026-10-26 · B · Phase1 기록 참조. 전체 확인 범위: [SOURCES.md](SOURCES.md#s107).

[^S108]: [2026 Instagram Organic Engagement Benchmarks](https://www.socialinsider.io/social-media-benchmarks/instagram) · Socialinsider / Elena Cucu · 게시·갱신: 표시 게시2026-02-20 / 메타데이터 갱신2026-10-22 · 접근: 2026-10-26 · B · Phase1 기록 참조. 전체 확인 범위: [SOURCES.md](SOURCES.md#s108).
