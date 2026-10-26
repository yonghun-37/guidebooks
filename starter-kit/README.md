# 하린의 첫 카드와 릴스 만들기

Python으로 **합성 RSS → 문안 초안 → 카드 5장 → 20초 릴스 → 사람 검수 → 게시 요청 미리보기**를 만듭니다. 코딩 경험·계정·API 키가 없어도 됩니다. 계정은 “출근길 3분 생활 뉴스”, 동봉 콘텐츠는 “청년 지원금, 신청 전 확인할 3가지”입니다. 대상·기간·서류를 점검하는 직접 작성 예시 문안이며 실제 제도명·혜택·금액을 안내하지 않습니다. 결과물 예시는 [samples](samples/)에서 먼저 볼 수 있습니다.

설치할 때만 인터넷이 필요합니다. 설치가 끝나면 기본 실습은 인터넷 없이 작동합니다. 기본 음성은 **무음 + 영상에 새긴 한국어 자막**입니다. 직접 녹음·사용자 음악·TTS 플러그·LLM 연결은 아래에서 선택할 때만 켭니다. 음성 합성·LLM·이미지 생성 서비스를 호출하지 않습니다.

## 1. 터미널과 Python 준비

터미널은 명령을 글자로 입력하는 창입니다. 코드 블록에서 명령만 복사하고 Enter를 누르세요. `$`, `>` 같은 기호는 붙이지 않습니다. 설치가 끝날 때까지 창을 닫지 마세요.

| 운영체제 | 터미널 여는 법 | Python 확인 |
|---|---|---|
| Windows | 시작 메뉴 → **PowerShell** 검색 → 실행 | `py -3.11 --version` |
| macOS | Spotlight(⌘+Space) → **터미널** 검색 → 실행 | `python3 --version` |
| Linux | 앱 메뉴의 **터미널** 또는 Ctrl+Alt+T | `python3 --version` |

