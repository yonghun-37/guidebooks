# 내 쇼츠 한 편 만들기

**설치 후 인터넷 없이 대본부터 완성 MP4까지 만들 수 있어요.** 본인 녹음·사진·클립을 넣어 보세요. 준비된 파일이 없으면 자체 타이틀 장면과 무음·자막으로 끝까지 연습해요. 계정이나 API 키는 필요 없어요.

도윤: “녹음이 아직 없는데 시작해도 되나요?”  
서진: “무음으로 먼저 한 편을 만들어요. 첫 화면을 멈춰 보고 자막이 읽히는지 확인하세요.”

이 실습이 끝나면 `short.mp4`, `subtitles.srt`, `preview.html`, `REVIEW.md`가 남아요. 정책은 **2026년 10월 조사 기준**이에요. 등장인물·채널 「자취생 10분 생존법」과 월급날 메모 사례는 가상이에요.

## 준비하고 첫 영상 만들기

터미널은 명령을 글로 입력하는 창이에요. Python을 설치하고, 압축을 푼 `shorts-kit` 폴더에서 터미널을 여세요. Python 설치 때 Windows의 PATH 추가 항목을 선택하세요. 경로는 파일이 있는 위치예요. 공백이 있으면 따옴표로 감싸요.

Windows에서는 탐색기에서 이 폴더를 열고 주소창에 `powershell`을 입력해요. 아래처럼 가상환경을 만들어요. 가상환경은 이 키트의 도구만 따로 설치하는 폴더예요. 활성화 대신 실행 파일을 직접 부르면 실행 정책을 바꿀 필요가 없어요.

```powershell
py -3 -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe run_pipeline.py run --output output/first
```

macOS에서는 터미널에서 `cd `를 입력한 뒤 Finder의 `shorts-kit` 폴더를 끌어 놓고 Enter를 눌러요.

```bash
python3 -m venv .venv
.venv/bin/python -m pip install -r requirements.txt
.venv/bin/python run_pipeline.py run --output output/first
```

**이렇게 보이면 성공:** 마지막에 `영상 생성 완료`, `검수 대기`, `미리보기`와 각 파일 경로가 나와요. `output/first/preview.html`을 브라우저에서 열어 재생하세요. 파일은 영상 출력 전 원본을 따로 보관해요.

이후 명령의 `python`은 Windows의 `.\.venv\Scripts\python.exe`, macOS의 `.venv/bin/python`으로 바꾸어 실행하세요. 설치에는 인터넷이 필요해요. 영상 생성에는 시스템 ffmpeg를 설치하지 않아요. `imageio-ffmpeg`가 제공하는 pip 바이너리를 써요.

| 남는 파일 | 무엇을 확인하나요? |
|---|---|
| `script.json` | 읽을 말·짧은 자막·장면 길이·제목·설명·해시태그 |
| `config.yaml` | 이번 결과 폴더의 녹음·장면·자막 설정 |
| `short.mp4` | 자막이 화면에 구워진 완성 영상 |
| `subtitles.srt` | 시간과 글자가 적힌 별도 자막 파일 |
| `video-info.json` | 실제 출력 규격·장면 시간·원본 해시·음성 상태 |
| `preview.html` | 장면 선택·반복 재생·프레임 이동·안전 영역·소리 따로 듣기 |
| `REVIEW.md` | 사람이 직접 확인할 체크 목록 |

JSON은 이름과 값의 쌍으로 적는 텍스트 파일이에요. `true`는 예, `false`는 아니요, `null`은 아직 정하지 않았다는 뜻이에요. `.json`·`.yaml`은 메모장이나 텍스트 편집기로 수정해요. 큰따옴표·쉼표를 유지하고 UTF-8로 저장하세요. macOS 텍스트 편집기는 일반 텍스트 모드로 바꾸세요.

## 대표 샘플의 장면까지 다시 만들기

기본 실행은 같은 월급날 대본에 단순 타이틀을 붙여요. 책에 실린 네 칸 메모 장면까지 재현하려면 [샘플 재현 절차](samples/README.md)를 따라 `samples/create_scenes.py`로 자체 도식을 만든 뒤 기존 `render`를 실행하세요. 공개 샘플은 무음이며 실제 계좌·금액·배분 비율을 넣지 않았어요.

