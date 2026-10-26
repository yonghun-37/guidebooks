# B4b 공통 파일 통합 요청

2026-10-26. 아래는 검수 후 통합 담당자가 적용할 제안이다. 작업자는 공통 파일을 수정하지 않았다. 다른 장 작업자의 요청과 합쳐 적용한다.

## 장 경로·상태

기존 slug와 실제 파일명이 일치한다. 상태를 `완성`으로 바꿔야 표지·목차·이전/다음 링크가 준비중 페이지 대신 본문을 가리킨다. 코드 머리의 상태 규약을 따른다.

```diff
--- a/site-blog/assets/book.js
+++ b/site-blog/assets/book.js
@@ -62,7 +62,7 @@
     "사실 확인과 내 경험을 더한 초안",
     "내 속도로",
     "입문",
-    "준비중"
+    "완성"
   ],
   [
     7,
@@ -72,7 +72,7 @@
     "권리와 사용 범위를 확인한 이미지",
     "내 속도로",
     "입문",
-    "준비중"
+    "완성"
   ],
   [
     8,
@@ -82,7 +82,7 @@
     "검색 의도와 글 구조 점검",
     "내 속도로",
     "입문",
-    "준비중"
+    "완성"
   ],
   [
     9,
@@ -92,7 +92,7 @@
     "신청 가능 여부와 다음 확인일",
     "내 속도로",
     "입문",
-    "준비중"
+    "완성"
   ],
   [
     10,
```

## 실험실 도구 등록

원본 장 전용 도구는 현재 직접 링크 또는 `?embed=<id>`로 작동한다. 다음 항목을 카탈로그에 병합하면 기존 실험실에서 원본을 재사용한다. 7장의 제목 배치 연습은 선택 등록이다. book.css·common.js·practice.js 수정은 필요 없다.

```diff
--- a/site-blog/assets/catalog.js
+++ b/site-blog/assets/catalog.js
@@ -5,5 +5,33 @@
     "id": "revenue-tool",
     "title": "방문과 구매로 수입 계산하기",
     "section": "simulator"
+  },
+  {
+    "chapter": 6,
+    "slug": "06-writing",
+    "id": "draft-tool",
+    "title": "AI 초안과 사람 손질 비교",
+    "section": "simulator"
+  },
+  {
+    "chapter": 7,
+    "slug": "07-images",
+    "id": "thumbnail-tool",
+    "title": "썸네일 제목 배치 연습",
+    "section": "simulator"
+  },
+  {
+    "chapter": 8,
+    "slug": "08-seo",
+    "id": "search-tool",
+    "title": "검색 결과 제목·설명 미리보기",
+    "section": "simulator"
+  },
+  {
+    "chapter": 9,
+    "slug": "09-monetize",
+    "id": "publish-tool",
+    "title": "발행 전 확인 분기",
+    "section": "simulator"
   }
 ]);
```

## 본문·출처·부록 연결

- 6장 프롬프트는 각 레시피에 2개와 공통 교정 요청이 있다. prompts 통합 시 원본은 `chapters/06-writing.html#info|review|trip|human`으로 연결한다.
- 모델·비용 부록: 6장은 ChatGPT Free 기본, Gemini·Claude 대안. 7장은 Canva·미리캔버스 무료 요소, Pro 월 14,900원(B052) 선택. 기본 글 완주에 새 결제는 필요 없다.
- credits: 각 장 말미의 B번호·공식 URL 목록을 통합한다. 7장 이미지 2장은 내장 이미지 생성 기능으로 생성했다. 실제 프롬프트는 7장에 전문을, 파일·크기·제작 방식은 B4b 결과에 남겼다.
- 연결 실습 4·5·8·9는 현재 준비중 URL이다. B5 통합 후 실제 파일 `practice/04-draft.html`, `05-images.html`, `08-search.html`, `09-monetize.html`과 함께 직접 링크로 교체한다. 7장 실제 발행 링크는 현재 본문으로 연결된다.
- 새 용어는 `phase-B4b-glossary.md`에 있다. 아직 용어집 앵커가 없으므로 본문에서 설명하고 깨진 용어 링크를 만들지 않았다.
- PROJECT_STATE·서가 진행 상태는 B4a/b/c 통합 담당자가 함께 갱신한다. B4b만 끝났다고 전체 이론·B5를 완료로 표시하지 않는다.
