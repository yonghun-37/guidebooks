너는 ai-insta 프로젝트의 작업자(Codex)다. AGENTS.md, .agents/skills/guidebook-writing·guidebook-pipeline, **docs/STYLE-GUIDE.md(최우선 문체)**, **docs/DESIGN-blog-advanced.md 전체(8절이 3·4절보다 우선)**, docs/DESIGN-baby.md 8절, docs/learner-questions-blog-advanced.md, research-blog-advanced/(BRIEFING·FACT-SHEET·SOURCES), **docs/results/phase-BX3k.md와 blog-auto-kit/(README, course/commands.md, course/expected/ — 실제로 mock 실행해 본다)**, 그리고 site-blog의 기존 구조(assets/book.js·book.css·common.js, practice/의 장 두 개, chapters/10-automation.html)와 형식 참고로 site/advanced/(인스타 심화편 A0·A6)를 읽어라.

이번 작업은 **Phase BX3. BlogBook 심화편 뼈대 + 샘플 2장**이다. 담당: `site-blog/advanced/`(00-start.html 자리, **01-environment.html, 09-sponsorship.html**, 나머지 장은 "준비 중" 자리 페이지), 전용 assets(`site-blog/assets/advanced.css`·`advanced.js`, 필요하면 `assets/img/advanced/`), 그리고 **이 작업에서만** 세 번째 트랙 연결에 필요한 최소 변경: `site-blog/assets/book.js`(트랙 "심화편(코드 운영)", A0~A12+E2E 장 데이터, 상태 '준비 중'/'완성'), 표지 `site-blog/index.html`의 트랙 진입 링크. 다른 폴더·키트·research는 수정하지 마라. 키트가 본문과 다르면 키트를 고치지 말고 `docs/results/phase-BX3-requests.md`에 적어라. commit하지 마라.

## 장 형식 (DESIGN 1.2 — 모든 심화 장의 틀이 된다)
먼저 답부터 → 이 장에서 만드는 것(파일 이름)·끝나면 되는 것 한 문장 → 한눈에 보기(그림) → **시작 상태 확인**(`python course.py start A?` / `check`) → 단계(명령: Windows PowerShell / macOS·Linux 탭 → "이렇게 보이면 성공": **course/expected/의 실제 출력에서 그대로 가져온다**) → 코드 읽기(발췌 25줄 이하 + 아래 "읽는 법" 표: 줄 → 하는 일, 파일:줄 링크) → 바꿔 보기(설정 한 줄 바꾸고 결과 차이) → 흔한 오류 표(실제 오류 문구 → 원인 → 고치는 명령) → 체크포인트(`course.py check`) → 확인할 점 상자(하나) → 정리.
- 장 머리에 "2026년 10월 조사 기준" 한 번. 사양·조건·가격·법 조항은 [BX###] 각주. 근거 없는 숫자·기대 수익 금지. 사실 ID·Phase 이름 등 내부 용어 본문 금지.
- 서윤(질문)·태오(직답) 대화는 장마다 1~2번, 짧게. 예시 블로그 「봄이랑 크는 집」.
- mock / 로컬 WordPress(Docker) / 실제 블로그의 "성공 화면"을 구별해서 보여 준다(DESIGN 8절).
- 관리자 화면·광고·제휴 사이트는 캡처 금지. 직접 그린 위치 그림 + "보통 이런 이름 + 공식 링크 + 버전에 따라 다를 수 있음".
- 시각자료: STYLE-GUIDE 6절. 흐름·상태·폴더 구조·요청/응답은 그림으로. 개수 채우기 금지. 라이트/다크 둘 다.

## 샘플 1: A1 같은 결과가 나오는 작업 환경
Python 확인 → 키트 폴더 → venv → `course.py doctor` → mock WordPress 서버 켜기 → `blog.py run --sample`(또는 BX3k가 정한 명령) → 결과 폴더 그림 → 바이트가 같은 이유(고정 날짜·시드) 짧게 → 꼬였을 때 `course.py reset`/`start` → (선택 상자) Docker로 로컬 WordPress 7.1.3. 학습자 질문 A1 6개에 본문이 직답하는지 마지막에 표로 자체 점검(결과 문서에만, 본문에 넣지 않음).

## 샘플 2: A9 육아용품 협찬 받기
협찬 대장 상태 기계 그림(문의→검토→수락/거절→계약→제품 수령→작성→광고주 확인→최종 사람 승인→발행→성과 보고→정산), **거절 사례: 「포근담요」 낮잠 이불**(안전 수면 충돌 → 프로젝트 거절, 이유 기록·정중한 거절 회신 예시), **수락 사례: 「도담」 그림책 꽂이**(분류·리콜 확인·권리·AI 허용 여부 확인 → 사람 작성/허용된 경로 → 대가성 표시 위치 → 광고주 확인 ≠ 최종 승인 → 발행 → 결과 보고서), 미디어킷 생성(아이 정보 비노출), 계약 때 물어볼 질문 목록, 세금 기록(판단은 공식 안내 링크, 육아휴직급여 수급 중 신고 확인). 법적 금지 / 프로젝트 거절 / 자료 보류 세 판정을 표로. 인터랙션: 협찬 문의 하나를 상태 기계로 끝까지 옮겨 보는 도구(키보드 조작·모바일 폭 지원, 저장은 `blogbook:` localStorage, 저장 차단 처리).

## 검증
style_lint, `scripts/check_site.py`(site-blog), 1280/375/360px × 라이트/다크, 콘솔 오류 0, 키보드, JS 없이 본문 읽기. 본문의 모든 명령을 빈 폴더 복사본에서 실제로 실행해 "이렇게 보이면 성공"과 비교(결과 문서에 대조표). 기존 이론·실습 페이지 회귀 없음.
결과 docs/results/phase-BX3.md(+스크린샷 docs/results/phase-BX3/), 남은 장 집필자에게 줄 "장 틀 사용법" 한 쪽. `python3 scripts/notify.py "✅ [블로그 심화 샘플 완료] ..." <대표 스크린샷>`.
