# Phase 1c — API 이동24시간 100/50 한도 상충

**2026년 10월 조사 기준** · 컷오프/접근일 2026-10-26. 한국어 공개 웹 문서 조사이며 실제 앱 로그인·게시·지급 검증은 하지 않았다.

- 원질의: `/home/yonghun/project/hermes-research/output/ai-insta-research-20261026/queries/r2-api-limits.txt`
- 원응답: `/home/yonghun/project/hermes-research/output/ai-insta-research-20261026/raw/r2-api-limits.md`
- 원응답 SHA256: `da6ddcc9abde8222a535f0ed74820526bc4a851f95c007313810e0150941a6a7`
- 확인 수준: `Hermes 본문`은 Hermes가 실제 열람했다고 보고한 범위, `Codex 직접`은 독립 열람한 범위다. 검색 발췌·무일자 문서·실기기 확인을 구분한다. 출처 메타데이터는 [SOURCES](SOURCES.md), 독립 대조는 [직접 확인 기록](verification-phase-1c.json)을 따른다.

## 재조사 결론

**공식 문서 상충은 여전히 미해결이다.** Hermes는 가이드 일반 한도100을 본문에서, 캐러셀50과 레퍼런스 필드 설명50을 검색 발췌에서 확보했다. Codex 직접 HTML 본문 대조에서는 세 문구를 모두 읽었다. Hermes 추출 누락을 ‘공식 50 문구 삭제’로 해석하지 않는다. [S001](SOURCES.md#s001) [S003](SOURCES.md#s003)

| 문서·구획 | 이번 Codex 직접 확인 | 의미 |
| --- | --- | --- |
| Content Publishing 사용 제한 | 이동24시간 API 게시100개, 캐러셀1건, media_publish에서 적용 | 일반 가이드의 문서값 |
| 같은 문서 캐러셀 제한 | 24시간 최대50개, 캐러셀1건 | 같은 문서 내부 상충 |
| 한도 레퍼런스 필드 설명 | quota_total 현재50, quota_duration86400초 | 단지 JSON 예시에만 남은 숫자라고 정리할 수 없음 |
| 같은 레퍼런스 JSON | quota_usage2·quota_total50·quota_duration86400 | 특정 한국 계정의 실측값이 아닌 **예시** |

## 계정별 확인 절차(미실행)

공식 경로 `GET /<IG_USER_ID>/content_publishing_limit`에 `fields=quota_usage,config`를 지정하여 사용량과 한도를 함께 읽는다. `quota_usage`는 사용량이며 남은 수가 아니다. `config.quota_total`·`quota_duration`을 계정별로 확인해야 한다. fields 생략 시 기본 quota_usage라는 설명은 Hermes가 [별도 공식 경로](https://developers.facebook.com/docs/instagram-api/reference/ig-user/content_publishing_limit) 본문에서 읽었다.

이번 단계는 실계정 API 호출 금지이므로 실행하지 않았다. 한도를 조회하도록 하라는 것은 문서 기반 운영 제안이며 키트에 구현한 변경이 아니다.

## 한국 적용·상충

- Instagram/Facebook/Unified Login별 호스트·토큰 구분이 있지만 **Instagram Login100/Facebook Login50**으로 배정할 근거는 없다.
- 한국·OS별 별도 상한이나 실제 계정의 quota_total은 미확인이다.
- Hermes가 확인한 가이드 표시 갱신일2026-10-20·레퍼런스2024-07-23은 변경 시행일이 아니다. 번역/호스트별 날짜 차이의 원인도 미확인이다.
- 변경이력에서50→100 시행 근거를 확보하지 못했다. 전체 이력에 그런 기록이 절대 없다고 단정하지 않는다.

## 출처 메타데이터·반영

S001·S003·별도 레퍼런스는 Meta for Developers, A, 접근2026-10-26. 게시일 미상; 표시 갱신일은 위 범위(별도 경로는 응답에 따라 미상/2024-07-23). Codex 재요청에서는 날짜를 독립 재확인하지 못했고 **숫자와 필드 본문**을 직접 읽었다. 응답 해시·판정은 verification-phase-1c.json에 있다.

이론10·실습8/9. 신규 R2-API-01. API-04·PRAC-13은 ‘재확인했으나 불일치 유지’로 기록한다. 50/100 중 하나를 보편 기본값으로 선택하지 않는다.

## 연결 출처

[S001](SOURCES.md#s001), [S003](SOURCES.md#s003), [S207](SOURCES.md#s207)
