# Phase A2 결과 — auto-kit 구현

2026-10-26 · Codex. **키트 구현·오프라인/모킹 검증 완료, Claude 최종 검수 대기. 실계정 게시·유료 생성·OS 실기기 성공을 뜻하지 않는다.**

## 작업 범위

- `auto-kit/`를 새로 작성했다. 요청한 본 결과 문서만 키트 바깥에 추가했다.
- AGENTS, pipeline·구현·검증 스킬, DESIGN-advanced 1·3·6절, A1 결과·브리핑·사실표·주제 노트, 기존 render/publish/daily/schedule/hosting/token/OAuth/review 코드를 읽고 재사용했다.
- starter-kit·shorts-kit는 읽기/코드 복사에만 사용했다. site*·blog-kit·research-blog·공통 설계·공통 상태·다른 작업자의 변경은 수정/되돌리지 않았다. 진행 중 다른 작업자가 기존 키트 파일을 수정한 흔적도 그대로 보존했다.
- commit/push·시스템 패키지 설치·계정 로그인·게시·유료 키 사용은 하지 않았다. `/tmp` 가상환경에 pip 바이너리 의존성을 설치했다. 완료 보고는 사용자 지시에 따른 별도 Discord 알림이다.

## 구현된 기능

| 영역 | 실제 구현 |
|---|---|
| 두 흐름 | insta: 소스→구조화 문안→선택 이미지/영상→PNG/JPEG/릴스→호스팅→관문→승인/예약→컨테이너 발행→지표. shorts: 소스→대본/장면→TTS/녹음→소재/생성 장면→MP4/SRT/음량→관문→승인/예약→재개 업로드→분석 |
| 공급자 | mock, OpenAI·Gemini·Anthropic LLM, Gemini 이미지, Google TTS, Runway 영상. 공통 draft/media/check 인터페이스·JSON Schema 검증·제한 재시도. 모델·단가·기준일은 config/prices 분리 |
| 비용 | 생성 전에 실행 최대비 예약, 모든 호출·재시도 비용을 원자적으로 그 안에서 예약/정산. UTC 일·월 상한·사용량 기록·불명/usage 누락 보수 유지·초과 중단/알림. 진행 중 영상 task의 비용 ticket 재사용 |
| 상태·재개 | SQLite/WAL·OS 실행 잠금·단계 체크포인트·실행 로그. 파일/문안 해시·계정/flow/드라이런-live 분리 중복 차단. 발행 불명은 기존 컨테이너/세션 조회, 새 게시 금지 |
| 운영 모드 | auto / post_review / approval. 기본 approval+dry-run. 승인에 파일·문안·실제 채널/계정·공개범위·AI·예약·비용 결합. 변경/만료 재검증. Instagram 로컬 지연 발행, YouTube private+publishAt 및 공개 전 거부/삭제 |
| 관문 | 숫자·이름 문자열 대조, 금지/민감 단어, 문자 4-gram Jaccard, JPEG/MP4 비율·길이·코덱·fps·용량, ffprobe 또는 pip ffmpeg 검사, loudnorm 실측, Boolean AI/아동용, 비용. 실패 이유 포함 예외 대기열. 선택 두 번째 LLM 원문 대조 |
| 소스·성과 | 직접 입력·RSS/Atom, 사용자 feed별 권리 확인, 소스 순서+이전 지표 점수, 이미 처리한 원문 제외. tick이 최근 완료 게시물을 매일 재수집해 지연 지표를 다음 주제에 반영 |
| Instagram | Instagram Login v26.0, JPEG/캐러셀/릴스, 생성·상태 폴링·부모 발행, 실제 content_publishing_limit, 50/100 임의 fallback 없음, 토큰 수명/갱신. 결과 불명 기존 게시 ID reconcile |
| YouTube | private 기본·publishAt·selfDeclaredMadeForKids·containsSyntheticMedia. Location/청크/308 Range 재개·서버 상태 조회. 실제 OAuth 채널 ID 승인 결합. Console 확인 로컬 cap+API quota 거절 연기, Pacific 날짜 카운터 |
| 호스팅 | 로컬 드라이런, 별도 교육용 Pages branch API, R2 S3. JPEG/MP4만 허용·용량 상한·인증 없는 공개 GET/MIME/파일 해시 검증 |
| 알림·운영 | 로컬 파일, Discord webhook 미리보기 첨부, Telegram 미리보기/inline 버튼·허용 사용자/chat/hash/offset 검증. 토큰 갱신·Testing 만료 경보, 자동 연기, 일일 보고·HTML 비용 막대/quota 게이지/관문/지표 |
| 예약·외부 상태 | Windows PowerShell 작업 스케줄러·macOS launchd·cron 설치 파일 생성. 15분 tick·현지 날짜 하루 생성 선점. Actions 예시는 examples/에만 존재. Fernet 암호화 private 백업·원자적 R2 lease·보존 실패 후 다음 실행 차단·Windows→Linux 경로 복원 |
| 초보자 안내 | Windows/macOS 설치→doctor→mock→승인→키/인증별 전환→예약→운영. 명령 성공 표시·흔한 오류·범위 구분. n8n 실제 Schedule Trigger/Execute Command를 쓰는 비활성 mock 가져오기 예시 |

