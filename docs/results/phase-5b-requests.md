# Phase 5b 공통 파일 통합 요청

이 문서는 적용하지 않은 diff 제안이다. 사용자 지시의 병행 작업 경계에 따라 `book.js`, `book.css`, `common.js`, `glossary.html`, `credits.html`, `index.html`, `PROJECT_STATE.md`는 수정하지 않았다. 담당 HTML은 공통 데이터와 같은 제목·slug·결과물을 쓰며, 공통 메타의 `추후 안내` 덮어쓰기를 피하려고 상단 메타를 직접 작성했다. 6~8장 사이 하단 이동은 실제 HTML을 연결한다.

## 1. 장 공개 상태·시간·난이도

6장 slug는 제안명 `06-ai-writing` 대신 현재 데이터의 `06-writing`을 사용했다. 검수자는 결과 기록과 브라우저 증거를 확인한 뒤 아래 변경을 적용한다.

```diff
--- a/site/assets/book.js
+++ b/site/assets/book.js
@@
-    [6, '06-writing', '2부 · 만들기', 'AI로 글쓰기: 카드 문안과 릴스 대본', '프롬프트 템플릿 3종'],
-    [7, '07-cards', '2부 · 만들기', '뉴스카드 디자인 자동화', '첫 뉴스카드 캐러셀 PNG'],
-    [8, '08-reels', '2부 · 만들기', '릴스 자동 생성: 대본에서 영상까지', '첫 릴스 MP4'],
-    [9, '09-pipeline', '3부 · 자동화', '파이프라인 잇기', '한 번 실행으로 카드와 릴스 생성'],
+    [6, '06-writing', '2부 · 만들기', 'AI로 글쓰기: 카드 문안과 릴스 대본', '프롬프트 템플릿 3종', '55분 · 설치 제외, 실습용 배분', '입문 · 파일 편집', '완성'],
+    [7, '07-cards', '2부 · 만들기', '뉴스카드 디자인 자동화', '첫 뉴스카드 캐러셀 PNG', '50분 · 설치 제외, 실습용 배분', '입문 · 문안과 색 편집', '완성'],
+    [8, '08-reels', '2부 · 만들기', '릴스 자동 생성: 대본에서 영상까지', '첫 릴스 MP4', '60분 · 설치 제외, 실습용 배분', '입문 · 영상 검수', '완성'],
+    [9, '09-pipeline', '3부 · 자동화', '파이프라인 잇기', '한 번 실행으로 카드와 릴스 생성', '60분 · 설치 제외, 실습용 배분', '입문 · 생성과 승인', '완성'],
```

적용 전 공통 목차·사이드바와 브라우저 제목은 계속 ‘준비 중’으로 표시된다. 본문은 직접 URL로 열어 검증했다. 적용 뒤에는 담당 네 HTML의 `<dl class="chapter-meta">`를 `<dl class="chapter-meta" data-chapter-meta>`로 바꿔 공통 메타 생성으로 복귀할 수 있다. 공통 데이터 적용 전에 그 속성만 먼저 넣으면 시간·난이도가 ‘추후 안내’로 바뀐다.

## 2. 모바일 용어 설명의 가로 넘침

375px 검사에서 공통 `.term-tip`의 `left: 0` 때문에 숨겨진 설명 상자도 문서 폭을 늘리는 문제를 확인했다. 담당 네 HTML의 최소 로컬 스타일로 해결했고 공통 CSS는 그대로 두었다. 통합 시 아래를 공통 모바일 구간에 넣고 담당 HTML의 동일한 `@media`를 제거할 수 있다.

```diff
--- a/site/assets/book.css
+++ b/site/assets/book.css
@@
 @media (max-width: 680px) {
+  .chapter .term-tip {
+    position: fixed;
+    left: 22px;
+    bottom: 24px;
+    width: calc(100vw - 44px);
+    max-width: 320px;
+  }
   body { font-size: 16px; line-height: 1.85; }
```

이 제안은 작은 화면에서 설명을 화면 아래쪽에 놓는다. 데스크톱 위치는 유지한다. 다른 장까지 적용할 때 해당 장의 용어 조작·375px 화면도 다시 확인한다. 공통 JS 개선은 필요하지 않았다.

## 3. 용어·실험실·출처 통합

- 새 용어는 [용어 표](phase-5b-glossary.md)를 사용한다. 새 용어 링크는 없는 앵커를 미리 만들지 않고 `../glossary.html`로 연결했다. 항목 추가 후 표의 제안 앵커를 반영한다.
- 실험실 담당자는 장별 핵심 모형 링크 `chapters/06-writing.html#simulator`, `chapters/07-cards.html#simulator`, `chapters/08-reels.html#simulator`, `chapters/09-pipeline.html#simulator`를 사용할 수 있다. 입력·공개 가정·경고를 함께 읽는 링크다.
- 출처·크레딧에는 research/SOURCES의 기존 번호를 그대로 사용한다. 새로운 사실 ID나 출처를 추가하지 않았다. 네 장의 각주는 원문 URL을 직접 연결한다.
- 병행 작업으로 5장·10장 HTML 초안이 생긴 것을 확인하고 6장의 선행 링크와 9장의 다음 링크를 실제 `05-sources.html`·`10-publishing.html`에 연결했다. 공통 목차의 상태 변경은 각 담당자 결과를 검수한 뒤 적용한다.

## 4. 프로젝트 현황 통합 제안

공유 현황은 동시 덮어쓰기를 피하고 아래 한 줄을 현재 산출물 섹션에 합치는 것으로 제안한다. 기존 다른 단계 현황을 지우지 않는다.

```diff
--- a/docs/PROJECT_STATE.md
+++ b/docs/PROJECT_STATE.md
@@
 ## 현재 산출물
+
+- **Phase 5b 6~9장 원고·모형·검증 완료, 통합 검수 대기:** [결과](results/phase-5b.md). 장별 9블록·퀴즈 4문항·모형 2개(총 8개), 키트 문안/카드/릴스/승인 실습을 실행하고 1280px·375px를 검사했다. 공통 장 상태·모바일 용어 설명·용어집 병합은 [요청](results/phase-5b-requests.md)을 따른다. 실제 API·TTS 서비스·계정 게시와 Windows/macOS 실기동은 검증하지 않았다.
```
