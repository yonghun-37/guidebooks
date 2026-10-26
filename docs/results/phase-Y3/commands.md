# Y3 검증 재현

저장소 루트에서 실행한다. 정적 검사에는 Python 표준 라이브러리만 필요하다.

```bash
python3 -m unittest discover -s scripts/tests -v
python3 scripts/check_site.py --site site-shorts --output docs/results/phase-Y3/static-check.json
python3 scripts/check_site.py --output docs/results/phase-Y3/reels-regression.json
python3 scripts/style_lint.py site-shorts/index.html site-shorts/chapters/*.html site-shorts/practice/*.html site-shorts/credits.html --output docs/results/phase-Y3/style-lint.json
node --check site-shorts/assets/book.js
node --check site-shorts/assets/practice.js
node --check site-shorts/assets/sim/common.js
node --check site-shorts/assets/shorts.js
git diff --check
git diff --name-only -- site/
```

`--baseline` / `--write-baseline`을 사용하지 않았다. 마지막 명령은 출력이 없어야 한다.

브라우저 검사에는 이 환경의 기존 Playwright와 Chromium을 사용한다. 경로는 두 `.mjs` 머리에 있다. 새 의존성을 설치하지 않았다. 검사 서버에는 Pages와 같은 경로 배치가 필요하다. 임시 디렉터리에 `shelf/.`를 복사하고 `site`를 `reels/`, `site-shorts`를 `shorts/`, 샘플 PNG/MP4를 `progress/samples/`로 복사한다. 실제 검사는 `/tmp/shorts-y3-preview/`에서 책 폴더를 원본으로 심볼릭 링크해 실행했다.

```bash
python3 -m http.server 8589 --bind 127.0.0.1 --directory /tmp/shorts-y3-preview
```

별도 터미널에서 실행한다.

```bash
node docs/results/phase-Y3/verify-tools.mjs
FONT_NETWORK=1 node docs/results/phase-Y3/verify-browser.mjs
```

`SITE_URL`은 도구 검사의 책 루트, `SITE_ORIGIN`은 화면 검사의 서버 원점을 바꾼다. `FONT_NETWORK`를 생략하면 글꼴 CDN을 빈 CSS로 대체해 시스템 글꼴 레이아웃을 확인한다. `fallback-browser-check.json`은 그 실행 결과다. `browser-check.json`과 현재 PNG는 실제 CDN 글꼴을 켠 최종 검사다.

`assembly-check.json`은 임시 복사본에 실제 워크플로 순서대로 파일을 조립하고 두 샘플 포함 여부·파일 수·합계 바이트를 확인한 결과다. GitHub Actions나 실계정 업로드를 실행하지 않았다.
