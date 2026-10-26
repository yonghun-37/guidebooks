# ReelsBook 검토 반영과 최종 게이트

2026-10-26 · Codex 작성자 수정·로컬 게이트 완료. Claude Code 최종 검수 대기.

기준: `AGENTS.md`, guidebook-writing/pipeline Skill, `STYLE-GUIDE.md`, `DESIGN.md` 12절, [독립 검토](phase-R-insta-findings.md). 이 기록은 기존 AId 통합·R 독립 검토를 잇는 수정 결과다.

## 범위와 판정

- **차단 0건, 혼란 11건·사소 2건 모두 반영. 미반영 항목 없음.** 실제 서비스의 가입·생성·게시 성공을 뜻하지 않는다.
- 구현 변경은 `site/` 16파일이다. `starter-kit/` 코드는 수정할 필요가 없어 유지하고, 깨끗한 복사본에서 설치·테스트·오프라인 생성을 다시 실행했다.
- 요청받은 이 결과 파일 외에는 문서를 변경하지 않았다. 다른 작업자가 수정 중인 `site-shorts/`와 기존 루트 README·검토 자료를 보존했다. 범위 지시에 따라 `PROJECT_STATE.md`, 서가 진행표, 공통 생성기·검사기는 수정하지 않았다. commit/push 없음.
- 정적 HTML/CSS/바닐라 JS 구조와 의존성은 유지한다. 새 ADR은 필요 없다.

## 최종 게이트

| 게이트 | 결과 | 실제 실행·확인 범위 |
|---|---|---|
| `check_site(site)` | **통과** | `python3 scripts/check_site.py --site site` 및 `check(root=Path.cwd(), site='site')`. 검사기 집계 HTML 40개·내부 참조 3,354개·도구 31개·실습/E2E 43키·퀴즈 57문항·오류 0. 브라우저 전수 대상인 site 자체는 38페이지이며 검사기는 서가 HTML도 포함한다. |
| `style_lint` | **통과** | 고정 `phase-9/baseline.json`의 25/25파일, 나머지 site HTML 13/13파일. 금지어·내부어 0. 상자 밖 지정 단서는 나머지 파일 합계 2회로 파일별 기준 충족. 기존 이론 14장 모두 기존 분량의 70% 이하. 뉴스카드 69.61%, 릴스 68.89%. 기준선은 변경하지 않았다. 신규 장·부록의 과거 축약률은 판정하지 않는다. |
| 1280/375/360px·라이트/다크 | **통과** | Chromium 149에서 site 38페이지 × 3폭 × 2테마, 접기 펼친 상태 포함. 전체 화면·탐색·퀴즈·탭·링크 2,967검사, 동적 내부 링크/앵커 1,012개. 가로 넘침 0. 실제 CDN 글꼴 사용. |
| 콘솔·페이지·내부 HTTP | **통과** | 전체 화면, AI 도구, 기존 도구, 수정 항목 추가 검사에서 오류 각 0. 기존 도구 조작 중 요청 3건은 로컬 삽화 지연 로드이며 외부 API 호출이 아니다. |
| 키보드·AI 도구 | **통과** | 420검사. 도구 지도 선택, 여섯 프롬프트 정확한 복사와 클립보드 거부 시 선택 복사, 모델 274행 검색·범주·빈 결과·초기화, 비용 조합·재시도·현금 지출, JS 없는 읽기. Enter/Space·방향키 조작 포함. |
| 기존 본문/실습 도구 회귀 | **통과** | 877검사. 수입·카드 편집·릴스 타임라인·가상 게시·증거 검수의 본문과 실습 재사용 도구를 3폭에서 조작. 키보드·극단값·무효 입력·모바일 결과 표시 확인. 이 검사는 기존 방식대로 CDN CSS 대신 시스템 글꼴도 확인한다. |
| 이번 수정의 추가 동작 | **통과** | 27검사. 최초 비용 0원·5장, 저비용/고비용 변경 후 키보드 초기화→무료 복원, 내부 B번호 제거·서비스 가격표 링크, 달력의 앱 게시 경로, 모션/세 샷 접기의 키보드, 메뉴 Escape·초점 복귀, 해설 준비 체크의 E2E 공유. 모션 도식 3폭·2테마와 프롬프트 360px 다크를 캡처하고 대표 화면을 육안 확인. |
| starter-kit 설치·테스트 | **통과** | Linux x86_64/Python 3.11.15. `.venv`, `.env`, 캐시·생성물을 제외한 새 복사본에 새 가상환경과 `requirements-dev.txt` 설치. `python -m pytest -q`: **116 passed in 26.87s**. |
| starter-kit 오프라인 생성 | **통과** | 새 복사본에서 `python run_pipeline.py --offline --output output/final-smoke`. `REVIEW.md` 검수 대기로 정상 종료. 사람 승인·실제 게시를 자동 수행하지 않는다. |
| JS·diff | **통과** | 변경한 `ai-guide.js`, `plan-v2.js` 각각 `node --check`; `git diff --check -- site starter-kit` 통과. |

