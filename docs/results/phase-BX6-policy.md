# Phase BX6-policy — 독립 정책·안전 검토

검토일: **2026-10-28, 한국 기준**. 결론: **수정 후 가능**. 현재 상태로의 공개 승인은 보류한다. 아래 **차단 6건**을 해소하고 **수정 7건**을 반영한 뒤, 변경된 관문·산출물을 다시 검토해야 한다. 본 검토는 사이트·키트의 수정이나 실제 계정 게시·광고 승인·세무 신고를 수행한 결과가 아니다.

공정위 지침의 시행일·표시 위치, 품목별 규제의 큰 구분, 세금과 육아휴직급여의 확인 경로는 대체로 적절하다. 그러나 **건강 검토 대기 글과 기존 글 갱신의 무승인 예약**, **금지 광고·숨긴 표시의 승인 후 예약**, **미디어 메타데이터 검사 누락**이 재현됐다. 정상 샘플의 테스트 통과만으로 “위험 글은 어떤 설정에서도 자동 발행되지 않는다”는 요구를 충족했다고 볼 수 없다.

## 1. 범위·방법·집계

- `AGENTS.md`, `docs/DESIGN-blog-advanced.md` 6·8절과 1.1절, `docs/DESIGN-baby.md` 8절, `docs/STYLE-GUIDE.md`, `research-blog-advanced/{SOURCES,FACT-SHEET,SOURCE-CHECKS}.md`, `research-baby/BRIEFING.md` ④를 읽었다.
- `site-blog/advanced/` A0~A12·E2E **14장 전체**와 `blog-auto-kit/{gates,monetize,samples,content}/` **텍스트 34파일·래스터 2파일**을 검토했다. 발행 경로를 확인하기 위해 `core/`·`wordpress/`·관련 테스트도 읽었다. 공통 그림·시뮬레이터에 전달되는 본문 예시와 코드 발췌도 포함했다. 연결된 advanced.js·계산기/관문/표시/진행표 전용 JS 5개도 읽었다.
- 외부 법·정책·조건·금액 주장은 아래 목록의 **144개 검토 단위**로 추출했다. 같은 의미가 본문·FAQ·표·샘플에 반복되면 한 행에 위치를 모았다. 한 제도의 함께 적용되는 조건 묶음은 한 행이다. **문장 출현 횟수나 법 조항 개수라는 뜻이 아니다.** 가상 수입·모의 지표·설정값은 외부 사실로 세지 않고 별도 검증했다.
- **원문 대조 완료 139/144**: 일치 134, 원문으로 확인했지만 인용 연결을 보완해야 하는 항목 3, 현재 원문과 불일치 1, 의무 항목 누락 1. **부분 대조 2·확인 보류 3**은 완료 수에 넣지 않았다. 보류는 거짓으로 판정한 수가 아니다.
- 본문 각주 **BX 출처 89개**, 관문 해석에 필요한 모법/시행령/시행규칙 **3개**, 샘플의 **N 출처 14개**, 합계 **기존 출처 URL 106개**를 직접 요청했다. 웹 열람으로 보완한 결과 본문 수신 100, 해당 주장 일부만 확인 2, 원문 미확인 4다. HTTP 200의 제목·빈 JS 화면은 본문 확인으로 세지 않았다. 보완 근거 4항목은 5절에 별도로 적었다. **원문 수신 수는 주장 검증 수가 아니다.**
- 웹 도구와 `urllib`로 현행 안내·본문·부칙을 열고, PDF 6개는 본문을 추출해 읽었다. 기존 조사자의 “직접 확인” 표시는 이번 결과에 자동 승계하지 않았다. 정책 문서는 조회 시점의 내용이며 개별 계정 자격·제품 심의·실제 기관 접수는 시험하지 않았다.
- 실행·실험은 `/tmp/bx6-policy/`의 복사본·합성 자료만 사용했다. 테스트 중 실제 아이 정보·실제 광고주·실계정·유료 API를 쓰지 않았다. 저장소의 영구 산출물은 이 파일만이다. 다른 검토 작업자가 만드는 `phase-BX6-repro/` 등은 변경하지 않았다.

## 2. 공개 전 차단 6건

### B01. 건강 관문이 사람 검토로 판정해도 자동 예약된다

**위치:** `gates/checks.py:19`, `gates/risk.py:5`, `core/approval.py:18`, `wordpress/publish.py:30`.

**본문 원문:** A0 “건강·안전 … 항상 사람 승인. 자동 발행 금지”, A5 “건강·상업·경험·아이 사진이 있으면 자동 설정보다 사람 승인 규칙을 우선해요.”

**재현:** 일반 정보 글의 제목·설명을 그림책 정리로 두고, 본문에 `해열제에 관한 설명입니다.`를 추가했다. `risk_flags=[]`, HTML은 같은 마크다운에서 다시 생성했다. 실제 `evaluate → prepare_draft → publish_draft(mode='auto')` 경로에서 **H1 `review`, `human_resolvable=true`인데 `requires_human=false`**, 서버 상태 **`future`·승인 없음**으로 끝났다. 약 사용을 권하지 않는 설명 문장으로도 건강 분류와 발행 판정의 불일치를 확인할 수 있다.

**원인:** 건강 검사와 발행 위험 분류의 단어 집합이 다르다. `require_ready()`는 사람이 해결할 수 있는 `review`를 허용하고, 발행은 이 결과 대신 별도의 `requires_human()`만 본다. 미표시 아동 식별 문장 `가상 아이의 이름은 테스트봄이이고 병원은 가상병원입니다.`도 같은 일반 글에서 `pass → future`, 승인 없음이었다. C2의 `아이 실명:` 같은 고정 양식 밖의 표현은 놓친다.

