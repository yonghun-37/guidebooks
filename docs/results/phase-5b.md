# Phase 5b 결과 — 6·7·8·9장 집필

2026-10-26. 담당 네 장의 원고·시뮬레이터·실습 검증을 완료했다. 공통 파일은 수정하지 않았으며 공개 상태·용어집 등의 통합은 [별도 요청](phase-5b-requests.md)에 남겼다. 사용자 지정 Phase 5b 범위가 PLAN의 과거 분할보다 우선한다. 기존 `docs/results/` 기록 관례를 재사용해 요구·방법·진행·결과를 이 문서에 모았고 별도 specs·ADR은 만들지 않았다.

## 요구와 구현 전략

초보자가 5장의 출처 메모 → 6장의 프롬프트·문안 → 7장의 카드 → 8장의 릴스 → 9장의 통합 생성·사람 검수를 이어 가도록 구성했다. 장 번호·제목·결과물은 `book.js`와 DESIGN 5·9절을 따랐다. 제안 slug `06-ai-writing` 대신 실제 데이터의 `06-writing`을 사용했다.

공통 9블록과 기존 퀴즈·체크 저장·복사 버튼을 재사용했다. 각 장은 클릭 가능한 흐름도와 핵심 모형을 하나씩 갖춘다. 모형은 공통 `ReelsSim.mount`·`buttonGroup`을 사용하며 외부 호출이 없다. 정책·가격·권리 설명에는 기존 사실 ID와 출처 번호·원문 URL·조사 기준일을 연결하고, 미확인·간접 확인을 본문에 구분했다. 과장 수치나 새 성공 공식을 도입하지 않았다.

- [x] 필수 자료·관련 구현·기존 작업 상태 확인
- [x] 담당 HTML 4개, 장별 9블록·퀴즈 4문항·상단 결과물/시간/난이도/선행 장
- [x] 장마다 모형 2개, 텍스트 결과·키보드·가정 공개·무너뜨리기 프리셋
- [x] 키트 실습 CLI 실행, API 차단/모의 계약·음원 입력·승인 변경 감지 확인
- [x] 1280px·375px, 링크·앵커·콘솔·가로 넘침·퀴즈·키보드·체크 저장 확인
- [x] 결과 증거·스크린샷 2장·공통 변경 요청·새 용어 표 작성
- [ ] 공통 장 상태·모바일 용어 설명·용어집 통합 검수 — 공유 파일 담당자 범위

## 산출물과 연결

| 장 | 본문 | 별도 JS | 구현한 학습 도구 |
|---|---|---|---|
| 6 | [06-writing](../../site/chapters/06-writing.html) | [ch6-writing.js](../../site/assets/sim/ch6-writing.js) | 원자료→지시→전체 JSON→대조 흐름도, 프롬프트 요소 조립·누락 경고 |
| 7 | [07-cards](../../site/chapters/07-cards.html) | [ch7-cards.js](../../site/assets/sim/ch7-cards.js) | 카드 역할 흐름도, 글자 수·크기·실제 색 대비에 따른 배치 경고 |
| 8 | [08-reels](../../site/chapters/08-reels.html) | [ch8-reels.js](../../site/assets/sim/ch8-reels.js) | 대본·음성·자막 흐름도, 24fps 기준 장면 배분·자막 속도 시간표 |
| 9 | [09-pipeline](../../site/chapters/09-pipeline.html) | [ch9-pipeline.js](../../site/assets/sim/ch9-pipeline.js) | 생성·검수·드라이런 흐름도, 연결 누락/생성 오류/승인/수정 상태 전이 |

총 8개 모형이다. 단순화한 모형과 실제 키트 구현을 구분했다. 카드 1080×1350, 릴스 1080×1920·15~30초, 장면별 균등 배분은 이 키트의 실습 계약으로 설명했다. 카드 렌더링은 실제 구현인 Pillow를 따르고 HTML 캡처 방식으로 소개하지 않았다.

`points`가 본문 이미지에 표시되고 `subtitle`이 영상 대본·자막에 쓰임을 반복 안내했다. 프롬프트는 폴더를 나눠 3종을 보존하며, 연속 편집 때 현재 JSON을 함께 제공하도록 안내했다. API는 비활성 오류를 직접 확인하는 안전 명령과 조건·모의 시험 범위를 설명했다. 외부 서비스에 호출하는 미검증 명령은 실습 코드에 넣지 않았다.

