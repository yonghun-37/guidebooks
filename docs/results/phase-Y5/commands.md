# Y5 검증 재현

저장소 루트에서 실행한다. 브라우저 스크립트의 Playwright·Chromium 경로는 이 작업 환경의 기존 설치다. 테스트 의존성은 기존 `/tmp/shorts-y4k-venv/`를 재사용했다.

```bash
python3 scripts/build_appendices.py --site site-shorts
python3 scripts/check_site.py --site site-shorts --output docs/results/phase-Y5/check-site.json
python3 scripts/style_lint.py $(rg --files site-shorts -g '*.html') --output docs/results/phase-Y5/style-lint.json
python3 docs/results/phase-Y5/check-content.py
/tmp/shorts-y4k-venv/bin/python -m pytest scripts/tests -q
```

키트는 `shorts-kit/`를 작업 디렉터리로 삼아 실행했다.

```bash
/tmp/shorts-y4k-venv/bin/python -m pytest -q
```

브라우저는 저장소 루트 HTTP 서버를 별도 터미널에서 실행한다. 원래 검증 실행에서는 임시 Python 래퍼가 같은 서버를 열고 검사 종료 후 닫았다.

```bash
python3 -m http.server 8615 --bind 127.0.0.1
```

다른 터미널의 저장소 루트에서 실행한다.

```bash
node docs/results/phase-Y5/verify-browser.mjs
git diff --check
```

`generation-check.json`은 생성 전후 `site-shorts/` 파일 SHA256을 비교했다. 두 번의 연속 실행에서 차이가 없었다. 키트 샘플의 바이트 일치는 `check-content.py`가 다시 검사한다. `--site site-shorts`를 생략하면 ReelsBook 생성기가 실행되므로 쇼츠 통합에서는 반드시 인자를 쓴다.
