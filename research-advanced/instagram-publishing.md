# Instagram 게시·미디어·한도·분석

- Hermes 원응답: `/home/yonghun/project/hermes-research/output/advanced-research-20261026/raw/02-instagram-media.md` · SHA256 `44f91c120d1a91ea45acdf30e1574746bb685e403e67b246d468e69de927224b` · exit 0.
- 실행·실패 구분: [provenance.json](provenance.json). 핵심 주장은 Codex 직접 열람/기존 근거와 대조했다.

2026년 10월 조사 기준 · v26.0. 기존 게시·한도 조사 재사용. 핵심 직접 확인: A006~A009, A109~A110.

## 생성 → 처리 확인 → 발행

| 형식 | `POST /{ig_id}/media` 입력 | 다음 단계 |
|---|---|---|
| 이미지 | `image_url`, `caption` | 생성 ID 상태 확인 후 발행 |
| 캐러셀 | 각 자식 `image_url` 또는 `video_url`와 `is_carousel_item=true`; 부모 `media_type=CAROUSEL`, `children`, `caption` | 자식 준비 확인 → 부모 준비 확인 → 부모만 발행 |
| 릴스 | `media_type=REELS`, `video_url`, `caption` | 영상 처리 완료 후 발행 |
| 스토리 | `media_type=STORIES`, `image_url` 또는 `video_url` | 계정/로그인별 지원 확인 후 발행 |

