너는 ai-insta 프로젝트의 작업자(Codex)다. AGENTS.md, .agents/skills/guidebook-writing·guidebook-pipeline, **docs/STYLE-GUIDE.md(특히 7절 예시 원칙 — 이번 작업의 기준, 6절 시각자료)**, docs/DESIGN-shorts.md, research/ai-production.md, research-shorts/FACT-SHEET.md, 그리고 site-shorts/ 전체와 shorts-kit/(README, samples/, prompts/, 테스트)를 읽어라.
사용자 지적(원문): "쇼츠 같은 건 예시로 좀 그럴싸한 걸 해야지. 케이블 같은 건 너무 설명을 위한 설명 아니냐?" 이번 작업은 **Phase E-shorts. ShortsBook 예시 전면 교체** 다. 담당: site-shorts/ 전체(advanced/ 제외 — 아직 없음)와 shorts-kit/의 samples·prompts·예시 데이터(코드 로직 변경은 최소, 테스트 통과 유지). 다른 폴더(site/, auto-kit/, blog-kit/, research*)는 수정하지 마라. commit하지 마라.

## 새 예시 (도윤의 가상 채널 "자취생 10분 생존법" — 기본안, 더 나은 근거가 있으면 docs/results에 이유를 적고 조정)
- **책을 꿰는 대표 영상 = 유형② 얼굴 없는 해설**: 예 "월급날 10분, 통장 4개로 나누는 법" 또는 "전기요금 덜 나오는 자취방 습관 3가지" 같은 1분 생활·돈 상식(숫자·제도는 근거 있는 것만, 없으면 일반 상식 수준으로 쓰고 금액을 지어내지 않는다).
- **유형① 직접 촬영 + AI 편집**: "전자레인지 5분 계란밥"처럼 휴대폰으로 실제 찍을 수 있고 보기 좋은 자취 요리.
- **유형③ AI 영상 생성**: "펭귄 택배기사의 하루"처럼 캐릭터가 있는 짧은 AI 상상 스토리(실존 IP·캐릭터 모방 금지), 장면 간 캐릭터 일관성을 보여 주는 예.
- 세 영상 모두 기획 → 훅 3안 → 대본 → 장면 목록 → 음성 → 장면 → 편집·자막 → 출력 → 제목·설명 → 업로드 → 지표 해석까지 장을 넘어 같은 영상으로 이어진다.

## 할 일
1. `grep`으로 케이블·종이 로봇·종이 분류·책상 정리 등 기존 인위적 예시를 모두 찾아 목록화(docs/results/phase-E-shorts-before.md).
2. 이론 장·실습 장·부록(prompts, ai-models, lab)·JS 데이터(y4b.js, operations.js 등)의 예시 문장·프롬프트·좋은/나쁜 예·계산 예·그림을 새 예시로 교체한다. 사실·정책·수치·각주·인터랙션 동작은 그대로 유지한다.
3. AI 예시 이미지를 새로 만든다(이미지 생성 기능): 유형③ 캐릭터 기준 이미지 + 장면 키프레임 2~3장(같은 캐릭터 일관성), 유형② 장면 그림 1~2장, 유형① 완성 장면 느낌의 예시 1장. "AI 생성 예시"와 실제 사용 프롬프트를 함께 표시, WebP 400KB 이하. 실존 인물·브랜드·로고 금지. 쓰지 않게 된 기존 예시 이미지는 지우고 크레딧·생성 기록을 맞춘다.
4. V-shorts에서 그린 도식(샷 크기, 자막 위치, 편집 영역 등)의 소재도 새 예시로 다시 그린다.
5. shorts-kit/samples: 대표 영상(유형②)으로 script.json·자막·preview·short.mp4를 다시 만든다(README대로 실제 실행, 10MB 이하). README·prompts 예시도 교체, pytest 통과.
6. 검증: style_lint, check_site(site-shorts), 1280/375/360px × 라이트/다크, 콘솔 오류, 기존 내용 보존 검사(사실·각주·인터랙션). 남은 인위적 예시 grep 0건. 스크린샷 docs/results/phase-E-shorts/.
7. 결과 docs/results/phase-E-shorts.md, `python3 scripts/notify.py "🎬 [E-shorts 완료] ..." <새 AI 예시 이미지 또는 대표 스크린샷>`.
