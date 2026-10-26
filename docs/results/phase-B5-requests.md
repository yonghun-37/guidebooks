# B5 공통 파일·조사 통합 요청

2026-10-26. 담당 범위인 `practice/`와 `assets/practice-workbook.js|css`만 구현했다. 아래는 **미적용 diff**다. 공통 자산·표지·출처·용어집·PROJECT_STATE·서가는 수정하지 않았다.

## 필수: 실습 목차를 실제 파일로 연결

공통 `book.js`는 실습 7 외에 여전히 `준비중`이라 사이드바·전체 목차가 pending으로 간다. 본문 상단·마지막의 직접 상대 링크로는 0→10→E2E가 연결된다. 통합 때 이 상태와 표지의 정적 목차를 함께 적용한다. 이론편 상태 변경과 충돌하면 해당 담당 결과를 함께 반영한다.

```diff
--- a/site-blog/assets/book.js
+++ b/site-blog/assets/book.js
@@ -213,8 +213,8 @@
     "Blogger 기본·설치형 WordPress 심화 계획"
   ]
 ];
-  const practice = practiceRows.map(([slug,title,deliverable],number) => Object.freeze({number,slug,title,deliverable,duration:'내 속도로',track:'practice',part:'실습편',difficulty:'입문',status:number===7?'샘플':'준비중'}));
-  practice.push(Object.freeze({number:null,slug:'e2e',title:'한 편 완성 체크리스트',deliverable:'공개 글과 실습 기록',duration:'필요할 때',track:'practice',part:'실습편',difficulty:'입문',status:'준비중'}));
+  const practice = practiceRows.map(([slug,title,deliverable],number) => Object.freeze({number,slug,title,deliverable,duration:['5분','15분','10분','15~20분','20~40분','10~15분','15분','10분','15분','15분','선택 25분'][number],track:'practice',part:'실습편',difficulty:'입문',status:'완료'}));
+  practice.push(Object.freeze({number:null,slug:'e2e',title:'한 편 완성 체크리스트',deliverable:'공개 글과 실습 기록',duration:'전체 시간표 참고',track:'practice',part:'실습편',difficulty:'입문',status:'완료'}));
   const appendices = [['prompts','프롬프트 모음'],['ai-models','AI 모델·사용처·비용 총정리'],['credits','출처·크레딧']].map(([slug,title])=>Object.freeze({number:null,slug,title,deliverable:slug==='credits'?'샘플에서 인용한 원문':'블로그 작업별 자료 준비중',track:'appendix',part:'부록',status:slug==='credits'?'샘플':'준비중'}));
   const tracks = Object.freeze([
     { id: 'theory', title: '(이론) 이론편', chapters },
```

