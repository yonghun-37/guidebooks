# YouTube Data API v3·OAuth·감사·Analytics

- Hermes 원응답: `/home/yonghun/project/hermes-research/output/advanced-research-20261026/raw/03-youtube-quota-audit.md` · SHA256 `aeadd293a120686f5d2df719a76e03d2301d1d3b14ca68c45fcb07861aa65bda` · exit 0.
- Hermes 원응답: `/home/yonghun/project/hermes-research/output/advanced-research-20261026/raw/04-youtube-fields-analytics.md` · SHA256 `ec29cc084dead594a3fdb75a676974021a8c329bc7495da3437b67755b071464` · exit 0.
- 실행·실패 구분: [provenance.json](provenance.json). 핵심 주장은 Codex 직접 열람/기존 근거와 대조했다.

2026년 10월 조사 기준 · Data API v3, Analytics API v2. 기존 `research-shorts/13-api-quota-audit.md`, `14-oauth-setup.md`, `15-analytics.md`의 근거와 키트 재개 업로드를 재사용한다.

## OAuth와 매주 끊기는 자동화

1. Google Cloud 프로젝트에서 YouTube Data API v3를 활성화한다.
2. Google Auth Platform의 Branding·Audience·Data Access를 구성한다. 개인 Gmail의 본인 실습은 `External`이며 조직 전용 `Internal`이 아니다.
3. Testing 상태면 본인 계정을 테스트 사용자에 추가한다. 업로드 최소 범위는 `https://www.googleapis.com/auth/youtube.upload`이다.
4. OAuth Client를 **Desktop app**으로 만들고 인증 설정 파일을 비공개로 내려받는다.
5. 로컬 시스템 브라우저와 loopback redirect로 최초 동의를 받고 access/refresh token을 저장한다. CI에서는 이 브라우저 인증을 매일 반복하지 않는다. [A017](SOURCES.md#a017) [A018](SOURCES.md#a018)

**External+Testing의 refresh token은 보통 7일 후 만료된다.** 기본 프로필·이메일 범위만 요청한 예외는 `youtube.upload`에 적용하지 않는다. access token 갱신 코드가 있어도 refresh token 자체의 만료를 해결하지 못한다. `invalid_grant` 때 무한 재시도하지 않고 재인증을 안내한다. [A018](SOURCES.md#a018)

매일 장기 운영하려면 Production 전환·개인 사용 예외·요청 범위의 검증 조건을 확인한 후 다시 동의받는다. **Production 버튼, OAuth 앱 검증, YouTube API 감사는 각각 다른 절차**다. 커뮤니티의 ‘본인 사용은 검증 없이 가능’ 답변을 외부 사용자 배포에 확대하지 않는다. 서비스 계정을 개인 채널 업로더의 대안으로 가르치지 않는다. [A017](SOURCES.md#a017) [A015](SOURCES.md#a015) [A117](SOURCES.md#a117)

## 할당량: 하루 몇 편인가

| 시점·범위 | 문서값 | 해석 |
|---|---|---|
| 과거 | videos.insert 약1,600 units | 현재 계산에 사용 금지 |
| 2025-12-04 변경 이력 | 약100 units | 당시 값 |
| 2026-06-01 이후 granular quota | insert 전용 버킷; 현행 1 unit/호출, 기본100호출/일 | 업로드 요청을 직접 계산 |
| search.list | 별도 기본100호출/일 | 업로드 몫을 공유하지 않음 |
| 그 밖의 엔드포인트 | 합계 기본10,000 units/일 | videos.list·update·thumbnail 등을 계산 |

직접 확인: [A012](SOURCES.md#a012) [A013](SOURCES.md#a013) [A014](SOURCES.md#a014) [A079](SOURCES.md#a079). Quota Calculator·감사 안내의 표시 갱신일은 2026-10-15이다. 날짜를 기능 시행일로 바꾸지 않는다. 일일 리셋은 Pacific Time 자정이다.

**한 편에 새 insert 1회라면 기본 버킷으로 이론상 하루100편**이다(`100÷1`). 실패/잘못된 요청도 할당량을 쓰므로 운영 성공 편수와 다르다. 채널별 업로드 제한·처리·정책·계정 상태도 적용된다. 하루1편 예제는 30일 동안 insert30회지만 일별 할당량은 월30개 풀과 다르다. 동일 세션의 재개 청크를 매번 새 insert로 계산하거나, 반대로 재시작 요청 비용을 무시하지 않는다. 자신의 Cloud Console → API → Quotas에서 **실제 버킷**을 확인한다.

## 미검증 프로젝트 비공개 잠금·감사

| 근거 | 현재 확인 |
|---|---|
| 2020년 변경 이력 | 2020-07-28 이후 생성된 미검증 API 프로젝트 업로드를 비공개로 제한, 감사로 해제하는 안내 |
| 현재 `videos.insert` | 미검증 프로젝트 업로드가 비공개로 제한되지 않는다는 문장 |
| 현재 한국어 ‘비공개 상태로 잠긴 동영상’ | 미확인 API로 잠긴 영상은 항소 불가; 검증 서비스/공식 앱 재업로드 또는 API 감사 안내 |

[A014](SOURCES.md#a014) [A012](SOURCES.md#a012) [A016](SOURCES.md#a016). **공식 문서 상충 미해결**이다. 해제 시행일·한국 계정 적용을 찾지 못했으므로 ‘2026년에는 무조건 해제’도 ‘모든 신규 프로젝트가 반드시 잠김’도 확정하지 않는다.

| 상태 | 학습자 권장 행동 |
|---|---|
| 감사 전/상태 미확인 | private로 1개 시험 → 응답 status와 Studio 제한·메일 확인. 공개 URL이 당장 필요하면 공식 Studio 업로드 |
| 비공개 잠금 발생 | `privacyStatus=public` 반복으로 해제 시도하지 않음. API 감사 또는 공식 업로드 경로 |
| 감사 승인 후 | 승인 범위 내 공개/예약 게시를 사용자 확인. 추가 할당량은 별도 승인값이며 자동증설 아님 |

감사 절차: [공식 안내 A015](SOURCES.md#a015) → [Audit and Quota Extension Form A088](SOURCES.md#a088) → 요청 유형 선택 → 프로젝트 번호·API Client·연락처·사용 사례·동의/업로드 화면 시연·정책 준수 설명 제출 → 후속 이메일 대응. 신청서의 실제 필요한 필드는 선택 유형에 따라 바뀐다. **확정 처리 일수/SLA는 확보하지 못했다.** ‘며칠이면 통과’라고 쓰지 않는다. 이번에 양식을 제출하지 않았다.

## 재개 업로드

- `POST https://www.googleapis.com/upload/youtube/v3/videos?uploadType=resumable&part=snippet,status`에 메타데이터·파일 타입/크기를 보내고 응답 `Location`을 저장한다.
- `PUT Location`으로 파일/청크를 전송한다. 마지막을 제외한 청크는 256KiB 배수다.
- 중단하면 같은 세션에 `Content-Length: 0`, `Content-Range: bytes */전체크기`로 조회한다. `308 Resume Incomplete`의 `Range` 다음 바이트부터 재개한다.
- 완료의 200/201 응답에서 영상 ID를 기록한다. 세션 만료의 404는 새 세션이 필요하지만 먼저 Studio에서 중복 여부를 확인한다. 5xx/전송 실패는 지수 대기 후 **동일 세션 상태 조회**부터 한다. [A019](SOURCES.md#a019)

YouTube는 로컬 파일 업로드이므로 Instagram 같은 공개 미디어 URL이 필요 없다. `shorts-kit/upload.py`는 이미 세션·파일/메타데이터 해시·결과 ID를 저장한다. 새 키트에서 이를 읽고 재사용하되 실제 전송 검증을 했다고 쓰지 않는다.

## 상태·예약·AI 공개

| 필드 | 값·제약 |
|---|---|
| `status.privacyStatus` | `private`·`unlisted`·`public`; 생략 시 API 기본 public이므로 **항상 명시** |
| `status.publishAt` | ISO8601 날짜. `privacyStatus=private`, 아직 공개된 적 없는 영상에 설정. 과거 시각은 즉시 공개될 수 있어 시각 검증 필요 |
| `status.selfDeclaredMadeForKids` | Boolean. 실제 아동용 대상 여부를 작성자가 판단; AI 사용 여부 아님 |
| `status.containsSyntheticMedia` | Boolean. 사실적 합성/변형 공개 여부. 대본에 LLM을 썼다는 이유로 모두 같은 값으로 강제하지 않음 |
| `isShorts` | 업로드용 status 필드가 아님. 보내지 않음 |

[A020](SOURCES.md#a020) [A012](SOURCES.md#a012) [A071](SOURCES.md#a071). 예약 전 UTC/한국시각·기존 공개 이력·승인 해시를 확인한다. API 전송 완료와 공개 처리·권리 검토·Shorts 분류 완료는 구분한다.

Shorts: 일반 채널은 2024-10-15 이후 업로드한 정사각/세로, 최대3분 영상이 대상이다. 공식 아티스트/음악 Content Owner 연결 채널에는 2025-12-08 분기 예외가 있다. `#Shorts`만 붙여 가로 긴 영상을 쇼츠로 바꾸지 못한다. [A022](SOURCES.md#a022)

## 썸네일

`thumbnails.set`은 별도 업로드 메서드이며 `image/jpeg`·`image/png` 등을 받는다. **현재 API 레퍼런스의 최대 파일값은 50MB**, 비용은 약50 units다. 흔한 ‘2MB’ 과거 안내를 API 현행값이라고 단정하지 않는다. [A021](SOURCES.md#a021)

현재 공식 도움말은 **인증된 계정의 PC Studio에서 Shorts 사용자 썸네일 파일 업로드**를 안내한다. 과거의 ‘Shorts는 프레임 선택만 가능’ 안내를 현행으로 반복하지 않는다. PC 파일 상한50MB와 모바일 일반 영상2MB는 서로 다른 조건이다. 2026-09-14 변경 이력도 API 상한2→50MB를 기록한다. API 설정 뒤 검색·채널·Shorts 피드 각각의 반영은 사용자가 확인한다. [A124](SOURCES.md#a124) [A014](SOURCES.md#a014)

## Analytics API

업로드 scope만으로 분석 권한을 대신하지 않는다. 기본 분석은 `yt-analytics.readonly`, 수익 보고는 `yt-analytics-monetary.readonly`와 실제 수익화 접근 조건을 확인한다. Analytics의 `reports.query`에서 `ids=channel==MINE`, `startDate`, `endDate`, `metrics`, `dimensions=day` 또는 `video`, 필요 시 `filters=video==ID`를 사용한다. 모든 지표/차원 조합이 유효한 것은 아니다. [A024](SOURCES.md#a024)

| API metric | 의미·단위 |
|---|---|
| `views` / `engagedViews` | 재생/유효 시청; Shorts 공개 조회수 분모와 유효 시청을 구별 |
| `estimatedMinutesWatched` | 추정 시청 시간, 분 |
| `averageViewDuration` | 평균 시청 시간, 초 |
| `averageViewPercentage` | 평균 시청 비율, % |
| `subscribersGained`, `subscribersLost` | 구독 증가·감소 |
| `estimatedRevenue` | 추정 수익; 수익 scope·보고서 조건과 currency 확인 |

[A023](SOURCES.md#a023). API는 요청한 모든 지표가 준비된 마지막 날짜까지만 반환한다. ‘오늘까지’ 요청해도 오늘 데이터가 없을 수 있다. 확정된 공통 지연 시간을 만들어 넣지 않는다. 수익·시청 지표를 나눠 조회하고 반환 날짜·단위·조회시각을 CSV에 저장한다. Studio의 realtime 카드와 같은 숫자라고 가정하지 않는다. [A024](SOURCES.md#a024)

한국 실계정 OAuth·업로드·지표 조회는 하지 않았다. A2/A5/A6/A8/A9에 반영한다.
