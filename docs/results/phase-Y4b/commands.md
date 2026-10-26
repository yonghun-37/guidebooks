# Y4b 검증 재현

저장소 루트에서 실행한다. Python 표준 라이브러리와 기존 Playwright/Chromium을 사용한다. 새 의존성을 설치하지 않았다.

```bash
python3 scripts/style_lint.py site-shorts/chapters/06-scenes.html site-shorts/chapters/07-editing.html site-shorts/chapters/08-captions.html site-shorts/chapters/09-export.html --output docs/results/phase-Y4b/style-lint.json
python3 scripts/check_site.py --site site-shorts --output docs/results/phase-Y4b/static-check.json
node --check site-shorts/assets/y4b.js
git diff --check
```

브라우저 검사(서버와 검사를 한 프로세스에서 관리해 검사 중 서버가 종료되지 않게 한다):

```bash
python3 - <<'PY'
import http.server, threading, subprocess, os
class Handler(http.server.SimpleHTTPRequestHandler):
    def log_message(self, *args):
        pass
server = http.server.ThreadingHTTPServer(('127.0.0.1', 18634), Handler)
threading.Thread(target=server.serve_forever, daemon=True).start()
try:
    result = subprocess.run(['node', 'docs/results/phase-Y4b/verify-browser.mjs'],
                            env={**os.environ, 'FONT_NETWORK': '1'})
finally:
    server.shutdown()
raise SystemExit(result.returncode)
PY
```

`FONT_NETWORK`가 있으면 실제 버전 고정 글꼴 CDN을 불러온다. 없으면 글꼴 CSS를 빈 내용으로 대체해 시스템 글꼴을 검사한다. `fallback-browser-check.json`은 시스템 글꼴 검사, `browser-check.json`과 PNG는 실제 CDN을 켠 최종 검사다. 스크린샷은 기본 예제이며 본문 첫 화면 4개와 도구 12개다. 긴 도구의 요소 스크린샷에 고정 머리글과 초점용 건너뛰기 링크가 중간에 끼어들지 않도록 **캡처 중에만** 해당 두 요소를 숨긴다. 서비스 CSS나 HTML을 바꾸지 않는다.

HTML/구조·FAQ·퀴즈·화면 가로 넘침·앵커·키보드·경계값·재생/정지·반복·화면 이탈 정지·저장 차단·JS 꺼짐을 검사한다. 실제 업로드·OS 앱 조작·기기별 플레이어 가림 영역은 검증 범위 밖이다. 공용 목차의 준비중 표시는 통합 요청 전제라 테스트가 완성 표시를 요구하지 않는다.
