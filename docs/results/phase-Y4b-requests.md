# Y4b 통합 요청

공용 파일과 조사 파일은 수정하지 않았다. 아래는 통합 담당자가 다른 작업 묶음의 결과와 함께 검토·적용할 제안 diff다. `book.css`, `sim/common.js`, `practice.js`, `shorts.css`, `shorts.js` 변경은 필요 없다. 네 장은 `y4b.css`·`y4b.js`를 직접 불러온다.

## 1. 목차 연결과 준비중 표시

현재 데이터 구조는 완성 상태를 URL에 사용하지 않으므로 상태·경로·배지·제목을 함께 바꾸는 최소안이다. 예상 시간은 새 숫자를 만들지 않고 기존 ‘추후 안내’를 유지한다. `index.html`은 공용 데이터로 목차를 생성하므로 별도 변경이 필요 없다. 다른 묶음의 상태 변경과 합칠 때 아래 행을 중복 적용하지 않는다.

```diff
--- a/site-shorts/assets/book.js
+++ b/site-shorts/assets/book.js
@@ -59,40 +59,40 @@
     "06-scenes",
     "이론편",
     "그림: 촬영·소재·AI 영상 생성",
-    "내 영상 제작 메모",
-    "추후 안내",
-    "입문",
-    "준비중"
+    "촬영 장면과 소재 권리 메모",
+    "추후 안내",
+    "입문",
+    "완성"
   ],
   [
     7,
     "07-editing",
     "이론편",
     "편집: 컷·리듬·전환",
-    "내 영상 제작 메모",
-    "추후 안내",
-    "입문",
-    "준비중"
+    "컷·자막·소리 시간표",
+    "추후 안내",
+    "입문",
+    "완성"
   ],
   [
     8,
     "08-captions",
     "이론편",
     "자막과 화면 글자",
-    "내 영상 제작 메모",
-    "추후 안내",
-    "입문",
-    "준비중"
+    "읽기·가림·시간을 확인한 자막",
+    "추후 안내",
+    "입문",
+    "완성"
   ],
   [
     9,
     "09-export",
     "이론편",
     "출력과 화질",
-    "내 영상 제작 메모",
-    "추후 안내",
-    "입문",
-    "준비중"
+    "원본과 비교한 출력 설정 메모",
+    "추후 안내",
+    "입문",
+    "완성"
   ],
   [
     10,
@@ -247,12 +247,12 @@
   const url = path => prefix + path;
   const chapterUrl = chapter => {
     const folder = chapter.track === 'practice' ? 'practice' : 'chapters';
-    if (chapter.sample || chapter.slug === '00-start') return url(`${folder}/${chapter.slug}.html`);
+    if (chapter.status === '완성' || chapter.sample || chapter.slug === '00-start') return url(`${folder}/${chapter.slug}.html`);
     return url(`${folder}/coming-soon.html?chapter=${chapter.slug}`);
   };
   const byNumber = number => chapters.find(chapter => chapter.number === number);
   const esc = text => String(text).replace(/[&<>"']/g, char => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[char]));
-  const status = chapter => `<span class="status ${chapter.sample ? 'ready' : ''}">${chapter.sample ? '확인용 샘플' : '준비중'}</span>`;
+  const status = chapter => `<span class="status ${chapter.status === '완성' || chapter.sample ? 'ready' : ''}">${chapter.status === '완성' ? '완성' : chapter.sample ? '확인용 샘플' : '준비중'}</span>`;
   const label = chapter => `(${chapter.track === 'practice' ? '실습' : '이론'}) ${chapter.number != null ? chapter.number + (chapter.track === 'practice' ? '. ' : '장 · ') : ''}${chapter.title}`;
   const link = chapter => `<a href="${chapterUrl(chapter)}">${esc(label(chapter))} ${status(chapter)}</a>`;
   const selected = (document.body.dataset.chapter === 'pending' || document.body.dataset.practice === 'pending') ? new URLSearchParams(location.search).get('chapter') : document.body.dataset.chapter;
@@ -279,7 +279,7 @@
   });
   document.querySelectorAll('[data-chapter-link]').forEach(anchor => {
     const chapter = byNumber(Number(anchor.dataset.chapterLink));
-    if (chapter) { anchor.href = chapterUrl(chapter); if (!chapter.sample) anchor.append(' · 준비 중'); }
+    if (chapter) { anchor.href = chapterUrl(chapter); if (chapter.status !== '완성' && !chapter.sample) anchor.append(' · 준비 중'); }
   });
   if (current) {
     document.querySelectorAll('[data-chapter-title]').forEach(node => { node.textContent = label(current); });
@@ -309,7 +309,7 @@
     });
     document.title = `${label(current)} | ShortsBook`;
     document.querySelectorAll('.sidebar-chapters a').forEach(anchor => { if (new URL(anchor.href).pathname + new URL(anchor.href).search === location.pathname + location.search) anchor.setAttribute('aria-current', 'page'); });
-    if (!current.sample) document.title = `${current.title} · 준비 중 | ShortsBook`;
+    if (current.status !== '완성' && !current.sample) document.title = `${current.title} · 준비 중 | ShortsBook`;
   }
   document.querySelectorAll('[data-site-footer]').forEach(footer => {
     footer.className = 'site-footer';
```

