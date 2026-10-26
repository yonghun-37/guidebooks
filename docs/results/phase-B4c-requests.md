# B4c 통합 요청

공통 파일은 수정하지 않았다. 아래 diff는 통합 담당자가 다른 묶음 요청과 합쳐 적용한다. 현재는 본문 직접 주소와 하단 묶음 링크로 읽을 수 있으며, 공통 목차·이전/다음·선행 장은 아직 준비중으로 연결된다.

## 장 데이터

```diff
--- a/site-blog/assets/book.js
+++ b/site-blog/assets/book.js
@@ -102,7 +102,7 @@
     "직접 발행·예약·선택 API 구분",
     "내 속도로",
     "입문",
-    "준비중"
+    "완성"
   ],
   [
     11,
@@ -112,7 +112,7 @@
     "방문·조회·확정 수입 기록",
     "내 속도로",
     "입문",
-    "준비중"
+    "완성"
   ],
   [
     12,
@@ -122,7 +122,7 @@
     "내 글의 권리·표시 점검",
     "내 속도로",
     "입문",
-    "준비중"
+    "완성"
   ],
   [
     13,
@@ -132,7 +132,7 @@
     "내 시간에 맞춘 운영 메모",
     "내 속도로",
     "입문",
-    "준비중"
+    "완성"
   ],
   [
     14,
```

## 실험실 원본 도구 등록

```diff
--- a/site-blog/assets/catalog.js
+++ b/site-blog/assets/catalog.js
@@ -5,5 +5,33 @@
     "id": "revenue-tool",
     "title": "방문과 구매로 수입 계산하기",
     "section": "simulator"
+  },
+  {
+    "chapter": 10,
+    "slug": "10-automation",
+    "id": "automation-tool",
+    "title": "오늘 재사용할 틀 하나",
+    "section": "simulator"
+  },
+  {
+    "chapter": 11,
+    "slug": "11-analytics",
+    "id": "analytics-tool",
+    "title": "두 기간의 변화 읽기",
+    "section": "simulator"
+  },
+  {
+    "chapter": 12,
+    "slug": "12-policy",
+    "id": "disclosure-tool",
+    "title": "생활 가전 후기의 표시 위치 고르기",
+    "section": "simulator"
+  },
+  {
+    "chapter": 13,
+    "slug": "13-plan",
+    "id": "plan-tool",
+    "title": "하루 60분 계획표",
+    "section": "simulator"
   }
 ]);
```

네 도구는 `?embed=<id>`로 원본을 그대로 연다. localStorage를 쓰지 않으며 현재 입력/체크는 해당 화면에만 남긴다. 실험실 iframe·포커스 범위의 최종 검증은 등록을 적용한 뒤 수행한다. 13장 계획표는 모바일에서 행을 카드로 표시한다.

## 출처·진행 상태

- credits 통합 시 담당 네 장의 `aside.source-notes`에서 실제 인용 B번호와 원문 주소를 병합한다. 연구 파일은 변경하지 않았다.
- glossary는 `phase-B4c-glossary.md`의 항목을 병합한다. 기존 UV/PV/RPM을 중복 등록하지 않는다.
- prompts 통합은 각 장의 복사용 프롬프트 원본을 재사용한다. 각 장의 아래 ID에서 원문을 가져온다: `template-prompt`, `analysis-prompt`, `policy-prompt`, `plan-prompt`.
- 프로젝트 상태·서가 진행표는 통합 담당자가 B4c의 로컬 검증 결과를 반영한다. 실제 계정 발행·live API·OS 예약은 검증한 것으로 올리지 않는다.

## credits 인용 추가 diff

통합 시 다른 묶음의 중복을 제거하고 최종 목록을 정렬한다.

