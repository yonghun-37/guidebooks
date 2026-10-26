# 검증 재현

저장소 루트에서 실행한다. 사이트 스크립트는 이 환경의 기존 Playwright 설치와 Chromium 경로를 사용한다. 실제 서비스·OS 앱 조작이 아닌 Linux Chromium 검사다.

```bash
python3 scripts/style_lint.py site-shorts/practice/*.html --output docs/results/phase-Y4p/style-lint.json
python3 scripts/check_site.py --site site-shorts --output docs/results/phase-Y4p/static-check.json
node --check site-shorts/practice/production.js
git diff --check
python3 -m http.server 8594 --bind 127.0.0.1 --directory /home/yonghun/project/ai-insta
# 다른 터미널
node docs/results/phase-Y4p/verify-browser.mjs
```

954개 브라우저 확인: 12페이지 × 1280/375/360px × 라이트/다크, 실제 고정 CDN 글꼴, 접힌 FAQ/OS 탭을 펼친 후 넘침, Enter·Space·방향키·Home·End, 프롬프트 실제 클립보드 복사, 자막 끝 복구·극단 예·프레임·반복, 체크와 주소의 양방향 저장·복원, 217개 링크와 앵커, 저장 차단 대안을 포함한다. URL 입력 시험은 example.org의 더미 문자열이며 실제 게시 주소가 아니다.

## 깨끗한 키트 복사본

`/tmp/shorts-y4p-*/한글 공백/shorts-kit`에 기존 가상환경·출력·입력·비공개 파일·실제 설정을 제외하고 복사했다. Python 3.11.15의 새 가상환경에 README대로 requirements를 설치했다.

```bash
python3.11 --version
python3.11 -m venv .venv
.venv/bin/python -m pip install -r requirements.txt
.venv/bin/python run_pipeline.py run --output output/first
.venv/bin/python run_pipeline.py run --mode prompt --output output/my-script
# 사용자 파일 저장 단계에 해당하는 검증용 script.json 작성 후
.venv/bin/python run_pipeline.py validate output/my-script
.venv/bin/python run_pipeline.py render output/my-script
# config.example.yaml 복사 → 합성 톤 M4A와 장면 파일·권리 메모 지정 후
.venv/bin/python run_pipeline.py render output/my-script --config config.yaml
# 두 공개 판단을 false로 정한 검증용 대본을 저장한 후
.venv/bin/python run_pipeline.py render output/my-script
# REVIEW.md 여섯 항목 직접 검수·체크 후
.venv/bin/python run_pipeline.py approve output/my-script
.venv/bin/python upload.py output/my-script
.venv/bin/python -m pip install -r requirements-live.txt
.venv/bin/python oauth_setup.py --help
.venv/bin/python upload.py --help
```

처음에는 `영상 생성 완료`, `검수 대기`, `미리보기`와 실제 경로가 나왔다. validate는 `대본 형식 확인 완료. 사실·권리·자막 시점은 직접 검수하세요.`를 출력했다. approve는 승인 기록과 전송 없는 드라이런을 만들었고 upload 기본값 역시 `network_calls: 0`이다.

prompt 모드 직후 script.json을 저장하지 않은 상태의 validate가 파일 누락으로 멈추는 것도 확인했다. 본문은 저장 단계를 반드시 거치게 한다. 이후 정상 명령·실제 출력은 `kit-commands.json`, 실제 영상 정보는 `kit-video-info.json`에 있다. 원래 첫 설치·생성의 터미널 출력은 세션에서 확인했으며 별도 stdout 전문 파일을 만들지 않았다.

음성 입력은 **실제 사람 녹음이 아니라 합성 톤을 M4A로 인코딩한 검증 파일**이다. 장면은 이번에 생성한 종이 로봇 그림 사본이다. 대본 수정·장면 수에 맞춘 입력·M4A 디코딩·출력·재검수 흐름을 확인했다. 실제 TTS 서비스 가입/생성이나 녹음 품질·낭독 동기화 실험으로 세지 않는다.

`verify-kit-browser.mjs`는 `/tmp/y4p-kit-path`에 기록된 복사본을 연다. MP4 실제 재생·치수·중간 탐색·마지막 재생·세 폭 넘침·오류를 확인한다. 복사본이 삭제되면 같은 절차로 새 경로를 기록한 뒤 실행한다. 파일 탐색기로 열어도 결과 폴더의 `preview.html`을 볼 수 있다.

Windows/macOS의 경로 표기는 해당 OS 안내다. 이 환경에서 실제 실행한 명령은 Linux의 `.venv/bin/python`이며 실기기 OS 검증을 완료했다고 쓰지 않는다. `oauth_setup.py`의 실제 인증과 `upload.py --live`는 실행하지 않았다.