## 산출물과 재사용

- [README](../../auto-kit/README.md), [구현 계획·결정](../../auto-kit/docs/plan.md), [추가 공식 근거·기본값·재사용 기록](../../auto-kit/docs/sources.md).
- [실행기](../../auto-kit/pipeline.py), [doctor](../../auto-kit/doctor.py), [구조화 공급자](../../auto-kit/providers/__init__.py), [상태/비용](../../auto-kit/state.py), [지표](../../auto-kit/insights.py).
- 렌더·재개 프로토콜은 starter-kit/render_cards.py, shorts-kit/render.py·upload.py에서 복사·수정했다. MIT 및 폰트 OFL을 보존했다. FFmpeg 바이너리는 저장소에 넣지 않았다.
- [그림 모음](../../auto-kit/docs/figures.html): 시스템·하루 타임라인·API 시퀀스·상태·관문·폴더/설정·비용/한도·대시보드/알림, **8종×라이트/다크 16 SVG**. Python 스크립트로 재생성 가능.
- [공개 mock 샘플](../../auto-kit/samples/README.md): 카드 PNG/JPEG, MP4/SRT, 요청 계획·관문·CSV·알림·대시보드. **496,054 bytes, 10MB 이하**. DB/토큰/개인 세션은 제외했다.

## 검증

| 검사 | 실제 결과 |
|---|---|
| pytest 전체 | **64 passed**. 각 테스트에서 실제 socket 연결 차단 |
| 두 흐름 | mock 전체 완주, 승인/재개/드라이런. live 코드 조립도 생성·인증·호스팅·게시·분석 외부 경계를 전부 모킹 |
| 게시·비용 회귀 | 308·유실 후 같은 세션, 시작 불명 새 insert 금지, Instagram 폴링/오류/한도/발행 불명, 변경 승인·중복 차단, 일/월/동시 예산·실행 예약 정산, schema 재시도·usage 누락, Pages/R2 모킹 업로드·공개 MIME/바이트 대조 |
| 운영 회귀 | Telegram 허용 사용자/chat/hash/offset, 토큰 갱신, 실제 채널 교체 차단, 예약 취소 scope, 현지 날짜 생성 1회, 완료 지표 재수집, Windows 경로 복원, 암호화·미완료 lease로 후속 실행 차단 |
| 깨끗한 복사본 | README 오프라인 명령 **15개** 성공. doctor·두 흐름·승인/재개·지표·보고·3 OS 예약 생성·tick 반복, 쉘 설치 스크립트 `sh -n` 확인 |
| 로컬 링크 | **69개**, 오류 **0개**. README·원본 SVG·그림/샘플 HTML 포함 |
| Chromium | 4개 로컬 HTML×3폭(1280/375/360)×2테마+16 SVG, **40개 검사**. 뷰포트 넘침·깨진 이미지·SVG 노드 글자 넘침·page error **0개** |
| 로컬 미디어 | 실제 Pillow 카드, H.264/AAC MP4·SRT, loudnorm 측정/보정. pip ffmpeg filter 도움말 exit 0. 공식 FFmpeg 페이지 열람 시간 초과는 근거 문서에 별도 기록 |
| 공개 파일 안전성 | credential 패턴 검사 **0개**, 공개 대상 .env/DB/토큰/업로드 세션 **0개**. compileall 통과 |

재현 명령: `python -m pytest -q auto-kit/tests`, `python auto-kit/tests/check_readme.py`. 브라우저 재현은 tests/check_visuals.cjs에서 `PLAYWRIGHT_MODULE`, `CHROMIUM_PATH`로 사용자 설치 경로를 지정한다. 명령별 결과는 [commands.json](../../auto-kit/docs/verification/commands.json), 화면은 [라이트](../../auto-kit/docs/verification/figures-light.png)·[다크](../../auto-kit/docs/verification/figures-dark.png)에 있다.

## 독립 검토와 수정

