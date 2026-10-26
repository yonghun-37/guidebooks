# AIc · 인스타 실습의 AI 서비스 기본 경로

2026-10-26 작성. **실습 0·3·4·5·E2E 개편과 지정 검증 완료, 공통 메타·목차 통합 및 Claude Code 검수 대기.**

## 요구와 범위

“어떤 서비스에 무엇을 넣고 어떻게 만드는가”에 답하도록 기존 실습을 실제 서비스 중심으로 다시 썼다. 기준은 `STYLE-GUIDE.md`, `DESIGN.md` 12절, `research/ai-production.md`와 AIP 사실표·출처표다. 이 기록과 [통합 요청](phase-AIc-requests.md)이 기능 기록을 겸한다. 공통 파일과 `PROJECT_STATE.md`는 통합 담당자 소유이므로 직접 수정하지 않았다.

- [x] 실습별 학습자 질문 5개·입출력·복사용 프롬프트·성공/오류·PC/휴대폰 안내
- [x] 기존 키트 명령을 접기 상자로 보존하고 깨끗한 임시 복사본에서 실행
- [x] 공통 메타·목차·다음 단계·용어·출처·상태 변경 요청 기록
- [x] 문체·정적 검사, 1280/375/360px·콘솔·키보드 검증과 화면 보존

## 바뀐 결과

| 파일 | 기본 경로와 손에 남는 것 |
|---|---|
| `site/practice/00-start.html` | 뉴스카드 / 카드→모션 / 얼굴 없는 해설 선택. ChatGPT·Canva·CapCut·Vrew와 무료 조건·한국 지원·약 60/95/80분 제작 목표를 비교한다. 키트 설치를 선택으로 분리한다. |
| `site/practice/03-copy.html` | ChatGPT 무료 가입 → 새 대화 → 원문·날짜·권리 메모 → 요약표 → 원문 대조 → 카드 문안 → TXT/메모 저장. 요약·문안 프롬프트, 가상 공지의 좋은/나쁜 문안이 있다. |
| `site/practice/04-cards.html` | Canva Free → 카드뉴스 템플릿 / 1080×1350 새 캔버스 → 5장에 제목·본문·출처 → 선택 AI 삽화와 표시 → PNG/JPG 전체 다운로드·압축 해제·치수·장수 확인. |
| `site/practice/05-reel.html` | 본인 녹음 또는 Vrew TTS → CapCut 새 프로젝트·9:16 → 장면/말 길이 맞추기 → 자동 자막·부정 표현 교정 → 음악 권리 → 1080p MP4 → 저장본 끝까지 재생. 무료 출력 잠금은 Clipchamp 대안으로 연결한다. |
| `site/practice/e2e.html` | 기본 경로와 선택 키트·API·매일 생성을 나눈다. 서비스 결과물 검수표·검수 메모 → 앱 게시 경로를 제공한다. 기존 38개 진행 키를 보존하고 5개를 추가해 본문과 같은 43개를 갖는다. |

각 실습은 지금 하는 일 / 왜 / 따라 하기 / 성공 / 이렇게 보이면? / PC·휴대폰 탭을 반복한다. 서비스 메뉴 옆에 표준 버튼 안내와 공식 도움말이 있다. 무료·가격·한국 가용성은 2026년 10월 조사 기준 각주로 연결하고, 시간·장수·해상도는 연습 목표로 구분했다. 수익화와 단순 모션 제작 성공도 구별했다.

직접 그린 SVG 제작 흐름 3개를 HTML에 넣었다. 서비스 화면·로고는 사용하지 않았고 이번 담당 범위에서 AI 이미지 파일은 생성하지 않았다. 선택 삽화 프롬프트·AI 생성 삽화 표시·원본/프롬프트 보관 방법을 안내한다. 같은 작업 트리에 다른 단계가 추가한 AI 예시 자산은 이 작업의 생성물로 세지 않는다.

기존 키트 설명은 각 실습 끝 **자동화·무료 대안**에 남겼다. 동봉 합성 자료와 실제 게시용 자료를 구분하고, 서비스 TXT/이미지/MP4를 키트 JSON 경로에 바로 넣지 않도록 했다. 본문 H1은 새 제목을 직접 표시한다. 공통 `book.js`의 브라우저 제목·목차·pager 메타는 요청 diff 적용이 남았다.

## 실행한 검증

