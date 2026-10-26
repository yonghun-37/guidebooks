# Phase 5a 공통 파일 통합 요청

2026-10-26. 사용자 지정 충돌 방지 범위에 따라 아래 변경은 **적용하지 않았다**. 장 HTML과 전용 JS는 작성했고 직접 URL에서 검증한다. 검수자가 다른 작업자의 변경과 병합한 뒤 적용한다.

## 장 메타데이터

`site/assets/book.js`의 기존 네 행을 아래처럼 바꾼다. slug·제목·결과물은 원래 데이터를 유지한다. 시간은 장별 작업실 단계의 합이며 통계가 아닌 실습 배분이다.

```diff
--- a/site/assets/book.js
+++ b/site/assets/book.js
@@
-    [2, '02-formats', '1부 · 이해하기', '인스타그램은 무엇을 보여 주는가: 알고리즘과 포맷', '포맷 선택 메모'],
-    [3, '03-revenue', '1부 · 이해하기', '돈은 어디서 들어오는가: 수익 구조 6가지', '내 계정에 맞는 수익 경로 2개'],
-    [4, '04-niche', '1부 · 이해하기', '니치와 계정 기획', '계정 기획 시트'],
-    [5, '05-sources', '2부 · 만들기', '소재 찾기: 뉴스 소싱과 저작권', 'RSS 소스 목록과 인용 규칙'],
+    [2, '02-formats', '1부 · 이해하기', '인스타그램은 무엇을 보여 주는가: 알고리즘과 포맷', '포맷 선택 메모', '30분 · 실습용 배분', '입문', '완성'],
+    [3, '03-revenue', '1부 · 이해하기', '돈은 어디서 들어오는가: 수익 구조 6가지', '내 계정에 맞는 수익 경로 2개', '35분 · 실습용 배분', '입문', '완성'],
+    [4, '04-niche', '1부 · 이해하기', '니치와 계정 기획', '계정 기획 시트', '40분 · 실습용 배분', '입문', '완성'],
+    [5, '05-sources', '2부 · 만들기', '소재 찾기: 뉴스 소싱과 저작권', 'RSS 소스 목록과 인용 규칙', '45분 · 실습용 배분', '입문', '완성'],
```

미적용 상태에서는 공통 목차·사이드바·브라우저 제목이 여전히 ‘준비 중’이고 목차 링크는 coming-soon으로 간다. 장 상단의 결과물·시간·난이도·선행 장, 하단 2→3→4→5 이동은 장 HTML에 정적으로 두어 직접 검토할 수 있다. `data-chapter-meta`·`data-chapter-pager` 자동 생성 훅은 이 두 영역에서 사용하지 않았다. 메타데이터 통합 후 이 정적 영역을 기존 공통 훅으로 되돌리는 것은 선택 사항이며, 위 diff만으로도 공통 목차 공개가 가능하다.

5장 다음 링크는 현재 공통 상태를 따라 `coming-soon.html?chapter=06-writing`이다. 6장 원고 검수·등록 시 해당 장의 작성자와 함께 다음 링크를 `06-writing.html`로 통합한다.

## 공통 CSS·JS와 용어집

- `common.js` 개선은 필요하지 않았다. 표·번호 입력·그림 강조는 각 장의 짧은 `<style>`에 넣었다.
- 공통 `term-tip`의 숨겨진 말풍선이 375px에서 10px 넘치는 문제를 확인했다. 담당 장 안의 모바일 CSS로만 우선 보정했다. 아래 공통 CSS diff를 적용하면 다른 장에서도 같은 문제를 예방할 수 있다. 적용 후 담당 장의 동일한 `.chapter .term-tip` 규칙은 제거해도 된다.

```diff
--- a/site/assets/book.css
+++ b/site/assets/book.css
@@
 @media (max-width: 680px) {
+  .term-tip { position: fixed; left: 22px; right: 22px; bottom: 24px; width: auto; }
   body { font-size: 16px; line-height: 1.85; }
```
- 새 용어와 앵커 후보는 [phase-5a-glossary.md](phase-5a-glossary.md)에 있다. glossary.html 담당자가 통합한다. 현재 새 용어는 용어집 기본 URL로 연결하며 기존 `carousel`·`api` 앵커는 유지한다.
- 15장 실험실에 연결할 전용 도구: `02-formats.html#simulator`, `03-revenue.html#simulator`, `04-niche.html#simulator`, `05-sources.html#simulator`. 각 장의 만져 보는 그림은 `#figure`다. 원고마다 시뮬레이터 2개(개념 그림+입력 도구)가 있다.

## 프로젝트 현황에 병합할 문장

`docs/PROJECT_STATE.md`는 병행 작업자가 공유하므로 직접 수정하지 않았다. 기존 ‘현재 산출물’ 절에 아래 항목을 병합하는 제안이다. 다른 Phase 상태는 해당 담당자의 검증 기록에 따라 유지한다.

```diff
--- a/docs/PROJECT_STATE.md
+++ b/docs/PROJECT_STATE.md
@@
 ## 현재 산출물
+
+- Phase 5a의 2~5장 원고·전용 JS 작성 및 Chromium 1280px/375px 검증 완료. [결과](results/phase-5a.md), [공통 등록 요청](results/phase-5a-requests.md), [용어 인계](results/phase-5a-glossary.md). 공통 book.js의 완성 상태 등록·용어집·실험실 통합과 Claude Code 검수/커밋은 남아 있다. 실제 운영용 RSS 약관·한국 수익화의 기존 조사 공백은 확정하지 않았다.
```

별도 명세·ADR 디렉터리는 만들지 않았다. 이 저장소의 기존 Phase 결과 기록을 요구사항·구현·검증·미완료 상태의 인계 문서로 재사용한다.
