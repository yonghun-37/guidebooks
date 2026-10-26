# Phase 3 결과 — 사이트 뼈대·디자인 시스템·1장

## 범위와 구현

Phase 3의 정적 웹 교과서와 1장 학습 흐름을 구현했다. Phase 4 스타터 키트와 후속 장 본문은 구현하지 않았다. 기존 설계와 Phase 2 분석을 입력으로 사용했으며, 원 사이트의 문장·이미지·CSS/JS를 복사하지 않았다.

- `site/index.html`: 표지, 독자별 시작 경로, 부별 전체 목차, 가상 인물 소개.
- `site/assets/book.js`: 16장과 출처 부록의 단일 메타데이터(번호·slug·부·제목·결과물·시간·난이도·준비중/완성). 표지 목차, 헤더 메뉴, 장 상단 메타, 사이드바·모바일 장내 목차, 이전·다음 링크를 생성한다. 현재는 1장만 완성 상태다.
- `site/chapters/coming-soon.html?chapter=<slug>`: 미완성 본문 장의 공통 안내. 해당 장 제목과 이전·다음 이동을 유지한다. 실험실·용어집·크레딧도 실제 파일이 있는 준비 중 페이지이며, 용어집에는 1장 링크를 위한 세 용어의 짧은 설명만 넣었다.
- `site/assets/book.css`: 본문 704px, 종이색·녹색 기반 라이트/다크 토큰, 역할명·아이콘·번호를 갖춘 9단계 블록, 모바일 단일 열, 포커스 표시, 모션 감소, 인쇄 시 시뮬레이터 숨김. Pretendard CDN은 v1.3.9 고정이며 시스템 글꼴을 대체로 사용한다.
- 공통 동작: 시스템 테마 추종·수동 선택·토글, 용어 툴팁과 용어집 앵커, 각주 왕복 링크, 코드/메모 복사와 실패 시 직접 선택, 결과물 체크 저장과 실패 안내, 데이터 속성 기반 즉시 채점·정답·해설·다시 풀기.
- `site/assets/sim/common.js`: 명명된 시뮬레이터 영역, 텍스트 결과의 상태 알림, 버튼 그룹의 네이티브 클릭·Enter/Space 및 방향키·Home/End 조작.
- `site/chapters/01-map.html`: 9단계 전체, 하린·정 선배 서사, 목표·시간 예산 메모 실습, 결과물 체크 네 개, 퀴즈 네 문항, 출처 대기 각주.
- `site/assets/sim/map.js`: 소재→문안→카드/릴스→검수→게시→분석→수익의 일곱 단계. 선택 시 설명·도구·하린의 가상 시간 배분·관련 장 링크를 표시한다. 주당 시간 슬라이더로 30일 제작 시간 예산을 계산한다.
- `docs/chapter-template.html`: 9단계 전체와 작성 규칙, 자원 경로·장 데이터 등록·사실 각주·입력·체크 저장·퀴즈의 공통 계약. 시뮬레이터 자리는 작성용 안내이며 동작하는 도구로 표현하지 않는다.

빌드·프레임워크·사이트 런타임 패키지는 추가하지 않았다. `site/index.html` 직접 열기 또는 아래 정적 서버로 확인할 수 있다.

```bash
python3 -m http.server 8765 --bind 127.0.0.1 --directory site
# http://127.0.0.1:8765/
```

## 계산 가정과 출처 보류

이 모형은 게시량 권장이나 수익 예측이 아니다. 카드 한 묶음 **또는** 릴스 한 편을 게시물 하나로 센다. 가상 제작 시간은 소재 10분·문안 15분·제작 20분·검수 10분·게시 준비 5분으로 합계 60분이다. 매주 분석 30분·수익 경로 검토 30분을 따로 남긴다. 계산식과 제외한 학습·설치·수정 시간은 도구 아래 공개했다.

`floor(max(0, 주당 시간 × 60 − 60) × (30/7) ÷ 60)`

검증 기준값은 주 0/0.5/1시간 → 0개, 1.5시간 → 2개, 3시간 → 8개, 5시간 → 17개다. 하린의 나이·생활·수익 목표도 가상 인물 설정이며 실제 성과의 근거가 아니다.

작성·검증 시점에 `research/FACT-SHEET.md`와 `research/SOURCES.md`가 없었다. 따라서 공식 게시 API 요건, 한국 수익화 가용성, 저작권·광고·AI 표시, 공개 사례는 확정 문장을 쓰지 않고 정확히 `<span class="fact-pending">[출처 확인 대기]</span>`로 표시했다. 정책 확인 구간에는 **2026년 10월 조사 기준**을 명시했다. 사실 ID·SOURCES 번호는 만들지 않았다. [가]~[라]는 대기 구간으로 돌아가기 위한 로컬 각주 표식이며 SOURCES 번호가 아니다.

조사 완료 후 검수자가 FACT-SHEET의 해당 사실 ID와 SOURCES 번호·원문을 연결해야 한다. 이는 현재 남은 콘텐츠 의존성이다. 실존 계정의 실제 사례 블록도 조사 전까지 대기 상태다.

## 검증 결과

