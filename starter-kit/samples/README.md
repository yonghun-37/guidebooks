# 실제 생성한 오프라인 샘플

모든 인물·사건·단체·링크는 **합성 데이터이며 실제 뉴스가 아닙니다.** 카드와 영상에도 이를 표시했습니다. 카드 4장 PNG(1080×1350), 릴스 MP4(1080×1920, 24fps, 20초, H.264/AAC), 자막 SRT와 사용한 문안·피드 JSON을 동봉합니다. 음성 합성은 하지 않았으며 오디오 트랙은 무음입니다.

2026-10-26에 Ubuntu 22.04 x86_64 / Python 3.11.15에서 생성했습니다. 생성 명령(저장소 루트 기준):

```bash
starter-kit/.venv/bin/python starter-kit/run_pipeline.py --offline --output starter-kit/output/2026-10-26
```

폰트 굵기·줄바꿈 조정 후 같은 결과 폴더에 최종 렌더링을 수행했습니다.

```bash
starter-kit/.venv/bin/python starter-kit/run_pipeline.py render starter-kit/output/2026-10-26
```

`output/2026-10-26/cards/*.png`, `reel.mp4`, `subtitles.srt`, `copy.json`, `news.json`을 이 폴더로 복사했습니다. 출력 폴더의 검수표·승인 기록·로컬 절대 경로는 샘플에 포함하지 않습니다. 재생성할 때는 다른 출력 폴더 이름을 써서 기존 결과를 보존하세요.

미디어·JSON·자막 합계 **500,433바이트**, 이 안내문을 포함해도 **10MB 미만**입니다. 테스트에서 폴더 전체 용량과 실제 샘플 규격을 확인합니다.

코드·합성 데이터·샘플의 이용 조건은 [MIT](../LICENSE), 폰트 소프트웨어는 [OFL](../assets/fonts/OFL.txt)입니다. 상업 콘텐츠 제작에 실제 뉴스·사진·음원을 추가하면 해당 자료의 이용 조건을 별도로 확인하세요. 이 동봉 합성 샘플은 연습용이며 live 게시 경로는 거부하도록 구현했습니다.
