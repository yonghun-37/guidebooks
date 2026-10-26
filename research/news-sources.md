# 뉴스 소재 발굴: RSS·검색 API·정부 자료

작성: 2026-10-26, Codex 정리. **2026년 10월 조사 기준**(컷오프2026-10-26). Hermes 원응답과 별개인 편집본이며, 아래 사실의 확인 수준은 독립적으로 표시했다.

## 질의·원응답과 확인 범위

- 원응답: `/home/yonghun/project/hermes-research/output/ai-insta-research-20261026/raw/news-sources.md`
- SHA256: `a25186f955fc1c5586cfc240eb0b11a4cc4a9bc5795a612bc4664392aa616fa3`
- 원응답: `/home/yonghun/project/hermes-research/output/ai-insta-research-20261026/raw/news-sources-supplement.md`
- SHA256: `ef3dcbfadde3f843989d6e75fa6296bf740cdbdb2e27cf94207e02317152860c`

초기 응답의 가격 주제는 일부 공식 본문을 얻었고, 다수 주제는 웹 중계 프록시403으로 근거를 얻지 못했다. 보충 질의도 실행별로 평가했다. exit0·URL 존재를 본문 확인으로 세지 않았다. Codex가 별도 경로로 읽은 근거는 SOURCES의 확인 범위와 [직접 확인 기록](verification-phase-1b.json)을 따른다.

## 핵심 사실(출처 각주)

- **NEWS-01 · 확인함**: 기존 네이버 뉴스검색 문서는XML/JSON,제목·원문링크·요약·발행시각 등 검색결과와 하루25000회 호출한도를 설명한다. 검색 API 반환 필드는 기사/사진 재게시 라이선스가 아니다. [^S120] [^S010]
- **NEWS-02 · 확인함**: NAVER API HUB 공식 뉴스검색 문서는/search/v1/news와NCP API키 헤더·25000회/일을 안내한다. 개발자센터 기존 경로와 인증·호스트가 다르므로 신규 가입 실습 경로를 구분해야 한다. [^S159] [^S120]
- **NEWS-03 · 검색 발췌; 신규 절차 실증 없음**: 네이버 공식 공지 검색색인에는2026-07-31 신규신청 중단·기존 이용자의2027-06-30까지 이관 유예가 나타난다. 직접 공지 본문이 비어 정확한 일정과 예외 전체는 추가 확인 대상으로 남긴다. [^S160]
- **NEWS-04 · 확인함**: NewsAPI Developer는개발/테스트용100요청/일·24시간지연을 표시하며 약관은 내부를 포함한 staging/production에 무료플랜 사용을 금지한다. 유료API를 사도 저작권 기사 복제·재게시가 포괄 허락되는 것은 아니다. [^S161] [^S162]
- **NEWS-05 · 부분 확인; 개별 서비스 약관 추가 필요**: 공공 보도자료도 개별 공공누리·첨부물 권리를 확인해야 한다.2/4유형의 비상업 조건이나3/4유형의 변경금지를 뉴스카드 요약용 허락으로 바꿀 수 없다. RSS·빅카인즈·공공데이터의 개별 상업 재이용 조건은 별도 미확인이다. [^S128] [^S010]

## 수치 표

| 소스 | 기술·무료 관찰값 | 이용 판단 |
| --- | --- | --- |
| NAVER 기존 검색 | 25000회/일·기존앱인증 | 신규신청경로변경공백 [^S120] [^S160] |
| NAVER API HUB | 25000회/일·NCP헤더 | 신규등록·청구·저장/재게시약관별도 [^S159] |
| NewsAPI Developer | 100회/일·24시간지연 | 개발/테스트만,운영불가 [^S161] [^S162] |
| 정부·RSS | 자료별 표식/계약 | 전체무료재게시로일괄판정금지 [^S128] [^S010] |

## 한국 가용성

국내 뉴스 발굴용 네이버 문서는 한국어다. 신규 키 발급·로그인·유료 등록은 하지 않았다. 한국어 검색 지원이 기사 전문 복제·광고 소재 사용 허락은 아니다. [^S159] [^S010]

## 불확실·상충

NAVER 기존/신규 경로의 차이는 우선 이관·대상 차이로 기록하고 한도 자체의 상충으로 만들지 않는다. NewsAPI의 연/월결제 토글과 월표시가 혼재해 유료 금액을 교재 기본예산으로 채택하지 않았다. 공공데이터/API별 재배포조건은 남아 있다. [^S159] [^S160] [^S161]

## 교과서 반영 포인트(장 번호)

편집 제안: 소재 목록에는 제목·원문URL·게시일·사건일·접근일·권리표식을 남긴다. 원문을 읽고 사실을 다시 쓰며 사진/도표 권리는 별도 확인한다. 실행 코드·RSS 채택은 후속 Phase에서 결정한다. [^S120] [^S010] [^S128]

[^S120]: [검색 > 뉴스 API](https://developers.naver.com/docs/serviceapi/search/news/news.md) · NAVER Developers · 게시·갱신: 게시·갱신일 미상 · 접근: 2026-10-26 · A · 확인함. 전체 확인 범위: [SOURCES.md](SOURCES.md#s120).

[^S010]: [저작권법(현행 본문)](https://www.law.go.kr/LSW/lsInfoR.do?lsiSeq=283335&chrClsCd=010202&efYd=20260811) · 국가법령정보센터 / 문화체육관광부 · 게시·갱신: 2026-02-10 개정 / 현행판 시행 2026-08-11 · 접근: 2026-10-26 · A · Phase1 기록 참조. 전체 확인 범위: [SOURCES.md](SOURCES.md#s010).

[^S159]: [NAVER API HUB 뉴스 검색 결과 조회](https://api.ncloud-docs.com/docs/naver-api-hub-search-news) · NAVER Cloud · 게시·갱신: 게시·갱신일 미상 · 접근: 2026-10-26 · A · 확인함. 전체 확인 범위: [SOURCES.md](SOURCES.md#s159).

[^S160]: [네이버 API 이관·이용약관 개정 공지(목록)](https://developers.naver.com/notice/?page=1) · NAVER Developers · 게시·갱신: 검색표시2026-07-20 · 접근: 2026-10-26 · A · 검색 발췌. 전체 확인 범위: [SOURCES.md](SOURCES.md#s160).

[^S161]: [News API Pricing](https://newsapi.org/pricing) · NewsAPI · 게시·갱신: 게시·갱신일 미상 · 접근: 2026-10-26 · A · 확인함. 전체 확인 범위: [SOURCES.md](SOURCES.md#s161).

[^S162]: [News API Terms of Service](https://newsapi.org/terms) · NewsAPI · 게시·갱신: 갱신2020-04-30 · 접근: 2026-10-26 · A · 확인함. 전체 확인 범위: [SOURCES.md](SOURCES.md#s162).

[^S128]: [저작권정책·공공누리 유형 안내](https://goe.go.kr/goe/cm/cntnts/cntntsView.do?cntntsId=1046&mi=10092) · 경기도교육청 · 게시·갱신: 최종수정2026-02-11 · 접근: 2026-10-26 · A · 확인함. 전체 확인 범위: [SOURCES.md](SOURCES.md#s128).
