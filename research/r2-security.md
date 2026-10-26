# Phase 1c — 인증 앱과 백업 코드

**2026년 10월 조사 기준** · 컷오프/접근일 2026-10-26. 한국어 공개 웹 문서 조사이며 실제 앱 로그인·게시·지급 검증은 하지 않았다.

- 원질의: `/home/yonghun/project/hermes-research/output/ai-insta-research-20261026/queries/r2-security.txt`
- 원응답: `/home/yonghun/project/hermes-research/output/ai-insta-research-20261026/raw/r2-security.md`
- 원응답 SHA256: `f111607559c8352b3c87fe15ba9e4ff19ec04dc5e0f3dfe76e1af7260e15c317`
- 확인 수준: `Hermes 본문`은 Hermes가 실제 열람했다고 보고한 범위, `Codex 직접`은 독립 열람한 범위다. 검색 발췌·무일자 문서·실기기 확인을 구분한다. 출처 메타데이터는 [SOURCES](SOURCES.md), 독립 대조는 [직접 확인 기록](verification-phase-1c.json)을 따른다.

## 핵심 사실·절차

| 작업 | 확인한 한국어 공식 메뉴·범위 | 근거·수준 |
| --- | --- | --- |
| 인증 앱 설정 | 프로필/프로필 사진 → 메뉴 → 계정 센터 → 비밀번호 및 보안 → 2단계 인증 → 사용할 Instagram 계정 선택 → 인증 앱 → 다음 → 인증 앱이 생성한 코드 입력으로 완료 | [S181](SOURCES.md#s181), Hermes 한국어 Android 본문 |
| 백업 코드 조회 | 프로필 → 메뉴 → 계정 센터 → 비밀번호 및 보안 → 2단계 인증 → 대상 계정 → 추가 방법 → 백업 코드 | [S182](SOURCES.md#s182), Hermes 한국어 Android 본문·공식 Facebook 도메인의 Instagram 문서 교차 열람 |
| 재발급 | 같은 화면에서 새 코드 받기. 이전 목록을 취소하고 새 목록을 받는 작업 | [S182](SOURCES.md#s182), Hermes 본문 |
| 보관 | 문서가 복사·스크린샷 등 저장 방법을 안내함. 저장 방식의 실제 보안성까지 검증한 것은 아님 | [S182](SOURCES.md#s182), Hermes 본문 |

## 수치·한국 가용성

백업 코드의 **개수·자릿수·개별 사용 횟수·만료 기간은 미확인**이다. 한국어 Android 도움말이 있다는 사실과 한국의 모든 계정/앱 버전에 같은 화면이 노출된다는 사실을 구분한다. iPhone 상세 한국어 순서는 본문 확보에 실패했다. [S181](SOURCES.md#s181) [S182](SOURCES.md#s182)

## 불확실·상충

- Hermes는 계정에 따라 ‘계정 센터’ 대신 ‘Meta 계정 설정’이 표시될 수 있다는 전환 안내를 읽었다. Meta 계정 전용 경로를 Instagram에 옮기지 않는다.
- QR·설정 키 복사·앱 내부 등록·최종 완료 버튼 이름은 확보한 본문에 없다. 인증 코드 입력까지 완료해야 한다는 조건만 채택한다.
- Codex가 같은 Android·한국어 URL을 직접 요청했지만 본문 없이 도움말 껍데기만 받았다. 따라서 **기존 메타데이터 → Hermes 한국어 본문 근거로 상향**, Codex 독립 메뉴 확인으로는 올리지 않는다.
- 도움말 게시·갱신일은 미상이다. 접근일을 UI 변경일로 사용하지 않는다.

## 출처와 교과서 반영

- S181의 한국어 Android 원문: https://help.instagram.com/1582474155197965/?cms_platform=android-app&locale=ko_KR
- S182의 한국어 Android 원문: https://help.instagram.com/1006568999411025/?cms_platform=android-app&locale=ko_KR
- S182의 공식 미러: https://www.facebook.com/help/instagram/1006568999411025?cms_platform=android-app&locale=ko_KR
- 모두 Meta/Instagram 고객 센터, 게시·갱신일 미상, 접근 2026-10-26, A(공식).

실습 1·이론 4/12장의 경로 근거로 제공한다. 실습 확인 목록에는 Android 문서 확인과 iPhone/실기기 미확인을 함께 적는다. 신규 사실 ID R2-SEC-01~02. 사이트 원고와 생성 스크립트는 이번 단계에서 수정하지 않았다.

## 연결 출처

[S181](SOURCES.md#s181), [S182](SOURCES.md#s182)
