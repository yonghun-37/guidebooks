너는 ai-insta 프로젝트의 작업자(Codex)다. AGENTS.md, .agents/skills/guidebook-pipeline, **docs/DESIGN-advanced.md(3절 auto-kit)**, research-advanced/(BRIEFING·FACT-SHEET·주제 노트), docs/results/phase-A1.md(조정 제안), 그리고 재사용할 starter-kit/(render·publish·daily·schedule_setup·prepare_hosting·token_check)·shorts-kit/(render·upload·oauth_setup·review)를 읽어라.
이번 작업은 **Phase A2. auto-kit 구현** 이다. `auto-kit/`만 만든다(다른 작업자가 site*/, blog-kit/, research-blog/를 수정 중 — 건드리지 마라. starter-kit/·shorts-kit/는 읽기만, 코드는 복사해 재사용). commit하지 마라. 시스템 패키지 설치 금지(pip 바이너리 사용). **유료 API 키를 쓰지 마라. 모든 외부 호출은 모킹 테스트.**

요구:
- 두 흐름: `insta`(소스 → LLM 카드 문안 JSON → (선택) 이미지 API → 카드 PNG/캐러셀, (선택) 모션 릴스 MP4 → 공개 URL 호스팅 → 승인 → Instagram API 게시 → 인사이트) / `shorts`(주제 → LLM 대본·장면 JSON → TTS API 또는 본인 녹음 → 장면: 이미지/영상 생성 API 또는 소재 폴더 → ffmpeg 조립·자막 → 승인 → YouTube 재개 업로드 → Analytics).
- `providers/`: LLM(OpenAI·Gemini·Anthropic), 이미지, TTS, 영상 — 공통 인터페이스, JSON 스키마 구조화 출력 + 검증·재시도, 호출별 비용 추정 기록과 **일/월 비용 상한**(넘으면 중단·알림), `mock` 공급자. 공급자·모델 이름과 가격표는 config(research-advanced 근거, 날짜 표기)로 분리.
- `pipeline.py run --flow insta|shorts [--provider mock]`: 단계별 상태 저장(SQLite), 실패 단계부터 재시작(`resume`), 콘텐츠 해시로 중복 게시 방지, 실행 로그.
- 운영 모드 `mode: auto|post_review|approval`(DESIGN-advanced 1절). auto = 자동 품질 관문 통과 시 자동 게시, post_review = 예약 게시 후 공개 전 거부 가능, approval = `approve <id>` 후 게시. 디스코드/텔레그램 웹훅 알림(미리보기 첨부).
- `gates/`: 사실 대조(요약 속 숫자·고유명사가 원문에 있는지), 금지어·정책 규칙, 최근 게시물 유사도(중복·반복 콘텐츠), 규격(비율·길이·용량·LUFS), AI 표시 필드, 비용 → 통과/예외 대기열(사유 포함).
- `topics/`: 소스(RSS 등) + 지난 성과 점수로 주제 자동 선정.
- `ops/`: 토큰 자동 갱신(가능한 플랫폼)·만료 경보, 한도·할당량 확인 후 자동 연기, 일일 실행 보고, 정적 HTML 대시보드(실행 이력·관문 결과·비용·지표).
- 게시: Instagram(A1 결론의 권장 API 경로, 컨테이너 생성·상태 폴링·publish·한도 확인·토큰 만료 점검) / YouTube(재개 업로드, privacyStatus 기본 private, publishAt 예약, 아동용·AI 관련 필드는 A1 근거대로). **기본 드라이런**, `--live`는 사용자가 .env/인증 파일을 직접 넣었을 때만. 토큰은 출력·로그 금지, .env는 .gitignore.
- 호스팅: A1 결론의 무료 선택지 1~2개 어댑터 + 로컬 드라이런.
- 실행 예약: Windows 작업 스케줄러·macOS launchd·cron 설치 스크립트, GitHub Actions 워크플로 예시(.github/가 아니라 auto-kit/examples/에 둔다, Secrets 사용법 주석).
- (선택) 노코드: A1에서 고른 도구의 가져오기용 워크플로 JSON 1개(examples/n8n/), 실제 노드 이름은 근거대로.
- `insights.py`: 지표 수집 → CSV(모킹 테스트).
- `doctor.py`: 키·토큰·ffmpeg·한도·비용 상한 설정을 점검하고 무엇이 빠졌는지 한국어로 안내.
- pytest: mock 공급자로 두 흐름 전체, 재시작, 중복 방지, 비용 상한, 드라이런 요청 내용, 모킹 게시·폴링·오류 처리. samples/에 mock 실행 결과(10MB 이하).
- 초보 개발자용 README(Windows/macOS): 설치 → `doctor` → mock 전체 실행 → 키 하나씩 넣어 실제 전환 → 예약 → 운영. 명령마다 "이렇게 보이면 성공", 흔한 오류 표.
- 결과 docs/results/phase-A2.md, `python3 scripts/notify.py "✅ [auto-kit 완료] ..."`.
- **범위**: docs/DESIGN-advanced.md 1.1 — 심화편은 API와 코드만. Canva·미리캔버스·Clipchamp·CapCut 같은 화면 조작 웹 도구는 다루지 않는다(카드는 코드 템플릿, 이미지는 생성 API, 영상은 ffmpeg).
- **전자동·시각자료**: DESIGN-advanced 1절(전자동 목표, 운영 모드 3종)과 1.2절(심화편 시각자료 목록)을 따른다. 심화편은 그림이 핵심이다: 시스템 구성도, 하루 실행 타임라인, API 시퀀스, 상태 흐름, 품질 관문 판정 흐름, 폴더·설정 구조, 비용·할당량 차트, 대시보드·알림 예시를 내용에 맞게 적극적으로 쓴다(직접 그린 SVG, 라이트/다크).