8장은 무음으로 먼저 끝내고 음성이 필요하면 본인 녹음을 우선한다. TTS·음악의 상업/플랫폼/화자 권리, AI 자기공개, 모션 추가와 수익화 적격의 차이를 설명했다. 9장은 기존 수동 편집본을 통합 run이 자동으로 읽지 않는 점, 설정 스냅샷, 수동 검수, 재생성 시 승인 폐기를 다룬다. 원격 중복 게시 방지·영속 오류 로그가 이미 구현됐다고 소개하지 않는다.

## 실제 키트 검증

환경: 기존 `starter-kit/.venv`의 Python 3.11.15, Pillow·PyYAML·imageio-ffmpeg, 동봉 FFmpeg. 추가 의존성·모델 설치, 유료 키·실제 LLM/TTS 서비스·계정 로그인/게시가 없었다. 테스트용 출력은 Git에서 제외되는 `starter-kit/output/phase5b-*`에 생성했다. 임시 `config.yaml`은 이번 작업에서 생성 후 제거했고 기존 사용자 설정은 없음을 먼저 확인했다.

starter-kit 폴더에서 가상환경의 Python으로 실행한 명령 범위:

```text
fetch_news.py --output output/phase5b-manual/news.json
write_copy.py output/phase5b-manual/news.json --output output/phase5b-manual/copy.json
write_copy.py ... --mode prompt --template cards|reel-script|caption --output 각기_다른_폴더/copy.json
write_copy.py output/phase5b-manual/news.json --validate --output output/phase5b-manual/copy.json
write_copy.py output/phase5b-manual/news.json --mode api --output output/phase5b-manual/copy.json
render_cards.py output/phase5b-manual/copy.json --output output/phase5b-manual/cards
render_cards.py output/phase5b-manual/copy.json --config config.yaml --output output/phase5b-manual/cards-themed
make_reel.py output/phase5b-manual/copy.json --cards output/phase5b-manual/cards --output output/phase5b-manual
make_reel.py output/phase5b-manual/copy.json --cards output/phase5b-manual/cards --config config.yaml --output output/phase5b-voice
run_pipeline.py --offline --output output/phase5b-review
run_pipeline.py approve output/phase5b-review
publish.py output/phase5b-review
run_pipeline.py render output/phase5b-review
```

위 목록은 실행한 명령 범위의 요약이다.

- 합성 피드·규칙 기반 copy, 프롬프트 3종·구조 검증, PNG 5장+JPEG 5장, 20초 MP4·SRT 생성 성공.
- 테마를 ink로 바꾼 설정 경로의 카드와 별도 영상 생성 성공. 선택 설정 CLI는 무음 파일로 확인했으며 본인 실녹음·상용 TTS를 사용했다고 표현하지 않았다.
- `--mode api`만 준 명령은 기대한 비활성 오류(exit 1)로 차단. API 요청 계약은 아래 모의 시험으로만 검증.
- 검수표 미완료 approve 차단 → 시험용 체크 후 approve 드라이런 성공(요청 계획 16단계) → copy 수정 후 publish 차단 → render 후 승인 폐기·여섯 칸 초기화 → 재검수 전 approve 차단 확인.
- 승인 시험의 체크 변경은 테스트용 자동 처리다. 본문에는 자동 체크 명령을 넣지 않았으며 독자가 실제 파일·권리를 직접 보고 체크하도록 안내했다. 최종 시험 폴더는 재생성 후 미승인·검수 대기 상태다.
- 모든 카드의 PNG/JPEG 규격과 전체 MP4 디코딩을 확인했다. 카드 5장과 영상 중간 프레임을 직접 열어 한글·출처·합성 표시·자막 배치를 확인했다.
- 웹 채팅 답변 수신은 하지 않았다. 기본 offline copy를 편집/검증 가능한 입력으로 사용했다. 실제 외부 LLM 품질·한국어 내레이션 품질을 검증한 것이 아니다.

다음 기존 시험을 추가 실행했다.

```bash
cd starter-kit
.venv/bin/python -m pytest tests/test_phase4b.py -q -k 'api or real_audio_paths_mix_and_review_manifest'
```

**14 passed, 25 deselected in 18.96s.** 모의 API 명시적 허용·응답 오류·기존 문안 보존과, 테스트용 WAV/MP3의 내레이션/음악/믹싱 실제 인코딩·디코딩, 모의 TTS 플러그·음원 해시 변경 차단을 확인했다. 실제 화자 녹음·TTS 모델 품질이나 라이선스 적합성 인증이 아니다. 전체 55개 시험을 다시 실행했다고 보고하지 않는다.

