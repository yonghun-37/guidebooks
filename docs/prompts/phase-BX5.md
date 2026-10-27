너는 ai-insta 프로젝트의 작업자(Codex)다. AGENTS.md, .agents/skills/guidebook-pipeline·guidebook-writing, docs/STYLE-GUIDE.md, docs/DESIGN-blog-advanced.md(8절 우선), docs/results/phase-BX3*.md·phase-BX4a*.md·phase-BX4b*.md(requests·glossary 포함), research-blog-advanced/SOURCES.md를 읽어라.

이번 작업은 **Phase BX5. BlogBook 심화편 통합 + 클린룸 재현**이다. 이 단계에서만 공통 파일을 고친다: site-blog/assets/book.js(심화 A0~A12·E2E 모두 '완성'), book.css·common.js·advanced.css/js(요청분), index.html(표지 세 번째 트랙 설명·진입), glossary.html, credits.html(심화 출처 BX### 등록 — check_site의 미등록 출처 0), 장 사이 이전/다음·상호 링크, shelf/(서가 카드의 블로그 편 설명에 심화편 한 줄, shelf/progress/index.html에 BX 단계 상태), docs/PROJECT_STATE.md(덮어쓰기, BlogBook 심화편 항목 추가). 키트 변경 요청(requests)은 **blog-auto-kit을 고쳐 반영**하되 고친 뒤 course/build_expected.py로 예상 출력을 다시 만들고 본문 성공 문구를 함께 맞춘다. commit하지 마라.

## 할 일
1. requests·glossary 반영, 용어 첫 사용 링크, 출처 등록, 장 데이터 완성, 이전/다음.
2. **가독성 일관성**: 14개 장이 같은 틀(먼저 답 → 만드는 것 → 한눈에 보기 → 시작 상태 → 단계 → 코드 읽기 → 바꿔 보기 → 흔한 오류 → 체크포인트 → 확인할 점 → 정리)인지 표로 점검하고 맞춘다. 두 OS 명령이 같으면 "공통" 블록 하나(A1·A9 포함 전 장). 코드 발췌 25줄 초과·"읽는 법" 표 누락·같은 설명 반복을 찾아 고친다. 장 사이 용어·파일 이름·명령·인물 말투 일치. A1의 "지금 할 일: A9로 이동, 중간 장은 준비 중" 같은 샘플 시기 문구 제거.
3. **본문 ↔ 키트 일치 자동 검사**: 스크립트 `scripts/check_blog_advanced.py`를 만든다 — 본문 HTML의 명령 블록을 추출해 course/commands.md와 비교, "이렇게 보이면 성공" 블록을 course/expected/의 실제 출력과 비교, 코드 발췌가 키트 파일의 해당 줄과 같은지 비교(파일:줄 표기 기준). 불일치 0이어야 한다. `--check` 모드로 게이트에 쓴다.
4. **클린룸 재현**: scripts/repro_blog_advanced.sh 통과 + 본문 순서대로(A0→E2E) 명령을 빈 폴더 복사본에서 실행하는 재현을 한 번 더(스크립트 4가 추출한 명령 사용). 결과 원문 끝부분을 결과 문서에.
5. 게이트: style_lint(심화 전 장), scripts/check_site.py(site-blog 오류 0, 다른 네 책도 오류 0 유지), 브라우저 1280/375/360 × 라이트/다크(심화 14페이지 + 표지·목차), 콘솔 오류 0, 키보드, JS 없이 읽기, 도구 동작, pytest(blog-auto-kit 전체), 다른 키트 테스트 회귀 없음.
결과 docs/results/phase-BX5.md(+스크린샷). `python3 scripts/notify.py "✅ [BX5 통합 완료] ..."`.
