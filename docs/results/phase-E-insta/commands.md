# E-insta 검증 재현

작업 시작 기준 커밋: `da62a01bdca3801b07f577b9a05e785d10135a5a`. 시작 시 site/·starter-kit/은 미수정 상태였다. before-hashes.json은 설치·출력·캐시를 제외한 시작 시점 파일 해시다. 검증은 저장소 루트에서 실행한다.

```bash
python3 scripts/check_site.py --site site --output docs/results/phase-E-insta/check-site.json
python3 docs/results/phase-E-insta/verify-content.py
python3 -m http.server 8647 --bind 127.0.0.1
# 별도 터미널
node docs/results/phase-E-insta/verify-browser.mjs
node docs/results/phase-E-insta/verify-interactions.mjs
# 키트 폴더에서
.venv/bin/python -m pytest -q
```

verify-content.py는 /tmp/e-insta-before에 둔 시작 시점 site/·starter-kit/ 사본과 비교한다. 미래 세션에서는 위 기준 커밋의 해당 두 폴더를 별도 임시 폴더로 추출해 같은 위치에 두면 된다. `.git`을 쓰거나 현재 작업 파일을 되돌릴 필요가 없다. 브라우저 검증은 이 환경의 기존 Playwright·Chromium 경로를 사용한다.

문체 검사에서는 기존 기준선에 등록된 파일에만 그 기준선을 적용한다. 기준선을 새로 만들거나 수정하지 않는다.

```python
import json, subprocess
from pathlib import Path
base = json.loads(Path('docs/results/phase-9/baseline.json').read_text())['files']
files = sorted(str(p) for p in Path('site').rglob('*.html')
               if '/drafts/' not in str(p) and p.name != 'coming-soon.html')
for label, paths, extra in [
    ('baseline', [p for p in files if p in base], ['--baseline', 'docs/results/phase-9/baseline.json']),
    ('other', [p for p in files if p not in base], []),
]:
    subprocess.run(['python3', 'scripts/style_lint.py', *paths, *extra,
                    '--output', f'docs/results/phase-E-insta/style-{label}.json'], check=True)
```

샘플은 starter-kit/samples/README.md의 20초 기본 생성 → 문안 복사·15초 설정 → 구조 검증 → 재생성 절차를 따른다. 실제 실행 기록은 sample-commands.txt, 실파일 규격·해시는 sample-audit.json에 있다. pytest는 실제 디코딩·모션·무음과 모킹한 live 차단을 확인하며, 외부 게시 요청은 하지 않는다.
