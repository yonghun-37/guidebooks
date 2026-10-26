# 계정·보안·OAuth 준비

2026년 10월 조사 기준 · 접근일 2026-10-26 · 반영: 실습1·9

- 원응답: `/home/yonghun/project/hermes-research/output/shorts-research-20261026/raw/14-oauth-setup.md`
- SHA256: `f2db51c7a801cdd30363d67321ae62a6908ceaca1cb731e5ed6349536ece7de8`
- 원응답: `/home/yonghun/project/hermes-research/output/shorts-research-20261026/raw/14-oauth-setup-retry.md`
- SHA256: `fb4fcbc4cc7299d508542915f4bc69cd46f98996a74f837d699534938ac9191c`

Hermes는 조사 단서이며 아래 결론은 출처별 확인 수준과 상충 판정을 거쳤다. 원응답 전문은 저장소에 넣지 않는다. 직접 확인 증거는 SOURCES와 Phase Y2 결과를 참고한다.

## 핵심 사실

- **YT-074** 채널은 프로필→설정→계정→채널 추가 또는 관리→채널 만들기에서 이름과 핸들을 정한다. Google 계정과 업로드용 채널은 구별한다. [Y043](SOURCES.md#y043) — 확인.
- **YT-075** Google 계정의 보안 및 로그인→Google에 로그인하는 방법→2단계 인증에서 보안을 설정한다. [Y044](SOURCES.md#y044) — 확인.
- **YT-076** Google Auth Platform은 Branding·Audience·Data Access를 제공한다. 외부 앱의 본인 테스트 계정은 Audience→Test users→Add users→Save로 추가한다. [Y041](SOURCES.md#y041) — 공식영문메뉴확인.
- **YT-077** External+Testing의 refresh token은 보통 7일 만료이며 기본 프로필 범위 예외가 있다. YouTube 업로드 범위를 기본 프로필 예외로 취급하지 않는다. [Y042](SOURCES.md#y042) [Y037](SOURCES.md#y037) — 조건부확인.
- **YT-078** 채널 이름과 핸들은 나중에 Studio 맞춤설정→프로필에서 변경하고 게시할 수 있다. 2단계 인증의 백업 코드는 별도 안전한 곳에 보관하고 공유하지 않는다. [Y092](SOURCES.md#y092) [Y093](SOURCES.md#y093) — 직접 본문 확인.
- **YT-079** 외부 Testing 앱은 최대100명 테스트 사용자를 허용한다. Internal은 조직 내부 사용자 구분이며 혼자 쓰는 개인 앱이라는 뜻이 아니다. [Y099](SOURCES.md#y099) — 직접 본문 확인.

## 수치·비교 표

| 순서 | 설정/확인 |
|---|---|
| 1 | Cloud프로젝트선택/생성→API라이브러리→YouTube Data API v3사용 |
| 2 | Google Auth Platform→브랜딩(Branding)·대상(Audience) |
| 3 | 외부/테스트→테스트사용자추가 |
| 4 | 데이터액세스(Data Access)→필요범위 youtube.upload |
| 5 | 클라이언트(Clients)→데스크톱앱OAuth→인증파일다운로드 |
| 6 | 본인브라우저승인→로컬토큰저장 |

프로젝트/API는[Y038](SOURCES.md#y038),범위는[Y037](SOURCES.md#y037),동의화면은[Y041](SOURCES.md#y041). 5·6의구체UI와실행코드는후속실습검증대상이다.

## 한국 가용성

한국어Cloud콘솔명은번역후보이며공식영문명과병기한다. 개인Google 계정의외부테스트앱을기본시나리오로제안한다.

## 불확실·상충과 권장 결론

테스트 사용자 100명 한도는 공식 상태 안내에서 확인했다(Y099). 현재 한국어 콘솔 버튼과 로컬 인증 실행은 미실측이다. 개인 계정이라고 Internal을 선택하지 않는다. 서비스 계정이나 구형 OOB 인증을 기본 업로드 경로로 가르치지 않는다. 결제 계정 연결을 필수 단계로 추가하지 않는다.

## 교과서 반영 포인트

인증파일과refresh token은비공개로보관하고공개저장소·스크린샷에넣지않는다. 토큰만료는비밀번호오류와구별한다. 처음인증만설명하고자동화매일운영을보장하지않는다.
