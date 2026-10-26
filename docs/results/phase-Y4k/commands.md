# 검증 재현

저장소 루트에서 실행했다. 시스템 패키지는 설치하지 않았다. Python 가상환경은 `/tmp/shorts-y4k-venv`이며 실행 시점에 core/dev/live 의존성을 pip로 설치했다. 실제 OAuth 인증·외부 대본 API·YouTube 업로드·예약 등록은 실행하지 않았다.

```bash
python3 -m venv /tmp/shorts-y4k-venv
/tmp/shorts-y4k-venv/bin/pip install -r shorts-kit/requirements-dev.txt -r shorts-kit/requirements-live.txt
/tmp/shorts-y4k-venv/bin/python -m pytest -q shorts-kit --rootdir=shorts-kit --junitxml=docs/results/phase-Y4k/pytest.xml
/tmp/shorts-y4k-venv/bin/python docs/results/phase-Y4k/verify-kit.py
python3 -m compileall -q shorts-kit
python3 scripts/check_site.py --site site-shorts --output docs/results/phase-Y4k/static-check.json
git diff --check
```

`verify-kit.py`는 공백·한글 경로의 새 임시 복사본에서 오프라인 run, prompt run, 붙여넣은 대본 validate/render, 시험용 자체 생성물 approve, upload 드라이런, 다른 작업 폴더에서 daily, Windows/macOS 예약 안내를 실제 실행한다. 플랫폼별 셸 등록 명령의 문자열만 검증하며 두 OS에서 설치·예약 등록한 결과를 뜻하지 않는다.

문체 검사기는 HTML 전용이다. 두 README는 `html.escape`로 전체 텍스트를 감싼 `<main><pre>` 임시 HTML로 바꿨다. 원본 내용은 생략하지 않았고 사이트·키트 파일은 바꾸지 않았다.

```bash
python3 scripts/style_lint.py site-shorts/index.html site-shorts/chapters/*.html site-shorts/practice/*.html site-shorts/credits.html shorts-kit/samples/preview.html /tmp/shorts-y4k-README.md.html /tmp/shorts-y4k-samples-README.md.html --output docs/results/phase-Y4k/style-lint.json
```

새 이론 원고가 아니므로 분량 기준선은 만들지 않았다. 자동 검사는 금지어·내부 용어·단서 기준에 적용했다. 정책·수치·FAQ 직답은 수동으로 확인했다.

브라우저: 기존 Playwright·Chromium을 사용했다. `/tmp/shorts-y4k-web/shorts`는 실제 `site-shorts/`에 연결한다. 사이트는 아래 서버에서, 키트는 사용자가 기본 안내대로 여는 `file://` 로컬 HTML에서 검사한다. 최소 Python HTTP 서버는 초기 미디어 탐색 범위가 0이 되는 사례가 있어 키트의 기본 검사 경로로 쓰지 않았다. README에도 서버 재생 시 탐색 실패 대안을 안내했다.

```bash
python3 -m http.server 8593 --bind 127.0.0.1 --directory /tmp/shorts-y4k-web
node docs/results/phase-Y4k/verify-browser.mjs
```

별도 터미널에서 브라우저 명령을 실행한다. 키트에는 외부 리소스가 없으며 사이트의 선택 CDN 글꼴은 빈 CSS로 대체해 시스템 글꼴 레이아웃을 확인했다. `verify-browser.mjs` 머리에 실행 파일 경로가 있다. 실제 모바일 기기 검증은 포함하지 않는다.
