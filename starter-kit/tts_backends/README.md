# 사용자 선택 TTS 플러그

기본값은 `reel.tts: silent`입니다. 실행기·모델·화자·출력물의 라이선스와 화자 동의를 사용자가 확인하고 선택한 백엔드만 연결하세요. 동봉·자동 설치하는 모델이나 TTS 서비스는 없습니다. 가장 권장하는 경로는 본인이 녹음한 내레이션 파일입니다.

키트 폴더에 본인이 작성한 `my_voice.py`를 두고 아래 함수를 구현합니다.

```python
from pathlib import Path

def synthesize(*, text: str, output_path: Path):
    # 여기서 사용자가 선택·설치한 엔진을 호출합니다.
    # text는 copy.json의 subtitle을 순서대로 이어 붙인 대본입니다.
    # output_path에 실제 WAV 파일을 저장해야 합니다. 반환 값은 쓰지 않습니다.
    raise NotImplementedError("이 부분에 본인의 백엔드를 연결하세요")
```

설정의 `reel.tts`를 `plugin`, `reel.tts_plugin`을 `my_voice:synthesize`로 지정하고 `narration`은 null로 둡니다. `make_reel.py --config config.yaml` 또는 `run_pipeline.py render 출력폴더`로 명시적으로 실행합니다. pipeline의 `--offline` 실행에서는 플러그를 차단합니다. 플러그는 Python 코드를 실행하므로 본인이 검토한 모듈만 지정하세요. 모듈 내부 API 키는 환경변수로만 읽고 코드·로그·설정에 저장하지 마세요.

WAV는 검수 대상 `audio/narration.wav`로 복사됩니다. 대본 길이를 릴스 전체 길이에 맞춰 녹음·합성하세요. 짧은 음원은 나머지를 무음으로 채우고 긴 음원은 영상 끝에서 잘라냅니다. 자동 단어 정렬·음성 인식은 제공하지 않습니다. 출력 음성과 자막의 의미·타이밍 및 AI 자기공개 필요 여부를 사람이 확인해야 합니다.
