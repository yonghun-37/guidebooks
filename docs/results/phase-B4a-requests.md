# B4a 공용 파일 통합 요청

네 장과 장 전용 자산은 작성했으며 공용 파일은 수정하지 않았다. 아래 diff는 통합 담당자가 B4b·B4c 요청과 합쳐 적용한다.

## 장 상태와 목차 연결

현재 공용 목차·이전/다음 버튼은 이 네 장을 여전히 준비중으로 보낸다. 다음 상태 변경을 적용하면 원본 본문으로 연결된다. 기존 slug를 그대로 사용했다.

```diff
--- a/site-blog/assets/book.js
+++ b/site-blog/assets/book.js
@@ -12,7 +12,7 @@
     "내 글의 독자와 첫 발행 경로",
     "내 속도로",
     "입문",
-    "준비중"
+    "완성"
   ],
   [
     2,
@@ -32,7 +32,7 @@
     "글·이미지·키워드 작업별 도구 메모",
     "내 속도로",
     "입문",
-    "준비중"
+    "완성"
   ],
   [
     4,
@@ -42,7 +42,7 @@
     "목표에 맞는 블로그 플랫폼",
     "내 속도로",
     "입문",
-    "준비중"
+    "완성"
   ],
   [
     5,
@@ -52,7 +52,7 @@
     "키워드와 고른 이유",
     "내 속도로",
     "입문",
-    "준비중"
+    "완성"
   ],
   [
     6,
```

## 도구 카탈로그

원본 장에서 직접 실행되며 `?embed=<id>`로 기존 실험실 외곽에 넣을 수 있다. 입력·선택은 현재 화면에서만 유지한다. 1장 지도는 첫 빈 단계로, 4장 분기는 조건 충돌일 때 재선택으로, 5장 연습은 선택 근거로 안내한다.

```diff
--- a/site-blog/assets/catalog.js
+++ b/site-blog/assets/catalog.js
@@ -1,9 +1,37 @@
 window.BlogCatalog = Object.freeze([
+  {
+    "chapter": 1,
+    "slug": "01-map",
+    "id": "first-post-tool",
+    "title": "첫 글까지 단계 지도",
+    "section": "simulator"
+  },
   {
     "chapter": 2,
     "slug": "02-revenue",
     "id": "revenue-tool",
     "title": "방문과 구매로 수입 계산하기",
     "section": "simulator"
+  },
+  {
+    "chapter": 3,
+    "slug": "03-ai-tools",
+    "id": "tool-picker",
+    "title": "다음에 열 도구",
+    "section": "simulator"
+  },
+  {
+    "chapter": 4,
+    "slug": "04-platforms",
+    "id": "platform-tool",
+    "title": "플랫폼 고르기 분기",
+    "section": "simulator"
+  },
+  {
+    "chapter": 5,
+    "slug": "05-keywords",
+    "id": "keyword-tool",
+    "title": "키워드 고르기 연습",
+    "section": "simulator"
   }
 ]);
```

## 용어집·출처·상태 반영

- 새 용어 후보와 정의·장 위치는 `phase-B4a-glossary.md`를 병합한다. 새 용어가 아직 공용 용어집에 없으므로 깨진 용어 링크는 넣지 않았다.
- 각 장 끝에 실제 인용한 B번호의 공식 원문 링크를 달았다. credits에는 이 네 장의 출처도 통합한다. 원문 전문·조사 외부 원응답은 저장하지 않는다.
- PROJECT_STATE·서가 진행 상태·공용 장 상태는 통합 작업자가 갱신한다. B4a 결과와 검사 기록은 `phase-B4a.md` 및 `phase-B4a/`에 있다.
- book.css·common.js·practice.js 변경 요청은 없다. 표의 모바일 가로 이동과 선택 도구 배치는 각 장 CSS에만 있다.
