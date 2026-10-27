# 봄이랑 크는 집 · 블로그 코드 운영 키트

Python **3.11 이상**으로 네트워크·계정·유료 키 없이 실행합니다. 정책·샘플 금액은 **2026년 10월 조사 기준**입니다. 등장인물·제품·지표는 가상입니다.

시작은 세 단계입니다.

1. 설치: `python3.11 -m venv .venv` → `source .venv/bin/activate` (PowerShell: `py -3.11 -m venv .venv` → `.venv\Scripts\Activate.ps1`). 실행용 패키지 설치는 없습니다.
2. 진단: `python course.py doctor`.
3. 완주: `python blog.py run --sample`. `output/drafts/info.html`과 `output/analytics/weekly.html`을 엽니다. 기본 mock에서 초안·가상 승인 시연·예약까지 확인합니다.

실제 사용자가 승인하는 실습은 `python blog.py gate --sample info --approve 서윤`입니다. 관문 통과, 광고주 확인, 사람 승인, 서버 공개 확인은 각각 기록합니다. 건강·안전·협찬·제휴·아이 사진/경험·기존 글 갱신은 자동 모드에서도 승인이 필요합니다.

| 장 | 명령 색인 |
|---|---|
| A1 | `course.py doctor`, `blog.py status --mock` |
| A2 | `blog.py pages` |
| A3 | `blog.py topics` |
| A4 | `blog.py draft` |
| A5 | `blog.py gate` |
| A6 | `blog.py publish --prepare` → `gate --approve` → `publish` → `status` |
| A7 | `blog.py ads` |
| A8 | `blog.py affiliate` |
| A9 | `blog.py sponsor demo`, `sponsor settle` |
| A10 | `blog.py report` |
| A11 | `blog.py run --ops`, `run --restore` |
| A12 | `blog.py run --audit` |
| E2E | `blog.py run --scenarios` |

본문에 복사할 정확한 순서는 [course/commands.md](course/commands.md)입니다. `python course.py start A9`는 앞 장 산출물을 복원합니다. `python course.py check A9`는 파일·SQLite·명령 출력을 비교합니다. `python course.py reset`은 실습 상태를 지웁니다(`.env` 보존).

예상 출력 재생성은 `python course/build_expected.py`, 검증은 `python course/build_expected.py --check`입니다. 테스트는 `python -m pip install -r requirements-dev.lock` 후 `python -m pytest -q`로 실행합니다. 저장소의 `bash scripts/repro_blog_advanced.sh`는 빈 폴더와 새 venv에서 전 장과 6종 시나리오를 검사합니다.

설정은 `config.example.toml`을 `config.toml`로 복사해 바꿉니다. 비밀은 `.env`에만 넣습니다. 로컬/실제 WordPress와 키 교체·백업 안내는 [ops/README.md](ops/README.md)를 보세요. mock 서버는 각 명령이 임시 로컬 포트에서 켜고 끕니다.

실연결은 기본 드라이런입니다. 실제 WordPress는 `wordpress.mode=local/live`와 본인 `.env`, 명시적 `--live`가 필요합니다. 쿠팡 live API는 현행 서명·자격·약관 확인 전 비활성입니다. LLM·GA4·GSC 어댑터는 주입된 전송 함수를 모킹 테스트합니다. 자동 관문은 의료·법률 판단이나 사진의 시각 검토를 대신하지 않습니다.