위 검사 수는 프로그램의 확인 항목 수다. 독립 사용성 실험 참여자 수나 외부 서비스 성공 횟수가 아니다.

## 항목별 해결

| ID | 반영 위치 | 해결 내용 |
|---|---|---|
| RI-01 · 혼란 | `chapters/01-map.html`, `04-niche.html`, `14-plan.html`, `practice/01-account.html`, `assets/sim/plan-v2.js` | 첫 준비와 FAQ를 ChatGPT→Canva→선택 편집→검수→앱 게시로 통일했다. Python·설정 파일은 키트 선택자만 사용한다. 실습 1 본문은 실습 3을 기본으로, 실습 2를 선택 설치로 안내한다. 30일 표·동적 달력에서 생성 예약을 기본 과제로 빼고 앱 게시 기록으로 바꿨다. 실습 9 링크도 선택 키트 생성 예약으로 표시했다. |
| RI-02 · 혼란 | `practice/04-cards.html`, `05-reel.html`, `e2e.html` | 해설은 장면표 작성→Canva 1080×1920 새 디자인→한 행당 한 페이지→scene-01.png부터 저장→CapCut으로 연결했다. 카드 4:5·5장 경로와 캔버스·문안 배치·저장을 각각 분기하고 준비물·성공 기준·E2E 순서도 맞췄다. 삽화 요청도 해설이면 9:16으로 바꾼다. 기존 진행 키는 보존했다. |
| RI-03 · 혼란 | `practice/05-reel.html#voice`, `prompts.html#reel-prompt` | 대본 프롬프트가 장면표와 읽을 문장만 별도 출력하게 했다. storyboard.txt와 voice-script.txt를 구분하고, 표만 나왔을 때 다시 요청할 문장을 제공했다. 가상 공지의 완성 낭독 입력과 Vrew에 넣을 파일·빼야 할 번호/그림 지시/URL·미리듣기 성공 기준을 명시했다. |
| RI-04 · 혼란 | `practice/05-reel.html#motion-steps`, `chapters/08-reels.html#voice-paths` | PC의 클립 선택→4초 길이→시작 100%·첫 마름모→끝 105%·두 번째 마름모→전체 재생을 번호 순서로 제공했다. 연습값임을 밝히고 직접 그린 SVG, 모바일 대응 순서·잘림 수정·공식 도움말을 붙였다. 이론에서 직접 연결한다. |
| RI-05 · 혼란 | `practice/03-copy.html#signup`, `#text-limit` | 첫 초안 전 한도 소진에도 Gemini 웹→개인 계정→새 채팅→같은 프롬프트/원문→TXT 저장→원문 대조→Canva로 이어지게 했다. 두 서비스 모두 제한되면 직접 작성으로 마치고 “AI 초안 재시도 대기”를 따로 기록하며 AI 생성 완료 체크를 하지 않게 했다. |
| RI-06 · 혼란 | `chapters/07-cards.html#faq-4` | Noto Sans KR의 실제 OFL 조건으로 광고 카드의 글자 사용 허용과 폰트 파일 단독 판매 금지를 대비했다. 자산명·허락·용도·확인일이 있는 권리 메모 완성 예를 주고, 사진의 허락은 따로 보관하게 했다. 기존 S095와 연구 VIDEO-08 근거를 사용했다. 무료 여부만으로 허락을 판단하는 문장을 제거했다. |
| RI-07 · 혼란 | `chapters/08-reels.html#faq-2`, `#timing` | Vrew 한국어 기본 AI 화자·무료 잔여량·낭독문→미리듣기→오디오/MP4 저장과 조건 메모를 이론에서 답했다. Voicevox 출처 예외와 타입캐스트 Free의 상충으로 인한 제외를 대비하고 실습 5 음성 절로 바로 연결했다. 기존 S330/AIP-032와 S336·337/AIP-053을 사용했다. |
| RI-08 · 혼란 | `chapters/08-reels.html#generated`, `prompts.html#video-prompt` | 기준 이미지 완성 요청과 reference.png 저장부터 안내했다. 영어 완성 입력 세 개를 몸 돌리기/고개 기울이기/물러나기로 제공하고 shot-01~03.mp4에 대응시켰다. 같은 참조·모델·비율·길이·빛을 유지하는 독립 클립임을 밝히고 연결·잘라내기·변형 시 재시도 기준을 제공했다. |
| RI-09 · 혼란 | `ai-models.html#cost-calculator`, `assets/ai-guide.js` | 최초 HTML·JS 결과와 초기화 모두 무료 앱·본인 소재·추가 사용분 0원이다. 결과 바로 위에 서비스 메뉴 실습과 별도 API 예산 실험의 차이를 적었다. 기존 유료 조합 계산·실제 첫 결제와 사용분 차이 설명은 유지했다. |
| RI-10 · 혼란 | `ai-models.html#plans`, `#models` | B3/B5/B11/B15/B17 및 추가 B24를 Google AI·Ideogram·Hailuo/MiniMax·ElevenLabs·CLOVA·미리클 가격표 이름과 앵커로 바꿨다. “본문 빈값”, “독립증거”, 가격 재현·읽기 과정 문구는 현재 요금표·결제 화면 확인 행동으로 바꿨다. 렌더링 본문에 B번호 0개, 각 링크 실제 이동을 확인했다. |
| RI-11 · 혼란 | `practice/09-schedule.html` | 준비물을 키트 PC·가상환경·로컬 피드/설정·OS 예약 권한으로 바꿨다. PC 초안 생성 예약임을 앞에서 밝히고 앱 게시 예약은 이론 11장으로 분리 연결했다. |
| RI-12 · 사소 | `ai-models.html#cost-calculator` | 선택 목록·비교표를 실습과 같은 총 5장으로 맞췄다. API 비교에서는 표지를 포함한 다섯 장 모두 삽화를 하나씩 생성하는 추가 선택을 가정한다고 공개했다. 무료 실습의 도형 경로와 구분하고 기존 5장 계산식은 유지했다. |
| RI-13 · 사소 | `practice/07-publish.html#carousel` | Canva PNG면 card-01.png부터, JPG면 card-01.jpg부터 실제 저장한 장수 전체를 선택하도록 했다. 이번 연습은 5장이며 확장자를 바꾸지 않는다고 명시했다. |

