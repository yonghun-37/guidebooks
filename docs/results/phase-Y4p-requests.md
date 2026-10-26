# Y4p 공통 파일 통합 요청

실습 0~10·E2E는 본문이 작성됐다. 승인 샘플 8은 이전/다음·E2E·선택 API 연결만 수정했다. 공통 파일은 수정하지 않았다. 각 새 페이지에는 실습 전체를 직접 여는 로컬 내비게이션이 있다.

## 목차 상태와 링크 (적용 제안)

현재 공통 book.js는 실습 0·8 외를 준비중 화면으로 보낸다. 아래 diff는 **통합 담당자가 적용할 제안**이다. 이론 담당자의 상태 diff와 함께 반영한다. 공통 목차·헤더·샘플 8의 자동 pager는 이 제안을 적용하기 전까지 준비중 표시가 남는다.

```diff
--- a/site-shorts/assets/book.js
+++ b/site-shorts/assets/book.js
@@ -171,49 +171,49 @@
   [
     "00-start",
     "시작 전에: 준비물, 오늘 끝나는 것",
-    "실습 원고 준비중",
+    "내 영상 제작 결과물",
     "추후 안내"
   ],
   [
     "01-account",
     "구글 계정·유튜브 채널 만들기(연습 채널 포함), 2단계 인증",
-    "실습 원고 준비중",
+    "내 영상 제작 결과물",
     "추후 안내"
   ],
   [
     "02-setup",
     "도구 설치: 무료 편집 프로그램 1종 + 스타터 키트(쇼츠용)",
-    "실습 원고 준비중",
+    "내 영상 제작 결과물",
     "추후 안내"
   ],
   [
     "03-script",
-    "대본 쓰기(웹 채팅 붙여넣기)",
-    "실습 원고 준비중",
+    "AI로 기획·대본 만들기",
+    "내 영상 제작 결과물",
     "추후 안내"
   ],
   [
     "04-voice",
-    "내레이션 녹음(휴대폰)",
-    "실습 원고 준비중",
+    "본인 녹음 또는 AI 음성 만들기",
+    "내 영상 제작 결과물",
     "추후 안내"
   ],
   [
     "05-scenes",
-    "장면 만들기: 폰 촬영 / 권리 확인 소재 / (선택) AI 생성",
-    "실습 원고 준비중",
+    "폰 촬영·스톡·AI 이미지·AI 영상으로 장면 만들기",
+    "내 영상 제작 결과물",
     "추후 안내"
   ],
   [
     "06-edit",
     "편집과 자막",
-    "실습 원고 준비중",
+    "내 영상 제작 결과물",
     "추후 안내"
   ],
   [
     "07-export",
     "9:16 출력과 화질 확인",
-    "실습 원고 준비중",
+    "내 영상 제작 결과물",
     "추후 안내"
   ],
   [
@@ -225,18 +225,18 @@
   [
     "09-api",
     "(선택) YouTube Data API로 업로드: 프로젝트·OAuth·할당량·미검증 앱 제한",
-    "실습 원고 준비중",
+    "내 영상 제작 결과물",
     "추후 안내"
   ],
   [
     "10-insights",
     "첫 24시간·7일 숫자 확인",
-    "실습 원고 준비중",
+    "내 영상 제작 결과물",
     "추후 안내"
   ]
 ];
   const practice = practiceRows.map(([slug, title, deliverable, duration], number) => Object.freeze({
-    number, slug, title, deliverable, duration, track: 'practice', part: '실습편', difficulty: '입문', status: '준비중', sample: number === 8
+    number, slug, title, deliverable, duration, track: 'practice', part: '실습편', difficulty: '입문', status: '완성', sample: number === 8
   }));
   const tracks = Object.freeze([
     { id: 'theory', title: '(이론) 이론편', chapters },
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
+  const status = chapter => `<span class="status ${chapter.status === '완성' || chapter.sample ? 'ready' : ''}">${chapter.status === '완성' ? '읽기 가능' : chapter.sample ? '확인용 샘플' : '준비중'}</span>`;
   const label = chapter => `(${chapter.track === 'practice' ? '실습' : '이론'}) ${chapter.number != null ? chapter.number + (chapter.track === 'practice' ? '. ' : '장 · ') : ''}${chapter.title}`;
   const link = chapter => `<a href="${chapterUrl(chapter)}">${esc(label(chapter))} ${status(chapter)}</a>`;
   const selected = (document.body.dataset.chapter === 'pending' || document.body.dataset.practice === 'pending') ? new URLSearchParams(location.search).get('chapter') : document.body.dataset.chapter;
```

실습별 deliverable은 본문 hero의 결과물로, 소요 시간은 실습 0의 학습 일정과 일치하게 교체한다. `추후 안내`를 기계적으로 같은 시간으로 바꾸지 않는다. E2E는 기존 실습 0/8의 직접 연결과 새 페이지 내비게이션으로 접근 가능하며 표지의 실습 목차 아래에도 연결한다.

## 표지·출처·상태 통합

- `site-shorts/index.html`: "실습 원고 준비중" 설명을 AI 제작 기본 경로(무료 ChatGPT → 녹음/AI 음성 → 촬영·스톡·생성 장면 → Clipchamp 자동 자막·출력 → 공식 업로드)와 `practice/e2e.html` 링크로 바꾼다.
- `site-shorts/credits.html`: 기존 research-shorts/SOURCES의 Y300·Y302·Y329~Y330·Y334·Y336~Y339·Y342~Y343·Y347~Y349·Y363~Y364·Y367·Y369·Y374·Y382~Y385·Y388·Y391·Y394 등을 중복 없이 통합한다. 정확한 사용 목록은 각 실습의 출처 aside를 기준으로 한다.
- 실제 AI 예시는 `assets/img/ai-examples/paper-robot-reference.png`. 내장 imagegen으로 생성했고 프롬프트를 실습 5와 결과 폴더 `image-provenance.json`에 공개했다. 서비스 화면·실존 인물·브랜드·로고를 넣지 않았다. AI 영상 생성 성공을 주장하는 예시는 아니다.
- `docs/PROJECT_STATE.md`: 실습 0~7·9·10·E2E 집필과 정적/Chromium·키트 임시 복사본 검증 완료를 반영한다. 공통 목차 상태 적용·독립 검수·실기기/실계정 확인은 별도로 남긴다.
- `shelf/progress/index.html`: 이 단계 원고 작성·로컬 검증 완료와 공통 통합/독립 검수 대기를 구별해 갱신한다.
- 용어 제안은 [phase-Y4p-glossary.md](phase-Y4p-glossary.md)에 있다.

## 키트 안내에서 발견한 점

prompt 모드는 prompt.md만 만든다. 사용자가 script.json을 저장하기 전 validate하면 파일 누락으로 멈춘다. 본문은 이 저장 단계를 명시했다. Windows/macOS 명령은 같은 CLI의 OS별 경로 안내이며 실제 실행 증거는 Linux/Python 3.11.15이다. README에 Python 버전 선택 예를 덧붙일 경우 실습 2와 맞춘다.

공통 문서 제목에도 아래 변경이 필요하다. 현재 완료 원고의 브라우저 탭 제목에 남는 "준비 중"은 이 조건에서 온다.

```diff
--- a/site-shorts/assets/book.js
+++ b/site-shorts/assets/book.js
@@
-    if (!current.sample) document.title = `${current.title} · 준비 중 | ShortsBook`;
+    if (!current.sample && current.status !== '완성') document.title = `${current.title} · 준비 중 | ShortsBook`;
```
