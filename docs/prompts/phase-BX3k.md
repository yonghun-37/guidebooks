너는 ai-insta 프로젝트의 작업자(Codex)다. AGENTS.md, .agents/skills/guidebook-pipeline, docs/STYLE-GUIDE.md, **docs/DESIGN-blog-advanced.md(이번 설계 전체, 특히 1.1 위험 등급·1.2 재현성/가독성 약속·4절 키트 구조·6절 규칙)**, docs/DESIGN-baby.md 8절, **research-blog-advanced/BRIEFING.md(④ 관문 규칙·⑤ 협찬 대장·⑥ 대가성 문구·③ 발행 경로)**와 FACT-SHEET.md, **DESIGN-blog-advanced.md 8절(조사 반영, 3절·4절보다 우선)**을 읽어라. 8절의 검증 시나리오 6종(mock 정상/규제 품목 거절/자료 보류/승인 후 수정 재승인/시간 초과 중복 방지/백업 복구)을 pytest와 repro 스크립트 양쪽에 넣는다. 참고로 blog-kit/과 auto-kit/의 구조(해시 승인, 상태 저장, 알림, 예약 생성기, 드라이런)를 읽되 **import하거나 수정하지 말고** 새 폴더에 짧게 새로 구현한다.

이번 작업은 **Phase BX3k. blog-auto-kit 구현**이다. 새 폴더 `blog-auto-kit/`와 `scripts/repro_blog_advanced.sh`, `docs/results/phase-BX3k.md`만 만든다. 다른 파일은 수정하지 마라. commit하지 마라. 실계정 로그인·유료 키·실제 발행은 하지 않는다.

## 1. 가장 중요한 두 가지
**재현 가능**
- Python 3.11+ 표준 라이브러리만으로 mock 전 과정이 끝나야 한다. 외부 패키지는 정말 필요할 때만 `requirements.lock`(정확한 버전)에, 테스트용은 `requirements-dev.lock`(pytest 고정 버전).
- 고정 시계: 기본 `--today 2026-10-27`, 고정 시드. ID·날짜·해시·출력 파일이 실행마다 바이트 단위로 같다(실행 시간·절대 경로를 출력 파일에 넣지 않는다).
- mock WordPress 서버(`wordpress/mock_server.py`, http.server): 실제 WordPress REST의 쓰는 부분만 흉내 — `/wp-json/wp/v2/posts`(GET/POST, status draft/future/publish, date, slug 충돌 시 실제처럼 접미사), `/media`, `/categories`, `/tags`, Basic 인증(애플리케이션 비밀번호 형식) 확인, 잘못된 인증 401 응답 본문은 실제 WordPress 오류 형식(`code`, `message`, `data.status`)과 같게. 상태는 `private/mock-wp/` JSON. 클라이언트는 mock과 실제 WordPress를 **같은 코드**로 부른다(주소만 다름).
- `ops/docker-compose.yml`: 실제 WordPress·DB 이미지(태그 고정, BRIEFING ③ 근거) + 로컬에서 애플리케이션 비밀번호를 쓰는 방법 안내. 이 환경에서 Docker가 되면 한 번 실제로 띄워 REST 발행을 확인하고, 안 되면 "미실행"으로 결과에 적는다.
- `course.py`: `doctor`(Python 버전·폴더·포트·쓰기 권한·시계), `start <장>`(그 장 시작 상태를 만든다: 앞 장 산출물을 course/states/에서 복원), `check <장>`(그 장의 산출물·상태·출력 비교, 다르면 무엇이 어떻게 다른지 한국어 한두 줄 + 고치는 명령), `reset`. A1~A12 모두.
- `course/expected/<장>/`: 본문에 넣을 명령별 예상 출력(터미널 텍스트)과 산출물 해시. 생성 스크립트 `course/build_expected.py`로 만들고 `--check`로 현재 출력과 비교한다.
- `scripts/repro_blog_advanced.sh`: 임시 빈 폴더에 blog-auto-kit만 복사 → 새 venv → (dev lock 설치) → `course/commands.md`에 있는 장별 명령을 순서대로 실행 → 각 장 `course.py check` → pytest. 마지막 줄에 통과/실패 요약. 이 스크립트가 통과해야 완료다. Python 3.11과 3.12가 있으면 둘 다.
- `course/commands.md`: 장별 명령 목록(본문이 그대로 가져다 쓴다). Windows PowerShell 표기와 macOS/Linux 표기를 나란히.

**가독성**
- 파일 하나 = 개념 하나, 파일당 200줄 이하, 함수 40줄 이하. 함수 이름은 하는 일 그대로. 모듈 맨 위 한국어 docstring 한 줄(무엇을 하는 파일인지).
- 진입점은 `blog.py` 하나: `blog.py topics | draft | gate | publish | pages | ads | affiliate | sponsor ... | report | run | status`. `--help`가 한국어로 장 번호와 함께 보인다.
- 설정 `config.example.toml`(tomllib로 읽기, 항목마다 한국어 주석), 비밀은 `.env`만(.gitignore). 설정 오류는 "어느 줄, 무엇이 잘못, 어떻게 고치나"로 출력.
- 출력은 짧고 일관되게: `✔ 통과`, `✖ 막힘: <이유> → <고치는 방법>`, 생성 파일 경로.

