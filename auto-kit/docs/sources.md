# 구현 근거·키트 기본값

기준: 2026-10-26. 모델·가격·API 버전은 조사 스냅샷이다. 실계정/유료 API 이용 성공 증거가 아니다.

| 구현 | 저장소 근거 |
|---|---|
| Instagram Login·장기 갱신·한도 상충 | [인증](../../research-advanced/instagram-auth.md), [게시](../../research-advanced/instagram-publishing.md), ADV-007/009/010/013/018/019 |
| YouTube 308·세션·private·publishAt·AI/아동용 | [YouTube](../../research-advanced/youtube-api.md), ADV-027/028/032/033/034 |
| 공급자 schema·모델·가격·강제 상한 | [생성 API](../../research-advanced/generation-apis.md), [비용](../../research-advanced/costs.md), providers/prices.json |
| Pages 교육용·R2 Standard 무료 범위와 초과 | [실행/호스팅](../../research-advanced/execution-hosting.md), ADV-063/064/065 |
| 승인 해시·Telegram offset·Discord 알림 | [승인/보안](../../research-advanced/approval-security.md), ADV-074/075/076 |
| 반복 콘텐츠·지표 준비 지연 | [정책](../../research-advanced/policy-safety.md), [운영](../../research-advanced/cases-operations.md), ADV-024/039/040 |

이번 구현 중 추가로 확인한 공식 자료:

- [YouTube videos.delete](https://developers.google.com/youtube/v3/docs/videos/delete): 취소는 HTTP 204이며 youtube.force-ssl 등 관리 권한 필요. upload scope만으로 대신하지 않는다.
- [YouTube channels.list](https://developers.google.com/youtube/v3/docs/channels/list): mine=true의 실제 ID를 처음·발행 직전·취소 직전에 읽어 승인한 계정과 대조한다. readonly scope를 별도 요청한다.
- [YouTube 재개 프로토콜](https://developers.google.com/youtube/v3/guides/using_resumable_upload_protocol): 308 Range 다음 위치, 동일 세션 상태 조회, 마지막 외 256KiB 배수.
- [FFmpeg loudnorm](https://ffmpeg.org/ffmpeg-filters.html#loudnorm), [ffprobe](https://ffmpeg.org/ffprobe.html): 공식 페이지 직접 열람은 시간 초과였다. 설치한 pip ffmpeg의 `-h filter=loudnorm`과 실제 렌더/측정으로 필터·출력을 검증한다. 외부 문서 확인 성공으로 기록하지 않는다.
- [n8n Execute Command](https://docs.n8n.io/integrations/builtin/core-nodes/n8n-nodes-base.executecommand/): 셀프 호스팅 전용·2.0부터 기본 비활성화·Docker 실행 위치. 실 import/실행은 사용자 확인.
- [Cloudflare R2 S3 API](https://developers.cloudflare.com/r2/api/s3/api/): 공식 표에서 PutObject의 If-None-Match와 원자적 조건부 쓰기를 확인했다. 상태 저장소 lease는 `IfNoneMatch='*'`가 실패하면 닫힌 채로 중단한다. 실계정 접근·권한은 사용자 검증 항목이다.

숫자/이름 문자열 대조, 문자 n-gram Jaccard, 원자적 예약·중복 해시·미완료 lease는 키트 구현 결정이다. 완전한 사실검증·서비스 멱등성 기능으로 소개하지 않는다. 유사도 0.82, 4-gram, 최근 30개, 음량 -19~-13 LUFS/목표 -16, 일 $1/월 $10, 2회 시도, 사후 확인 2시간, 승인 만료 24시간, 연기 60분, 최근 지표 재조회 7일, 호스팅 25MB, 상태 묶음 256MiB는 **키트 기본값(바꿀 수 있음)**이다. Instagram/Shorts 규격값은 연구 노트의 플랫폼 요건과 구분한다.

## 복사·수정한 코드

- `rendering/cards.py`: starter-kit/render_cards.py의 글자 줄바꿈·도형·PNG/JPEG 템플릿. 최상위 CLI/문안 validator를 공통 스키마로 교체.
- `rendering/short_base.py`: shorts-kit/render.py의 사진/클립·Pillow 자막·ffmpeg·SRT 조립. 공통 스키마로 연결하고 variable font가 아닌 경우 처리.
- `publish/youtube_protocol.py`: shorts-kit/upload.py의 private_json/valid_session/resumable. 세션 시작 전에 결과 불명 표식을 추가.
- `common.save_json`, `oauth_setup.py`, `schedule/install.py`, `hosting/`, `ops/tokens.py`: 두 키트의 비공개 파일/권한·절대경로·허용파일·로그 가림 패턴을 재사용·확장.
- 라이선스: [MIT](../LICENSE). 폰트 Noto Sans KR는 [OFL](../assets/fonts/OFL.txt). FFmpeg 실행 파일은 pip 설치물이며 이 저장소에는 재배포하지 않는다.
