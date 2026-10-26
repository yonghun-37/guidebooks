# 검증 재현

저장소 루트에서 실행한다. `check-preservation.py`는 작업 시작 때의 커밋을 고정해 비교한다. 다른 작업자의 수정이 있는 현재 검사기는 읽고 실행만 한다.

```bash
python3 scripts/style_lint.py site-shorts/*.html site-shorts/chapters/*.html site-shorts/practice/*.html site-shorts/assets/samples/preview.html --output docs/results/phase-V-shorts/style-lint.json
python3 scripts/check_site.py --site site-shorts --output docs/results/phase-V-shorts/check-site.json
python3 docs/results/phase-V-shorts/check-preservation.py
python3 -m http.server 8637 --bind 127.0.0.1
```

서버를 켠 별도 터미널에서:

```bash
node docs/results/phase-V-shorts/verify-browser.mjs
```

브라우저 스크립트는 이 환경의 기존 `playwright-core`(`/tmp/ai-insta-phase3-browser/node_modules/`)와 Chromium(`/home/yonghun/.cache/ms-playwright/chromium-1228/chrome-linux64/chrome`)을 사용한다. 다른 환경에서는 해당 두 import/실행 경로만 설치 위치에 맞춘다. 새 패키지·의존성을 저장소에 추가하지 않았다.

전체 36페이지를 6가지 폭/테마 조합으로 열고, 각 figure 캡션·이미지 로드·경계·SVG 변환 후 글자 크기·펼친 설명의 가로 넘침을 확인한다. 대표 그림 4종은 6조합 모두, 나머지 그림은 360px 다크로 저장한다. element 스크린샷을 찍을 때만 고정 헤더를 숨겨 그림이 가려지지 않게 한다. 실제 화면 검사는 원래 헤더가 있는 상태에서 실행한다.

최종 결과의 한계: 실제 폰·서비스 계정 조작이나 독립 초보자 실습을 대신하지 않는다. 원본 도구 계산 로직은 변경하지 않았으며 이번에는 퀴즈·방향키·임베드와 구조 보존을 회귀 검사했다.
