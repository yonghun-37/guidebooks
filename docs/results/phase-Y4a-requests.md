# Y4a 공통 파일 통합 요청

담당 네 HTML은 직접 열어 사용할 수 있다. 공통 파일은 수정하지 않았다. 아래 diff는 **통합 담당자가 검수 뒤 적용할 제안**이다. 다른 장 묶음의 상태 변경과 병합한다.

## 장 데이터·준비 상태

현재 `chapterUrl`은 sample만 실제 파일로 연결하고 상태·문서 제목도 sample 여부로 판단한다. 네 장의 본문·도구가 있어도 공통 목차에서는 준비중 페이지로 가고 탭 제목에 준비중이 붙는다. `status === '완성'`도 준비 완료로 취급하되 기존 2장·실습8 샘플 표시는 보존한다. 장 안의 이전·다음 링크는 명시적 상대 링크로 이미 연결했다. 예측 소요시간을 추가하지 않는다.

```diff
--- a/site-shorts/assets/book.js
+++ b/site-shorts/assets/book.js
@@ -9,10 +9,10 @@
     "01-map",
     "이론편",
     "쇼츠 한 편이 만들어지기까지",
-    "내 영상 제작 메모",
-    "추후 안내",
-    "입문",
-    "준비중"
+    "내 영상 제작 메모와 다음에 할 일",
+    "추후 안내",
+    "입문",
+    "완성"
   ],
   [
     2,
@@ -29,30 +29,30 @@
     "03-hook",
     "이론편",
     "기획: 첫 3초와 한 편의 구조",
-    "내 영상 제작 메모",
-    "추후 안내",
-    "입문",
-    "준비중"
+    "좁힌 주제와 첫 문장 두 안, 시작·과정·결과 메모",
+    "추후 안내",
+    "입문",
+    "완성"
   ],
   [
     4,
     "04-script",
     "이론편",
     "대본 쓰기와 AI 활용",
-    "내 영상 제작 메모",
-    "추후 안내",
-    "입문",
-    "준비중"
+    "읽기 시간을 확인한 대본과 말·장면·자막 메모",
+    "추후 안내",
+    "입문",
+    "완성"
   ],
   [
     5,
     "05-audio",
     "이론편",
     "소리: 내레이션·TTS·음악",
-    "내 영상 제작 메모",
-    "추후 안내",
-    "입문",
-    "준비중"
+    "시험 녹음 비교와 소리 균형·음악 이용 조건 메모",
+    "추후 안내",
+    "입문",
+    "완성"
   ],
   [
     6,
@@ -245,14 +245,15 @@
   const allChapters = [...chapters, ...practice];
   const prefix = new URL('.', location.href).href === root.href ? '' : '../';
   const url = path => prefix + path;
+  const isReady = chapter => chapter.status === '완성' || chapter.sample;
   const chapterUrl = chapter => {
     const folder = chapter.track === 'practice' ? 'practice' : 'chapters';
-    if (chapter.sample || chapter.slug === '00-start') return url(`${folder}/${chapter.slug}.html`);
+    if (isReady(chapter) || chapter.slug === '00-start') return url(`${folder}/${chapter.slug}.html`);
     return url(`${folder}/coming-soon.html?chapter=${chapter.slug}`);
   };
   const byNumber = number => chapters.find(chapter => chapter.number === number);
   const esc = text => String(text).replace(/[&<>"']/g, char => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[char]));
-  const status = chapter => `<span class="status ${chapter.sample ? 'ready' : ''}">${chapter.sample ? '확인용 샘플' : '준비중'}</span>`;
+  const status = chapter => `<span class="status ${isReady(chapter) ? 'ready' : ''}">${chapter.status === '완성' ? '완성' : chapter.sample ? '확인용 샘플' : '준비중'}</span>`;
   const label = chapter => `(${chapter.track === 'practice' ? '실습' : '이론'}) ${chapter.number != null ? chapter.number + (chapter.track === 'practice' ? '. ' : '장 · ') : ''}${chapter.title}`;
   const link = chapter => `<a href="${chapterUrl(chapter)}">${esc(label(chapter))} ${status(chapter)}</a>`;
   const selected = (document.body.dataset.chapter === 'pending' || document.body.dataset.practice === 'pending') ? new URLSearchParams(location.search).get('chapter') : document.body.dataset.chapter;
@@ -279,7 +280,7 @@
   });
   document.querySelectorAll('[data-chapter-link]').forEach(anchor => {
     const chapter = byNumber(Number(anchor.dataset.chapterLink));
-    if (chapter) { anchor.href = chapterUrl(chapter); if (!chapter.sample) anchor.append(' · 준비 중'); }
+    if (chapter) { anchor.href = chapterUrl(chapter); if (!isReady(chapter)) anchor.append(' · 준비 중'); }
   });
   if (current) {
     document.querySelectorAll('[data-chapter-title]').forEach(node => { node.textContent = label(current); });
@@ -309,7 +310,7 @@
     });
     document.title = `${label(current)} | ShortsBook`;
     document.querySelectorAll('.sidebar-chapters a').forEach(anchor => { if (new URL(anchor.href).pathname + new URL(anchor.href).search === location.pathname + location.search) anchor.setAttribute('aria-current', 'page'); });
-    if (!current.sample) document.title = `${current.title} · 준비 중 | ShortsBook`;
+    if (!isReady(current)) document.title = `${current.title} · 준비 중 | ShortsBook`;
   }
   document.querySelectorAll('[data-site-footer]').forEach(footer => {
     footer.className = 'site-footer';
```

## 다른 공통 파일