## 내 대본으로 바꾸기

**첫 영상은 짧게 읽어 보고 길이를 정하세요.** 이 키트의 기본 길이는 36초이며 첫 과제의 30~60초 안에 있어요. 이 길이와 아래 자막값은 책의 연습용 선택이에요. 쇼츠의 분류 조건은 최대 3분, 정사각형 또는 세로예요. [Y001]

오프라인 모드는 동봉된 가상 월급날 네 칸 해설 대본을 만들어요. `script.json`의 `hooks`에는 질문형·결과 먼저·행동 제안형 첫 문장 세 가지가 들어 있어요. 하나를 골라 첫 장면의 `title`·`narration`·`subtitle`에 직접 옮겨요. `hooks`를 바꾸는 것만으로 영상의 말과 글이 바뀌지는 않아요.

웹 채팅을 쓰려면 아래 명령으로 별도 폴더를 만들어요.

```bash
python run_pipeline.py run --mode prompt --output output/my-script
```

1. 생성된 `prompt.md`를 열어 내 주제를 넣고 웹 채팅에 붙여 넣으세요. 훅·대본·제목/설명/해시태그 템플릿이 함께 들어 있어요.
2. 답변의 JSON만 `output/my-script/script.json`에 저장해요. 파일명 뒤에 `.txt`가 붙지 않게 해요.
3. `narration`은 읽을 말, `subtitle`은 화면에 읽힐 짧은 글로 고쳐요. 출처가 필요한 사실은 원문과 대조하세요.
4. `duration`은 각 장면의 초예요. 정수 초로 맞추고 합이 녹음 길이 이상인지 확인하세요.
5. 아래 명령으로 형식 검사와 출력을 해요.

```bash
python run_pipeline.py validate output/my-script
python run_pipeline.py render output/my-script
```

**이렇게 보이면 성공:** `대본 형식 확인 완료` 뒤 새 MP4·미리보기가 생겨요. 문장과 장면 순서는 `scenes` 배열의 순서대로 나와요. 형식 검사는 사실 여부를 판정하지 않아요.

선택한 기존 API가 있을 때만 `--mode api --allow-api`를 써요. `LLM_BASE_URL`(HTTPS의 `/v1` 주소), `LLM_API_KEY`, `LLM_MODEL`을 본인 터미널 환경변수로 준비하세요. 키를 대본·설정 파일에 적지 마세요. API 모드는 네트워크와 제공자 이용 조건을 따르므로 무료 오프라인 실습에는 필요 없어요. 이 키트는 유료 계정을 만들거나 키를 발급하지 않아요.

## 녹음·장면·자막·음악 넣기

**내 녹음 파일이 있으면 그 파일을 먼저 써요.** 녹음이 없으면 무음 AAC 트랙을 넣고 자막으로 전달해요. TTS나 음원 다운로드를 자동 실행하지 않아요.

먼저 키트의 `config.example.yaml`을 `config.yaml`로 복사해요. `input/` 폴더를 만들고 파일을 넣어요. 다음은 연습용 설정 예예요. 사진·클립은 장면 수와 같은 개수로 준비해요.

```yaml
video:
  narration: input/voice.m4a
  scenes_dir: input/scenes
  music: null
```

위 세 줄만 새 파일로 만들지 말고, 복사한 설정의 같은 항목을 바꾸세요. `rights.narration`에는 본인 녹음 또는 화자 동의, `rights.scenes`에는 파일별 출처·사용 조건·증빙 위치를 적어요. 장면 폴더에 `01.mp4`, `02.jpg`, `03.png`처럼 넣으면 파일명 순서로 사용해요.

