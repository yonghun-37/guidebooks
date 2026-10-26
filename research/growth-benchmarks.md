# 성장 벤치마크·표본 한계·운영 지표

작성: 2026-10-26, Codex 정리. **2026년 10월 조사 기준**(컷오프: 2026-10-26). Hermes 원응답과 별개인 편집본이다.

- 원응답: `/home/yonghun/project/hermes-research/output/ai-insta-research-20261026/raw/growth-benchmarks.md`
- SHA256: `0b2c685ee9ec66cf83fdb67e5389e244cb2c07613d8e5bb2db023d28fc6aa4bb`
- 원응답: `/home/yonghun/project/hermes-research/output/ai-insta-research-20261026/raw/growth-benchmarks-supplement.md`
- SHA256: `d33e49deb0ab0188ae78542d6bfdd19db3e3595ef242b420c6260a981c060a8c`

## 핵심 사실(출처 각주)

- **GROW-01 · 확인함**: Buffer 연구 본문은 210만 게시물·약102000계정의 피드 사진·릴스·캐러셀을 분석하고 Stories는 제외했다고 설명한다. 계정별 기준 성장 대비 z-score 비교는 게시 빈도와 성장의 관찰 관계이며 무작위 실험이나 한국 뉴스 계정 예측치가 아니다. [^S107]
- **GROW-02 · 불일치**: Socialinsider의2026년 보고서 페이지는 방법론에2024년1월~2026년12월을 분석 기간으로 적어 조사 컷오프2026-10-26을 넘는다. 소개의3500만과 방법론의약6754만 게시물 및 계정 규모 문구도 혼재해 성과 수치 채택을 보류한다. [^S108]
- **GROW-03 · 확인함**: Meta 계정 인사이트의 reach는 광고를 포함한 콘텐츠를1회 이상 본 고유 계정 수인 추산치다. views는 콘텐츠가 재생·표시된 횟수로 고유 계정 수와 구분한다. 계정 지표와 미디어별 지표의 범위를 섞지 않는다. [^S111] [^S110]
- **GROW-04 · 확인함**: 미디어의 saved는 저장한 횟수, shares는 공유 횟수로 문서화되어 있다. 계정 수준 저장 지표명 saves와 미디어 수준 saved도 다르며 모든 값이 고유 사람 수라는 가정을 하지 않는다. [^S110] [^S111]
- **GROW-05 · 확인함**: 릴스 ig_reels_video_view_total_time은 재시청을 포함한 총 재생 시간, ig_reels_avg_watch_time은 평균 재생 시간으로 문서화된다. 확보한 절에서 단위·평균 분모를 끝까지 확인하지 못해 조회수로 임의 나눠 같은 값이라고 설명하지 않는다. [^S110]
- **GROW-06 · 확인함**: 인사이트 API는 프로페셔널 계정을 대상으로 하고 Instagram Login 인사이트 권한은 instagram_business_manage_insights 등이 게시 권한과 별도로 필요하다. 데이터가 없거나 사용 불가일 때 빈 데이터가 반환될 수 있어0으로 해석하면 안 된다. [^S109]
- **GROW-07 · 미확인/추가 조사 필요**: 한국 뉴스카드 계정의 대표 참여율·도달·단가·전환율, 날짜 있는 성장 사례와0→1000→10000 달성 기간을 검증한 자료는 확보하지 못했다. 해외 도구 표본이나 브랜드 평균을 개인 수익 보장으로 옮기지 않는다. [^S107] [^S108] [^S024]

## 수치 표

| 항목 | 값·적용 범위 | 판정·출처 |
| --- | --- | --- |
| Buffer 분석 표본 | 210만 게시물·약102000계정; Stories 제외 | 기간·국가 구성 미상; 관찰 연구 [^S107] |
| Buffer 빈도 구간 | 0 / 주1~2 /3~5 /6~9 /10개 이상 | 성장 권장량·보장 수치가 아닌 연구 분류 [^S107] |
| Socialinsider 성과 수치 | 채택 보류 | 방법론 종료2026-12로 컷오프초과·표본 혼재 [^S108] |
| 참여율 분모 | 연구별 팔로워/도달/조회수 등 확인 필요 | 같은 이름의 비율을 바로 비교하지 않음 [^S108] |
| 한국 성장·협찬·전환 대표값 | 미확인 | 사용자 입력 가정으로 분리 [^S024] [^S107] |

## 한국 가용성

