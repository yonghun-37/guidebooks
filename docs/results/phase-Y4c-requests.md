# Y4c 공통 파일 반영 요청

공통 파일은 수정하지 않았다. 아래는 현재 파일에 대한 **미적용 제안 diff**다. 통합 시 다른 묶음의 완성 장 목록과 합쳐야 한다.

## 공통 목차와 상태

현재 `chapterUrl`은 샘플만 실제 원고로 연결한다. 10~14장 원고가 있어도 전체 목차·책의 지도는 준비중 화면으로 이동한다. 완성 상태를 지원하고 실제 원고로 연결하는 안이다.

```diff
--- a/site-shorts/assets/book.js
+++ b/site-shorts/assets/book.js
@@ -166,7 +166,7 @@
   ]
 ];
   const chapters = chapterRows.map(([number, slug, part, title, deliverable, duration = '추후 안내', difficulty = '추후 안내', status = '준비중']) =>
-    Object.freeze({ number, slug, part, title, deliverable, duration, difficulty, status, sample: number === 2, track: 'theory' }));
+    Object.freeze({ number, slug, part, title, deliverable, duration, difficulty, status: [10, 11, 12, 13, 14].includes(number) ? '완성' : status, sample: number === 2, track: 'theory' }));
   const practiceRows = [
   [
     "00-start",
@@ -247,12 +247,12 @@
   const url = path => prefix + path;
   const chapterUrl = chapter => {
     const folder = chapter.track === 'practice' ? 'practice' : 'chapters';
-    if (chapter.sample || chapter.slug === '00-start') return url(`${folder}/${chapter.slug}.html`);
+    if (chapter.sample || chapter.status === '완성' || chapter.slug === '00-start') return url(`${folder}/${chapter.slug}.html`);
     return url(`${folder}/coming-soon.html?chapter=${chapter.slug}`);
   };
   const byNumber = number => chapters.find(chapter => chapter.number === number);
   const esc = text => String(text).replace(/[&<>"']/g, char => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[char]));
-  const status = chapter => `<span class="status ${chapter.sample ? 'ready' : ''}">${chapter.sample ? '확인용 샘플' : '준비중'}</span>`;
+  const status = chapter => `<span class="status ${chapter.sample || chapter.status === '완성' ? 'ready' : ''}">${chapter.sample ? '확인용 샘플' : chapter.status}</span>`;
   const label = chapter => `(${chapter.track === 'practice' ? '실습' : '이론'}) ${chapter.number != null ? chapter.number + (chapter.track === 'practice' ? '. ' : '장 · ') : ''}${chapter.title}`;
   const link = chapter => `<a href="${chapterUrl(chapter)}">${esc(label(chapter))} ${status(chapter)}</a>`;
   const selected = (document.body.dataset.chapter === 'pending' || document.body.dataset.practice === 'pending') ? new URLSearchParams(location.search).get('chapter') : document.body.dataset.chapter;
@@ -279,7 +279,7 @@
   });
   document.querySelectorAll('[data-chapter-link]').forEach(anchor => {
     const chapter = byNumber(Number(anchor.dataset.chapterLink));
-    if (chapter) { anchor.href = chapterUrl(chapter); if (!chapter.sample) anchor.append(' · 준비 중'); }
+    if (chapter) { anchor.href = chapterUrl(chapter); if (!chapter.sample && chapter.status !== '완성') anchor.append(' · 준비 중'); }
   });
   if (current) {
     document.querySelectorAll('[data-chapter-title]').forEach(node => { node.textContent = label(current); });
@@ -309,7 +309,7 @@
     });
     document.title = `${label(current)} | ShortsBook`;
     document.querySelectorAll('.sidebar-chapters a').forEach(anchor => { if (new URL(anchor.href).pathname + new URL(anchor.href).search === location.pathname + location.search) anchor.setAttribute('aria-current', 'page'); });
-    if (!current.sample) document.title = `${current.title} · 준비 중 | ShortsBook`;
+    if (!current.sample && current.status !== '완성') document.title = `${current.title} · 준비 중 | ShortsBook`;
   }
   document.querySelectorAll('[data-site-footer]').forEach(footer => {
     footer.className = 'site-footer';
```

10~14장 본문의 이전·다음 링크는 이미 실제 파일로 연결했다. 전용 `operations.js`는 이 묶음의 문서 제목만 실제 h1로 표시한다. 위 상태 반영 뒤 해당 제목 보정은 제거할 수 있다. 다른 장·준비중 화면·샘플에 대한 상태를 이번 작업에서 바꾸지 않았다.

## 용어집·출처·실험실

- 용어는 [용어 제안](phase-Y4c-glossary.md)을 기존 항목과 합쳐 반영한다.
- 각 장 하단에 사용한 Y출처 원문 링크를 넣었다. `credits.html` 추가 조사는 필요하지 않다.
- 도구 모음 연결이 필요하면 `10-templates.html#pipeline-tool`, `11-upload.html#metadata-tool`, `12-analytics.html#retention-tool`, `13-policy.html#policy-tool`, `14-plan.html#plan-tool`을 사용한다. 자산은 `assets/operations.css`, `assets/operations.js`이며 11장은 기존 `assets/shorts.js`도 필요하다.
- `docs/PROJECT_STATE.md`·서가 진행표 갱신은 통합 담당자에게 맡긴다. 이 묶음의 집필 완료와 공통 목차 미반영을 구분해 적어야 한다.
