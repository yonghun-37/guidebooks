# AIa 공통 파일 통합 요청

2026-10-26. 공통 파일·프로젝트 상태·진행 페이지는 수정하지 않았다. 실제 보호 해시는 [before-hashes.json](phase-AIa/before-hashes.json)과 [scope-check.json](phase-AIa/scope-check.json)을 비교한다. 아래는 통합 담당자가 적용할 구체 diff다.

## 목차·페이지 경로·하단 링크와 출처 재생성

새 장은 5장 뒤·6장 앞이다. 번호는 확정 전이므로 `null`로 제안하며, 전체 장 번호를 정할 때 통합 담당자가 바꾼다. 이 상태에서도 slug로 읽기·이전/다음·모바일 목차가 작동한다. 두 부록은 루트 HTML 경로 분기에 꼭 추가한다. 표지의 목차는 `book.js`가 생성하므로 별도 index HTML 수정이 필요 없다.

```diff
--- a/site/assets/book.js
+++ b/site/assets/book.js
@@ -9,6 +9,7 @@
     [3, '03-revenue', '1부 · 이해하기', '돈은 네 갈래로 들어옵니다', '내 수익 경로와 오늘 할 일', '약 35분', '입문', '완성'],
     [4, '04-niche', '1부 · 이해하기', '니치와 계정 기획: 도울 독자를 좁힙니다', '계정 기획 시트', '약 40분', '입문', '완성'],
     [5, '05-sources', '2부 · 만들기', '소재 찾기: 뉴스 소싱과 저작권', '원문·권리·출처를 적은 소재 메모', '약 45분', '입문', '완성'],
+    [null, '05b-ai-tools', '2부 · 만들기', 'AI 도구 지도', '내 콘텐츠용 도구 조합과 월 예산 메모', '약 25분', '입문', '완성'],
     [6, '06-writing', '2부 · 만들기', 'AI로 글쓰기: 카드 문안과 릴스 대본', '지시문과 사실 대조 항목', '약 55분', '입문 · 파일 편집', '완성'],
     [7, '07-cards', '2부 · 만들기', '뉴스카드 디자인 자동화', '카드 정보 역할과 검수 기준', '약 50분', '입문 · 문안과 색 편집', '완성'],
     [8, '08-reels', '2부 · 만들기', '릴스 자동 생성: 대본에서 영상까지', '대본·음성·자막의 검수 계획', '약 60분', '입문 · 영상 검수', '완성'],
@@ -20,6 +21,8 @@
     [14, '14-plan', '4부 · 지키기·벌기', '30일 동안 할 일을 내 시간에 맞춥니다', '내 달력과 주간 점검표', '약 25분', '입문', '완성'],
     [15, 'lab', '실험실', '자동화 실험실', '그림·계산·연습 모음', '자유롭게', '입문', '완성'],
     [16, 'glossary', '부록', '용어집', '용어 찾아보기', '자유롭게', '입문', '완성'],
+    [null, 'prompts', '부록', '프롬프트 모음', '작업별 복사용 프롬프트 6종', '자유롭게', '입문', '완성'],
+    [null, 'ai-models', '부록', 'AI 모델·사용처·비용 총정리', '모델·사용처·월 지출과 편당 비용', '자유롭게', '입문', '완성'],
     [null, 'credits', '부록', '출처·크레딧', '출처와 업데이트 기록', '자유롭게', '입문', '완성']
   ];
   const chapters = chapterRows.map(([number, slug, part, title, deliverable, duration = '추후 안내', difficulty = '추후 안내', status = '준비중']) =>
@@ -49,7 +52,7 @@
   const url = path => prefix + path;
   const chapterUrl = chapter => {
     if (chapter.track === 'practice') return url(`practice/${chapter.slug}.html`);
-    if (['lab', 'glossary', 'credits'].includes(chapter.slug)) return url(`${chapter.slug}.html`);
+    if (['lab', 'glossary', 'prompts', 'ai-models', 'credits'].includes(chapter.slug)) return url(`${chapter.slug}.html`);
     return chapter.status === '완성' ? url(`chapters/${chapter.slug}.html`) : url(`chapters/coming-soon.html?chapter=${chapter.slug}`);
   };
   const byNumber = number => chapters.find(chapter => chapter.number === number);
@@ -121,7 +124,7 @@
   }
   document.querySelectorAll('[data-site-footer]').forEach(footer => {
     footer.className = 'site-footer';
-    footer.innerHTML = `<span>ReelsBook · 작은 콘텐츠 작업실을 만드는 책</span><span><a href="${url('glossary.html')}">용어집</a> &nbsp; <a href="${url('credits.html')}">출처·크레딧</a></span>`;
+    footer.innerHTML = `<span>ReelsBook · 작은 콘텐츠 작업실을 만드는 책</span><span><a href="${url('glossary.html')}">용어집</a> &nbsp; <a href="${url('credits.html')}">출처·크레딧</a> &nbsp; <a href="${url('prompts.html')}">프롬프트</a> &nbsp; <a href="${url('ai-models.html')}">모델·비용</a></span>`;
   });
 
   // 저장소 접근 자체도 실패할 수 있다. 테마와 체크 상태 모두 읽기/쓰기를 보호한다.
--- a/scripts/build_appendices.py
+++ b/scripts/build_appendices.py
@@ -10,7 +10,7 @@
 ROOT = Path(__file__).resolve().parents[1]
 SITE = ROOT / 'site'
 CHAPTERS = sorted((SITE / 'chapters').glob('[0-9][0-9]-*.html'))
-PAGES = CHAPTERS + sorted((SITE / 'practice').glob('*.html'))
+PAGES = sorted(CHAPTERS + [SITE / 'chapters/05b-ai-tools.html']) + sorted((SITE / 'practice').glob('*.html')) + [SITE / 'prompts.html', SITE / 'ai-models.html']
 E = html.escape
 
 
@@ -184,7 +184,8 @@
             for sid in sorted(set(re.findall(r'\bS\d{3}\b', text(item)))):
                 assert sid in sources, sid
                 track = '실습' if p.parent.name == 'practice' else '이론'
-                label = f'({track}) {int(p.name[:2])}' if p.name[:2].isdigit() else f'({track}) 전체 진행표'
+                ai_labels = {'05b-ai-tools': '(이론) AI 도구 지도', 'prompts': '(부록) 프롬프트 모음', 'ai-models': '(부록) AI 모델·사용처·비용 총정리'}
+                label = ai_labels.get(p.stem) or (f'({track}) {int(p.name[:2])}' if p.name[:2].isdigit() else f'({track}) 전체 진행표')
                 cited.setdefault(sid, []).append((str(p.relative_to(SITE).with_suffix('')), sorted(used)[0], label))
     entries=[]
     for sid,links in sorted(cited.items()):
```