`superpowers:requesting-code-review`에 따라 독립 검토자를 사용했다. Critical 0, Important 6개를 받고 모두 수정·회귀 검증했다.

1. YouTube 설정 account만 hash에 들어가던 문제 → 실제 OAuth 채널 ID를 처음/발행/취소 직전에 대조.
2. approval/auto의 publishAt 예약에 삭제 scope 누락 → 모든 예약 설정에 force-ssl 요구.
3. UTC daily key와 현지 예약 시각 혼용 → 현지 날짜 key·원자적 하루 선점.
4. Windows 상태의 Linux 복원 실패 → PureWindowsPath·상대 파일 binding.
5. 지표가 업로드 직후 1회로 끝남 → tick의 최근 완료 게시물 일일 재수집.
6. 원격 상태 push 실패 후 오래된 상태로 중복 게시 가능 → 게시 작업 전 외부 conditional lease, 저장 성공 후만 해제.

Minor 3개도 반영했다: 토큰 검사 문자열 오탐을 고유 sentinel로 수정, RSS 명시 권리 확인 설정, 진행 중 영상 task 비용 예약 재사용. 독립 검토 뒤 같은 검토를 반복하지 않고 작성자가 회귀 테스트와 전체 검사를 실행했다.

## 남은 사용자 검증과 한계

- **Windows/macOS 실제 설치·다음 날 실행·절전/로그인 조건·PowerShell 정책**, Actions 배포·예약과 n8n import/노드 허용은 실환경 검증 전이다.
- **사용자 실계정 OAuth/토큰 갱신·Instagram 한도 실응답/게시 가시성·YouTube private 잠금/예약/취소·Analytics·호스팅 실공개·한국어 TTS 발음·유료 모델 접근/청구**는 실행하지 않았다. private 1편 또는 본인 소량 시험부터 확인한다.
- 자동 사실 대조는 문맥/모든 한국어 인명/저작권의 완전 검증이 아니다. 자막은 장면 시간 배분이며 강제 음성 정렬이 아니다. 임계값은 키트 기본값임을 config·README에 표시했다.
- 이미지 실제 청구 토큰의 전체 가격 조합이 확인되지 않으면 최대 예약액을 유지한다. 세금·구독·호스팅·전기는 생성 비용 상한 밖이므로 공급자/클라우드 상한도 별도 확인한다.
- 상태 보존 실패·강제 취소로 lease가 남으면 최신 DB/발행 ID 복구가 필요하다. 오래된 snapshot으로 우회하지 않는다. 상태 묶음은 기본 256MiB 상한이다.
- 확정 설계의 구현 단계를 넘어 site*/advanced 집필·공통 배포/서가 상태를 수정하지 않았다. **통합 작업자는 PROJECT_STATE에 A2 구현/모킹 완료와 실계정·OS 검증 대기를 반영하면 된다.**

## 완료 알림

요청된 `python3 scripts/notify.py "✅ [auto-kit 완료] ..."`를 실행해 **HTTP 200 전송 성공**을 확인했다. 두 흐름·산출물·pytest 64개/명령 15개/브라우저 40개·사용자 실환경 검증 대기를 한국어 4줄로 보고했다. 토큰은 출력하거나 결과에 넣지 않았다.

## A2b 수정

2026-10-26 · Codex. Claude 검수의 예시·Python 버전 불일치를 수정했다. 수정 범위는 `auto-kit/`와 요청한 이 절뿐이다. `site-blog/`와 다른 작업자의 파일·공통 상태 문서는 건드리지 않았고 commit/push하지 않았다.

### 바뀐 내용

