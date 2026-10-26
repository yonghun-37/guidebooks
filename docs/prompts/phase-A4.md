너는 ai-insta 프로젝트의 작업자(Codex)다. AGENTS.md, .agents/skills/guidebook-writing·guidebook-pipeline, **docs/STYLE-GUIDE.md(최우선)**, **docs/DESIGN-advanced.md**, docs/learner-questions-advanced.md, research-advanced/(BRIEFING·FACT-SHEET·SOURCES·노트), docs/results/phase-A1.md·phase-A2.md, **auto-kit/(README와 코드, 실제로 mock 실행해 본다)**, 그리고 site-shorts의 기존 구조(assets/book.js·book.css·common.js·practice.js, practice/의 실습 장 두 개, e2e.html)를 읽어라.
이번 작업은 **Phase A4. ShortsBook(쇼츠) 심화편(API 완전 자동화) 집필** 이다. 담당: `site-shorts/advanced/`(A0~A9 + e2e.html)와 그 전용 assets(`site-shorts/assets/advanced.css`·`advanced.js`, 필요하면 `assets/img/advanced/`). 공통 파일(book.js·book.css·common.js·practice.js·index·glossary·credits)은 **이 작업에서만 예외적으로** 심화 트랙 연결에 필요한 최소 변경을 허용한다(표지·목차에 세 번째 트랙 "심화편(API 자동화)", 장 데이터, 용어, 출처 A###). 다른 책 폴더·키트·research는 수정하지 마라. commit하지 마라.

- 플랫폼 중심: YouTube Data API(OAuth·테스트 모드 토큰 만료·할당량·미검증 앱 비공개 잠금과 감사·재개 업로드·예약·AI 공개 필드·Analytics), 쇼츠 자동 제작(LLM 대본 → TTS → 이미지/영상 생성 API → ffmpeg 조립·자막) 흐름.
- 장 구성: STYLE-GUIDE 틀 + 심화 실습형 — 장마다 "이 장에서 만드는 것", 복사해 실행하는 명령(Windows/macOS 탭), auto-kit의 실제 출력과 일치하는 "이렇게 보이면 성공", 흔한 오류 메시지와 해결 표, 비용 상자(편당·월, 날짜), "확인할 점" 상자. 개발자 콘솔·대시보드 화면은 캡처 금지, 직접 그린 도식과 "보통 이런 이름 + 공식 문서 링크 + 버전에 따라 다를 수 있다" 표준 문구.
- 필수 도식/도구: A0 파이프라인 전체 그림(단계 클릭 → 해당 장), A1 상태 흐름(실패·재시작), A2 비용 계산기(편수×공급자 단가, 상한), A5 게시 API 호출 순서 시퀀스(요청·응답 예, 토큰 가림), A6 자동 품질 관문 판정 흐름(검사별 통과/예외 대기열), A7 실행 방식 고르기 분기(로컬/GitHub Actions, 노코드는 상자로)·하루 실행 타임라인, A8 개선 루프 그림.
- 결론 먼저: "처음엔 이 조합" 하나(A1 BRIEFING 결론)와 월 비용. **목표는 전자동**(주제 선정→생성→자동 품질 관문→게시→분석→다음 주제 반영)이고, 승인제(첫 1~2주) → 사후 확인 → 전자동 순서로 넘어가는 기준(관문 통과율·예외 수)을 구체적으로 안내한다.
- 모든 사양·한도·가격은 research-advanced 근거 [A###] 각주, 2026년 10월 조사 기준. 근거 없는 숫자 금지. 사실 ID·내부 용어 본문 금지.
- 검증: style_lint, check_site(site-shorts), 1280/375/360px·라이트/다크·콘솔·키보드. 결과 docs/results/phase-A4.md + 스크린샷 docs/results/phase-A4/. 끝나면 `python3 scripts/notify.py "✅ [A4 완료] ..." <대표 스크린샷>`.
- **시각자료**: docs/STYLE-GUIDE.md 6절 — 개수 기준 없음. 흐름·숫자·선택지 비교·화면 위치·결과 예시·구조처럼 그림이 더 잘 전달하는 내용은 적극적으로 그림으로, 장식·개수 채우기는 하지 않는다.
- **범위**: docs/DESIGN-advanced.md 1.1 — 심화편은 API와 코드만. Canva·미리캔버스·Clipchamp·CapCut 같은 화면 조작 웹 도구는 다루지 않는다(카드는 코드 템플릿, 이미지는 생성 API, 영상은 ffmpeg).
- **전자동·시각자료**: DESIGN-advanced 1절(전자동 목표, 운영 모드 3종)과 1.2절(심화편 시각자료 목록)을 따른다. 심화편은 그림이 핵심이다: 시스템 구성도, 하루 실행 타임라인, API 시퀀스, 상태 흐름, 품질 관문 판정 흐름, 폴더·설정 구조, 비용·할당량 차트, 대시보드·알림 예시를 내용에 맞게 적극적으로 쓴다(직접 그린 SVG, 라이트/다크).