- 해외 연구의 한국 표본 포함·한국어 뉴스 계정 대표성이 확인되지 않았다. 한국 초보자의 예상 성장률로 사용하지 않는다.
- 공식 인사이트 정의를 읽었으나 한국 계정의 로그인·인사이트 조회·특정 항목 제공은 실증하지 않았다. 계정/형식/권한별 지원을 별도 확인한다.

## 불확실·상충

- 초기·보충 Hermes는 프록시403으로 출처 원문을 읽지 못했다. 확인함은 Codex가 후보 출처와 공식 문서를 직접 대조한 부분이다.
- Socialinsider의2025값을2026제목으로 제시했다는 주석·분기 갱신·미래까지의 방법론이 혼재한다. 특정 성과 수치만 골라 채택하지 않는다. [^S108]
- Buffer 연구의 절대 분석기간·국가·계정 규모 구성·완전한 성장률 분모는 추가 확인 대상이다. z-score0.07을7% 성장으로 해석하지 않는다. [^S107]
- 평균 시청시간 단위·분모, 프로필/스토리/광고 링크 클릭 위치, 외부 전환의 기여기간을 한 수치로 합치지 않는다. [^S110]

## 교과서 반영 포인트(장 번호)

- 4장: 니치 점수표를 관심·지속 가능한 제작 시간·수요 관찰·경쟁·전환 경로의 교육용 질문으로 둔다. 검증된 성장 예측기로 부르지 않는다.
- 11장: 기간·지표명·단위·분모·계정/미디어·추산 여부·빈 데이터 상태를 같이 기록한다.
- 3·13·14장: 실측 도달·클릭·인정 구매와 가정값을 분리하고 성장 기간·예상 수익을 보장하지 않는다.

[^S107]: [How Often Should You Post on Instagram in 2026? What Data From 2 Million Posts Tells Us](https://buffer.com/resources/how-often-to-post-on-instagram/) · Buffer / Kirsti Lang · 게시·갱신: 표시 게시2025-08-13; 정확한 갱신일 미상 · 접근: 2026-10-26 · B · Codex 본문 직접 확인; 210만 게시물·102K계정·동일 계정 기준 z-score, 분석기간·국가 미상, 관찰 상관 연구. 전체 메타데이터: [SOURCES.md](SOURCES.md#s107).

[^S108]: [2026 Instagram Organic Engagement Benchmarks](https://www.socialinsider.io/social-media-benchmarks/instagram) · Socialinsider / Elena Cucu · 게시·갱신: 표시 게시2026-02-20 / 메타데이터 갱신2026-10-22 · 접근: 2026-10-26 · B · Codex 직접 확인; 방법론 종료일2026-12로 컷오프 초과, 표본·규모 설명도 내부 혼재. 성과 수치 전부 채택 보류. 전체 메타데이터: [SOURCES.md](SOURCES.md#s108).

[^S111]: [Instagram Account Insights](https://developers.facebook.com/documentation/instagram-platform/api-reference/instagram-user/insights) · Meta for Developers · 게시·갱신: 2026-06-16 갱신 · 접근: 2026-10-26 · A · Codex reach·views·saves·shares 표 직접 확인; 계정 단위와 미디어 단위 구분. 전체 메타데이터: [SOURCES.md](SOURCES.md#s111).

[^S110]: [Instagram Media Insights](https://developers.facebook.com/documentation/instagram-platform/reference/instagram-media/insights) · Meta for Developers · 게시·갱신: 2026-09-11 갱신 · 접근: 2026-10-26 · A · Codex 지표 표·적용 형식 직접 확인; 시청시간 단위/평균 분모 미확인. 전체 메타데이터: [SOURCES.md](SOURCES.md#s110).

[^S109]: [Instagram Platform Insights](https://developers.facebook.com/documentation/instagram-platform/insights) · Meta for Developers · 게시·갱신: 2026-10-20 갱신 · 접근: 2026-10-26 · A · Codex 본문 확인; 권한·개인 계정 미지원·빈 응답과0 구분. 예제 옛 지표를 실행 코드로 채택하지 않음. 전체 메타데이터: [SOURCES.md](SOURCES.md#s109).

[^S024]: [2025 Influencer Marketing Report](https://collabstr.com/2025-influencer-marketing-report) · Collabstr · 게시·갱신: 2025년판, 정확한 게시일 미상; 데이터 2024-01-01~2024-12-15 · 접근: 2026-10-26 · B · Hermes 일부; 광고주 40000·크리에이터 100000 표본 설명, 국가·팔로워 구간 단가 산식 미확인. 전체 메타데이터: [SOURCES.md](SOURCES.md#s024).
