# Phase 1c — 스팸·비독창 추천 제한과 실제 제재 사례

**2026년 10월 조사 기준** · 컷오프/접근일 2026-10-26. 한국어 공개 웹 문서 조사이며 실제 앱 로그인·게시·지급 검증은 하지 않았다.

- 원질의: `/home/yonghun/project/hermes-research/output/ai-insta-research-20261026/queries/r2-failures.txt`
- 원응답: `/home/yonghun/project/hermes-research/output/ai-insta-research-20261026/raw/r2-failures.md`
- 원응답 SHA256: `dd2cb87f5d80d88dd633e705d121ccf2c6073bb3a5d7983a8f9d8b60f4bb73b4`
- 확인 수준: `Hermes 본문`은 Hermes가 실제 열람했다고 보고한 범위, `Codex 직접`은 독립 열람한 범위다. 검색 발췌·무일자 문서·실기기 확인을 구분한다. 출처 메타데이터는 [SOURCES](SOURCES.md), 독립 대조는 [직접 확인 기록](verification-phase-1c.json)을 따른다.

## 정책·회복의 확인 범위

| 대상 | 이번 결과 | 근거·수준 |
| --- | --- | --- |
| 무허가 접근/수집 | 한국어 약관의 허가 없는 계정 생성·정보 접근·수집 금지. 자동 접근의 로그인 무관 세부 표현은 영어 검색 발췌 범위 | [S112](SOURCES.md#s112), Hermes 한국어 본문 일부 |
| 스팸 | 매우 높은 게시·공유·상호작용·계정 생성은 수동/자동 모두 대상. 반복/비진정성에 따라 낮은 빈도에도 제한 가능 | [Spam](https://transparency.meta.com/en-us/policies/community-standards/spam), Hermes 본문. 보편적 하루 안전 횟수 미확인 |
| 2026 독창성 확대 | 2026-04-30 발표는 릴스 외 사진/캐러셀에도 비독창 재게시 계정 추천 제한을 확대. 자막/테두리/워터마크/출처 추가만으로 실질 기여 인정 아님 | [공식 발표](https://creators.instagram.com/blog/rewarding-original-creators-on-instagram), Hermes 본문 |
| 추천 회복 | 최근 이동30일 게시물 대부분이 독창적으로 평가되면 적격 회복 가능 | 같은 발표. **30일 쉬면 자동 복구**라는 뜻 아님·수치 비율/복원 시간 미확인 |
| 계정상태 | 삭제·기능 제한·검토 요청 확인 가능. 적격도 실제 추천 보장 아님 | [S063](SOURCES.md#s063)·[S062](SOURCES.md#s062), Hermes 본문 일부 |
| 비활성화 검토 | 실수라고 생각하면 로그인 후 표시 안내에 따라 검토 요청. 비활성화 메시지 없으면 다른 로그인 문제일 수 있음 | [S116](SOURCES.md#s116)의 [한국어 본문](https://help.instagram.com/366993040048856?locale=ko_KR), Hermes 확인. 실제 로그인 미실시 |

## 사건과 주장 구분

| 사례 | 확인한 처분·설명 | 한계 |
| --- | --- | --- |
| Mystalk/Ekrem Ateş | Meta는 자동화 계정으로35만명 초과 프로필을 수집·복제사이트 게시했다고 주장하며 계정 비활성화·접근철회·중지요구·2022-07-05 제소를 발표 | [Meta 집행 발표](https://about.fb.com/news/2022/07/actions-against-scraping-for-hire), Hermes 본문. **소송 당사자 주장**, 확정판결/항소/계정복구 미확인. 뉴스카드 직접 사례 아님 |
| No Kings Coalition | 2026-10-17 일시 정지·자동 검토 복원. 후속 Meta 설명은 Claude의 읽기 요청 급증에 의한 보안 오집행 | [대변인 원문 일부](https://x.com/andymstone/status/2111920686306627816)·[Bloomberg 전재 보도](https://www.straitstimes.com/world/united-states/meta-says-claude-ai-tool-triggered-no-kings-instagram-suspension), Hermes 확인. 공식 설명과 주최 측 주장 분리; AI 뉴스 자동 게시 위반 사례 아님 |

No Kings의 약1시간 자동복원(Meta 설명), 약90분 비공개·관리자 접근 지연(주최측 주장)은 다른 사건 상태/시점이다. 이를 정식 항소 처리시간·복구 보장·일반 안전 수집 한도로 쓰지 않는다. 직접 부합하는 **AI/자동화 뉴스·정보 Instagram 계정의 행위→제재→항소결과**를 모두 연결한 공개사례는 확보하지 못했다.

## 한국 적용·미확인

한국어 약관·비활성화 문서 근거와 한국 개별 계정의 실제 집행은 다르다. OS별 Account Status 전체 한국어 경로·버튼·기한·SLA·해킹복구·제재/성장 실패확률은 미확인이다. 공식 영문 경로를 한국어 실제 메뉴로 임의 번역하지 않는다. ‘AI로 만들면 밴’이라는 보편 인과도 확보되지 않았다.

## 출처 메타데이터·반영

Meta 도움말/Spam은 A·게시갱신일미상·접근2026-10-26. 2026 독창성 발표는 Instagram for Creators·A·게시2026-04-30·갱신미상, Meta 집행발표는 A·게시2022-07-05(페이지 다른 날짜2022-06-30 용도미상). 대변인 X는 A(공식 발언)·게시2026-10-18(검색표시)·부분 원문만, Straits Times/Bloomberg는 B·게시/갱신2026-10-19 09:03. 모두 Hermes 근거이고 실제 사건 기술감사/법원기록 전체를 확보한 것은 아니다.

이론2/9/11/12장. 신규 R2-RISK-01~03. RISK-04의 정책 본문 공백을 보완하되 직접 뉴스계정 사례·확률·복구 실증은 남긴다.

## 연결 출처

[S062](SOURCES.md#s062), [S063](SOURCES.md#s063), [S112](SOURCES.md#s112), [S116](SOURCES.md#s116), [S220](SOURCES.md#s220), [S221](SOURCES.md#s221), [S222](SOURCES.md#s222), [S223](SOURCES.md#s223), [S224](SOURCES.md#s224)
