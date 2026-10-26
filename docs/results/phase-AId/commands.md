# AId 검증 재현

저장소 루트에서 실행했다. Linux·Python 3.11·Chromium 기준이다. 브라우저 스크립트의 Playwright/Chromium 절대 경로는 이 환경의 기존 설치를 사용한다.

```bash
python3 scripts/build_appendices.py
python3 scripts/check_site.py --output docs/results/phase-AId/check-site.json
python3 -m unittest discover -s scripts/tests
starter-kit/.venv/bin/python -m pytest -q starter-kit/tests
```

문체: 현재 원고 33페이지를 고정 `phase-9/baseline.json`에 있는 25페이지와 기준선이 없는 8페이지로 나누어 검사했다. 기준선은 바꾸지 않았다. 각 명령에 `--output docs/results/phase-AId/style-baseline.json` 또는 `style-new.json`을 지정한다. 기준선이 없는 페이지에 새 비교 기준선을 만들어 축약 통과로 세지 않는다. 과거 선택안인 `site/drafts/`와 대기용 페이지는 문체 집계에서 제외한다.

정적 서버 두 개를 사용했다. 8596은 저장소 루트다. 8597은 `/tmp/aid-deploy`에 `shelf/`를 복사하고 `reels→site/`, `shorts→site-shorts/`를 연결하고 `progress/samples/`에 키트 샘플을 복사한 실제 배포 경로다.

```bash
python3 -m http.server 8596 --bind 127.0.0.1
python3 -m http.server 8597 --bind 127.0.0.1 --directory /tmp/aid-deploy
node docs/results/phase-AId/verify-browser.mjs
FONT_NETWORK=1 node docs/results/phase-AId/verify-ai.mjs
SITE_URL=http://127.0.0.1:8596/site/ node docs/results/phase-AId/verify-practice.mjs
node docs/results/phase-AId/verify-integration.mjs
SITE_URL=http://127.0.0.1:8596/ node docs/results/phase-AId/verify-interactions.mjs
SITE_URL=http://127.0.0.1:8596/ node docs/results/phase-AId/verify-interaction-edge.mjs
```

전체 화면·AI 도구·실습·통합 검사는 실제 CDN 글꼴을 사용한다. 기존 도구/경계 회귀 검사는 CDN CSS를 빈 응답으로 치환해 시스템 글꼴 환경도 확인한다. 키트 대안 안의 도구는 접기를 열고 검사한다. AIb가 바꾼 퀴즈에는 이전 퀴즈의 재시도 링크를 요구하지 않으며 현재 남은 재시도 링크를 검사한다. 지연 로드 이미지는 도구 조작 중 내려받을 수 있으므로 로컬 assets 요청만 허용하고 외부 API 요청은 허용하지 않는다.

`regeneration.json`: 생성기 재실행 전후 site 파일 해시 비교. `static-numbering.json`: 현재 목차 번호와 모든 정적 장 링크 텍스트 비교. `js-check.json`: site JS 30개 `node --check`. 회귀 검사 red/green 로그는 새 AI 장 누락·15장/실험실 충돌·인증 토큰 오연결을 고치기 전후의 결과다.