- 녹음: WAV·MP3·M4A·AAC·FLAC·OGG를 받아요. 영상보다 긴 녹음은 오류로 멈춰요. `script.json`의 장면 길이를 늘려 말이 잘리지 않게 하세요.
- 장면: MP4·MOV·MKV·WEBM 클립, JPG·PNG·WEBP 사진을 받아요. 세로 화면을 채우도록 가운데를 잘라요. 짧은 클립은 해당 장면 끝까지 반복돼요. 소리는 녹음·음악 파일만 사용해요. 원본 클립의 소리는 넣지 않아요.
- 자막: 대본에서 SRT와 번인 자막을 자동 생성해요. 음성 인식은 하지 않아요. 긴 글은 화면 너비에 맞춰 나누고 장면 시간에 배분해요. 실제 말과 맞지 않으면 장면을 더 나누고 길이를 고치세요. `video.duration`은 새 대본의 시작 길이이고, 재출력 길이는 `scenes`의 `duration` 합이에요.
- 크기·위치: `caption_size` 기본 56px, 여백은 왼쪽 90·오른쪽 180·위 240·아래 420px이에요. 이 키트의 시작값이에요. 공식 고정값이 아니에요. 실제 플레이어에서 버튼·제목과 겹치는지 확인하세요. [Y080]

새 설정으로 출력할 때는 다음처럼 실행해요. `--config`를 생략하면 결과 폴더 안의 `config.yaml`을 써요. SRT만 고쳐도 영상의 번인 자막은 바뀌지 않아요. `script.json`의 `subtitle`을 고치고 다시 출력하세요.

```bash
python run_pipeline.py render output/first --config config.yaml
```

**배경음은 사용권을 확인한 내 파일만 넣어요.** Creative Commons 트랙은 필요한 저작자 표시를 설명란에 넣어요. [Y016] 설정의 `rights.music`에 아래 값을 적으세요.

```yaml
music:
  confirmed: true
  source: '원작자와 원문 주소'
  license: '사용 가능한 범위와 조건'
  evidence: input/music-license.txt
  attribution: '필요한 표시문구'
```

이 블록은 `rights` 아래 기존 `music`을 바꾸는 예예요. 별도로 `video.music`에 음원 경로를 넣고, `evidence` 파일에 사용권 증거를 보관해요. 표시가 필요하면 같은 문구를 `script.json`의 `description`에도 넣으세요. 필요 없는 표시문구는 빈 문자열로 두어요. `confirmed: true`는 사용자의 확인 기록이에요. 키트가 법적 허가를 판정하지 않아요.

미리보기에서 녹음과 음악을 따로 들은 뒤 완성 영상을 들어요. 음악이 말을 덮으면 `music_gain`을 낮추고 다시 출력하세요. 기본 0.12는 음량을 곱하는 연습값이에요. 짧은 음악 뒤에는 무음이 이어져요. 자막의 안전 영역은 미리보기 체크로 보고, 장면 버튼·이전/다음 프레임·반복 재생으로 말과 글이 함께 끝나는지 확인하세요.

## 출력 확인하고 승인하기

**완성 파일을 끝까지 본 다음 승인하세요.** 키트는 9:16·1080×1920·30fps·H.264/AAC MP4를 만들어요. 이는 이 키트의 출력 선택이에요. MP4·H.264는 공식 인코딩 안내에도 있어요. [Y003] 길이는 최대 3분을 검사해요. [Y001]

1. `preview.html`에서 첫 화면·각 장면·마지막 화면을 보세요. 자막 크기·크롭·소리·사실·권리를 확인해요.
2. `script.json`의 `privacyStatus`를 확인해요. 기본 `private`는 비공개예요. `unlisted`는 주소를 아는 사람이 볼 수 있고 `public`은 공개예요. [Y032]
3. `selfDeclaredMadeForKids`를 아동용이면 `true`, 아니면 `false`로 정해요. 의도한 시청자·주제·표현을 함께 보고 판단하세요. 가족이 볼 수 있다는 이유만으로 아동용은 아니에요. [Y014]
4. `containsSyntheticMedia`는 사실적 합성 등 공개 대상이면 `true`로 정해요. 대본·자막 보조만 쓴 예는 공개 예외에 들어가요. 사용한 영상·소리 전체를 보고 결정하세요. [Y013] API가 받는 실제 필드는 이 두 불리언과 `privacyStatus`예요. `isShorts`는 보내지 않아요. [Y037]
5. 값을 고쳤으면 다시 출력해 검수 목록을 새로 만들어요.

