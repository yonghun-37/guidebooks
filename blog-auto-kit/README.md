# 봄이랑 크는 집 · 블로그 코드 운영 키트

Python **3.11 이상**으로 네트워크·계정·유료 키 없이 실행합니다. 정책·샘플 금액은 **2026년 10월 조사 기준**입니다. 등장인물·제품·지표는 가상입니다.

시작은 세 단계입니다.

1. 설치: `python3.11 -m venv .venv` → `source .venv/bin/activate` (PowerShell: `py -3.11 -m venv .venv` → `.venv\Scripts\Activate.ps1`). 실행용 패키지 설치는 없습니다.
2. 진단: `python course.py doctor`.
3. 완주: `python blog.py draft --sample info` → `python blog.py publish --sample info --prepare` → 초안을 읽고 `python blog.py gate --sample info --approve 서윤` → `python blog.py run --sample`. `output/drafts/info.html`과 `output/analytics/weekly.html`을 엽니다. 기본 mock에서 명시적으로 승인한 글만 예약하며 시연도 승인을 대신 만들지 않습니다.

실제 사용자가 승인하는 실습은 `python blog.py gate --sample info --approve 서윤`입니다. 관문 통과, 광고주 확인, 사람 승인, 서버 공개 확인은 각각 기록합니다. 자동 발행은 사람이 승인한 틀에 검증된 구조화 데이터만 채운 글뿐입니다. AI나 사람이 쓴 자유 문장은 모두 사람이 읽고 글별 승인합니다. `python blog.py template approve library --by 서윤`으로 `content/templates/library.md`와 `library.schema.json`의 해시를 승인하며, 파일 변경 시 승인이 무효가 됩니다. 데이터는 정해진 칸·타입·길이·열거값만 허용하는 JSON Schema 부분집합으로 검사합니다. 자유 문자열·중첩·알 수 없는 규칙은 거절합니다. URL은 현재 설정의 정확한 기관 호스트만 허용합니다. 발행 직전 제목·설명·본문·HTML과 문서 전체가 렌더 결과와 같아야 합니다. 신규·모든 관문 pass·설정 허용 유형도 필요합니다. 본문·HTML의 제휴·쇼핑 링크는 표시 관문과 사람 승인으로 보내며 미허용 URL도 사람이 확인합니다. 건강·안전·협찬·제휴·아이 사진/경험·기존 글 갱신은 자동 모드에서도 승인이 필요합니다. 지원하는 JPEG·PNG는 실제 형식으로 검사하고 메타데이터를 제거해 재검사한 공개용 사본만 업로드합니다. 약 이름·식별·표시 문구 검사는 보조 장치이며 원문과 사진 내용은 사람이 확인합니다.

| 장 | 명령 색인 |
|---|---|
| A1 | `course.py doctor`, `blog.py status --mock`, `blog.py run --sample` |
| A2 | `blog.py pages` |
| A3 | `blog.py topics`, `blog.py template approve library --by 서윤` |
| A4 | `blog.py draft`, `blog.py status --costs` |
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

예상 출력 재생성은 `python course/build_expected.py`, 검증은 `python course/build_expected.py --check`입니다. 테스트는 `python -m pip install -r requirements-dev.lock` 후 `python -m pytest -q`로 실행합니다. 저장소의 `bash scripts/repro_blog_advanced.sh`는 빈 폴더와 새 venv에서 전 장과 우회 시도 묶음을 포함한 7종 시나리오를 검사합니다.

설정은 `config.example.toml`을 `config.toml`로 복사해 바꿉니다. 비밀은 `.env`에만 넣습니다. 로컬/실제 WordPress와 키 교체·백업 안내는 [ops/README.md](ops/README.md)를 보세요. mock 서버는 각 명령이 임시 로컬 포트에서 켜고 끕니다.

실연결은 기본 드라이런입니다. 실제 WordPress는 `wordpress.mode=local/live`와 본인 `.env`, 명시적 `--live`가 필요합니다. 쿠팡 live API는 현행 서명·자격·약관 확인 전 비활성입니다. LLM·GA4·GSC 어댑터는 주입된 전송 함수를 모킹 테스트합니다. 자동 관문은 의료·법률 판단이나 사진의 시각 검토를 대신하지 않습니다.

교과서와 키트의 일치 검사는 저장소 루트에서 `python3 scripts/check_blog_advanced.py --check`로 실행합니다. 빈 복사본 재현은 `bash scripts/repro_blog_advanced.sh`, HTML 기본 명령 추출·재현은 `python3.11 scripts/check_blog_advanced.py --check --replay`입니다. A1 맛보기에서 예약한 글은 A6에서 같은 번호로 재사용합니다. 예약 예시 파일은 `report`만 실행하며, 실제 등록·발행은 하지 않습니다.

자동 예약 시연은 별도 연습 복사본에서 틀·데이터 파일을 읽고 위 틀 승인 명령을 실행한 뒤, `publishing.mode="auto"`로 바꾸고 `python blog.py run --sample library`를 실행합니다. 시연이 글별 승인을 만들거나 틀을 스스로 승인하지 않습니다. 가상 편집 목록이며 기관의 실제 선정 목록을 수집한 결과는 아닙니다. 틀·데이터 규칙 파일은 코드와 함께 별도로 보관하고 승인 DB를 복원해도 현재 파일 해시를 다시 검사합니다.
