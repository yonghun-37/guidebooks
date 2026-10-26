# Phase 10r — 교과서 서가 인터랙션 분석

작성: 2026-10-26, Codex. **분석·설계 제안 작성 완료, Claude Code 검수 대기.** 사이트·키트 구현은 하지 않았다.

## 산출물과 범위

- [교과서 서가 분석](../reference-analysis-books.md): 서가69항목(출간52·예정17), 선정4권×표지/본문2/종합 도구1 = 16페이지, 패턴 카탈로그·기술/접근성·고도화 제안20개·상위5 화면/입력→상태→출력·ShortsBook 별도 절·저작권 주의·완전한 Evidence 대장.
- 선정: CameraBook(촬영 비교/미션), MusicBook(소리 합성/트랙 편집), NetworkBook(단계/상태/실패), YieldBook(증거 선택/원인 추리). ColorBook 두 계열은 제외했다.
- 상위5: **3장 수익 흐름도 / 7장 문안 카드 편집기 / 8장 재생 타임라인 / 10장 게시 단계 모형 / 12장 상황별 검수**. 구현 확정·착수·완료로 기록하지 않는다.

## 사용 도구·성공과 실패

| 도구 | 결과·확인 범위 |
|---|---|
| 로컬 셸·Git 읽기 | cwd·status·AGENTS·DESIGN·STYLE-GUIDE·이전 분석·관련 코드 확인. 작업 중 다른 담당자의 파일 변경도 확인했으며 보존했다. commit/push 미시도 |
| REA `list_browser_targets` | 성공. 별도 임시 프로필의 Chromium149, loopback9337에서 공개 서가 target 선택 |
| REA `capture_browser_scenario` | 16페이지 방문과 버튼·range 키보드·경로/원인 선택·촬영 미션·시퀀서 재생 수행. 처음 빈 actions와 잘못된 action discriminator 입력2회는 스키마 검증 거절; 제공자 스키마를 읽고 고친 뒤 성공. 거절을 분석 Evidence로 세지 않음 |
| REA `inspect_web_page` | 성공. 서가 및4권의 DOM/접근성·script source·자원 확인. 초기 결과 요약 코드2회 오류는 도구 실행 실패가 아니며 반환 Evidence를 보존해 요약을 수정 |
| REA `inspect_web_event_listeners` | 성공. Camera segmented button, Music 부모 격자 click 위임·range input·Canvas 포인터, Network 다음 버튼, Yield 제출 버튼 위치 확인. Music 자식 셀의 빈 목록은 위임을 확인하는 출발점으로 사용 |
| REA `capture_web_screenshot` | 성공.4권 화면 확인. 시나리오 종료 후 크기 복구를 처음 적용 실패로 오인한 점은 제공자 적용/복구 확인 후 정정. 혼합된 모바일 중간 화면은 판정에서 제외 |
| REA `analyze_web_bundle` | 성공. Camera/Music/Network4개씩, Yield6개 script 파싱, 실패0. 외부 origin 제외·실행 인과·서버 동작은 범위 밖 |
| REA `export_web_scripts`·`trace_web_module_imports` | 성공. Yield 캡처를 저장소 밖으로 내보내고 장 script의 ES import0건 확인. 일반 script 의존성 부재를 뜻하지 않음 |
| REA `export_evidence_bundle` | 성공.57건·19,018,079B를 저장소 밖 `/tmp/ai-insta-10r.1DGMei/rea-evidence-bundle.json`으로 보존. 개별ID는 분석 문서 부록에 기록 |
| CDP 보완 | 성공. REA가 지원하지 않는 좌표 드래그와 계산 스타일/Resource Timing 측정. 모바일은375×812를 같은 세션에서 설정·탐색·측정·캡처.4종합 페이지 문서 scrollWidth=clientWidth=360px(창375−스크롤바15). 내부 가로 스크롤은 별개 |
| curl 보완 | 성공. REA 자원 목록만으로 알 수 없는 CSS 전환/반응형 규칙을 공개 CSS4개에서 확인. 원본은 임시 폴더에만 둠 |
| 웹 열기 | Books URL 접근 실패. REA/Chromium은 성공했으므로 이 도구를 통한 대체 조사로 진행하지 않음 |