```bash
python run_pipeline.py render output/first
```

새 `REVIEW.md`의 여섯 칸을 직접 확인하고 `[ ]`를 `[x]`로 바꾸어 저장하세요. 아직 모르는 항목이 있으면 먼저 해결해요. 그다음 승인해요.

```bash
python run_pipeline.py approve output/first
python upload.py output/first
```

**이렇게 보이면 성공:** `APPROVED.json`과 `dry-run.json`이 생겨요. 드라이런은 요청 내용을 미리 보여 주는 예행연습이에요. `network_calls: 0`이고 실제 전송하지 않아요. POST로 세션 시작 → PUT으로 청크 전송 → 중단 시 같은 세션의 서버 위치 조회 순서를 읽어 보세요. 승인 뒤 대본·영상·설정·자막·검수 문서가 바뀌면 다시 검수해야 해요.

오늘 실제 게시하려면 완성 MP4를 공식 Studio/앱에 직접 올리고 공개 상태·Shorts 분류·제한사항·주소를 확인하세요. [업로드 실습](../site-shorts/practice/08-publish.html)을 따라 하세요. API는 아래 선택 경로예요.

## 선택: 내 계정에서 API 업로드

**사용자 인증 파일과 토큰이 모두 있어야 `--live`가 동작해요.** 토큰은 허용한 권한을 증명하는 개인 파일이에요. API 키만으로 사용자 채널에 업로드하지 않아요. [Y037]

1. Google Cloud 콘솔에서 프로젝트를 선택하거나 만들고 **API 및 서비스 → 라이브러리 → YouTube Data API v3 → 사용**으로 가요. [Y037]
2. Google Auth Platform의 **Branding·Audience·Data Access**를 설정해요. 외부 테스트 앱은 **Audience → Test users → Add users → Save**에 본인 계정을 넣어요. Internal은 조직 내부용이에요. [Y041] [Y099]
3. 사용자 인증 정보에서 **OAuth 클라이언트 ID → 데스크톱 앱**을 만들고 JSON을 받아 키트의 `private/client_secret.json`으로 저장해요. [Y101]
4. 아래 명령을 직접 실행하면 본인 브라우저에서 로그인·채널·권한을 확인해 토큰을 저장해요. 이 명령은 영상을 업로드하지 않아요.

```bash
python -m pip install -r requirements-live.txt
python oauth_setup.py
```

5. 사용할 채널이 맞는지 확인한 뒤, 위 검수·승인을 마친 폴더만 전송해요.

```bash
python upload.py output/first --live
```

**이렇게 보이면 성공:** 완료 응답의 `id`·주소와 `upload-result.json`이 남아요. 요청한 공개 상태와 응답의 `status`를 대조하세요. Studio에서 실제 공개 상태·처리·Shorts 구분·제한사항을 다시 확인하세요. API 전송 완료만으로 공개 완료를 판단하지 마세요. [Y032]

연결이 끊기면 같은 명령을 다시 실행하세요. 개인 `upload-session.json`에 저장한 세션으로 서버가 받은 위치를 조회하고 남은 부분만 보내요. 완료 기록이 있으면 새 업로드를 시작하지 않아요. 세션이 만료되면 Studio에서 이미 생성된 영상이 있는지 확인한 뒤 새 폴더에서 시작하세요. 전송 기록이 있는 폴더는 재렌더하지 않아요.

> **확인할 점**  
> 현재 업로드는 별도 버킷에서 호출당 1 unit, 기본 하루 100호출이에요. 실제 프로젝트의 Cloud 할당량 화면을 확인하세요. [Y037] [Y038] [Y088] 공식 insert 문서는 미검증 프로젝트의 비공개 제한이 없다고 하지만 한국어 잠금 도움말은 제한을 설명해요. 먼저 비공개로 보내고 Studio에서 실제 잠금을 확인하세요. 잠긴 영상은 단순 공개 전환으로 해결되지 않으며 공식 경로 재업로드 또는 API 감사를 안내해요. API 감사·할당량 증설과 OAuth 앱 검증은 다른 절차예요. [Y037] [Y086] [Y040] [Y041] 외부 Testing 앱의 refresh token은 보통 7일에 만료돼요. 만료되면 기존 토큰을 안전한 곳으로 옮긴 뒤 본인 테스트 계정으로 재인증하세요. [Y042]