`build_appendices.py`의 `catalog()`는 기존 이론 숫자 장만 읽는 현행 동작을 유지한다. 이번 diff는 출처·용어 처리용 `PAGES`에 새 파일을 더한다. 새 도구를 실험실에도 넣으려면 장 번호 확정 후 별도 통합한다.

크레딧 HTML은 위 diff를 적용한 뒤 `credits()`만 실행해 새 출처와 역링크를 생성한다. 전체 스크립트 실행은 용어 링크 등을 다른 장에도 쓰므로, 병렬 원고를 합친 뒤에만 한다. 현재 각 페이지에는 직접 원문으로 연결하는 자체 각주가 있다.

```python
import sys
sys.path.insert(0, 'scripts')
import build_appendices
print(build_appendices.credits())
```

재생성은 `site/credits.html`의 출처 목록과 인용 수를 바꾼다. 새로운 AI 이미지는 생성하지 않아 이미지 크레딧 추가는 없다. 서비스 화면·로고는 사용하지 않았다.

## 용어집

[신규 용어 후보](phase-AIa-glossary.md)의 쉬운 설명과 첫 등장 위치를 기존 생성기 용어 목록에 합친다. 이미 있는 API·TTS·지시문을 중복 등록하지 않는다. 원고에서는 새 용어를 처음 나온 자리에서 풀어 썼다. 미등록 `data-term` 링크는 넣지 않았다.

## 상태·진행 페이지

통합 담당자가 `docs/PROJECT_STATE.md`의 현재 구현 항목에 다음 diff를 반영한다. 전체 조사/출처/장 수는 다른 작업과 합친 뒤 재계산한다.

```diff
--- a/docs/PROJECT_STATE.md
+++ b/docs/PROJECT_STATE.md
@@ -12,6 +12,7 @@
 
 ## 현재 구조와 구현
 
+- ReelsBook AIa는 이론 ‘AI 도구 지도’와 부록 ‘프롬프트 모음’·‘AI 모델·사용처·비용 총정리’를 추가했다. 실제 서비스 표·무료/월 14,900원 카드/24,800원 디자인·음성 조합·선택 도우미, 복사용 6종, 모델/기능 274개 검색·모바일 카드·비용 계산을 제공한다. [AIa 결과](results/phase-AIa.md)에 검증과 화면을 기록했다. 공통 목차·번호·출처 재생성·최종 검수는 통합 단계에서 진행한다.
 - `site/`: 빌드 없는 정적 HTML/CSS/바닐라 JS. 이론1~14장·실험실·용어집·출처와 실습0~10·E2E의 두 트랙이다. `book.js`가 공통 메타·목차·이동을 관리한다. 모든 이론 장에 읽기·메모 예상 시간과 선행 장을 표시하며 연결 실습 시간은 별도다. 상대 링크로 `/reels/` 등 하위 경로를 지원한다.
 - 문체는 A 축별 설명+B FAQ5개+C 단계표다. 이론의 9블록·정리3줄·퀴즈를 유지하며 고정 기준선의70% 이하로 줄였다. [문체 통합](results/phase-9-int.md)·[인터랙션 구현](results/phase-11.md) 기록을 재사용한다. 비교 샘플은 `site/drafts/`에 보존한다.
 - 3장 돈의 네 갈래·7장 카드 편집·8장 재생 타임라인·10장 가상 게시·12장 증거 검수는 실습에서도 같은 도구를 쓴다. 3·13장 SVG 수입·비용·잔액은 텍스트 결과를 유지하며 무효 입력은 이전 그림을 숨긴다. 8장 미리보기는 모바일150px·데스크톱200px 폭으로 키웠다. 수치 입력은 모바일2열/접기로 줄였다.
```

`shelf/progress/index.html`은 기존 AI 관련 진행 항목에 이 결과 링크를 연결한다. 새 단계 타임라인을 임의로 늘리지 않는다. 완료 판단에는 실제 서비스 계정 가입·유료 생성·결제·게시가 포함되지 않는다.

## 추가 변경이 필요 없는 파일

`book.css`, `common.js`, `practice.js`에는 추가 변경이 필요 없다. 전용 `assets/ai-guide.css`·`assets/ai-guide.js`를 새 3페이지에서만 불러온다. 공통 자동 복사와 충돌하지 않도록 프롬프트는 읽기 전용 textarea와 전용 버튼을 사용한다. 전체 비용 계산 입력은 서버나 브라우저 저장소에 전송·저장하지 않는다.
