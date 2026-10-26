# Y4ai · ShortsBook AI 제작 보강

2026-10-26 · **담당 범위 집필·검증 완료, 공통 파일 통합·Claude Code 검수 대기**.

## 해결한 문제와 구현

“정확히 어떤 서비스·TOOL을 이용하고 어떤 과정으로 AI 콘텐츠를 만드는지”를 기존 이론 4~8장의 중심 제작 모듈과 새 도구 지도에 넣었다. DESIGN 12절·확정 STYLE-GUIDE를 우선하고, 공통 조사 `research/ai-production.md`의 직접 촬영+AI 편집 / 얼굴 없는 해설 / AI 영상 생성 세 레시피를 연결했다. R3b 노트가 존재하므로 모델·비용 부록도 작성했다.

| 원고 | 구현한 내용 |
|---|---|
| [AI 도구 지도](../../site-shorts/chapters/02b-ai-tools.html) | 처음 쓸 ChatGPT·Clipchamp, 작업별 실제 서비스·무료량·가격·한국어/한국·상업 조건·공개 판단, 세 레시피의 입력·메뉴·출력·시간·비용, 경로 선택 도구·FAQ5·퀴즈3 |
| [4장 대본](../../site-shorts/chapters/04-script.html) | ChatGPT/Gemini 새 대화에 사실·장면 메모 입력→대본·장면표→원문·낭독 검수→TXT. 촬영/해설/샷 설계·수정 프롬프트 |
| [5장 소리](../../site-shorts/chapters/05-audio.html) | 본인 녹음·타입캐스트의 대본/화자/발음/다운로드, Vrew·Clipchamp 대안, 보관함 MP3·CC 표시문→음악 트랙. 무료 생성/다운로드/상업 사용 구분 |
| [6장 장면](../../site-shorts/chapters/06-scenes.html) | 촬영 MP4·장면 PNG·생성 MP4 구분. 기준 그림→Flow Frames/Ingredients·Runway I2V→샷 검사·저장. 피사체/한 동작/샷/카메라/빛/스타일/길이 프롬프트·같은 참조 유지·앞뒤 자세 연결·크레딧 계산 |
| [7장 편집](../../site-shorts/chapters/07-editing.html) | 세 레시피의 재료를 Clipchamp 타임라인으로 모으기, 음성 기준 컷·카드 모션·생성 클립 연결·자막·음악·출력, CapCut/Vrew 대체 메뉴 |
| [8장 자막](../../site-shorts/chapters/08-captions.html) | 한국어 전사→숫자/부정어/이름 교정→폰 크기·시간 검사→SRT/MP4 따로 저장. 직접 만든 좋은/나쁜 자막 예·교정 프롬프트 |
| [프롬프트 모음](../../site-shorts/prompts.html) | 작업별 10개 복사용 프롬프트·좋은/나쁜 요청 비교·장별 입력 메뉴 링크·실제 이미지 생성 프롬프트 2개 |
| [AI 모델·사용처·비용 총정리](../../site-shorts/ai-models.html) | R3b의 24개 구독표·6분류 271개 모델/버전/미공개 기능 항목·검색·한국 제공/상업권/출력/표시/각주. 32초 쇼츠 비용 시나리오와 재생성·월정액·사용분 구분 |

종료된 Sora 세 버전의 과거 사양은 부록에서 빼고 “종료됨”으로 모았다. CLOVA X/Cue:도 “종료됨”만 표시했다. **HyperCLOVA X 모델군은 대화 서비스 CLOVA X와 다르므로 유지**했다. 모델 표 271행은 기반 모델 271개가 모두 현행 제공된다는 뜻이 아니다. 이전 세대·종료 endpoint·앱의 미공개 엔진도 상태를 나눠 표시했다.

가격·무료량·한국 가용성은 R3·R3b 사실표/출처의 Y번호로 연결하고 조사 기준월을 표시했다. 시간은 조사 노트의 작업 계획용 값으로, 가입·설치·생성 대기·재시도 시간을 더 잡고 독자가 실제 시간을 기록하도록 했다. 무료 기본 경로는 본인 촬영·녹음+Clipchamp이며 무료 생성 영상 성공은 약속하지 않았다.

## 파일과 소유권

- 기존 4~8장의 9블록·FAQ5·기존 ID·인라인 및 외부 스크립트를 보존했다. 새 모듈은 축별 설명의 맨 앞에서 읽을 수 있다. 로컬 AI 제작 내비게이션으로 도구 지도·프롬프트·모델 부록을 직접 연다.
- 추가 스타일/동작: `site-shorts/assets/ai-production.css`, `ai-production.js`. 공통 파일을 수정하지 않고 기존 book.js의 복사·퀴즈·테마 기능을 재사용했다.
- 공통 book.js/book.css/common.js/practice.js/index/credits, 공유 PROJECT_STATE·서가 진행 페이지는 수정하지 않았다. [보호 파일 해시](phase-Y4ai/protected-files.json)와 [보존 확인](phase-Y4ai/content-verification.json)에 기록했다. glossary 실파일은 현재 없다.
- 새 장 3장 배치·기존 번호 조정·ready 상태·목차/표지/푸터·출처 고지·상태 인계는 [통합 요청 diff](phase-Y4ai-requests.md)에 있다. 임시 복사본에서 `patch --dry-run`으로 세 파일의 diff 적용 가능성을 확인했다. 제안 JS 구문도 검사했다.
- [용어집 제안](phase-Y4ai-glossary.md)을 남겼다. 새 문서 구조/ADR은 만들지 않고 기존 단계 결과 기록 방식을 사용했다. 요구사항은 기존 `docs/prompts/phase-Y4ai.md`를 재사용했다.
- 시작 시 있던 인스타 원고·쇼츠 실습·연구 결과·다른 담당자의 변경을 보존했다. 커밋·push·배포를 실행하지 않았다.

