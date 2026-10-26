# 검증 재현

저장소 루트에서 실행한다. 별도 임시 서버는 다음 명령으로 연다.

```bash
python3 -m http.server 8606 --bind 127.0.0.1
```

다른 터미널에서 실행한다. 기존 설치 Playwright와 Chromium 경로는 `verify.mjs` 머리에 있다. 신규 의존성은 설치하지 않았다.

```bash
python3 scripts/style_lint.py site-shorts/chapters/1*.html --output docs/results/phase-Y4c/style-lint.json
python3 scripts/check_site.py --site site-shorts --output docs/results/phase-Y4c/static-check.json
node --check site-shorts/assets/operations.js
node docs/results/phase-Y4c/verify.mjs
git diff --check
```

`SITE_ORIGIN`으로 서버 주소를 바꿀 수 있다. 기본값은 `http://127.0.0.1:8606`이다. 실제 버전 고정 CDN 글꼴을 켜서 검사했다. 브라우저 검증은 이 묶음의 다섯 장과 해당 페이지에서 생성한 링크를 대상으로 한다. 정적 검사는 실행 시점의 전체 `site-shorts`와 서가를 포함한다. 기준선 생성·70% 비교·실계정 로그인·업로드는 수행하지 않는다.

`content-check.json`은 학습자 질문 25개와 FAQ 문구의 정확한 대조 및 블록·행동·각주 앵커 검사 기록이다. `protected-files.json`은 공통 파일·샘플·프로젝트 상태 11개의 HEAD 동일성과 SHA256을 기록한다. 질문별 직답·예·행동의 의미와 수치 근거는 별도로 원고를 읽고 확인했다.