상세 증거: [kit-check.json](phase-5b/kit-check.json). 자격 증명·개인 설정 파일·원응답 전문은 포함하지 않았고 로컬 절대 경로는 줄였다.

## 브라우저·콘텐츠 검증

정적 서버 `python3 -m http.server 8792 --bind 127.0.0.1 --directory site`, 기존 Chromium 1228과 `/tmp/ai-insta-phase3-browser`의 Playwright로 검사했다. 네 장 × 1280px·375px = 8개 조합에서 아래를 확인했다.

- HTML마다 9블록 순서, 상단 메타 4항목, 퀴즈 4문항·정답 하나씩, 모형 2개·교육용 배지·가정·텍스트 결과.
- 모든 내부 URL과 앵커의 HTTP 성공·대상 ID 존재. 사실 ID는 FACT-SHEET, 각주 번호는 SOURCES와 대조.
- 페이지 오류·콘솔 오류 0건, 가로 넘침 0건. 라이트·다크 모드 모두 문서 폭이 뷰포트 안에 들어감.
- 흐름도 방향키·Home/End, 프리셋 Enter, 체크박스 Space, 슬라이더 Home/End, 선택 목록 방향키, 퀴즈 Enter.
- 프롬프트 누락 경고, 카드 넘침/작은 글자/낮은 대비, 릴스 시간·장면 선택, 파이프라인 연결 누락/음원 누락/미승인 차단/수정 뒤 차단을 확인.
- 퀴즈 오답 피드백 → 초기화 → 4문항 정답·점수 → 초기화. 체크 상태 새로고침 후 유지. localStorage 접근을 차단한 별도 환경에서도 네 장의 체크·퀴즈·모형에 오류 없음.
- 장별 JS `node --check`, 담당 새 파일 공백 오류 검사, `git diff --check` 통과.

첫 모바일 검사에서 공통 툴팁이 숨겨진 상태로 문서 폭을 늘리는 문제를 발견했다. 담당 HTML의 작은 화면용 로컬 스타일로 해결하고 전체 검사를 재실행했다. 모형의 초기화 메시지도 초기 상태와 일치시킨 뒤 최종 검사를 통과했다. 공통 개선 제안은 요청 문서에 있다.

증거: [브라우저 검사](phase-5b/browser-check.json), [구조·사실 ID 검사](phase-5b/content-check.json).
스크린샷: [1280px 카드 모형](phase-5b/desktop-cards.png), [375px 릴스 모형](phase-5b/mobile-reels.png).

집필 중 W3C 대비·자막 해설, Meta 자기공개 발표, CapCut 약관, ElevenLabs 상업 이용 안내, MMS 모델 카드, Make 과금 단위, n8n 템플릿의 기존 출처를 다시 열었다. 확인 범위를 넘어 사실표를 고치거나 새로운 정책 수치를 만들지 않았다. 모든 각주는 기존 SOURCES 원문으로 연결한다.

## 인계·남은 범위

- [공통 변경 요청](phase-5b-requests.md): 장 상태·시간·난이도 정확한 diff, 모바일 툴팁 공통화 diff, 프로젝트 현황 통합 문장, 용어·실험실 연결.
- [새 용어 11개](phase-5b-glossary.md): 쉬운 설명·첫 장·관련 사실 ID. 없는 용어집 앵커를 미리 만들지 않았다.
- 공통 목차·사이드바·브라우저 제목은 `book.js` 상태 반영 전까지 ‘준비 중’이다. 직접 URL의 본문과 6~9장 이동은 동작한다. 병행 작업에서 5장·10장 파일이 생긴 것을 확인하고 실제 이전/다음 링크로 연결했다.
- Windows/macOS 실기동, 웹 채팅 실제 응답, 유료 API·실제 TTS·직접 녹음 품질, Instagram 계정/게시·원격 재시도는 미검증이다. 본문에도 범위를 밝혔다.
- 공통 파일·키트 소스·research·다른 작업자의 파일·미추적 프롬프트는 보존했다. commit·push는 시도하지 않았다.
- Discord 완료 보고: `python3 scripts/notify.py`로 한국어 5줄과 데스크톱 스크린샷을 전송했고 HTTP 200을 확인했다.
