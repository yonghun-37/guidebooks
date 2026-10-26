너는 ai-insta 프로젝트의 작업자(Codex)다. AGENTS.md, docs/DESIGN.md, docs/PLAN.md, research/FACT-SHEET.md, research/ai-video-voice-tools.md, research/ai-text-image-tools.md, research/graph-api-publishing.md를 읽어라.
이번 작업은 docs/PLAN.md의 **Phase 4. 스타터 키트** 만이다. 사이트 파일(site/)은 다른 작업자가 동시에 수정 중이니 건드리지 마라.

1. DESIGN.md 6절대로 starter-kit/을 구현한다. 도구 선택은 research 노트의 무료·상업 이용 가능 경로를 따르고, 선택 이유와 라이선스를 starter-kit/README.md에 적는다.
2. 오프라인 모드(외부 API·키 없음)로 끝까지 실행되어야 한다: 예제 RSS 대신 동봉한 샘플 피드 파일(합성 데이터, 합성임을 표시)로도 동작하게 하라. TTS도 오프라인 대안(예: 시스템/오픈소스 TTS, 불가하면 무음+자막 모드)을 둔다. 폰트는 오픈 라이선스 한국어 폰트를 쓰고 라이선스를 기록한다.
3. publish.py는 기본 드라이런: 실제 호출 대신 보낼 요청(엔드포인트, 파라미터, 순서: 컨테이너 생성→상태 확인→게시)을 출력한다. 실제 업로드는 `--live`와 환경변수 토큰이 모두 있을 때만. 이번 작업에서 live 실행은 하지 마라.
4. run_pipeline.py는 소재 수집→문안→카드 PNG→릴스 MP4→검수 대기(사람이 output/<날짜>/REVIEW.md 확인 후 approve 명령)→드라이런 게시 순서로 동작한다.
5. tests/(pytest)에 오프라인 전체 실행, 카드 크기 1080x1350, 릴스 1080x1920·길이 범위, 드라이런 출력 검증을 넣고 통과시킨다. 의존성 설치는 starter-kit/.venv 등 저장소 안에서만 한다. 시스템 패키지(ffmpeg 등)가 없으면 설치를 시도하지 말고 확인 결과를 기록한 뒤 대안(imageio-ffmpeg 등 pip 바이너리)을 쓴다.
6. starter-kit/samples/ 에 오프라인 모드로 실제 생성한 카드 PNG 세트와 릴스 MP4를 저장한다(용량 10MB 이하).
7. README.md는 완전 초보 기준: 터미널 여는 법, Python 설치 확인, 설치 명령(Windows/macOS/Linux), 첫 실행, 결과 확인, 흔한 오류 표.
8. docs/results/phase-4.md 를 쓴다(commit은 하지 않는다, Claude가 한다). docs/PROJECT_STATE.md와 research/는 다른 작업자가 수정 중이니 건드리지 마라. notify로 보고하며 샘플 카드 PNG 1장을 첨부한다.