이론 8·9장은 추가 예 때문에 분량 기준을 넘지 않도록 중복 안내를 줄였다. 질문·직답·예·행동, 기존 퀴즈·실습 체크 키·도구 ID는 보존했다. 무료 음성/자산의 판단 예와 핵심 경로 충돌을 직접 다시 읽어 확인했으며 새 독립 검토자가 전체 문체 기준을 재채점한 것으로 표기하지 않는다.

## 실행 환경과 재현

검사·로그·화면·임시 회귀 스크립트는 `/tmp/reelsbook-F-insta/`에 보관했다. 임시 폴더의 영구 보존은 보장하지 않으므로 실제 결과·방법·한계는 이 문서에 기록한다. 정적 검사 원본 JSON은 `/tmp/reelsbook-F-site.json`이다.

- 서버: `python3 -m http.server 8657 --bind 127.0.0.1 --directory site`.
- 문체: `docs/results/phase-9/baseline.json`의 `files` 키 25개에 `scripts/style_lint.py --baseline ...`을 적용하고, 나머지 `site/**/*.html` 13개는 기준선 없이 검사했다.
- 전체 화면은 `phase-AId/verify-browser.mjs`를 임시 복사해 대상은 site만, URL은 위 서버, 산출물은 `/tmp`로 바꿨다. AI 검사는 `phase-AId/verify-ai.mjs`를 같은 방법으로 복사하고, 초기화 뒤 무료 조합을 확인한 다음 API 조합을 명시적으로 선택해 재시도 키보드 계산을 검사했다. 원본 검사 스크립트는 수정하지 않았다. 최초 실패는 옛 검사기의 API 기본값 가정이었으며 새 기본값 기대와 API 명시 선택으로 수정 후 420검사 통과했다.
- 기존 도구는 R 검토에서 사용한 임시 회귀 스크립트의 서버·출력 경로를 바꿔 877검사를 실행했다. 추가 27검사는 `/tmp/reelsbook-F-insta/verify-final.mjs`에서 수행했다.
- 키트는 `/tmp/reelsbook-F-insta/starter-kit`에 복사 후 `python3.11 -m venv .venv`, `.venv/bin/python -m pip install -r requirements-dev.txt`, 키트 폴더에서 `.venv/bin/python -m pytest -q`와 오프라인 명령을 실행했다.
- Noto Sans KR OFL 원문, Vrew 상업 이용 FAQ, Gemini 로그인 도움말과 CapCut 공식 키프레임 안내를 직접 열람/검색해 이번 안내와 대조했다. 정책·가격을 전수 재조사한 작업은 아니다. CapCut 조작은 [공식 PC 안내](https://www.capcut.com/resource/how-to-add-keyframes-in-capcut)를 참고했으며 앱 메뉴 차이 대응은 본문에 남겼다.

## 남은 확인

미반영 검토 항목은 없다. 외부 서비스 가입·한국어 화자 실제 생성/다운로드·영상 생성·휴대폰 전송·Instagram 로그인/게시·Windows/macOS 실기기·OS 예약 등록과 다음 날 실행은 이번에 수행하지 않았다. 유료 API·결제를 사용하지 않았다. 위 로컬 게이트는 이 실서비스 확인을 대신하지 않는다. Claude Code의 최종 검수·커밋·배포는 별도다.

## 알림

`python3 scripts/notify.py "✅ [ReelsBook 최종 수정 완료] ..."` 전송 성공: HTTP 200, 메시지 ID `1564162160031047781`. 결과 경로·게이트/키트 통과·남은 실서비스/최종 검수·commit 없음으로 보고했다.
