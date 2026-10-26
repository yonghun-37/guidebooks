# 검증 재현

저장소 루트:

```bash
python3 scripts/style_lint.py site-shorts/*.html site-shorts/chapters/*.html site-shorts/practice/*.html site-shorts/assets/samples/preview.html --output docs/results/phase-E-shorts/style-lint.json
python3 scripts/check_site.py --site site-shorts --output docs/results/phase-E-shorts/check-site.json
/tmp/vshorts-venv/bin/python docs/results/phase-E-shorts/check-preservation.py
/tmp/e-shorts-kit-clean/.venv/bin/python -m pytest shorts-kit/tests -q
python3 -m http.server 8637 --bind 127.0.0.1
```

서버를 켠 다른 터미널:

```bash
node docs/results/phase-E-shorts/verify-browser.mjs
```

브라우저 검증은 이 환경의 기존 playwright-core(`/tmp/ai-insta-phase3-browser/node_modules/`)와 Chromium(`/home/yonghun/.cache/ms-playwright/chromium-1228/chrome-linux64/chrome`)을 사용한다. 다른 환경에서는 스크립트의 import/실행 경로를 설치 위치에 맞춘다. 보존 검사에는 BeautifulSoup4가 있는 Python을 쓴다. 키트 의존성은 shorts-kit/requirements-dev.txt에 있다. 저장소에 새 런타임 의존성을 추가하지 않았다.

샘플 제작 명령은 [샘플 README](../../../shorts-kit/samples/README.md)에 실제 실행 순서로 적었다. clean copy에서 run→create_scenes→validate→render를 실행하고 생성한 MP4·SRT·script.json·preview.html·video-info.json만 공개 샘플로 복사했다. 샘플 본문·자막은 같은 내용이며 녹음은 넣지 않았다.

보존 비교 기준은 `40997bce3fda926a4ffe0257f6cbff450e30a114`다. 작업 시작 시 텍스트 해시·각주·앵커·입력 속성을 baseline.json에 저장했고, 이 커밋의 대상 파일 해시와 일치함을 확인했다. 원본에 있던 pytest 캐시 파일은 비교에서 제외했다. 고정 기준을 바꾸지 말고 실제 차이를 확인한다.

style_lint의 분량 축약 비교는 이번 예시 교체에 적용하지 않았다. 금지어·내부 용어·단서 회귀를 검사했다. 자료 수집·서비스 정책 재조사는 하지 않고 기존 조사 근거·각주를 보존했다.
