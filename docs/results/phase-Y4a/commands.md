# Y4a 검증 명령

저장소 루트에서 실행했다. 실행 환경은 기존 Playwright Core와 Chromium을 사용한다(각 검증 스크립트의 import/실행 파일 경로 참고). 추가 설치·결제는 하지 않았다.

```bash
python3 -m http.server 8594 --bind 127.0.0.1
```

별도 터미널에서:

```bash
python3 scripts/style_lint.py site-shorts/chapters/01-map.html site-shorts/chapters/03-hook.html site-shorts/chapters/04-script.html site-shorts/chapters/05-audio.html --output docs/results/phase-Y4a/style-lint.json
python3 scripts/check_site.py --site site-shorts
node docs/results/phase-Y4a/verify-tools.mjs
node docs/results/phase-Y4a/verify-regressions.mjs
node docs/results/phase-Y4a/verify-edge-cases.mjs
node docs/results/phase-Y4a/verify-browser.mjs
git diff --check
```

결과: 문체4장·정적 오류0·기본도구24·리뷰회귀2·확장경계59·화면/탐색626 통과. 화면/탐색 검사는 실제 CDN 글꼴을 사용하고, JS 없음/저장소 차단도 확인한다. 합성음은 AudioContext의 실제 실행·정지까지 확인하되 실제 녹음의 발음 평가나 휴대폰 실기기 음질 검증을 뜻하지 않는다.

통합 diff는 다음 명령으로 임시 복사본에만 적용한 뒤 검증했다.

```bash
python3 - <<'PY'
from pathlib import Path
import subprocess
root = Path('/tmp/y4a-integration')
(root / 'site-shorts/assets').mkdir(parents=True, exist_ok=True)
(root / 'site-shorts/assets/book.js').write_text(Path('site-shorts/assets/book.js').read_text())
doc = Path('docs/results/phase-Y4a-requests.md').read_text()
patch = doc.split('```diff\n', 1)[1].split('\n```', 1)[0] + '\n'
(root / 'book.patch').write_text(patch)
subprocess.run(['patch', '-p1', '-i', str(root / 'book.patch')], cwd=root, check=True)
PY
node docs/results/phase-Y4a/verify-integration.mjs
```

결과: 임시 JS 응답으로 통합 diff 15개 검사 통과. 저장소의 공통 파일은 수정하지 않았다. credits 삽입 diff는 수동 통합용이며 자동 patch에 포함하지 않는다.

`source-syntax-check.json`은 네 장의 Y 각주 참조와 출처 절의 일치, 인라인 JS를 추출한 `node --check` 결과다. `tools-red.txt`, `regressions-red.json`, `audio-restore-red.txt`는 기능 부재 또는 수정 전 문제를 재현한 기록이다. 수정 후 파일은 `tools-check.json`, `regressions-green.json`, `edge-check.json`이다.

도구 스크린샷만 캡처할 때 고정 헤더·본문 건너뛰기 링크의 `visibility`를 캡처 스타일로 숨겼다. 실제 제품 스타일과 전체 화면 캡처는 그대로다. 대표 화면은 B 문장·1.5초 프레임을 선택한 별도 캡처다.
