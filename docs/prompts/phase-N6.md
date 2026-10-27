너는 ai-insta 프로젝트의 작업자(Codex)다. AGENTS.md, .agents/skills/guidebook-pipeline·guidebook-writing, docs/STYLE-GUIDE.md, **docs/DESIGN-baby.md(8·11절 최우선)**를 읽어라. 그리고 docs/results/phase-N3.md, phase-N4a.md, phase-N4b.md, phase-N4c.md, phase-N5.md의 **"통합 요청" 절을 모두** 읽어라.
이번 작업은 **Phase N6. BabyBook 통합** 이다. 이제는 site-baby 전체를 혼자 맡는다. 공용 자산도 수정할 수 있다. 다른 책(site/, site-shorts/, site-blog/)과 kit은 수정하지 마라. commit하지 마라.

1. 통합 요청을 모두 반영한다. 반영 / 반영 안 함(이유) 표를 결과 문서에 남긴다.
   - book.js·catalog.js의 장·실습 상태와 이전/다음 링크를 정리한다.
   - pending 링크를 실제 파일로 바꾼다. 쓸모가 없어진 pending.html은 지운다.
   - 표지의 목차를 정리한다.
2. **출처**: credits.html에 본문이 인용한 N### 전부를 SOURCES.md 원본대로 등록한다. 각주 앵커가 모두 살아 있게 하고, 장 하단에 임시로 단 '출처 원문'은 공용 방식으로 통일한다. 인용하지 않은 출처는 등록하지 않는다.
3. **용어집**: glossary.html에 각 작업이 제안한 후보와 본문 핵심 용어를 정의한다(30~45개). 정의는 근거 범위 안에서 짧게 쓴다. 새 의학적 정의는 추정하지 않는다.
4. **실험실**: lab.html에 장·실습의 도구를 모두 등록한다. 각 도구에 한 줄 설명과 바로 가기를 단다.
5. **일관성 점검** (책 전체를 실제로 읽고 고친다):
   - 응급 신호가 모두 emergency-data.js 공통 컴포넌트를 쓰는지 확인한다. 복사된 문구가 남아 있으면 교체한다.
   - 같은 사실의 숫자·날짜·금액이 장마다 같은지 확인한다(부모급여·아동수당·첫만남, 검진 14~35일, 로타 14주 6일, 출생신고 1개월, 체온 기준 등). 불일치 목록과 수정 결과를 남긴다.
   - 봄이 가족 타임라인(일령·장면)이 장끼리 모순되지 않는지 확인한다.
   - 이론↔실습 상호 링크가 양쪽으로 다 걸려 있는지 확인한다.
   - DESIGN-baby 8절 위반이 없는지 확인한다: 약 이름·용량, 브랜드, "집에서 지켜봐도 됨" 판정, 분유량 계산기, 자체 대변 색표, EPDS 점수 계산기, 100일 이유식·통잠 목표.
   - 내부 용어·사실 ID가 본문에 노출되지 않았는지 확인한다.
6. **서가·진행**: shelf/index.html과 shelf/progress/index.html에 BabyBook 상태를 갱신한다. docs/PROJECT_STATE.md도 갱신한다.
7. **게이트**:
   - `python3 scripts/check_site.py --site site-baby` 오류 0.
   - style_lint로 전 쪽을 검사한다.
   - 단위 테스트 전체가 통과한다.
   - 기존 세 책의 check_site 오류도 0이어야 한다(회귀 없음).
   - 브라우저로 전 쪽을 1280/375/360px, 라이트/다크에서 확인한다(넘침·콘솔 오류·키보드). 인쇄물 4종은 A4 1쪽으로 확인한다.
   - 대표 스크린샷은 docs/results/phase-N6/에 둔다.
8. docs/results/phase-N6.md를 쓰고 `python3 scripts/notify.py "🧩 [육아 편 통합 완료] ..."`로 보고한다.