**근거:** 심화 설계 1.1·6.1·6.4, BXF-091. 개인정보의 정의는 [개인정보 보호법 제2조](https://www.law.go.kr/LSW/lsInfoR.do?lsiSeq=283839&efYd=20260911)이며, 얼굴·실명 비공개는 이 프로젝트의 더 높은 보호 기준이다.

**고칠 동작/문장:** “건강·아이 정보 등 사람 검토 결과가 하나라도 있으면 자동 모드에서도 승인 대기예요. 분류를 확정하지 않은 글도 사람이 확인해요.” 발행 시 관문 결과를 같은 판정의 근거로 사용하고, 미분류 입력을 낮은 위험으로 간주하지 않아야 한다. 즉시 가능한 작은 조치는 이 경로의 자동 예약을 닫고 승인제를 유지하는 것이다. 단어 몇 개 추가만으로 모든 표현의 안전을 보장했다고 쓰면 안 된다.

### B02. 이미 공개된 글의 갱신을 자동 모드로 재예약할 수 있다

**위치:** `wordpress/prepare.py:78`, `wordpress/publish.py:30`, `gates/risk.py:10`.

**본문 원문:** A0 “기존 글 갱신 … 자동 탐지 + 사람 승인”, A11 “기존 글 갱신은 항상 사람 승인이에요.”

**재현:** 낮은 위험 글을 `auto`로 예약하고 mock 시계를 옮겨 `publish`를 확인했다. 같은 글의 본문을 수정해 HTML도 갱신하고 `prepare_draft()`를 다시 호출했다. `update_draft()`가 승인을 지운 뒤에도, `is_update`·갱신 위험 플래그를 사용자가 직접 넣지 않으면 **같은 post_id=1을 `auto`로 `future` 재예약**, `approval=null`이었다. 2026-10-28 신규 예약 → 10-30 공개 확인·수정·재준비·재예약으로 실행했다.

**원인:** 이미 서버에 존재하는 글을 갱신하는 사실이 위험 분류에 전달되지 않는다. JSON의 자가 선언에만 의존한다. 이전 승인이 있으면 내용 변경을 거부하는 경로는 있지만, **새 준비로 승인을 없앤 뒤 자동 모드**를 고르면 그 보호가 충분하지 않다.

**근거:** 설계 1.1의 “기존 글 갱신”, 8절의 내용 변경 후 재승인.

**고칠 동작/문장:** “기존 서버 글을 수정하면 서버 기록으로 갱신 글임을 판단하고, 최종본의 새 사람 승인 뒤에만 예약해요.” 갱신 이력은 `--prepare`·상태 재조회·재시도 후에도 보존해야 한다. 본문에 `is_update`를 적으라는 안내만 추가하는 것으로 닫히지 않는다.

### B03. 제품 규제 관문이 금지 문구를 놓치고 메타데이터 한 칸을 예외로 삼는다

**위치:** `gates/products.py:25`·`:31`, `gates/checks.py:87`, A5·A8·A12의 법적 금지 표.

**본문 원문:** A8 “법적 금지 내용은 사람 승인으로 풀지 않아요.”

**실행 결과:** 제품·분류·심의 자료 필드가 채워진 제휴 샘플을 다음처럼 바꾸고 실제 관문·초안·승인·예약 경로를 실행했다.

| 입력 | 실제 결과 | 요구되는 결과 |
|---|---|---|
| 의료기기, `comparison_only=true`, 본문과 human 경험 칸에 직접 사용 소감 | P5 차단 없음, 사람 승인 후 `future` | 체험담을 단순 비교 플래그로 면제하지 않음 |
| 화장품, “아토피피부염을 예방합니다.” | `pass`, 사람 승인 후 `future` | 의약품 오인 광고를 차단/자료 보류하고 문안을 재검토 |
| 건강기능식품, “감기를 예방합니다.” | `pass`, 사람 승인 후 `future` | 질병 예방·치료 오인 광고를 차단 |

기존 검사에는 ‘질병을 치료’ 등 몇 표현만 있고 **질병 예방**을 검사하지 않는다. 의료기기는 사용자 체험담의 실제 유무보다 `comparison_only`를 분기로 쓴다.

**근거:** [의료기기 시행규칙 별표7 제8호](https://www.law.go.kr/LSW/flDownload.do?gubun=&flSeq=166537359&bylClsCd=110201), [현행 식품표시광고법 제8조](https://www.law.go.kr/LSW/lsInfoR.do?lsiSeq=269957&efYd=20250919), [화장품법 제13조 대조 판본](https://www.law.go.kr/LSW/lsInfoR.do?lsiSeq=270323&efYd=20260402). 화장품의 허용된 기능성 설명과 질병 자체의 예방을 구별해야 한다.

**고칠 동작/문장:** “제품의 분류·허용 문안과 실제 본문·경험을 함께 대조해요. ‘자료 비교’ 표시나 사람 승인만으로 금지 체험담·질병 예방 광고를 통과시키지 않아요.” 규제 품목에서 문안 범위를 확정하지 못하면 자료 보류로 닫아야 한다. 모든 건강 관련 표현을 법적 금지로 묶는 수정도 피한다.

### B04. 표시 위치 검사만으로 불충분한 관계·숨긴 표시가 승인된다

**위치:** `gates/checks.py:71`, `gates/body.py:consistent`, `monetize/affiliate.py:47`, A5·A8·A9·A12.

**본문 원문:** A5 “키트는 실제 받은 물품·현금·수수료 관계를 첫 문단에서 확인해요.”

**재현 1:** 제휴 샘플 첫 문단을 `제휴 활동 안내입니다.`로 바꾸고 원문·HTML을 일치시켰다. 수수료를 받는다는 공개 없이 **`pass → 사람 승인 → future`**였다. 현재 검사는 `수수료` 또는 `제휴`가 있는지만 본다.

**재현 2:** 수수료 표시가 있는 첫 `<p>`를 `<p style="display:none">`으로 바꾸었다. 텍스트는 같아 `content.consistency`도 통과했고 **`pass → 사람 승인 → future`**였다. 보이는 표시인지 확인하지 않는다.

**복합 관계 점검:** 여러 sponsor 관계에 같은 단어 하나를 재사용하며 실제 각 관계의 `details`를 확인하지 않는다. `prepare_affiliate()`도 program이 쿠팡이면 kind와 무관하게 수수료 문장을 선택한다. 쿠팡 제휴 외의 제품 제공·광고비까지 받은 사실을 그 문장만으로 공개할 수 없다. 관계 메타데이터가 비어 있으면 상업 유형이어도 D1/D2 반복문이 돌지 않는다. 이 부분은 코드 확인이며 위 두 실행 사례와 구분한다.

**근거:** [현행 공정위 지침 Ⅴ.6](https://www.law.go.kr/LSW/admRulInfoR.do?admRulSeq=2100000280130&chrClsCd=010201), [공정위 Q&A PDF](https://www.korea.kr/common/download.do?fileId=198296345&tblKey=GMN), [쿠팡 가이드 인쇄 25쪽](https://partners.coupangcdn.com/partners-guide/partners-guide-20260917111657.pdf). 제목/첫부분뿐 아니라 구별·인식 가능한 형식과 실제 경제관계 내용이 중요하다.

**고칠 동작/문장:** “첫부분에서 실제 수수료·제품 제공·광고비 관계를 각각 밝히고 모바일 화면에서 보이는지 확인해요.” 표시 유형·관계 누락을 자료 보류/차단으로 연결하고, 임의 HTML의 숨김·스타일을 텍스트 일치만으로 승인하지 않아야 한다. 원고 문구 생성도 관계별로 해야 한다.

### B05. 공개 가능한 미디어에서 EXIF·위치정보가 누락된다

**위치:** `gates/checks.py:62`, `gates/privacy_exif.py:31`, `wordpress/prepare.py:remote_assets`, A5·A12의 메타데이터 제거 안내.

**본문 원문:** A5 “원본과 변환본에서 위치정보를 제거하고 다시 확인하세요.”

**실행 결과:**

- 실제 PNG의 `eXIf`에 합성 Make/설명 정보를 넣었다. 독립 디코더는 EXIF를 읽지만 관문은 **`pass`**, `requires_human=false`였다.
- 제공 JPEG의 바이트를 그대로 두고 이름만 `renamed.png`로 바꾸면 관문은 **`pass`**였다. 실제 형식은 JPEG였다.
- JPEG APP1 EXIF를 지우는 함수는 동작했지만 별도 APP1 XMP의 합성 `GPSLatitude`는 남았고 `inspect_exif()`는 빈 목록이었다.
- 업로드 함수는 현재 바이트를 그대로 올린다. 자동 제거가 발행 경로에 통합되어 있다고 볼 수 없다. 정상 확장자의 EXIF JPEG를 관문이 차단하는 것은 확인했다.

**근거:** 설계 6.4, BXF-054·055, [Apple의 사진 위치 메타데이터 안내](https://support.apple.com/ko-kr/guide/personal-safety/ips0d7a5df82/1.0/web/1.0). 함수 이름의 EXIF 제거와 모든 위치정보 제거는 같은 약속이 아니다.

**고칠 동작/문장:** “공개할 파일의 실제 형식을 확인하고 EXIF·위치 메타데이터를 제거한 공개용 사본을 다시 검사해요. 검사하지 못한 형식은 보류해요.” 최소한 확장자만으로 검사를 생략하지 않아야 하며, PNG 등 허용 형식을 검사하거나 검증되지 않은 형식의 업로드를 막아야 한다. XMP를 그대로 두고 “위치정보 제거 완료”라고 표시하지 않는다.

### B06. 약 이름 전면 금지·본문의 응급 문구 강제 규칙이 구현과 다르다

**위치:** `gates/checks.py:19`·`:23`·`:27`, `gates/risk.py:HEALTH`, A5 건강 규칙.

**본문 원문:** A5 “약 이름·용량이나 ‘집에서 지켜봐도 된다’는 판정이 있으면 차단해요.”

**재현:**

1. 일반 글 본문에 `아스피린에 관한 설명입니다.`를 넣으면 **`pass → auto future`, 승인 없음**이었다. 몇 약 이름을 열거한 H3 검사로 DESIGN-baby의 약 이름 전면 제외를 충족했다고 할 수 없다.
2. 일반 제목·설명의 본문에 `아기 발열에 관한 설명입니다.`를 넣으면 H1만 생긴다. `emergency_topics=[]`이면 **H4 공통 문구 누락 차단이 없고 사람 승인 후 `future`**였다. 응급 주제 자동 추론은 제목·설명만 읽는다.
3. 숫자 약 용량 문장은 N1 출처 검사에 막힐 수 있었지만, 이것을 약 이름/용량 안전 관문 성공으로 세지 않았다. 어떤 관문에서 어떤 이유로 막았는지를 구별했다.

**근거:** `DESIGN-baby.md` 8.3·8.4, 심화 설계 6.1. 샘플 응급 문구 자체는 BabyBook과 **10/10 완전 일치**한다. 잘못된 원문을 고치는 문제가 아니라 필요한 글에 그 문구를 강제하는 범위의 문제다.

**고칠 동작/문장:** “건강 주제는 본문까지 분류하고, 약 이름·용량을 제외한 원고와 필요한 공통 응급 문구를 확인한 뒤 승인해요.” 검증되지 않은 건강 문안을 일반 자동 발행으로 보내지 않아야 한다. 검사 범위를 넓힌 뒤 본문의 전면 차단 표현도 실제 보장 수준에 맞춰야 한다.

## 3. 수정 7건

| ID | 위치·현재 원문/동작 | 원문 대조·문제 | 고칠 문장/조치 |
|---|---|---|---|
| R01 | A7 확인할 점, `monetize/ads.py:26`: “19세와 … 18세가 달라요” | 10-28 직접 열람한 [자격 안내](https://support.google.com/adsense/answer/9724?hl=ko)와 [연령 안내](https://support.google.com/adsense/answer/14230?hl=ko) 모두 **만19세**. 기존 BXF-018의 현재 상충 설명을 재현하지 못했다. | “2026년 10월 한국어 안내 두 곳은 만19세 이상으로 안내해요. 신청 시 본인 적용 약관도 확인하세요.” 생성 점검표와 조사 사실표를 함께 갱신할 것. 과거에 왜 달랐는지는 추정하지 않음. |
| R02 | A2 처리방침 표/발췌, `monetize/pages.py:12`: 목적·기간·파기·이메일 위주 | [법30조](https://www.law.go.kr/LSW/lsInfoR.do?lsiSeq=283839&efYd=20260911)와 [시행령31조](https://www.law.go.kr/LSW/lsLinkCommonInfo.do?lsJoLnkSeq=1029331787)의 **안전성 확보조치**, 책임자 성명/부서와 연락처, 법정대리인 권리, 해당 시 민감정보 공개 선택·가명처리·국외이전 세부 등이 체크리스트에 충분히 드러나지 않는다. 현재 미연결 예제라는 설명은 적절하다. | “실제 처리 전 법30조·시행령31조의 필수 항목을 채워요. 안전조치·권리행사·책임자/연락처도 넣고, 위탁·제3자 제공·국외이전·자동수집 등 해당 항목은 실제 흐름으로 작성하세요.” 빈 양식을 법 준수 완성본으로 제공하지 않음. |
| R03 | `gates/products.py:20`·`:41`: `'리콜 확인'` 포함 시 block, 대부분 block은 법적 금지 | **“리콜 확인 결과 없음”도 리콜 확정으로 오판**했다. 비체험 의료기기 자료 소개도 `comparison_only=false`라 P5 법적 금지로 묶는다. `영아용 조제식` 문자열만으로 법상 조제유류인지 확정하는 것도 범위를 넘는다. | 리콜의 확인 절차와 실제 회수 대상을 별도 값으로 관리. P3의 BXF-097(품목 적용범위), P5의 BXF-047(심의 범위) 등 근거 ID도 실제 판정 사유와 맞출 것. 규제 분류·용도를 확인하지 못하면 **자료 보류**, 더 보수적으로 거절한다면 **프로젝트 거절**. “리콜 대상 확인 여부와 제품 분류 근거를 확인한 뒤 판정해요.” |
| R04 | `samples/fake-exif.jpg`, `samples/make_images.py:JPEG_BASE` | APP1 제거 전후 모두 Pillow 엄격 디코딩에서 **`broken data stream when reading image file`**. EXIF 구조는 읽히지만 정상 사진 시연 파일로 검증됐다고 할 수 없다. | 합성 그림을 정상 JPEG로 인코딩하고 같은 가짜 EXIF를 삽입. “원본·제거본이 모두 정상으로 열리고, 제거본에서 Make·GPS가 사라짐을 확인하세요.” 4절의 정상 합성 파일 시험을 회귀 조건으로 사용. |
| R05 | A7 BX026, A5·A8·A9·A12 BX078, A3 BX091, A4 BX111 각주 | BX026·BX078은 직접 요청 404, BX091은 TLS 실패, BX111은 HTTP200이나 JS 제목뿐이다. 기존 확인 기록만으로 현행 본문 재확인 완료로 세지 않았다. | 광고 차단은 [현재 공식 안내](https://support.google.com/adsense/answer/164131), 안전수면은 현재 직접 읽은 BX086 등 작동하는 원문으로 연결. 접종 첨부·레뷰 범위는 “공식 최신 안내에서 확인 전 보류”를 유지하고 접근 가능한 공식 원문을 확보. 원문 실패를 내용 폐지로 단정하지 않음. |
| R06 | A2 확인할 점: “플러그인 안내와 가격 FAQ는 문구가 달라요” | BX008은 모든 유료 플랜 플러그인 지원. BX010의 이번 응답도 유료 Personal 등에 plugin installation을 안내하지만 한국어 FAQ의 기존 상충 구절은 확인되지 않았다. 카페24 BX015의 가격은 확인했으나 추가 플러그인·SSH·FTP 미지원은 이번 수신 본문에서 재확인하지 못했다. | “선택할 플랜의 코드 삽입·광고·플러그인·REST·복구 지원을 구매 전에 확인해요.” 현행 상충/미지원 사실을 유지하려면 해당 문구가 있는 공식 본문·언어·조회일을 붙일 것. 확인 못 한 제한을 반대로 ‘지원’으로 바꾸지 않음. |
| R07 | A12 종합소득세 행의 BX053 각주 | 문장의 “통상 다음 해 5월 1~31일”은 [소득세법70조](https://www.law.go.kr/lsLinkCommonInfo.do?chrClsCd=010202&lsJoLnkSeq=1032883919)와 맞는다. 그러나 BX053은 **2025귀속·2026-06-01까지 신고**인 특정 연도 안내여서 2027년 일반 기한의 직접 근거로 부정확하다. | 일반 기한은 제70조, 해당 연도 실제 기한은 국세청 연간 안내를 인용. “통상 다음 해 5월이며, 신고 예외·휴일에 따른 실제 마감일과 본인 신고 여부는 그해 국세청 안내에서 확인하세요.” 세금·급여에 공통 면제선이나 일괄 세율을 만들지 않는 현재 설명은 유지. |

## 4. 실행 검증·아이 사생활

### 4.1 기존 검사와 추가 반례

깨끗한 `/tmp/bx6-policy/kit` 복사본에서 Python **3.11.15**로 실행했다. 원본 코드에 테스트용 monkeypatch를 넣거나 관문 함수를 대체하지 않은 추가 실험을 별도로 수행했다. 기존 테스트 자체가 사용하는 외부 호출 모킹은 그 테스트의 방식 그대로다.

```text
/tmp/bx5-tools/bin/python -m pytest -q -p no:cacheprovider
124 passed, 38 subtests passed in 7.12s
```

| 검증 | 실제 결과 | 한계/판정 |
|---|---|---|
| approval/auto × health/commercial/affiliate/sponsor/child_photo/experience/existing_update 명시 플래그 14조합 | 전부 무승인 발행 거부 | 플래그가 올바르게 붙은 경우의 결과. B01·B02의 누락 경로를 반증하지 않음 |
| `play.risk_flags=[]` | 제목·본문의 터미타임으로 사람 검토 유지 | 원래 샘플에서만 확인한 긍정 사례 |
| 계약 미확인 AI 생성, 광고주 확인 없이 협찬 승인 | 기존 테스트의 거부 검사 통과 | 사용자 입력·외부 약관 진위까지 자동 확인한다는 뜻 아님 |
| 승인 후 원고·링크·계약·로컬/원격 미디어·서버 분류 변경 | 기존 테스트에서 예약 회수·승인 무효화 확인 | B02처럼 prepare로 지운 승인 뒤 auto 재예약은 별도 반례 |
| 생성 응답 유실 후 slug 조회, 0개/복수 결과, 예약 응답 유실·원격 변경 | 기존 안전/복구 테스트 통과 | 실제 WordPress에서 네트워크 장애를 일으킨 것은 아님 |
| 동시에 예약·상한 초과·중복 글 | 공유 상태 잠금 관련 기존 검사 통과 | 상태를 따로 복사하거나 삭제하는 운영은 보호 범위 밖 |
| 사후 확인 등 허용되지 않은 publishing mode | 설정 검증에서 거부 | 허용 모드는 approval/auto. local/live의 발행 함수도 같은 승인 경로 사용(코드 확인), 실제 외부 연결은 미실행 |
| `run --sample`의 가상 자동 승인 | mock/info 전용으로 제한 | 실서비스 자동 승인 도구로 설명하지 않은 현재 본문은 적절 |
| B01~B06 반례 | 별도 mock REST를 통해 실제 future 예약까지 재현 | 법적/의학적 적정성을 일반 테스트 성공으로 대체하지 않음 |

공통 반례 입력은 `load_sample('info')`의 title/description/markdown을 `그림책 정리`/`책 고르는 기준`/단순 소제목·설명으로 바꾸고, HTML은 `content.markdown.render()`로 재생성한 문서다. 출처·작성자·미디어 등 필수 칸은 남겼다. 각 실험은 새 `Store`와 복사한 샘플 폴더를 쓰며, `running_server(port=0)` → `Client` → `prepare_draft` → 필요한 경우 `approve_document` → `publish_draft(mode='auto')` 순서다. 승인 생략 여부는 로컬 `posts.approval`과 서버 `status`로 확인했다. 따라서 HTML 불일치나 출처 필드 삭제 때문에 중간에서 실패한 사례를 발행 성공으로 세지 않았다.

### 4.2 CLI 명령 순서 재현

두 별도 복사본에서 `[wordpress] mode="mock"`, `[publishing] mode="auto"`로 실행했다. `draft --sample info` 뒤 생성 JSON의 제목/설명을 그림책 정리로 바꾸고 단순 본문과 같은 HTML을 넣었다. 건강 사례에는 위 B01 문장 한 줄을 더했다. **아래 과정에는 `gate --approve`가 없다.**

```text
# 건강 사례
python blog.py gate --sample info
✔ 통과: 자동 검사 완료 · 사람 검토 대기
python blog.py publish --sample info --prepare
✔ 통과: WordPress post_id=1 · draft
python blog.py publish --sample info
✔ 통과: WordPress post_id=1 · future

# 별도의 일반 글: 최초 예약 뒤 공개 상태를 확인하고 본문·HTML을 수정
python blog.py status --sample info --advance-days 2
✔ 통과: 서버 상태 재조회
# status.json에서 publish 확인 후, 내용 수정 → 재준비 → 무승인 재예약
python blog.py publish --sample info --prepare --today 2026-10-30
✔ 통과: WordPress post_id=1 · draft
python blog.py publish --sample info --today 2026-10-30
✔ 통과: WordPress post_id=1 · future
```

두 사례의 모든 명령이 exit0으로 끝났다. 함수 직접 호출 반례와 실제 CLI 경로가 같은 결과임을 확인했다. 실제 블로그에는 연결하지 않았다.

### 4.3 EXIF 시연

시연용 **가짜 제조사 FAKE·좌표 0,0**만 사용했다. 실제 사람의 위치가 아니다.

| 파일/상태 | 바이트 | 함수 검사 | 독립 EXIF 판독 | 이미지 디코딩 |
|---|---:|---|---|---|
| 저장소 `fake-exif.jpg` | 673 | EXIF 있음 | Make=FAKE, GPS N/E 0,0 | 실패 |
| `strip_exif()` 출력 | 517 | EXIF 없음 | Make 없음·GPS 없음 | 실패 |
| 새 정상 합성 JPEG + 같은 EXIF | 788 | EXIF 있음 | Make=FAKE·GPS 있음 | 정상 16×16 |
| 새 정상 합성 JPEG 제거본 | 632 | EXIF 없음 | Make 없음·GPS 없음 | 정상 16×16 |

원본 SHA256 `f4bc6651811b13ade0922ccb78c969d66168706ab0d072faa5ac4f3c1f075f44`, 제공 파일 제거본 `6efab2e180d3b541375823c7ae5826038db29293e8a8b6d7ed09b7745b44b15a`. 새 정상 합성 파일 `246ccb984783e59f4b17648987d83d315e81a5e2c2ce12b52c8bed8aa3b6070a`, 제거본 `f88d9b3f28949ffd8e03f0882312deb1391cc89f70e3032419c481ff451fc18f`.

제거 함수의 기본 재현법(키트 복사본에서 실행, 출력도 임시 경로):

```python
from pathlib import Path
from gates.privacy_exif import inspect_exif, strip_exif
src = Path('samples/fake-exif.jpg').read_bytes()
clean = strip_exif(src)
Path('/tmp/bx6-clean.jpg').write_bytes(clean)
print(len(src), len(clean), inspect_exif(src), inspect_exif(clean))
# 673 517 ['EXIF 위치·기기 정보 확인 필요'] []
```

독립 판독에는 임시 폴더에 설치한 Pillow를 썼고 `Image.open(...).getexif()`와 `load()`를 각각 실행했다. 검토 대상 키트의 의존성은 변경하지 않았다. **EXIF 제거 기능의 좁은 성공**, **제공 시연 이미지의 디코딩 실패**, **공개 미디어 전체의 개인정보 제거 실패**를 구분한다.

### 4.4 샘플·그림·미디어킷·보고서

- 샘플 네 글과 JSON·사람 메모에는 가상 인물·가상 제품임을 표시한다. 실제 아이 실명·정확한 생일·기관·생활 위치·아이 사진은 발견하지 못했다. PNG·SVG는 책꽂이 도형이며 PNG를 실제로 열어 확인했다. 14장에는 외부 아이 사진을 불러오는 `<img>/<image>`가 없고 도식·표·모바일 글 예시를 사용한다.
- 미디어킷·광고주 보고서·tax/ledger 내보내기는 집계·가상 연락처·가상 거래만 담는다. 방문120·검색클릭20·광고 예상0.12달러는 **모의** 표시가 있다. 성과·단가·실수익 근거로 쓰지 않도록 한 본문은 적절하다.
- 문의 양식은 disabled·전송 미연결이고 30일은 법정 기간이 아닌 예시다. 아이 건강·생일·주소를 기본 필수로 요구하지 않는 안내는 적절하다. 실제 수집 연결 전 R02를 해결해야 한다.
- `samples/emergency.json`의 **10문구 모두** `site-baby/assets/emergency-data.js`와 `research-baby/BRIEFING.md` ④에 문자열 그대로 존재했다. 발열·호흡/반응·먹지 못함·황달·위험 구토·배꼽·부모 위기·저체온·울음·발진이다. 상태/신호가 모두 함께 있어야 한다는 완화는 없다. NHS는 국외임을 표시한다. 응급 문구에서 약 이름·용량·“38℃ 미만이면 안전” 판정은 발견하지 못했다.
- 터미타임 샘플은 깨어 있음·보호자 관찰·불편하면 중단·소아과 확인으로 연결하고 WHO 국외 출처를 표시한다. “다섯 놀이”의 구성은 편집 제안이지 WHO가 똑같이 제시한 다섯 가지 공식 처방으로 쓰면 안 된다.

## 5. 원문 대조에서 확인한 적용 경계

1. **공정위 표시:** 시행2026-06-01·예규499호·Ⅴ.6이 맞다. 문자형의 제목/첫부분, 본문과 구별되는 인식 가능성, 실제 경제관계, 사진형의 예외를 함께 읽었다. 현재 원고의 큰 설명은 맞지만 B04의 코드가 그 설명을 보장하지 못한다. 사진 내 표시를 모든 블로그 삽화의 의무로 확대하면 안 된다.
2. **조제유류:** 별표6의 정의·광고/판촉 금지·법정 표시사항 인터넷 게시 예외를 읽었다. 무료/저가 공급, 체험단, 제조사 연결 후기 등의 판매촉진을 금지하는 근거가 있으며 비대가 양육기록 전부·젖병 전부를 금지하는 근거로 확장하지 않은 본문은 적절하다. 실제 유류 여부와 판매촉진성을 분류할 수 없으면 보류한다.
3. **의료기기:** 별표7 제8호는 체험담 광고 금지다. 자율심의 여부와 금지 체험담 여부는 다른 문제다. 시행령의 **일평균 이용자10만명**은 해당 SNS 광고매체 기준이며 개인 블로그 방문자 수의 일괄 면제선이 아니다. 현재 본문은 이 오해를 만들지 않지만 B03의 코드가 비교 플래그로 금지 범위를 줄인다.
4. **화장품:** 현행 의약품 오인·허위 광고 금지, 책임판매업자의 영유아 제품별 안전자료와 블로거의 확인 역할을 구별한다. 최신 통합 화면에 AI 전문가 오인 금지 조문이 보여도 법률21709호 부칙(공포 후6개월)을 함께 읽어 **11-27 시행 예정**으로 구분한 원고는 적절하다.
5. **건강기능식품·어린이제품:** 질병 예방·치료 오인 금지와 자율심의, 허용 기능·대상 연령을 함께 확인해야 한다. 어린이제품의 세 안전 절차, 제외 품목, 공급자적합성 자료 입증과 검색 결과 부재를 구별한 본문은 적절하다. 리콜을 확인했다는 글자만으로 법적 위반 확정을 내리는 R03은 고쳐야 한다.
6. **AdSense·쿠팡:** 승인 글 수·방문자·운영일을 새로 만들지 않았다. 광고→제휴→협찬도 학습 순서임을 명시한다. 쿠팡의 **15만원은 판매금액·채널검토 시작**이고 API·정산의 최종승인 단계와 구별한 설명, 권장 수수료 문장은 공식 PDF와 맞는다. PDF 표지는 **2024.12**이며 파일명20260917을 새 정책 시행일로 쓰지 않은 점도 적절하다. 실제 API 쿼터·가격 캐시 조건은 확인 보류, live 함수는 명시적으로 비활성이다.
7. **세금·육아휴직급여:** 이름만 보고 기타소득·일괄3.3%·현물 비과세로 판단하지 않고 126/관할 세무서에 실제 계약을 제시하도록 한다. 휴직급여 취업 신고의 **주15시간 또는 월150만원**은 원문과 맞고, 매출·소비자가격·세후입금에 직접 대입하지 않으며 고용센터/1350 경로를 준다. 그 기준 미만이면 무조건 신고 불필요·급여 유지라고 단정하지 않았다. R07은 세금 원칙 자체보다 인용 연결의 수정이다.

새로 보완한 근거 4항목(연결된 교차 확인 안내도 2026-10-28 본문 직접 열람):

| 보완 ID | 원문 | 이번 검토에서 사용한 부분 |
|---|---|---|
| V01 | [개인정보 보호법 시행령31조](https://www.law.go.kr/LSW/lsLinkCommonInfo.do?lsJoLnkSeq=1029331787) | 시행2026-09-11, 처리 항목·국외이전·안전조치·해외 직접수집 시 국가명, 지속 게시 |
| V02 | [소득세법70조](https://www.law.go.kr/lsLinkCommonInfo.do?chrClsCd=010202&lsJoLnkSeq=1032883919) | 시행2026-07-01, 일반 확정신고 기한 |
| V03 | [AdSense 민감 카테고리 차단](https://support.google.com/adsense/answer/164131) | 현재 작동하는 공식 세부 안내. [차단 기능 전체 안내](https://support.google.com/adsense/answer/180609?hl=ko)에서도 연결 확인 |
| V04 | [Google 게시자 정책](https://support.google.com/adsense/answer/10502938?hl=ko) | 개인정보 보호 공개, Google 사용의 수집·공유·사용·쿠키/IP 고지, 아동 대상 처리·맞춤광고 제한 |

## 6. 주장 추출·대조 목록

A0~A12는 `site-blog/advanced/00-start.html`~`12-policy.html`의 해당 장이다. `samples/`, `content/`, `monetize/`는 `blog-auto-kit/` 안의 경로다. 각 BX/N ID의 **원문 URL과 이번 열람 결과**는 다음 절에 있다. “근거보완”은 문장이 틀렸다는 뜻이 아니라 현재 각주 실패/범위 부족을 다른 공식 원문으로 보완한 항목이다. “확인보류”의 live·생성 중지 권고는 유지한다.

### 환경·요금

| 주장 ID | 위치 | 추출한 주장 | 각주/근거 | 대조 결과 |
|---|---|---|---|---|
| C001 | A1,A2 | WordPress 7.1.3 및 고정한 공식 이미지 태그가 존재한다. | BX001,BX002 | 일치 |
| C002 | A1,A2,A6 | 설치형 WordPress의 앱 비밀번호는 사용자 프로필에서 발급·폐기한다. | BX003 | 일치 |
| C003 | A2,A6 | 운영 연결은 HTTPS·사용자 권한·Authorization 전달을 확인한다. | BX003 | 일치 |
| C004 | A2,A6 | 설치형 WordPress는 /wp-json/wp/v2 REST 경로를 사용한다. | BX004 | 일치 |
| C005 | A2 | WordPress.com은 서비스 전용 API와 OAuth 인증을 구별한다. | BX096 | 일치 |
| C006 | A2 | WordPress.com 플러그인·외부 광고·WordAds 조건은 각각 확인한다. | BX008,BX009,BX097 | 일치 |
| C007 | A2 | 현재 플러그인 안내와 한국어 가격 FAQ가 서로 다르다. | BX008,BX010 | 부분 |
| C008 | A2 | 네이버 글쓰기 Open API는 종료됐다. | BX013 | 일치 |
| C009 | A2 | 티스토리 Open API는 종료됐다. | BX014 | 일치 |
| C010 | A0,A2 | 카페24 해당 스타트업 월 500원·설치 5,000원은 VAT 포함이다. | BX015 | 일치 |
| C011 | A0,A2 | 해당 카페24 상품은 추가 플러그인·SSH·FTP를 지원하지 않는다. | BX015 | 부분 |
| C012 | A0 | Hostinger Premium 공개 예: 48개월 119.52달러 선납·갱신 10.99달러/월이다. | BX016 | 일치 |
| C013 | A0 | 가비아 .com 정가는 10월 24,000원/년·11월부터 25,000원/년, VAT 별도다. | BX019 | 일치 |
| C014 | A0,A4 | OpenAI API 요금은 ChatGPT 구독과 구별한다. | BX071 | 일치 |
| C015 | A4 | gpt-6-luna Standard 단문·캐시 없음 입력/출력은 100만 토큰당 $0.10/$0.50다. | BX071 | 일치 |
| C016 | A4 | Structured Outputs는 Responses text.format의 json_schema·strict를 사용한다. | BX072 | 일치 |
| C017 | A4 | 구조화 출력의 스키마 준수는 사실 정확성을 보장하지 않는다. | BX072 | 일치 |
| C018 | A4,A11 | 공급자의 지출 알림과 강제 한도는 다르며 강제 적용에도 전파 지연이 있다. | BX073 | 일치 |
| C019 | A4 | 현재 모델 ID·가격·지원 종료는 공급자 모델/종료 문서에서 확인한다. | BX071,BX074 | 일치 |

### 발행·수집

| 주장 ID | 위치 | 추출한 주장 | 각주/근거 | 대조 결과 |
|---|---|---|---|---|
| C020 | A6 | WordPress draft/future/publish는 초안·예약·공개 상태다. | BX004 | 일치 |
| C021 | A6 | date는 사이트 시간대, date_gmt는 UTC다. | BX004 | 일치 |
| C022 | A6 | 이미지는 /media 업로드 반환 ID를 featured_media에 연결한다. | BX004,BX005 | 일치 |
| C023 | A6 | 글의 카테고리·태그는 ID 배열로 연결한다. | BX004,BX006,BX007 | 일치 |
| C024 | A6,A9,A11,E2E | WP-Cron은 방문 시 기한 작업을 실행하므로 예약은 정각 공개 보장이 아니다. | BX127 | 일치 |
| C025 | A6 | Blogger 공개 읽기 API 키와 쓰기 OAuth는 다르다. | BX011 | 일치 |
| C026 | A6 | Blogger 초안 isDraft와 예약 publishDate는 다른 호출이다. | BX011,BX012 | 일치 |
| C027 | A6 | Blogger AdSense 신청·연결은 수익 메뉴의 별도 단계다. | BX095 | 일치 |
| C028 | A10 | GA4 activeUsers·sessions·screenPageViews는 사용자·세션·조회로 단위가 다르다. | BX058 | 일치 |
| C029 | A10 | GA4 engagementRate는 참여 세션/전체 세션이다. | BX058 | 일치 |
| C030 | A10 | GSC impressions·clicks·ctr·position은 검색 노출·클릭·클릭률·평균순위다. | BX059 | 일치 |
| C031 | A10 | GA4 방문과 GSC 검색 클릭을 같은 수로 맞출 필요가 없다. | BX058,BX059 | 일치 |
| C032 | A10 | 사용자 수를 일별·페이지별로 단순 합산하면 중복될 수 있다. | BX058 | 일치 |
| C033 | A10 | GA4는 사용자 OAuth/서비스 계정 인증과 속성 권한을 따로 준비한다. | BX062 | 일치 |
| C034 | A10 | GSC도 요청 신원에 해당 사이트 권한이 있어야 한다. | BX059 | 일치 |
| C035 | A7,A10 | AdSense 개인 보고서는 사용자 OAuth·adsense.readonly 등과 기간·통화·시간대를 쓴다. | BX063 | 일치 |
| C036 | A10 | GA4는 속성 시간대, GSC 일 단위 날짜는 PT다. | BX058,BX059 | 일치 |
| C037 | A10 | GSC는 통상 2~3일 지연되며 빈 행이 곧 방문 0은 아니다. | BX116 | 일치 |
| C038 | A10 | GSC dataState=final은 최종 데이터를 요청한다. | BX059 | 일치 |
| C039 | A10 | GSC rowLimit 기본 1,000·최대 25,000, startRow 기본 0이다. | BX059 | 일치 |
| C040 | A10 | GSC 순회에도 일/검색유형당 50,000 상위행 한계가 있다. | BX116 | 일치 |
| C041 | A10 | GA4 표준 Core 속성당 하루 200,000·시간 40,000·프로젝트/속성/시간 14,000토큰이다. | BX057 | 일치 |
| C042 | A10 | GA4 표준 Core 속성당 동시요청 10·프로젝트/속성/시간 서버 오류 10이다. | BX057 | 일치 |
| C043 | A10 | GA4 토큰은 요청 건수가 아니며 returnPropertyQuota로 잔여 한도를 확인한다. | BX057 | 일치 |
| C044 | A10 | GSC 검색분석은 사이트/사용자 각 1,200QPM·프로젝트 40,000QPM/30,000,000QPD와 별도 부하 한도가 있다. | BX060 | 일치 |
| C045 | A10 | Site Kit은 WordPress에서 Google 지표를 연결하는 대안이다. | BX110 | 일치 |
| C046 | A10 | Jetpack 요금·상업 사이트 적용 조건은 현행 플랜을 확인한다. | BX109 | 일치 |
| C047 | A11 | Actions 예약은 기본 UTC·기본 브랜치 최신 커밋이며 지연·누락 가능성이 있다. | BX080 | 일치 |

### 검색·광고

| 주장 ID | 위치 | 추출한 주장 | 각주/근거 | 대조 결과 |
|---|---|---|---|---|
| C048 | A3,A5,A12 | 검색 순위 조작 목적의 추가 가치 없는 대량 생성은 Google 스팸 정책 위반이다. | BX064 | 일치 |
| C049 | A12 | AI 사용 자체를 일률 금지하지 않으며 도구보다 목적·가치를 본다. | BX066 | 일치 |
| C050 | A12 | 사이트 평판 악용은 제3자 콘텐츠로 호스트의 순위 신호를 악용하는 경우이며 협찬 전부가 아니다. | BX064 | 일치 |
| C051 | A5,A12 | YMYL은 건강·안전·경제적 안정에 큰 영향을 주는 주제다. | BX065 | 일치 |
| C052 | A12 | E-E-A-T는 단일 공개 점수가 아니다. | BX065 | 일치 |
| C053 | A0,A7,monetize/ads.py | AdSense에 보편적인 최소 글 수·방문자·운영일 조건을 만들지 않는다. | BX020,BX022 | 일치 |
| C054 | A7 | AdSense는 독창적 자체 콘텐츠·정책 준수·HTML 관리권을 요구한다. | BX020 | 일치 |
| C055 | A7,monetize/ads.py | 한국어 자격은 19세, 연령 전용 안내는 18세여서 현재 상충한다. | BX020,BX021 | 불일치 |
| C056 | A7 | 소개·문의·광고 정책 페이지 수만으로 광고 승인이 보장되지 않는다. | BX020,BX022 | 일치 |
| C057 | A7 | 거절 사유는 계정/메일로 확인하고 중복 계정 생성으로 해결하지 않는다. | BX022 | 일치 |
| C058 | A7 | 고정 광고 개수 합격 공식이 없고 오클릭 유도·본문 방해 배치를 피한다. | BX024 | 일치 |
| C059 | A7,monetize/ads.py | ads.txt는 적극 권장되지만 보편적 가입 필수조건은 아니다. | BX025 | 일치 |
| C060 | A7,monetize/ads.py | ads.txt는 실제 게시자 ID의 판매자 행을 루트 /ads.txt에 둔다. | BX025 | 일치 |
| C061 | A7 | 부모 대상 육아 주제만으로 아동 대상 사이트로 분류하지 않는다. | BX028 | 일치 |
| C062 | A7 | 미국 아동 대상/미국 아동 정보 인지 수집 등의 조건이면 해외 운영자도 COPPA를 검토한다. | BX028 | 일치 |
| C063 | A7 | 연령 처리 설정은 광고 코드 유형별로 확인하고 TFAT/예전 TFCD·TFUA를 구별한다. | BX098 | 일치 |
| C064 | A7 | EEA·영국·스위스 맞춤 광고에는 Google 인증 CMP 요건을 확인한다. | BX029 | 일치 |
| C065 | A7 | 민감한 광고 카테고리는 차단 관리에서 검토하며 차단 후에도 실제 노출을 확인한다. | BX026 | 근거보완 |
| C066 | A7 | AdFit은 사전승인·초대/제휴 문의와 매체 심사부터 진행한다. | BX123 | 일치 |

### 제휴·협찬

| 주장 ID | 위치 | 추출한 주장 | 각주/근거 | 대조 결과 |
|---|---|---|---|---|
| C067 | A8 | 쿠팡 API 이용은 필수가 아니며 수동 링크·배너로 활동할 수 있다. | BX032 | 일치 |
| C068 | A8 | 쿠팡 누적 판매 15만 원은 최종 채널 검토 시작 기준이다. | BX032 | 일치 |
| C069 | A8 | 최종승인 뒤 API 이용 가능이며 검토 시작이 자동 승인/API 키 발급은 아니다. | BX032 | 일치 |
| C070 | A8 | 활동 매체·링크·표시 화면을 등록하고 실제 활동 주소와 맞춘다. | BX032 | 일치 |
| C071 | A8,monetize/affiliate.py | 쿠팡 권장 문구는 게시물이 파트너스 활동이며 일정액 수수료를 받는다는 문장이다. | BX032 | 일치 |
| C072 | A8 | 쿠팡 현행 최근실적·쿼터·가격 보관·서명은 현재 계정 원문 확인 전 확정하지 않는다. | BX032 | 확인보류 |
| C073 | A8 | 네이버 약관의 웹 매체 정의만으로 WordPress 단독가입/모든 캠페인 허용을 뜻하지 않는다. | BX034,BX102 | 일치 |
| C074 | A8 | 네이버 쇼핑 검색 API와 제휴 링크 발급은 다른 기능이다. | BX102 | 일치 |
| C075 | A4,A8,A9 | 쓰지 않은 제품의 후기를 실제 경험처럼 꾸미면 안 된다. | BX037 | 일치 |
| C076 | A9 | 서울형 1인미디어 표준계약서는 참고이며 모든 블로그의 강제 공통 서식은 아니다. | BX124 | 일치 |
| C077 | A4 | 레뷰 계약의 AI 원고·합성사진 허용 범위는 현행 약관에서 먼저 확인한다. | BX111 | 확인보류 |
| C078 | A4 | 리뷰타임은 AI 후기 글·생성/합성사진 등 사용 제한을 공지했다. | BX113 | 일치 |

### 표시 의무

| 주장 ID | 위치 | 추출한 주장 | 각주/근거 | 대조 결과 |
|---|---|---|---|---|
| C079 | A8,A9,A12 | 현행 추천·보증 심사지침은 예규 499호·2026-06-01 시행이며 공개 조항은 Ⅴ.6이다. | BX037 | 일치 |
| C080 | A5,A8,A9,A12 | 문자형 블로그는 게시물 제목 또는 첫 부분에 쉽게 알아보게 관계를 표시한다. | BX037 | 일치 |
| C081 | A5,A8,A12 | 댓글·더보기·하단에만 감춘 표시는 적절한 공개로 취급하지 않는다. | BX037 | 일치 |
| C082 | A8,A9,A12 | 제품 무료 제공·대여·광고비·미래 판매수수료 등 실제 관계를 밝힌다. | BX037,BX081 | 일치 |
| C083 | A8,A12 | 제품 제공과 제휴 수수료가 함께 있으면 두 관계를 모두 밝힌다. | BX037 | 일치 |
| C084 | A8,A9,A12 | 사진형 추천은 사진 내 표시가 원칙이며 연결 본문과 쉽게 인식되면 첫부분 표시 예외가 있다. | BX037 | 일치 |
| C085 | A8,A12 | 사진만 재사용할 때는 표시를 다시 점검한다. | BX037 | 일치 |
| C086 | A8,A12 | 유료 링크 rel=sponsored는 검색용이며 독자용 표시를 대신하지 않는다. | BX064 | 일치 |
| C087 | A2,A7,A12 | 광고·협찬 정책 페이지 자체와 개별 글의 경제관계 표시는 별개다. | BX037 | 일치 |

### 제품 규제

| 주장 ID | 위치 | 추출한 주장 | 각주/근거 | 대조 결과 |
|---|---|---|---|---|
| C088 | A5,A8,A9,A12 | 조제유류의 인터넷 광고·판매촉진은 별표6의 금지와 표시사항 게시 예외를 따른다. | BX038,BX082 | 일치 |
| C089 | A8 | 일반 부모의 비대가성 양육기록 전체를 조제유류 광고금지로 확대하지 않는다. | BX037,BX082 | 일치 |
| C090 | A8 | 젖병·젖꼭지 전품목에 조제유류 광고금지를 그대로 적용하지 않는다. | BX041,BX082 | 일치 |
| C091 | A5,A8,A9,A12 | 어린이제품의 안전인증·안전확인·공급자적합성확인을 구별한다. | BX041,BX126 | 일치 |
| C092 | A5,A8,A12 | 의료기기·화장품·식품용 기구/용기는 어린이제품법의 같은 KC 절차로 묶지 않는다. | BX041 | 일치 |
| C093 | A8,A9,A12 | 라벨의 모델·업체·상태·리콜을 SafetyKorea에서 대조한다. | BX040,BX125 | 일치 |
| C094 | A8,A9,A12 | 공급자적합성 품목의 검색 결과 없음만으로 불법/안전을 판정하지 않는다. | BX126 | 일치 |
| C095 | A8,A12 | 화장품의 의약품 오인·허위 효능 표현은 금지된다. | BX104 | 일치 |
| C096 | A8,A12 | 영유아용 안전성 자료 작성·보관은 책임판매업자 의무이며 블로거의 직접시험 의무로 바꾸지 않는다. | BX043,BX104 | 일치 |
| C097 | A8,A12 | 화장품 AI 가상전문가 오인광고 신설 조항은 2026-11-27 시행 예정이다. | BX042 | 일치 |
| C098 | A5,A8,A9,A12 | 의료기기 사용자 감사장·체험담 이용 광고는 별표7 제8호에서 금지한다. | BX105,BX131 | 일치 |
| C099 | A8,A12 | 의료기기 허가/인증/신고와 광고 매체·내용별 자율심의는 따로 확인한다. | BX044,BX083 | 일치 |
| C100 | A8 | 소규모 개인 블로그라는 이유만으로 의료기기 심의가 무조건 면제되지는 않는다. | BX044,BX083 | 일치 |
| C101 | A8,A12 | 건강기능식품의 질병 예방·치료 오인 광고와 미심의·심의 위반 광고는 금지된다. | BX106 | 일치 |
| C102 | A8,A12 | 건강기능식품은 허용 기능·해당 심의·대상 연령을 구별한다. | BX084,BX106 | 일치 |
| C103 | A5,A8,A9,A12 | 영아 수면의 베개·느슨한 이불·경사형 등 위험 근거와 프로젝트 홍보 거절을 구별한다. | BX078,BX086 | 근거보완 |

### 개인정보

| 주장 ID | 위치 | 추출한 주장 | 각주/근거 | 대조 결과 |
|---|---|---|---|---|
| C104 | A2,A7,A12 | 업무 목적 개인정보처리자에 처리방침 수립·공개 의무가 있다. | BX048 | 일치 |
| C105 | A2,A7,monetize/pages.py | 처리방침은 목적·항목·보유기간·파기·권리·책임자·안전조치 및 해당 처리의 고지를 갖춘다. | BX048 | 누락 |
| C106 | A2,monetize/pages.py | 동의 수집 시 목적·항목·보유기간·거부권과 불이익을 알린다. | BX048 | 일치 |
| C107 | A12 | 개인 양육 기록과 업무 목적으로 개인정보파일을 운용하는 경우를 구별한다. | BX048 | 일치 |
| C108 | A12 | 동의를 근거로 14세 미만 정보를 처리하면 법정대리인 동의·확인이 필요하다. | BX048 | 일치 |
| C109 | A12 | 촬영 동의와 사진 공표에 대한 동의 범위는 다르다. | BX129 | 일치 |
| C110 | A5,A9,A12 | 아이 얼굴·일상·배경 정보의 공유는 개인정보 노출 위험이 있다. | BX049 | 일치 |
| C111 | A5,A12 | 사진에는 촬영 위치 메타데이터가 들어갈 수 있으며 위치 제거와 시각 검토는 다르다. | BX085 | 일치 |
| C112 | A12 | 삭제·처리정지 요청은 권한·범위·법정 예외를 확인해 처리한다. | BX048 | 일치 |

### 저작권·자료

| 주장 ID | 위치 | 추출한 주장 | 각주/근거 | 대조 결과 |
|---|---|---|---|---|
| C113 | A3 | 어린이집 기관정보 API는 무료 공개 XML이며 개인 명단/입소 가능 자리 보장이 아니다. | BX068,BX069 | 일치 |
| C114 | A3 | 중앙부처복지서비스 API는 원문·대상·금액을 다시 확인하는 출발점이다. | BX089 | 일치 |
| C115 | A3 | 센터 현황 CSV는 2025-12-31 기준 유형·연도별 집계이며 기관 주소록이 아니다. | BX090 | 일치 |
| C116 | A3 | 전국센터현황 주소록과 센터 수 집계를 구별한다. | BX070,BX090 | 일치 |
| C117 | A3 | 공개 접종 일정표와 아이 개인 접종기록 API를 구별하며 첨부 재이용 조건을 확인한다. | BX091 | 확인보류 |
| C118 | A3 | 공공누리 0유형은 출처표시 조건 없는 자유 이용이다. | BX122 | 일치 |
| C119 | A3,A12 | 공공누리 1유형은 출처표시·상업/변경 가능, 2유형은 상업금지다. | BX122 | 일치 |
| C120 | A3,A12 | 공공누리 3유형은 변경금지, 4유형은 상업/변경 금지다. | BX122 | 일치 |
| C121 | A3,A12 | 데이터 이용허락과 첨부 사진·로고·제3자 권리를 따로 확인한다. | BX122 | 일치 |

### 세금·급여

| 주장 ID | 위치 | 추출한 주장 | 각주/근거 | 대조 결과 |
|---|---|---|---|---|
| C122 | A0,A9,A12 | 현물 소비자가격을 현금입금에 합산하지 않으며 현금/물품/반납/비용/입금을 나눈다. | BX050,BX118 | 일치 |
| C123 | A12 | 근로·계속적 프리랜서·일시 우발 원고료의 소득 구분은 다르다. | BX117 | 일치 |
| C124 | A9,A12 | 금전 외 수입은 거래 당시 가액으로 계산하며 사업 관련 무상자산도 검토한다. | BX050,BX118 | 일치 |
| C125 | A9,A12 | 과세 거래의 금전 외 대가는 공급한 재화/용역 시가를 본다. | BX119 | 일치 |
| C126 | A9,A12 | 소득 종류·등록·부가세는 실제 계약을 126/세무서에 제시해 확인하며 공통 세율로 정하지 않는다. | BX117,BX119 | 일치 |
| C127 | A12 | 사업 개시일부터 20일 이내 등록이 원칙이다. | BX052 | 일치 |
| C128 | A12 | 통상 다음 해 5월 1~31일 신고, 2026년 수입은 원칙적으로 2027년 5월이다. | BX053 | 근거보완 |
| C129 | A0,A9,A12 | 육아휴직급여 소득 활동 신고는 세금 신고와 별도로 고용센터/1350에 확인한다. | BX108 | 일치 |
| C130 | A12 | 시행규칙 116조3항은 주 소정근로 15시간 이상 또는 자영업소득/근로대가 월 150만원 이상이다. | BX108 | 일치 |
| C131 | A12 | 매출·제품 정가·세후입금을 곧바로 신고 기준 소득으로 대입하지 않고 실제 자료로 확인한다. | BX108 | 일치 |

### 샘플·건강

| 주장 ID | 위치 | 추출한 주장 | 각주/근거 | 대조 결과 |
|---|---|---|---|---|
| C132 | samples/info.md,content/samples.py | 부모급여 0~11개월 100만원·12~23개월 50만원이며 어린이집 이용 시 지급방식/차액을 확인한다. | N037 | 일치 |
| C133 | samples/info.md | 아동수당은 2026년 9세 미만 기본 월 10만원, 지역 추가·개별 조건을 확인한다. | N038 | 일치 |
| C134 | samples/play.md | 터미타임은 깨어 있을 때 진행하며 WHO 국외 안내임을 밝힌다. | N092 | 일치 |
| C135 | samples/emergency.json fever | 3개월 미만 38.0℃ 이상이면 좋아 보여도 즉시 응급실 진료다. | N001 | 일치 |
| C136 | samples/emergency.json breathing | 호흡곤란·입술/혀 청색·깨우기 어려움/반응 이상·경련은 각각 즉시 도움 요청 신호다. | N001,N085,N090 | 일치 |
| C137 | samples/emergency.json feeding | 잘 못 먹음·소변 감소·처짐이면 진료를 지연하지 않는다. | N001,N090 | 일치 |
| C138 | samples/emergency.json jaundice | 첫날 황달·악화/지속·흰/회백색 변은 의료진 진료로 연결한다. | N003,N031 | 일치 |
| C139 | samples/emergency.json vomit | 초록/노란/피 섞인/분수 구토·못 먹음/처지는 구토는 즉시 진료한다. | N060 | 일치 |
| C140 | samples/emergency.json navel | 배꼽 붉어짐·압통·고름/악취·지속출혈은 진료한다. | N007 | 일치 |
| C141 | samples/emergency.json parent | 자신/아기를 해칠 것 같으면 혼자 버티지 않고 즉시 다른 어른·응급 도움을 요청한다. | N052,N054 | 일치 |
| C142 | samples/emergency.json cold | NHS의 저체온 위험 신호와 5세 미만 겨드랑이 전자체온계 안내를 구별해 제공한다. | N090,N130 | 일치 |
| C143 | samples/emergency.json cry | 매우 약하거나 날카롭게 달라진 울음은 즉시 의료 도움 요청 신호다. | N026 | 일치 |
| C144 | samples/emergency.json rash | 눌러도 옅어지지 않는 발진은 즉시 의료 도움 요청 신호다. | N001 | 일치 |

### 키트·설계 자체의 주장 20개(외부 사실 144개와 별도)

법이 정한 의무로 세지 않고 설계와 실제 코드·실행을 대조했다. 같은 근거 규칙을 법적 금지라고 과장하는지와 “코드가 막는다”는 구현 설명을 구별한다.

| ID | 본문/키트의 주장 | 근거·판정 |
|---|---|---|
| K01 | 높은 위험은 설정과 관계없이 사람 승인 | 명시 플래그는 거부했으나 건강 분류 누락·갱신 경로 반례. **B01·B02 불일치** |
| K02 | 터미타임은 놀이여도 건강 등급 | 기본 샘플 및 플래그 삭제 시 유지. 일치 |
| K03 | 경험은 AI로 채우지 않고 사람이 작성 | mock 경험 칸은 비어 있음. D4가 “human” 여부를 확인. 실제 경험 진위는 사람이 확인해야 함 |
| K04 | AI 허용을 생성 전에 확인 | make_draft가 일반 샘플 계약과 협찬 reviewing 기록을 검사. 사람이 불허/불명 값을 임의 변경해도 약관 적법성이 생기지 않음 |
| K05 | 금지 약 이름·용량·자가관찰 문장은 전부 차단 | 일부 패턴만 구현. **B06 불일치** |
| K06 | 응급 관련 글은 공통 문구 그대로 | 공통 문자열 10/10 일치, 본문 주제 추론은 누락. **B06 부분** |
| K07 | 관계 첫부분 검사로 실제 받은 물품·현금·수수료 확인 | 단어 포함 검사여서 실제 종류/시각 표시 누락. **B04 불일치** |
| K08 | 법적 금지는 사람이 승인해도 남길 수 없음 | 탐지된 block은 거부하지만 탐지 누락 문구는 승인·예약 가능. **B03 불일치** |
| K09 | 법적 금지/프로젝트 거절/자료 보류를 구별 | P7 프로젝트 거절·review 보류 분리는 있으나 나머지 block을 법적 금지로 일괄 분류. **R03 부분** |
| K10 | 안전 수면과 충돌하는 협찬은 거절 | 기본 낮잠 이불 시연은 프로젝트 거절. 비수면 용도 담요까지 법적 금지라 하지 않는 본문은 적절 |
| K11 | 아이 얼굴·실명·생일·기관·생활위치 기본 비공개 | 배포 샘플은 충족. 검사식으로 모든 실제 정보를 탐지하지는 못함. **B01·B05** |
| K12 | EXIF 제거·공개 파일 재검사 | JPEG EXIF 제거 함수는 좁게 성공. 형식·XMP 검사 누락과 시연 파일 손상. **B05·R04** |
| K13 | 자동 검사와 최종 사람 승인 별개 | 명령·저장 구조가 별개. 다만 H1 review를 발행이 승계하지 않는 **B01** 존재 |
| K14 | 광고주 확인과 최종 작성자 승인 별개 | sponsor 상태표·해시 연결 및 기존 테스트에서 분리 확인. 실제 광고주 회신을 얻은 것은 아님 |
| K15 | 승인 뒤 원고·사진·관계·목적지 변경 시 무효 | 해시·원격 스냅샷 검사 확인, 기존 회귀 검사 통과. 갱신의 prepare→auto는 **B02** |
| K16 | 시간 초과는 조회하고 생성 POST 반복 금지 | claim·slug 재조정·예약 상태 조회 관련 기존 검사 통과 |
| K17 | 하루2개·유사도0.9는 운영값 | 소스의 기본값 확인. 검색엔진 안전선/법정 수치로 쓰지 않아 일치 |
| K18 | 모의 수입과 실제 입금·세금 평가를 구별 | 광고/미디어킷/세금 CSV가 모의·미확정·반납·비용/실입금 구분. 실제 과세판정 기능은 없음 |
| K19 | 운영·상태·알림의 미응답은 승인 아님 | 알림은 기록, publish가 승인 검사. 다만 높은 위험 식별 누락은 **B01**로 별도 차단 |
| K20 | 개인정보 보유30일·9시예약·최대3회 재시도는 예시 | 30일/9시는 설정 예시, 3회는 본문의 향후 운영 권고이며 범용 CLI 재시도 구현이라고 하지 않음. 일치 |

## 7. 기존 출처 URL의 이번 열람 기록

접근일은 전부 **2026-10-28**. 아래 “본문 수신”은 제목만 받은 경우를 제외하며, 각 주장의 실제 대조 결론은 6절을 따른다. 모든 원문/응답·임시 실험 파일은 `/tmp/bx6-policy/`에만 두었다. 공개 저장소에는 원응답 전문을 복사하지 않았다. 임시 파일은 장기 보존을 보장하지 않으므로 아래 URL·본문 위치·주장·재현 입력을 이 문서에 남긴다.

| 출처 | 원문 | 이번 확인 수준·주요 대조 위치 |
|---|---|---|
| BX001 | [WordPress Versions](https://wordpress.org/documentation/article/wordpress-versions/) | 본문 수신: Released Versions 최신 안정판 |
| BX002 | [Docker Official Images WordPress 목록](https://raw.githubusercontent.com/docker-library/official-images/master/library/wordpress) | 본문 수신: 7.1.3-php8.3-apache 태그·아키텍처 |
| BX003 | [Application Passwords](https://developer.wordpress.org/advanced-administration/security/application-passwords/) | 본문 수신: HTTPS·권한·비활성 필터·Authorization |
| BX004 | [Posts REST reference](https://developer.wordpress.org/rest-api/reference/posts/) | 본문 수신: draft/future/date/date_gmt/categories/tags/featured_media |
| BX005 | [Media REST reference](https://developer.wordpress.org/rest-api/reference/media/) | 본문 수신: POST media·alt_text·반환 ID |
| BX006 | [Categories REST reference](https://developer.wordpress.org/rest-api/reference/categories/) | 본문 수신: POST categories·name·parent |
| BX007 | [Tags REST reference](https://developer.wordpress.org/rest-api/reference/tags/) | 본문 수신: POST tags·name·slug |
| BX008 | [WordPress.com Plugins](https://wordpress.com/support/plugins/) | 본문 수신: 모든 유료 요금제 플러그인 지원 |
| BX009 | [Monetize your site](https://wordpress.com/support/monetize-your-site/) | 본문 수신: third-party networks·WordAds·협찬·제휴 |
| BX010 | [WordPress.com Pricing](https://wordpress.com/pricing/) | 부분: 이번 응답은 영문 가격표·FAQ. 한국어의 기존 상충 구절 재확인 못함(R06) |
| BX011 | [Blogger Using API](https://developers.google.com/blogger/docs/3.0/using) | 본문 수신: OAuth·공개 읽기 API key·쓰기 권한 |
| BX012 | [Blogger posts.publish](https://developers.google.com/blogger/docs/3.0/reference/posts/publish) | 본문 수신: publishDate 예약·OAuth |
| BX013 | [네이버 블로그 Open API 종료](https://developers.naver.com/notice/article/7527) | 본문 수신: research-blog B006 재사용; 복구 여부 재확인 |
| BX014 | [티스토리 Open API 종료](https://notice.tistory.com/2664) | 본문 수신: research-blog B007 재사용; 복구 여부 재확인 |
| BX015 | [워드프레스 블로그 호스팅](https://hosting.cafe24.com/?controller=new_product_page&page=wordpress-blog) | 부분: 웹 도구로 월요금·설치비·VAT 확인. 추가 설치/SSH/FTP 제한은 재확인 못함(R06) |
| BX016 | [Managed WordPress hosting](https://www.hostinger.com/wordpress-hosting) | 본문 수신: Premium 48개월119.52달러·갱신10.99달러/월·주간백업 |
| BX019 | [도메인 가격 인상 예정](https://www.gabia.com/gabia_notice/view.php?seq_no=45623) | 웹 도구 본문: 2026-10-01 공지·11-01 적용·신규/연장/이전·VAT별도 가격표 |
| BX020 | [애드센스 자격 요건](https://support.google.com/adsense/answer/9724?hl=ko) | 본문 수신: 자체 콘텐츠·정책·HTML 관리·한국어19세 |
| BX021 | [애드센스 연령 요건](https://support.google.com/adsense/answer/14230?hl=ko) | 본문: 이번에는 만19세로 표시. 기존 18세 상충 설명과 다름(R01) |
| BX022 | [애드센스 승인 거절 원인](https://support.google.com/adsense/answer/81904?hl=ko) | 본문 수신: 중복계정·콘텐츠·탐색·트래픽·언어 |
| BX023 | [애드센스 프로그램 정책](https://support.google.com/adsense/answer/48182?hl=ko) | 본문 수신: 무효클릭·개인정보·트래픽·게시자 정책 |
| BX024 | [광고 게재위치 정책](https://support.google.com/adsense/answer/1346295?hl=ko) | 본문 수신: 오클릭 유도·광고와 콘텐츠 구별 |
| BX025 | [ads.txt 가이드](https://support.google.com/adsense/answer/12171612?hl=ko) | 본문 수신: 루트 ads.txt·게시자 ID |
| BX026 | [민감한 광고 카테고리 차단](https://support.google.com/adsense/answer/3016453?hl=ko) | 원문 미확인: 직접404·웹 열람 실패. V03으로 차단 기능 보완(R05) |
| BX028 | [Complying with COPPA FAQ](https://www.ftc.gov/business-guidance/resources/complying-coppa-frequently-asked-questions) | 웹 도구 본문: A/D·해외사업자 적용 질문. 부모 주제만으로 아동 대상으로 확대하지 않음 |
| BX029 | [Google certified CMP requirements](https://support.google.com/adsense/answer/13554116?hl=en) | 본문 수신: 방문자 지역 기준·한국과 구별 |
| BX032 | [쿠팡 파트너스 이용가이드](https://partners.coupangcdn.com/partners-guide/partners-guide-20260917111657.pdf) | PDF81쪽: 인쇄20쪽 최종승인·25쪽 수수료 권장 문장·정책 부분. 표지2024.12 |
| BX034 | [네이버 어필리에이트 크리에이터 통합약관](https://brandconnect.naver.com/service/term/affiliate/creator) | 본문 수신: 등록채널·외부매체 제한; 로그인벽 가능 |
| BX037 | [추천ㆍ보증 등에 관한 표시ㆍ광고 심사지침](https://www.law.go.kr/LSW/admRulInfoR.do?admRulSeq=2100000280130&chrClsCd=010201) | 본문: 시행일·Ⅴ.5·Ⅴ.6의 일반원칙/문자/사진 구분 |
| BX038 | [식품 표시광고법 시행규칙](https://www.law.go.kr/LSW/lsInfoR.do?lsiSeq=267855&efYd=20260101) | 본문: 제8조·별표6 연결, BX082의 정의·예외와 함께 확인 |
| BX040 | [제품안전정보센터](https://www.safetykorea.kr/) | 본문 수신: 인증정보·리콜·대상품목 |
| BX041 | [어린이제품 안전 특별법](https://www.law.go.kr/LSW/lsInfoR.do?lsiSeq=276551&efYd=20251001) | 본문: 제2조 제외 품목·세 안전절차 |
| BX042 | [화장품법](https://www.law.go.kr/LSW/lsInfoR.do?lsiSeq=291337&efYd=20261020) | 본문: 제4조의2·13조와 법률21709호 부칙. 통합 화면만으로 10월 시행이라고 판단하지 않음 |
| BX043 | [영유아화장품 안전성 자료](https://www.law.go.kr/LSW/lsLawLinkInfo.do?ancYnChk=&chrClsCd=010202&lsJoLnkSeq=1014693901) | 본문 수신: 제4조의2 제품·안전평가·효능증명 자료 |
| BX044 | [의료기기법 제25조](https://www.law.go.kr/lsLinkCommonInfo.do?lsJoLnkSeq=1026877617) | 조문 본문: 제25조 대상매체·내용 예외·변경 심의 |
| BX048 | [개인정보 보호법](https://www.law.go.kr/LSW/lsInfoR.do?lsiSeq=283839&efYd=20260911) | 본문: 제2·15·22의2·28의8·30조. V01 시행령으로 필수항목 보완 |
| BX049 | [자녀사진 알고 공유합시다](https://pipc.go.kr/np/cop/bbs/selectBoardArticle.do?bbsId=BS074&mCode=C020010000&nttId=8874) | 본문 수신: 셰어런팅 노출위험·교육; 법적일괄금지아님 |
| BX050 | [소득세법 제24조](https://www.law.go.kr/lsLinkCommonInfo.do?chrClsCd=010202&lsJoLnkSeq=1032880365) | 본문 수신: 금전외 수입 거래당시 가액 |
| BX052 | [사업자등록 언제 어떻게](https://www.nts.go.kr/nts/na/ntt/selectNttInfo.do?nttSn=1396&mi=2448) | 본문 수신: 개시20일 원칙; B154재사용 |
| BX053 | [모두채움 종합소득세](https://www.nts.go.kr/nts/cm/cntnts/cntntsView.do?cntntsId=238978&mi=40483) | 본문: 2025귀속·2026-06-01 신고 안내. 일반 기한 근거는 V02로 보완(R07) |
| BX057 | [GA4 Data API quotas](https://developers.google.com/analytics/devguides/reporting/data/v1/quotas) | 본문 수신: 표준core 토큰/일200000·시간40000·프로젝트14000 |
| BX058 | [GA4 Data API schema](https://developers.google.com/analytics/devguides/reporting/data/v1/api-schema) | 본문 수신: activeUsers/sessions/screenPageViews/engagementRate |
| BX059 | [GSC searchanalytics.query](https://developers.google.com/webmaster-tools/v1/searchanalytics/query) | 본문 수신: rowLimit25000·dataState·PT날짜·상위행 |
| BX060 | [GSC usage limits](https://developers.google.com/webmaster-tools/limits) | 본문 수신: 사이트/사용자/프로젝트 QPM·QPD·load quota |
| BX062 | [GA4 API quickstart](https://developers.google.com/analytics/devguides/reporting/data/v1/quickstart) | 본문 수신: 서비스계정/OAuth·속성권한 |
| BX063 | [AdSense Management API reports.generate](https://developers.google.com/adsense/management/reference/rest/v2/accounts.reports/generate) | 본문 수신: OAuth scope·기간·통화·시간대·행제한 |
| BX064 | [Google Search spam policies](https://developers.google.com/search/docs/essentials/spam-policies) | 본문 수신: 대량생성·사이트평판·만료도메인 |
| BX065 | [Helpful reliable people-first content](https://developers.google.com/search/docs/fundamentals/creating-helpful-content) | 본문 수신: E-E-A-T·YMYL·Who/How/Why |
| BX066 | [Google generative AI content guidance](https://developers.google.com/search/docs/fundamentals/using-gen-ai-content) | 본문 수신: AI사용자체와 대량저가치 생성구별 |
| BX068 | [전국 어린이집 API](https://www.data.go.kr/data/15101155/openapi.do) | 본문 수신: 정원·기관·주소; 개인정보분리 |
| BX069 | [어린이집별 기본정보 API](https://www.data.go.kr/data/15101154/openapi.do) | 본문 수신: 개별기관 정보·이용허락범위 |
| BX070 | [전국 육아지원센터 현황](https://cmsadm.childcare.go.kr/lcentral/d1_10000/d1_10007.jsp) | 본문 수신: 센터목록; 재이용허락은별도확인 |
| BX071 | [OpenAI API pricing](https://developers.openai.com/api/docs/pricing) | 본문 수신: Luna0.10/0.50·Sol2/10 USD1M; 기존A025 |
| BX072 | [OpenAI Structured Outputs](https://developers.openai.com/api/docs/guides/structured-outputs) | 본문 수신: json_schema/strict/거절/부분스키마 |
| BX073 | [OpenAI Spend limits](https://developers.openai.com/api/docs/guides/spend-limits) | 본문 수신: Project Limits Spend Enforce a hard limit |
| BX074 | [OpenAI Deprecations](https://developers.openai.com/api/docs/deprecations) | 본문 수신: 사용모델종료확인·이미지/TTS본문미확대 |
| BX078 | [영아돌연사증후군](https://health.kdca.go.kr/healthinfo/biz/health/gnrlzHealthInfo/gnrlzHealthInfoView.do?cntnts_sn=5467) | 원문 미확인: 직접404. 이번 안전수면 근거는 BX086 및 N031로 보완(R05) |
| BX080 | [GitHub Actions 예약 실행](https://docs.github.com/en/actions/reference/workflows-and-actions/events-that-trigger-workflows#schedule) | 본문 수신: 예약지연·timezone·60일·기본브랜치 재사용 |
| BX081 | [Q&A로 알아보는 경제적 이해관계 표시(2025)](https://www.korea.kr/common/download.do?fileId=198296345&tblKey=GMN) | PDF47쪽: 공개 위치·명확한 문구·미래 수수료 Q&A. 현행 지침과 대조 |
| BX082 | [식품 광고 시 준수사항 별표6](https://www.law.go.kr/LSW/flDownload.do?gubun=&flSeq=147458325&bylClsCd=110201) | PDF1쪽: 별표6 제2·3호, 조제유류 정의·인터넷 표시 예외·판촉 구분 |
| BX083 | [의료기기법 시행령](https://www.law.go.kr/LSW/lsInfoR.do?lsiSeq=287221&efYd=20260701) | 본문: 제10조의3의 인터넷/SNS 광고매체 및 10만 이용자 기준 |
| BX084 | [건강기능식품 광고심의 대상](https://ad.khff.or.kr/user/intro/IntroUser1.do?_menuNo=217) | 본문 수신: 인터넷포함 대상매체·식품표시광고법10조 |
| BX085 | [사진 앱 위치 메타데이터 관리](https://support.apple.com/ko-kr/guide/personal-safety/ips0d7a5df82/1.0/web/1.0) | 본문 수신: 위치메타데이터·공유제거·기기설정 |
| BX086 | [경사진 영아수면용품 주의](https://www.ciss.go.kr/DATA/bbs/85/20240827011002198.pdf) | PDF17쪽: 한국소비자원 조사·주의 권고. 판매 일괄 금지로 옮기지 않음 |
| BX089 | [중앙부처복지서비스 API](https://www.data.go.kr/data/15090532/openapi.do) | 본문 수신: 목록·상세XML·이용허락범위제한없음 |
| BX090 | [육아종합지원센터 현황 CSV](https://www.data.go.kr/data/15101484/fileData.do) | 본문 수신: 유형/연도집계; 주소목록과구별·연간·제한없음 |
| BX091 | [예방접종 공개 자료 다운로드](https://nip.kdca.go.kr/irhp/mngm/goFormBrdList.do) | 원문 미확인: 직접 TLS 재협상 실패. 검색 결과는 본문 확인으로 세지 않음 |
| BX095 | [Blogger AdSense 연결](https://support.google.com/blogger/answer/1269077?hl=ko) | 본문 수신: 수익 메뉴 신청·승인분리 |
| BX096 | [WordPress.com OAuth2](https://developer.wordpress.com/docs/oauth2/) | 본문 수신: Bearer access token·설치형Basic과구별 |
| BX097 | [WordAds 지원조건](https://wordpress.com/support/wordads/) | 본문 수신: Premium이상·공개사이트·독립도메인 |
| BX098 | [현재 AdSense age-treatment 요청](https://support.google.com/adsense/answer/9007197?hl=en) | 본문: TFCD/TFUA deprecated와 TFAT 안내, 코드 유형 구별 |
| BX102 | [쇼핑커넥트 링크 발급·삽입 안내](https://help.naver.com/service/30027/contents/24104?lang=ko&osType=COMMONOS) | 본문 수신: 원하는콘텐츠삽입·대가성원문 |
| BX104 | [화장품법 적용시기 대조용 구판](https://www.law.go.kr/LSW/lsInfoR.do?lsiSeq=270323&efYd=20260402) | 본문: 2026-04-02 판본 제4조의2·13조. BX042·부칙과 대조 |
| BX105 | [의료기기법 시행규칙](https://www.law.go.kr/LSW/lsInfoR.do?lsiSeq=287877&efYd=20260701) | 본문: 제45조와 별표7 연결 |
| BX106 | [식품 등의 표시광고법](https://www.law.go.kr/LSW/lsInfoR.do?lsiSeq=269957&efYd=20250919) | 본문: 제8조 질병 예방/치료 등·제10조 심의 |
| BX108 | [고용보험법 시행규칙 취업신고](https://www.law.go.kr/LSW/lsInfoR.do?lsiSeq=288723&efYd=20260918) | 본문: 제116조3항의 주15시간 또는 월150만원, 지급제한 심사와 구별 |
| BX109 | [Jetpack Stats 현행 가격·FAQ](https://jetpack.com/stats/) | 본문 수신: 현행Free기초기능·고급유료; 상업사이트유료강제 과거안내재확인 |
| BX110 | [Google Site Kit](https://sitekit.withgoogle.com/) | 본문 수신: 공식WordPress통계/AdSense연동플러그인 |
| BX111 | [레뷰 통합회원 약관](https://webview.revu.net/terms/terms-of-use?tab=integrated) | 원문 미확인: HTTP200이나 JS 제목26자뿐. 약관 본문 확인으로 세지 않음 |
| BX113 | [리뷰타임 AI 금지 공지](https://byreview.net/bbs_detail.php?bbs_num=78&tb=board_notice) | 본문: 2026-09-16 공지, AI 후기 글·생성/합성 사진·과도 변형 제한 |
| BX116 | [Search Console 전체 데이터·지연](https://developers.google.com/webmaster-tools/v1/how-tos/all-your-data) | 본문 수신: 일/검색유형 50K·통상2~3일 지연 |
| BX117 | [국세청 원고료 소득구분 사례](https://www.nts.go.kr/nts/cm/cntnts/cntntsView.do?cntntsId=7890&mi=6610) | 본문: 원고료/강의료의 근로·프리랜서·일시 우발 구분표 |
| BX118 | [소득세법 시행령 제51조](https://law.go.kr/lsLinkCommonInfo.do?chrClsCd=010202&lspttninfSeq=126445) | 조문 본문: 제51조 사업 관련 무상자산 |
| BX119 | [부가가치세법 제29조](https://www.law.go.kr/LSW/lsLinkCommonInfo.do?lsJoLnkSeq=1032157099) | 조문 본문: 제29조3항2호의 금전 외 대가·공급 용역 시가 |
| BX122 | [공공누리 최신 이용조건](https://www.kogl.or.kr/info/license.do) | 본문: 0~4유형 이용조건·상업/변경 제한 |
| BX123 | [AdFit 가입·제휴문의](https://kakaobusiness.gitbook.io/main/partner/adfit/join.md) | 공식 Markdown 본문: 사전승인/초대·제휴문의·인증코드 |
| BX124 | [서울형 1인미디어 표준계약서](https://news.seoul.go.kr/economy/archives/521079) | 본문: 서울형 광고거래/출연 표준서식 배포, 강제 서식 아님 |
| BX125 | [SafetyKorea 인증 상세 예](https://www.safetykorea.kr/release/certDetail?certNum=CB063R11687-6001&certUid=6233959) | 본문: 모델·업체·인증상태·리콜현황 상세 화면 |
| BX126 | [공급자적합성확인 절차](https://www.safetykorea.kr/policy/targetsSafetySupply) | 본문: 공인/자체 시험성적서 등 공급자적합성 입증 방법 |
| BX127 | [WordPress WP-Cron](https://developer.wordpress.org/plugins/cron/) | 본문 수신: 방문 요청 기반 트리거·실제예약지연 |
| BX129 | [대법원 초상권 판례](https://law.go.kr/LSW/precInfoP.do?precSeq=217373) | 판례 본문: 2021다219116, 촬영과 공표 동의 범위·증명책임 |
| BX131 | [의료기기 금지광고 별표7](https://www.law.go.kr/LSW/flDownload.do?gubun=&flSeq=166537359&bylClsCd=110201) | PDF2쪽: 별표7 제8호 체험담, 허위/미심의 광고 등 |
| N001 | [소아 발열 대처법](https://health.kdca.go.kr/healthinfo/biz/health/gnrlzHealthInfo/gnrlzHealthInfo/gnrlzHealthInfoView.do?cntnts_sn=6951) | 본문 수신: 샘플의 해당 건강/제도 주장과 대조 |
| N003 | [신생아 황달](https://health.kdca.go.kr/healthinfo/biz/health/gnrlzHealthInfo/gnrlzHealthInfo/gnrlzHealthInfoView.do?cntnts_sn=5723) | 본문 수신: 샘플의 해당 건강/제도 주장과 대조 |
| N007 | [신생아 > 건강과 일상](https://www.childcare.go.kr/?menuno=424) | 본문 수신: 샘플의 해당 건강/제도 주장과 대조 |
| N026 | [Colic](https://www.nhs.uk/conditions/colic/) | 본문 수신: 샘플의 해당 건강/제도 주장과 대조 |
| N031 | [영유아건강검진 문진표(14~35일용), 별지 제4호](https://www.law.go.kr/flDownload.do?bylClsCd=200203&flSeq=148392197) | PDF 본문: 문진표의 대변색·수면 문항(문진표 질문을 진단으로 쓰지 않음) |
| N037 | [2026년 부모급여, 이렇게 지원합니다!](https://www.korea.kr/news/policyNewsView.do?newsId=148957936) | 본문 수신: 샘플의 해당 건강/제도 주장과 대조 |
| N038 | [아동수당 9세 미만으로 확대…1~3월분 소급해 24일 지급](https://www.korea.kr/news/policyNewsView.do?newsId=148963373) | 본문 수신: 샘플의 해당 건강/제도 주장과 대조 |
| N052 | [산후 우울증](https://www.childcare.go.kr/?menuno=417) | 본문 수신: 샘플의 해당 건강/제도 주장과 대조 |
| N054 | [자살예방상담전화 FAQ: 기존 정신건강상담전화는?](https://www.129.go.kr/faq/faq06.do?searchConsultingKeyword=F01&ssn=15224) | 본문 수신: 샘플의 해당 건강/제도 주장과 대조 |
| N060 | [Reflux in babies](https://www.nhs.uk/conditions/reflux-in-babies/) | 본문 수신: 샘플의 해당 건강/제도 주장과 대조 |
| N085 | [세기관지염](https://health.kdca.go.kr/healthinfo/biz/health/gnrlzHealthInfo/gnrlzHealthInfo/gnrlzHealthInfoView.do?cntnts_sn=6736) | 본문 수신: 샘플의 해당 건강/제도 주장과 대조 |
| N090 | [When to get urgent medical help for babies and children under 5](https://www.nhs.uk/baby/health/when-to-get-urgent-medical-help-for-babies-and-children-under-5/) | 본문 수신: 샘플의 해당 건강/제도 주장과 대조 |
| N092 | [To grow up healthy, children need to sit less and play more](https://www.who.int/news-room/detail/24-04-2019-to-grow-up-healthy-children-need-to-sit-less-and-play-more) | 본문 수신: 샘플의 해당 건강/제도 주장과 대조 |
| N130 | [How to take your baby’s temperature](https://www.nhs.uk/baby/health/how-to-take-your-babys-temperature/) | 본문 수신: 샘플의 해당 건강/제도 주장과 대조 |

법령 열람은 조문·부칙의 시행 범위를 기준으로 했다. 특히 최신 공포 통합 화면과 시행 조항을 구별했다. 세금·제품의 개별 적용이나 의료 진단을 수행했다고 표현하지 않는다. 원문 미확인을 “문제없음”으로 처리하지 않았으며 자료 보류 항목을 공개 자동화에 연결하지 않는 것이 재검토 조건이다.

## 8. 권고·재검토 완료 조건

- **A01 — 출처 검사의 의미:** `official=true`, 입력한 `claims`, `experience_by=human`은 자가 선언이다. N1은 메모와 숫자의 일치이지 외부 원문의 사실 검사나 사람 경험 증명이 아니다. “공식 근거를 자동 검증했다”는 표현으로 바꾸지 말고, 원문 확인일·확인자를 보존한다.
- **A02 — 문안과 사람 검토:** 그림책 놀이 다섯 제안은 편집 제안으로, 건강 수칙·상품 안전·허용 효능은 공식 근거로 나눈다. 새 건강 샘플을 추가할 때 BabyBook 공통 문구·독립 조건·국외 표시와 함께 검토한다.
- **A03 — 산출물 공개 범위:** 미디어킷/보고서에는 집계와 공개 허용 데이터만 유지한다. 운영자가 나중에 입력할 실제 연락처·상담 내용·아이 정보·세금 증빙은 공개 저장소로 자동 내보내지 않는다. EXIF가 없어도 명찰·배경·파일명·본문의 결합 식별 가능성은 사람이 확인한다.

재검토 때 다음 실제 결과를 제시해야 한다.

1. H1 등 사람 검토 항목이 있는 글, 누락/미분류 입력, 기존 서버 글 갱신을 approval/auto 두 설정과 CLI 명령 순서 변경으로 시험해 **무승인 future/publish가 0건**임을 확인한다.
2. 의료기기 체험담·질병 예방 광고·불충분/숨긴 표시를 입력해 **사람 승인으로도 금지 내용이 예약되지 않음**을 확인한다. 잘못된 법적 금지 과잉 판정도 함께 고친다.
3. 정상 JPEG·PNG·확장자 불일치·XMP 위치·변환본에서 미검사 파일을 보류하고, 제거본의 실제 디코딩·메타데이터 재검사가 성공해야 한다.
4. 본문 발열/약 이름 등 미탐지 사례와 응급 문구 10종 일치를 회귀 검사한다. 기존 내용 변경·시간 초과·중복·백업 회귀 검사도 다시 통과해야 한다.
5. R01~R07의 문구·템플릿·각주를 일관되게 고치고, 부분/보류 5개 검토 단위는 원문 확보 또는 확인 전 실행 보류를 유지한다. 확인 못 한 API 자격·쿼터를 임의로 채우지 않는다.

**최종 판정: 수정 후 가능.** 현재 배포 샘플에서 실제 아이 식별 정보는 발견하지 못했으나, 위험 글의 자동 예약 차단과 표시·제품·메타데이터 관문이 설계의 안전 보장을 충족하지 못했다. 이 보고서는 발견 사항과 수정안을 제공하며, 수정 완료·재검토 통과·실계정 성공을 선언하지 않는다. 사이트·키트·조사 문서·PROJECT_STATE는 수정하지 않았고 commit/push하지 않았다.

기본 검토 대상(14 HTML·키트 36파일) 지문: 50파일, 경로별 SHA256 목록을 정렬해 다시 해시한 값 `c2ff04b55f4f41bf943390a96bb42cbc1be465bac9b921c59196d357085c6b68`. 재검토 시 입력 변경 여부를 구별하기 위한 지문이다.
