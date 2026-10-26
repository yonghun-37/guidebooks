# V-insta 검증 재현

저장소 루트에서 실행한다. Python 3.11·이 환경에 설치되어 있던 Playwright/Chromium을 사용했다.

```bash
python3 scripts/check_site.py --output docs/results/phase-V-insta/check-site.json
python3 scripts/check_site.py --site site-shorts --output docs/results/phase-V-insta/check-shorts.json
python3 -m unittest discover -s scripts/tests -v
python3 docs/results/phase-V-insta/verify-static.py
python3 -m http.server 8614 --bind 127.0.0.1
# 다른 터미널에서
node docs/results/phase-V-insta/verify-browser.mjs
```

문체 검사에는 기존 `docs/results/phase-9/baseline.json`에 등록된 25파일만 `--baseline`을 지정했다. 기타 본편/부록 8파일에는 새 기준선을 만들지 않았다. 과거 문체 시안 `site/drafts/`와 준비 안내 페이지는 문체 집계에서 제외하고, 브라우저에서는 전체 38 HTML을 확인했다.

```python
import json
import subprocess
from pathlib import Path
base = json.loads(Path('docs/results/phase-9/baseline.json').read_text())['files']
files = sorted(p.as_posix() for p in Path('site').rglob('*.html')
               if '/drafts/' not in str(p) and p.name != 'coming-soon.html')
for label, paths, extra in [
    ('baseline', [p for p in files if p in base], ['--baseline', 'docs/results/phase-9/baseline.json']),
    ('other', [p for p in files if p not in base], []),
]:
    subprocess.run(['python3', 'scripts/style_lint.py', *paths, *extra,
                    '--output', f'docs/results/phase-V-insta/style-{label}.json'], check=True)
```

브라우저는 1280/375/360px에서 실제 CDN 글꼴을 기다리고 라이트/다크 선택 후 접힌 내용을 펼쳤다. 새 그림의 글자 크기·SVG 텍스트 경계·HTML 넘침, 모든 figure의 캡션·이미지 로드, 페이지 가로 폭과 퀴즈 키보드 조작을 검사했다. 로컬 서비스나 외부 계정에 요청하는 인터랙션은 없다.

`browser-check.json`의 56개 자동 스크린샷과 별도 직접 확인한 `card-compare-360-light.png`를 보관했다. 그림을 가리키는 내부 앵커·API 문서 근거는 정적 검사로 확인했다. 실제 서비스 화면과 OS 실기기를 검증했다는 뜻은 아니다.
