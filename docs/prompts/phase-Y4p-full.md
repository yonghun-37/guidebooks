너는 ai-insta 프로젝트의 작업자(Codex)다. 먼저 AGENTS.md, .agents/skills/guidebook-pipeline·guidebook-writing, **docs/STYLE-GUIDE.md(최우선)**, **docs/DESIGN-shorts.md**, **docs/DESIGN.md 12절(AI 제작 핵심 모듈)**, **research/ai-production.md(Phase R3 AI 제작 조사)**, docs/learner-questions-shorts.md, research-shorts/(BRIEFING·FACT-SHEET·SOURCES·QUESTION-MAP와 관련 노트), docs/reference-analysis-books.md 8절, docs/results/phase-Y3.md, 그리고 **사용자가 승인한 샘플** site-shorts/chapters/02-revenue.html·site-shorts/practice/08-publish.html을 읽어라. 샘플의 구성·문체·인물(도윤·서진)·컴포넌트를 기준으로 삼는다.
공통 규칙: 담당 파일만 수정(site-shorts/assets/book.js·book.css·common.js·practice.js, index, glossary, credits는 수정 금지 → docs/results/phase-Y4p-requests.md에 diff, 새 용어는 phase-Y4p-glossary.md). 모든 정책·수치는 research-shorts FACT-SHEET 또는 research/ai-production.md 근거와 각주. 근거 없는 숫자 금지. 학습자 질문 5개(learner-questions-shorts.md)에 직답. YouTube 로고·UI 복제 금지, 직접 그린 도식. commit하지 마라.
검증: style_lint(금지어·내부 용어·단서 기준), check_site(site-shorts), 1280/375/360px·콘솔 오류·키보드 조작. 결과 docs/results/phase-Y4p.md + 스크린샷 docs/results/phase-Y4p/. 끝나면 `python3 scripts/notify.py "✅ [Y4p 완료] ..." <대표 스크린샷>`.

## 이번 작업: Y4p (AI 제작 우선 실습편)

실습편 **0~7, 9, 10과 e2e.html** 집필(site-shorts/practice/, 실습 8은 승인된 샘플이므로 필요한 연결만). **사용자 지적: "어떤 AI로 영상을 어떻게 만드는지가 제일 중요한데 잘 안 보인다."** 따라서 실습 3~6은 **AI 도구로 실제 영상을 만드는 것이 기본 경로**이고, shorts-kit는 "자동화·무료 대안" 경로다.

- 실습 0 시작 전에: 오늘 만들 쇼츠 유형 3가지 중 하나 고르기(① 직접 촬영 + AI 편집 ② 얼굴 없는 해설: AI 대본·음성 + 스톡/AI 이미지 장면 ③ AI 영상 생성 쇼츠) — 각각 필요한 도구·무료 가능 여부·소요 시간.
- 실습 1 계정·채널(연습 채널, 2단계 인증, 계정 보호 상자).
- 실습 2 도구 준비: research/ai-production.md의 "처음엔 이것 하나" 추천 도구 가입(무료 등급), 무료 편집 프로그램 1종 설치, (선택) shorts-kit 설치.
- 실습 3 AI로 기획·대본: 추천 LLM에 붙여 넣을 복사용 프롬프트(훅 3안, 30~45초 대본, 장면 목록, 제목·설명), 좋은/나쁜 결과 예, 사실 확인.
- 실습 4 목소리: 본인 녹음(기본) 또는 추천 TTS(무료 범위·상업 이용 조건·AI 음성 표시), 파일 옮기기·변환.
- 실습 5 장면 만들기: 유형별 — 폰 촬영 가이드 / 스톡 영상·이미지(라이선스) / AI 이미지 생성(프롬프트, 9:16, 스타일 일관성) → 움직임 주기 / AI 영상 생성(한국 가용 도구, 무료 크레딧, 프롬프트 공식: 샷 크기·카메라 움직임·조명·스타일·길이, 여러 클립 일관성). 각 경로에 복사용 프롬프트와 예시.
- 실습 6 편집·자막: 추천 편집 프로그램에서 컷 → 음성 → 장면 맞추기 → 자동 자막 생성·수정 → 음악(오디오 보관함 등 권리 확인) — 버튼 표준 안내 문구. 키트 경로도 병기.
- 실습 7 9:16 출력·화질 확인, AI 사용 부분 기록(업로드 시 AI 표시 판단용).
- 실습 9 (선택) Data API 업로드, 10 지표 확인.
- **shorts-kit/(Y4k 완성본)과 docs/results/phase-Y4k.md를 읽고**, 키트 경로 명령은 깨끗한 임시 복사본에서 README대로 실제 실행해 '이렇게 보이면 성공'을 실제 출력과 일치시킨다.
- AI 결과 예시가 필요하면 너의 이미지 생성 기능으로 예시 이미지를 만들어 site-shorts/assets/img/ai-examples/에 넣고 "AI 생성 예시"와 사용한 프롬프트를 함께 표시한다(실존 인물·브랜드·로고 금지).
- ReelsBook 실습편의 F01~F15 교훈(실제 자료 분기, OS별 파일 저장, Python 버전, 녹음 변환, 토큰 숨김 입력, 총 소요 시간 표시)을 처음부터 반영한다. E2E 체크리스트로 실습 0→10 전체 단계를 묶는다.
