너는 ai-insta 프로젝트의 작업자(Codex)다. AGENTS.md, **docs/STYLE-GUIDE.md 7절(예시 원칙)**, docs/DESIGN-advanced.md, docs/results/phase-A2.md, docs/results/phase-E-insta.md·phase-E-shorts.md(두 책의 새 예시), auto-kit/ 전체를 읽어라.
이번 작업은 **Phase A2b. auto-kit 검수 수정** 이다. auto-kit/만 수정한다(site-blog/는 다른 작업자들이 집필 중 — 건드리지 마라). commit하지 마라.

Claude 검수 지적:
1. **예시가 인위적이다**: mock 소스·초안이 "가상도서관의 책 소식, 책 12권"이다. 사용자가 두 번 지적한 문제다("설명을 위한 설명", "현실성 있는 예제로"). 두 책의 새 예시와 맞춘다 — insta 흐름은 하린의 "출근길 3분 생활 뉴스"(예: 청년 지원금 신청 전 확인할 3가지, 생활 제도 변화 요약 — 실제 제도명·금액은 지어내지 말고 예시 문안 표시), shorts 흐름은 도윤의 "자취생 10분 생존법"(예: 월급날 돈 네 칸 메모 해설). sources 예제 피드(RSS 픽스처)·topics·mock 공급자 출력·샘플·README·SVG 도식 속 예문을 모두 교체하고, 품질 관문(사실 대조)이 새 예시로도 의미 있게 동작하는 테스트(통과 1, 원문에 없는 숫자로 걸리는 예 1)를 둔다.
2. **Python 버전 불일치**: README는 "3.10 이상 필요"인데 Pillow==13.0.0 등은 3.10에 설치되지 않는다(실제로 3.10.12에서 `No matching distribution` 확인). 최소 버전을 3.11로 통일하고 README·doctor.py 검사·오류 표를 맞춘다. 설치 명령은 Windows `py -3.11`, macOS `python3.11`(또는 설치한 3.11+) 기준.
3. 그 밖에 README 명령을 깨끗한 임시 복사본에서 Python 3.11로 다시 실행해 '이렇게 보이면 성공'을 실제 출력과 맞춘다. pytest 전체 통과.
결과는 docs/results/phase-A2.md 끝에 "A2b 수정" 절로 추가, `python3 scripts/notify.py "✅ [A2b 완료] auto-kit 예시·Python 버전 수정 ..."`.