생성 응답 `id`는 게시물 ID가 아니다. `GET /{container_id}?fields=status_code`에서 `FINISHED`를 확인한 뒤 `POST /{ig_id}/media_publish`에 `creation_id`를 보낸다. `IN_PROGRESS`는 대기, `ERROR`·`EXPIRED`는 원인 확인, `PUBLISHED`는 중복 발행 방지에 사용한다. 컨테이너는 미발행 24시간 후 만료되며 생성 제한 400개/이동 24시간과 게시 제한은 다르다. [A006](SOURCES.md#a006) [A007](SOURCES.md#a007)

**운영 제안:** 게시 요청의 응답이 끊겼다고 새 컨테이너를 즉시 생성하지 않는다. 기존 컨테이너·게시 ID·계정 피드를 먼저 확인한다. 범용 멱등 키가 있다고 가정하지 않는다. 기존 키트의 `LIVE_ATTEMPT.json` 보호를 재사용하되 후속 구현은 재개 상태를 더 세분한다.

## 미디어 요건

| 형식 | 현행 API 문서값 | 학습용 출력 제안 |
|---|---|---|
| 피드 이미지 | JPEG, 8MB 이하, 너비 320~1440px, 비율 4:5~1.91:1, sRGB | 1080×1350 JPEG; API에 PNG 그대로 보내지 않음 |
| 캐러셀 | 게시 가이드 최대 20개; 오류표에는 2~10개 문구 잔존 | 5장으로 먼저 검증. 20개를 모든 계정 실측값으로 쓰지 않음 |
| 릴스 | MOV/MP4, H.264/HEVC, AAC(최대48kHz), 23~60fps, 3초~15분, 300MB 이하, 9:16 권장 | 1080×1920, H.264/AAC, 30fps, `+faststart` |
| 스토리 이미지 | JPEG, 8MB 이하, 9:16 권장 | Business 경로부터 사용자 확인 |
| 스토리 영상 | MOV/MP4, H.264/HEVC, AAC, 23~60fps, 3~60초, 100MB 이하 | 릴스 길이 제한과 혼동하지 않음 |

[A007](SOURCES.md#a007) [A006](SOURCES.md#a006) [A009](SOURCES.md#a009). 앱 촬영 상한·추천 노출 길이는 API 업로드 규격의 근거로 쓰지 않는다.

## 공개 URL과 resumable upload

**Instagram Login 기본 경로의 이미지·영상 URL은 Meta 서버가 인증 없이 읽을 수 있어야 한다.** 파일 선택 화면 URL·Drive 미리보기·로컬 `file://`·로그인 세션이 필요한 URL은 입력이 아니다. `GET`으로 파일 본문·MIME·상태를 확인하고, 만료 링크는 처리 완료까지 유효해야 한다. [A006](SOURCES.md#a006) [A007](SOURCES.md#a007)

Facebook Login for Business의 영상 재개 업로드는 `upload_type=resumable`로 컨테이너/업로드 URI를 만든 뒤 `rupload.facebook.com/ig-api-upload/v26.0/{container_id}`에 로컬 바이너리를 보낸다. 예시는 Authorization과 `offset`, `file_size`, `--data-binary`를 사용한다. **이 경로의 영상은 공개 영상 URL 없이 올릴 수 있지만, 이미지 URL과 별도 커버 이미지 URL까지 없애지는 않는다.** [A006](SOURCES.md#a006) [A007](SOURCES.md#a007)

> 확인할 점: 현재 게시 가이드는 재개 세션을 Facebook Login for Business에 한정하고 Instagram Login 호스트 표에는 rupload를 기재하지 않는다. 기존 `practice-instagram.md`에 양 로그인 지원으로 해석한 흔적과 상충한다. **Instagram Login에 `rupload.instagram.com`을 구현하지 않는다.** Unified는 호스트 표에 rupload가 있지만 상세 로그인 구성의 지원을 후속 검증한다. 재개 전송은 `video_status.uploading_phase.bytes_transferred` 조회값부터 offset을 맞추는 공식 절차를 참고한다. 가이드 예제에 상태 문구가 일관되지 않는 부분은 실응답을 확인한다. [A142](SOURCES.md#a142). 무료 공개 URL 선택은 [실행·호스팅](execution-hosting.md)에 정리했다.

## 100건과 50건

| 공식 문서 | 직접 읽은 값 |
|---|---|
| 게시 가이드 일반 제한 | 이동 24시간 100건, 캐러셀은 1건 |
| 같은 가이드 캐러셀 제한 | 24시간 50건 |
| `content_publishing_limit` 필드 설명·JSON | `config.quota_total=50`, `quota_duration=86400` |
| 같은 레퍼런스 예제 요청 | `rate_limit_settings`를 요청하면서 응답은 `config`; 예제 내부 이름 불일치 |

[A006](SOURCES.md#a006) [A008](SOURCES.md#a008). 로그인별로 100/50을 배정할 근거는 없다. 권장: **교육 예제는 1일 1건, 방어적 작업 한도는 50건 이하로 두고 계정 조회값이 더 낮으면 그 값을 따른다.** 50건도 허용 보장은 아니다.

`GET /{ig_id}/content_publishing_limit?fields=quota_usage,config`를 문서 필드 기준으로 사용해 `quota_usage`(사용량), `config.quota_total`(총량), `quota_duration`(기간)을 기록한다. 기본 반환은 사용량뿐이므로 남은 횟수로 오독하지 않는다. 실제 응답의 필드/권한과 일반 호출 제한도 사용자가 확인한다. 실패 시 100을 임의 기본값으로 넣지 않는다.

## 표시·음악

| 기능 | 확인한 범위 |
|---|---|
| AI 공개 | `is_ai_generated=true`; 양 기존 로그인 지원. 캐러셀 **부모에만** 넣음 |
| 협찬/파트너십 | `is_paid_partnership`, `branded_content_sponsor_ids`; 현행 가이드는 Facebook Login만. 브랜드 사전승인·권한·개수 제약 확인 |
| 음악 | **Audio API 지원**: Facebook/Unified Login에서 Reels용 원본 오디오·Meta Sound Collection 음악 검색/부착. Instagram Login은 미지원. `audio_name`과 음원 선택을 구별 |

[A006](SOURCES.md#a006) [A007](SOURCES.md#a007) [A011](SOURCES.md#a011) [A125](SOURCES.md#a125). 2026-06-01 변경 이력에 Audio API 도입이 있다. `GET /ig_audio?audio_type=music&user_id=...&search_query=...`로 `audio_id`를 받고, 릴스 생성의 `audio_configuration`에 `audio_id`, `audio_volume`, `video_volume`을 넣는다. 볼륨은 문서상1~100이다. 앱 전체 인기곡 라이브러리·모든 형식의 음악 부착으로 확대하지 않는다. Audio API의 Before You Start는 연결페이지·User token을 쓰지만 소개는 Unified도 지원한다고 적어, 페이지 없는 Unified의 구체 준비 조건은 추가 확인한다. 한국 반환 카탈로그와 곡별 사용 조건은 실제 계정에서 확인한다. Instagram Login 실습은 사용권 있는 오디오를 렌더에 넣거나 앱 마무리를 선택한다.

## 오류 대응

| code / subcode | 의미 | 권장 처리 |
|---|---|---|
| `9007 / 2207027` | 미디어 처리 중 | 상태 폴링 후 FINISHED에서 발행 |
| `9004 / 2207052` | URL 파일 가져오기 실패 | 외부 GET·인증·리디렉션·MIME·만료 확인 |
| `352 / 2207026` | 영상 형식 불가 | ffprobe로 코덱·길이·파일 확인 |
| `36000 / 2207004` | 이미지 과대 | JPEG 크기 축소 |
| `36003 / 2207009` | 이미지 비율 불가 | 4:5~1.91:1로 재렌더 |
| `9 / 2207042` | 게시 한도 | limit 조회·대기, 반복 발행 안 함 |
| `4 / 2207051` | 스팸 의심 활동 제한 | 중단·계정 상태 확인 |
| `25 / 2207050` | 계정 제한/체크포인트 | 사용자가 앱에서 복구 |
| `24 / 2207008` | 컨테이너 없음/만료 | 게시 여부 확인 후 필요할 때 재생성 |

[A009](SOURCES.md#a009). 공식 오류표 자체 오기(3600/36000 등)가 있어 숫자 하나만으로 분류하지 않는다. 오류 메시지·subcode·상태를 함께 저장하되 토큰·개인 응답 전문은 제외한다. 인증 만료는 재인증/갱신 대상으로 분리하고 영구 오류를 자동 재시도하지 않는다.

## 인사이트

Instagram Login은 `instagram_business_basic`·`instagram_business_manage_insights`, Facebook 경로는 `instagram_basic`·`instagram_manage_insights`와 해당 페이지 권한을 확인한다. `/{media_id}/insights`와 `/{ig_id}/insights`를 분리한다. [A109](SOURCES.md#a109) [A110](SOURCES.md#a110)

| 범위 | 우선 수집 | 주의 |
|---|---|---|
| 게시물 | `views`, `reach`, `likes`, `comments`, `saved`, `shares`, `total_interactions` | 미디어별 지원표에서 골라 요청 |
| 릴스 | 위 지표 중 지원값, `ig_reels_avg_watch_time`, `ig_reels_video_view_total_time` | 시간 단위·재생 분모를 메타데이터에 기록 |
| 계정 | `views`, `reach`, `accounts_engaged` 등 | `metric_type=total_value`·`period`·breakdown 조합 확인 |

지표 계산 데이터는 **최대 48시간 지연**될 수 있다. 일반 User 지표 보존은 90일, `online_followers`는 최근 30일; 일부 지표는 팔로워 100명 미만에서 불가하다. 데이터 없음의 빈 배열을 0으로 바꾸지 않는다. 오래된 `impressions` 예제를 새 미디어에 복사하지 않는다. Story 지표의 조회 가능 기간도 따로 관리한다. [A085](SOURCES.md#a085) [A109](SOURCES.md#a109) [A110](SOURCES.md#a110)

한국 실계정의 지표 반환·라벨·게시 성공은 미검증이다. A4/A5/A8/A9에 반영한다.