## 실제 AI 생성 이미지

내장 `image_gen`으로 첫 그림을 생성하고, 이를 참조해 다음 장면을 생성했다. 서비스 화면·브랜드 로고·실존 인물은 사용하지 않았다. 두 파일 모두 **720×1280, 9:16**이며 WebP 압축했다. 본문과 부록에 “AI 생성 예시”·실제 사용 프롬프트·참조 관계를 표시했다.

| 파일 | 크기 |
|---|---|
| [기준 그림](../../site-shorts/assets/img/ai-examples/y4ai-robot-reference.webp) | 24,528 bytes |
| [고개를 기울인 장면 카드](../../site-shorts/assets/img/ai-examples/y4ai-robot-observe.webp) | 28,866 bytes |

실제 지시문·생성 방법·후처리는 [y4ai-prompts.json](../../site-shorts/assets/img/ai-examples/y4ai-prompts.json)에 있다. 압축 후 400KB 이하와 파일 해시를 확인했다. 이는 **정지 그림의 실제 생성 예**다. Flow·Runway에서 영상 생성까지 실행한 결과로 서술하지 않았다.

## 검증 결과

- `style_lint.py`: 변경/신규 HTML **8/8 통과**, 금지어·내부 용어·바깥 단서 표현 **0**. [보고서](phase-Y4ai/style-lint.json). 쇼츠에 기존 고정 분량 기준선이 없고 이번 요구는 제작 핵심 모듈 추가이므로 새 기준선을 만들어 70% 축약을 통과한 것처럼 기록하지 않았다.
- `check_site.py --site site-shorts`: **35 HTML·내부 참조 2,739개·퀴즈 45개·오류0**. [보고서](phase-Y4ai/check-site.json). 신규 `02b` 파일은 검사기의 기존 번호 패턴 밖이므로 9블록·FAQ5·퀴즈는 브라우저에서 별도로 검사했다.
- [Chromium 검증](phase-Y4ai/browser-check.json): **1,174 검사 통과**, 변경/신규 8페이지×1280/375/360px×라이트/다크. 접기 전후 가로 넘침0·콘솔/페이지/내부 HTTP 오류0. 실제 버전 고정 CDN 글꼴을 사용했다. 내부 링크·앵커452개, 이미지 로드·정확한 9:16, 표 가로 스크롤, 프롬프트12개 정확한 복사·클립보드 거부 대체, 모델 검색/0결과/초기화, 경로 선택, 퀴즈·본문 건너뛰기, 기존 계산기·뮤트·구도·프레임·자막 극단값/복구를 확인했다.
- `node --check site-shorts/assets/ai-production.js`, 제안 book.js 구문 검사, `git diff --check` 통과. 기존 도구 스크립트 동일성·ID 보존·FAQ/9블록·보호 파일 해시·이미지 용량도 [보존 확인](phase-Y4ai/content-verification.json)에 있다.
- 브라우저 검사 중 lazy 이미지 decode·비동기 클립보드 완료 대기·기존 슬라이더의 max85·동일 페이지 해시 이동의 응답 null을 검사 스크립트에 반영한 뒤 전체를 다시 실행해 통과했다. 사이트 동작을 검사에 맞춰 바꾸지는 않았다.

재현: 저장소 루트에서 `python3 -m http.server 8597 --bind 127.0.0.1` 후 `node docs/results/phase-Y4ai/verify-browser.mjs`. 실행 환경의 Chromium/Playwright 경로는 스크립트 상단에 기록했다. 기존 서버가 같은 포트를 쓰면 해당 서버를 재사용한다.

대표 화면: [AI 생성 예시 1280](phase-Y4ai/ai-examples-1280.png) · [375 레시피](phase-Y4ai/recipe-375.png) · [360 생성 예시](phase-Y4ai/ai-examples-360.png). 표지·프롬프트·모델 부록 포함 스크린샷 총21개를 [결과 폴더](phase-Y4ai/)에 보관했다.

## 남은 일과 실행 범위

공통 목차·브라우저 제목에는 기존 준비중 표시가 남아 있다. 통합 담당자가 요청 diff와 다른 Y4 결과를 합쳐 번호·상태·전체 출처·PROJECT_STATE·진행 페이지를 갱신해야 한다. 이 작업에서는 본문·로컬 링크·레시피를 직접 열 수 있게 했다.

외부 서비스의 실제 한국 계정 가입/결제·TTS 다운로드·Flow/Runway 영상 생성·실제 Studio 게시·모바일 OS 앱 조작은 실행하지 않았다. 정지 이미지 생성과 로컬 교과서 UI의 Linux Chromium 검증을 완료한 범위다. 앱 메뉴는 조사된 기능과 표준 버튼 변경 안내·공식 도움말을 함께 제시했다. 실습 원고는 기존 Y4p 파일로 연결하며 이번 작업에서 수정하지 않았다.

디스코드 완료 알림을 대표 화면 `ai-examples-1280.png` 첨부와 함께 전송했다. `scripts/notify.py` 응답 HTTP 200, 메시지 ID `1564151257260630016`.