인증 파일·토큰·세션 주소를 공유하지 마세요. [Y102] 키트의 `.gitignore`는 `private/`, `input/`, `output/`, 실제 설정과 토큰을 제외해요. 다른 위치의 파일은 따로 보호해야 해요. 결과 폴더에는 원본 경로·권리 메모가 있어요. 공개 샘플만 공유하세요.

## 매일은 초안 생성까지만 예약해요

**매일 영상 초안을 만들고 사람 검수에서 멈춰요.** 기존 날짜 폴더는 덮어쓰지 않아요. 설정이 API 모드여도 날짜별 생성은 오프라인이에요.

```bash
python daily.py --date 2026-10-26 --output-root output/daily
python schedule_setup.py --os windows --time 09:30
python schedule_setup.py --os macos --time 09:30
```

예약 안내에는 등록·확인·수동 실행·삭제 명령이 나와요. 직접 내용을 확인한 뒤 등록하세요. 컴퓨터가 켜진 현지 시각에 실행돼요. 예약은 업로드나 승인을 실행하지 않아요. 실제 녹음·장면을 바꾸고 검수하는 단계는 남아요.

## 자주 묻는 질문: 반복 제작

1. **두 번째 영상부터 무엇을 저장하나요?** `config.yaml`과 대본의 장면 틀을 저장해요. 예를 들어 도윤은 월급날 해설 구조만 남기고 다음 영상의 행동·녹음·장면을 바꿔요. 새 `--output` 폴더로 만드세요.
2. **비슷한 영상을 많이 만들면 수익화가 막히나요?** 최소 수정한 대량생산과 의미 있는 변형이 부족한 재사용은 수익화 심사에서 문제가 될 수 있어요. [Y011] [Y012] 예제 타이틀만 반복 게시하지 말고 내 설명·촬영·편집을 더하세요.
3. **사람이 꼭 확인할 것은 무엇인가요?** 사실·자막·소리·권리·공개 설정을 확인해요. 예를 들어 무음인지 음성 누락인지 직접 구분하세요. `REVIEW.md`를 끝까지 체크해요.
4. **음성과 자막이 빠지면 어디서 찾나요?** 터미널 오류와 `video-info.json`의 `audio`·`warnings`를 보세요. `silent`는 녹음 미지정 상태예요. 파일 경로를 고치고 다시 출력해요. 자막 시점은 `script.json`을 고쳐요.
5. **매일 올리려면 API부터 배워야 하나요?** 완성 MP4를 공식 Studio/앱으로 올리면 돼요. [Y031] 먼저 새 영상 한 편과 공개 주소를 남기세요. API는 반복 제작이 익숙해진 뒤 선택해요.

## 자주 묻는 질문: API 준비

1. **프로젝트와 API는 어디서 켜나요?** Cloud 콘솔의 프로젝트와 API 라이브러리에서 켜요. 예를 들어 내 연습 프로젝트를 선택하고 YouTube Data API v3의 사용 상태를 확인하세요. [Y037]
2. **동의 화면·테스트 사용자는 어디서 설정하나요?** Google Auth Platform의 Branding·Audience·Data Access에서 설정해요. Audience의 Test users에 본인 계정을 넣고 저장하세요. [Y041]
3. **인증 파일을 저장소에 안 올리려면요?** `private/`에 보관하고 Git 제외 상태를 확인하세요. 토큰은 비밀번호처럼 다뤄요. 예를 들어 받은 JSON을 공개 샘플 폴더에 두지 마세요. [Y102]
4. **업로드 비용과 기본량은요?** 현재 별도 업로드 버킷에서 호출당 1 unit·기본 하루 100호출이에요. 내 프로젝트의 Cloud 할당량 화면을 확인하세요. [Y037] [Y038] [Y088]
5. **비공개 잠금과 감사는요?** 잠금은 업로드한 영상의 제한이고, API 감사는 서비스의 정책 준수를 확인하는 절차예요. OAuth 동의 화면 검증과도 구분해요. 비공개 시험 뒤 Studio 상태를 확인하고, 잠겨 있으면 공식 잠금 도움말의 재업로드·감사 안내를 따르세요. [Y086] [Y040] [Y041]