**Python 3.11 이상**이 필요합니다. 없거나 낮은 버전이면 [Python 공식 다운로드](https://www.python.org/downloads/)에서 설치하세요. Windows 설치 화면에서는 **Add python.exe to PATH** 항목이 있으면 선택하세요. 설치 확인 명령에서 Microsoft Store만 열린다면 실행 별칭/설치 경로를 확인하고 `py -3.11 --version`으로 다시 확인하세요. Linux는 배포판의 Python/venv 설치 안내를 따르세요. 이 키트는 시스템 패키지를 자동 설치하지 않습니다. Windows에서 3.12 이상을 설치했다면 아래 `py -3.11`을 해당 버전(예: `py -3.12`)으로 바꾸세요.

[저장소](https://github.com/yonghun-37/guidebooks)의 **Code → Download ZIP**으로 받아 압축을 푸세요. 탐색기/Finder에서 `starter-kit` 폴더 위치를 확인합니다. 터미널에서 `cd `를 입력한 뒤 그 폴더의 전체 경로를 따옴표로 감싸 붙여넣으세요. 예:

```text
cd "C:\Users\내이름\Downloads\guidebooks-main\starter-kit"
```

macOS/Linux의 경로는 보통 `"/Users/내이름/Downloads/guidebooks-main/starter-kit"` 또는 `"/home/내이름/Downloads/guidebooks-main/starter-kit"` 형태입니다. 실제 압축을 푼 위치로 바꾸세요. `dir`(Windows) 또는 `ls`(macOS/Linux)를 입력했을 때 `run_pipeline.py`가 보이면 맞게 이동했습니다.

## 2. 설치: pip 권장

가상환경(`.venv`)은 이 폴더에만 프로그램을 설치하는 상자입니다. 운영체제에 맞는 명령을 **한 줄씩** 실행하세요.

Windows **PowerShell**(활성화 정책을 바꾸지 않는 경로):

```powershell
py -3.11 -m venv .venv
.venv\Scripts\python.exe -m pip install --cache-dir .cache/pip -r requirements.txt
```

Windows에서는 아래 모든 `python`을 `.venv\Scripts\python.exe`로 바꿔 실행하세요. 명령 프롬프트(cmd)를 사용한다면 `.venv\Scripts\activate.bat`로 활성화한 뒤 `python`을 쓸 수도 있습니다.

macOS / Linux:

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --cache-dir .cache/pip -r requirements.txt
```

macOS/Linux에서 창 왼쪽에 `(.venv)`가 보이면 활성화됐습니다. `python --version`으로 다시 3.11 이상인지 확인하세요. 새 터미널을 열 때는 폴더 이동과 활성화 명령을 다시 실행합니다. PowerShell 사용자는 활성화 대신 `.venv\Scripts\python.exe`를 아래 모든 `python` 자리에 써도 됩니다.

**uv를 쓰는 대체 경로:** 위에서 가상환경 생성·활성화까지만 실행하고, 마지막 설치 명령 대신 아래를 실행하세요. uv도 가상환경 안에 설치합니다. pip 경로와 둘 다 할 필요는 없습니다.

```bash
python -m pip install --cache-dir .cache/pip uv
uv pip install --cache-dir .cache/uv --python .venv -r requirements.txt
```

FFmpeg를 따로 설치할 필요는 없습니다. 시스템 FFmpeg가 있으면 쓰고, 없으면 설치된 `imageio-ffmpeg`의 바이너리를 사용합니다. 지원하는 바이너리가 없는 운영체제/CPU에서는 설치·실행이 실패할 수 있습니다. 테스트한 환경은 아래 검증 절을 보세요.

## 3. 첫 실행: 계정이나 키를 넣지 마세요

```bash
python run_pipeline.py --offline
```

성공하면 `검수 대기: .../output/날짜/REVIEW.md`가 나옵니다. 예를 들어 2026년 10월 26일 실행 결과는 `output/2026-10-26/`입니다. 명령을 실행한 컴퓨터의 날짜를 씁니다. **여기서 정상 종료합니다. 승인하기 전에는 게시 요청도 만들지 않습니다.**

같은 날 다시 실행할 때는 기존 결과를 덮어쓰지 않습니다. 다른 이름을 지정하세요.

```bash
python run_pipeline.py --offline --output output/second-practice
```

| 생성 파일 | 확인하는 법 |
|---|---|
| `news.json` | 메모장/텍스트 편집기로 제목·링크·짧은 요약 확인 |
| `copy.json` | 카드 제목·본문·릴스 자막·캡션·AI 표시 선택값 확인 |
| `cards/card-01.png` ~ `card-05.png` | 더블 클릭해 카드 1080×1350과 한글 확인 |
| `cards/*.jpg` | PNG와 같은 카드의 API 게시용 JPEG |
| `reel.mp4` | 더블 클릭해 세로 1080×1920, 20초, 자막과 무음 확인 |
| `subtitles.srt` | 영상 자막의 시간표. MP4에는 자막이 이미 새겨져 있음 |
| `frames/`, `frames.txt` | 장면 배경·자막 PNG, 장면 MP4와 연결 순서표 |
| `REVIEW.md` | 게시 전 검수표. 텍스트 편집기로 열기 |
| `config.json`, `reel-info.json`, `manifest.json` | 사용 설정·제작 정보·변경 감지 해시 |

샘플 카드에는 **합성 데이터 · 예시 문안 · 실제 제도 아님** 표시가 있습니다. 실제 기사·사진·음원은 동봉하지 않았습니다. 합성 피드를 실제 소식처럼 게시하지 마세요. 실습 기본 크기와 15~30초 길이는 [DESIGN.md](../docs/DESIGN.md)의 학습 목표입니다.

## 실습편 2~6에서 같은 폴더 이어 쓰기

사이트 실습편은 날짜 대신 고정 이름 `output/first-post`를 사용합니다. 첫 실행은 다음 한 번이며, 이미 있다면 새 이름을 정하고 뒤 명령의 경로도 함께 바꾸세요. Windows PowerShell은 아래 모든 `python`을 `.venv\Scripts\python.exe`로 바꿉니다.

```bash
python run_pipeline.py --offline --output output/first-post
python write_copy.py output/first-post/news.json --mode prompt --template cards --output output/first-post/copy.json
```

`prompt.md`를 웹 채팅에 직접 붙여 넣거나 기존 `copy.json`을 직접 편집합니다. 채팅은 현재 JSON도 함께 제공하고 답변 전체 JSON만 저장합니다. 이후 구조 검증 → 카드·릴스 재생성 순서입니다.

```bash
python write_copy.py output/first-post/news.json --validate --output output/first-post/copy.json
python run_pipeline.py render output/first-post
```

성공 출력은 각각 `구조 검증 OK: output/first-post/copy.json (사실 확인은 사람이 해야 합니다)`와 `검수 대기: …/output/first-post/REVIEW.md`입니다. 카드는 5장 PNG/JPEG, 기본 릴스는 20초·무음·자막입니다. 선택 녹음은 현재 출력 폴더 `config.json`의 reel.narration에 본인 mp3/wav 경로를 입력하고 다시 render합니다.

모든 파일과 REVIEW.md의 여섯 항목을 **사람이 확인·저장한 다음에만** 아래를 실행합니다.

```bash
python run_pipeline.py approve output/first-post
python publish.py output/first-post
```

두 명령은 `"mode": "dry-run"`을 출력하며 실제 게시하지 않습니다. `APPROVED.json`과 `dry-run.json`이 생깁니다. 합성 연습 다음에 본인 자료로 바꿀 때는 이용 조건을 확인한 로컬 RSS를 `my-feed.xml`로 준비하고 `python run_pipeline.py --offline --feed my-feed.xml --output output/my-news`로 새 실행을 만듭니다. 사이트 실습 3의 XML 입력 예시를 따르고 이후 모든 경로를 `output/my-news`로 바꿉니다. 합성 파일의 synthetic 값만 바꿔 실제 자료라고 표시하지 마세요.

## 4. 사람이 확인하고 approve 실행

`REVIEW.md`에 있는 여섯 항목을 확인합니다. 모든 PNG/JPEG와 릴스를 직접 열어 보고, 완료한 항목을 `- [ ]`에서 `- [x]`로 고쳐 저장하세요. 다음 명령의 폴더를 **본인의 출력 폴더**로 바꿉니다.

```bash
python run_pipeline.py approve output/2026-10-26
```

`APPROVED.json`에 승인 시점과 파일 해시를 저장하고, **캐러셀과 릴스의 드라이런**을 출력합니다. `dry-run.json`에도 같은 내용을 보관합니다. 각 미디어의 **컨테이너 생성 → FINISHED 상태 확인 → 게시** 순서와 엔드포인트·파라미터를 보여 줍니다. 캐러셀은 자식 JPEG들의 생성·확인을 먼저 보여 줍니다. `v26.0`(기본 설정값), `<IG_USER_ID>`, `{CHILD_1}` 등은 예시 자리표시자입니다. 토큰은 출력하지 않습니다.

승인 후 드라이런만 다시 보고 싶으면:

```bash
python publish.py output/2026-10-26
```

문안을 바꾸려면 `copy.json`의 `title`, `body`, `subtitle`, `caption`, `is_ai_generated`를 편집하세요. JSON은 큰따옴표·쉼표를 유지해야 합니다. `REVIEW.md`의 캡션만 편집해도 실제 문안은 바뀌지 않습니다. 아래로 이미지와 영상을 다시 만든 후 **새 검수표를 다시 확인·저장·승인**하세요.

```bash
python run_pipeline.py render output/2026-10-26
python run_pipeline.py approve output/2026-10-26
```

재생성은 기존 승인을 지웁니다. 승인 뒤 문안·카드·영상·검수표가 달라져도 게시를 차단합니다. 이 기록은 로컬 실습의 변경 감지이며 사용자 인증 시스템은 아닙니다.

## 5. 계정 이름·색과 소재 바꾸기

`config.example.yaml`을 같은 폴더에 `config.yaml`로 복사해 계정 이름과 `theme`을 바꾸세요. 프리셋은 `forest`(크림·초록), `ink`(남색·블루), `coral`(크림·코랄)입니다. `colors: {accent: '#007F73'}`처럼 색 일부를 덮어쓸 수도 있습니다. 폰트·피드·사용자 이미지·음원의 상대 경로는 설정 파일 위치 기준입니다. 기본은 `llm.mode: offline`, `reel.tts: silent`입니다.

```bash
python run_pipeline.py --offline --config config.yaml --output output/my-style
```

다른 **로컬 RSS 2.0 파일**을 넣어도 됩니다. Atom은 지원하지 않습니다. 최대 3개 항목의 제목·링크·요약만 가져오며 기사 본문은 다운로드하지 않습니다.

```bash
python run_pipeline.py --offline --feed fixtures/sample-feed.xml --output output/local-feed
```

실제 RSS는 해당 제공자의 이용 조건을 먼저 확인한 뒤 본인이 고른 URL로 수집하세요. `--online`은 RSS URL과 설정에서 명시적으로 선택한 TTS 플러그를 허용합니다. LLM API는 `llm.mode: api`와 별도 `--allow-api`도 필요합니다. 게시 호출은 켜지 않습니다. `--offline`과 동시에 쓸 수 없으며 오프라인 실행에서는 API·TTS 플러그를 차단합니다.

```text
python run_pipeline.py --online --feed "이용 허락을 확인한 RSS URL" --output output/my-news
```

RSS 제공이 상업 재게시 허락을 보장하지는 않습니다([LAW-08](../research/FACT-SHEET.md), [문안 경로 AI-01·07](../research/ai-text-image-tools.md)). 규칙 기반 문안은 요약 AI가 아니며 사실 확인도 수행하지 않습니다. 실제 자료는 직접 대조·재작성하세요. 기사 전체를 복사하는 용도로 쓰지 마세요.

이번 신청 체크 샘플은 직접 쓴 예시 문안입니다. 실제 지원 공고를 쓸 때는 [공공누리 조사 노트](../research/music-assets-licensing.md)와 [공식 유형·출처 안내](https://goe.go.kr/goe/cm/cntnts/cntntsView.do?cntntsId=1046&mi=10092)를 읽고, 해당 본문·첨부물의 표식을 확인하세요. 제1유형은 출처 표시로 상업 이용·변경이 허용됩니다. 출처에는 기관·작성연도·제목·표시된 작성자·URL과 요약·재구성 여부를 남기세요. 표식이 없는 자료는 허락을 확인하기 전까지 넣지 마세요.

단계별 실행도 가능합니다. 아래 `manual` 폴더 산출물은 단계별 연습용입니다. 검수·승인·게시 흐름까지 잇는 실습은 `run_pipeline.py`를 사용하세요.

```bash
python fetch_news.py --output output/manual/news.json
python write_copy.py output/manual/news.json --output output/manual/copy.json
python render_cards.py output/manual/copy.json --output output/manual/cards
python make_reel.py output/manual/copy.json --cards output/manual/cards --output output/manual
```

## 카드 문안·이미지 편집 (7장)

`copy.json`은 **표지 cover → 본문 body → 마무리 closing** 순서입니다. 표지는 큰 헤드라인·브랜딩, 본문은 번호가 붙은 요점 1~3개, 마무리는 출처·저장/공유 안내·계정명을 보여 줍니다. 제목과 요점에 `**핵심 구문**`을 쓰면 강조색이 적용됩니다. 본문 카드는 `body` 대신 **`points` 배열**을 화면에 표시하므로 두 값을 함께 편집하세요. `subtitle`은 영상 자막·내레이션 대본입니다.

사진을 쓸 표지·본문 scene에 `"image": "assets/my-photo.jpg"`를 추가하세요. 파일은 사용자가 직접 제공해야 하며 자동 검색·다운로드하지 않습니다. 사진은 슬롯을 채우도록 중앙을 기준으로 잘릴 수 있습니다. image를 생략하면 자체 기하 패턴을 그립니다. 사진을 생성한 결과라고 표시하지 않습니다. 합성 피드일 때만 카드 하단에 작은 **합성 데이터 · 실제 뉴스 아님** 표시를 유지하며, 실제 RSS 카드에는 합성 표시를 넣지 않습니다.

수정 후 `run_pipeline.py render 출력폴더`로 재생성하고 다시 검수하세요. 출력 폴더의 `config.json`이 설정 스냅샷입니다. 기존 실행의 테마를 바꾸려면 config.json의 `colors`를 수정하세요. config.yaml의 theme 변경은 **새 실행**부터 반영됩니다.

## LLM 연결: 세 가지 경로 (6장)

모든 경로는 같은 `copy.json` 구조를 씁니다. **기본 offline**은 규칙 기반 후보 추출입니다. 키·모델·결제 없이 끝까지 실행할 수 있습니다.

**prompt: API 결제 없이 웹 채팅을 사용하는 경로.** 아래 명령은 LLM을 호출하지 않고 원자료·출력 JSON 예시를 포함한 `prompt.md`를 만듭니다. ChatGPT/Claude/Gemini 등 본인이 이용 가능한 웹 채팅에 내용을 직접 붙여 넣으세요. 웹 서비스의 무료 이용 한도와 데이터 처리 조건은 각 서비스에서 확인하세요([AI-01·06](../research/FACT-SHEET.md)). 답변의 **전체 JSON 객체**를 메모장으로 `output/manual/copy.json`에 저장합니다. 코드 울타리나 설명 문장은 제외하세요.

```bash
python fetch_news.py --output output/manual/news.json
python write_copy.py output/manual/news.json --mode prompt --template cards --output output/manual/copy.json
python write_copy.py output/manual/news.json --validate --output output/manual/copy.json
```

`prompts/`에는 [카드 문안](prompts/cards.md), [릴스 대본](prompts/reel-script.md), [캡션+해시태그](prompts/caption.md) 3종이 있습니다. `--template`을 `cards` / `reel-script` / `caption`으로 선택하세요. 각 템플릿은 사실 추가 금지·원출처 유지·과장 금지를 요구합니다. 모두 전체 JSON을 반환하는 계약입니다. 단계마다 이전에 편집한 문안을 유지하려면 웹 채팅에 **현재 copy.json도 함께 제공**하고 변경할 필드만 지정하세요. 프롬프트 생성은 기존 copy.json을 덮어쓰지 않습니다.

파이프라인에 이어 붙이려면 config.yaml에 `llm.mode: prompt`를 지정한 뒤 실행하세요.

```bash
python run_pipeline.py --offline --config config.yaml --output output/web-chat
```

`news.json`, `config.json`, `prompt.md`만 만들고 **문안 대기**에서 멈춥니다. 웹 채팅 답변을 `output/web-chat/copy.json`에 저장한 다음:

```bash
python write_copy.py output/web-chat/news.json --validate --output output/web-chat/copy.json
python run_pipeline.py render output/web-chat
```

구조 검증은 필수 필드·자료형·레이아웃 순서·요점 수·합성 표시·원출처 링크 보존을 검사합니다. **허위 사실·왜곡·저작권 적합성을 자동 판별하지 않습니다.** 렌더링도 구조와 원출처를 다시 검증하며 승인 전에는 게시되지 않습니다.

**api: 선택한 OpenAI 호환 엔드포인트.** 기본 비활성이며 `--mode api --allow-api`를 모두 지정해야 요청합니다. SDK 추가 설치 없이 `POST /chat/completions`의 model/messages와 choices/message/content JSON 형식을 사용합니다. 모델명은 하드코딩하지 않습니다. 키만 설정해도 호출되지는 않습니다. 이 연결 형식은 [공식 OpenAI 문서](https://developers.openai.com/api/reference/resources/chat/subresources/completions/methods/create)를 확인했으며, 호환 서비스별 지원·가격·품질을 검증한 것은 아닙니다. 이 작업의 테스트는 **모킹만** 사용했습니다.

본인 운영체제에서 `LLM_BASE_URL`(예: 선택한 서버의 HTTPS `/v1` 주소), `LLM_API_KEY`, `LLM_MODEL` 환경변수를 설정하세요. 실제 키는 코드·설정·명령 예시·Git에 적지 않습니다. 이 LLM 연결은 `.env`를 자동으로 읽지 않습니다(Instagram 게시 연결의 `.env` 지원은 6절). 유료 서비스일 수 있으므로 공급자의 이용 조건과 비용을 확인한 경우에만 실행하세요. 이번 작업에서는 키를 사용하거나 결제하지 않았습니다.

```bash
python write_copy.py output/manual/news.json --mode api --allow-api --output output/manual/copy.json
```

실패·중단·JSON 형식 오류·출처 누락은 오류로 종료하며 기존 copy.json은 보존합니다. 응답 전문과 인증 값은 출력하지 않습니다. 파이프라인에서 API를 쓰려면 config.yaml의 `llm.mode: api`에 더해 `run_pipeline.py --online --allow-api --config config.yaml --output output/api-practice`가 필요합니다. 무료 웹 채팅과 API 비용은 별개입니다.

## 움직이는 릴스와 음성 선택 (8장)

릴스에는 카드별 페이드 전환, 느린 줌/팬, 아래 자막의 페이드·슬라이드 등장, 전체 진행 막대가 있습니다. 별도 자막 영역을 두어 카드 움직임과 자막을 분리합니다. 장면 길이는 균등 배분되며 전체 길이는 24fps 프레임 단위로 반올림됩니다.

**이 예제는 연습용이며 수익화 적격을 보장하지 않습니다. 직접 촬영·내레이션 같은 독창적 요소를 더하세요.** 2026년 10월 조사 기준, [META-06](../research/FACT-SHEET.md)의 정적 영상·슬라이드쇼·반복 영상·텍스트 몽타주 제한을 고려해야 합니다. 이 항목은 Hermes의 원문 일부 확인 보고이며 Codex의 독립 본문 확인에는 한계가 있습니다. 모션·TTS를 추가했다는 사실만으로 이 제한을 벗어났다고 판단하면 안 됩니다. [ALG-03·04](../research/FACT-SHEET.md)에 따라 단순 연결·장식과 실질적 독창성을 구분하고, 게시 허용·추천·수익화 적격도 각각 확인하세요.

**기본은 무음+자막입니다. 가장 권장하는 음성은 본인이 직접 녹음한 내레이션**입니다. 본인의 말과 목소리로 녹음하면 별도 TTS 모델·타인 화자의 권리를 도입하지 않아도 됩니다. 녹음에 타인의 음원·목소리·글이 섞이면 해당 권리는 별도로 확인해야 합니다. config.yaml 예:

```yaml
reel:
  duration: 20
  tts: silent
  narration: assets/my-narration.wav  # mp3도 가능
  music: null  # 사용자 제공 파일만. 필요하면 assets/my-music.mp3
  tts_plugin: null
```

새 실행은 `python run_pipeline.py --offline --config config.yaml --output output/my-voice`로 만듭니다. 단계별 실행은 `python make_reel.py output/manual/copy.json --cards output/manual/cards --config config.yaml --output output/manual`입니다. 기존 실행에서는 출력 폴더 config.json의 reel 설정을 고친 뒤 render하세요. 경로는 config.json에서는 절대 경로를 쓰는 것이 편합니다.

내레이션은 원래 음량, 음악은 0.18배로 믹싱하고 클리핑을 제한합니다. 음악은 **사용자 제공 mp3/wav만** 받으며 자동 검색·생성·다운로드하지 않습니다. 짧은 음원은 남은 시간을 무음으로 채우고 긴 음원은 영상 끝에서 자릅니다. 음원을 반복하지 않습니다. 대본의 장면별 시간에 맞춰 녹음하고, 완성 영상을 들으며 타이밍을 직접 확인하세요. 자동 음성 인식·단어 정렬은 지원하지 않습니다.

**TTS는 사용자가 선택하는 플러그**입니다. `reel.tts: plugin`, `reel.tts_plugin: my_voice:synthesize`, `narration: null`로 설정합니다. [연결 계약과 예제](tts_backends/README.md)를 따라 본인이 검토한 모듈을 작성하세요. 엔진 코드·모델·화자 동의·상업용 출력물의 라이선스 확인 책임은 사용자에게 있습니다([VIDEO-01~04·10](../research/FACT-SHEET.md)). 기본 백엔드·모델·서비스는 동봉하지 않으며 자동 다운로드도 없습니다. 플러그는 오프라인 pipeline run에서 차단됩니다. 별도 make_reel 또는 명시적 render는 선택한 플러그를 실행합니다.

사용 음원은 출력 폴더 `audio/`에 복사되어 검수·승인 해시에 포함됩니다. REVIEW.md의 **내레이션·배경음악·TTS 라이선스 체크박스**를 확인하세요. 사실적으로 들리는 합성 음성이나 생성·변형한 실사형 영상을 사용하면 [LABEL-03](../research/FACT-SHEET.md)의 AI 자기공개 필요 여부도 검토하세요(2026년 10월 조사 기준). 합성 피드 표시와 Meta의 AI 정보 자기공개는 서로 다른 표시입니다.

## 6. 실제 게시 기능의 경계

**2026년 10월 조사 기준.** 이 예제는 [Instagram Login 경로](../research/graph-api-publishing.md)(API-01·06·08·12)를 사용합니다. 프로페셔널 계정·권한·앱 설정은 별도 준비가 필요합니다. PNG는 직접 보내지 않고 JPEG를 사용합니다. 서버가 읽을 수 있는 공개 미디어 URL도 필요합니다. 토큰 발급·로그인·웹 호스팅은 사용자가 준비합니다. 날짜별 생성 예약은 아래 안내로 직접 등록합니다.

`publish.py`는 **이미지와 동영상 모두 공개 URL**을 쓰는 Instagram Login 경로입니다(PRAC-08·09). Facebook Login의 resumable 경로를 이 키트에 적용하지 않습니다. 다음은 선택 심화 경로이며 앱 첫 게시에는 필요 없습니다.

1. 실제 자료를 직접 검수·승인하세요. 합성 샘플은 live에서 거부됩니다.
2. `.env.example`을 `starter-kit/.env`로 복사합니다. `IG_ACCESS_TOKEN`, 숫자 `IG_USER_ID`를 로컬 편집기로 입력합니다. 토큰은 API에 접근할 권한을 담은 비밀 문자열입니다. 이 파일은 Git에서 제외되며 **publish만** 읽습니다. 환경변수가 같은 이름의 값보다 우선합니다. LLM 연결의 .env 지원을 뜻하지 않습니다.
3. `IG_API_VERSION` 기본은 **v26.0**(2026-07-29 출시, PRAC-01)입니다. `.env` 또는 환경변수로 바꿀 수 있습니다. 기본 드라이런에도 이 버전을 표시합니다. `--live`를 명시하지 않으면 네트워크를 호출하지 않습니다. `approve`는 언제나 드라이런입니다.
4. 아래 명령으로 승인된 JPEG/MP4만 별도 새 폴더에 준비합니다. 명령은 복사와 안내 출력만 하며 업로드하지 않습니다.

```bash
python prepare_hosting.py output/2026-10-26 --dest hosting/first-post
```

성공 출력은 `공개 준비 완료: 6개 JPEG/MP4 → ...`입니다(기본 카드 5장일 때). `.env`·설정·검수표는 복사하지 않으며, 변경된 승인 파일·기존 대상 폴더·웹 업로드 제한 초과는 거부합니다.

5. **본인의 별도 공개 GitHub 저장소**에서 **Add file → Upload files**를 엽니다. `hosting/first-post` 안의 **cards 폴더와 reel.mp4**를 함께 드래그 앤 드롭하고 **Commit changes**로 저장합니다. 상위 `first-post` 폴더 전체를 올렸다면 URL에도 `/first-post`가 들어갑니다. **Settings → Pages → Build and deployment → Source: Deploy from a branch**에서 branch와 `/(root)`를 선택합니다(PRAC-14·15).
6. 배포가 끝나면 `https://사용자.github.io/저장소/cards/card-01.jpg`와 `/reel.mp4`가 로그인 없는 창에서 파일 자체로 열리는지 확인합니다. HTML 미리보기·Drive 공유 링크는 사용할 수 없습니다. HTTP 응답/MIME와 실제 파일을 확인해도 Meta 수신 성공을 보장하지는 않습니다. GitHub 웹 업로드는 파일당 **25MiB**이며 Pages는 작은 비민감 교육 실습용 후보입니다. 사업 운영용 무료 호스팅 이용 제한이 있으므로 운영 CDN의 포괄 권장으로 읽지 마세요(PRAC-14·15).
7. 먼저 드라이런으로 파일 경로를 확인합니다. `<URL>`은 `cards/`와 `reel.mp4`가 바로 아래에 있는 **HTTPS 폴더 주소**입니다. 따옴표 안 값을 본인 주소로 바꿉니다.

```text
python publish.py output/2026-10-26 --base-url "<URL>"
```

본인 실제 자료·계정·권한·라벨·공개 파일을 모두 확인한 경우에만 아래 명령을 선택합니다. 이 프로젝트 작업자는 이 명령을 실행하지 않았습니다. 기존 `--public-base-url`도 같은 인자로 유지합니다.

```text
python publish.py output/2026-10-26 --live --base-url "<URL>"
```

**토큰 만료와 갱신:** 대시보드 **Generate token**은 60일 장기 토큰이고 OAuth 토큰은 1시간 단기입니다(PRAC-06). 장기 토큰은 발급 후 24시간 이상 지났고 만료 전일 때 `GET https://graph.instagram.com/refresh_access_token`에 `grant_type=ig_refresh_token`, `access_token`을 전달해 다시 60일 갱신할 수 있습니다(PRAC-07). 비공개 실행 환경에서 공식 [Instagram Login 문서](https://developers.facebook.com/docs/instagram-platform/instagram-api-with-instagram-login/business-login/)에 따라 갱신하고 반환된 토큰·expires_in을 확인하세요. 만료했다면 다시 인증해야 합니다. 키트는 자동 갱신·로그인·호스팅을 대신하지 않습니다. 날짜별 생성 예약은 아래 안내로 직접 등록합니다. 토큰·시크릿을 셸 기록·공개 Git·스크린샷·AI 채팅에 남기지 마세요.

자기 소유 계정 Standard Access 검수 면제와 개발 모드의 일반 독자 공개는 별개입니다. 공통 App Modes와 앱 생성 문서에 범위 차이가 있어, 개발 모드 게시 성공이나 일반 공개를 보장하지 않습니다(PRAC-02·03). 권한은 `instagram_business_basic`, `instagram_business_content_publish`이며 Facebook 페이지 연결이 필수인 다른 로그인 경로와 구분하세요.

live는 캐러셀과 릴스를 각각 게시하므로 총 2개 게시물입니다. 실행 시작부터 `LIVE_ATTEMPT.json`을 남기며 같은 폴더의 재실행을 막습니다. 중간 실패나 응답 유실 시 일부가 이미 게시됐을 수 있습니다. 자동 복구는 없으므로 대시보드에서 확인해야 합니다. 파일을 무작정 지우고 재실행하면 중복될 수 있습니다. 실제 API 경로의 동작과 한국 계정 게시 성공은 검증하지 않았습니다.

`is_ai_generated`는 기본 false이며 실제 사용한 제작 도구와 콘텐츠에 맞게 사람이 판단합니다. 필요하면 `copy.json`에서 true로 바꾸고 재생성·검수하세요. AI 표시와 광고 표시의 판단은 별도이며, 광고/파트너십 게시 전용 파라미터는 이 예제에서 지원하지 않습니다([API-12·13](../research/graph-api-publishing.md)).

## 본인 계정 ID와 이름 확인

토큰을 발급받은 사용자는 로컬 터미널에서 다음을 실행하세요. 명령 뒤에 토큰을 붙이지 않습니다.

```bash
python token_check.py
```

숨김 입력창에 토큰을 붙여넣고 Enter를 누르면 `user_id: 숫자`와 `username: 계정이름`만 표시됩니다. 발급 대상 계정과 일치하는지 확인한 뒤 user_id를 비공개 `.env`의 `IG_USER_ID`에 저장하세요. 이 도구는 본인 계정을 읽는 요청 한 번만 보내며 토큰·응답 전문을 출력하거나 파일에 저장하지 않습니다. 숨김 입력이 불가능한 창에서는 중단합니다. 요청 실패 시 앱 대시보드에서 토큰·권한을 확인하세요. 성공은 **확인한 순간 계정을 읽을 수 있음**을 뜻하며 만료일이나 게시 권한까지 확인하지 않습니다. [조사 근거와 공식 안내](../research/practice-instagram.md)를 참고하세요.

## 매일 초안 만들기와 OS 예약 (실습 9)

`daily.py`는 매일 생성까지만 실행합니다. 키트 폴더에서 먼저 수동으로 확인하세요.

```bash
python daily.py
```

컴퓨터의 오늘 날짜가 2026-10-26이면 `output/daily/2026-10-26/`에 카드·릴스와 `REVIEW.md`가 생기고 검수 대기에서 끝납니다. `config.yaml`이 있으면 사용하고, 없으면 `config.example.yaml`을 사용합니다. 항상 오프라인이며 API·TTS 플러그는 켜지지 않습니다. 웹 채팅 모드(`llm.mode: prompt`)는 문안 대기에서 멈추므로 매일 카드·릴스까지 만들려면 `llm.mode: offline`을 사용하세요. 직접 녹음 경로가 있으면 그 파일은 사용합니다.

같은 날짜 폴더는 덮어쓰지 않습니다. 오늘 수동 확인 뒤 예약이 실행되면 로그에 중복 오류가 남을 수 있으며 기존 결과는 보존됩니다. 다음 날 폴더 생성은 아래처럼 **실제 다음 날 날짜로 바꾸어** 먼저 연습할 수 있습니다.

```bash
python daily.py --date 2026-10-27
```

`--date YYYY-MM-DD`, `--config config.yaml`, 반복 `--feed fixtures/my-feed.xml`, `--output-root output/daily-rehearsal`을 선택할 수 있습니다. 상대 경로는 모두 **키트 폴더 기준**입니다. 피드는 로컬 XML만 받습니다. 다른 날짜나 다른 출력 루트로 연습하면 이전 결과를 지우지 않아도 됩니다. 실패 후 남은 날짜 폴더도 자동 덮어쓰지 않으므로 파일과 로그를 먼저 확인하세요.

예약 안내는 설치한 가상환경의 Python으로 생성합니다. 아래에서 자신의 운영체제 **한 줄만** 실행하세요. Windows PowerShell은 앞서 안내한 것처럼 `python` 대신 `.venv\Scripts\python.exe`를 사용합니다.

```bash
python schedule_setup.py --os windows --time 09:00
python schedule_setup.py --os macos --time 09:00
python schedule_setup.py --os linux --time 09:00
```

이 명령은 등록·확인·수동 실행·삭제 안내를 **출력만** 합니다. 컴퓨터 설정을 바꾸지 않습니다. Python과 daily.py는 절대 경로로 지정합니다. macOS/Linux는 설정·출력·로그·피드도 절대 경로를 씁니다. Windows는 명령을 짧게 하기 위해 키트 내부 설정·피드·로그·사용자 지정 출력 폴더를 키트 기준 상대 경로로 전달하고, 기본 출력 폴더 옵션은 생략합니다. daily.py가 키트 기준으로 해석하므로 예약의 작업 폴더와 무관합니다. 키트 밖의 파일은 절대 경로를 유지합니다. 기본 Python은 안내를 생성한 실행 파일이며 `--python 절대경로`로 바꿀 수 있습니다. `--config`, 반복 `--feed`, `--output-root`도 지원합니다. 사용할 설정 파일은 예약 안내 생성 시 선택되므로 나중에 config.yaml을 새로 만들거나 경로를 옮기면 안내를 다시 생성하고 기존 예약을 직접 교체하세요.

- **Windows:** PowerShell에서 `cmd.exe`를 입력해 명령 프롬프트로 바꾼 뒤 출력된 `schtasks /Create ...` 한 줄을 실행하세요. 공백 경로를 감싼 중첩 따옴표와 백슬래시를 유지합니다. 같은 이름 `ReelsBookDaily`가 이미 있으면 자동 교체하지 않습니다. 변경하려면 출력된 `/Delete`로 기존 작업을 삭제한 뒤 새 안내를 등록합니다. 이 키트는 `/TR`에 전달할 명령이 261문자를 넘으면 안내 생성을 중단합니다. 이는 긴 명령의 호환성 문제를 피하기 위한 보수적 제한이며 Windows 전체 명령 길이의 확정 규격을 뜻하지 않습니다. 오류가 나면 키트를 `C:\reels` 같은 짧은 경로로 옮기고 Python·외부 파일 경로도 줄인 뒤 안내를 다시 생성하세요. [Microsoft 등록 명령](https://learn.microsoft.com/en-us/windows-server/administration/windows-commands/schtasks-create)
- **macOS/Linux:** 출력된 `crontab -e`를 실행하고 `분 시 * * * ...` 한 줄을 추가해 저장하세요. `crontab -l`에서 같은 줄이 보이는지 확인합니다. 삭제는 편집 화면에서 해당 daily.py 줄만 지우고 저장합니다. 경로에 `%`가 있으면 출력된 `\%`를 유지하세요. [cron 형식](https://man7.org/linux/man-pages/man5/crontab.5.html), [crontab 편집 명령](https://man7.org/linux/man-pages/man1/crontab.1p.html)

예약 시각은 컴퓨터의 현지 시간이며 컴퓨터가 켜져 있어야 합니다. 절전·전원 꺼짐 상태에서의 실행을 보장하지 않습니다. 로그는 기본 `output/daily/daily.log`에 누적됩니다(`--log 경로`로 직접 실행 로그도 저장 가능). 로그의 오류와 다음 날 날짜 폴더·REVIEW.md를 함께 확인하세요. 중복 실행이나 실패가 나면 자동 재시도·자동 승인·자동 게시는 하지 않습니다. 로그 파일은 필요할 때 보관하거나 정리하세요.

결과물을 열어 검수한 다음에만 `python run_pipeline.py approve output/daily/날짜`로 사람이 승인합니다. 이 명령은 게시 요청 미리보기까지만 실행합니다. 실제 자료의 앱 게시 또는 사용자가 준비한 `publish.py --live` 경로는 앞의 게시 안내를 따르세요. 동봉 합성 자료는 실제 게시할 수 없습니다.

## 7. 도구 선택과 라이선스

조사 근거는 [영상·음성·폰트 노트](../research/ai-video-voice-tools.md)의 VIDEO-01~10 및 [문안 노트](../research/ai-text-image-tools.md)입니다. 무료 웹 서비스의 제공량과 API 사용료를 혼동하지 않도록 외부 AI 서비스를 기본 경로에서 제외했습니다. 이 키트의 직접 작성한 코드·합성 데이터는 [MIT](LICENSE), 동봉 폰트는 별도의 OFL입니다.

| 선택 | 이유와 라이선스·상업 이용 경계 |
|---|---|
| 규칙 기반 Python 문안 | 키·모델 다운로드·과금 없음. 로컬 LLM을 실행했다고 주장하지 않음. 원자료의 권리는 별도 확인 |
| Pillow 13.0.0 | 한국어 글자 배치와 PNG/JPEG 생성. HTML→브라우저 캡처 대신 채택해 브라우저 설치 제거. MIT-CMU, 고지 유지(VIDEO-06) |
| PyYAML 6.0.3 | 설정 읽기. 설치 패키지 LICENSE의 MIT 확인. `safe_load` 사용. [공식 저장소](https://github.com/yaml/pyyaml) |
| FFmpeg / imageio-ffmpeg 0.6.0 | MP4 제작. wrapper는 BSD-2-Clause([공식 저장소](https://github.com/imageio/imageio-ffmpeg)). FFmpeg는 빌드별 LGPL/GPL 조건이 다름(VIDEO-07). 검증 환경 pip 바이너리는 FFmpeg 7.0.2, `--enable-gpl --enable-version3 --enable-libx264` 빌드. 바이너리는 Git에 동봉하지 않음. 재배포 시 별도 라이선스·소스 제공 의무 확인 |
| Noto Sans KR | 오픈 라이선스 한국어 폰트, 인터넷 없이 렌더링. SIL OFL 1.1(VIDEO-08/S095). 원본 TTF와 저작권·라이선스 [전문](assets/fonts/OFL.txt)을 함께 배포. 제작 이미지·영상에 폰트 라이선스 적용 의무는 없음. 폰트만 단독 판매 금지. [출처·해시](assets/fonts/README.md) |
| 무음 + 자막 | 별도 음원·모델·화자 권리 불필요. MMS는 비상업 모델, 다른 한국어 TTS의 상업 출력 권리는 조사에서 미확인이라 기본 채택하지 않음(VIDEO-01~04·10). 음성 합성을 수행한 결과물이 아님 |
| pytest 9.1.1 (개발용) | MIT. 네트워크 차단 상태에서 실제 카드·영상·드라이런 검증. [공식 저장소](https://github.com/pytest-dev/pytest) |

코드의 상업 이용 허용은 실제 뉴스·사진·음원·인물의 권리 확보나 영상 코덱 관련 조건을 대신하지 않습니다. 새 자산을 넣으면 출처와 이용 조건도 검수하세요. FFmpeg 라이선스 설명은 [S090](../research/SOURCES.md#s090)에 연결됩니다.

## 8. 테스트와 샘플 재생성

가상환경을 활성화한 상태에서:

```bash
python -m pip install --cache-dir .cache/pip -r requirements-dev.txt
python -m pytest -q
```

테스트는 날짜별 생성의 날짜·중복·공백 경로·검수 대기, 예약 명령의 인용·등록 미호출, 계정 확인의 숨김 입력·토큰 비노출을 모킹해 검사합니다. 외부 네트워크 호출을 차단한 상태에서 생성→검수 대기→테스트용 검수표 확인 처리→승인→드라이런까지 수행합니다. 세 레이아웃·테마·강조·사용자 이미지, 웹 채팅 프롬프트와 JSON 검증, 모킹한 API 성공/실패·인증 값 비노출, 직접 녹음 MP3·WAV 음악·믹싱·모킹한 TTS 플러그를 확인합니다. MP4를 실제 디코딩해 크기·프레임 수·코덱·오디오·길이를 검사합니다. 테스트의 자동 체크 처리는 테스트용이며 실제 검수는 사람이 해야 합니다.

[samples/README.md](samples/README.md)에 동봉 샘플의 생성 명령과 크기를 기록했습니다. 동봉 릴스는 같은 카드 5장을 **15초**로 줄인 편집본이며, 기본 실행은 기존 **20초** 설정입니다. 검증 환경: Ubuntu 22.04 x86_64, Python 3.11.15. Windows/macOS 명령은 안내했으며 해당 OS에서 실제 실행하지 않았습니다.

## 9. 흔한 오류

| 증상 | 해결 |
|---|---|
| `python`/`py`를 찾을 수 없음 | Python 설치 및 PATH 확인, 터미널 다시 열기. Windows는 `py -3.11`, macOS/Linux는 `python3`로 venv 생성 |
| 3.10 이하로 나옴 | 3.11 이상 설치 후 그 실행 파일로 `.venv` 생성. 이 환경 기본 `python3`도 3.10이어서 별도 3.11을 사용했음 |
| `No module named PIL/yaml/imageio_ffmpeg` | `.venv` 활성화 확인 후 `python -m pip install --cache-dir .cache/pip -r requirements.txt` |
| PowerShell에서 활성화 차단 | 명령 프롬프트(cmd)로 실행하거나 `.venv\Scripts\python.exe`를 직접 사용 |
| `No module named venv` / `ensurepip` 오류 | 배포판의 Python venv 구성 안내 확인. 시스템 설치를 키트가 자동 시도하지 않음 |
| `[Errno 17] File exists` | 같은 출력 폴더가 존재함. `--output output/second-practice`처럼 새 이름 사용 |
| `REVIEW.md` 여섯 칸 오류 | 결과물을 확인한 후 모든 `- [ ]`를 `- [x]`로 저장하고 approve |
| `검수 대상이 바뀌었거나 없습니다` | copy.json 변경 뒤 render 실행, 새 검수표 확인 후 다시 approve |
| 글이 영역을 넘침 | copy.json의 긴 제목·본문·출처를 줄인 후 render. 의미·조건·출처 링크는 보존 |
| 폰트를 열 수 없음 | `assets/fonts/NotoSansKR.ttf`가 있는지 확인. ZIP 전체를 풀고 폰트 경로 확인 |
| FFmpeg를 찾지 못함 / 영상 생성 실패 | imageio-ffmpeg 재설치와 지원 OS/CPU 확인. 시스템 ffmpeg 설치를 자동 시도하지 않음. 오류 내용을 검수자에게 전달 |
| 영상은 나오는데 소리가 없음 | 기본은 무음+자막. 음성을 원하면 위의 narration 또는 명시적 TTS 설정 확인 |
| 오프라인에서 URL 거부 | 동봉 로컬 피드를 사용. 실제 RSS만 필요하면 이용 허락 확인 후 --online |
| RSS 2.0 형식 오류 | Atom·일반 웹페이지가 아닌 channel/item 구조의 RSS XML인지 확인 |
| MP4 플레이어가 안 열림 | H.264/AAC MP4를 지원하는 로컬 플레이어로 열기. 우선 동봉 samples/reel.mp4 확인 |
