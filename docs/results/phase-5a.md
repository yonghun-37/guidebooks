# Phase 5a — 2~5장 집필·시뮬레이터

2026-10-26. 사용자 지정 범위는 2·3·4·5장이다. PLAN.md의 기존 5a 분할보다 이번 지시를 우선했다. 요구사항·구현 전략·결과를 이 저장소의 Phase 결과 문서에 모으며 별도 명세·ADR은 만들지 않는다.

## 요구사항과 구현

- [x] AGENTS·DESIGN 3/4/5/9절·템플릿·1장·book.js/book.css/common.js·브리핑·사실표·지정 조사 노트·키트 README와 관련 수집 코드를 읽었다.
- [x] book.js의 slug·제목·결과물을 유지해 2~5장을 작성했다. 각 장은 9블록, 상단 메타, 번호 단계별 시간·준비물·결과·오류, 복사할 메모, 저장되는 완료 체크, 가상 인물 서사, 4문항 퀴즈와 본문 근거 링크를 갖춘다.
- [x] 원문 각주에 FACT-SHEET 사실 ID·SOURCES 번호·발표/갱신일·확인 수준과 조사 기준일을 연결했다. 공개 사례의 확인 범위와 미확인 상태를 유지했다.
- [x] 각 장의 공통 래퍼 기반 도구 2개(개념 그림+입력 도구)를 구현했다. 네이티브 입력·키보드 대안·텍스트 결과·교육용 배지·가정값·무너뜨리기 프리셋을 제공한다.
- [x] 5장 명령을 starter-kit/.venv에서 실행했다. 합성 RSS의 3개 항목과 synthetic=true를 확인했다.
- [x] 최종 브라우저 결과·화면 검토 확정
- [x] Discord 스크린샷 첨부 보고 (HTTP 200)

| 장 | 원고 | 전용 JS | 입력 도구와 결과물 |
| --- | --- | --- | --- |
| 2 | [02-formats.html](../../site/chapters/02-formats.html) | [ch02.js](../../site/assets/sim/ch02.js) | 신호 가중치의 임의 점수·분모 0 체험, 포맷 선택 메모 |
| 3 | [03-revenue.html](../../site/chapters/03-revenue.html) | [ch03.js](../../site/assets/sim/ch03.js) | 여섯 경로 현금 장부, 수익 경로 두 개 |
| 4 | [04-niche.html](../../site/chapters/04-niche.html) | [ch04.js](../../site/assets/sim/ch04.js) | 근거·시간을 분리한 자기평가, 계정 기획 시트 |
| 5 | [05-sources.html](../../site/chapters/05-sources.html) | [ch05.js](../../site/assets/sim/ch05.js) | 허락·인용·다른 권리·사실 대조의 누락 확인, RSS 목록·인용 규칙 |

2장 형식 선택 → 3장 지급자·대가 → 4장 독자·질문·시간 → 5장 원문·권리 기록 → 6장 문안 재료로 결과물을 연결한다. 수익 장부는 설계 9절대로 3장에 두고 팔로워·도달에서 월수익을 예측하지 않는다. 점수는 임의 연습값이며 시간 0·근거 공백·권리 미확인을 합계로 덮지 않는다.

## 검증 기록

실행 환경은 Linux, 기존 Playwright Core·Chromium 1228이다. Windows/macOS의 실행 성공은 주장하지 않았다. 새로운 패키지 설치·유료 키·계정 로그인·게시·커밋·push는 하지 않았다.

실제 키트 실행(working directory: starter-kit):

```bash
.venv/bin/python fetch_news.py --feed fixtures/sample-feed.xml --output output/phase-5a/news.json
```

exit 0. 합성 표시와 세 항목을 직접 확인했다. 산출물은 Git 제외 output 폴더에 있고 재현 명령·해시는 [audit.json](phase-5a/audit.json)에 있다. 본문 전체 수집이나 실제 RSS URL 요청은 하지 않았다. 코드로 Windows 명령 전체를 별도로 제시하지 않고 실행 파일 경로 차이만 짧게 안내한다.

확인한 명령:

```bash
node --check site/assets/sim/ch02.js
node --check site/assets/sim/ch03.js
node --check site/assets/sim/ch04.js
node --check site/assets/sim/ch05.js
python3 docs/results/phase-5a/audit.py
```

전용 JS 구문 검사와 사실 ID·해당 출처·원문 URL·출처 앵커·중복 ID·9블록·합성 JSON 정합성 검사가 통과했다. [audit.py](phase-5a/audit.py)·[audit.json](phase-5a/audit.json)은 이 범위의 재검증용이며 원고 의미와 법적 적합성을 자동 보증하지 않는다.

브라우저 재실행은 루트에서 정적 서버를 먼저 실행한 뒤 다음과 같이 한다.

```bash
python3 -m http.server 8765 --bind 127.0.0.1 --directory site
```

별도 터미널:

