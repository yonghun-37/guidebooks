# A5v-insta 결과 · ReelsBook 심화편 시각자료 보강

2026-10-26 · Codex. 요청한 필수 시각자료를 A0~A9의 해당 학습 위치에 배치하고 로컬 검증을 완료했다. Claude 최종 검수 대기이며 commit/push는 하지 않았다.

## 구현

- [계획표](phase-A5v-insta-plan.md)에서 DESIGN-advanced 1.2절과 기존 그림을 대조했다. 핵심 그림 17개를 신설/교체·보완했다. 최종 심화편은 기존 자료를 포함해 figure 25개·SVG 패널 31개다. 개수 대신 연결 관계·판정·실물·수치 비교를 보강했다.
- A0: 실행기·pipeline·상태 저장·알림과 원문·공급자·렌더·공개 호스팅·관문·게시·분석을 연결했다. 지도 노드 11개가 해당 장으로 이동한다.
- A1/A2: 정상 상태와 실패/연기/예외/결과 불명 복구를 구분했다. 실제 코드/상태 폴더 트리, 설정 핵심 키 주석, 번호가 있는 API 키 발급 위치, 출력/시도 제한→실행 예약→일/월→공급자 강제 상한 계층을 그렸다.
- A3/A4: 실제 스키마 일부·mock JSON·내용 검사를 연결했다. 저비용/고품질 목표/영상 10초 추가를 편당·월 차트로 비교했다. 카드와 같은 문안의 실제 릴스 프레임을 WebP로 넣었다.
- A5/A6: 직접 그린 Meta 설정 위치, 게시 시퀀스의 오류/불명 분기, 계정 quota와 더 낮은 로컬 상한 게이지, 검사별 실패 이유와 정상/예외 gates.json, 운영 모드 전환 기준을 시각화했다.
- A7~A9: 시작/승인·예외 대기/공개 예정/다음 tick의 하루 타임라인, 실제 mock 대시보드·일일 보고·승인/예외 메시지 재현, 지표→분류 점수→다음 원문 계산 예, 위험별 차단 위치와 사람이 확인할 일을 연결했다.
- SVG는 직접 작성한 인라인 도식이며 테마 변수/currentColor를 사용한다. 모바일은 패널을 세로로 쌓는다. 모든 그림에 결론 캡션과 접근 가능한 이름을 두었다. 가격·한도에는 기존 A각주, 키트 숫자에는 기본값/실제 출력, 모드 전환에는 편집 제안 표시를 붙였다.
- A0/A6의 중복 표와 A3/A7/A8의 중복 설명을 정리했다. `p` 요소 글자 수는 23,461→23,226이며 그림 캡션·SVG 텍스트는 별도다. 실습 명령·정의·확인 행동은 유지했다.

변경 범위는 `site/advanced/`(11 HTML·전용 visuals.css·examples/)와 요청된 `docs/results/phase-A5v-insta*`다. 공통 CSS/JS·키트·연구·현재 상태·서가는 수정하지 않았다. 동시 작업자의 다른 책 변경은 보존했다.

## 실제 출력

[명령 기록](phase-A5v-insta/kit-commands.json) · [출력 정보](phase-A5v-insta/mock-evidence.json)

- 깨끗한 `/tmp/a5vi-kit-dge02pq8/auto-kit` 복사본과 기존 `/tmp/auto-kit-a2-venv/bin/python`으로 mock을 실행했다. 새 키·설치·유료 생성·호스팅·게시 호출은 없었다.
- carousel auto → `dry_run`, approval → `waiting_approval`, reel auto → `dry_run`. 테스트 설정에서 민감 단어에 「신청」을 추가한 실행은 `exception`·정상적인 종료 코드 2와 실제 `검토 단어: 신청` 알림을 남겼다. 이후 실제 `report`도 실행했다.
- 실제 JPEG는 1080×1350. 실제 릴스는 1080×1920·H.264/AAC·30fps·15.1초·-16.05 LUFS다. 4초 프레임을 추출했다. 소리는 연습용 신호음이다.
- WebP는 카드 23,908바이트·프레임 15,104바이트로 각각 400KB 이하이며 width/height·lazy를 지정했다. 그림의 문안은 실제 제도·금액·성과를 주장하지 않는 가상 연습 예다.
- 공개 예제 JSON은 로컬 mock 파일의 값이며 알림의 내부 승인 결합 해시 필드만 제외했다. 정상/예외 gates와 세 알림을 원본과 대조했다. 대시보드는 실제 HTML/JSON 내용을 모바일 폭에 맞춰 직접 그린 재현 그림이며 메신저 전송 화면이 아니다.