| 검사 | 결과·증거 |
|---|---|
| 문체 | 0·3·4·5는 기존 기준선으로 4/4, E2E는 기준선 없이 1/1 통과. 금지어·내부 용어 0. 실습에는 이론 분량 70% 제한을 적용하지 않았다. [4개 실습](phase-AIc/style-lint.json), [E2E](phase-AIc/style-lint-e2e.json) |
| 전체 정적 검사 | 최종 작업 트리 `check_site.py`: HTML 37개·내부 참조 1,474개·진행 키 43개·오류 0. [결과](phase-AIc/static-check.json) |
| 범위 분리 정적 검사 | Git HEAD를 임시 폴더에 내보내 AIc 다섯 파일만 덮어쓴 검사도 오류 0. [결과](phase-AIc/static-check-isolated.json), [범위](phase-AIc/static-scope.json) |
| 브라우저 | Linux Chromium, 5페이지 × 1280/375/360px × 라이트/다크. 접은/펼친 상태 가로 넘침 0, 콘솔·페이지·로컬 HTTP 오류 0. 탭 방향키·Home/End, 접기 Enter/Space, 퀴즈 Enter, 프롬프트 복사/클립보드 일치, 체크 Space·새로고침·E2E 공유·리셋·저장 차단과 동적 링크/앵커를 포함해 **544검사 통과**. [재현 코드](phase-AIc/verify-browser.mjs), [결과](phase-AIc/browser-check.json) |
| 보존 도구 | 접기 상자에서 카드 미리보기 재측정·넘침/복원, 릴스 방향키 탐색·Enter 재생/정지·모바일 가로 넘침을 검사. **49검사 통과**. [코드](phase-AIc/verify-preserved.mjs), [결과](phase-AIc/preserved-check.json) |
| 키트 | 새 임시 복사본과 Python 3.11.15 신규 venv에 requirements 고정 3종을 pip 설치. 기존 명령 블록 **12개 동일성**, **16개 명령 exit 0** 확인. 동봉 5장·단일 자료 3장, PNG 1080×1350, 계정 이름 전달, prompt의 기존 copy.json 보존, M4A→WAV, MP4 1080×1920·오디오 스트림·끝까지 디코딩을 확인. [코드](phase-AIc/verify-kit.py), [결과](phase-AIc/kit-check.json) |
| 공백·변경 범위 | 담당 HTML·결과 문서의 `git diff --check` 통과. 공통 JS/CSS·부록·인덱스·실습 6/7·키트 구현·연구 파일은 직접 수정하지 않았다. |

키트 첫 준비에서 시스템 Python 3.10으로 만든 venv는 요구 버전에 맞지 않아 설치가 실패했다. 이를 폐기하고 문서가 요구하는 Python 3.11.15로 새 venv를 만든 뒤 **외부 패키지 복사 없이 pip 설치와 실행을 완료**했다. Windows 명령의 실행 파일 경로는 Linux venv Python으로 바꾸어 같은 인자를 실행했다. Windows/macOS 실기기 실행으로 세지 않는다. 음성 변환 검증은 0.5초 사인파로 만든 파일이며 실제 내레이션 청취·정렬 품질을 검증한 것은 아니다.

최초 전체 정적 검사 중 동시에 편집 중이던 이론 6~8장과 기존 크레딧의 앵커 차이가 나타났다. 해당 파일을 고치지 않고 AIc 분리 검사를 수행했으며, 최종 전체 재실행에서는 오류 0을 확인했다. 처음부터 존재한 `docs/prompts/phase-Y4ai.md`와 작업 중 나타난 이론·쇼츠·이미지 등 다른 단계의 변경은 보존했다.

## 화면과 재현

스크린샷 **30장**: 각 페이지의 첫 화면과 주요 단계 × 3폭. 주요 단계 전체 캡처에서는 고정 헤더·건너뛰기 링크가 본문을 덮지 않도록 촬영 순간에만 숨겼다. 검사 자체에는 그 스타일을 적용하지 않는다.

- 대표: [유형 선택 1280px](phase-AIc/00-start-1280.png), [모바일 유형표 375px](phase-AIc/00-start-step-375.png)
- [ChatGPT 프롬프트 360px](phase-AIc/03-copy-step-360.png), [Canva 배치 1280px](phase-AIc/04-cards-step-1280.png)
- [자막 교정 360px](phase-AIc/05-reel-step-360.png), [서비스 파일 검수 375px](phase-AIc/e2e-step-375.png)

검증 서버와 명령:

```bash
python3 -m http.server 8593 --bind 127.0.0.1
node docs/results/phase-AIc/verify-browser.mjs
node docs/results/phase-AIc/verify-preserved.mjs
python3 scripts/style_lint.py site/practice/00-start.html site/practice/03-copy.html site/practice/04-cards.html site/practice/05-reel.html --baseline docs/results/phase-9/baseline.json --output /tmp/aic-lint.json
python3 scripts/style_lint.py site/practice/e2e.html --output /tmp/aic-e2e-lint.json
python3 scripts/check_site.py --output /tmp/aic-site.json
# 키트 재검증은 출력이 없는 새 복사본과 Python 3.11+ venv를 준비해 실행해요.
python3 docs/results/phase-AIc/verify-kit.py /tmp/새복사본/starter-kit
```

## 남은 통합·검증 범위

[phase-AIc-requests.md](phase-AIc-requests.md)에 공통 메타의 적용 가능한 diff와 요소별 통합 diff를 남겼다. 실습 6·7의 서비스/키트 분기, 목차·pager, 크레딧 역링크, 용어집, PROJECT_STATE·진행 페이지는 통합 담당자가 적용한다. 새 용어는 [phase-AIc-glossary.md](phase-AIc-glossary.md)에 있다. AIc 완료는 그 공통 통합이나 배포 완료를 의미하지 않는다.

실제 서비스 가입·로그인·생성·편집·유료 기능·다운로드, 한국 계정별 메뉴·잔여량, 실제 휴대폰 조작·원본 전송·게시 성공은 이번에 실행하지 않았다. 공식 자료와 기존 조사 노트로 절차를 작성했고, 사용자 화면에서 버튼·한도·출력 조건을 확인하는 방법을 붙였다. 유료 API 호출·결제·인스타 로그인·포스팅·commit·push는 하지 않았다.

`python3 scripts/notify.py "✅ [AIc 완료] …" docs/results/phase-AIc/00-start-1280.png`로 한국어 5줄 보고와 대표 화면을 전송했다. 응답 `sent 200`으로 성공을 확인했다. 공통 메타 diff도 임시 복사본에서 `patch --dry-run`으로 적용 가능함을 확인했다.
