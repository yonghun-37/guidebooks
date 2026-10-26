# Phase 1c — 보관·삭제·복원과 인사이트

**2026년 10월 조사 기준** · 컷오프/접근일 2026-10-26. 한국어 공개 웹 문서 조사이며 실제 앱 로그인·게시·지급 검증은 하지 않았다.

- 원질의: `/home/yonghun/project/hermes-research/output/ai-insta-research-20261026/queries/r2-insights-postmanage.txt`
- 원응답: `/home/yonghun/project/hermes-research/output/ai-insta-research-20261026/raw/r2-insights-postmanage.md`
- 원응답 SHA256: `1a14004ce5bee179b35de6ac0533c283e45a440bb4a3e9a6d7154648ddce8e75`
- 확인 수준: `Hermes 본문`은 Hermes가 실제 열람했다고 보고한 범위, `Codex 직접`은 독립 열람한 범위다. 검색 발췌·무일자 문서·실기기 확인을 구분한다. 출처 메타데이터는 [SOURCES](SOURCES.md), 독립 대조는 [직접 확인 기록](verification-phase-1c.json)을 따른다.

## 보관·삭제·복원

| 작업 | 한국어 공식 본문에서 확인한 메뉴 | 근거 |
| --- | --- | --- |
| 보관 | 프로필 → 게시물 → 옵션 → 보관. 프로필에서 숨기며 좋아요·댓글 유지 | [보관](https://help.instagram.com/136706673552668?locale=ko_KR&cms_platform=android-app), Hermes Android 본문 |
| 삭제 | 게시물 → 옵션 → 삭제 → 삭제 재선택 | [삭제](https://help.instagram.com/289302621183285?locale=ko_KR&cms_platform=iphone-app), Hermes iPhone 본문 |
| 최근 삭제 | 프로필 → 메뉴 → 내 Instagram 사용 방식 아래 내 활동 → 삭제 및 보관된 콘텐츠 아래 최근 삭제 항목 | [복원](https://help.instagram.com/866270964166174?locale=ko_KR&cms_platform=iphone-app), Hermes iPhone 본문 |
| 복원/영구 삭제 | 게시물/릴스 및 동영상/스토리 선택 → 콘텐츠 → 옵션 → 복원 → 복원 또는 삭제 → 삭제 | 같은 문서 |

일반 복원 대상은 30일, 보관함에 없는 스토리는 최대 24시간이다. 서버 삭제 처리 최대 90일·백업 잔존은 사용자 복원 기간과 다른 범위다. 이미 삭제된 메시지·외부 복사본까지 복구/제거된다는 의미가 아니다. [삭제 후 처리](https://help.instagram.com/711062676142607?locale=ko_KR), Hermes 한국어 본문.

캐러셀 부분 삭제·릴스 보관의 개별 조건·인사이트 유지·확인창 전문·미디어 원본 교체는 미확인이다. 캡션 수정 도움말의 핵심 본문은 누락되어 하단 AI 안내를 공식 단계로 쓰지 않았다. 게시 후 캐러셀 재정렬은 별도 [게시 조사](r2-publishing.md)의 문서 근거와 구분한다.

## 인사이트 경로·수치

| 항목 | 확인한 내용 | 근거·수준 |
| --- | --- | --- |
| 개별 게시물 | 프로필 → 게시물 → 인사이트 보기 | [게시물 인사이트](https://help.instagram.com/553860108359435?locale=ko_KR), Hermes 한국어 본문 |
| 대시보드 | 프로필 → 프로페셔널 대시보드. 미표시 시 더 보기 → 설정 및 활동 → 프로페셔널 아래 인사이트 | [대시보드](https://help.instagram.com/257516379077270?locale=ko_KR), Hermes 한국어 본문 |
| 기간 | 상단 드롭다운, 기본 기간 5개 또는 최근 90일 이내 맞춤 기간. 5개 전체 메뉴명은 미확인 | [계정/콘텐츠](https://help.instagram.com/1533933820244654?locale=ko_KR)·[기간](https://help.instagram.com/1407497629635879?locale=ko_KR), Hermes 본문 |
| 계정 재전환 | 개인용으로 바꾸면 앱 내 인사이트 접근 불가·90일 이내 프로로 돌아오면 이전 데이터 접근 가능하다는 안내 | [문제 해결](https://help.instagram.com/684550305010470?locale=ko_KR&cms_platform=iphone-app), Hermes 본문 |

## 한국 가용성·상충

[S195](SOURCES.md#s195)와 대시보드 문서에는 공개 개인 계정의 인사이트/내 대시보드 설명이 있으나 기간·문제 해결 문서는 비즈니스/크리에이터를 명시한다. **전부 프로 전용/개인 계정 모두 제공 중 어느 쪽도 보편 단정하지 않는다.** 날짜가 없어 변경 선후도 미확인이다. 한국 계정 노출·OS별 필터 배치·전환 전 데이터 전체 범위는 실증하지 않았다.

조회수(재생·표시 횟수)와 고유 계정 수를 구분한다. 영어 Viewers·한국어 조회자/도달 표현을 모든 현재 한국 앱에 일대일로 대응시키지 않는다. 공유·저장 세부 집계/취소/중복 제거 규칙은 이번 도움말에서 확보하지 못했다. 기존 API 지표 정의 [S110](SOURCES.md#s110)·[S111](SOURCES.md#s111)는 앱 UI 정의와 분리한다.

## 출처 메타데이터·반영

위 URL은 모두 Meta/Instagram 고객 센터, A(공식), 게시·갱신일 미상, 접근 2026-10-26. 이번 메뉴 확인은 Hermes 본문 보고다. Codex 직접 S195 요청은 소개만 반환했다.

실습 1/7/10·이론 11/12장에 제공한다. 신규 R2-MANAGE-01~02·R2-INSIGHT-01~02. 실계정 보관/삭제/인사이트 조회는 하지 않았다.

## 연결 출처

[S110](SOURCES.md#s110), [S111](SOURCES.md#s111), [S195](SOURCES.md#s195), [S228](SOURCES.md#s228), [S229](SOURCES.md#s229), [S230](SOURCES.md#s230), [S231](SOURCES.md#s231), [S232](SOURCES.md#s232), [S233](SOURCES.md#s233), [S234](SOURCES.md#s234), [S235](SOURCES.md#s235), [S236](SOURCES.md#s236)
