너는 ai-insta 프로젝트의 작업자(Codex)다. AGENTS.md, .agents/skills/guidebook-writing·guidebook-pipeline, **docs/STYLE-GUIDE.md(최우선)**, **docs/DESIGN-advanced.md**, docs/learner-questions-advanced.md, research-advanced/(BRIEFING·FACT-SHEET·SOURCES·노트), docs/results/phase-A1.md·phase-A2.md, **auto-kit/(README와 코드, 실제로 mock 실행해 본다)**, 그리고 site의 기존 구조(assets/book.js·book.css·common.js·practice.js, practice/의 실습 장 두 개, e2e.html)를 읽어라.
이번 작업은 **Phase A3. ReelsBook(인스타) 심화편(API 완전 자동화) 집필** 이다. 담당: `site/advanced/`(A0~A9 + e2e.html)와 그 전용 assets(`site/assets/advanced.css`·`advanced.js`, 필요하면 `assets/img/advanced/`). 공통 파일(book.js·book.css·common.js·practice.js·index·glossary·credits)은 **이 작업에서만 예외적으로** 심화 트랙 연결에 필요한 최소 변경을 허용한다(표지·목차에 세 번째 트랙 "심화편(API 자동화)", 장 데이터, 용어, 출처 A###). 다른 책 폴더·키트·research는 수정하지 마라. commit하지 마라.

- 플랫폼 중심: Instagram API(계정 종류·앱·권한·토큰·컨테이너→게시·캐러셀·릴스·한도·공개 URL 호스팅·인사이트), 뉴스카드 매일 자동 생성(RSS → LLM 요약·원문 대조 → 카드 렌더) 흐름.
- 장 구성: STYLE-GUIDE 틀 + 심화 실습형 — 장마다 "이 장에서 만드는 것", 복사해 실행하는 명령(Windows/macOS 탭), auto-kit의 실제 출력과 일치하는 "이렇게 보이면 성공", 흔한 오류 메시지와 해결 표, 비용 상자(편당·월, 날짜), "확인할 점" 상자. 개발자 콘솔·대시보드 화면은 캡처 금지, 직접 그린 도식과 "보통 이런 이름 + 공식 문서 링크 + 버전에 따라 다를 수 있다" 표준 문구.
- 필수 도식/도구: A0 파이프라인 전체 그림(단계 클릭 → 해당 장), A1 상태 흐름(실패·재시작), A2 비용 계산기(편수×공급자 단가, 상한), A5 게시 API 호출 순서 시퀀스(요청·응답 예, 토큰 가림), A6 실행 방식 고르기 분기(로컬/GitHub Actions/노코드).
- 결론 먼저: "처음엔 이 조합" 하나(A1 BRIEFING 결론)와 월 비용. 승인 1번이 들어간 자동화가 기본값임을 분명히.
- 모든 사양·한도·가격은 research-advanced 근거 [A###] 각주, 2026년 10월 조사 기준. 근거 없는 숫자 금지. 사실 ID·내부 용어 본문 금지.
- 검증: style_lint, check_site(site), 1280/375/360px·라이트/다크·콘솔·키보드. 결과 docs/results/phase-A3.md + 스크린샷 docs/results/phase-A3/. 끝나면 `python3 scripts/notify.py "✅ [A3 완료] ..." <대표 스크린샷>`.
- **시각자료**: docs/STYLE-GUIDE.md 6절 기준(이론 6개·실습 단계별 화면 위치 그림·심화 5개 이상, 인물 기준 시트로 삽화 그림체 통일 — 기준 시트 만드는 법은 docs/results/phase-V-insta.md)을 처음부터 지킨다.
