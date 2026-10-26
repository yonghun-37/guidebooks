너는 ai-insta 프로젝트의 작업자(Codex)다. AGENTS.md, docs/PLAN.md("Hermes 호출법"), research/FACT-SHEET.md, research/BRIEFING.md ⑦, docs/results/phase-7w-verify-list.md, docs/learner-questions.md(있으면)를 읽어라.
이번 작업은 **Phase 1c. 검색 복구 후 재조사**다. 사용자가 Hermes의 웹 검색 차단을 해제했다(2026-10-26 확인: 403 없음). Phase 1·1b·7r 원응답 다수가 검색 중계 403으로 근거가 비었으므로 공백을 Hermes로 다시 채운다. site/, starter-kit/, site/drafts/는 다른 작업자가 수정 중이니 건드리지 마라. commit하지 마라.

질의 한도 20회(재시도 포함), 최대 4개 병렬, `--max-turns 40`. 질의 파일 $RUN/queries/r2-*.txt, 원응답 $RUN/raw/r2-*.md. 공통 요구(한국어, 출처 URL+게시/갱신일, 공식 우선, 미확인 표시, 한국 가용성, 2026-10 기준)를 넣는다.

우선순위:
1. **인스타 앱 한국어 UI 절차(실습 확인 목록)**: 프로페셔널 계정 전환 메뉴 경로, 계정 추가·새 계정 만들기, 앱 한 곳에 추가 가능한 계정 수, 2단계 인증 경로, 캐러셀·릴스 게시 흐름, AI 정보 라벨 토글 위치, 유료 파트너십 라벨 위치, 예약 게시 위치와 최대 예약 기간, 인사이트 보는 법. phase-7w-verify-list.md의 항목을 모두 대상으로.
2. **돈 버는 구조의 구체 수치(학습자 질문)**: 인스타가 2026년 한국에서 조회수 기반 지급을 하는지(보너스 프로그램 현황), 선물/구독 현행 조건, 한국 인스타 협찬 단가 공개 자료(팔로워 구간별), 쿠팡 파트너스 현행 수수료율·SNS 규정, 체험단·협찬 플랫폼(레뷰 등) 구조, 유튜브 쇼츠·틱톡과의 수익 비교 수치.
3. **FACT-SHEET의 '미확인/추가 조사 필요' 항목** 중 교과서 판단에 중요한 것(API 게시 한도 100/50 상충의 최신 상태, 수익화 정책의 정적 영상 제한 원문, AI 라벨 한국 적용, 저작권 뉴스 인용 기준, 실패·제재 사례).

산출물: research/r2-<topic>.md, SOURCES.md·FACT-SHEET.md 갱신(기존 항목의 확인 수준이 올라가면 갱신 표시, 새 사실은 R2-* ID), docs/results/phase-1c.md(공백 해소표: 이전 상태 → 이번 결과), phase-7w-verify-list.md의 각 항목에 "확인됨: 실제 메뉴 이름 / 여전히 미확인" 열 추가.
핵심 공식 출처 8개 이상은 직접 열어 확인한다.
마지막에 `python3 scripts/notify.py "✅ [Phase 1c 재조사 완료] 공백 N개 중 N개 해소 ..."`로 한국어 보고.
