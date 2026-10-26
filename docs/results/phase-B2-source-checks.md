# Phase B2 공식 출처 직접 확인표

2026-10-26. Codex가 실제 원문 설명을 확인한 출처만 집계한다. 로그인 화면·메뉴만 나온 HTTP200, 검색 결과만 확인, Hermes만 확보, 기존 조사 재사용은 제외했다. 같은 URL의 중복 출처번호는 고유URL수에서 하나로 센다. 날짜 없는 문서는 개정일을 추정하지 않는다.

- 공식 직접 확인: **100개 출처 항목 / 100개 고유 URL**. 사용자 요구15개 이상 충족.
- 확인 수단: 웹 도구 본문 또는 urllib 다운로드+본문 추출. 쿠팡 PDF는 pypdf로81쪽 텍스트를 추출하고 관련 쪽을 대조했다. 전체 PDF를 화면별로 실사했다고 주장하지 않는다.
- 로컬 임시 추출·HTTP 기록: `/tmp/blog-b2-evidence/`(공개 저장소 미포함). 임시 자료는 장기 보존을 보장하지 않으며 원문 URL과 채택 사실을 저장소에 남겼다.

| 출처 | 기관·문서 | 읽어 확인한 범위/방법 |
|---|---|---|
| [B001](../../research-blog/SOURCES.md#b001) | 네이버 · [내 블로그 개설 방법](https://help.naver.com/service/5593/contents/15183?lang=ko&osType=COMMONOS) | 직접 본문 확인 |
| [B002](../../research-blog/SOURCES.md#b002) | 네이버 · [예약 글 등록 방법](https://help.naver.com/service/5593/contents/15428?lang=ko&osType=PC) | 직접 본문 확인 |
| [B003](../../research-blog/SOURCES.md#b003) | 네이버 · [AI 활용 설정 안내](https://help.naver.com/service/30016/contents/24136?lang=ko&osType=COMMONOS) | 직접 본문 확인 |
| [B004](../../research-blog/SOURCES.md#b004) | 네이버 · [블로그 검색 제한 기준 안내](https://help.naver.com/service/5626/contents/22928?lang=ko&osType=COMMONOS) | 직접 본문 확인 |
| [B005](../../research-blog/SOURCES.md#b005) | 네이버 · [블로그 검색 로직 D.I.A. 소개](https://help.naver.com/service/5626/contents/22926?lang=ko&osType=COMMONOS) | 직접 본문 확인 |
| [B006](../../research-blog/SOURCES.md#b006) | 네이버 · [블로그 오픈 API 종료 안내](https://developers.naver.com/notice/article/7527) | 직접 본문 확인 |
| [B007](../../research-blog/SOURCES.md#b007) | 티스토리 공식(공지 시점별 카카오/AXZ) · [티스토리 Open API 종료 안내](https://notice.tistory.com/2664) | 직접 본문 확인 |
| [B008](../../research-blog/SOURCES.md#b008) | 티스토리 공식(공지 시점별 카카오/AXZ) · [티스토리 자체 광고 신설](https://notice.tistory.com/2646) | 직접 본문 확인 |
| [B009](../../research-blog/SOURCES.md#b009) | 티스토리 공식(공지 시점별 카카오/AXZ) · [수익화 관련 운영 정책 변경](https://notice.tistory.com/2687) | 직접 본문 확인 |
| [B010](../../research-blog/SOURCES.md#b010) | WordPress.org · [Posts REST API](https://developer.wordpress.org/rest-api/reference/posts/) | 직접 본문 확인 |
| [B011](../../research-blog/SOURCES.md#b011) | WordPress.org · [Application Passwords](https://developer.wordpress.org/advanced-administration/security/application-passwords/) | 직접 본문 확인 |
| [B012](../../research-blog/SOURCES.md#b012) | Google · [Blogger API v3 posts.insert](https://developers.google.com/blogger/docs/3.0/reference/posts/insert) | 직접 본문 확인 |
| [B013](../../research-blog/SOURCES.md#b013) | Google · [Blogger API posts.publish](https://developers.google.com/blogger/docs/3.0/reference/posts/publish) | 직접 본문 확인 |
| [B014](../../research-blog/SOURCES.md#b014) | Google · [Blogger API Getting Started](https://developers.google.com/blogger/docs/3.0/getting_started) | 직접 본문 확인·HTTP200 메뉴만 수신과 구별 |
| [B015](../../research-blog/SOURCES.md#b015) | Automattic · [WordPress.com Pricing](https://wordpress.com/pricing/) | 직접 본문 확인 |
| [B016](../../research-blog/SOURCES.md#b016) | Automattic · [Monetize your site](https://wordpress.com/support/monetize-your-site/) | 직접 본문 확인 |
| [B017](../../research-blog/SOURCES.md#b017) | 카페24 · [워드프레스 블로그 호스팅](https://hosting.cafe24.com/?controller=new_product_page&page=wordpress-blog) | 직접 본문 확인 |
| [B018](../../research-blog/SOURCES.md#b018) | 네이버 · [애드포스트 가입 조건](https://help.naver.com/service/30005/contents/17695?lang=ko&osType=COMMONOS) | 직접 본문 확인 |
| [B019](../../research-blog/SOURCES.md#b019) | 네이버 · [개인회원 지급이 안된 경우](https://help.naver.com/service/30005/contents/17769?lang=ko&osType=COMMONOS) | 직접 본문 확인 |
| [B020](../../research-blog/SOURCES.md#b020) | 네이버 · [Npay 수입 전환 방법](https://help.naver.com/service/30005/contents/17793?lang=ko&osType=COMMONOS) | 직접 본문 확인 |
| [B021](../../research-blog/SOURCES.md#b021) | 네이버 · [애드포스트 자주 찾는 질문](https://help.naver.com/service/30005/bookmark/20033?lang=ko&osType=COMMONOS) | 직접 본문 확인 |
| [B022](../../research-blog/SOURCES.md#b022) | 네이버 · [애드포스트 설정 방법](https://help.naver.com/service/5593/contents/15308?lang=ko&osType=PC) | 직접 본문 확인 |
| [B023](../../research-blog/SOURCES.md#b023) | 네이버 · [미디어 등록 및 검수 방법](https://help.naver.com/service/30005/contents/17742?lang=ko&osType=COMMONOS) | 직접 본문 확인·고정 심사 숫자 미공개 |
| [B024](../../research-blog/SOURCES.md#b024) | Google · [애드센스 자격 요건](https://support.google.com/adsense/answer/9724?hl=ko) | 직접 본문 확인 |
| [B025](../../research-blog/SOURCES.md#b025) | Google · [지급 기준액](https://support.google.com/adsense/answer/1709871?hl=ko) | 직접 본문 확인 |
| [B026](../../research-blog/SOURCES.md#b026) | Google · [Updates to how publishers monetize with AdSense](https://blog.google/products/adsense/evolving-how-publishers-monetize-with-adsense/) | 직접 본문 확인 |
| [B027](../../research-blog/SOURCES.md#b027) | Google · [애드센스 프로그램 정책](https://support.google.com/adsense/answer/48182?hl=ko) | 직접 본문 확인 |
| [B030](../../research-blog/SOURCES.md#b030) | 쿠팡 · [쿠팡 파트너스 이용가이드](https://partners.coupangcdn.com/partners-guide/partners-guide-20251028182159.pdf) | 직접 PDF 다운로드·79쪽 텍스트 확인 |
| [B031](../../research-blog/SOURCES.md#b031) | Google · [웹사이트의 생성형 AI 콘텐츠 검색 안내](https://developers.google.com/search/docs/fundamentals/using-gen-ai-content?hl=ko) | 직접 본문 확인 |
| [B032](../../research-blog/SOURCES.md#b032) | Google · [Google 웹 검색 스팸 정책](https://developers.google.com/search/docs/essentials/spam-policies?hl=ko) | 직접 본문 확인 |
| [B033](../../research-blog/SOURCES.md#b033) | Google · [유용하고 신뢰할 수 있는 사용자 중심 콘텐츠](https://developers.google.com/search/docs/fundamentals/creating-helpful-content?hl=ko) | 직접 본문 확인 |
| [B034](../../research-blog/SOURCES.md#b034) | Google · [AI 기능 및 웹사이트](https://developers.google.com/search/docs/appearance/ai-features?hl=ko) | 직접 본문 확인 |
| [B035](../../research-blog/SOURCES.md#b035) | Google · [사이트 소유권 확인](https://support.google.com/webmasters/answer/9008080?hl=ko) | 직접 본문 확인 |
| [B037](../../research-blog/SOURCES.md#b037) | 공정위/국가법령정보센터 · [추천ㆍ보증 등에 관한 표시ㆍ광고 심사지침](https://www.law.go.kr/LSW/admRulInfoR.do?admRulSeq=2100000280130&chrClsCd=010201) | 직접 본문 확인 |
| [B038](../../research-blog/SOURCES.md#b038) | 국세청 · [SNS마켓 사업자 세무 안내](https://www.nts.go.kr/nts/cm/cntnts/cntntsView.do?cntntsId=7804&mi=2483) | 직접 본문 확인 |
| [B040](../../research-blog/SOURCES.md#b040) | OpenAI · [Prompt engineering](https://developers.openai.com/api/docs/guides/prompt-engineering) | 직접 본문 확인 |
| [B041](../../research-blog/SOURCES.md#b041) | Anthropic · [Prompt engineering overview](https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/overview) | 직접 본문 확인 |
| [B042](../../research-blog/SOURCES.md#b042) | Google · [Prompt design strategies](https://ai.google.dev/gemini-api/docs/prompting-strategies) | 직접 본문 확인 |
| [B046](../../research-blog/SOURCES.md#b046) | 네이버 · [웹 콘텐츠 스팸사례](https://searchadvisor.naver.com/guide/content-abusing) | 직접 본문 확인 |
| [B047](../../research-blog/SOURCES.md#b047) | 네이버 · [ONE 미지원 기능](https://help.naver.com/service/5593/contents/15545?lang=ko&osType=PC) | 직접 본문 확인 |
| [B048](../../research-blog/SOURCES.md#b048) | 네이버 · [글 발행 방법](https://help.naver.com/service/5593/contents/15541?lang=ko&osType=PC) | 직접 본문 확인 |
| [B049](../../research-blog/SOURCES.md#b049) | 네이버 · [크리에이터 가입 기준](https://help.naver.com/service/30027/contents/22952?lang=ko&osType=COMMONOS&ostype=commonos) | 직접 본문 확인 |
| [B050](../../research-blog/SOURCES.md#b050) | 뤼튼 · [뤼튼 고객센터](https://help.wrtn.ai/) | 직접 본문 확인·일부 검색 본문과 판본 차이 |
| [B051](../../research-blog/SOURCES.md#b051) | 뤼튼 · [뤼튼 이미지 제작](https://help.wrtn.ai/img_create) | 직접 본문 확인 |
| [B052](../../research-blog/SOURCES.md#b052) | 미리디 · [Pro 요금제 가이드](https://help.miricanvas.com/hc/ko/articles/48267019052057) | 직접 본문 확인 |
| [B053](../../research-blog/SOURCES.md#b053) | Google · [Google AI 한국 구독](https://gemini.google/kr/subscriptions?hl=ko) | 직접 기능 본문·Pro 금액 추출 누락 |
| [B054](../../research-blog/SOURCES.md#b054) | 네이버 · [키워드 도구 연관키워드 조회](https://ads.naver.com/help/faq/1406) | 직접 본문 확인·HTTP200 메뉴만 수신과 구별 |
| [B055](../../research-blog/SOURCES.md#b055) | 네이버 · [통합 검색어 트렌드](https://developers.naver.com/docs/serviceapi/datalab/search/search.md) | 직접 본문 확인·HTTP200 메뉴만 수신과 구별 |
| [B056](../../research-blog/SOURCES.md#b056) | Google · [FAQ about Google Trends data](https://support.google.com/trends/answer/4365533?hl=en) | 직접 본문 확인·HTTP200 메뉴만 수신과 구별 |
| [B057](../../research-blog/SOURCES.md#b057) | Google · [키워드 플래너 사용](https://support.google.com/google-ads/answer/7337243?hl=ko-KR) | 직접 본문 확인·HTTP200 메뉴만 수신과 구별 |
| [B058](../../research-blog/SOURCES.md#b058) | Google · [RPM 정의](https://support.google.com/adsense/answer/190515?hl=ko) | 직접 본문 확인 |
| [B059](../../research-blog/SOURCES.md#b059) | Google · [애드센스 계정 연령 요건](https://support.google.com/adsense/answer/14230?hl=ko) | 직접 본문 확인·자격요건 페이지와 상충 |
| [B068](../../research-blog/SOURCES.md#b068) | Google · [Blogger 맞춤 도메인 설정](https://support.google.com/blogger/answer/1233387?hl=ko) | 직접 본문 확인·HTTP200 메뉴만 수신과 구별 |
| [B069](../../research-blog/SOURCES.md#b069) | Google · [블로그 설정 관리](https://support.google.com/blogger/answer/9691230?hl=ko) | 직접 본문 확인·HTTP200 메뉴만 수신과 구별 |
| [B071](../../research-blog/SOURCES.md#b071) | 네이버 · [블로그 백업 안내](https://help.naver.com/service/5593/contents/15293?lang=ko&osType=COMMONOS) | 직접 본문 확인 |
| [B082](../../research-blog/SOURCES.md#b082) | 티스토리 공식(공지 시점별 카카오/AXZ) · [AdFit 신규 연동 신청 종료](https://notice.tistory.com/2701) | 직접 본문 확인 |
| [B083](../../research-blog/SOURCES.md#b083) | 카카오 · [AdFit 운영정책](https://adfit.kakao.com/web/html/use_kakao.html) | 직접 본문 확인 |
| [B084](../../research-blog/SOURCES.md#b084) | 티스토리 공식(공지 시점별 카카오/AXZ) · [AdFit 연동 승인 조건 변경](https://notice.tistory.com/m/2691) | 직접 본문 확인·종료 전 과거 조건 |
| [B085](../../research-blog/SOURCES.md#b085) | 네이버 · [회원 유형별 세금 정산](https://help.naver.com/service/30005/contents/17810?lang=ko&osType=COMMONOS) | 직접 본문 확인 |
| [B086](../../research-blog/SOURCES.md#b086) | 국세청 · [종합소득세 신고·납부](https://www.nts.go.kr/nts/cm/cntnts/cntntsView.do?cntntsId=7664) | 직접 본문 확인 |
| [B087](../../research-blog/SOURCES.md#b087) | Google · [Google 미국 세금 정보 제출](https://support.google.com/adsense/answer/2490070?hl=ko) | 직접 본문 확인 |
| [B091](../../research-blog/SOURCES.md#b091) | Automattic · [사이트 헤더 코드 추가](https://wordpress.com/support/adding-code-to-headers/) | 직접 본문 확인 |
| [B092](../../research-blog/SOURCES.md#b092) | 티스토리 공식(공지 시점별 카카오/AXZ) · [모바일 전면광고 제한](https://notice.tistory.com/2692) | 직접 본문 확인 |
| [B093](../../research-blog/SOURCES.md#b093) | 쿠팡 · [쿠팡 파트너스 최신 발견 이용가이드](https://partners.coupangcdn.com/partners-guide/partners-guide-20260917111657.pdf) | 직접 PDF 다운로드·81쪽 텍스트에서20·43~47·64쪽 확인 |
| [B094](../../research-blog/SOURCES.md#b094) | 네이버 · [블로그 C-RANK 소개](https://help.naver.com/service/5626/contents/22927?lang=ko&osType=COMMONOS) | 직접 본문 확인 |
| [B123](../../research-blog/SOURCES.md#b123) | 네이버 · [쇼핑커넥트 실적 인정 기준](https://help.naver.com/service/30027/contents/24106?lang=ko&osType=COMMONOS) | 직접 본문 확인 |
| [B124](../../research-blog/SOURCES.md#b124) | 네이버 · [쇼핑커넥트 수익 정산](https://help.naver.com/service/30027/contents/24108?lang=ko&osType=COMMONOS) | 직접 본문 확인 |
| [B133](../../research-blog/SOURCES.md#b133) | Google · [Blogger 백업·가져오기](https://support.google.com/blogger/answer/41387?hl=en) | 직접 본문 확인·Takeout/feed.atom |
| [B135](../../research-blog/SOURCES.md#b135) | 티스토리 공식(공지 시점별 카카오/AXZ) · [티스토리 크리에이터 운영 방식 개편](https://notice.tistory.com/2705) | 직접 본문 확인·2027예고 분리 |
| [B138](../../research-blog/SOURCES.md#b138) | 뤼튼 · [뤼튼 일부 기능 종료](https://help.wrtn.ai/notice_somend) | 직접 본문 확인 |
| [B140](../../research-blog/SOURCES.md#b140) | Perplexity · [Perplexity Terms of Service](https://www.perplexity.ai/hub/legal/terms-of-service) | 직접 약관 본문 확인·urllib 보완 |
| [B142](../../research-blog/SOURCES.md#b142) | 나라인포테크 · [바른한글 맞춤법·문법 검사기](https://www.nara-speller.co.kr/speller/) | 직접 입력UI 확인·이용약관/한도 미확인 |
| [B143](../../research-blog/SOURCES.md#b143) | Google · [고품질 리뷰 작성](https://developers.google.com/search/docs/specialty/ecommerce/write-high-quality-reviews?hl=ko) | 직접 본문 확인 |
| [B144](../../research-blog/SOURCES.md#b144) | Automattic · [WordPress.com REST API 시작](https://developer.wordpress.com/docs/api/getting-started/) | 직접 본문 확인 |
| [B148](../../research-blog/SOURCES.md#b148) | 법제처 · [공표된 저작물의 인용](https://www.easylaw.go.kr/CSP/CnpClsMainBtr.laf?ccfNo=3&cciNo=2&cnpClsNo=2&csmSeq=695) | 직접 본문 확인 |
| [B151](../../research-blog/SOURCES.md#b151) | 과기정통부 · [MSIT Releases Guidelines on Ensuring AI Transparency](https://www.msit.go.kr/eng/bbs/view.do?bbsSeqNo=42&mId=4&nttSeqNo=1215&sCode=eng) | 직접 본문 확인・urllib 보완 |
| [B152](../../research-blog/SOURCES.md#b152) | 국세청 · [원천징수 대상 사업소득](https://www.nts.go.kr/nts/cm/cntnts/cntntsView.do?cntntsId=7900&mi=6620) | 직접 본문 확인 |
| [B153](../../research-blog/SOURCES.md#b153) | 국세청 · [모두채움 종합소득세 안내](https://www.nts.go.kr/nts/cm/cntnts/cntntsView.do?cntntsId=238978&mi=40483) | 직접 본문 확인 |
| [B154](../../research-blog/SOURCES.md#b154) | 국세청 · [사업자등록 언제 어떻게](https://www.nts.go.kr/nts/na/ntt/selectNttInfo.do?nttSn=1396&mi=2448) | 직접 본문 확인 |
| [B155](../../research-blog/SOURCES.md#b155) | IRS · [About Form W-8 BEN](https://www.irs.gov/forms-pubs/about-form-w-8-ben) | 직접 본문 확인 |
| [B158](../../research-blog/SOURCES.md#b158) | 네이버 · [네이버 서비스 이용약관](https://policy.naver.com/rules/service.html) | 직접 본문 확인 |
| [B159](../../research-blog/SOURCES.md#b159) | 네이버 · [게시물 운영정책](https://policy.naver.com/policy/service_group.html) | 직접 본문 확인 |
| [B160](../../research-blog/SOURCES.md#b160) | 네이버 · [블로그 서비스 운영정책 개정 첨부](https://notice.naver.com/api/v1/file/download/123) | 직접 본문 확인·웹 도구 보완 |
| [B167](../../research-blog/SOURCES.md#b167) | 티스토리 공식(공지 시점별 카카오/AXZ) · [2024 가입 개선](https://notice.tistory.com/2672) | 직접 본문 확인 |
| [B170](../../research-blog/SOURCES.md#b170) | 티스토리 공식(공지 시점별 카카오/AXZ) · [글 저장·발행·예약](https://notice.tistory.com/m/2480) | 직접 본문 확인·現화면 실기 아님 |
| [B173](../../research-blog/SOURCES.md#b173) | 네이버 · [네이버 제공 서비스 웹마스터 도구 연동](https://help.naver.com/service/30010/contents/17597?osType=PC) | 직접 본문 확인·HTTP200 메뉴만 수신과 구별 |
| [B174](../../research-blog/SOURCES.md#b174) | 네이버 · [서치어드바이저 시작·소유확인](https://searchadvisor.naver.com/guide/seo-basic-intro?lang=ko) | 직접 본문 확인·HTTP200 메뉴만 수신과 구별 |
| [B176](../../research-blog/SOURCES.md#b176) | 네이버 · [RSS·사이트맵 제출](https://searchadvisor.naver.com/guide/request-feed?lang=ko) | 직접 본문 확인·HTTP200 메뉴만 수신과 구별 |
| [B177](../../research-blog/SOURCES.md#b177) | Google · [Search Console 속성 추가](https://support.google.com/webmasters/answer/34592?hl=ko) | 직접 본문 확인·HTTP200 메뉴만 수신과 구별 |
| [B178](../../research-blog/SOURCES.md#b178) | Google · [URL 검사 도구](https://support.google.com/webmasters/answer/9012289?hl=ko) | 직접 본문 확인·HTTP200 메뉴만 수신과 구별 |
| [B179](../../research-blog/SOURCES.md#b179) | Google · [애드센스 계정 만들기](https://support.google.com/adsense/answer/7402253?hl=ko) | 직접 본문 확인·HTTP200 메뉴만 수신과 구별 |
| [B180](../../research-blog/SOURCES.md#b180) | Google · [사이트 연결·검토 요청](https://support.google.com/adsense/answer/7584263?hl=ko) | 직접 본문 확인·HTTP200 메뉴만 수신과 구별 |
| [B181](../../research-blog/SOURCES.md#b181) | Google · [사이트 준비·승인 문제 해결](https://support.google.com/adsense/answer/81904?hl=ko) | 직접 본문 확인·HTTP200 메뉴만 수신과 구별 |
| [B183](../../research-blog/SOURCES.md#b183) | 티스토리 공식(공지 시점별 카카오/AXZ) · [티스토리 Search Console 플러그인](https://notice.tistory.com/2536) | 직접 본문 확인·HTTP200 메뉴만 수신과 구별 |
| [B184](../../research-blog/SOURCES.md#b184) | 티스토리 공식(공지 시점별 카카오/AXZ) · [자동 사이트맵](https://notice.tistory.com/2537) | 직접 본문 확인·HTTP200 메뉴만 수신과 구별 |
| [B186](../../research-blog/SOURCES.md#b186) | 미리디 · [미리캔버스 AI 서비스 이용약관](https://help.miricanvas.com/hc/ko/articles/31288096586649) | 직접 본문 확인·웹 도구 보완 |
| [B189](../../research-blog/SOURCES.md#b189) | 나라인포테크 · [바른한글 소개](https://nara-speller.co.kr/about) | 직접 본문 확인·웹 도구 보완 |
| [B200](../../research-blog/SOURCES.md#b200) | 티스토리/Daum 고객센터 · [데이터 백업 신청 방법](https://cs.daum.net/faq/service/2036/category/60785/detail/39646) | 직접 본문 확인 |
| [B201](../../research-blog/SOURCES.md#b201) | 티스토리/Daum 고객센터 · [개인 도메인 설정 오류 안내](https://cs.daum.net/faq/service/2036/category/60784/detail/39716) | 직접 본문 확인 |
| [B202](../../research-blog/SOURCES.md#b202) | 티스토리/Daum 고객센터 · [서비스 양도·개인정보 이전·약관 개정](https://cs.daum.net/notice/5135) | 직접 본문 확인 |

## 직접 재확인 실패·보류의 처리

- 미리캔버스AI약관·바른한글소개는 urllib403 뒤 웹 도구에서 본문을 확보했다. Canva 한국가격·바른한글구판은 urllib403 뒤 추가 웹 원문을 확보하지 못해 Hermes 근거로만 유지했다.
- 네이버 일부 도움말은200응답에도 본문 대신 메뉴만 나왔다. URL변형·다른공식문서로 보완하고 끝내 확보하지 못한 항목은 SOURCE에서 검색/Hermes/미확인 상태를 유지했다.
- 네이버2단계인증 상세 주소는 카테고리로 리디렉트되어 해당 상세 경로를 근거에서 제외했다. 구체 계정 화면 검수는 후속 확인이다.
- 저작권법 전체 페이지는 iframe만 확인되어 직접 확인 수에 넣지 않았다. 제28·37조 인용의 범위는 법제처 생활법령 본문으로 보완했다.
