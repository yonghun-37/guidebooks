# 장별로 그대로 실행할 명령

Python 3.11 이상을 설치하고 키트 폴더에서 시작하세요. 기본 시계는 `2026-10-27`, 시드는 `37`입니다.

| 준비 | macOS / Linux | Windows PowerShell |
|---|---|---|
| 가상환경 | `python3.11 -m venv .venv` | `py -3.11 -m venv .venv` |
| 활성화 | `source .venv/bin/activate` | `.venv\Scripts\Activate.ps1` |
| 테스트 설치(선택) | `python -m pip install -r requirements-dev.lock` | `python -m pip install -r requirements-dev.lock` |

아래는 두 운영체제에서 동일하게 실행합니다. 다른 장부터 시작하려면 먼저 `python course.py start A5`처럼 시작 상태를 복원하세요. 장의 명령을 다 실행한 뒤 `python course.py check A5`로 확인합니다. 기본 mock 서버는 각 명령이 잠깐 켜고 끕니다. 외부 네트워크·키가 필요 없습니다.

| 장 | macOS / Linux | Windows PowerShell |
|---|---|---|
| A1 | `python course.py doctor` | `python course.py doctor` |
| A1 | `python blog.py status --mock` | `python blog.py status --mock` |
| A2 | `python blog.py pages` | `python blog.py pages` |
| A3 | `python blog.py topics` | `python blog.py topics` |
| A4 | `python blog.py draft --sample info` | `python blog.py draft --sample info` |
| A4 | `python blog.py draft --sample play` | `python blog.py draft --sample play` |
| A4 | `python blog.py draft --sample affiliate` | `python blog.py draft --sample affiliate` |
| A5 | `python blog.py gate --sample info` | `python blog.py gate --sample info` |
| A5 | `python blog.py gate --sample play` | `python blog.py gate --sample play` |
| A6 | `python blog.py publish --sample info --prepare` | `python blog.py publish --sample info --prepare` |
| A6 | `python blog.py gate --sample info --approve 서윤` | `python blog.py gate --sample info --approve 서윤` |
| A6 | `python blog.py publish --sample info` | `python blog.py publish --sample info` |
| A6 | `python blog.py status --sample info` | `python blog.py status --sample info` |
| A7 | `python blog.py ads` | `python blog.py ads` |
| A8 | `python blog.py affiliate --sample affiliate` | `python blog.py affiliate --sample affiliate` |
| A8 | `python blog.py gate --sample affiliate` | `python blog.py gate --sample affiliate` |
| A9 | `python blog.py sponsor demo` | `python blog.py sponsor demo` |
| A9 | `python blog.py draft --sample sponsor --human-notes` | `python blog.py draft --sample sponsor --human-notes` |
| A9 | `python blog.py publish --sample sponsor --prepare` | `python blog.py publish --sample sponsor --prepare` |
| A9 | `python blog.py gate --sample sponsor --approve 서윤` | `python blog.py gate --sample sponsor --approve 서윤` |
| A9 | `python blog.py publish --sample sponsor` | `python blog.py publish --sample sponsor` |
| A9 | `python blog.py status --sample sponsor --advance-days 2` | `python blog.py status --sample sponsor --advance-days 2` |
| A9 | `python blog.py sponsor settle` | `python blog.py sponsor settle` |
| A10 | `python blog.py report` | `python blog.py report` |
| A11 | `python blog.py run --ops` | `python blog.py run --ops` |
| A11 | `python blog.py run --restore` | `python blog.py run --restore` |
| A12 | `python blog.py run --audit` | `python blog.py run --audit` |
| E2E | `python blog.py run --scenarios` | `python blog.py run --scenarios` |

원하는 명령만 바꿔 보려면 `python blog.py --help`를 읽으세요. 예상 출력은 `course/expected/<장>/terminal.txt`에 있습니다.
전체 명령 재실행은 `python course/execute.py --all`입니다. 이 명령은 현재 실습 상태를 초기화합니다. `.env`는 보존합니다.