- `book.css`, `sim/common.js`, `practice.js`, `shorts.css`, `shorts.js`의 필수 변경은 없다. 장별 도구 CSS·JS는 각 장 안에 있어 독립 작동한다.
- 표지의 완료 상태·용어집·출처 목록 갱신은 통합 때 다른 장 묶음과 함께 처리한다. 새 용어 후보는 [용어 목록](phase-Y4a-glossary.md), 이 장에서 사용한 출처는 각 장의 출처 절에 모두 들어 있다.
- 공통 검사기는 01장을 9블록 검사에서 제외한다. 이번 브라우저 검증에서 01장도 별도로 9블록을 확인했다. 다른 책 1장의 규칙과 분리해 처리할 필요가 있으므로 검사기 수정은 이번 범위에 넣지 않았다.

## credits.html 출처 목록에 추가할 항목

본문의 출처는 이미 각 장 안에 있어 사용 가능하다. 통합 출처에는 아래 19개가 아직 없다. 기존 `<ul>`의 마지막 `</ul>` 바로 앞에 삽입한다. 아래는 긴 한 줄 HTML 전체를 반복하지 않는 **삽입 위치 기준 diff**다(자동 patch 적용용이 아님).

```diff
--- a/site-shorts/credits.html
+++ b/site-shorts/credits.html
@@ 기존 출처 목록의 닫는 </ul> 바로 앞 @@
+<li id="source-y011">[Y011] <a href="https://support.google.com/youtube/answer/1311392?hl=ko">YouTube 채널 수익 창출 정책</a> · YouTube/Google · 본문 변경 안내2025-07-15</li>
+<li id="source-y012">[Y012] <a href="https://support.google.com/youtube/answer/2801973?hl=ko">스팸 정책</a> · YouTube/Google · 날짜 미표기</li>
+<li id="source-y015">[Y015] <a href="https://support.google.com/youtube/answer/2797370?hl=ko">Content ID의 원리</a> · YouTube/Google · 날짜 미표기</li>
+<li id="source-y021">[Y021] <a href="https://clipchamp.com/ko/pricing/">Clipchamp 무료 및 프리미엄 구독 요금제 비교</a> · Microsoft · 날짜 미표기</li>
+<li id="source-y022">[Y022] <a href="https://support.google.com/youtube/answer/13952912?hl=ko">YouTube Create 제공 지역</a> · YouTube/Google · 날짜 미표기</li>
+<li id="source-y025">[Y025] <a href="https://typecast.ai/kr/pricing/">타입캐스트 플랜 안내</a> · Neosapience/Typecast · 날짜 미표기</li>
+<li id="source-y026">[Y026] <a href="https://help.elevenlabs.io/hc/en-us/articles/13313564601361-Can-I-publish-the-content-I-generate-on-the-platform">Can I publish the content I generate on the platform?</a> · ElevenLabs · 날짜 미표기</li>
+<li id="source-y027">[Y027] <a href="https://vrew.ai/ko/pricing">Vrew 요금 페이지</a> · VoyagerX · 날짜 미표기</li>
+<li id="source-y028">[Y028] <a href="https://blog.youtube/creator-and-artist-stories/youtube-shorts-deep-dive/">YouTube Shorts deep dive: Todd Sherman and Jenny Hoyos</a> · YouTube/Google · 2025-01-28</li>
+<li id="source-y047">[Y047] <a href="https://business.google.com/kr/think/future-of-marketing/meet-the-creators-one-minute-musical-beautyfool-secret-to-creating-shorts-loved-by-gen-z/">Meet the Creators: 1분 뮤지컬 & 사내뷰공업</a> · Think with Google · 2023-06</li>
+<li id="source-y052">[Y052] <a href="https://support.google.com/youtube/answer/13521392?hl=ko">YouTube Create 자세히 알아보기</a> · YouTube/Google · 날짜 미표기</li>
+<li id="source-y065">[Y065] <a href="https://support.microsoft.com/en-us/clipchamp/how-to-add-stock-videos-to-a-video">How to add stock videos to a video</a> · Microsoft · 날짜 미표기</li>
+<li id="source-y069">[Y069] <a href="https://support.google.com/youtube/answer/2814000?hl=ko">저작권 위반 경고 기본사항</a> · YouTube/Google · 날짜 미표기</li>
+<li id="source-y078">[Y078] <a href="https://clipchamp.com/en/blog/text-to-speech-update/">AI text to speech: all the features to know about</a> · Microsoft Clipchamp · 2026-02-02 갱신</li>
+<li id="source-y079">[Y079] <a href="https://blog.youtube/creator-and-artist-stories/your-guide-to-getting-started-with-youtube-shorts/">Your guide to getting started with YouTube Shorts</a> · YouTube/Google · 2025-04-08</li>
+<li id="source-y080">[Y080] <a href="https://support.google.com/youtube/answer/16215842?hl=en">Enhance your Shorts</a> · YouTube/Google · 날짜 미표기</li>
+<li id="source-y095">[Y095] <a href="https://vrew.imweb.me/faq/?bmode=view&amp;idx=12343625">AI 목소리를 상업적인 용도로 사용할 수 있을까요?</a> · Vrew 가이드 · 2025-11-20 갱신</li>
+<li id="source-y096">[Y096] <a href="https://typecast.ai/policy/">Typecast Usage policy</a> · Typecast · 날짜 미표기</li>
+<li id="source-y097">[Y097] <a href="https://www.samsungsvc.co.kr/solution/38418">갤럭시 음성녹음 방법 및 저장 경로</a> · 삼성전자서비스 · 2025-05-01</li>
```
