# AIc 통합 요청 — 공통 파일은 수정하지 않음

AIc 소유 파일은 `site/practice/00-start.html`, `03-copy.html`, `04-cards.html`, `05-reel.html`, `e2e.html`이다. 공통 파일과 실습 6·7·상태 문서는 통합 담당자가 고친다. `book.css`·`common.js`·`practice.js` 변경은 필요 없다. PC/휴대폰 탭도 기존 탭 동작을 재사용한다.

## 1. book.js 메타 — 적용 가능한 diff

본문 H1은 새 제목을 직접 넣어 기존 메타가 덮어쓰지 않게 했다. 아래 diff를 적용하면 브라우저 제목·전체 목차·이전/다음 링크에도 새 제목·시간이 반영된다. 실습 1 뒤의 기본 이동은 실습 3이며, 실습 2는 선택 키트로 따로 접근하도록 통합한다. 실습 4 뒤는 릴스 선택 여부에 따라 본문의 두 경로를 따르게 한다.

```diff
--- a/site/assets/book.js
+++ b/site/assets/book.js
@@ -25,13 +25,13 @@
   const chapters = chapterRows.map(([number, slug, part, title, deliverable, duration = '추후 안내', difficulty = '추후 안내', status = '준비중']) =>
     Object.freeze({ number, slug, part, title, deliverable, duration, difficulty, status, track: 'theory' }));
   const practiceRows = [
-    ['00-start', '시작 전에', '오늘 할 경로와 준비물 메모', '약 10분'],
+    ['00-start', '오늘 만들 AI 콘텐츠 고르기', '오늘의 유형·서비스·시간·파일 보관 메모', '약 10분'],
     ['01-account', '테스트 계정과 보안 준비', '대상 계정 이름·공개 범위·복구 수단', '약 25분'],
-    ['02-setup', '키트 설치와 첫 실행', '카드·영상과 검수 대기 폴더', '약 35분'],
-    ['03-copy', '소재 고르기와 웹 채팅 문안', '원출처가 담긴 copy.json', '약 30분'],
-    ['04-cards', '뉴스카드 캐러셀 만들기', '순서와 글자를 확인한 JPEG 카드 묶음', '약 20분'],
-    ['05-reel', '본인 녹음과 릴스 만들기', '끝까지 재생해 본 reel.mp4', '약 25분'],
-    ['06-review', '게시 전 사람 검수', '검수표·APPROVED.json·드라이런', '약 20분'],
+    ['02-setup', '선택 · 키트 설치와 첫 실행', '카드·영상과 검수 대기 폴더', '약 35분'],
+    ['03-copy', 'ChatGPT로 뉴스 요약과 카드 문안 만들기', '원문과 대조한 cards.txt·출처·게시 설명문', '약 30분'],
+    ['04-cards', 'Canva로 4:5 뉴스카드 만들기', '1080×1350 카드 PNG/JPG 5장과 편집 원본', '약 30분'],
+    ['05-reel', 'CapCut으로 모션·해설 릴스 만들기', '검수한 reel.mp4·편집 원본·음성/자막/권리 메모', '모션 약 35분 / 해설 약 50분'],
+    ['06-review', '게시 전 사람 검수', '파일 검수·표시 메모 (키트는 승인·드라이런)', '약 20분'],
     ['07-publish', '앱으로 첫 게시하기', '직접 확인한 첫 게시물과 그 주소', '약 30분'],
     ['08-api', '선택 · API 자동 게시', '계정·권한·공개 URL을 확인한 요청 미리보기', '약 60분 이상 · 선택 심화'],
     ['09-schedule', '매일 생성 예약과 사람 승인', '매일 생성 설정·날짜별 폴더·검수와 게시 계획', '약 30분 + 다음 날 확인'],
```

## 2. 실습 6·7 기본 경로 연결 — 요소 단위 문맥 diff

아래는 한 줄 HTML 안에서 해당 요소를 교체할 문맥 diff다. AIc에서는 E2E의 `#service-review`에서 직접 검수하고 실습 7로 넘기는 경로를 이미 제공한다. 이 요청을 적용하면 실습 6의 첫 화면에서도 같은 분기가 보인다. 기존 키트 명령·승인 규칙은 보존한다.