```diff
--- a/site-blog/credits.html
+++ b/site-blog/credits.html
@@ -15,2 +15,35 @@
 <ul><li id="source-b002">[B002] <a href="https://help.naver.com/service/5593/contents/15428?lang=ko&amp;osType=PC">예약 글 등록 방법</a> · 네이버 · 확인 2026-10-26</li><li id="source-b003">[B003] <a href="https://help.naver.com/service/30016/contents/24136?lang=ko&amp;osType=COMMONOS">AI 활용 설정 안내</a> · 네이버 · 확인 2026-10-26</li><li id="source-b018">[B018] <a href="https://help.naver.com/service/30005/contents/17695?lang=ko&amp;osType=COMMONOS">애드포스트 가입 조건</a> · 네이버 · 확인 2026-10-26</li><li id="source-b019">[B019] <a href="https://help.naver.com/service/30005/contents/17769?lang=ko&amp;osType=COMMONOS">개인회원 지급이 안된 경우</a> · 네이버 · 확인 2026-10-26</li><li id="source-b023">[B023] <a href="https://help.naver.com/service/30005/contents/17742?lang=ko&amp;osType=COMMONOS">미디어 등록 및 검수 방법</a> · 네이버 · 확인 2026-10-26</li><li id="source-b024">[B024] <a href="https://support.google.com/adsense/answer/9724?hl=ko">애드센스 자격 요건</a> · Google · 확인 2026-10-26</li><li id="source-b025">[B025] <a href="https://support.google.com/adsense/answer/1709871?hl=ko">지급 기준액</a> · Google · 확인 2026-10-26</li><li id="source-b027">[B027] <a href="https://support.google.com/adsense/answer/48182?hl=ko">애드센스 프로그램 정책</a> · Google · 확인 2026-10-26</li><li id="source-b037">[B037] <a href="https://www.law.go.kr/LSW/admRulInfoR.do?admRulSeq=2100000280130&amp;chrClsCd=010201">추천ㆍ보증 등에 관한 표시ㆍ광고 심사지침</a> · 공정위/국가법령정보센터 · 확인 2026-10-26</li><li id="source-b048">[B048] <a href="https://help.naver.com/service/5593/contents/15541?lang=ko&amp;osType=PC">글 발행 방법</a> · 네이버 · 확인 2026-10-26</li><li id="source-b049">[B049] <a href="https://help.naver.com/service/30027/contents/22952?lang=ko&amp;osType=COMMONOS&amp;ostype=commonos">크리에이터 가입 기준</a> · 네이버 · 확인 2026-10-26</li><li id="source-b058">[B058] <a href="https://support.google.com/adsense/answer/190515?hl=ko">RPM 정의</a> · Google · 확인 2026-10-26</li><li id="source-b060">[B060] <a href="https://scv1218.tistory.com/344">애드센스 8월 수익 공개</a> · SCV/개인 · 확인 2026-10-26</li><li id="source-b064">[B064] <a href="https://rosayoon00.tistory.com/m/150">애드포스트 첫 수익 공개</a> · 개인 운영자 · 확인 2026-10-26</li><li id="source-b076">[B076] <a href="https://help.naver.com/service/30027/contents/24104?lang=ko">쇼핑커넥트 링크 발급·삽입</a> · 네이버 · 확인 2026-10-26</li><li id="source-b082">[B082] <a href="https://notice.tistory.com/2701">AdFit 신규 연동 신청 종료</a> · 티스토리 공식(공지 시점별 카카오/AXZ) · 확인 2026-10-26</li><li id="source-b093">[B093] <a href="https://partners.coupangcdn.com/partners-guide/partners-guide-20260917111657.pdf">쿠팡 파트너스 최신 발견 이용가이드</a> · 쿠팡 · 확인 2026-10-26</li><li id="source-b122">[B122] <a href="https://help.naver.com/service/30027/contents/24101?lang=ko">쇼핑커넥트 크리에이터 권한 기준</a> · 네이버 · 확인 2026-10-26</li><li id="source-b123">[B123] <a href="https://help.naver.com/service/30027/contents/24106?lang=ko&amp;osType=COMMONOS">쇼핑커넥트 실적 인정 기준</a> · 네이버 · 확인 2026-10-26</li><li id="source-b124">[B124] <a href="https://help.naver.com/service/30027/contents/24108?lang=ko&amp;osType=COMMONOS">쇼핑커넥트 수익 정산</a> · 네이버 · 확인 2026-10-26</li><li id="source-b125">[B125] <a href="https://brandconnect.naver.com/service/policy/creator">브랜드커넥트 운영정책 크리에이터</a> · 네이버 · 확인 2026-10-26</li><li id="source-b129">[B129] <a href="https://accounts.revu.net/terms">레뷰 통합 약관</a> · 레뷰 · 확인 2026-10-26</li><li id="source-b130">[B130] <a href="https://kmong.com/support/expert-center/posts/751">크몽 판매 수수료</a> · 크몽 · 확인 2026-10-26</li><li id="source-b148">[B148] <a href="https://www.easylaw.go.kr/CSP/CnpClsMainBtr.laf?ccfNo=3&amp;cciNo=2&amp;cnpClsNo=2&amp;csmSeq=695">공표된 저작물의 인용</a> · 법제처 · 확인 2026-10-26</li><li id="source-b168">[B168] <a href="https://notice.tistory.com/2620">티스토리 관리·글쓰기</a> · 티스토리 공식(공지 시점별 카카오/AXZ) · 확인 2026-10-26</li><li id="source-b170">[B170] <a href="https://notice.tistory.com/m/2480">글 저장·발행·예약</a> · 티스토리 공식(공지 시점별 카카오/AXZ) · 확인 2026-10-26</li><li id="source-b173">[B173] <a href="https://help.naver.com/service/30010/contents/17597?osType=PC">네이버 제공 서비스 웹마스터 도구 연동</a> · 네이버 · 확인 2026-10-26</li><li id="source-b178">[B178] <a href="https://support.google.com/webmasters/answer/9012289?hl=ko">URL 검사 도구</a> · Google · 확인 2026-10-26</li><li id="source-b180">[B180] <a href="https://support.google.com/adsense/answer/7584263?hl=ko">사이트 연결·검토 요청</a> · Google · 확인 2026-10-26</li><li id="source-b182">[B182] <a href="https://support.google.com/adsense/answer/1269077?hl=ko">Blogger 광고 수입 설정</a> · Google · 확인 2026-10-26</li><li id="source-b185">[B185] <a href="https://notice.tistory.com/2565">티스토리 애드센스 연동</a> · 티스토리 공식(공지 시점별 카카오/AXZ) · 확인 2026-10-26</li><li id="source-b186">[B186] <a href="https://help.miricanvas.com/hc/ko/articles/31288096586649">미리캔버스 AI 서비스 이용약관</a> · 미리디 · 확인 2026-10-26</li><li id="source-b193">[B193] <a href="https://help.naver.com/service/30005/contents/17690?lang=ko">애드포스트 소개</a> · 네이버 · 확인 2026-10-26</li><li id="source-b199">[B199] <a href="https://m.blog.naver.com/makenewocean/222645059164">전자책 수익 공개</a> · 개인 운영자 · 확인 2026-10-26</li><li id="source-b205">[B205] <a href="https://help.naver.com/service/5593/contents/15290?osType=PC">게시글 일괄 수정·삭제 방법</a> · 네이버 · 확인 2026-10-26</li><li id="source-b206">[B206] <a href="https://help.naver.com/service/5593/contents/15425?osType=PC">태그 입력 및 설정 방법</a> · 네이버 · 확인 2026-10-26</li><li id="source-b207">[B207] <a href="https://notice.tistory.com/1796">내가 쓴 글 관리하기</a> · 티스토리 공식 · 확인 2026-10-26</li></ul>
+<ul>
+<li id="source-b006">[B006] <a href="https://developers.naver.com/notice/article/7527">블로그 오픈 API 종료 안내</a> · 네이버 · 확인 2026-10-26</li>
+<li id="source-b007">[B007] <a href="https://notice.tistory.com/2664">티스토리 Open API 종료 안내</a> · 티스토리 공식(공지 시점별 카카오/AXZ) · 확인 2026-10-26</li>
+<li id="source-b010">[B010] <a href="https://developer.wordpress.org/rest-api/reference/posts/">Posts REST API</a> · WordPress.org · 확인 2026-10-26</li>
+<li id="source-b011">[B011] <a href="https://developer.wordpress.org/advanced-administration/security/application-passwords/">Application Passwords</a> · WordPress.org · 확인 2026-10-26</li>
+<li id="source-b012">[B012] <a href="https://developers.google.com/blogger/docs/3.0/reference/posts/insert">Blogger API v3 posts.insert</a> · Google · 확인 2026-10-26</li>
+<li id="source-b014">[B014] <a href="https://developers.google.com/blogger/docs/3.0/getting_started">Blogger API Getting Started</a> · Google · 확인 2026-10-26</li>
+<li id="source-b017">[B017] <a href="https://hosting.cafe24.com/?controller=new_product_page&amp;page=wordpress-blog">워드프레스 블로그 호스팅</a> · 카페24 · 확인 2026-10-26</li>
+<li id="source-b031">[B031] <a href="https://developers.google.com/search/docs/fundamentals/using-gen-ai-content?hl=ko">웹사이트의 생성형 AI 콘텐츠 검색 안내</a> · Google · 확인 2026-10-26</li>
+<li id="source-b032">[B032] <a href="https://developers.google.com/search/docs/essentials/spam-policies?hl=ko">Google 웹 검색 스팸 정책</a> · Google · 확인 2026-10-26</li>
+<li id="source-b033">[B033] <a href="https://developers.google.com/search/docs/fundamentals/creating-helpful-content?hl=ko">유용하고 신뢰할 수 있는 사용자 중심 콘텐츠</a> · Google · 확인 2026-10-26</li>
+<li id="source-b034">[B034] <a href="https://developers.google.com/search/docs/appearance/ai-features?hl=ko">AI 기능 및 웹사이트</a> · Google · 확인 2026-10-26</li>
+<li id="source-b038">[B038] <a href="https://www.nts.go.kr/nts/cm/cntnts/cntntsView.do?cntntsId=7804&amp;mi=2483">SNS마켓 사업자 세무 안내</a> · 국세청 · 확인 2026-10-26</li>
+<li id="source-b052">[B052] <a href="https://help.miricanvas.com/hc/ko/articles/48267019052057">Pro 요금제 가이드</a> · 미리디 · 확인 2026-10-26</li>
+<li id="source-b054">[B054] <a href="https://ads.naver.com/help/faq/1406">키워드 도구 연관키워드 조회</a> · 네이버 · 확인 2026-10-26</li>
+<li id="source-b055">[B055] <a href="https://developers.naver.com/docs/serviceapi/datalab/search/search.md">통합 검색어 트렌드</a> · 네이버 · 확인 2026-10-26</li>
+<li id="source-b069">[B069] <a href="https://support.google.com/blogger/answer/9691230?hl=ko">블로그 설정 관리</a> · Google · 확인 2026-10-26</li>
+<li id="source-b085">[B085] <a href="https://help.naver.com/service/30005/contents/17810?lang=ko&amp;osType=COMMONOS">회원 유형별 세금 정산</a> · 네이버 · 확인 2026-10-26</li>
+<li id="source-b086">[B086] <a href="https://www.nts.go.kr/nts/cm/cntnts/cntntsView.do?cntntsId=7664">종합소득세 신고·납부</a> · 국세청 · 확인 2026-10-26</li>
+<li id="source-b087">[B087] <a href="https://support.google.com/adsense/answer/2490070?hl=ko">Google 미국 세금 정보 제출</a> · Google · 확인 2026-10-26</li>
+<li id="source-b097">[B097] <a href="https://help.openai.com/en/articles/9275245-using-chatgpt-s-free-tier-faq">ChatGPT Free Tier FAQ</a> · OpenAI · 확인 2026-10-26</li>
+<li id="source-b107">[B107] <a href="https://www.canva.com/pricing/">Canva pricing</a> · Canva · 확인 2026-10-26</li>
+<li id="source-b108">[B108] <a href="https://www.canva.com/policies/content-license-agreement/">Canva Content License</a> · Canva · 확인 2026-10-26</li>
+<li id="source-b144">[B144] <a href="https://developer.wordpress.com/docs/api/getting-started/">WordPress.com REST API 시작</a> · Automattic · 확인 2026-10-26</li>
+<li id="source-b149">[B149] <a href="https://www.copyright.or.kr/gov/nuri/download.do?brdctsfileno=25590&amp;brdctsno=54253">AI 활용 저작물 등록 안내서</a> · 문체부/한국저작권위원회 · 확인 2026-10-26</li>
+<li id="source-b150">[B150] <a href="https://www.law.go.kr/LSW/lsLinkCommonInfo.do?lsJoLnkSeq=1031810727">AI 기본법 제31조</a> · 국가법령정보센터 · 확인 2026-10-26</li>
+<li id="source-b151">[B151] <a href="https://www.msit.go.kr/eng/bbs/view.do?bbsSeqNo=42&amp;mId=4&amp;nttSeqNo=1215&amp;sCode=eng">MSIT Releases Guidelines on Ensuring AI Transparency</a> · 과기정통부 · 확인 2026-10-26</li>
+<li id="source-b152">[B152] <a href="https://www.nts.go.kr/nts/cm/cntnts/cntntsView.do?cntntsId=7900&amp;mi=6620">원천징수 대상 사업소득</a> · 국세청 · 확인 2026-10-26</li>
+<li id="source-b153">[B153] <a href="https://www.nts.go.kr/nts/cm/cntnts/cntntsView.do?cntntsId=238978&amp;mi=40483">모두채움 종합소득세 안내</a> · 국세청 · 확인 2026-10-26</li>
+<li id="source-b154">[B154] <a href="https://www.nts.go.kr/nts/na/ntt/selectNttInfo.do?nttSn=1396&amp;mi=2448">사업자등록 언제 어떻게</a> · 국세청 · 확인 2026-10-26</li>
+<li id="source-b155">[B155] <a href="https://www.irs.gov/forms-pubs/about-form-w-8-ben">About Form W-8 BEN</a> · IRS · 확인 2026-10-26</li>
+<li id="source-b158">[B158] <a href="https://policy.naver.com/rules/service.html">네이버 서비스 이용약관</a> · 네이버 · 확인 2026-10-26</li>
+</ul>
 <p>전체 인용과 제작 안내는 <a href="credits.html">출처·크레딧</a>에서 읽습니다.</p></aside></main>
```
