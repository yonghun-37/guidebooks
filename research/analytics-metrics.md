# 조회·도달·저장·공유와 API 지표 변화

작성: 2026-10-26, Codex 정리. **2026년 10월 조사 기준**(컷오프2026-10-26). Hermes 원응답과 별개인 편집본이며, 아래 사실의 확인 수준은 독립적으로 표시했다.

## 질의·원응답과 확인 범위

- 원응답: `/home/yonghun/project/hermes-research/output/ai-insta-research-20261026/raw/analytics-metrics.md`
- SHA256: `856f871ef83f376c09186989ea67b9c1bf96ab0562ad1844f12569895285a8a5`
- 원응답: `/home/yonghun/project/hermes-research/output/ai-insta-research-20261026/raw/analytics-metrics-supplement.md`
- SHA256: `a074fb56a043412e5a02ff326d2936b03e5e93671f8b60b587e3636d2983a644`

초기 응답의 가격 주제는 일부 공식 본문을 얻었고, 다수 주제는 웹 중계 프록시403으로 근거를 얻지 못했다. 보충 질의도 실행별로 평가했다. exit0·URL 존재를 본문 확인으로 세지 않았다. Codex가 별도 경로로 읽은 근거는 SOURCES의 확인 범위와 [직접 확인 기록](verification-phase-1b.json)을 따른다.

## 핵심 사실(출처 각주)

- **METRIC-01 · 확인함; Phase1b curl 재확인**: Meta 변경이력의2025-01-21 항목은 계정·미디어 인사이트 views 도입과 일부 기존 지표의 폐기를 기록한다. 폐기는 v22.0 이상에 적용하고2025-04-21 전체 버전 적용을 명시한다. 앱의 Views 통합 발표일과 API 시행일은 구분한다. [^S032]
- **METRIC-02 · 확인함; sends 동일성 미확인**: 조회 views와 고유 계정 도달 reach는 분모가 다르다. 공유·저장도 계정/미디어·지원 형식·기간을 맞춰 읽는다. 앱의 전송 sends 발언이 API shares와 정확히 같은 정의라고 가정하지 않는다. [^S110] [^S111]
- **METRIC-03 · 확인함; Phase1b curl 재확인**: 현행 미디어 문서는 views와 광고·홍보·Facebook을 포함한 total_views 등을 구분하고 일부 총 지표를 Facebook Login 전용으로 설명한다. 합산 수치를 Instagram 단독 유기적 성과와 비교하면 범위가 달라진다. [^S110] [^S032]
- **METRIC-04 · 부분 확인**: 인사이트의 빈 데이터와 측정값0은 다르다. 권한·미지원 기간·계정 요건·지표 폐기를 먼저 점검한다. 평균 시청시간의 정확한 단위·분모와 Mosseri 최초 발언 전문은 추가 확인이 필요하다. [^S109] [^S110]

## 수치 표

| 기록할 수치 | 분모/단위 | 메모 |
| --- | --- | --- |
| 조회/도달 | 재생/표시수vs고유계정 | 미디어/계정/기간분리 [^S110] [^S111] |
| 참여율 | 예:(좋아요+댓글+공유+저장)/도달×100 | 교재계산정의·플랫폼공식단일식아님 [^S110] |
| 팔로워분모참여율 | Buffer:(상호작용합)/팔로워×100 | 다른식과직접비교금지 [^S151] |
| views도입/폐기 | 2025-01-21공지·v22+/2025-04-21전체 | 앱화면도입일과별개 [^S032] |

## 한국 가용성

프로페셔널 API 문서의 범위만 확인했다. 한국 앱의 번역·계정별 인사이트·실제 반환값은 미검증이다. [^S109]

## 불확실·상충

광고·교차추천·교차게시 범위를 맞추지 않은 합산은 비교하지 않는다. views와 total_views, 평균과 합계 시청시간은 이름·기간·단위를 각각 남긴다. 고정 랭킹 가중치는 미확인이다. [^S110] [^S032]

## 교과서 반영 포인트(장 번호)

편집 제안: 날짜·포맷·주제·광고 포함 여부·조회·도달·저장·공유·프로필/링크 행동·측정불가 사유를 주간표에 남긴다.0과 빈칸을 구별하고 공유 증가를 바로 매출로 환산하지 않는다. [^S109] [^S110]

[^S032]: [Instagram Platform Changelog](https://developers.facebook.com/documentation/instagram-platform/changelog) · Meta for Developers · 게시·갱신: 최종표시2026-10-20;항목별날짜별도 · 접근: 2026-10-26 · A · 확인함. 전체 확인 범위: [SOURCES.md](SOURCES.md#s032).

[^S110]: [Instagram Media Insights](https://developers.facebook.com/documentation/instagram-platform/reference/instagram-media/insights) · Meta for Developers · 게시·갱신: 표시갱신2026-09-11 · 접근: 2026-10-26 · A · 확인함. 전체 확인 범위: [SOURCES.md](SOURCES.md#s110).

[^S111]: [Instagram Account Insights](https://developers.facebook.com/documentation/instagram-platform/api-reference/instagram-user/insights) · Meta for Developers · 게시·갱신: 2026-06-16 갱신 · 접근: 2026-10-26 · A · Phase1 기록 참조. 전체 확인 범위: [SOURCES.md](SOURCES.md#s111).

[^S109]: [Instagram Platform Insights](https://developers.facebook.com/documentation/instagram-platform/insights) · Meta for Developers · 게시·갱신: 2026-10-20 갱신 · 접근: 2026-10-26 · A · Phase1 기록 참조. 전체 확인 범위: [SOURCES.md](SOURCES.md#s109).

[^S151]: [Best Time to Post on Instagram:9.6M Posts](https://buffer.com/resources/when-is-the-best-time-to-post-on-instagram/) · Buffer · 게시·갱신: 2026-09-23 · 접근: 2026-10-26 · B · 확인함. 전체 확인 범위: [SOURCES.md](SOURCES.md#s151).