```diff
--- a/site/practice/06-review.html
+++ b/site/practice/06-review.html
@@ .lead / 준비물 / 선행 실습
- <strong>검수표·APPROVED.json·드라이런</strong>
+ <strong>파일 검수·표시 메모 (키트는 승인·드라이런)</strong>
- <dd>원자료, 카드·영상, REVIEW.md, 이론 12장 체크리스트</dd>
+ <dd>원자료, 서비스 완성 파일·권리 메모 또는 키트 REVIEW.md, 이론 12장 체크리스트</dd>
- <dd><a href="05-reel.html">실습 5</a></dd>
+ <dd><a href="04-cards.html">실습 4 카드</a> 또는 <a href="05-reel.html">실습 5 릴스</a></dd>
@@ .chapter-hero 다음
+ <aside class="practice-box"><h2>Canva·CapCut으로 만들었다면</h2><p><a href="e2e.html#service-review">서비스 파일 검수표</a>로 사실·화면·권리와 표시를 확인하고 review.txt 또는 메모에 파일명·검수일을 적으세요. 아래의 AI·협찬 표시 설명을 함께 읽은 뒤 <a href="07-publish.html#transfer">실습 7 앱 게시</a>로 가세요. 키트용 REVIEW.md·APPROVED.json·드라이런은 만들지 않아요. 아래 묶음 승인 명령은 스타터 키트 경로를 고른 경우에만 따라요.</p></aside>
@@ #review .practice-follow / .practice-success
- <li><a href="../chapters/12-safety.html#safety-sim">이론 12장 게시 전 체크리스트</a>와 출력 폴더 REVIEW.md를 열어요.</li>
+ <li>서비스 파일은 <a href="e2e.html#service-review">서비스 검수표</a>로 확인하고, 키트는 <a href="../chapters/12-safety.html#safety-sim">이론 12장 체크리스트</a>와 출력 폴더 REVIEW.md를 열어요.</li>
- <strong>생성된 모든 JPEG와 영상 끝까지</strong>
+ <strong>선택한 경로의 모든 카드와 영상 끝까지</strong>
- 카드만 게시해도 현재 승인은 카드·영상 묶음 전체를 확인하므로 영상 검수를 생략하지 않아요.
+ 키트는 카드·영상 묶음을 승인하므로 카드만 게시해도 함께 생성된 영상을 검수해요. 서비스에서 카드만 만들었다면 그 카드만 검수해요.
- <p>REVIEW.md의 여섯 항목을 실제로 검토했고 여섯 줄만 [x]로 저장했어요. 자동으로 체크하는 명령은 사용하지 않아요.</p>
+ <p>서비스 파일은 review.txt에 파일명·검수일·수정 내용을 남겼어요. 키트는 REVIEW.md의 여섯 항목을 직접 검토해 [x]로 저장했어요.</p>
@@ #approve 제목
- <h2>승인과 드라이런 확인</h2>
+ <h2>키트 선택 · 승인과 드라이런 확인</h2>
--- a/site/practice/07-publish.html
+++ b/site/practice/07-publish.html
@@ 준비물 / 선행 실습 / 첫 안내
- <dd>본인 계정, 실습 6에서 검수한 실제 자료, 휴대폰, 전송 수단</dd>
+ <dd>본인 계정, 검수한 서비스 파일 또는 키트 실제 자료, 휴대폰, 전송 수단</dd>
- <dd><a href="06-review.html">실습 6</a></dd>
+ <dd><a href="e2e.html#service-review">서비스 파일 검수</a> 또는 <a href="06-review.html">실습 6 키트 검수</a></dd>
+ <p>Canva·CapCut 결과는 <a href="e2e.html#service-review">서비스 검수표</a>를 마친 파일로 시작해요. 키트 승인 명령은 필요 없어요.</p>
```

## 3. 목차·기본 이동

```diff
--- a/site/index.html
+++ b/site/index.html
@@ 실습편 기본 경로를 소개하는 문구
- <p>(실습) 0~7을 따라 계정·설치·문안·카드·릴스·검수·앱 게시를 잇습니다. 원리가 궁금하면 (이론)으로 돌아오세요.</p>
+ <p>실습 0 유형 선택 → 1 계정·보안 → 3 ChatGPT 문안 → 4 Canva 카드 → 선택 5 CapCut 릴스 → 파일 검수 → 7 앱 게시로 이어가요. 실습 2 키트 설치·8 API·9 매일 생성은 선택 경로예요.</p>
- <p>(실습) 6에서 검수·승인, 8에서 Instagram Login API 설정을 이어갑니다. (이론) 9~10장에서 경계와 실패 처리를 읽으세요.</p>
+ <p>기본 경로는 파일 검수 후 앱으로 게시해요. 키트의 검수·승인은 실습 6, Instagram Login API는 선택 실습 8에서 이어가요. 이론 9~10장에서 실패 처리를 읽으세요.</p>
--- a/site/assets/book.js
+++ b/site/assets/book.js
@@ data-chapter-pager의 practice 기본 이동 (통합 시 기본 경로만)
- const previous = sequence[index - 1], next = sequence[index + 1];
+ const previous = sequence[index - 1];
+ const next = current.track === 'practice' && current.slug === '01-account'
+   ? practice.find(item => item.slug === '03-copy') : sequence[index + 1];
```