## 2. 기능 (DESIGN 4절 구조 그대로)
- core/: 설정, SQLite 상태(글·실행·협찬·링크), 콘텐츠 해시, 고정 시계, 로그.
- content/: 주제 지도(월령·발달·제도·놀이·그림책), 글 유형 4종 JSON Schema(정보/놀이·교육/제휴 비교/협찬 후기 — `experience`·`photos`는 사람 칸), 출처 노트 형식, 마크다운→HTML(표준 라이브러리 수준의 단순 변환).
- providers/: mock LLM(고정 JSON) + 실제 공급자 1개(BRIEFING의 현재 권장, 구조화 출력) 어댑터는 모킹 테스트만. 비용 기록·월 상한.
- gates/: BRIEFING ④의 규칙을 그대로 구현 — health_safety(금지 표현·약 이름/용량 패턴·응급 문구는 BabyBook `site-baby/assets/emergency-data.js` 공통 문구를 **복사본**으로 넣고 출처 표시), child_privacy(이름·생일·병원·어린이집·위치 패턴, 이미지 EXIF 위치·기기 정보 탐지·제거), disclosure(제휴·협찬 글의 문구·위치), product_rules(영유아 제품 금지·주의 목록), duplicate(최근 글 유사도), seo(제목·설명·소제목·대체 텍스트), sources(숫자 문장에 출처). 결과는 통과/예외 대기열 + 사람이 읽는 보고서. 위험 등급별 운영 모드(DESIGN 1.1 표)를 코드로 강제: 건강·협찬·아이 사진 글은 어떤 설정에서도 자동 발행되지 않는다(테스트로 증명).
- wordpress/: REST 클라이언트(초안→예약, 미디어 업로드, 카테고리·태그 자동 생성, 콘텐츠 해시로 중복 방지, 결과 불명 시 slug로 기존 글 조회 후 재시도 금지).
- monetize/pages: 소개·개인정보처리방침(문의 폼 수집 항목 기준)·문의·광고/협찬 정책 페이지 생성. ads: 신청 준비 점검표(근거 있는 조건만), ads.txt 생성(게시자 ID 자리표시), 광고 위치 템플릿(본문 n번째 소제목 뒤 등 설정), 광고 보고서 mock 수집. affiliate: 링크 등록부(CSV), 대가성 문구 자동 삽입(BRIEFING ⑥ 원문), 링크 점검(mock), 쿠팡 파트너스 API 어댑터는 모킹 테스트만(서명 방식은 공식 문서 근거, 근거가 없으면 만들지 말고 결과에 적기). sponsor: 협찬 대장 상태 기계(`states.py` 표 하나 — 문의→검토→수락/거절→계약→제품 수령→작성→광고주 확인→발행→성과 보고→정산, 각 전이의 필수 기록), 거절 기준 자동 판정(안전 수면 충돌·규제 품목·표시 거부 조건), 미디어킷 HTML(지표 → 표, 아이 정보 비노출), 광고주 결과 보고서, 세금 기록 CSV(받은 물품·금액·날짜, 판단은 세무 안내 링크로).
- analytics/: mock 지표(고정 데이터) + GA4 Data API·Search Console API 어댑터(모킹 테스트), 주간 보고서 HTML, 다음 글감 점수, 갱신 대상 글(금액·날짜가 들어간 글의 기준일 경과).
- ops/: 디스코드·텔레그램 알림(드라이런 기본), 백업(SQLite+mock WP 상태+설정 → zip)·복구, 예약 실행 생성기(작업 스케줄러·cron·launchd 명령 출력만, 등록은 사용자가), GitHub Actions 예시(상태를 runner 밖에 두는 방법 주석).
- samples/: 「봄이랑 크는 집」 글 4편(정보: 2026 부모급여·아동수당 — research-baby 금액·기준일 그대로 / 놀이: 3~4개월 터미타임 — 공식 권고 범위만 / 제휴 비교: 손톱깎이 vs 전동 손톱갈이 — 가상 제품 / 협찬: 「포근담요」 낮잠 이불 거절 사례와 「도담」 그림책 꽂이 수락 사례 전 과정). 사람 경험 메모, 직접 그린 그림(Pillow 없이도 되게 SVG/PNG 고정 파일), EXIF 시연용 가짜 위치 정보 JPEG(표준 라이브러리로 바이트 생성).
- tests/: 모든 외부 호출 모킹. 장별 체크포인트, 위험 등급 강제, 협찬 상태 전이, 관문 각 규칙의 통과/막힘 예, mock 서버 왕복, 중복 발행 방지, 고정 출력 바이트 동일성.
- README.md: "시작 3단계"(설치 → doctor → `blog.py run --sample` 결과 확인)와 장별 명령 색인. 본문이 길어지지 않게 자세한 설명은 교과서에 맡긴다.

## 3. 결과
docs/results/phase-BX3k.md: 파일 트리(줄 수 표시, 200줄 초과 0), 장별 명령과 예상 출력 요약, repro 스크립트 결과 원문 끝 30줄, pytest 결과, Docker 실행 여부, 근거가 부족해 구현하지 않은 것, 집필 작업자에게 주는 "장별로 본문에 넣을 명령·발췌 후보(파일:줄)" 표.
`python3 scripts/notify.py "✅ [blog-auto-kit 완료] ..."`로 한국어 보고(5줄 이내).
