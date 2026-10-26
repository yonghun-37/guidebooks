# Phase A5v-shorts 결과 — ShortsBook 심화편 시각자료 보강

2026-10-26 · Codex. **시각자료 보강과 로컬 검증 완료, Claude 최종 검수 대기.**

## 구현 결과

[설계 대조표](phase-A5v-shorts-plan.md)에 따라 쇼츠 심화 A0~A9의 그림을 보강했다. 단순 단계 목록을 시스템 연결·실패 분기·실제 파일·입출력·비교·화면 위치·결과 예시로 바꿨다. 전체 체크의 기존 그림은 유지했다. 현재 심화 11페이지에는 **figure 28개, SVG 27개, 실제 프레임 WebP 3장, 기존 MP4 1개**가 있다. 이 중 직접 새로 작성한 SVG는 20개다. 개수 자체를 목표로 삼지 않았다.

| 장 | 구현한 시각자료와 독자가 확인할 것 |
|---|---|
| A0 | 클릭 가능한 시스템 구성도. 실행기·비공개 상태·생성 공급자/렌더·관문·게시·분석·알림·호스팅을 연결했다. 쇼츠의 공개 미디어 URL과 Actions의 비공개 상태 저장을 구분한다. |
| A1 | 정상 상태와 실패·연기·관문 예외·시작 결과 불명·세션 만료의 복구 지도, 실제 폴더 트리. 완료 상태에서 실패로 연결하지 않으며 결과 불명에 새 insert를 권하지 않는다. |
| A2 | 공급자 키/지출 제어의 번호 있는 화면 틀, 실제 config 키 주석, 공급자→월→일→실행 예약의 지출 제어 계층, 편당·월 비용 비교. 기존 계산기는 유지했다. |
| A3 | 원문 입력→구조화 요청→실제 draft 일부→실제 스키마 규칙→TTS/렌더·원문 관문 흐름. 구조 오류와 내용 오류를 구분한다. |
| A4 | 새 mock MP4의 1·8·31초 실제 프레임 3장. 데스크톱은 나란히, 모바일은 읽을 수 있는 크기로 세로 배치했다. 기존 전체 영상·SRT·조립 그림도 유지했다. |
| A5 | OAuth 준비 화면 틀, 기존 요청/응답 시퀀스와 실패 위치별 분기, 공식 버킷/로컬 cap 사용·잔여 게이지. 모두 토큰·Location을 표시하지 않는다. |
| A6 | 검사별 실패 화살표가 공통 예외 대기열로 모이는 판정 흐름, 실제 gates.json 발췌와 숫자 오류 결과, 3모드 전환·사고 후 복귀 지도. |
| A7 | 가상 하루 실행·승인/예외 대기·예약 공개 타임라인, 실제 대시보드·일일 보고의 모바일 재현, 실제 승인 알림·오류 검사로 만든 예외 알림 재현. 기존 실행 방식/Actions 복구 그림은 유지했다. |
| A8 | available/missing 분리→카테고리 점수→새 원문→제작·게시→다음 지표의 개선 순환. 현재 코드의 로그 평균 산식과 가상 1.321 계산을 연결한다. |
| A9 | 위험별 자동 차단 장치 지도. 검사·예약비·한도·세션·토큰 경보·lease와 사람의 문맥·권리·표시 판단을 나눈다. |

새 그림은 figure·의미 있는 SVG 제목/설명 또는 alt·결론 한 문장 캡션을 갖췄다. 테마 변수는 [전용 CSS](../../site-shorts/assets/advanced-visuals.css)를 사용한다. 외부 콘솔 캡처·로고·새 의존성은 없다. A3의 필수 키/장면 수 설명과 A6의 긴 전환 기준 반복, A8의 계산 예 문단은 그림·해당 절 링크로 줄였다.

비용은 `research-advanced/cost-model.json`·`costs.md`의 기존 근거 A025/A028/A038/A037과 연결했다. 저비용 $0.0032/편·$0.096/월, 고품질 목표 $0.2365/편·$7.095/월, 영상 10초 추가 시 $0.7365/편·$22.095/월이다. 사용량·월30편·이미지6장은 가상 견적이며, 실제 키트의 2~5장면과 다름을 명시했다. 90%·95%는 기존 책의 운영 제안이고 플랫폼 규정이나 자동 승격 기능이 아니다.

## 실제 출력과 근거

- 비밀 파일·기존 private·가상환경을 제외한 깨끗한 `/tmp/a5v-shorts-kit` 복사본에서 기존 Python 3.11 가상환경으로 실행했다. 원본 키트는 수정하지 않았다.
- `run --flow shorts --provider mock --mode approval` → `waiting_approval`, `approve` → `resume` → `dry_run`, `insights`·`report`를 실제 실행했다. mock 지표 12·0·missing은 성과가 아닌 연습 값이다.
- [관문 실물](phase-A5v-shorts/mock-gates.json)에서 6검사 통과, 1080×1920·30fps·H.264/AAC·36.1초·-16.05 LUFS를 확인했다. [숫자 오류 재현](phase-A5v-shorts/facts-failure.json)은 동일 검사 함수가 `passed:false`와 `원문에 없는 숫자: 99`를 반환한 결과다.
- [승인 알림](phase-A5v-shorts/mock-notification.json)과 [예외 알림](phase-A5v-shorts/exception-notification.json), [일일 보고](phase-A5v-shorts/mock-daily-report.json)·[대시보드 원본](phase-A5v-shorts/mock-dashboard.html)·[CSV](phase-A5v-shorts/mock-insights.csv)를 그림과 대조했다. 예외 알림은 오류 검사 결과로 `notify(live=False)`를 호출해 생성했다. 외부 알림 수신 성공으로 설명하지 않는다.
- [산출물 해시·재현 조건](phase-A5v-shorts/artifact-provenance.json): 새 mock MP4와 책에 있던 전체 MP4의 SHA256이 같다. 프레임은 그 MP4에서 추출했으며 WebP는 16,916·10,274·13,272바이트, 합계 **40,462바이트**다. 각 540×960·lazy·400KB 이하 조건을 충족한다.