## 이렇게 보이면?

| 증상 | 지금 할 일 |
|---|---|
| 이미 있는 폴더 | 다른 이름의 `--output`을 쓰거나 기존 폴더를 `render`해요. |
| 글자가 잘림·너무 빠름 | 자막을 줄이거나 장면을 더 나누고 `duration`을 늘려요. |
| 말과 자막이 어긋남 | 음성 인식 기능이 아니에요. 실제 녹음 구간에 맞춰 장면 길이·자막을 수정해요. |
| 화면 가장자리가 잘림 | 가운데 크롭이므로 주제를 중앙에 두거나 세로 촬영 파일을 쓰세요. |
| `null`이라 승인 실패 | 두 공개 판단을 직접 정하고 render·검수·approve를 다시 해요. |
| 음악 확인 오류 | 사용 조건·증빙 파일·필요한 설명 표시문구를 채워요. |
| MP4 생성 실패 | 파일 손상·지원 형식·음성 트랙·저장 공간을 확인해요. 경로에 URL을 넣지 마세요. |
| 로컬 미리보기 재생 안 됨 | `short.mp4`를 다른 플레이어에서 열거나 `python -m http.server 8765` 실행 후 `http://127.0.0.1:8765/output/first/preview.html`을 열어요. 장면 탐색이 안 되면 HTML을 직접 열거나 별도 플레이어를 써요. |

개발 검증: `python -m pip install -r requirements-dev.txt` → `python -m pytest`예요. [샘플](samples/README.md)은 직접 만든 작은 무음 예제예요. 코드·자체 생성 샘플은 [MIT](LICENSE), 글꼴은 [OFL](assets/fonts/OFL.txt)을 따라요.

## 출처

정책·수치의 전체 근거와 판정은 [사실표](../research-shorts/FACT-SHEET.md), [출처 목록](../research-shorts/SOURCES.md), [API 조사](../research-shorts/13-api-quota-audit.md)에 있어요. 출력·자막·음량의 키트 시작값은 플랫폼 의무와 구분해요.

[Y001]: https://support.google.com/youtube/answer/15424877?hl=ko
[Y003]: https://support.google.com/youtube/answer/1722171?hl=ko
[Y011]: https://support.google.com/youtube/answer/1311392?hl=ko
[Y012]: https://support.google.com/youtube/answer/2801973?hl=ko
[Y013]: https://support.google.com/youtube/answer/14328491?hl=ko
[Y014]: https://support.google.com/youtube/answer/9528076?hl=ko
[Y016]: https://support.google.com/youtube/answer/3376882?hl=ko
[Y031]: https://support.google.com/youtube/answer/12779649?hl=ko
[Y032]: https://support.google.com/youtube/answer/57407?hl=ko
[Y037]: https://developers.google.com/youtube/data/reference/rest/v3/videos/insert
[Y038]: https://developers.google.com/youtube/data/getting-started
[Y040]: https://developers.google.com/youtube/data/guides/quota_and_compliance_audits
[Y041]: https://developers.google.com/workspace/guides/configure-oauth-consent
[Y042]: https://developers.google.com/identity/protocols/oauth2#expiration
[Y080]: https://support.google.com/youtube/answer/16215842?hl=en
[Y086]: https://support.google.com/youtube/answer/7300965?hl=ko
[Y088]: https://developers.google.com/youtube/data/determine_quota_cost
[Y099]: https://developers.google.com/identity/protocols/oauth2/production-readiness/overview
[Y101]: https://developers.google.com/identity/protocols/oauth2/native-app
[Y102]: https://developers.google.com/identity/protocols/oauth2/resources/best-practices