## 2. 사실표 보충

기존 SOURCES와 조사 노트에 있는 근거의 세부를 사실표 행으로 옮기는 요청이다. 새 웹 조사 결과인 것처럼 표시하지 않는다. 새 ID는 통합 시 다른 요청과 충돌하지 않게 정한다. 아래 ID는 임시 제안이다.

```diff
--- a/research-shorts/FACT-SHEET.md
+++ b/research-shorts/FACT-SHEET.md
@@
 | YT-089 | 한국을 포함한 YPP 수익 창출자는 AdSense의 미국 세금 정보를 제출·점검해야 한다. 미국 원천징수와 한국 소득 신고를 같은 절차로 취급하지 않는다. | [Y091](SOURCES.md#y091) [Y057](SOURCES.md#y057) | 이론10·13·14, 실습0·1·7·10 | 직접 본문 확인 | [16-tax-workflow](16-tax-workflow.md) |
+| YT-090 | 권장 인코딩 도움말은 MP4/H.264·녹화 fps 유지·SDR 1080p 표준/높은 프레임 속도의 영상 비트레이트 8/12Mbps를 안내한다. 머리의 콘텐츠 관리자 전용 문구와 적용 범위를 함께 확인한다. | [Y003](SOURCES.md#y003) | 이론9, 실습7 | 기존 SOURCES의 직접 확인 기록; 본문은 연습 선택으로 사용 | [01-specs-feed](01-specs-feed.md) |
+| YT-091 | Clipchamp 자막 도움말은 언어 선택·생성·교정·SRT 다운로드를 안내한다. 화면에 구운 자막과 선택 자막 파일은 구분한다. | [Y066](SOURCES.md#y066) | 이론8, 실습6 | 기존 SOURCES와 음성·자막 노트의 직접 확인 기록 | [08-voice-captions](08-voice-captions.md) |
```

9장은 공식 8/12Mbps 권장표를 정책값으로 제시하지 않는다. 8Mbps×12초÷8=12MB는 가상 계산이다. 1080×1920·30/60fps도 제작 선택·정의의 계산으로 명시했다. 공식 권장 설정을 본문 표로 확장하려면 위 사실표 보충과 원문의 적용 범위를 통합자가 먼저 대조한다.

## 3. 통합 기록·실험실·용어집

- `docs/PROJECT_STATE.md`·서가 진행표: ‘Y4b 집필·담당 검증 완료, 공용 목차 통합 대기’로 반영한다. 전체 이론편 완료로 표시하지 않는다.
- 실험실 통합 시 후보: `chapters/06-scenes.html#framing-tool`, `07-editing.html#rhythm-tool`, `08-captions.html#caption-tool`, `09-export.html#quality-tool`. `?embed=<도구 ID>`로 기존 공용 임베드도 사용할 수 있다.
- 새 용어 정의는 [phase-Y4b-glossary.md](phase-Y4b-glossary.md)에 모았다. 자동 용어 링크는 등록 뒤 붙인다.
- [Y003]과 [Y066]은 기존 출처 목록에 있다. 신규 출처 번호·공용 credits 수정은 필요 없다.