## 검증

| 검사 | 실행 결과 |
|---|---|
| [style_lint](phase-A5v-insta/style-lint.json) | 11/11 통과, 금지어·내부 용어 0. 기존 축약 기준선에 심화편 항목이 없어 A3와 동일하게 기준선 없이 검사 |
| [check_site --site site](phase-A5v-insta/check-site.json) | 51 HTML·내부 참조 3,971개, 오류 0 |
| [그림·출처·출력](phase-A5v-insta/content-check.json) | SVG XML·중복 ID·캡션·접근성·A각주 등록/연결·이미지 속성·용량·비용 산식·실제 JSON 일치, 오류 0 |
| [브라우저](phase-A5v-insta/browser-check.json) | 11페이지×1280/375/360×라이트/다크=66조합, 가로 넘침·SVG 글자 잘림·이미지 실패·페이지/콘솔/내부 HTTP 오류 0 |
| 가독성·연결 | 모든 본문 SVG의 실제 표시 글자 크기 13px 이상. 기존 A4/A7/E2E 그림의 작은 보조 글씨도 키웠다. 내부 링크/앵커 301개, 시스템 지도 11개 노드 focus+Enter 이동 확인 |
| 기존 기능 | 비용 계산기의 $0.02400/$1.49250 시나리오, OS 탭 방향키·퀴즈 Enter, JS 없는 11페이지 읽기 확인 |
| [보존 검사](phase-A5v-insta/preservation-check.json) | 키트·research-advanced 추적 파일 136개 해시 유지. 기존 SVG 8쌍의 라이트/다크 텍스트 동일 확인. 다른 책 동시 변경은 이 작업에서 수정/회수하지 않음 |
| 공백 검사 | 담당 경로 `git diff --check` 통과 |

재현: 저장소 루트에서 `python3 -m http.server 8768 --bind 127.0.0.1`, 별도 창에서 [verify-content.py](phase-A5v-insta/verify-content.py)·[verify-browser.cjs](phase-A5v-insta/verify-browser.cjs)를 실행한다. Chromium을 사용했고 기존 선택 CDN 폰트 CSS는 빈 응답으로 처리해 시스템 폰트 대안을 검증했다. 외부 CDN 가용성·Windows/macOS 실기기 성공을 검증한 결과는 아니다. 전체 키트 pytest는 이번 시각자료 변경에서 재실행하지 않았다.

그림 스크린샷 36장을 [검증 폴더](phase-A5v-insta/)에 저장했다. 대표: [시스템 1280 라이트](phase-A5v-insta/00-start-visual-system-1280-light.png) · [운영 보고 360 다크](phase-A5v-insta/07-operations-visual-operations-report-360-dark.png). 추가: [하루 일정](phase-A5v-insta/07-operations-visual-daily-timeline-1280-light.png) · [관문](phase-A5v-insta/06-gates-visual-gates-360-dark.png) · [비용](phase-A5v-insta/03-generate-visual-cost-comparison-360-dark.png) · [실물](phase-A5v-insta/04-render-visual-render-output-1280-light.png).

## 남은 확인

- 실제 릴스에는 공통 영상 템플릿의 「자취생 10분 생존법 / 도윤의 연습」 문구가 남아 있다. A4의 실제 프레임과 캡션에 그대로 밝히고 `rendering/short_base.py`의 교체 위치를 안내했다. 키트는 담당 범위 밖이므로 수정하지 않았다. 키트 담당자가 인스타용 채널 문구를 분리하는 후속 검토가 필요하다.
- 실계정 인증·quota·라벨·실제 공개 시각·분석·청구·메신저 승인과 OS/Actions 다음 날 실행은 사용자 환경에서 확인할 항목이다. 이번 작업은 로컬 mock·시각자료·사이트 검증이다.
- PROJECT_STATE·서가 통합과 Claude 검수·commit은 통합 담당자의 영역이다. 이번 요청의 폴더 제한에 따라 변경하지 않았다.

## 완료 알림

지정 `scripts/notify.py`로 한국어 5줄 보고와 대표 스크린샷 2장을 첨부해 전송했고 **HTTP 200 성공**을 확인했다. 토큰은 출력하거나 저장하지 않았다.