```diff
--- a/site-blog/index.html
+++ b/site-blog/index.html
@@ -12,7 +12,7 @@
 <p class="eyebrow">SEARCH · WRITE · PUBLISH</p>
 <h2>AI로 초안을 쓰고,<br>내 경험으로 완성합니다.</h2>
 <p class="lead">검색으로 찾아온 독자의 질문에 답하는 글. 기획부터 사실 확인·발행·수익까지, 수아와 태오가 함께 갑니다.</p><div class="button-row"><a class="button primary" href="practice/00-start.html">오늘 첫 글 발행까지: 실습편 시작 →</a><a class="button" href="chapters/02-revenue.html">이론 2장 샘플 읽기</a></div>
-<p class="hero-foot">현재 공개: 수익 이론 · 첫 글 발행 샘플. 나머지 장은 준비중입니다.</p></div>
+<p class="hero-foot">실습 0~10과 전체 체크리스트를 읽을 수 있습니다. 첫 글 발행 뒤 검색·신청 상태를 기록하세요.</p></div>
 <figure class="cover-art"><div class="art-top"><span>퇴근 후 생활 정보</span><span>가상 블로그</span></div><svg viewBox="0 0 300 265" role="img" aria-label="독자의 질문을 AI 초안과 사람의 검수를 거쳐 공개 글로 완성하는 순서"><title>내 글이 만들어지는 순서</title><rect x="15" y="10" width="270" height="45" rx="8"/><text x="30" y="38">독자 질문 · 내 메모 · 공식 출처</text><path d="M150 60v20"/><rect x="15" y="85" width="270" height="45" rx="8"/><text x="30" y="114">AI · 개요와 초안</text><path d="M150 135v20"/><rect x="15" y="160" width="270" height="45" rx="8"/><text x="30" y="189">나 · 원문 대조와 경험 추가</text><text x="30" y="247">공개 글 → 모바일 확인 → 주소</text></svg><figcaption class="art-caption">내 자료와 사람의 확인이 글을 완성합니다.</figcaption></figure></section><div class="intro-strip">
 <p><strong>이론편</strong>수익·플랫폼·AI·검색을 이해합니다.</p>
 <p><strong>실습편</strong>내 글을 실제로 공개하고 주소를 남깁니다.</p>
@@ -26,5 +26,5 @@
 <ol><li><a href="chapters/pending.html?chapter=01-map">블로그 글 한 편이 돈이 되기까지</a> · 준비중</li><li><a href="chapters/02-revenue.html">블로그는 무엇으로 돈을 버나</a> · 샘플</li><li><a href="chapters/pending.html?chapter=03-ai-tools">AI 도구 지도</a> · 준비중</li><li><a href="chapters/pending.html?chapter=04-platforms">플랫폼 고르기</a> · 준비중</li><li><a href="chapters/pending.html?chapter=05-keywords">주제와 키워드</a> · 준비중</li><li><a href="chapters/pending.html?chapter=06-writing">AI로 글 쓰기 레시피</a> · 준비중</li><li><a href="chapters/pending.html?chapter=07-images">이미지·썸네일</a> · 준비중</li><li><a href="chapters/pending.html?chapter=08-seo">검색에 잘 보이는 글</a> · 준비중</li><li><a href="chapters/pending.html?chapter=09-monetize">수익 장치 붙이기</a> · 준비중</li><li><a href="chapters/pending.html?chapter=10-automation">반복과 자동화</a> · 준비중</li><li><a href="chapters/pending.html?chapter=11-analytics">숫자 읽기</a> · 준비중</li><li><a href="chapters/pending.html?chapter=12-policy">정책·저작권·광고 표시·세금</a> · 준비중</li><li><a href="chapters/pending.html?chapter=13-plan">30일 운영 계획</a> · 준비중</li></ol></section>
 <section>
 <h2>실습편</h2>
-<ol><li><a href="practice/pending.html?chapter=00-start">시작 전에: 오늘 쓸 글 고르기</a> · 준비중</li><li><a href="practice/pending.html?chapter=01-account">계정과 블로그 만들기</a> · 준비중</li><li><a href="practice/pending.html?chapter=02-setup">도구 준비</a> · 준비중</li><li><a href="practice/pending.html?chapter=03-keywords">키워드 고르기</a> · 준비중</li><li><a href="practice/pending.html?chapter=04-draft">AI 초안과 사실 확인</a> · 준비중</li><li><a href="practice/pending.html?chapter=05-images">이미지·썸네일 만들기</a> · 준비중</li><li><a href="practice/pending.html?chapter=06-editor">편집기에서 글 다듬기</a> · 준비중</li><li><a href="practice/07-publish.html">첫 글 실제로 발행하기</a> · 샘플</li><li><a href="practice/pending.html?chapter=08-search">검색 등록</a> · 준비중</li><li><a href="practice/pending.html?chapter=09-monetize">수익 장치 신청</a> · 준비중</li><li><a href="practice/pending.html?chapter=10-automation">선택: 자동화와 첫 숫자 확인</a> · 준비중</li></ol></section></div></section></main>
+<ol><li><a href="practice/00-start.html">시작 전에: 오늘 쓸 글 고르기</a> · 완료</li><li><a href="practice/01-account.html">계정과 블로그 만들기</a> · 완료</li><li><a href="practice/02-setup.html">도구 준비</a> · 완료</li><li><a href="practice/03-keywords.html">키워드 고르기</a> · 완료</li><li><a href="practice/04-draft.html">AI 초안과 사실 확인</a> · 완료</li><li><a href="practice/05-images.html">이미지·썸네일 만들기</a> · 완료</li><li><a href="practice/06-editor.html">편집기에서 글 다듬기</a> · 완료</li><li><a href="practice/07-publish.html">첫 글 실제로 발행하기</a> · 완료</li><li><a href="practice/08-search.html">검색 등록</a> · 완료</li><li><a href="practice/09-monetize.html">수익 장치 신청</a> · 완료</li><li><a href="practice/10-automation.html">선택: 자동화와 첫 숫자 확인</a> · 완료</li></ol></section></div></section></main>
 <footer data-site-footer></footer></body></html>
```

