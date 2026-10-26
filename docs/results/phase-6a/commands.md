# Phase 6a 실행 증거와 재현 명령

2026-10-26. Linux x86_64, Python 3.11.15, Chromium 149.0.7827.55. 원본 `site/`·`starter-kit/`는 수정하지 않았다. 아래 명령의 출력은 이번 실행에서 확인했다. 실제 키·계정·외부 게시 요청은 사용하지 않았다.

## 새 복사본과 설치

주검토 디렉터리는 Python 표준 라이브러리의 `tempfile.mkdtemp`로 만든 `/tmp/reelsbook-6a-fb1xgz8a`다. 기존 `.venv`·`.cache`·`output`·`__pycache__`·개인 `.env`를 제외하고 starter-kit을 새로 복사했다. README pip 경로를 선택했고 uv 경로는 선택하지 않았다.

요청한 셸 `mktemp -d` 경로도 `/tmp/reelsbook-6a-clean.FEAaWg`에 별도로 실행했다. 그곳에서도 새 복사·새 venv·pip 설치·고정 폴더 첫 생성·prompt·validate까지 다시 성공했다. 두 디렉터리 모두 기존 Python 패키지나 출력물을 가져오지 않았다.

```bash
review_clean_dir=$(mktemp -d /tmp/reelsbook-6a-clean.XXXXXX)
# 이 새 디렉터리에 원본 starter-kit을 복사한다. .env 등 개인 파일은 제외한다.
cd "$review_clean_dir/starter-kit"
python3 --version
# 이 환경에서는 Python 3.10.12. 설치된 3.11 실행 파일을 선택했다.
python3.11 -m venv .venv
source .venv/bin/activate
python --version
python -m pip install --cache-dir .cache/pip -r requirements.txt
```

실제 설치 성공: Pillow 13.0.0, PyYAML 6.0.3, imageio-ffmpeg 0.6.0. 시스템 Python·시스템 패키지를 설치/변경하지 않았다. Linux에서 `python3.11`을 고른 것을 macOS 실기기 확인으로 기록하지 않는다.

## README 첫 실행과 실습 2~6

주검토 복사본에서 README 날짜 폴더 첫 실행과 실습 고정 폴더 경로를 각각 실행했다.

```bash
python run_pipeline.py --offline
python run_pipeline.py --offline --output output/first-post
python write_copy.py output/first-post/news.json --mode prompt --template cards --output output/first-post/copy.json
python write_copy.py output/first-post/news.json --validate --output output/first-post/copy.json
```

확인한 출력:

```text
검수 대기: /tmp/reelsbook-6a-fb1xgz8a/starter-kit/output/2026-10-26/REVIEW.md
검수 대기: /tmp/reelsbook-6a-fb1xgz8a/starter-kit/output/first-post/REVIEW.md
웹 채팅에 붙여 넣을 프롬프트: output/first-post/prompt.md. 답변 JSON을 output/first-post/copy.json에 저장하고 --validate로 확인하세요.
구조 검증 OK: output/first-post/copy.json (사실 확인은 사람이 해야 합니다)
```

채팅 서비스는 사용하지 않고 실습이 허용하는 직접 편집 경로를 택했다. [독자 메모](learner-notes.md)의 문장으로 title·body·points·subtitle을 편집한 뒤 검증을 다시 실행했다.

```bash
python write_copy.py output/first-post/news.json --validate --output output/first-post/copy.json
python run_pipeline.py render output/first-post
```

실습 5의 무음 선택을 유지하고 안내된 render도 실행했다. 각 실행은 검수 대기 경로를 출력했다. PNG/JPEG 10개를 열고 원자료·문안을 대조했다. 영상은 브라우저에서 20초 끝까지 재생했고 다섯 장면 중간도 확인했다. 폰트 OFL·합성 피드·무음·미사용 외부 자산·캡션·AI/광고 표시 여부를 검토한 뒤 REVIEW.md의 여섯 항목을 편집해 저장했다. 생성만 보고 검토를 생략하지 않았다.

```bash
python run_pipeline.py approve output/first-post
python publish.py output/first-post
python prepare_hosting.py output/first-post --dest hosting/first-post
python publish.py output/first-post --base-url "https://example.org/review-only"
```

approve와 publish는 `mode: dry-run`, `login: Instagram Login`, Bearer 자리표시자 및 컨테이너 생성→상태 확인→게시의 요청 목록을 출력했다. `APPROVED.json`·`dry-run.json`이 생성됐다. `prepare_hosting` 출력은 다음과 같았다.

```text
공개 준비 완료: 6개 JPEG/MP4 → /tmp/reelsbook-6a-fb1xgz8a/starter-kit/hosting/first-post
```

호스팅 폴더는 `cards/card-01.jpg`~05.jpg와 `reel.mp4`뿐이다. 공개 GitHub 업로드·토큰 발급·`.env` 비밀 값 입력·live는 실행하지 않았다. example.org 주소는 출력 값 치환을 확인하기 위한 자리표시자다. 해당 URL이 실제 미디어를 제공한다고 검증한 것이 아니다.

## 실습 3 실제 자료 분기의 구조 검증

