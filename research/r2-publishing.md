# Phase 1c — 캐러셀·릴스 게시와 링크 복사

**2026년 10월 조사 기준** · 컷오프/접근일 2026-10-26. 한국어 공개 웹 문서 조사이며 실제 앱 로그인·게시·지급 검증은 하지 않았다.

- 원질의: `/home/yonghun/project/hermes-research/output/ai-insta-research-20261026/queries/r2-publishing.txt`
- 원응답: `/home/yonghun/project/hermes-research/output/ai-insta-research-20261026/raw/r2-publishing.md`
- 원응답 SHA256: `b78a7c0bca0732474c6dc665f258449e6ca932ce8775304fd7b3e7c62f02b99e`
- 확인 수준: `Hermes 본문`은 Hermes가 실제 열람했다고 보고한 범위, `Codex 직접`은 독립 열람한 범위다. 검색 발췌·무일자 문서·실기기 확인을 구분한다. 출처 메타데이터는 [SOURCES](SOURCES.md), 독립 대조는 [직접 확인 기록](verification-phase-1c.json)을 따른다.

## 확인한 절차

| 작업 | 공식 한국어 본문에서 확인한 순서 | 근거·범위 |
| --- | --- | --- |
| 캐러셀 | 상단 만들기/피드 오른쪽 밀기 → 게시 → 여러 항목 선택 → 사진·동영상 최대 20개 선택 → 각 항목 프레임 조정 → 다음 → 필터·길게 눌러 끌어 재정렬 → 다음 → 캡션/위치/태그 → 공유하기 | [S068](SOURCES.md#s068), Hermes Android/iPhone 본문; 최종 공유하기 문자열은 Android 공식 미러 |
| 릴스 진입 | Android: 프로필 사진 → 새로 만들기 → 릴스. iPhone: 피드 하단 만들기 → 릴스 | [릴스 녹화](https://help.instagram.com/2720958398006062/?cms_platform=iphone-app&helpref=platform_switcher&locale=ko_KR), Hermes OS별 한국어 본문 |
| 릴스 가져오기·편집 | 왼쪽 아래 카메라 롤에서 가져오기 → 다음 → 오디오/텍스트/스티커·동영상 수정·클립 추가 등 편집 | 같은 문서. ‘카메라 롤’은 설명문이며 실제 버튼 이름으로 확정하지 않음 |
| 릴스 표지·공유 | 편집 → 다음 → 커버 수정 → 프레임/기기 사진 선택 → 캡션·위치 등 → 공유하기 | 같은 문서의 iPhone 후반 본문. Android 후반 단계는 추출 누락 |
| 자동 음성인식 자막 | 동영상 선택 → 다음 → 다음 → 옵션 더 보기 → 선택 캡션 활성화 | [선택 캡션](https://help.instagram.com/7487270478066359/?cms_platform=iphone-app&helpref=platform_switcher&locale=ko_KR), Hermes iPhone 한국어 본문 |
| 직접 녹음 | 클립 선택/녹화 → 동영상 수정 → 보이스오버 → 녹화 → 완료. 시작 위치는 슬라이더 | [보이스오버](https://help.instagram.com/2828827904041367/?cms_platform=android-app&helpref=platform_switcher&locale=ko_KR), Hermes Android 본문 |
| 게시물 주소 | 게시물 아래 보내기 → 링크 복사 | [URL 얻기](https://help.instagram.com/372819389498306/?cms_platform=android-app&locale=ko_KR), Hermes Android/iPhone 본문 |
| 릴스 주소 | 릴스 열기 → 오른쪽 아래 공유 옵션 → 링크 복사 | [릴스 관리](https://help.instagram.com/742856103197927/?cms_platform=iphone-app&helpref=platform_switcher&locale=ko_KR), Hermes iPhone 본문 |

## 수치·한국 가용성

캐러셀 20개는 도움말 본문 및 Codex가 직접 읽은 S068 메타데이터가 일치한다. 계정별 실제 선택 가능 개수는 미검증이다. 릴스 제작 문서는 본문 최대 20분과 상단 소개 3분이 혼재한다. 이를 모든 한국 계정의 촬영·가져오기 상한으로 고정하지 않는다. API의 별도 길이 제한과 구분한다. [S068](SOURCES.md#s068) [릴스 녹화](https://help.instagram.com/2720958398006062/?cms_platform=iphone-app&helpref=platform_switcher&locale=ko_KR)

## 불확실·상충

- 선택 번호·선택순서 유지 규칙·권한 팝업·다음 버튼 횟수의 전 계정 동일성은 미확인. 문서가 안내한 재정렬로 최종 순서를 확인한다.
- **커버 수정** 확인을 프로필 그리드 크롭 위치 확인으로 확대하지 않는다. 게시 후 표지 수정 불가라는 검색 발췌도 확정값으로 채택하지 않는다.
- /1038071743007909는 크기/화면 비율 문서다. 제작 흐름 증거는 /2720958398006062를 사용한다. 기존 S066의 다른 URL 기록은 보존하고 이번 절차 근거 URL을 별도로 등록한다.
- 현재 캐러셀 본문에는 게시 후 더보기 → 수정 → 길게 눌러 순서 변경 → 완료 안내도 있다. ‘게시 후 재정렬 불가’로 단정하지 않으며 실제 한국 계정 적용·도입 시점은 미확인이다.
- 한국어 도움말 제공은 한국의 모든 계정에 자막·음원·여러 캡션이 제공됨을 보장하지 않는다. 자동 자막과 본문 캡션, 보이스오버와 텍스트 음성 변환을 구분한다.
- 최종 성공 메시지·대기시간·실게시 결과는 미확인. 게시된 대상을 다시 열어 내용/순서/재생/URL을 확인하라는 것은 **검증 권고**다.
- 비공개 게시물 URL은 팔로워에게만 보일 수 있다. URL 복사가 일반 공개를 뜻하지 않는다. [URL 얻기](https://help.instagram.com/372819389498306/?cms_platform=android-app&locale=ko_KR)

## 출처 메타데이터·반영

위 도움말은 모두 Meta/Instagram, A(공식), 게시·갱신일 미상, 접근 2026-10-26. S068의 한국어 본문 URL은 https://help.instagram.com/269314186824048/?cms_platform=android-app&helpref=platform_switcher&locale=ko_KR 이며 iPhone은 해당 플랫폼 매개변수로 구분한다. 이번 절차 확인은 Hermes 보고이고 Codex 독립 HTTP에서는 S068 본문을 받지 못했다.

실습 7·이론 7/8장에 제공할 근거다. R2-PUB-01~03. 메뉴 문자열을 실제 앱 실증으로 표기하지 않으며 사이트·키트에는 반영하지 않았다.

## 연결 출처

[S068](SOURCES.md#s068), [S242](SOURCES.md#s242), [S243](SOURCES.md#s243), [S244](SOURCES.md#s244), [S245](SOURCES.md#s245), [S246](SOURCES.md#s246)
