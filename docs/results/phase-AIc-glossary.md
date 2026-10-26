# AIc 용어집 통합 후보

본문은 첫 등장 자리에서 설명한다. 공통 용어집은 수정하지 않았다. TTS·프롬프트·템플릿·JSON 등 기존 항목은 재사용한다.

| 용어 | 뜻 | 첫 설명 위치 | 통합 시 권장 ID |
|---|---|---|---|
| LLM | 질문을 받아 글을 만드는 AI | `practice/03-copy.html#signup` | `llm` |
| 공용 크레딧 | 음성 만들기·음성 분석 등 여러 작업이 함께 쓰는 사용량 | `practice/00-start.html#record` | `shared-credits` |
| 키프레임 | 영상에서 시작과 끝의 크기·위치를 정하는 표시 | `practice/05-reel.html#video` | `keyframe` |
| B-roll | 해설 중에 보여 주는 보조 장면 | `practice/05-reel.html#video` | `b-roll` |

추가할 요소의 문맥 diff:

```diff
--- a/site/glossary.html
+++ b/site/glossary.html
@@ .glossary-list의 기존 항목 다음 (통합 생성기에도 같은 내용 반영)
+ <article class="glossary-entry" id="llm" data-glossary-entry data-category="제작" data-search="LLM 질문을 받아 글을 만드는 AI"><p class="small">제작</p><h2>LLM</h2><p>질문을 받아 글을 만드는 AI.</p><p><a href="practice/03-copy.html#signup">실습에서 보기 →</a></p></article>
+ <article class="glossary-entry" id="shared-credits" data-glossary-entry data-category="제작" data-search="공용 크레딧 여러 작업이 함께 쓰는 사용량"><p class="small">제작</p><h2>공용 크레딧</h2><p>음성 만들기·음성 분석 등 여러 작업이 함께 쓰는 사용량.</p><p><a href="practice/00-start.html#record">실습에서 보기 →</a></p></article>
+ <article class="glossary-entry" id="keyframe" data-glossary-entry data-category="제작" data-search="키프레임 keyframe 시작과 끝의 크기 위치 표시"><p class="small">제작</p><h2>키프레임</h2><p>영상에서 시작과 끝의 크기·위치를 정하는 표시.</p><p><a href="practice/05-reel.html#video">실습에서 보기 →</a></p></article>
+ <article class="glossary-entry" id="b-roll" data-glossary-entry data-category="제작" data-search="B-roll 비롤 해설 보조 장면"><p class="small">제작</p><h2>B-roll</h2><p>해설 중에 보여 주는 보조 장면.</p><p><a href="practice/05-reel.html#video">실습에서 보기 →</a></p></article>
```