기존 설치 Chromium **149.0.7827.55**를 Playwright Core로 구동했다. 브라우저를 새로 설치하지 않았다. 검증 도구만 `/tmp/ai-insta-phase3-browser/`에 설치했으며 저장소 의존성에 포함하지 않았다. npm 기본 캐시는 읽기 전용이어서 `/tmp/ai-insta-phase3-npm-cache`로 지정해 설치했다.

[검증 스크립트](phase-3/verify.mjs), [실행 결과 JSON](phase-3/verification.json)에 재현 방법과 실제 판정을 남겼다. 최종 실행은 **81개 확인 통과**, 고유 내부 링크·앵커 **46개 정상**, 콘솔/페이지 오류 **0개**, 네트워크 실패 **0개**였다.

| 대상 | 확인 결과 |
|---|---|
| 표지·1장·준비 중 본문·실험실·용어집·크레딧 | 각각 1280px·375px·360px에서 문서 `scrollWidth === clientWidth` |
| 지도 | 일곱 단계의 설명·도구·시간·관련 장, 단일 선택 상태, 방향키·Home·End·Enter |
| 시간 계산 | 0/0.5/1/1.5/3/5시간 경계·기준값, 네이티브 슬라이더 키보드 입력과 텍스트 결과 |
| 학습 기능 | 체크 재방문 복원, 잘못된 저장 JSON 복구, 퀴즈 정오답·해설·보기 잠금·초기화·전 문항 정답 |
| 실패 경로 | localStorage 읽기/쓰기 모두 차단해도 체크·테마·계산 동작, 복사 거부 시 선택 가능한 텍스트와 안내 |
| 테마·탐색 | 시스템 다크 추종, 수동 우선·저장·시스템 복귀, 모바일 목차 열기·Escape·포커스 복귀, 용어 포커스·Escape |
| 정적 구조 | HTML 7개 lang/title/viewport/main/중복 ID 검사, 장·템플릿의 9블록, 템플릿 퀴즈 |
| 대체 사용 | JS 비활성화 시 1장 본문과 퀴즈 정답 읽기, `file://`에서 장 내비·계산 실행, print에서 시뮬레이터 숨김 |

시스템 테마·클립보드의 비동기 완료를 기다리도록 검증 스크립트를 보정했고, 표지 SVG의 긴 라벨과 사이드 목차의 장식 문자를 화면 검토 후 정리했다. 전체 보조기기·실기기 터치·브라우저별 검증 및 정식 HTML 표준 적합성 검사는 수행하지 않았다.

재실행 예시(정적 서버 실행 후, 경로는 설치 환경에 맞춘다):

```bash
node --check site/assets/book.js
node --check site/assets/sim/common.js
node --check site/assets/sim/map.js
node docs/results/phase-3/verify.mjs \
  /tmp/ai-insta-phase3-browser/node_modules/playwright-core/index.mjs \
  /home/yonghun/.cache/ms-playwright/chromium-1228/chrome-linux64/chrome
```

## 화면 산출물

- 표지: [데스크톱 1280px](phase-3/desktop-cover.png), [모바일 375px](phase-3/mobile-cover.png)
- 1장 상단: [데스크톱](phase-3/desktop-chapter.png), [모바일](phase-3/mobile-chapter.png)
- 지도: [데스크톱](phase-3/desktop-pipeline.png), [모바일](phase-3/mobile-pipeline.png)
- 다크 모드 계산기: [모바일](phase-3/mobile-dark-budget.png)

## 작업 경계와 인계

사용자의 병행 작업 지시에 따라 `research/`, `docs/PROJECT_STATE.md`, `docs/PLAN.md`는 수정하지 않았다. 별도의 명세/ADR 구조를 만들지 않고 기존 Phase 기록을 이어 썼다. 기존 미추적 파일은 유지했다. 지시된 사이트·템플릿·Phase 3 결과와 기존 Phase 2 분석 문서만 명시적으로 스테이징하려 했으나, 아래 읽기 전용 제한으로 스테이징과 커밋은 완료하지 못했다. push는 하지 않았다.

다음 검수에서는 디자인·장 서사·교육용 가정을 확인하고, 조사 자료가 준비되면 위 네 출처 대기 구간을 채운다. 후속 장·전체 용어집·실험실 본문은 이 단계의 완성 기능으로 간주하지 않는다.

## 커밋 미완료 — 환경의 Git 메타데이터 쓰기 제한

요청한 파일 목록으로 `git add -- site docs/chapter-template.html docs/results/phase-3.md docs/results/phase-3 docs/reference-analysis.md docs/results/phase-2.md`를 실행했으나 다음 오류가 발생했다.

```text
fatal: Unable to create '/home/yonghun/project/ai-insta/.git/index.lock': Read-only file system
```

요청한 `git commit -m "Phase 3: site skeleton and chapter 1"`도 같은 오류로 실패했다. 현재 실행 환경에서 `.git`은 읽기 전용이다. 기존 잠금 파일과의 충돌이 아니므로 잠금 삭제나 승인 설정 변경은 하지 않았다. 작업 파일·검증 결과·스크린샷은 보존되어 있으며 커밋은 생성되지 않았다. Git 쓰기가 허용된 환경에서 위의 명시적 add와 commit을 실행해야 한다.

Discord 보고는 `scripts/notify.py`로 표지 데스크톱·1장 모바일 스크린샷 두 장을 첨부해 전송했고 HTTP 200 응답을 확인했다.