```bash
node docs/results/phase-5a/verify.mjs \
  /tmp/ai-insta-phase3-browser/node_modules/playwright-core/index.mjs \
  /home/yonghun/.cache/ms-playwright/chromium-1228/chrome-linux64/chrome
```

검사 과정에서 공통 모바일 용어 말풍선의 10px 넘침을 발견해 담당 HTML의 짧은 모바일 CSS로 보정했다. 검사기는 공통 테마 버튼의 실제 접근성 이름과 같은 문서 앵커 이동의 null 응답을 올바르게 처리하도록 고쳤다. 앵커는 DOM의 실제 ID도 확인한다. 이는 사이트 링크 실패를 숨기는 처리가 아니다.


최종 [브라우저 검사 결과](phase-5a/verification.json): **8개 화면 조합, 내부 링크·앵커 148개, 콘솔 오류 0, 링크 실패 0**. 네 장 모두 1280px·375px에서 문서 너비가 뷰포트를 넘지 않았다. 라이트·다크 모두 확인했다.

| 확인 항목 | 실행 결과 |
| --- | --- |
| 구조 | 각 장 9블록·4문항·도구 2개, 중복 ID 없음 |
| 퀴즈 | 오답 해설·정답 보기·잠금·초기화·전 문항 정답 점수 통과 |
| 개념 그림 | 방향키·Home·End·Enter, 선택 상태와 텍스트 결과 통과 |
| 2장 가중치 | 가중치 변경 시 순위 변경, 0 가중치 분모 오류를 텍스트로 표시 |
| 3장 장부 | 예시 현금 잔액 90,000원·시간당 9,000원, 빈칸·음수·상한 초과 차단, 0시간·적자 표시 |
| 4장 점수표 | 범위 입력·근거 선택, 높은 합계라도 제작 여유 0 경고 |
| 5장 흐름도 | 선택 키보드 조작, 출처만 있는 상태·인용 근거·다른 권리 미해결·기록 모음 상태 분리 |
| 브라우저 저장·대체 | 체크 상태 재방문 복원, localStorage 차단에도 장부·체크 동작, JS 비활성 상태의 본문·정답 존재 |
| 외형 | 네 장의 1280px/375px 가로 넘침 없음, 다크 모드 확인, 아래 두 화면 직접 검토 |

화면 산출물:

- [데스크톱 수익 장부 · 1280×1700](phase-5a/desktop-ledger.png)
- [모바일 소재 권리 흐름도 · 375×1900](phase-5a/mobile-rights.png)

검사는 담당 장과 그 페이지에서 연결하는 내부 파일·앵커 범위다. 준비 중인 다른 장의 본문 품질이나 공통 목차 완성 상태까지 통과 판정한 것이 아니다.

## 공통 파일·한계·후속

- book.js·book.css·common.js·glossary.html·credits.html·index.html·PROJECT_STATE와 다른 담당 장은 수정하지 않았다. 기존 미추적 프롬프트와 병행 작업 산출물을 보존했다.
- 장 상태·메타데이터, 모바일 용어 말풍선 공통 보정, PROJECT_STATE 병합 문장은 [정확한 diff 요청](phase-5a-requests.md)에 있다. 미적용 상태에서는 공통 목차와 브라우저 제목이 ‘준비 중’이며 목차는 대기 페이지로 간다. 직접 HTML URL과 담당 장 사이의 정적 하단 이동은 동작한다.
- 새 용어는 [용어 인계](phase-5a-glossary.md)에 있다. 신규 용어를 미구현 앵커로 보내지 않고 용어집 기본 URL로 연결했다. 용어집·실험실·6장 이후와의 공개 등록 통합은 해당 담당자와 검수자의 후속 범위다.
- 실제 운영용 RSS 엔드포인트·매체별 상업 재사용 약관은 이번 조사에서 확인하지 못했다. 5장 결과는 동작하는 로컬 합성 RSS 목록과 운영 후보의 미확인 칸·직접 채울 권리표다. 실제 뉴스 수집 성공이나 상업 이용 허락을 주장하지 않는다.
- Gifts 과거 5,000/도움말 보고 500, 구독의 한국 현행 활성화·구매·지급 미확인, 초기 캐러셀 API 10개 발췌와 본문 20개 교정, Socialinsider 미래 분석 기간 문제를 독자에게 명시했다. 새로운 임의 성공률·단가·법적 안전 글자 수는 만들지 않았다.
- 한국 초보자의 성장·수익·거래 자격, 개별 저작물의 법적 적합성, 실기기·보조기기 전체·다른 브라우저·Windows/macOS 실행은 검증하지 않았다.

## 완료 보고

`python3 scripts/notify.py`로 한국어 5줄과 데스크톱 장부 스크린샷을 전송했고 HTTP 200을 확인했다. 토큰·개인 환경·Hermes 원응답은 산출물에 포함하지 않았다. 커밋은 시도하지 않았다.