## 검증과 수정

| 검사 | 실제 결과 |
|---|---|
| 문체 | [style_lint](phase-A5v-shorts/style-lint.json): 심화 11/11 통과. 금지어·내부 용어 0, 상자 밖 단서 1개(실제 대시보드의 상태 라벨 「미확인」). 기존 이론편 축약 기준선은 심화편에 적용하지 않음 |
| 정적 사이트 | [check_site --site site-shorts](phase-A5v-shorts/check-site.json): HTML 49개·내부 참조 4,245개, 오류 0 |
| 그림·출처·출력 | [검사 코드](phase-A5v-shorts/verify-content.py)·[결과](phase-A5v-shorts/content-check.json): 캡션·대체 설명·ID·각주 앵커·이미지 크기·정상/오류 관문·비용 계산 통과 |
| 브라우저 | [재현 코드](phase-A5v-shorts/verify-browser.mjs)·[결과](phase-A5v-shorts/browser-check.json): **심화 11페이지 × 1280/375/360 × 라이트/다크 = 66조합**, 가로 넘침·SVG/상자 밖 글자·이미지 실패·콘솔/페이지/내부 HTTP 오류 0 |
| 연결·조작 | 내부 링크·앵커 **288개**, 시스템 링크 포커스/Enter 이동, 관문 실패 분기·기존 비용 계산·기존 영상 메타데이터, 전체 11페이지 JS 없는 그림 읽기 통과 |
| 보존·공백 | [보존 기록](phase-A5v-shorts/preservation-check.json): 기준 2,306파일 중 auto-kit/research-advanced 136파일 해시 유지. 담당 파일 `git diff --check` 통과 |

별도 읽기 전용 검토에서 상태명 오류 1건을 확인해 수정했다. 세션 시작 응답 불명은 처음 `failed`, 다음 재개에서 `uncertain`이며, 세션 만료 404/410은 `failed`다. A1·A5·A9 그림과 관련 문장을 실제 `publish/youtube_protocol.py`·`pipeline.py`에 맞췄다. 초기 각주 검사에서 발견한 A0의 A019 출처 앵커 누락도 추가했다. 수정 후 위 문체·정적·내용·66조합 브라우저 검증을 다시 통과했다.

화면 검사는 Linux Chromium에서 기존 시스템 폰트 대안으로 실행했다. 외부 Google Fonts 요청은 빈 CSS로 처리했으므로 CDN 가용성을 검증한 결과는 아니다. 그림 캡처 때 고정 헤더만 숨겨 내용이 가려지지 않게 했다. 키트 기능을 변경하지 않아 전체 키트 pytest는 재실행하지 않았다.

## 대표 화면

- [실제 영상 프레임 · 1280 라이트](phase-A5v-shorts/render-frames-1280-light.png)
- [품질 관문 분기 · 360 다크](phase-A5v-shorts/gate-branches-360-dark.png)
- [시스템 구성도 · 360 다크](phase-A5v-shorts/system-map-360-dark.png)
- [비용 비교 · 360 라이트](phase-A5v-shorts/cost-comparison-360-light.png)
- [실제 관문 결과 · 360 다크](phase-A5v-shorts/gates-result-360-dark.png)
- [전환·복귀 · 360 라이트](phase-A5v-shorts/mode-ladder-360-light.png)
- [하루 타임라인 · 360 다크](phase-A5v-shorts/daily-timeline-360-dark.png)
- [대시보드 재현 · 1280 라이트](phase-A5v-shorts/report-sample-1280-light.png)

## 범위·남은 확인

수정은 쇼츠 심화 A0~A9·전용 CSS/WebP와 지정 계획·결과·검증 자료에 한정했다. E2E 파일·기존 공통 CSS/JS·부록·연구·키트·PROJECT_STATE·서가는 수정하지 않았다. 실행 중 다른 책/research-blog에 생긴 동시 변경은 보존 기록에 구분했으며 되돌리지 않았다. commit/push·새 유료 키·결제·계정 로그인·실제 게시도 하지 않았다.

Claude 최종 검수·배포와 사용자 실계정의 발음·권리·토큰·할당량·업로드/공개·예약 취소·분석·OS/Actions/R2 동작 확인은 남아 있다. 이번 작업은 시각자료의 실제 mock/문서/브라우저 검증이며 실계정 전자동 운영 성공 판정은 아니다.

## 완료 알림

지정 `python3 scripts/notify.py "🖼️ [A5v-shorts 완료] ..."`에 실제 프레임 1280 라이트·관문 분기 360 다크 화면 2장을 첨부해 전송했고 **HTTP 200**을 확인했다. 한국어 4줄로 산출물·검증·남은 확인을 보고했다.
