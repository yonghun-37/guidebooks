너는 ai-insta 프로젝트의 작업자(Codex)다. AGENTS.md, .agents/skills/guidebook-writing·guidebook-pipeline, docs/STYLE-GUIDE.md(6·7절 포함), docs/DESIGN-blog.md, **docs/results/phase-B7-findings.md·phase-B7-scorecard.md(이번 작업의 입력)**, research-blog/를 읽어라.
이번 작업은 **Phase B8. BlogBook 독립 검토 수정 + 최종 게이트** 다. 담당: site-blog/, blog-kit/, research-blog/(근거 추가 시). 다른 책 폴더·auto-kit은 다른 작업자가 수정 중 — 건드리지 마라. commit하지 마라.

1. B7의 11건(차단 0·혼란 8·사소 3)을 모두 고친다. 발견마다 제안을 검토해 더 나은 방법이 있으면 이유를 적고 적용한다. 특히:
   - B7-01: **실제 공공 자료 하나**(공공누리 제1유형 등 이용 조건을 공식 안내로 확인한 정책브리핑·지자체·정부 공고)를 골라 근거 [B###]를 추가하고, 짧은 메모 → 채운 요청문 → 자료표 → 수정 표시 → 출처가 있는 완성 글까지 한 바퀴를 보여 준다. 기준일을 명시하고, 신청이 끝난 자료라면 학습용임을 밝힌다. 금액·조건은 원문 그대로만.
   - B7-02: 정보/후기/여행 세 경로마다 고정 제목·메모·사진 파일명을 정하고 이론·실습·키트 샘플 끝까지 같은 것을 쓴다(후기 제품 하나로 통일).
   - B7-03: 화면 위치 그림은 실제 공간 배치(도구 영역·캔버스·제목칸·사진/링크 도구·발행 버튼)를 직접 그린 단순 화면 틀 + 번호로 다시 그린다(로고·UI 복제 금지).
2. 게이트: style_lint, check_site(--site site-blog), 1280/375/360px × 라이트/다크·콘솔 오류·키보드, blog-kit pytest(Python 3.11, 원본·ZIP).
3. 결과 docs/results/phase-B8.md(발견별 처리 표: 고침/다르게 고침/보류와 이유), docs/PROJECT_STATE.md 갱신, `python3 scripts/notify.py "✅ [B8 블로그 수정·게이트 완료] ..."`.