실습 4의 “카드만이면 검수 → 7 / 영상이면 5”, 실습 5의 “검수 → 7” 버튼은 본문에 구현했다. 기존 공통 pager를 필수 순서로 오해하지 않게 통합 문구를 맞춘다. 실습 진행 저장 키는 기존 38개를 유지하고 서비스 가입·템플릿·삽화 선택·자막·내보내기의 5개를 추가했다(총 43개). 이전 체크는 보존되며 새 결과를 재확인하라는 안내가 있다.

## 4. 출처·크레딧

공통 `credits.html`은 직접 수정하지 않았다. 통합 원고가 확정되면 기존 `scripts/build_appendices.py`의 `credits()`만 사용해 인용 출처와 역링크를 다시 생성한다. 전체 스크립트 실행은 다른 공통 파일·원고까지 바꿀 수 있으므로 별도 통합 검수가 필요하다. 아래는 AIc에서 새로 인용하는 항목만 표시한 데이터 diff다(실제 HTML은 기존 생성기를 사용).

```diff
--- a/site/credits.html 인용 출처·역링크
+++ b/site/credits.html 인용 출처·역링크
+ S300: practice/00-start.html#source-s300, practice/03-copy.html#source-s300, practice/04-cards.html#source-s300, practice/e2e.html#source-s300
+ S302: practice/03-copy.html#source-s302
+ S303: practice/03-copy.html#source-s303
+ S318: practice/00-start.html#source-s318, practice/04-cards.html#source-s318, practice/e2e.html#source-s318
+ S320: practice/00-start.html#source-s320, practice/04-cards.html#source-s320
+ S326: practice/00-start.html#source-s326, practice/05-reel.html#source-s326
+ S327: practice/00-start.html#source-s327, practice/05-reel.html#source-s327, practice/e2e.html#source-s327
+ S328: practice/05-reel.html#source-s328
+ S330: practice/00-start.html#source-s330, practice/05-reel.html#source-s330
+ S334: practice/00-start.html#source-s334, practice/05-reel.html#source-s334, practice/e2e.html#source-s334
+ S365: practice/00-start.html#source-s365, practice/04-cards.html#source-s365
+ S366: practice/00-start.html#source-s366, practice/05-reel.html#source-s366
+ S374: practice/04-cards.html#source-s374
+ S380: practice/00-start.html#source-s380, practice/05-reel.html#source-s380, practice/e2e.html#source-s380
+ S385: practice/05-reel.html#source-s385
+ S388: practice/00-start.html#source-s388, practice/05-reel.html#source-s388
+ S389: practice/04-cards.html#source-s389, practice/05-reel.html#source-s389, practice/e2e.html#source-s389
+ S396: practice/00-start.html#source-s396, practice/03-copy.html#source-s396
```

현 작업 트리에는 다른 단계에서 편집 중인 이론 6~8장·쇼츠 파일이 있다. 첫 `check_site.py`는 당시 편집 중이던 이론·기존 크레딧의 앵커 차이를 검출했다. 최종 재실행은 현재 작업 트리 전체와 AIc 다섯 파일만 HEAD 위에 적용한 분리 검사 모두 통과했다. 전체 검사 결과와 재현 범위는 `phase-AIc/`에서 확인한다.

## 5. 용어집·현재 상태

새 용어 후보와 첫 설명 위치는 [phase-AIc-glossary.md](phase-AIc-glossary.md)에 정리했다. `glossary.html`은 미수정이다.

```diff
--- a/docs/PROJECT_STATE.md
+++ b/docs/PROJECT_STATE.md
@@ 현재 구조와 구현의 실습편 경로
- 실습7 앱 게시가 기본이며 첫 게시 경로는0~7이다.
+ 실습7 앱 게시가 기본이며 AI 서비스 첫 제작은 0 유형 선택 → 1 계정·보안 → 3 ChatGPT 문안 → 4 Canva 카드 → 선택 5 CapCut 릴스 → 파일 검수 → 7 앱 게시다. 키트 2·API 8·매일 생성 9는 선택 경로다. 기본 경로는 TXT/메모·PNG/JPG·MP4를 넘기고 키트 대안은 기존 명령을 유지한다. E2E43개 키는 본문과 일치한다.
@@ 작업 중 / 남은 통합
+ AIc 실습0·3·4·5·E2E 원고와 검증은 완료했다. book.js·목차·실습6/7 연결·크레딧 통합은 phase-AIc-requests.md를 적용한 뒤 전체 검사와 Claude Code 검수가 필요하다. 실계정 로그인·서비스 생성·실기기 조작·게시 성공은 검증 범위에 포함하지 않았다.
--- a/shelf/progress/index.html
+++ b/shelf/progress/index.html
@@ AI 제작 실습 진행 안내
+ AIc · 인스타 실습 0·3·4·5·E2E 작성·검증 완료, 공통 메타·크레딧 통합 대기 (docs/results/phase-AIc.md)
```