주요 실행 근거: Camera f/5.6→f/1.4와 미션 성공, Music 두 셀 click/Enter·112→180BPM·재생/정지, Network 단계0→3→2→0 및 경로17→16단계, Yield 가상 사건 예산14→13→13→11→오답 후7. 동작 시나리오5개에서 수집된 page-error0·이벤트 drop0을 확인했다. 원 사이트 전체의 오류 부재를 뜻하지 않는다. CDP 배음 드래그도 실제 포인터로 지표 변화를 확인했다.

## 검증과 제한

- 문서의20개 제안·상위5 명세·16페이지 근거·도구/ID 대응·상대 문서 링크를 정적 확인했다. 기존 사이트/키트 테스트는 이 분석 변경과 무관하여 실행하지 않았다.
- 마이크·저장/공유·WAV 내보내기·클립보드·Network 진도 복원 전체·모든 퀴즈 정오답·실물 터치·보조기기·냉시작 성능은 검증하지 않았다. 표본 코드의 기능 존재와 실행 성공을 구분했다.
- 유료 키·결제·실제 Instagram 로그인/게시·Hermes 호출·설정 변경을 하지 않았다. 원본 코드/이미지/캡처 전문은 저장소에 넣지 않았다. 조사용 Chromium과 임시 화면 크기 보조 프로세스는 종료했다. `/tmp` 자료는 영구 보관을 보장하지 않는다.
- 새 기능 구현이 없는 Level0 조사이므로 별도 `docs/specs/`·ADR·architecture 변경을 만들지 않았다.

## 공용 상태 반영 요청

작업 중 추가된 [guidebook-pipeline 스킬](../../.agents/skills/guidebook-pipeline/SKILL.md)의 파일 소유 규칙은 **“상태는 docs/PROJECT_STATE.md(통합 작업자만)”**이다. 다른 작업자의 미커밋 변경이 있는 공용 현황과 사이트/서가를 수정하지 않았다. 통합 담당자는 현황에 “Phase10r 분석 완료·검수 대기, 제안20개·상위5 명세, 사이트/키트 미변경”과 이 결과 링크를 반영하면 된다. 기존 현황의 다른 단계 검증 수치를 이번 분석 결과로 갱신하지 않는다.

## 핵심 결론 10줄

1. 네 책의 차이는 조작 장치보다 학습자가 바꾸는 대상·질문·피드백의 차이다.
2. CameraBook은 설정의 결과와 여러 조건을 만족시키는 미션을 연결한다.
3. MusicBook은 트랙과 시간을 조작하면서 전체 재생을 확인하게 한다.
4. NetworkBook은 보이지 않는 절차를 현재 상태·다음 행동·단계 설명으로 드러낸다.
5. YieldBook은 정답보다 먼저 필요한 증거와 조사 순서를 선택하게 한다.
6. ReelsBook은 기존 도구를 실제 문안·시간·가상 오류·증거에 연결하는 개선이 우선이다.
7. 상위5는 수익 흐름·카드 편집·릴스 재생·게시 단계·상황별 검수다.
8. 모바일 가로 넘침이 없어도 긴 격자·경로와 작은 셀은 별도 대안이 필요하다.
9. 키보드 버튼·DOM 결과·읽기/완료 분리·동작 줄이기를 모든 개선에 적용해야 한다.
10. 원 사이트의 문장·코드·이미지를 복사하지 않고 자체 예제와 구현으로 패턴만 적용한다.

## 완료 보고

사용자 지정 `python3 scripts/notify.py`로20개 제안과 상위5·산출물·남은 검수 상태를 한국어4줄로 보고했다. **HTTP200 전송 성공**. commit·push·배포는 하지 않았다. 최종 정합성 검사(제안20·화면/명세5·Evidence57·방문16·모바일4·문서 링크·결론10줄)와 `git diff --check`가 통과했다.