- 하린의 가상 계정 **출근길 3분 생활 뉴스**는 **청년 지원금, 신청 전 확인할 3가지**를 카드 5장으로 만든다. 대상·기간·서류 확인을 원문→문안→카드→요청 계획까지 연결했다. 실제 제도명·금액·마감일은 만들지 않았고 직접 작성한 예시 문안임을 표시했다.
- 도윤의 가상 채널 **자취생 10분 생존법**은 **월급날 10분, 돈을 네 칸으로 나누기**를 36초 장면으로 만든다. 월세·생활비·비상금·목표를 끝까지 이어 쓰며 10분은 메모 활동 시간이다. 배분 비율·절약액·수익을 만들지 않았다. mock 신호음은 장면 길이에 맞추며 실제 낭독이 아님을 안내한다.
- `sources/sample.json`과 동등한 두 RSS 픽스처(`insta-feed.xml`, `shorts-feed.xml`)를 동봉했다. 소스·피드의 선택적 `flow`로 흐름을 고르며, 이 값이 없는 사용자 소스는 기존처럼 공용이다. mock은 원문 첫 줄과 `항목: 설명`에서 장면을 만든다. `synthetic: true`·권리 미확인에 따른 live 차단을 유지한다.
- README·샘플 안내·공개 원문/초안·PNG/JPEG·MP4/SRT·관문·요청 계획·알림·CSV·대시보드와 SVG 생성 원본/라이트·다크 도식의 예문을 갱신했다. 도식에도 원문 확인과 잘못 추가한 금액의 실패를 연결했다. 샘플 CSV 줄 끝은 LF로 내보낸다.
- 최소 **Python 3.11**로 README·구현 계획·doctor·오류 표를 통일했다. Windows는 `py -3.11`, macOS는 `python3.11`로 가상환경을 만든다. doctor는 버전 검사 뒤에 ffmpeg 의존성을 읽어 3.10에서도 버전 오류를 먼저 안내한다.
- README의 RSS 실행에는 `--config config.json`, 지표 조회에는 해당 승인 연습의 `--state`를 명시했다. tick 연습도 별도 상태를 사용해 앞서 소비한 샘플 원문과 충돌하지 않게 했다. 성공 문구는 실제 상태/출력과 대조했다.

### 실행·검증

`/tmp/a2b-clean-ozfn8f4d/auto-kit`의 깨끗한 복사본에서 Python **3.11.15**로 새 `.venv`를 만들고 README의 `--only-binary=:all: -r requirements-dev.txt` 설치를 성공했다. Linux에서 명령과 미디어를 검사했으며 Windows/macOS 실기기 설치·예약 등록은 수행하지 않았다.

| 검사 | 실제 결과 |
|---|---|
| pytest 전체 | **75 passed in 44.58s**. 기존 64개와 새 회귀 검사 11개. 실제 socket 연결 차단 유지 |
| 사실 대조 | 두 흐름 각각 정상 원문 통과·원문에 없는 `99` 추가 실패, **4 passed**. 추가 파이프라인 검사에서 잘못된 지원금 문안은 예외 대기열에 이유를 남기고 발행/승인 우회 차단 |
| 주제/RSS | 흐름별 JSON·RSS 원문/해시/mock 출력 일치, synthetic·권리 상태 보존, flow 생략 시 공용 소스 호환 확인 |
| Python 버전 | 3.10/3.11/3.12 경계 검사. 실제 **3.10.12**의 `python3 auto-kit/doctor.py`도 최소 버전·새 가상환경 안내 출력 후 **exit 1** |
| README 명령 | 별도 깨끗한 임시 복사본에서 **21개** 예상대로 동작. doctor live 설정 미비는 예상한 exit 1이며 원격 호출 없음. 승인/재개·사후 거부·두 RSS 흐름·예약 파일·tick 반복·지표·암호화 키 파일 생성 포함 |
| 로컬 링크·브라우저 | 링크 **75개**, 오류 **0**. 새 샘플 4 HTML×3폭(1280/375/360)×2테마 및 16 SVG, **40개 검사 통과**, 가로/글자 넘침·이미지 실패·page error 0 |
| 공개 샘플 | Python 3.11 임시 복사본에서 재생성. 전체 **1,587,276바이트**, 10MB 이하. 카드 5장 **1080×1350**, 쇼츠 **1080×1920·30fps·H.264/AAC·약 36.1초·-16.05 LUFS**, 전체 디코딩 성공. 초안과 mock 원문 출력 일치 확인 |
| 잔여 예시·공백 | 가상도서관·책 12권·가상공원·옛 Python 3.10 요구 문구 검색 **0건**. `git diff --check` 통과 |

검증 기록: [통합 수치·사실 대조](../../auto-kit/docs/verification/a2b.json), [전체 pytest](../../auto-kit/docs/verification/pytest.txt), [명령별 실제 출력](../../auto-kit/docs/verification/commands.json), [새 라이트 화면](../../auto-kit/docs/verification/figures-light.png)·[다크 화면](../../auto-kit/docs/verification/figures-dark.png). 카드 표지·마무리와 쇼츠의 추출 프레임도 직접 열어 확인했다.

생성·호스팅·게시 API의 실제 호출, 실계정 로그인·게시, 유료 키 사용은 하지 않았다. Claude 최종 검수와 기존 A2의 사용자 실환경 확인은 남아 있다.

요청한 `python3 scripts/notify.py "✅ [A2b 완료] auto-kit 예시·Python 버전 수정 ..."`를 실행해 **HTTP 200** 전송 성공을 확인했다.
