# Y4k 통합 요청

담당 범위 밖의 공통 파일·서가·상태 문서·배포 설정은 수정하지 않았다. 새 키트는 `shorts-kit/`이며 인스타 키트와 독립 실행된다. 다음은 통합 작업자가 적용 여부를 판단할 제안이다.

```diff
--- a/docs/PROJECT_STATE.md
+++ b/docs/PROJECT_STATE.md
@@ ShortsBook 현재 상태
+쇼츠 키트: shorts-kit/에 독립 구현. 오프라인 대본→무음 또는 사용자 녹음·장면·음악→SRT/번인→MP4→사람 검수→기본 드라이런을 제공한다. OAuth 설정이 있는 사용자의 명시적 --live만 재개 업로드를 수행한다. 실제 계정 인증·게시와 Windows/macOS 실기기 검증은 수행하지 않았다. 검증 결과는 docs/results/phase-Y4k.md를 참고한다.
```

배포에 샘플을 포함한다면 새 샘플의 `short.mp4`, `preview.html`, `subtitles.srt`만 같은 폴더에 복사한다. 인증·세션·실제 설정·출력 폴더를 배포하지 않는다. 공통 목차나 새 실습 원고에서는 키트 README의 실제 명령을 재사용한다. 새 실습 단계는 이번 담당 범위가 아니다.

API 근거 대조: 기존 [Y037]은 privacyStatus·selfDeclaredMadeForKids·containsSyntheticMedia를 지원한다. 공식 프로토콜은 https://developers.google.com/youtube/data/guides/using_resumable_upload_protocol 을 2026-10-26에 열람했다. 청크의 256 KiB 배수·308 Range·중단 후 상태 조회는 구현 규칙이며 학습자에게 정책 합격 수치로 제시하지 않는다. research-shorts의 공동 사실표·출처 목록은 수정하지 않았다.
