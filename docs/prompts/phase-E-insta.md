너는 ai-insta 프로젝트의 작업자(Codex)다. AGENTS.md, .agents/skills/guidebook-writing·guidebook-pipeline, **docs/STYLE-GUIDE.md(특히 7절 예시 원칙 — 이번 작업의 기준, 6절 시각자료)**, docs/DESIGN.md, research/(ai-production.md, FACT-SHEET, SOURCES, 출처·저작권 관련 노트), docs/results/phase-V-insta.md, 그리고 site/ 전체와 starter-kit/(README, samples/, 데이터·프롬프트, 테스트)를 읽어라.
사용자 지적(원문): "쇼츠 같은 건 예시로 좀 그럴싸한 걸 해야지 … 인스타도 마찬가지야. 현실성 있는 예제로 변경해." 지금 ReelsBook의 예시는 "가상 별빛도서관, 조용한 독서 모임", "초록작업실 종이 재사용", "달빛마을 산책 지도"처럼 아무도 보지 않을 소재다. 이번 작업은 **Phase E-insta. ReelsBook 예시 전면 교체** 다. 담당: site/ 전체(advanced/ 제외 — 아직 없음)와 starter-kit/의 samples·예시 데이터·README 예시(코드 로직 변경은 최소, 테스트 통과 유지). 다른 폴더는 수정하지 마라. commit하지 마라.

## 새 예시 (하린의 계정 — 기본안, 더 나은 근거가 있으면 이유를 적고 조정)
- 계정 콘셉트: 실제로 팔로우할 만한 정보 계정. 예: "출근길 3분 생활 뉴스"(생활·돈·제도 변화 요약 카드뉴스).
- **대표 뉴스카드**: "다음 달부터 바뀌는 생활 제도 3가지", "청년 ○○ 지원 신청 방법 한 장 정리" 같은 실제로 저장·공유되는 카드. **원자료는 상업 이용·변경이 허용되는 공공 자료**(예: 정책브리핑 등 공공누리 제1유형 표시 자료)를 쓰고, 이용 조건·출처 표기 방법을 research와 공식 안내로 확인해 각주를 단다. 확인이 안 되면 실제 제도 이름·금액을 지어내지 말고 "예시 문안"으로 형식만 보여 준다.
- **카드 → 모션 릴스**: 같은 카드로 만든 15초 릴스.
- **얼굴 없는 해설 릴스**: 같은 주제를 30초 음성 해설로("신청 전 꼭 확인할 3가지").
- **AI 영상 생성 릴스**: 정보 계정에 어울리는 짧은 AI 장면(예: 출근길 도시 풍경 위에 자막) — 실존 인물·브랜드 금지.
- 기획 → 원문 대조 → 카드 문안 → 디자인 → 릴스 → 게시 → 지표 해석까지 장을 넘어 같은 콘텐츠로 이어진다.

## 할 일
1. 기존 인위적 예시(가상 별빛도서관·초록작업실·달빛마을 등) 전수 목록 docs/results/phase-E-insta-before.md.
2. 이론·실습·부록(prompts, ai-models, lab)·JS 데이터의 예시 문장·프롬프트·좋은/나쁜 예·계산 예·그림을 새 예시로 교체. 사실·정책·수치·각주·인터랙션 동작은 유지.
3. AI 예시 이미지 새로 생성(카드 배경, 릴스 장면 등 2~4장, "AI 생성 예시"+프롬프트, WebP 400KB 이하). 쓰지 않는 기존 예시 이미지 삭제, 크레딧 갱신.
4. starter-kit/samples: 새 예시로 news.json·copy.json·카드 PNG·reel.mp4·자막을 README대로 실제 실행해 다시 만든다. 공공 자료를 쓰면 출처 표기를 카드·캡션에 넣는다. 동봉 샘플의 live 게시 차단 장치는 유지한다. pytest 통과.
5. 검증: style_lint, check_site(site), 1280/375/360px × 라이트/다크, 콘솔 오류, 내용 보존 검사. 남은 인위적 예시 grep 0건. 스크린샷 docs/results/phase-E-insta/.
6. 결과 docs/results/phase-E-insta.md, `python3 scripts/notify.py "📰 [E-insta 완료] ..." <새 카드 예시 이미지>`.
