# ai-insta 개발 지침

이 저장소는 "AI로 인스타그램 릴스·뉴스카드를 자동 생성·포스팅해 수익화하기" 입문 교과서(정적 웹사이트)와 따라 하기용 스타터 키트를 만든다. 문서와 교과서 본문은 한국어로 쓴다.

## 역할 분담

- **Claude Code**: 설계(docs/DESIGN.md, docs/PLAN.md)와 단계별 검수를 맡는다.
- **Codex**: 실제 작업(조사 지휘, 원고, 사이트 구현, 스타터 키트, 검증)을 맡는다.
- **Hermes**(`/home/yonghun/project/hermes-research`의 컨테이너, provider `openai-codex`): 웹 자료조사를 맡는다. 사용법은 docs/PLAN.md의 "Hermes 호출법"을 따른다.

## 규칙

- 현재 단계의 지시는 docs/PLAN.md의 해당 Phase만 따른다. 다른 Phase 작업을 미리 하지 않는다.
- 단계를 마치면 `python3 scripts/notify.py "메시지"`로 디스코드에 짧게 보고한다(한국어, 5줄 이내, 무엇을 했고 산출물 경로와 남은 문제). 토큰을 출력하거나 다른 채널로 보내지 않는다.
- 상태는 docs/PROJECT_STATE.md를 덮어써서 최신으로 유지한다. 단계별 결과는 docs/results/phase-N.md에 추가한다.
- hermes-research 저장소는 **읽기 전용**으로 취급한다. 예외: Hermes 질의 파일과 원응답을 `hermes-research/output/ai-insta-research-20261026/` 아래에만 쓴다. 그 저장소의 코드·config·runtime·Skill·Prefect·DB는 변경하지 않는다.
- 유료 API 키를 새로 쓰거나 결제를 하지 않는다. 실제 인스타그램 계정에 로그인·포스팅하지 않는다.
- 사실 주장(정책, 수치, 요건, 가격)은 research/의 출처 노트에 근거가 있어야 한다. 근거 없는 수치는 쓰지 않거나 "확인 필요"로 표시한다. 정책은 "2026년 10월 조사 기준"을 명시한다.
- 참고 사이트(art.euiyun.com/color)는 구조·학습 설계·UX 패턴만 참고한다. 그 사이트의 문장, 이미지, CSS/JS 코드를 복사하지 않고 새로 구현한다.
- 등장인물·사례 계정은 가상이다. 실존 인물·브랜드를 사칭하지 않는다. 실제 사례를 인용할 때는 출처를 단다.
- Codex 샌드박스는 .git 쓰기가 막혀 있으므로 commit은 Claude Code가 Phase 검수 후 한다. Codex는 commit을 시도하지 않는다. push는 하지 않는다.
