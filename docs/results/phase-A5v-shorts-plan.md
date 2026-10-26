# Phase A5v-shorts — 쇼츠 심화편 시각자료 보강 계획

## 목표·범위

DESIGN-advanced 1.2절과 STYLE-GUIDE 6절에 따라 독자가 시스템 연결, 예외 분기, 설정 위치와 실제 출력 모습을 그림으로 이해하게 한다. 기존 SVG의 단순 단계 나열을 구체적인 연결·분기·비교로 바꾸고 중복 본문을 줄인다. 별도 설계·승인 단계 없이 사용자가 지정한 설계를 현재 작업 공간에서 직접 구현한다.

수정 범위는 `site-shorts/advanced/`, 쇼츠 전용 `site-shorts/assets/advanced-visuals.css`·`site-shorts/assets/img/advanced/`, 이 계획·결과·검증 자료뿐이다. PROJECT_STATE·공통 자산·키트·조사 자료·다른 책은 수정하지 않는다. 키트는 `/tmp/a5v-shorts-kit`에 비밀 파일과 기존 실행 상태를 제외하고 복사해 mock 실행한다. commit·push·실계정·유료 API 호출은 하지 않는다.

## 장별 대조표

| 장 | 그림 / 현재 부족한 점 → 작업 | 보여 줄 결론 | 데이터 근거 |
|---|---|---|---|
| A0 | 전체 단계 띠 → 시스템 구성도로 교체 | 실행기·공급자·상태·관문·게시·알림·분석이 연결되며, 공개 호스팅은 쇼츠 업로드에 불필요 | auto-kit README·pipeline.py·ops/state_sync.py; execution-hosting.md·youtube-api.md A019 |
| A0 | 운영 모드 표 → 전환·복귀 그림(A6에 배치) | 통과율과 예외 수를 직접 집계해 설정을 바꾸며 자동 승격은 없음 | 기존 A0 운영 제안(9/10·19/20, 플랫폼 규정 아님) |
| A1 | 상태 나열 → 정상·실패·연기·관문 예외·결과 불명 분기 | 실패는 같은 ID로 재개하고 결과 불명은 기존 세션부터 조회 | pipeline.py·state.py; youtube-api.md A019 |
| A1 | 폴더 카드 → 실제 들여쓰기 트리 | 실행 파일·공통 DB·인증 파일은 저장 위치와 공개 가능 범위가 다름 | auto-kit 실제 트리·새 mock 실행 출력 |
| A2 | 설정 주석 그림 신규 | mode·providers·budget·youtube 설정은 비밀 값 없이 config에 저장 | config.example.json 실제 키·기본값 |
| A2 | 생성 API 키·강제 상한 화면 위치 신규 | 공급자 프로젝트에서 키와 지출 제어를 따로 준비 | generation-apis.md·costs.md A081·A030·A115, A107 |
| A2 | 상한 계층 신규 | 실행 최대비 예약·일/월 상한·공급자 제어를 함께 확인 | README·providers/prices.json·config.example.json; A031 |
| A2 | 비용 비교 차트 신규(기존 계산기는 유지) | 영상 생성 추가가 LLM·TTS보다 예산을 크게 바꿈 | cost-model.json shorts-low/high; costs.md A025·A028·A038·A037. 월30편·600자·이미지6장은 견적 가정 |
| A3 | 생성 입출력 띠 → 실제 JSON 일부·스키마·오류 분기 | JSON 모양과 원문 정확성은 별도 검사 | providers/content.schema.json·adapters.py·gates; A026·A029·A033 |
| A4 | 실제 영상만 있음 → 실제 프레임 WebP 추가 | 제목·장면 자막이 실제 MP4에 어떻게 합성되는지 확인 | 새 mock의 short.mp4에서 프레임 추출, 원본 PNG와 대조. AI 생성 이미지 아님 |
| A4 | 조립 그림·실제 MP4 유지 | 장면 시간으로 배분한 자막은 직접 발화와 맞춰야 함 | rendering/media.py·실제 SRT·probe 결과 |
| A5 | OAuth 화면 위치 신규 | Console 설정 파일과 브라우저 동의 후 토큰은 서로 다른 결과 | youtube-api.md A017·A018·A024·oauth_setup.py |
| A5 | 기존 게시 시퀀스 유지·실패 분기 보강 | 중단은 같은 Location 조회, 만료·시작 결과 불명은 새 insert 금지 | youtube-api.md A019·A020, publishing/youtube.py |
| A5 | 기본량 비교 막대 → 할당량·로컬 cap 게이지 | 프로젝트 버킷과 낮춘 로컬 cap 중 하나라도 차면 연기 | youtube-api.md A012·A013; config.example.json. 사용량은 가상값 명시 |
| A6 | 검사 나열 → 검사별 실패 경로와 공통 예외 대기열 | 어느 검사에서 실패했는지와 수정 행동이 연결됨 | gates/__init__.py·config.example.json·실제 gates.json |
| A6 | gates.json 실물·실패 비교 신규 | passed와 reasons로 실제 원인을 읽고 승인 우회를 막음 | 새 mock 정상 출력, 원문에 없는 숫자를 넣어 같은 검사 함수 실행 |
| A6 | 3모드 전환·복귀 그림 신규 | 90%·95%는 책의 운영 제안이며 잘못 공개하면 승인제로 복귀 | A0 기존 가상 운영 기준·review.hours 기본값 |
| A7 | 시각 나열 → 하루 실행·승인/예외 대기·공개 타임라인 | 제작 시작과 공개 시각은 다르며 승인을 기다리는 동안 실행은 종료 | schedule/install.py·pipeline.py tick·review.hours. 모든 시각은 가상 운영 예 |
| A7 | 가상 보고 띠 → 실제 보고·대시보드 재현 | 예외·비용·지표 준비 상태를 한곳에서 읽음 | ops/report.py가 만든 daily-report.json·dashboard.html |
| A7 | 승인·예외 알림 재현 신규 | 알림에는 실행 ID·실패 이유·미리보기만 담고 비밀은 제외 | 실제 notification.json·ops/notifications.py. Discord는 알림, Telegram 승인은 별도 |
| A7 | 실행 방식 선택·Actions 복구 그림 유지 | 복구 실패 시 빈 상태로 새 실행하지 않음 | README·ops/state_sync.py·execution-hosting.md |
| A8 | 단계 나열 → 개선 순환·실제 산식 그림 | available 값만 카테고리 점수에 더하고 새 원문을 고름 | pipeline.py 주제 점수·insights.py; mock 12·0·missing은 가상 데이터; A023·A024 |
| A9 | 판단 목록 → 위험별 차단 장치 지도 | 자동으로 막는 조건과 사람이 확인해야 하는 위험을 구분 | gates·pipeline·ops/tokens·state_sync·README; policy-safety.md A070·A071·A075·A107 |
| E2E | 기존 증거 3단계 유지 | mock·설정 준비·실계정 성공을 따로 기록 | 현행 전체 체크 |

## 구현·검증

- [x] 독서·목록 대조, 실제 mock·gates·알림·보고 자료 확보
- [x] 장별 SVG·실제 WebP 삽입, figure/결론 캡션/대체 설명, 중복 문장 축소
- [x] style_lint·check_site(site-shorts), 그림 구조·각주·파일 크기 검사
- [x] 전체 심화 11페이지 × 1280/375/360 × 라이트/다크: 넘침·SVG 글자·이미지·콘솔·내부 링크·클릭 및 키보드 이동
- [x] 대표 화면과 결과 문서, 담당 외 파일 보존 확인, 지정 Discord 알림(대표 2장)

검증은 기존 Chromium/Playwright와 키트 가상환경을 재사용한다. SVG는 직접 작성한 인라인 도형과 책 테마 변수를 사용한다. 캡처 금지인 외부 콘솔은 재현 그림으로만 설명한다. 실제 mock 영상 프레임은 WebP 400KB 이하·lazy·명시 크기를 적용한다.
