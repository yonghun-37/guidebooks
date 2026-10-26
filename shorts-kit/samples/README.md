# 월급날 네 칸 · 얼굴 없는 해설 샘플

가상 채널 「자취생 10분 생존법」의 대표 영상 「월급날 10분, 돈을 네 칸으로 나누기」예요. `preview.html`을 열고 처음부터 재생한 뒤 장면 버튼·반복 재생·프레임 이동으로 확인하세요. 월세·생활비·비상금·목표를 직접 그린 카드로 설명해요. **무음 예제**이며 내레이션 원고는 `script.json`에 있어요. 본인 녹음은 상위 [README](../README.md)대로 넣으세요.

- `short.mp4`: 36초·1080×1920·30fps·H.264/AAC, 화면 자막 포함.
- `script.json`: 질문형·결과 먼저·행동 제안형 훅 3안, 대본·자막·제목·설명. 아동용·AI 공개 판단은 비워 두었어요.
- `subtitles.srt`: 같은 시간·문장으로 만든 자막.
- `video-info.json`: 실제 출력 규격·장면 원본 해시·무음 상태.
- `create_scenes.py`: 같은 카드 3장을 만드는 자체 도식 원본 코드. 키트 실행 로직을 바꾸지 않아요.

네 칸은 설명용 분류, 제목의 10분은 메모에 써 볼 활동 시간이에요. 통장 개설·금액·배분 비율·절약 효과를 권하거나 보장하지 않아요. 샘플 전체는 10MB 이하이며 승인·인증·실제 계좌 정보는 없어요.

## 같은 샘플 다시 만들기

상위 README대로 가상환경과 requirements.txt 설치를 마친 뒤 **shorts-kit 폴더에서** 실행해요. 아래 `python`은 내 OS의 가상환경 Python으로 바꾸세요. 기존 결과를 덮어쓰지 않도록 새 폴더 이름을 쓰세요.

```bash
python run_pipeline.py run --output output/money-example
python samples/create_scenes.py --output input/money-scenes
```

`config.example.yaml`을 키트 루트의 `config.yaml`로 복사하고 기존 항목 중 아래 값을 바꿔요. 다른 항목은 남겨 두세요.

```yaml
video:
  scenes_dir: input/money-scenes
  narration: null
  music: null
rights:
  scenes: samples/create_scenes.py로 직접 그린 가상 네 칸 메모
```

```bash
python run_pipeline.py validate output/money-example
python run_pipeline.py render output/money-example --config config.yaml
```

`영상 생성 완료`, `검수 대기`, `미리보기`와 경로가 나오면 `output/money-example/preview.html`을 열어요. 첫 장면은 네 칸 소개, 둘째는 용도 구분, 셋째는 내 메모에 옮기는 행동이에요. 장면 길이는 각각 12초예요. 녹음이 없으므로 AAC 트랙은 무음이에요. 직접 읽은 파일을 넣을 때는 대본 길이·장면 경계를 다시 맞추세요.

공개 샘플에는 위 결과의 script.json·subtitles.srt·video-info.json·preview.html·short.mp4만 복사했어요. 장면 PNG는 이 코드로 다시 만들 수 있어요. 다른 사람이 재현하면 영상 인코더 버전에 따라 MP4 해시가 달라질 수 있어요.

글·도형·원고·샘플 코드는 자체 제작이며 [MIT](../LICENSE), 글꼴은 [OFL](../assets/fonts/OFL.txt)이에요. 타인의 영상·음악·플랫폼 화면·로고를 쓰지 않았어요. 책의 [세 영상 대본](../../site-shorts/prompts.html#three-videos)과 같은 대표 영상을 이어 만들어요.