예시와 같은 RSS 2.0 XML에 item 한 개를 넣어 `my-feed.xml`로 저장했다. 제목·날짜·URL·설명을 로컬 검토용 값으로 채운 **명령 시험 입력**이다. 실제 뉴스 게시용 권리나 원문 검증을 마쳤다고 주장하지 않는다.

```bash
python run_pipeline.py --offline --feed my-feed.xml --output output/my-news
```

검수 대기에서 정상 종료했고 `scenes`는 3개, PNG/JPEG도 각각 3개다. `synthetic=false`인 것은 합성 태그 없는 입력의 처리 결과이며, 실제 자료임을 자동 검증했다는 뜻이 아니다. card-04/05는 생성되지 않았다. 이것이 F02의 재현 근거다. 기본 `account_name`이 계속 하린으로 남는 것도 확인했다.

## README 개별 명령 경로

```bash
python fetch_news.py --output output/manual/news.json
python write_copy.py output/manual/news.json --output output/manual/copy.json
python render_cards.py output/manual/copy.json --output output/manual/cards
python make_reel.py output/manual/copy.json --cards output/manual/cards --output output/manual
```

실행 종료값 0. `output/manual/news.json`, 카드 PNG 다섯 경로, `output/manual/reel.mp4`를 확인했다. 이 별도 연습 폴더를 사람 승인 파이프라인과 혼합하지 않았다.

## 매체 검증

`media-playback.json`은 로컬 JPEG 5개 크기, MP4 3.99→8.02→12.07→16.11→20초 진행과 ended=true를 기록한다. 브라우저는 영상 1080×1920·길이 20초를 읽었다.

설치된 imageio-ffmpeg 실행 파일로 같은 MP4를 디코딩하고 `volumedetect`를 실행했다.

```text
Duration: 00:00:20.00
Video: h264 (High), yuv420p, 1080x1920, 24 fps
Audio: aac (LC), 48000 Hz, stereo
mean_volume: -91.0 dB
max_volume: -91.0 dB
```

무음 AAC 트랙이 있는 것이며 음성 합성을 했다고 기록하지 않는다. 2·6·10·14·18초의 `reel-mid-*.png`는 장면 중간 화면이다.

## 사이트·문체·키트 검사

```bash
python3 scripts/check_site.py
python3 scripts/style_lint.py site/chapters/[0-9]*.html site/practice/[0-9]*.html \
  --baseline docs/results/phase-9/baseline.json --output docs/results/phase-6a/style-lint.json
python3 scripts/style_lint.py site/practice/e2e.html site/lab.html site/glossary.html site/credits.html \
  --output docs/results/phase-6a/style-lint-appendices.json

# 주검토용 새 복사본의 .venv에서, README 테스트 절차
python -m pip install --cache-dir .cache/pip -r requirements-dev.txt
python -m pytest -q
```

- check_site: HTML 37개·내부 참조 1,326개·catalog 29개·실습 단계 35개, 오류 0.
- style_lint: 본문 25/25, 부록 4/4 통과. 금지어·내부 용어·상자 밖 지정 단서 표현 0.
- pytest: **67 passed in 25.69s**.
- 브라우저: 본문 경로 29개×3폭에서 넘침 0·콘솔/페이지 오류 0. 이론 도구·공용 실습 도구 조작 93개 기록. 추가 브라우저 기록 59개에는 이론 전체 퀴즈, OS 탭, 실험실 28개 선택, 용어 링크를 포함한다.

브라우저 조작을 만든 임시 스크립트에서 퀴즈 선택 잠금·숨겨진 iframe·비활성 이전 버튼을 잘못 골랐던 시행 오류는 고친 뒤 재실행했다. 사이트 결함이나 사이트 수정으로 보고하지 않았다. 최종 JSON의 errors는 모두 빈 배열이다. 전체 퀴즈 정답 수는 `extra-browser-checks.json`을 사용한다. 첫 순회는 문항마다 초기화했으므로 `browser-reading.json` 이론 score는 마지막 한 문항만 남는다.

## 미실행 범위

실제 계정 가입·로그인·연락·포스팅·예약·토큰·LLM/TTS 호출·유료 API·공개 배포, 실제 스마트폰 전송, 24시간/7일 경과 관찰, Windows/macOS·Safari 실기기, 선택 녹음·음악은 수행하지 않았다. 계정·웹 채팅·외부 설정은 문안의 구체성만 판정했다.

조사 주장을 모두 새로 조사하는 작업도 아니다. 인용 표기·저장소 사실표와 연결을 점검했고, NAVER의 RSS 관련 원문은 직접 열어 확인했다. Meta 계정 도움말의 새 요청은 429였으므로 성공으로 쓰지 않았다.

검토 기록만 작성했으며 commit·push·사이트/키트 수정은 하지 않았다. 임시 디렉터리는 재현·후속 확인용으로 남겼고 `/tmp` 보존을 보장하지 않는다. 장기 근거는 이 문서·JSON·스크린샷이다.

## 완료 보고

요청한 `python3 scripts/notify.py`를 차단 1·혼란 12·사소 2 집계와 기록 경로·남은 문제로 실행했다. 응답 `sent 200`을 확인했다. 알림에 토큰이나 개인 환경 값을 포함하지 않았다. 최종 [파일 보존·집계 확인](final-verification.json)에서 사이트·키트 2,752개 파일의 전후 SHA256이 일치했다.
