# Phase 1c — Instagram 테스터 수락과 Business Suite 데스크톱

**2026년 10월 조사 기준** · 컷오프/접근일 2026-10-26. 한국어 공개 웹 문서 조사이며 실제 앱 로그인·게시·지급 검증은 하지 않았다.

- 원질의: `/home/yonghun/project/hermes-research/output/ai-insta-research-20261026/queries/r2-tester-suite.txt`
- 원응답: `/home/yonghun/project/hermes-research/output/ai-insta-research-20261026/raw/r2-tester-suite.md`
- 원응답 SHA256: `a82e0c96e84e8568988885ef2ab8576a8813d17bd2838fab88d2b68b88dfbc71`
- 확인 수준: `Hermes 본문`은 Hermes가 실제 열람했다고 보고한 범위, `Codex 직접`은 독립 열람한 범위다. 검색 발췌·무일자 문서·실기기 확인을 구분한다. 출처 메타데이터는 [SOURCES](SOURCES.md), 독립 대조는 [직접 확인 기록](verification-phase-1c.json)을 따른다.

## 핵심 사실·확인 절차

| 대상 | 확인한 한국어 메뉴·정책 범위 | 근거·수준 |
| --- | --- | --- |
| Instagram 웹 앱 관리 진입 | 더 보기 → 설정 → 내 앱 및 미디어 아래 웹사이트 권한 → 앱 및 웹사이트 | [앱 관리](https://help.instagram.com/1144624522593085?locale=ko_KR), Hermes 본문. **테스터 초대 수락 경로 자체는 아님** |
| 테스터 초대 수락 | 현행 초대 탭·수락 버튼·한국어 명칭·Android/iPhone 전체 경로 **미확인** | [S179](SOURCES.md#s179). 과거 Basic Display 커뮤니티 답변을 현행 증거로 채택하지 않음 |
| Suite 게시 대상 | 게시물 만들기 → 게시할 위치에서 Instagram 선택(Facebook 선택 시 해제) → 미디어 → 게시물 상세 정보 | [데스크톱 작성](https://www.facebook.com/business/help/942827662903020?locale=ko_KR&helpref=uf_permalink), Hermes 한국어 본문 |
| 예약 | 예약 옵션 → 날짜·시간 → 예약 | 같은 데스크톱 문서 |
| 목록·변경 | 대상 Instagram 선택 → 플래너 → 예약 콘텐츠 → 옵션 → 일정 변경/삭제 | [데스크톱 플래너](https://www.facebook.com/business/help/1678733516458988?locale=ko_KR), Hermes 한국어 본문 |
| 관리 항목 | 게시물 수정·게시물 일정 변경·임시 저장본으로 이동·게시물 삭제. ‘예약 취소’로 임의 이름 변경하지 않음 | 데스크톱 작성 문서의 [다른 공식 호스트](https://business.facebook.com/business/help/942827662903020?locale=ko_KR), Hermes 본문 |
| 페이지 미연결 | 프로페셔널 Instagram 자격증명으로 Suite 접근 가능 경로. 포트폴리오 추가와 Facebook 페이지 연결은 다름 | [S038](SOURCES.md#s038)의 [영문 문서](https://business.facebook.com/business/help/428687951269163), Hermes 본문 |

## 수치·한국 가용성

Suite 데스크톱 작성 도움말의 Instagram 사진 수는 최대 10장이다. 앱/API 캐러셀 20개와 제품별 문서 범위를 분리한다. ‘활동 시간’은 지난 7일의 팔로워 활동 추천이며 **시간대 설정**의 근거가 아니다. 전체 관리/콘텐츠 권한이 필요하다는 문서 조건과 한국 계정 실제 기능 제공은 구분한다.

## 불확실·상충

- Instagram 대상 Suite 데스크톱 최소·최대 예약 기간·시간대 결정/선택 메뉴·OS별 화면·계정별 라벨/음원 조합은 미확인이다. Facebook 페이지 문서의 20분~29일을 Instagram 한도로 옮기지 않는다.
- 페이지 미연결 접근은 영문 공식 문서 근거지만 한국 모든 계정의 예약 기능 동일성을 보장하지 않는다.
- 콘텐츠 → 게시물 및 릴스 → 예약됨 경로는 [목록 도움말](https://www.facebook.com/business/help/2223502627919449?locale=ko_KR)에서 확인했으나 데스크톱 전용 문서가 아니므로 위 플래너 문서를 우선한다.
- Facebook Authorized App Tester 정의·수락 경로는 검색 발췌 수준이고 Instagram 테스터 수락의 증거가 아니다.
- 과거 커뮤니티의 `/accounts/manage_access/`·Tester Invites는 현행 한국어 수락 단계로 사용하지 않는다.

## 출처 메타데이터·반영

위 공식 문서는 모두 Meta/Instagram 또는 Meta 비즈니스 지원 센터, A, 게시·갱신일 미상, 접근 2026-10-26. S179 갱신 2025-09-08은 이번 Hermes 보고 범위이며 기존 Codex 직접 확인 범위를 확대하지 않는다.

실습 8/9·이론 10장. 신규 R2-SUITE-01~02·R2-TESTER-01. 데스크톱·모바일·Facebook 페이지·Instagram 계정의 근거를 분리했다. 한국 실기기와 실제 예약 발행은 미검증이다.

## 연결 출처

[S038](SOURCES.md#s038), [S040](SOURCES.md#s040), [S179](SOURCES.md#s179), [S256](SOURCES.md#s256), [S257](SOURCES.md#s257), [S258](SOURCES.md#s258)
