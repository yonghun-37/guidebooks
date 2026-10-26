# 교과서 서가 인터랙션 분석 — Phase 10r

조사일: 2026-10-26. [Books 서가](https://books.euiyun.com/)에서 **CameraBook·MusicBook·NetworkBook·YieldBook 4권, 책마다 표지·본문 2장·종합 도구 1페이지, 총 16페이지**를 REA로 관찰했다. ColorBook 두 계열(`colorbook.euiyun.com`, 이전에 분석한 `art.euiyun.com/color/`)은 선정에서 제외했다.

가장 유용한 공통점은 **설명한 변수를 직접 바꾸면 그림·수치·해석이 함께 바뀌고, 종합 도구에서 그 판단을 다시 사용한다**는 것이다. ReelsBook에는 도구 수를 늘리기보다 기존 도구를 실제 문안·시간·판단에 연결하는 개선을 제안한다. 아래 20개는 설계 검토안이며 구현 완료나 범위 확정이 아니다. 사이트·키트·설계서·공용 상태 파일은 수정하지 않았다.

## 1. 범위, 선정과 근거 읽는 법

### 서가 목록 확인

홈페이지에는 52권 안내가 있고, [전체 책장](https://books.euiyun.com/library/)의 이번 렌더링은 출간52개·예정17개로 총69개였다. 출간만 세는 수와 예정까지 합친 수를 구분한다. 아래는 장르별 목록을 확인한 결과다. 예정 항목은 방문 가능한 책으로 선정하지 않았다. 근거: `shelf`, `library`, `.catalog-book`, `.catalog-book.published`, `.catalog-book.planned`, `#shown`.

| 분야 | 확인한 책장 항목 |
|---|---|
| 반도체 24 | DeviceBook, DigitalBook, DesignBook, SoCBook, AnalogBook, ProcessBook, LithoBook, EtchBook, DopingBook, YieldBook, FailureBook, TCADBook, PackagingBook, TestBook, MemoryBook, OpticsBook, SensorBook, DisplayBook, GPUBook, PowerBook, ChipIndustryBook, ThinFilmBook, CMPBook, FabInfraBook |
| 기초과학·공학 11 | ElectromagneticsBook, ThermoBook, MaterialsBook, PlasmaBook, 일반화학, 일반물리학, 현대물리학, 유기화학, 정역학, 동역학, 유체역학 |
| 컴퓨터·AI 7 | ComputerBook, OSBook, NetworkBook, DatabaseBook, AIBook, AXBook, StatBook |
| 기기·시스템 5 | CarBook, ShipBook, PhoneBook, ColorBook, ElectricBook |
| 돈·부동산 6 | MoneyBook, EconomicsBook, StockBook, InsureBook, TaxBook, EstateBook |
| 건강 1 | BodyBook |
| 예술·교양 15 | CameraBook, MusicBook, MathBook, ArtBook 색채·구도·드로잉·타이포·미술사·이미지·웹·제품 디자인·산업디자인, GuitarBook, PianoBook, DrumBook |

### 선정 이유와 방문 페이지

| 책 | 선정 이유: 다른 조작과 학습 목적 | 표지 / 대표 장 2개 / 실험실·도구 URL |
|---|---|---|
| CameraBook | 같은 장면의 촬영 설정을 바꾸는 지각 비교, 여러 조건을 만족시키는 미션. 카드·영상 미리보기와 연결하기 좋다. | [표지](https://camerabook.euiyun.com/) · [4장 셔터](https://camerabook.euiyun.com/chapters/shutter.html) · [14장 영상](https://camerabook.euiyun.com/chapters/video.html) · [16장 연습장](https://camerabook.euiyun.com/chapters/playground.html) |
| MusicBook | 배음 막대 직접 편집, 트랙×시간 격자, 소리·파형·재생 위치의 동시 피드백. 릴스와 Shorts의 시간 편집에 적합하다. | [표지](https://musicbook.euiyun.com/) · [2장 배음](https://musicbook.euiyun.com/chapters/harmonics.html) · [12장 시퀀서](https://musicbook.euiyun.com/chapters/sequencer.html) · [17장 작업실](https://musicbook.euiyun.com/chapters/studio.html) |
| NetworkBook | 절차를 이전/다음으로 재생하고, 손실·지연을 넣어 실패를 관찰한다. API 게시와 자동화 상태 이해에 적합하다. | [표지](https://networkbook.euiyun.com/) · [9장 TCP](https://networkbook.euiyun.com/chapters/tcp.html) · [10장 웹](https://networkbook.euiyun.com/chapters/apps.html) · [24장 통합 여행](https://networkbook.euiyun.com/chapters/journey.html) |
| YieldBook | 원인을 바로 고르기 전에 조사할 증거를 선택한다. 제한된 예산·복합 원인·재열람 가능한 단서 로그로 검수 판단을 연습시킨다. | [표지](https://semi.euiyun.com/yield/) · [9장 패턴](https://semi.euiyun.com/yield/chapters/patterns.html) · [13장 공통성](https://semi.euiyun.com/yield/chapters/commonality.html) · [15장 수사실](https://semi.euiyun.com/yield/chapters/detective.html) |

NetworkBook의 24장은 명칭이 실험실은 아니지만 여러 앞 장의 원리를 한 상황에 합치는 종합 도구다. 다른 책을 무작위로 같은 수만큼 방문한 비교 연구가 아니며, 선택한 표본의 발견을 서가 전체 특성으로 일반화하지 않는다.

### 방법과 한계

- 기존 Chromium 149.0.7827.55를 `--headless --no-sandbox --remote-debugging-address=127.0.0.1 --remote-debugging-port=9337`로 실행했다. `mktemp -d /tmp/ai-insta-10r.XXXXXX`로 만든 `/tmp/ai-insta-10r.1DGMei/profile`을 사용했다. 개인 프로필·로그인·실계정은 사용하지 않았다.
- REA MCP의 `list_browser_targets` → `capture_browser_scenario` → `inspect_web_page` → 이벤트 리스너·번들·스크린샷 순으로 조사했다. 선언한 버튼·키 입력·선택 동작은 **REA가 실제 실행**했다. 수동 호출한 CDP 드래그는 별도 근거로 표시한다.
- 본문의 `camera_actions` 같은 이름은 부록의 **완전한 Evidence ID**에 대응한다. REA 원본에는 URL·시나리오 입력·단계별 DOM/접근성·스크립트 해시·제한 사항이 있다. 문서에는 재현에 필요한 선택자와 변화만 요약했다.
- 수동 자료와 REA Evidence 57건의 내보내기 묶음은 위 임시 폴더에만 보관했다. `rea-evidence-bundle.json`은 19,018,079B다. `/tmp`와 MCP 세션은 영구 보관소가 아니므로 Evidence ID만으로 미래 세션에서 다시 조회된다고 보장하지 않는다. 공개 저장소에 원문·코드·이미지·캡처 전문을 넣지 않았다.
- REA 수동 관찰은 접속 이전 네트워크·콘솔을 복원하지 못한다. 기본 origin 범위 밖 CDN·분석 스크립트가 제외된다. 번들 파싱의 `complete`는 **캡처한 스크립트 범위의 완결성**이며 사이트 전체·외부 라이브러리·서버 코드 분석 완료가 아니다.
- REA 시나리오는 종료하면서 화면 크기 설정을 복구한다. 종료 뒤 별도 스크린샷이 1280×757로 나온 것을 처음에는 적용 실패로 오인했으나 제공자 구현의 적용/복구와 시나리오 내 캡처를 확인해 정정했다. 혼합된 화면 크기·스크롤 상태의 중간 캡처는 모바일 판정에서 제외하고, 최종 판정은 CDP로 같은 세션 안에서 크기 설정→탐색→스타일 측정→캡처한 결과를 사용했다.
- **CDP 보완 이유**: REA 시나리오가 지원하는 동작에 좌표 드래그가 없고, 수동 검사에는 JS 평가·계산 스타일·Resource Timing 질의가 없다. 이 항목만 기존 Playwright/CDP로 보완했다. **curl 보완 이유**: REA는 CSS 자원 URL·크기는 제공하지만 스타일시트 본문을 제공하지 않아, 4권의 공개 `css/style.css`만 임시 다운로드해 전환 시간·미디어 규칙을 확인했다.
- 웹 열기 도구는 Books URL 접근에 실패했다. REA와 로컬 Chromium은 성공했으므로 웹 열기 실패를 사이트 장애로 해석하지 않았다. REA 설정·설치·승인 정책을 변경하지 않았다.

## 2. 책별 발견

### CameraBook — 설정의 의미를 결과로 보여 주고, 미션에서 다시 사용한다

**뛰어난 점:** 추상적인 숫자가 장면의 흐림·밝기·움직임으로 바로 돌아온다. 종합 도구는 정답 설정 하나를 외우게 하기보다 노출·초점·흐림·흔들림 조건을 따로 보여 준다.

| 관찰 위치·근거 | 관찰 내용 | ReelsBook에 가져올 판단 |
|---|---|---|
| 표지 `.home-hero`, range, 생성 과정 SVG — `camera_cover` | 시작/연습장 진입점, 가상 촬영 조작, 결과 해석, 오해별 관련 장, 목적별 학습 경로가 있다. | 표지는 완성 카드·짧은 영상의 한 변수만 바꾸는 체험으로 시작할 수 있다. 원리 링크는 결과 가까이에 둔다. |
| 셔터 `#sim-motion`, `#sim-curtain`, `#sim-rolling` — `camera_shutter` | 속도·셔터·패닝을 조합하고, 느린 셔터막 재생이나 센서 읽기 프리셋으로 시간 차이를 설명한다. 밝기 자동 보정 해제처럼 다른 효과를 드러내는 조작도 있다. | 자막·장면 길이를 바꿀 때 다른 변수를 고정하는 비교가 필요하다. 실패를 유발할 때 무엇을 고정했는지 적는다. |
| 영상 `#fp-m`, `#an-a`, `#an-pause`, `#sim-log` — `camera_video`, `camera_video_actions` | 같은 운동을 여러 fps 행에 나란히 표현한다. 실시간/슬로 재생을 바꾸고 셔터 각도를 고른 뒤 한 프레임을 정지할 수 있다. Log 비교는 고정된 장면의 표시 방법을 바꾼다. | ‘재생 중 인상’과 ‘멈춘 화면의 읽기 쉬움’을 따로 검사하게 한다. 서로 다른 내용을 전후 비교로 사용하지 않는다. |
| 연습장 `#missions`, `#brief`, `#c-ap`, `#c-shoot`, `#c-msg` — `camera_lab`, `camera_actions` | 힌트 후 `#c-ap`에서 Home 입력: f/5.6→f/1.4. 셔터 버튼 후 성공 문장이 표시됐다. 다른 초점 클릭 없이 이 표본의 초기 초점 상태로 성공했다. | 실습 성공 기준을 항목별로 보여 주고, 충족하지 못한 항목에만 힌트를 준다. 성공 문구를 실제 PNG·MP4 제작 성공과 혼동하지 않는다. |

설명 흐름은 개념 문단→조작 도구→아래의 관찰 방법·해석→후속 표·주의로 이어진다. 모든 도구가 예측 답을 먼저 받는 구조는 아니다. 미션은 목표·조건을 조작 전에, 힌트·결과를 조작 후에 보여 준다. 모바일 연습장에서는 목표→장면→입력이 세로로 쌓여 한 화면에 모두 들어오지 않는다. 우리 책은 대표 입력을 줄이고 현재 결과를 가까이 두어야 한다.

기술 근거 `camera_inspect`, `camera_bundle`, `camera_listener`: 일반 script와 장별 지역 상태, `CB` 공통 helper, Canvas 2D·설명 SVG 조합이다. `#an-a` 버튼 click은 `js/common.js`의 **0부터 세는 319행**으로 연결된다. 이는 등록 위치이며 실제 실행 인과 전체를 증명하는 스택은 아니다. 번들에서 분석한 4개 script에는 모듈 import 간선과 프레임워크 지문이 없었다. ‘사이트 전체가 라이브러리를 쓰지 않는다’는 뜻은 아니다.

### MusicBook — 시간과 소리를 편집 가능한 구조로 만든다

**뛰어난 점:** 직접 만든 조합을 재생하면서 소리·시간 위치·파형·수치를 함께 읽는다. 프리셋은 완성 예제이자 출발점이고, 개별 편집 후 원래 예제로 돌아갈 수 있다.

| 관찰 위치·근거 | 관찰 내용 | ReelsBook에 가져올 판단 |
|---|---|---|
| 표지 코드 버튼·비트 프리셋 — `music_cover` | 표지에서 소리 조합을 누르고 대표 실험·목적별 경로로 들어간다. 전역 음소거 버튼이 있다. | 영상도 사용자가 재생을 요청하도록 한다. 소리 없이 배울 경로를 함께 둔다. |
| 배음 `#cv-add`, `#add-presets`, `.sim-readout` — `music_harmonics`, `music_add_actions`, `music_add_listener` | 프리셋 선택과 Canvas 막대 조작이 합성 파형·지표에 연결된다. REA는 pointerdown/move/up 등록 위치를 확인했다. CDP 좌표 드래그 후 무게중심 352→358Hz, 짝수/홀수 에너지 −5.0→−3.6dB였다. 음질을 사람이 청취 평가한 결과는 아니다. | 자막 한 장면의 길이를 바꾸면 해당 장면과 전체 길이·읽기 부담을 동시에 바꾼다. 직접 드래그에는 동등한 숫자 입력이 필요하다. |
| 시퀀서 `#seq-grid`, `#seq-bpm`, `#seq-play` — `music_sequencer`, `music_actions` | 지우기 뒤 킥 첫 칸 클릭·둘째 칸 Enter 입력으로 켤 수 있었다. 템포 End 입력은 112→180BPM, 재생/정지 버튼과 현재 칸 표시가 바뀐다. | 트랙×시간 구조를 장면·자막·음성으로 재해석한다. 반복 재생을 해도 편집값을 잃지 않게 한다. |
| 작업실 `#sim-std-main`, `#std-mix`, `#sim-std-arrange`, `#std-save`, `#std-wav` — `music_lab` | 코드·드럼·베이스·선율을 한 작업에 합치고, 구간별 트랙 on/off, 믹서, 브라우저 저장·링크·WAV 출력 UI가 있다. 저장·공유·WAV 내보내기는 이번에 실행하지 않았다. | 15장에 모든 조작을 펼치기보다 목표 선택→관련 편집→검수→원리 복습을 이어 준다. 웹 모형과 실제 키트 출력의 역할을 표시한다. |

설명은 행렬·배음 원리를 소개한 뒤 편집기를 놓고, 조작 설명과 결과 수치를 붙인다. 시퀀서 한 도구만 해도 모바일 높이 약 1,760px로 입력·결과·해석이 떨어진다. 기본 상태에서 많은 트랙·프리셋·심화 옵션을 동시에 보여 주는 방식은 입문 교재에 그대로 가져오기 어렵다.

기술 근거 `music_inspect`, `music_bundle`, `music_grid_listener`, `music_bpm_listener`: `#seq-grid .cell`의 직접 리스너 목록은 비었지만 **부모 `#seq-grid`에 click 위임**이 있었다(본문 HTML 0기준 505행). 자식에 리스너가 없다고 비작동으로 결론내리면 안 된다. range input은 공통 helper(0기준 268행)다. `MB.Clock`은 공통 script에서 오디오 시각을 기준으로 120ms 앞을 예약하고 25ms 간격으로 채우며, 화면은 requestAnimationFrame으로 갱신한다. 이는 코드의 설정값이고 실제 기기 지연 보장값이 아니다. 이 구조를 참조해 음성과 화면에 서로 독립된 타이머를 두는 일을 피한다.

접근성은 부분적이다. 시퀀서 셀은 이름 있는 native button이라 Enter가 작동하지만 켜짐 상태는 관찰한 마크업에서 class로 표시되고 `aria-pressed`는 없었다. 배음 Canvas에는 role·이름·키보드 막대 편집이 확인되지 않았다. 키보드로 소리를 내는 기능과 배음 편집의 키보드 대안은 구분해야 한다.

### NetworkBook — 보이지 않는 과정을 상태와 단계로 드러낸다

**뛰어난 점:** 도착한 결과만 보여 주지 않고 현재 단계·양쪽 상태·변한 데이터·시간 비용을 연결한다. 같은 원리를 정상 상황, 손실 복구, 통합 사례에서 반복한다.

| 관찰 위치·근거 | 관찰 내용 | ReelsBook에 가져올 판단 |
|---|---|---|
| 표지 계층 지도·학습 경로 — `network_cover` | 연결된 계층 지도와 목적별 읽기 순서가 있다. | 자동화 전체 지도에서 ‘파일 안의 문제’와 ‘전송 중 문제’의 위치를 구분한다. |
| TCP `#hs-next`, `#hs-prev`, `#hs-reset`, `#hs-desc` — `network_tcp`, `network_actions` | 0/11→1/11→2/11→3/11에서 양쪽 상태가 CLOSED/LISTEN→SYN_SENT/SYN_RCVD→ESTABLISHED/SYN_RCVD→양쪽 ESTABLISHED로 바뀌었다. 이전은 2/11 상태를 복구, 초기화는 0/11을 복구했다. | 게시의 요청·처리·완료를 분리한다. 이전 단계 탐색은 교육용 상태 탐색이며 실제 요청 취소가 아니라는 의미를 화면에 반영한다. |
| TCP `#rel-lose`, `#rel-go`; 웹 `#sim-abr`, `#abr-pre`, `#abr-alg`, `#abr-buf` — `network_actions`, `network_apps` | 마지막 패킷 손실 선택·전송을 실행했다. 재전송 시간의 정량 비교는 하지 않았다. 웹 장에는 네트워크 프리셋·직접 곡선 그리기·방식 비교·예측 문제가 있다. 직접 그리기와 모든 비교 결과는 실행하지 않았다. | 정상·처리 지연·접근 불가 등의 결정된 가상 응답을 골라 복구 판단을 연습한다. 랜덤 오류만 보여 주지 않는다. |
| 종합 도구 `#sim-trip`, `#jnext`, `#jall`, `#jmode`, `#jdesc` — `network_lab`, `network_journey_actions` | 다음은 0/17→1/17, 끝까지는 17/17. 릴레이에서 직접 연결로 전환하면 **경로를 새로 만들며 0/16으로 초기화**됐다. | 흐름 분기는 설명만 바꾸는 탭이 아니라 실제 단계 수·현재 위치와 일관돼야 한다. 수익 경로·게시 경로에도 적용할 수 있다. |

단계별 본문은 원리→시각 도구→현재 단계 설명→조작→누적 결과 순이다. 웹 장에는 조작 뒤 예상 답을 고르는 질문이 있으며, 항상 ‘예측→조작’ 순서를 강제하지 않는다. 통합 여행은 공통 장면 하나로 여러 장을 다시 연결한다. 책의 원리와 도구를 서로 돌아갈 수 있게 하는 것이 핵심이다.

기술 근거 `network_inspect`, `network_bundle`, `network_listener`: 장별 지역 상태와 `NB` helper를 사용한다. `#jnext`는 본문 HTML 0기준 829행에 등록됐다. 자동 단계 간격은 소스 설정상 3,800ms, 단계 전이 계수는 초당 0.8로 약 1.25초에 완료되며 프레임별 선형 증가다. CSS 이징과 이 단계 이동을 혼동하지 않는다. 지속적인 UI/그림 갱신은 화면 가시성 helper와 연결된다.

책 전체 장치에는 **읽기 위치·최근 장·퀴즈 응답 저장과 복원** 코드가 있다(`js/common.js`, `nb-progress-v1`). 읽은 비율 최대값 92%에서 읽음 처리하는 코드도 있다. 이는 정적 확인이며 재접속 복원 전체를 실행 검증하지 않았다. 이전 ColorBook 표본의 테마 저장만 관찰한 결과와 구별한다. 우리 책은 읽기와 실제 결과물 완료를 합치지 않는다.

### YieldBook — 먼저 증거를 고르고, 추측의 대가를 체험한다

**뛰어난 점:** 정답 선택보다 ‘어떤 자료가 필요한가’를 조작하게 한다. 같은 단서 다시 보기, 조사 비용, 오답 비용, 범위·복합 원인의 구별이 판단 과정을 남긴다.

| 관찰 위치·근거 | 관찰 내용 | ReelsBook에 가져올 판단 |
|---|---|---|
| 표지 추리 지도·사건 진입 — `yield_cover` | 원리 장에서 추리 도구로 연결한다. | 검수 장과 작업실에서 같은 가상 콘텐츠를 이어 다룬다. |
| 패턴 `#sim-atlas`, `#at-view`, `#sim-ov`, `#sim-quiz` — `yield_patterns` | 단일 패턴, 겹친 패턴, 랜덤 변동을 비교하게 하고 분류 연습 UI를 둔다. 해당 장의 모든 프리셋과 10문제는 실행하지 않았다. | 광고 표시를 고쳐도 권리·사실 오류가 남는 복합 상황을 만든다. 단일 위험 점수로 압축하지 않는다. |
| 공통성 `#cm-step`, `#cm-guess`, `#sim-cc`, `#sim-dp` — `yield_commonality` | 관찰자료만의 비교와 추가 실험의 비교를 구별한다. | 지표가 떨어졌다고 즉시 대본·자막 탓으로 정하지 않고 비교 대상을 확인하게 한다. |
| 수사실 `#dt-i-bins`, `#dt-i-common`, `#dt-log`, `#dt-submit`, `#dt-msg` — `yield_lab`, `yield_actions` | 관찰 사건 YD-3503에서 예산 14→빈별 맵 후 13→같은 맵 재열람 후 13→공통성 후 11. 베이스라인을 잘못 지목한 뒤 7로 줄고 오답 문장이 나왔다. 즉 조사 1·2, 오답 4의 비용을 별도로 체험했다. 이 숫자는 가상 게임 규칙이다. | 검수에서는 열어 본 근거와 남은 질문을 기록하고 재열람을 쉽게 한다. 실제 법률 판단을 게임 점수로 보증하지 않는다. |

규칙→사건/가상 데이터→조사 선택→단서 누적→원인·범위 제출→피드백/사후 해설의 흐름이다. 정답을 공개하기 전에도 증거가 행동의 이유를 설명한다. 사건 번호로 같은 상황을 다시 여는 UI가 있지만, 이번 동작 표본은 무작위 생성 사건을 사용했다. 문서에 남긴 번호는 관찰 식별자다.

기술 근거 `yield_inspect`, `yield_bundle`, `yield_submit_listener`: 공통 UI, `wafer.js` 계산·그리기, 장 내 지역 사건 상태를 조합한다. 제출 버튼은 본문 HTML 0기준 878행에 등록됐다. `#dt-msg`에는 `aria-live="polite"`가 있다. 사건·예산을 DOM 수치로 제공하지만 Canvas 그림 자체는 이름·대체 설명이 충분하지 않다. `yield_imports`는 캡처한 장 script의 **ES module import 0건**을 반환했다. 일반 script 태그·전역 helper 호출을 추적한 결과와 혼동하지 않는다.

## 3. 인터랙션 유형 카탈로그

아래에서 ‘화면/정적’은 UI·마크업·스크립트 관찰이고 ‘실행’은 입력 후 변화를 확인한 범위다.

| 패턴 | 무엇을 조작하는가 | 학습 목적과 피드백 | 근거·확인 수준 |
|---|---|---|---|
| 연속 변수 | 촬영 설정, 템포, 무늬 강도 | 같은 대상의 변화량을 숫자·색·그림으로 연결 | `camera_actions`, `music_actions` 실행; 나머지 장 UI |
| 이산 프리셋 | 셔터 각도, 파형, 패턴, 경로 | 대표 조합을 출발점으로 주고 손으로 수정 | `camera_video_actions`, `music_add_actions` 실행 |
| 직접 드래그 | 배음 막대 높이 | 입력 위치를 진폭으로 바꾸고 파형·지표를 다시 계산 | `music_add_listener` + CDP 드래그 실행 |
| 직접 곡선 그리기 | 시간별 대역폭 | 독자가 그린 실패 조건에서 재생 품질을 비교 | `network_apps` 화면/정적만 |
| 같은 장면 비교 | fps·표준/Log·미세 타이밍 | 원본 내용은 고정하고 표현·시간만 바꿈 | `camera_video_actions` 일부 실행, 나머지 UI |
| 재생/정지·단일 프레임 | 시퀀서, 셔터 움직임 | 인상과 순간 상태를 오가며 확인 | `music_actions`, `camera_video_actions` 실행 |
| 이전/다음·자동 단계 | 연결·패킷 이동 | 상태 변환과 누적 시간을 단계 설명으로 연결 | `network_actions`, `network_journey_actions` 수동 단계 실행; 자동 간격 정적 확인 |
| 실패 주입 | 패킷 손실·타임아웃·밝기 보정 해제 | 정상 전제와 복구가 필요한 지점을 드러냄 | `network_actions` 손실 선택/전송 실행, 정량 복구 비교 미수행 |
| 조건 충족 미션 | 촬영 설정 조합 | 목표를 여러 독립 조건으로 보여 주고 힌트→재시도 | `camera_actions` 실행 |
| 증거 선택·시나리오 분기 | 조사 종류, 가설, 원인·범위 | 조사 로그·남은 예산·오답 설명으로 사고 과정 표시 | `yield_actions` 실행 |
| 트랙×시간 격자 | 박별 on/off·세기·뮤트 | 부분이 전체 재생에 기여하는 방식을 분리 | `music_actions` 두 셀·템포·재생 실행; 믹서/편곡 UI |
| 관찰 보기 전환 | 파형·빈별·스택·샷 경계 | 계산 대상과 관찰 표현을 나눔 | `yield_actions` 빈별; `camera_video`·`yield_patterns` UI |
| 예측 질문·해설 | 조작 결과에 대한 선택 | 숫자만 보는 것을 넘어 원인을 문장으로 설명 | `network_tcp`, `network_apps` 화면/정적; 정오답 채점 실행 미수행 |
| 통합 작업·복습 지도 | 미션, 작업실, 사건 | 앞 장의 개념을 새 조합에 적용하고 관련 장 복습 | 네 책 종합 페이지 화면/정적, 일부 미션 실행 |

### 설명 문장의 위치와 정보량

공통적인 외곽은 제목/목표→보기→입력→수치→짧은 관찰 안내다. 실제 배치는 책과 도구마다 다르고, 수치와 조작이 별도 행에 놓이기도 한다. 본문을 모두 읽은 뒤에야 조작을 이해할 수 있게 하지 않는 점이 좋다. 반면 조작 안내 안에 여러 실험이 긴 문장으로 들어가면 모바일에서 읽기 부담이 커진다.

ReelsBook에서는 STYLE-GUIDE의 **먼저 답부터→한눈에 보기→축별 설명→해 보기**를 유지한다. ‘예측→조작→관찰→설명’은 복잡한 전역 새 틀이 아니라 도구 안에서 다음 네 줄로 쓴다: 예상 고르기(선택)→한 변수 바꾸기→대표 숫자 하나+해석 한 문장→실제 실습으로 옮길 행동. 원 사이트처럼 장마다 도구를 여러 개 연속해서 붙일 필요가 없다.

## 4. 시각 언어·모바일·접근성

| 항목 | 관찰 사실과 근거 | 적용 시 판단 |
|---|---|---|
| 도식 | 설명용 인라인 SVG와 조작/연속 변화용 Canvas 2D 조합. Camera는 장면/촬영 HUD, Music은 파형/격자, Network는 경로/상태, Yield는 맵/범례. `*_inspect`, `*_screen` | 생성물 미리보기·시간 편집·상태 흐름의 역할을 구분한다. 클릭 가능한 노드에는 native button·목록 대안이 있는 SVG/HTML을 우선한다. |
| 색 | 밝은 바탕·얇은 경계·강조색·보조색 구조. CSS의 라이트 강조색은 Camera `#d9480f`, Music `#6741d9`, Network `#0a6cc9`, Yield `#3b5bdb`. 다크 토큰 별도. | 원본 팔레트를 복제하지 않는다. 우리 책의 승인/보류/현재 위치를 색과 문장·아이콘으로 함께 표시한다. |
| 위계 | CDP 표본: 본문 17px/29.75px, 모바일 16px/28px. 장 제목 46px→32px, 절 제목 28px→24px. 도구 제목 17px, 보조 설명 14px. | 실제 읽기·입력값·해석에 위계를 둔다. 글자 크기를 단순 축소해 입력을 한 줄에 욱여넣지 않는다. |
| 화면 밀도 | 데스크톱 장 본문 880px, 도구 제어 열 280px 사례. 모바일 375px 창에서는 세로 스크롤바 15px를 제외한 clientWidth 360px, 본문 328px. | 이 수치를 우리 본문 폭 요구로 바꾸지 않는다. ReelsBook 680~720px를 기본으로 필요한 도구만 확장한다. |
| 모션 | CSS drawer 250ms ease, 배경 dim 200ms(기본 easing ease), 카드 hover 150ms. Music 건반 배경 60ms, 패드 50ms. Network 자동 단계 3.8초, 이동 약1.25초 선형. curl CSS·REA 캡처 소스 근거. | 강조 전환과 교육용 시간축을 구분한다. 실제 영상 재생은 미디어 시각을 기준으로, 단계 설명은 독자의 다음 버튼을 기준으로 한다. |
| 동작 줄이기 | 표본 공통 loop는 화면 밖에서 rAF를 쉬지만, 읽은 CSS·helper에서 `prefers-reduced-motion` 분기는 찾지 못했다. 시나리오에 reduced motion 설정을 주는 것만으로 사이트 대응이 입증되지 않는다. | 명시적 재생·정지·단계 이동을 기본으로 하고, 줄이기 설정에서는 자동 루프를 끄고 정적 결과를 유지한다. |
| 모바일 격자 | Music `#seq-grid` 자체 가로 스크롤, 행 최소460px. 첫 셀 실측 약28.2×26px. CDP 최종 표본의 문서 scrollWidth=clientWidth=360px. | 내부 스크롤과 문서 넘침을 구분한다. 짧은 화면에서는 장면 목록·이전/다음·시간 숫자 편집을 제공한다. |
| 모바일 경로 | Network `#cv-trip` 최소720px, 바깥 보기에서 내부 가로 스크롤. 문서 전체 너비는 넘치지 않았다. | ‘문서 가로 넘침 없음’만으로 합격하지 않는다. API 흐름은 세로 단계 목록으로 전환한다. |
| 터치 | 배음 Canvas의 `.harm-edit`는 `touch-action:none`, 포인터로 막대를 편집한다. Camera는 장면 클릭으로 AF 위치를 바꾼다. | 그림을 끄는 동안 페이지 스크롤을 막는 범위를 좁힌다. 숫자 입력과 위치 프리셋을 제공한다. 실물 터치 제스처는 이번에 검증하지 않았다. |
| 키보드·이름 | REA로 range Home/End, 시퀀서 셀 Enter를 실행했다. 반면 방문한 주요 Canvas들은 tabIndex −1, role/aria-label/내부 대체 문장 없음. Camera 설명 SVG에는 이름 있는 사례가 있다. | 버튼·range의 키보드 가능성과 그림 자체의 접근성을 따로 검사한다. 생성물·차트의 핵심 결과를 DOM 문장과 목록으로 제공한다. |
| 상태 전달 | 일반 segmented button은 aria-pressed를 갱신하지만 Music 셀은 class로 켜짐을 나타낸다. Yield `#dt-msg`는 polite live region. | 셀·보기 모드에는 상태 속성을 붙이고, 연속 입력 결과는 과도하게 읽지 않게 묶어서 알린다. 색만으로 정오답을 표시하지 않는다. |

최종 CDP 모바일 표본 4개는 모두 `scrollWidth=clientWidth=360`이었다. 이는 **375px 창에서 문서 전체 넘침 검사**이며 내부 패널 가로 스크롤·조작 난도·전체 장 모든 상태·스크린리더 적합성을 보증하지 않는다. Music·Network 도구는 특히 모바일 대안이 필요하다. 원 사이트 스크린샷은 분석용으로만 보고 이 저장소에 넣지 않았다.

## 5. 기술·성능·책 전체 장치

### 구현과 성능

일반 script, 공통 네임스페이스/helper, 장별 지역 상태가 중심이다. 번들 분석에서 Camera/Music/Network 각4개, Yield6개 script가 파싱 성공했고 파싱 실패는0이었다. 외부 CDN은 기본 origin 필터로 제외되므로 ‘React 등 의존성 전혀 없음’으로 확대하지 않는다. 직접 import 간선이 없다는 것과 일반 script 의존성이 없다는 것도 다르다.

| 표본 | 공통 JS 디코딩 크기 | 공통 CSS 디코딩 크기 | 같은 origin의 추가 주요 JS |
|---|---:|---:|---|
| Camera 영상 | 79,787B | 30,365B | 용어 데이터24,565B·tooltip11,036B |
| Music 시퀀서 | 99,584B | 37,171B | 용어 데이터25,264B·tooltip11,036B |
| Network 통합 여행 | 56,126B | 35,224B | terms110,494B·tooltip11,036B |
| Yield 수사실 | 45,196B | 34,422B | wafer46,281B·용어 데이터62,575B·tooltip11,036B·shared shell1,736B |

근거는 `*_inspect`의 resources/content_size와 curl CSS 바이트 교차 확인이다. **압축 전송량·문서/폰트/이미지/CDN 포함 총량·초기 다운로드 비용이 아니다.** 장 inline script는 이미 HTML에 포함되므로 별도 파일처럼 합산하면 중복된다. 참고로 캡처한 inline JS는 Camera 영상7,844B, Music 시퀀서46,883B, Network 여행43,949B, Yield 수사실56,231B였다(`*_bundle`).

일부 방문 장에는 KaTeX0.16.9 CSS/JS·auto-render, 글꼴 CDN, Cloudflare beacon이 있었다. CDP의 Music 표본에서 KaTeX JS 디코딩 크기는277,038B였다. 같은 origin 번들 분석만 보고 이 비용을 빼먹으면 안 된다. Resource Timing은 이미 여러 번 방문한 캐시 환경이므로 짧은 duration과 transferSize0을 일반 독자의 로딩 속도로 인용하지 않는다. 냉시작·저사양 FPS·Lighthouse는 측정하지 않았다.

공통 Canvas는 ResizeObserver·DPR 상한2·테마 변경 재그리기, 애니메이션 helper는 IntersectionObserver로 화면 밖 루프 중단을 처리한다. 이는 **연산을 쉬는 것**이지 도구 코드의 지연 다운로드가 아니다. 용어 도우미는 script/link를 동적으로 붙여 데이터를 읽는 경로가 있지만 도구 전부가 viewport 진입 시 코드 분할되는 구조는 확인하지 못했다. 우리 책도 이미지·재생 자원의 지연 로드와 계산 루프 중단을 각각 설계해야 한다.

### 책 전체 학습 장치

| 장치 | 실제 표본 | ReelsBook 판단 |
|---|---|---|
| 읽기 위치·절 목차 | 네 책 공통 상단 스크롤 막대·현재 절 표시. Network는 위치·읽음·최근 장 저장 코드까지 확인 | 이미 있는 결과물 완료 체크를 유지하고, 스크롤 진도와 분리 |
| 복습·퀴즈 | 대표 장 끝 퀴즈·해설 구조, Camera 미션별 관련 장 표, Music 작업실 지도, Network 종합 병목 문제, Yield 사후 해설 코드 | ‘틀린 이유→관련 절→같은 예제 다시 조작’으로 연결. 퀴즈를 늘리는 것보다 회복 경로 개선 |
| 용어 | 각 책 용어 데이터와 동적 tooltip, 용어집 링크. 검색·popover의 모든 키보드 상태는 이번에 시험하지 않음 | 기존 용어집의 정의 재사용, 도구를 벗어나지 않는 짧은 설명·관련 장 링크 |
| 장 사이 연결 | 목적별 추천 순서·공통 장 지도·관련 원리 장·이전/다음 | 이론→실습 이동 때 현재 결과를 요약해 넘기되 초기 예시와 실제 입력을 구별 |
| 종합 공간 | Camera 조건 미션, Music 다중 트랙 작업실, Network 하나의 여행, Yield 새 사건 | 15장에 모든 패널을 복제하기보다 기존 원본 도구를 목표 단위로 재사용 |

저장 UI·내보내기 UI의 존재와 실제 성공을 구별했다. Music 저장/WAV·마이크·파일 다운로드·클립보드는 실행하지 않았고, Network 진도 복원은 코드로만 확인했다. 음성 재생은 UI 및 엔진 동작 관찰이며 청취 품질·기기 오디오 지연을 검증한 것이 아니다.

## 6. ReelsBook 고도화 제안 20개

읽기 기준은 [STYLE-GUIDE](STYLE-GUIDE.md)가 우선이다. 장마다 새 도구를 추가하는 목록이 아니라 기존 1~2개 도구의 개선 후보다. 작업 시점에 `ch03.js`의 수입·비용 입력, `ch7-cards.js`의 글자 수/크기/대비 모형, `ch8-reels.js`의 균등 장면 배분, `publishing.js`의 예약/가정 한도 계산, `safety.js`의 항목별 자기 점검이 있음을 읽었다. 다른 작업자가 개편 중이므로 아래 제안의 현재 구현 차이는 착수 시 다시 확인한다.

난이도는 **S: 기존 UI·계산 재사용**, **M: 새로운 상태·연동·검증 필요**, **L: 시간/음성/파일 처리 통합 필요**라는 상대 평가다. 기간 추정이 아니다. P0는 먼저 검토할 상위5개, P1은 그다음, P2는 효과를 확인한 후의 선택 후보다. 참고 근거는 교육 패턴이며 인스타그램 정책·요건의 근거가 아니다. 정책·요건·수치에는 기존 research 출처와 ‘2026년 10월 조사 기준’을 적용한다.

| ID·패턴 | 참고 근거 | 어느 장·실습에 어떻게 적용 | 기대 학습 효과 | 난이도 | 우선순위 |
|---|---|---|---|---|---|
| R01 돈의 네 갈래 조작형 흐름 | Network 경로 분기 `network_journey_actions`, Camera 표지 과정 지도 | 3장: 네 축 선택→돈을 보내는 쪽·독자가 하는 일·받는 조건·남는 돈을 연결. 기존 입력 계산으로 내려가기 | 조회수와 실제 돈의 흐름을 연결 | M | P0·1 |
| R02 실제 문안 카드 편집기 | Camera 같은 장면/조건 미션 `camera_actions`, `camera_video` | 7장·실습4: 글자 수로 합성 문장을 만드는 모형을 실제 연습 문안 편집·줄바꿈·잘림 미리보기로 개선 | 바꾼 문장이 배치에 미치는 영향 학습 | M | P0·2 |
| R03 재생 가능한 릴스 타임라인 | Music 격자/오디오 시계 `music_actions`, `music_inspect`; Camera 프레임 정지 | 8장·실습5: 장면·자막·음성 트랙, 재생 헤드, 구간 반복, 숫자 시간 편집. 균등 배분 계산에서 실제 관찰로 확장 | 읽는 시간과 듣는 시간을 체험 | L | P0·3 |
| R04 게시 단계 시뮬레이션 | Network 연결 상태/이전·다음 `network_actions` | 10장·선택 실습8: 파일 준비→공개 URL 확인→요청→처리 상태 확인→게시→결과 확인을 가상 단계로 탐색 | 요청 성공과 게시 완료를 구별 | M | P0·4 |
| R05 상황별 검수 분기 | Yield 조사·단서·오답 `yield_actions` | 12장·실습6: 가상 콘텐츠의 증거를 먼저 고르고 권리·정확성·표시·보안을 각각 보류/수정/확인 | 막연한 자기 체크를 근거 있는 판단으로 개선 | M | P0·5 |
| R06 파이프라인 고장 실험 | TCP 손실 주입 `network_tcp`, `network_actions` | 9장: 생성물 누락·사람 승인 대기·처리 오류 가상 상태를 고르고 실패 단계·다음 행동 보기 | 무조건 재실행하는 실수 감소 | M | P1 |
| R07 질문별 짧은 학습 경로 | 네 표지 `*_cover` | 표지·1장: 카드 첫 제작/릴스 첫 제작/수익 구조 이해의 짧은 경로와 결과물 연결 | 초보자가 지금 할 일을 선택 | S | P1 |
| R08 제목·대본 A/B 비교 | Camera 동일 장면 비교 `camera_video` | 6장·실습3: 같은 사실·분량을 고정하고 제목/도입만 바꾸며 어떤 질문에 답하는지 비교 | 표현 변화와 사실 변화 구별 | S | P1 |
| R09 수정 전후·보조 보기 | Camera 프로필/파형 `camera_video`; Yield 빈별 보기 | 7장: 같은 카드의 수정 전/후·작게 보기·흑백·출처 영역 표시 | 수치만으로 놓치는 읽기 문제 발견 | S | P1 |
| R10 자막 실패→한 항목 복구 | Camera 조건 미션 `camera_actions` | 8장: 너무 긴 자막 프리셋→문장 축약 또는 시간 늘리기→동일 장면 다시 재생 | 원인 하나씩 고치는 습관 | S | P1 |
| R11 지표 원인 탐정 | Yield 공통성 `yield_commonality`, 단서 `yield_actions` | 11장·실습10: 가상 지표를 보고 기간·분모·콘텐츠 차이를 먼저 확인한 뒤 추가 실험 선택 | 상관관계를 성과 원인으로 단정하는 오류 감소 | M | P1 |
| R12 한 달 운영 목표 미션 | Camera 목표 조건 `camera_lab`, Network 지연 예산 `network_lab` | 14장: 독자 시간 예산 안에서 제작·검수·휴식을 배분하고 초과 구간 조정 | 남는 시간 없이 채우는 계획의 한계 관찰 | M | P1 |
| R13 목표별 통합 실험실 | 네 종합 도구 `*_lab` | 15장: 카드 읽기 점검/릴스 시간 맞추기/게시 오류 이해 목표를 골라 기존 원본 도구와 복습 절 연결 | 앞 장 지식을 한 과제로 통합 | M | P1 |
| R14 용어의 문맥 설명 | 네 `*_inspect` tooltip 자원·용어집 연결 | 6~10장: 토큰·공개 URL·비트레이트 등을 입력 옆에서 한 문장 설명하고 용어집으로 이동 | 화면을 떠나지 않고 조작 의미 이해 | S | P1 |
| R15 퀴즈→틀린 개념 재실험 | Network 문제·진도 코드, Camera 미션별 복습 표 | 장 끝 퀴즈: 오답 해설에 관련 도구의 시작 프리셋 링크. 실제 완성 체크와 퀴즈 점수 분리 | 읽은 설명을 조작으로 다시 확인 | S | P1 |
| R16 정보원·권리 증거 분리 | Yield 서로 다른 조사 `yield_lab`, `yield_patterns` | 5장·실습3: 소재 발견과 이미지/음성 사용 허락을 서로 다른 칸에서 확인 | 출처 표시만으로 권리 문제 해결했다고 오인 방지 | M | P1 |
| R17 숫자 입력·버튼 동등 조작 | Music 셀 Enter 성공과 Canvas 편집 한계 | 7~10장: 드래그마다 숫자/앞뒤 버튼, 현재 상태 문장, 선택 상태 속성 제공 | 터치·키보드·그림 접근 경로 확대 | M | P1·모든 P0의 수용 조건 |
| R18 한 변수씩 바꾸는 예측 질문 | Network 웹 예측 문제 `network_apps`, Camera 비교 | 2·3·11장: 예상 선택 후 변수 하나만 바꾸고 결과와 이유를 한 줄로 설명 | 조작을 무작위 놀이에서 가설 확인으로 전환 | S | P2 |
| R19 편집값 포함 학습 메모 | Music 저장/공유 UI `music_lab` | 7·8·14장: 입력·가정·선택·미해결 항목을 텍스트 복사. 비밀 값/계정 정보 제외 | 실습으로 옮길 의사결정 기록 | M | P2 |
| R20 읽기 재개와 산출물 완료 분리 | Network `nb-progress-v1` 정적 확인 | 공통 내비: 최근 절 재개와 내 결과물 완료를 다른 표시로 유지, 저장 불가 안내 | 스크롤 완료를 실습 완료로 오인 방지 | S | P2 |

## 7. 상위 5개 화면 스케치와 동작 명세

아래 문구와 구조는 우리 책용으로 새로 만든 개념 스케치다. 실제 정책 값·API 계약은 구현할 때 research 및 키트와 맞춘다. 각 화면은 ‘해 보기’ 도구 하나 안에 들어가며, 이론 설명·FAQ·실습을 중복해서 늘리는 용도가 아니다.

### R01 — 3장: 어느 행동이 돈으로 이어질까

```text
돈은 이 네 경로에서 들어옵니다. 하나를 골라 보세요.
[협찬] [제휴] [내 상품·서비스] [플랫폼 기능]

  돈을 보내는 쪽 ── 내가 하는 일 ── 돈을 받는 조건
       [노드]            [노드]             [노드]
                         ↓
              들어온 돈 − 비용·환불 = 남는 돈

선택한 경로: 제휴
연습 입력 [판매 금액] [인정된 건수] [요율]
결과 [가상 계산 금액] / “구매가 인정되어야 계산에 들어갑니다.”
[이 경로의 조건 읽기] [내 계획에 적기]
```

참고: `network_journey_actions`의 경로 전환→단계 재구성, `camera_cover`의 과정 지도. 네 축은 선택한 STYLE-GUIDE 구성에 맞추고 세부 서비스·상품·플랫폼 기능은 안에서 펼친다. 기존 수입 입력을 무조건 없애거나 정산 기준을 네 범주로 단순화하지 않는다.

| 입력 | 상태 | 출력 |
|---|---|---|
| 경로 버튼 | `route`, 선택 세부 경로; 이전 입력은 같은 경로 안에서 보존 | 관련 노드·조건·설명·입력 항목만 표시. aria-pressed와 제목 동기화 |
| 숫자 변경 | 입력값과 유효성. 빈칸·실제0·가상 기본값을 구분 | 공개된 식으로 금액 재계산. 대표 숫자 하나+해석 한 문장. 요율은 확인한 근거나 독자 가정 표시 |
| 설명 노드/조건 링크 | 선택 절 | 같은 장의 해당 설명으로 이동, 돌아왔을 때 선택 유지 |
| 초기화 | 해당 경로 연습값 | 가상 예제로 복귀했다는 안내 |

검증 조건: 경로를 바꿔도 숨은 값이 이중 합산되지 않는다. 조회수만 넣어 수익이 자동 발생하지 않는다. 모바일은 노드 세로 목록, 키보드는 버튼 순서로 같은 정보를 읽는다.

### R02 — 7장: 내 문안이 카드 안에 들어갈까

```text
한 카드에는 질문 하나만 담아 보세요.
┌────────────┬──────────────────┐
│ 휴대폰 크기 카드 미리보기 │ 제목 [직접 입력]              │
│ 제목 / 본문 / 출처        │ 본문 [직접 입력 여러 줄]      │
│ 잘린 부분에 표시         │ 글자 크기 [−] [값] [+]        │
│                         │ 여백 [값] / 색 조합 [선택]    │
└────────────┴──────────────────┘
결과 “본문이 연습 상자를 2줄 넘습니다. 마지막 문장을 줄여 보세요.”
[넘치는 예] [수정 전/후] [출처 위치] [기본값]
[실습4에서 실제 카드 만들기]
```

참고: `camera_video`의 내용 고정 비교, `camera_actions`의 조건별 판정. 기존 글자 수 기반 합성 문장을 직접 입력한 문안으로 바꾸는 것이 핵심이다. 일반 디자인 프로그램 전체를 만들지 않는다.

| 입력 | 상태 | 출력 |
|---|---|---|
| 제목·본문·출처 문자열 | 길이 제한을 둔 연습 문안, 선택 카드, 설정 | 같은 문안의 줄바꿈·넘침·출처 위치를 즉시 미리보기. 사용자 문자열을 HTML로 해석하지 않음 |
| 글자 크기·여백·팔레트 | 숫자 설정, 색 조합 | 해당 카드와 진단만 갱신. 숫자 필드와 range 동등 제공 |
| 넘침 예/기본값 | 복구 가능한 연습 프리셋 | 무엇이 바뀌었는지 표시. 수정 전/후는 같은 원문으로 비교 |
| 원리/실습 링크 | 현재 설정 요약 | 실제 PNG 생성·휴대폰 확인 단계로 연결 |

검증 조건: 긴 단어·한글·줄바꿈·빈칸·작은 출처·폰트 대체를 확인한다. 측정은 브라우저 연습 렌더링이며 Pillow 출력과의 일치를 주장하지 않는다. 결과물 색은 사이트 다크 모드와 독립이다. 텍스트는 그림 밖에서도 읽힌다.

### R03 — 8장: 이 자막을 끝까지 읽을 수 있을까

```text
       [세로 영상 미리보기]  현재 00:04.2 / 00:20.0
       지금 장면 / 지금 자막 / 음소거 표시
[재생] [정지] [이전 장면] [다음 장면] [이 구간 반복]

시간     0       5       10       15       20
장면     [도입][핵심1     ][핵심2    ][마무리]
자막     [A   ][B      ][C       ][D         ]
음성     [권리를 확인한 연습 음성 또는 무음     ]
                  ↑ 재생 위치
선택 자막 [문장] 시작 [3.0] 끝 [6.0] [−0.1초] [+0.1초]
결과 “이 자막은 3초 동안 보입니다. 직접 읽으며 맞춰 보세요.”
[빠른 자막 예] [수정 후 다시 재생] [실습5]
```

참고: `music_actions`·`music_inspect`의 트랙/시각 동기화, `camera_video_actions`의 프레임 정지. 기존 균등 배분 모형은 초기값 생성에 재사용한다. 웹에서 MP4 생성·음성 인식·TTS를 새로 제공하는 요구가 아니다.

| 입력 | 상태 | 출력 |
|---|---|---|
| 재생/정지/탐색 | 공통 현재 시각 `t`, playing, 선택 구간 | 미리보기 장면·자막·재생 헤드를 같은 시각으로 갱신. 별도 타이머로 트랙을 독립 진행하지 않음 |
| 시작/끝 숫자 또는 경계 드래그 | 유효한 구간 배열, 선택 자막 | 길이·총 시간·연습 읽기 부담 표시. 끝≤시작·범위 밖은 적용 전 오류 표시 |
| 음소거·구간 반복 | mute, loopRange | 무음 확인과 해당 범위 반복. 반복 종료 때 위치 일관성 유지 |
| 실패 프리셋→문장 수정 | 수정 가능한 초깃값, 변경 문장 | 같은 장면을 다시 재생하고 문장/길이 변경 효과 확인 |

검증 조건: 구간 경계의 중복·빈 틈, 처음/끝 탐색, 재생 중 변경, 탭 숨김 후 복귀를 확인한다. 모바일은 장면 목록·시간 숫자·대표 트랙 하나씩 표시한다. 소리 자동재생 금지, 자막을 DOM 목록으로 제공한다. 읽기 경고선은 가상 연습 기준이며 알고리즘 성공 공식으로 표시하지 않는다.

### R04 — 10장: 요청을 보냈는데 왜 아직 게시되지 않았을까

```text
교육용 게시 연습 · 가상 요청만 사용합니다
상황 [정상] [주소 접근 불가] [처리 지연] [응답 불명]

[파일]→[공개 주소]→[생성 요청]→[처리 확인]→[게시 요청]→[확인]
                           ↑ 현재 단계 4 / 6
현재 상태 “처리 중” / 지금 할 일 “완료 상태를 확인합니다.”
가상 기록  요청 종류 | 응답 상태 | 다음 판단
[이전] [다음] [자동 재생/정지] [처음으로]
결과 “처리 중에는 게시 단계로 넘어가지 않습니다.”
[실습8에서 실제 준비물 확인]
```

참고: `network_actions`의 양쪽 상태, 이전·초기화, `network_journey_actions`의 조건 변경 시 경로 재구성. 기존 한도 계산과 합쳐 한 화면에 모든 API 설정을 넣지 않는다. 기본 앱 게시 경로는 유지하고 선택 API 실습의 이해 도구로 둔다.

| 입력 | 상태 | 출력 |
|---|---|---|
| 정상/실패 상황 | 고정된 가상 응답 집합, 단계0, 실행 기록 초기화 | 현재 경로·설명·대표 상태. 실제 토큰·URL 입력을 요구하지 않음 |
| 다음 | 허용되는 다음 교육 상태 | 요청/처리/완료를 구분하는 가상 기록·도식·다음 행동 |
| 실패 상태에서 해결 선택 | 접근 불가/대기/완료 불명 등 분기 | 원인에 맞는 확인 순서. 응답 불명 때 무조건 재게시하는 답을 정답 처리하지 않음 |
| 이전/처음/자동 | 재생 위치 또는 자동 여부 | 일관된 설명과 버튼 상태. 이전은 실제 요청 취소 의미가 아님 |

검증 조건: 외부 요청0, 자격 증명 수집0. 키트의 승인·드라이런·중복 시도 방지와 모순되지 않게 한다. 실제 API 순서·응답 예는 검증된 research에 맞춘다. 모바일은 연결선을 줄이고 세로 단계 목록으로 보여 준다.

### R05 — 12장: 이 게시물을 내보내기 전에 무엇을 확인할까

```text
가상 사례: AI 그림·기사 요약·제휴 링크가 있는 카드
예상 [지금 게시] [고쳐서 게시] [근거부터 확인]

열어 볼 증거 [원출처] [이미지 허락] [광고 관계] [AI 사용] [보안]
단서 메모  확인한 것 / 아직 모르는 것
판단      권리 [보류] 사실 [수정] 표시 [확인] 보안 [확인]

선택 “출처를 달았으니 그림을 그대로 사용한다”
피드백 “이미지 사용 허락도 확인해야 합니다.”
[근거 다시 보기] [소재 교체] [누락 항목 확인]
결과 “남은 확인 1개: 이미지 사용 범위”
[실습6의 내 검수표로 이동]
```

참고: `yield_actions`의 조사→단서→가설 제출, `yield_patterns`의 복합 원인. 기존 항목별 점검을 버리지 않고, 입력을 고르는 이유를 연습하는 앞부분을 추가/대체한다. 본문 도구 수는 늘리지 않는다.

| 입력 | 상태 | 출력 |
|---|---|---|
| 가상 사례 선택·예상 답 | 사건, 예상 판단, 미확인 항목 집합 | 필요한 증거 목록. 실제 인물·계정이나 개인정보 입력 없음 |
| 증거 열기/재열람 | 열람 집합·단서 로그 | 새 단서 표시, 다시 열 때 중복 항목 추가 없음. 정보가 없으면 미확인 상태 유지 |
| 판단·수정 행동 | 권리/사실/표시/보안별 상태 | 바뀐 항목만 갱신. 다른 위험이 자동 해소되지 않음 |
| 검수표로 이동 | 남은 확인·행동 요약 | 실제 자산의 검수는 실습에서 진행. 가상 성공을 법적 허용/계정 안전 보증으로 표시하지 않음 |

검증 조건: 광고 표시만 수정해도 권리 문제는 남는다. 증거가 없는 상태와 확인된 허락을 분리한다. 예산 점수는 넣지 않는 것을 기본으로 한다. 필요하면 조사 순서 복습에만 쓰고 ‘안전도 100점’으로 바꾸지 않는다. 실제 세무·법 판단은 research의 확인 범위를 따른다.

## 8. 유튜브 쇼츠 편에 특히 유용한 패턴

ShortsBook은 아직 구현 대상이 아니다. [DESIGN의 영상 제작 중심 범위](DESIGN.md)에 대한 후속 설계 입력이며 이번에 파일·책을 만들지 않았다.

| 패턴 | 참고 근거 | 영상 제작 중심 활용 | 먼저 검증할 학습 질문 |
|---|---|---|---|
| 장면·자막·음성 공통 시간축 | Music 시퀀서/작업실, R03 | 짧은 예제 하나에서 컷·자막 시작/끝을 편집하고 프레임 정지·반복 재생 | “왜 자막이 말보다 먼저 사라질까?” |
| 같은 운동의 fps·셔터 비교 | Camera `#sim-fps`, `#sim-angle` | 동일한 자체 합성 동작으로 촬영 fps와 내보내기 fps를 구분 | “느리게 만들 때 왜 끊겨 보일까?” |
| 소리의 부분 듣기·뮤트·솔로 | Music 믹서/편곡 UI | 직접 제작한 예제 음성·배경음을 각각 듣고 함께 비교. 파형과 문장 설명 제공 | “음악을 넣으니 말이 안 들리는 이유는?” |
| 수치와 실제 미리보기 비교 | Camera 프로필/파형, Music 스펙트럼 | 원본/압축 예제·자막 확대·클리핑 표시를 번갈아 보기 | “파일이 작아지면 어느 부분이 먼저 깨질까?” |
| 목적이 다른 촬영 미션 | Camera 연습장 | 정적인 설명·손동작·움직이는 피사체 등 자체 장면별 성공 조건·힌트 | “이 장면에서는 무엇부터 맞출까?” |
| 제작 파이프라인 단계·실패 | Network 연결/손실 | 대본→녹음→자막→편집→검수→내보내기를 재생하고 누락 파일을 찾기 | “미리보기는 되는데 출력은 왜 실패할까?” |
| 복합 문제를 분리하는 증거 로그 | Yield 수사실 | 소리·화면·사실·권리 문제를 서로 다른 증거로 점검 | “음원 허락을 확인하면 영상 소재도 해결될까?” |
| 하나의 예제를 통합 작업실로 | Music 작업실·Camera 미션 | 대본·오디오·자막을 같은 짧은 자체 제작 예제로 이어 가고 실습 출력과 연결 | “이 설정을 내 영상에 어떻게 옮길까?” |

ShortsBook도 처음부터 다중 트랙 편집 프로그램을 만들 필요는 없다. R03의 단순 타임라인·프레임 확인·한 변수 비교를 먼저 검토하고, 브라우저 렌더러·실제 내보내기·미디어 라이브러리 도입은 별도 설계에서 정한다. CameraBook의 촬영 수치나 MusicBook의 이론 문장을 영상 권장 규격·저작권 근거로 재사용하지 않는다.

## 9. 따라 하지 않을 점과 구현 검토 순서

1. **원 사이트의 문장·HTML/CSS/JS·그림·음원·스크린샷을 교재 자산으로 복사하지 않는다.** 공개 라이선스 안내가 있어도 이번 작업은 패턴 분석으로 한정했다. 자체 가상 사례·SVG·합성 미디어·코드를 새로 만든다. 참고 URL은 출처로 남긴다.
2. 각 장에 대형 체험 여러 개를 쌓는 구성을 답습하지 않는다. 기존 원고 축약·FAQ·한 도구 원칙에 맞추고, 추가 조작은 심화로 접는다.
3. 드래그만 가능한 Canvas, 작은 셀, 색만으로 켜짐 표시, 설명 없는 가로 스크롤을 가져오지 않는다. 수치 입력·키보드·DOM 결과·모바일 단계 목록을 기본 수용 조건으로 둔다.
4. 자동 루프와 긴 설명 애니메이션을 읽기에 강제하지 않는다. 정지·한 단계·동작 줄이기·화면 밖 연산 중단을 제공한다.
5. 수익·도달을 물리식처럼 확정 예측하지 않는다. 가상 예제와 직접 확인한 실제값을 구분한다. 사이트의 계산 정밀도·게임 점수는 현실 보장 근거가 아니다.
6. 실패 주입을 실제 업로드·토큰 검증·유료 호출로 구현하지 않는다. 가상 상태로 충분하며 실제 실습과 명확히 구분한다.
7. 시뮬레이터의 성공을 결과물 제작·실제 게시·법적 허용으로 자동 인정하지 않는다. 기록·읽기·퀴즈·완료의 뜻을 분리한다.
8. 공통 helper 구조가 있다는 이유로 새 프레임워크·전역 상태 계층·범용 시뮬레이터 엔진을 만들지 않는다. 기존 정적 HTML·SVG·바닐라 JS와 원본 도구 재사용을 먼저 검토한다.

후속 구현은 P0 각각을 기존 도구와 비교→한 화면 프로토타입→학습자 질문으로 검토→375/360px·키보드·저장 실패·상태 전이 검증 순으로 진행할 수 있다. 이번 산출물은 이 결정을 위한 근거이며 구현 착수를 승인받은 것으로 보지 않는다. 정책 추가 조사나 새 API 계약 변경을 이번 관찰로 정당화하지 않는다.

## 부록 A. REA Evidence 대장

다음 ID는 이번 MCP 세션의 실제 반환값이다. `inspect_web_event_listeners` 위치의 행 번호는 CDP 기준0부터 센다. 소스에 없는 의존성·실행 경로를 ID만으로 추정하지 않는다. 원본 묶음과 수동 보완 자료는 저장소 밖 임시 경로에 있으며 본 문서가 지속되는 요약 근거다.

| 별칭 | REA 도구 | Evidence ID |
|---|---|---|
| `discovery` | `list_browser_targets` | `ev_eb0cbaff14f60c2eb62790509d4b21a2c24733d5fced4c34a950bbbd53cc6706` |
| `library` | `capture_browser_scenario` | `ev_d244e750cb929dc2a04383a74d91fb607866539f1b536cbca9ced3913cedfe2c` |
| `shelf` | `inspect_web_page` | `ev_5bd2fa0ae306eb15717cff5eaff25b9cbd36b1c26b8ac0bec39f5a424c1d650f` |
| `camera_cover` | `capture_browser_scenario` | `ev_0b4138dcf349adb2e2958885f8c40ab326d53d42aa6f978c52aa4efff416c3b4` |
| `camera_shutter` | `capture_browser_scenario` | `ev_2c8ab36cc661bfd8f30e0298a15932e7b4bd4246f115b9d2ec74b9b658c653c0` |
| `camera_video` | `capture_browser_scenario` | `ev_e9e2dd0bb762a5c0d39a590e34bc3d2f3193b26115fb4308ded731bcecb5936a` |
| `camera_lab` | `capture_browser_scenario` | `ev_4232b6fc9e4d64e956d517450f673441a1d66f906ffdde8870e3b8332e614760` |
| `music_cover` | `capture_browser_scenario` | `ev_12e5acf8b82069e8747f942f4a0031928e7aa7bae2895e358131c4a95c627e7b` |
| `network_cover` | `capture_browser_scenario` | `ev_e08d7d1dc549ff5170da2f1fa409983e348edd5f40215ef573d847f60269b0b7` |
| `yield_cover` | `capture_browser_scenario` | `ev_610174200fb8f73507446f06ab7d8c47ec9378758a661bca5ad892a58b968407` |
| `music_harmonics` | `capture_browser_scenario` | `ev_b0ceb354aa7e9ad712103ff6bbcd37a49be30e5184c89ccc6774c0a115d17d42` |
| `music_sequencer` | `capture_browser_scenario` | `ev_4bdb1cfc65384d49e2795c91aa0804dd050f35b1a9411fd8b95756a83bd3f382` |
| `music_lab` | `capture_browser_scenario` | `ev_26cd12dd68595512945dd5c5fc786e121d5d0e926e62d202a7d1b8c2c288d328` |
| `network_tcp` | `capture_browser_scenario` | `ev_96f17327ad8d52c5a0b5f5aa5a4f59f245393839456b1b25ed2c2672eb748d3e` |
| `network_apps` | `capture_browser_scenario` | `ev_384c257ecc4b2a209bb8297403110786bfd2cc9da63544c672445296a66d9798` |
| `network_lab` | `capture_browser_scenario` | `ev_6ee6592fa1bbef7633dc3d37495333dc4d4072a8a956c67ba876ee48702dc6d3` |
| `yield_patterns` | `capture_browser_scenario` | `ev_783578ddc6616ae186e92f28d6c4a01fb3d1fb65fbd53fbe7503bdc15932394a` |
| `yield_commonality` | `capture_browser_scenario` | `ev_b6f2a832cb37f5e4a309cb6ab2476340938045c2143314b4061b0d2d48aee306` |
| `yield_lab` | `capture_browser_scenario` | `ev_8bc5751eba38c2b27829e728974ce53f9fbc757a6fb665b4b35187bd93e4fed9` |
| `yield_inspect` | `inspect_web_page` | `ev_89654c89dd74a7045b2fe382856fc0ade74cfb0fd74b43465ebef15777a48207` |
| `yield_bundle` | `analyze_web_bundle` | `ev_543fa67cdde367126923ce837ea22311c4aa0ebaa2e97d30c62c7fc2481424fe` |
| `yield_listener` | `inspect_web_event_listeners` | `ev_25ca0b7150096b23a50f589adcd74c72869fd6b5ff8772533c7191de19cd2d1f` |
| `yield_submit_listener` | `inspect_web_event_listeners` | `ev_b0bdd866c8215ac1e8013d2765c159abd35572d7f1e54cd4f9459c8bb382e0c8` |
| `yield_screen` | `capture_web_screenshot` | `ev_3747c4f089c0aa6ff068124e54889885eb60aa7b66bbf63c714748946f5d3048` |
| `yield_scripts` | `export_web_scripts` | `ev_b155088c72fda8a71cc2d30da8be55b4fb8c4769b61f3d5de1189faa2cc5d3f8` |
| `yield_imports` | `trace_web_module_imports` | `ev_685ad3400aac26dd22dbc9693261e5d6ec61205a61ff38ffa4950eb4150485ee` |
| `yield_actions` | `capture_browser_scenario` | `ev_15eb22f437dcfa863a5d05af3721dd08bf49079e1d142abe2b0a8eee95248049` |
| `network_actions` | `capture_browser_scenario` | `ev_739adbfc72a6aff36beadd9f4683a4b522a4c4e7adf51ad2b6a8861e608a3e0c` |
| `camera_actions` | `capture_browser_scenario` | `ev_223e1ec112792adbd29b1951a1e8745b87c6103049a5d54c56883384d44197b0` |
| `music_actions` | `capture_browser_scenario` | `ev_096bdb3ceae775d9e65093b5733c429c84adfe505402ce92de53bfa025391537` |
| `music_inspect` | `inspect_web_page` | `ev_329eb8a114d998b3deb6370a5104b4a5a70c5a4a11fe3425a87f91e413fde0bf` |
| `music_bundle` | `analyze_web_bundle` | `ev_0437171f7c62546beed83c22bed92c7b8b9c07bed999218ab19733e05060bcae` |
| `music_listener` | `inspect_web_event_listeners` | `ev_15bc1618190237811c1b888865a675de58bdc5d30de9033ea269acc24d0f8623` |
| `music_screen` | `capture_web_screenshot` | `ev_374686ce30c59d400981255704cc8268cf6ed33eb40a7d56956351c54d24b220` |
| `music_grid_listener` | `inspect_web_event_listeners` | `ev_f379da194347cba329764ac42bd3424f66deeada6a696dc427b66eb2146826a8` |
| `music_bpm_listener` | `inspect_web_event_listeners` | `ev_9bd806f69872be39ea49e41e796363776e0cfdb047867614424581349b677228` |
| `network_journey_actions` | `capture_browser_scenario` | `ev_568635eb3cb1586b38c8deaae83bebb2710706287913651cb6fe08c953c44358` |
| `network_inspect` | `inspect_web_page` | `ev_6a0335b68956d243f40a9ce7d21533ed872dcaac879faa10ec1ee94f04a1d3aa` |
| `network_bundle` | `analyze_web_bundle` | `ev_eba134778c11ef11f9d6d2f1a56e19001fd3eda46ce2d7ef34567c9a5aaa35a0` |
| `network_listener` | `inspect_web_event_listeners` | `ev_114d825810a9b38ef38b96875861d3aedffcff7ef715dd4f75a7a917515dd1ae` |
| `network_screen` | `capture_web_screenshot` | `ev_2a280b381174d45720e65e374c2618998c8c6d851d505ead7545e47186e7f3f5` |
| `camera_video_actions` | `capture_browser_scenario` | `ev_5204666041152e15e6aa545ef6335344fe4bf681ff973624e7e3381f9dd69d2d` |
| `camera_inspect` | `inspect_web_page` | `ev_e0f3d12c188740d99c070999d7a39575d7c226a211f7f8de05fb10c057ce6b27` |
| `camera_bundle` | `analyze_web_bundle` | `ev_5184ce95cd71d801f50545a12ed3480954f260f023a0fbac7942996808d39e59` |
| `camera_listener` | `inspect_web_event_listeners` | `ev_953117a680629e4c57b1dc493a227ea374c9c43f7768938d1d704f3b88a26625` |
| `camera_screen` | `capture_web_screenshot` | `ev_d40b0209dcd3d80d21b889177eeded96d394f140b220d13663031928bc0efa95` |
| `music_add_actions` | `capture_browser_scenario` | `ev_ce3a933bf50a01ffc81b1ee6c7b721dd38ad792cd89f8461b0b508fa82e812e1` |
| `music_add_listener` | `inspect_web_event_listeners` | `ev_df94ef43d14cc509388cb396b48b3edd3f00786c1eb8024b1afd6772182b8e7b` |
| `music_mobile` | `capture_browser_scenario` | `ev_faa48821d9bfe583c3ef3c4c140d699e3550bf240ba8ee7174f626aa2788034f` |
| `music_mobile_screen` | `capture_web_screenshot` | `ev_4f4151465f979933a872f0644afe37da1c56b92c8cffcb5a9e686a897d4f1d88` |
| `music_mobile_cdp` | `capture_browser_scenario` | `ev_335bb1a64c617347f1b0d91bbf6a42f0f3dc7bdb0c57e80ebabb96199ca2064e` |
| `music_mobile_actual` | `capture_web_screenshot` | `ev_721bcc6b32a1cd6d9c2071f05530ae3d6b2b191d9b4fed84ce07a0dece65f652` |
| `music_mobile_375` | `capture_web_screenshot` | `ev_c86b93a05e89e58be9a44ef065fdb1e7cfb92b46dc7db7f44d6901864e0accf1` |
| `camera_mobile` | `capture_browser_scenario` | `ev_036040559f6cf3e494d69d7b49607e6e5c74977ef29cd19f9b9217c10be99a78` |
| `music_mobile_verified` | `capture_browser_scenario` | `ev_cd5af0e3af99f1d174584ae5971d60a8075699c24ba4598482871e7fc0808fda` |
| `network_mobile` | `capture_browser_scenario` | `ev_55d9cf878a7a0db11006e990f9384c23e57e3c170d8eb74ea9d21aa1c4320998` |
| `yield_mobile` | `capture_browser_scenario` | `ev_35215210e88876e292d0fcb06f4236aed89717095d8f1a3103ba155dc09e76a3` |

## 부록 B. 보완 관찰 재현과 경계

자체 보완 스크립트는 `/tmp/ai-insta-10r.1DGMei/supplement.cjs`에만 있다. 기존 설치 Playwright의 `chromium.connectOverCDP('http://127.0.0.1:9337')`로 같은 임시 브라우저에 붙었다. 최종 모바일은 연결을 유지한 채 `setViewportSize({width:375,height:812})`→대상 URL 탐색→700ms 안정화→동일 세션에서 screenshot·getComputedStyle·scrollWidth 측정 순서다. 네 표본의 자세한 측정은 `camera-mobile-final.json`, `music-mobile-final.json`, `network-mobile-final.json`, `yield-mobile-final.json`에 있다. 이 파일들도 임시 자료이며 저장소에는 넣지 않았다.

드래그는 배음 장 `#cv-add`의 실제 경계 상자를 얻어 폭의13%·높이18% 지점에서 누르고 폭22%·높이37%까지8단계 이동한 뒤 뗐다. 실제 포인터 입력 전후 `.sim-readout`을 비교한 값은 `cdp-drag.json`에 있다. DOM의 값만 바꾸고 드래그 성공이라고 보고하지 않았다.

CSS는 각 책의 위 `css/style.css` URL을 `curl -fsSL`로 임시 파일에 저장했다. 수동 관찰에는 REA Evidence ID를 붙이지 않는다. `music_mobile_screen`, `music_mobile_actual`은 종료 후1280px 캡처이고 `music_mobile_375`는 별도 크기 실험이며, 이름에 mobile이 있어도 최종 모바일 검증으로 사용하지 않았다. 네 `*_mobile` 시나리오는 동작/캡처 성공 기록이지만, 최종 화면 배치 판정은 위 CDP 네 표본을 따른다.
