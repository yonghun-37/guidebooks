너는 ai-insta 프로젝트의 작업자(Codex)다. AGENTS.md, .agents/skills/guidebook-writing·guidebook-pipeline, **docs/STYLE-GUIDE.md(최우선 문체)**, **docs/DESIGN-blog-advanced.md 전체(8절 우선)**, docs/DESIGN-baby.md 8절, docs/learner-questions-blog-advanced.md, research-blog-advanced/(BRIEFING·FACT-SHEET·SOURCES·노트), **docs/results/phase-BX3.md의 "장 틀 사용법"과 샘플 완성본 site-blog/advanced/01-environment.html·09-sponsorship.html(이 형식을 그대로 따른다)**, docs/results/phase-BX3k.md, blog-auto-kit/(course/commands.md, course/expected/ — 실제로 실행해 본다)를 읽어라.

이번 작업은 **Phase BX4b. BlogBook 심화편 집필: A7, A8, A10, A11, A12, E2E (A9는 샘플 완성본 — 필요하면 다듬기만)**이다. 담당 파일: site-blog/advanced/의 07-ads, 08-affiliate, 10-analytics, 11-operations, 12-policy, e2e (.html)와 그 장 전용 assets(site-blog/assets/advanced-<장>.css/js, assets/img/advanced/<장>-*). 공통 파일(book.js, book.css, common.js, advanced.css/js, index, glossary, credits)과 다른 장·키트·research는 수정하지 마라 — 필요한 변경은 docs/results/phase-BX4b-requests.md에, 새 용어는 phase-BX4b-glossary.md에. 병렬로 다른 작업자가 나머지 장을 쓴다. commit하지 마라.

## 원칙 (사용자 핵심 요구: 재현 가능 + 가독성)
- **명령이 두 OS에서 똑같으면 탭을 만들지 말고 "Windows·macOS·Linux 공통" 블록 하나로** 보인다(탭은 실제로 다를 때만: 가상환경 만들기·활성화·파일 복사 등). 같은 내용 반복은 가독성을 해친다.
- 장 하나 = 결과물 하나. 샘플 장과 같은 순서(먼저 답 → 만드는 것 → 한눈에 보기 → 시작 상태 확인 → 단계 → 코드 읽기 → 바꿔 보기 → 흔한 오류 → 체크포인트 → 확인할 점 → 정리).
- 모든 명령은 course/commands.md 그대로, "이렇게 보이면 성공"은 course/expected/의 실제 출력에서 그대로. 키트를 고치지 말고 다르면 requests에 적는다.
- 코드 발췌 25줄 이하 + "읽는 법" 표. 학습자 질문(해당 장 6개)에 본문이 첫 문장에서 직답하는지 결과 문서에 자체 점검표.
- 사양·조건·가격·법 조항은 [BX###] 각주, 2026년 10월 조사 기준, 근거 없는 숫자·기대 수익 금지, 내부 ID 본문 금지. 건강 정보는 DESIGN-baby 8절. 브랜드·광고주는 가상.
- 관리자·광고·제휴 화면 캡처 금지, 직접 그린 위치 그림. 시각자료는 STYLE-GUIDE 6절(필요한 곳에 적극적으로, 개수 채우기 금지), 라이트/다크.

## 장별 필수 내용
A7: 신청 준비 점검표(공식 최소 글 수 기준 없음을 분명히), ads.txt, 광고 위치 템플릿 그림, 개인정보처리방침 의무/권장, 애드핏 사전 문의, 수익 보고서(예상/확정/입금 구분). A8: 링크 등록부, 대가성 문구 위치 미리보기 도구(제목·첫머리·링크 옆, 모바일), 쿠팡 최종 승인 기준과 API 자격 구분, live API는 선택(현행 확인 후), 영유아 제품 규제 표. A10: GA4/GSC 수집(시간대·지연·빈 행), 주간 보고서·다음 글감 점수·갱신 대상 글. A11: 하루·한 주 운영 타임라인 그림, 예약 실행(작업 스케줄러·cron·launchd·GitHub Actions — 상태를 runner 밖에), 알림, 백업·복구 실습, 키 교체, WP-Cron 지연. A12: 출시 전 점검표(구글 스팸 정책·공정위 지침 2026-06-01·영유아 제품·아이 사생활·저작권·세금: 현물·부가세·사업자 등록·육아휴직급여 수급 중 신고 확인). E2E: mock 완주 / 로컬 WordPress / 실제 블로그 세 열 진행표, 시나리오 6종 결과 기록.

## 검증
style_lint, scripts/check_site.py(site-blog), 1280/375/360px × 라이트/다크, 콘솔 오류 0, 키보드, JS 없이 본문 읽기. 본문 명령을 빈 폴더 복사본에서 실행해 성공 문구 대조표. 결과 docs/results/phase-BX4b.md(+스크린샷 docs/results/phase-BX4b/). `python3 scripts/notify.py "✅ [BX4b 완료] ..."`로 한국어 보고.