표지 정적 목차에는 `practice/e2e.html` 링크도 추가한다. 준비중 안내 페이지는 미완성 장의 안내로만 사용한다. 메타데이터의 7장 '샘플'→'완료'는 승인된 본문 변경을 의미하지 않는다.

## 출처 통합: 새로 직접 확인한 조작 안내

본문 정책·가격·요건은 기존 B 출처를 인용한다. 다음 세 페이지는 가입·대화·보안 조작을 보완하기 위해 추가로 열었다. 현재 실습 1·2에서는 **공식 사용 안내 직접 링크**로 제공한다. 출처표에 존재하지 않는 번호를 임의 각주로 사용하지 않았다. 통합 작업자가 충돌 없는 번호로 등록한 뒤 필요하면 B 각주로 전환한다.

| 제안 번호 | 공식 원문·확인일 | 실제 확인한 내용 | 적용 |
|---|---|---|---|
| B208 | [네이버 2단계 인증](https://help.naver.com/service/5640/contents/19238?lang=ko&osType=MOBILE), 2026-10-26 | 네이버ID 보안설정 → 2단계 인증, 인증 받을 네이버 앱·기기 확인. 최신 앱·스마트폰 안내 | 실습 1 보안. 기존 조사에서 재확인 대상으로 남은 경로 보완 |
| B209 | [카카오 2단계 인증](https://talksafety.kakao.com/toolandguide/account/auth), 2026-10-26 | 설정 → 카카오계정 → 2단계 인증, 카카오톡/전화번호 인증·비상연락 이메일 | 실습 1 티스토리 계정 보안 |
| B210 | [ChatGPT on the web](https://learn.chatgpt.com/docs/web), 2026-10-26 | 공식 웹 로그인·Chat·첫 메시지·결과 수정 흐름 | 실습 2, 3~6 대화 입력 위치. 무료 가격·한도 근거는 기존 B097 사용 |

모두 공식 본문 열람이며 로그인 후 실계정 조작을 뜻하지 않는다. `research-blog/SOURCES.md`, `FACT-SHEET.md`와 UI/AI 노트에 추가하고, QUESTION-MAP P01-5·P02-1의 재확인 메모를 갱신한다. Search Console·티스토리 가입·자동 사이트맵은 기존 B167·B178·B183·B184를 다시 열어 대조했다. B173·B176 재열람은 웹 도구 오류였으며 기존 직접 확인 기록에 근거했다.

## 상태·공통 부록

- PROJECT_STATE BlogBook 항목: B5 실습 0~6·8~10·E2E 작성·로컬 검증 완료, 실습 7 연결만 수정, 공통 목차 통합 대기로 갱신한다. B4a/b/c·B3k의 상태는 해당 결과 문서와 함께 통합한다. 현재의 '전체 집필은 시작하지 않았다' 문구는 통합 때 교체한다.
- glossary는 [phase-B5-glossary.md](phase-B5-glossary.md)를 검토한다. 본문에 없는 용어 앵커를 미리 만들지 않았다.
- credits에 이번 실습의 실제 B 인용과 AI 배경 1장의 제작 안내를 합친다. 이미지·요청문은 [B5 결과](phase-B5.md)의 제작 기록을 사용한다.
- 서가 진행표에는 B5 로컬 검증 완료·통합 대기를 반영한다. 배포·실계정 발행은 완료로 표시하지 않는다.
- `blog-kit` README/샘플은 수정하지 않았다. kit-run.json의 깨끗한 복사본 실행과 동일한 배포본을 제공하고, 공개 저장소에서 README/ZIP 경로가 열리는지 통합·배포 단계에 확인한다.

## 공통 JS 변경 불필요

실습 본문의 명시적 이전/다음·전체 경로는 기존 메타데이터 상태와 관계없이 실제 파일에 연결된다. 진행·주소 저장은 기존 practice.js의 `blogbook:practice:v1`, 추가 작업 메모는 `blogbook:worknotes:v1`을 사용한다. 검수표 15키는 E2E와 정확히 일치한다. 실습별 메모·복사 기능 때문에 공통 common.js나 practice.js를 수정할 필요는 없다.
