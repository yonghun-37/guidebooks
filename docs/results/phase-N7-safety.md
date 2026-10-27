# Phase N7 — BabyBook 건강 정보 안전 독립 검토

검토일: 2026-10-27. 검토자: Codex, 건강 정보 안전 검토 역할. 제작 완료 여부와 별도로 현재 원고·동작·원문을 대조했다. 기준은 `docs/DESIGN-baby.md` 8·11절, `research-baby/FACT-SHEET.md`, `SOURCES.md`, `BRIEFING.md` ④⑦⑧이다.

**결론: 수정 후 가능. 현재 상태의 출판 승인은 보류한다. 차단 4건·수정 9건·권고 3건이다.** 공통 문구가 설계와 일치하는 것과 원문에 비춰 안전한 것은 별개다. 특히 아래 B02~B04는 채택된 조사 요약에도 들어 있는 문제이므로, 다음 단계에서 조사 기준과 공통 문구를 함께 재검토해야 한다.

코드·원고·조사자료·프로젝트 상태는 수정하지 않았다. 이 보고서만 산출한다. 커밋·로그인·지원 신청·기관 통화는 하지 않았다. 브라우저 입력에는 합성 자료만 사용했다.

## 검토 범위와 집계 방법

- 전체 33 HTML: 이론 13장, 실습 0~10/E2E 12쪽, 인쇄 4종, 표지·실험실·용어집·출처 4쪽. 본문·SVG 내부 글자/대체설명·그림 캡션·FAQ·퀴즈 정답/오답·용어 설명을 읽었다.
- 실제 도구 15개와 연결 JS를 읽고 Chromium에서 열었다. 도구를 포함한 33쪽에서 입력·제출·체크 변경을 실행하면서 네트워크를 관찰했다. 기록기에는 합성 수유·기저귀 기록을 추가했다.
- 원고에서 참조하는 서로 다른 출처는 **101개**다. SOURCES의 해당 URL 모두에 접근을 시도했다. **100개는 본문/PDF/브라우저 렌더링으로 열었고, N079 1개는 대조 불가**였다. 다태아 금액의 인용 보완을 위해 기존 대장의 N045도 추가로 직접 열었다(접근 시도 합계 102개, 본문 확인 101개).
- HTTP 200만으로 본문 확인으로 세지 않았다. CDC 등의 urllib 403은 웹 도구로 재열람했고, 법원 N042·N043의 빈 정적 본문은 Chromium에서 실제 공개 안내를 렌더링해 확인했다. N025·N027·N031·N032·N056·N057·N076·N083·N091은 내려받은 PDF 본문을 추출했다. N031·N032·N091 표는 PDF를 렌더링해 시각적으로도 대조했다.
- 아래 ‘주장 대조표’는 같은 사실이 본문·FAQ·그림·실습에서 반복되면 하나로 묶고, 수치·적용 대상·행동이 다르면 나눈 검토 단위다. 문장 수나 각주 개수를 주장 수로 부풀리지 않았다. 소프트웨어 동작 검사는 주장 집계와 따로 적었다. ‘일치’는 해당 단위의 원문 일치를 뜻하며 이 책 전체의 안전 승인이 아니다.

**주장 집계: 대조 대상 157개 중 원문 대조 완료 156개(일치 143개·보완 필요 13개), 대조 불가 1개.** 대조 불가 주장은 성장도표의 판본·WHO 도입 대상 상세(C078, R01)이며, 해당 N079 원문은 404다. 다음 표의 번호가 집계의 기준이다.

## 차단 — 출판 전에 해결해야 할 안전 문제

### B01. 핵심 응급 안내가 JS 실패·비활성 시 사라진다

- **위치·인용:** `site-baby/print/emergency.html#main`, `chapters/07-hospital.html#emergency`, `practice/06-emergency.html#cases`, `assets/emergency.js`. 인쇄물의 대체 문구는 “응급 문구를 불러오려면 자바스크립트를 켜 주세요. 위급하면 119에 연락하세요.”다.
- **재현:** JS를 끈 새 브라우저 컨텍스트에서 위 3쪽의 `[data-emergency-id]`가 모두 0개였다. 응급 인쇄표에는 7개 신호·행동이 전부 없고 연락처 안내만 남는다. 실습의 다섯 사례에서도 정작 어느 기관에 연락할지 설명하는 공통 상자가 사라진다. 정상 JS 환경의 A4 한 쪽 출력 성공과 구분해야 한다.
- **근거 원문:** N001 요약의 “컨디션과 무관하게 즉시 응급실 진료”, N090의 “is difficult to wake”는 즉시 행동을 알리는 핵심 정보다. [설계 8.4·11절](../DESIGN-baby.md#8-건강-정보-안전-규칙-이-책-전용-최우선)도 본문·실습·인쇄의 동일 응급 안내를 요구한다. [N001] [N090]
- **고칠 문장·구현 제안:** 현재 7개 통일 문구와 행동을 정적 HTML에도 남겨 JS 없이 읽고 인쇄할 수 있게 한다. “자바스크립트를 켜 주세요”를 응급 안내의 대체물로 사용하지 않는다. 공통 데이터에서 생성하더라도 배포된 HTML에 문구가 있어야 한다. 아래 B02~B04를 반영한 최종 문구로 재생성한다.

### B02. 통일 문구의 결합 조건이 원문보다 좁다

- **위치·인용:** `site-baby/assets/emergency-data.js`의 `feeding`, `breathing`, `jaundice`, `navel`; 대표 화면은 `chapters/07-hospital.html#feeding`, `#breathing`, `#jaundice`, `#navel`, `print/emergency.html#main`이다.
  - “잘 먹지 못하고 소변이 뚜렷하게 줄거나 평소보다 처지면…”
  - “깨워도 반응이 거의 없거나…”
  - “황달이 심해지면서 잘 먹지 못하거나…”
  - “배꼽 주변이 붉고 아파 보이거나…”
- **문제:** 먹지 못함에 소변 감소까지, 황달 악화에 수유 저하까지, 배꼽 붉어짐에 통증까지 함께 있어야 연락하는 문장으로 읽힌다. 깨우기 어려움도 ‘반응이 거의 없음’까지 심해져야 하는 듯 좁아진다. 원문은 이 변화를 각각 평가 대상으로 둔다. 황달이 오래 지속되는 경우도 7장에 명시되지 않았다. ‘모든 신호에 해당할 필요는 없다’는 일반 설명만으로 각 문장의 AND 조건은 해결되지 않는다.
- **근거 원문:** N090 “is a baby and is not feeding”; N003 “생후 2주 이상 황달이 사라지지 않고 계속되는 경우”; N007 “제대 밑 부분의 피부가 붉어진 경우”. 깨우기 어려움은 B01의 N090 발췌와 같다. [N090] [N003] [N007]
- **고칠 문장 제안:** 각각 “평소와 달리 잘 먹지 못하거나, 소변이 뚜렷하게 줄거나, 평소보다 처지면 지체하지 말고 진료받으세요”, “깨우기 어렵거나 평소처럼 반응하지 않으면 즉시 119에 연락하세요”, “황달이 심해지거나 오래 지속되면 의료진에게 알리고 진료받으세요. 잘 먹지 못하거나 처지면 지체하지 마세요”, “배꼽 주변이 붉어지거나, 만질 때 아파하거나, 고름·악취가 나면 진료받으세요”로 독립 조건을 분명히 한다. 나머지 기존 응급 조건도 유지한다.
- **적용 범위:** BRIEFING ④와 공통 데이터는 서로 정확히 일치한다. 이 발견은 개별 장의 복사 오류가 아니라 채택된 요약 자체의 재검토 요청이다.

### B03. 분수 구토에 ‘반복’ 조건을 추가하고 노란 구토를 빠뜨렸다

- **위치·인용:** `site-baby/assets/emergency-data.js`의 `vomit`; `chapters/07-hospital.html#vomit`, `chapters/02-feeding.html#burp`, `practice/03-feeding.html#burp`, `practice/06-emergency.html#cases`, `print/emergency.html#main`. “초록색이나 피가 섞인 구토, **반복되는 분수 구토**…”
- **근거 원문:** N060 Urgent advice는 “green or yellow”, “is projectile vomiting”을 각각 열거한다. 여러 번 일어나야 한다는 조건이 없다. [N060]
- **위험:** 처음 발생한 힘센 분수 구토는 더 반복될 때까지 관찰하거나, 노란 구토는 목록 밖의 일반 변화로 취급할 수 있다.
- **고칠 문장 제안:** “초록색·노란색이나 피가 섞인 구토, 분수처럼 힘차게 뿜는 구토, 먹지 못하거나 처지는 구토는 즉시 진료받으세요.” 색만으로 집에서 원인을 판정하지 않으며, 숨·반응 이상은 119라는 안내를 함께 둔다. 공통 원본·관련 FAQ·실습·인쇄 모두 같은 기준으로 맞춘다.

### B04. 원문상 즉시 도움 대상이 ‘목록 밖이면 오늘 문의’로 내려갈 수 있다

- **위치·인용:** `site-baby/assets/emergency.js`의 전체 상자 ③, `chapters/07-hospital.html#emergency`, `chapters/04-crying.html#check`, `#pattern`, `chapters/06-body.html#skin`, `print/emergency.html#main`. ③은 “목록에 없는 변화도 걱정되면 오늘 소아과에 연락하세요”다. 저체온·특이한 울음·눌러도 옅어지지 않는 발진은 공통 7개에 없다.
- **근거 원문:** N090 즉시 도움 항목의 “less than 36C”; N026의 “weak or high-pitched cry”; N001의 “눌러도 사라지지 않는 발진”. [N090] [N026] [N001]
- **위험:** 예를 들어 낮은 체온에 평소와 다른 약한 울음만 있는 아기가 현재 119/즉시 진료 문구에 해당하지 않는 것으로 읽힌다. ‘열이 없어도 다른 신호 확인’이라는 설명만으로 이 신호의 긴급성이 전달되지는 않는다.
- **고칠 문장 제안:** 7장·울음 장과 인쇄표에 “영국 NHS는 체온이 36℃ 미만으로 낮은 경우도 응급 신호로 안내합니다. 몸이 차고 평소와 다르거나, 울음이 매우 약하거나 날카롭게 달라지거나, 눌러도 옅어지지 않는 발진이 있으면 즉시 응급의료 도움을 받으세요”라는 원문 기반 추가 경로를 둔다. 국외 기준·측정 방법을 함께 확인해 표기한다. ③에는 “목록이 모든 응급상황을 담지는 않습니다. 심하게 아파 보이거나 급격히 달라지면 즉시 도움을 요청하세요”를 추가한다. 단순히 모든 목록 밖 증상을 비응급으로 묶지 않는다.

## 수정 — 근거·조건·도구 출력 보완

### M01. 38℃ 안내와 겨드랑이 측정 안내의 관계를 더 분명히 해야 한다

- **위치·인용:** `site-baby/chapters/07-hospital.html#fever`, `practice/06-emergency.html#temperature`, `print/emergency.html#main`. “4주 미만은 겨드랑이 전자체온계로 측정”한 뒤 공통 상자에는 측정 부위 없이 “38.0℃ 이상”이라고 나온다.
- **근거 원문:** N001은 “체온은 측정 부위에 따라 정상 범위가 다릅니다”라고 설명하고, 일반 발열 정의는 직장 38.0℃, 액와는 별도 값으로 서술한다. 이 구분과 3개월 미만 38℃ 즉시 응급실이라는 요약이 같은 문서 안에 있다. 원고의 38℃ 문구 자체는 요약과 일치하지만, 겨드랑이에서 그 값까지 기다리는 규칙으로 만들어서는 안 된다. [N001]
- **고칠 문장 제안:** 기존 즉시 응급실 문구 옆에 “측정 부위에 따라 값과 정확도가 달라요. 겨드랑이에서 38℃가 될 때까지 기다리는 뜻은 아니에요. 아기가 뜨겁거나 평소와 다르면 잰 부위·값을 알려 바로 의료진에게 문의하세요”를 둔다. 임의 환산이나 새 가정용 판정표는 만들지 않는다. 인쇄물에도 짧게 남긴다.

### M02. 관련 장과 실습의 응급 상자가 동일한 범위로 제공되지 않는다

- **위치·인용:** `site-baby/chapters/02-feeding.html#signals`·`#burp`·`#summary`에는 먹기·구토만, `chapters/03-sleep.html#tired`에는 숨·먹기만 나온다. `practice/04-sleep.html#clear`·`#night`, `practice/10-play.html#play`에는 공통 응급 상자가 0개다. 실습 4의 “수유·구토 걱정은 소아과에 말해요”만으로 긴급 신호를 알 수 없다.
- **근거 원문·규칙:** N001의 3개월 미만 발열과 N090의 호흡·반응 신호는 활동에 관계없이 적용된다. 설계 8.4는 “응급 신호는 모든 관련 장에 **같은 문구·같은 신호등 상자**로 반복한다”고 정하고, 11절도 동일 적용을 요구한다. [N001] [N090]
- **고칠 문장·배치 제안:** 먹이기·잠·울음·기저귀·몸·성장과 직접 돌보는 실습에서 읽을 수 있는 공통 응급 상자를 제공한다. 특히 잠 실습·놀이 실습에는 숨·반응/발열/먹지 못함 경로를 넣는다. 상자 앞은 “돌보는 중 아래 신호가 보이면 실습을 멈추고 즉시 연락하세요”로 통일한다. 10장처럼 행정 설명만 있는 쪽에 전체 상자가 없다는 것은 결함으로 세지 않았다.

### M03. 모유 실온 4시간의 국내 문진표 인용 번호가 틀리다

- **위치·인용:** `site-baby/chapters/02-feeding.html#storage`: “국내 검진 문진표의 실온 4시간 이내”에 `[N031]`을 붙였다.
- **근거 원문:** N031은 14~35일용이며 이 문항이 없다. **N032** 4~6개월용 PDF의 영양 교육 3번은 “유축한 모유는 상온에서 최대 4시간까지만 보관 가능한 것을 알고 있습니까?”다. 두 PDF의 실제 화면을 대조했다. [N031] [N032]
- **고칠 문장 제안:** “국내 4~6개월 검진 문진표는 유축 모유 상온 최대 4시간을 안내합니다.[N032]”로 출처와 대상 문진표를 함께 고친다. FACT-SHEET·BRIEFING의 같은 잘못된 N031 연결도 다음 수정 단계에서 정정해야 한다.

### M04. 트림의 손동작은 인용한 N060에 없다

- **위치·인용:** `site-baby/chapters/02-feeding.html#burp`의 본문·그림 캡션, `practice/03-feeding.html#burp`: “영국 NHS는 등을 부드럽게 문지르는 방법을 안내해요.[N060]”
- **근거 원문:** N060은 역류 안내로 “hold your baby upright”, “burp your baby regularly”를 말한다. 머리·목 받침과 등 문지르기의 구체 동작은 이 페이지에 없다. [N060]
- **고칠 문장 제안:** 현재 인용만 유지할 때는 “NHS는 수유 중·뒤에 아기를 세워 안고 트림을 돕도록 안내해요”까지로 한정한다. 손동작 실습·그림은 실제 동작을 설명하는 별도 공식 원문을 확인하고 그 근거를 붙인 뒤 유지한다. 동작이 위험하다고 단정한 발견이 아니라 인용한 원문이 동작을 입증하지 못한다는 발견이다.

### M05. 청각 ‘1·3·6개월’ 중 3·6개월은 N035에서 대조되지 않는다

- **위치·인용:** `site-baby/chapters/08-growth.html#screening`: “1개월 안에 선별, … 3개월 안에 확진, 6개월 안에 중재”; `chapters/01-map.html#handover`의 3개월 확진 목표. 둘 다 `[N035]`다.
- **근거 원문:** N035의 검사시기는 “출생 후 1개월 이내 검사 실시”이고, 나머지는 비용 지원 안내다. 3개월 확진·6개월 중재 목표는 이 URL 본문에 없다. N031·N032의 청각 문항에는 미숙아의 경우 **출생 예정일 기준**이라는 예외가 있다. [N035] [N031] [N032]
- **고칠 문장 제안:** 현 근거만 사용할 때는 “퇴원 전 선별검사 여부·결과·재검 필요를 확인하고, 놓쳤다면 지금 병원에 검사·확진·중재 계획을 문의하세요. 미숙아는 적용 시기를 담당 병원에 확인하세요.” 3·6개월 목표를 유지하려면 이를 명시한 공식 원문을 추가 확인한다. 목표 자체가 거짓이라고 판정한 것은 아니다.

### M06. 태아당 진료비 추가지원의 인용을 보완해야 한다

- **위치·인용:** `site-baby/chapters/10-benefits.html#voucher`: “추가 신청하면 태아당 100만 원 수준으로 지원합니다.[N036][N107]”
- **근거 원문:** N107에는 일태아 100만·다태아 기본 140만원과 사용기한만 있고 태아당 추가 지급 내용은 없다. 기존 SOURCES의 N045는 “태아 당 100만원이 되도록 추가 지급(2태아: 60만원, 3태아: 160만원 등)”을 명시한다. 추가 원문도 이번에 직접 열었다. [N107] [N045]
- **고칠 문장 제안:** “다태아 기본액은 140만원이고, 추가지급 대상이면 별도 신청으로 태아당 100만원이 되도록 더 지원합니다.[N107][N045] 적용 조건·서류는 공단에 확인하세요.” 현재 금액이 틀린 것이 아니라 해당 절의 출처 연결이 불충분하다.

### M07. 실습 일정 도구가 입력 변경 후에도 이전 아기·경로 결과를 남긴다

- **위치·인용:** `site-baby/practice/08-checkups.html#schedule-tool`, `assets/p08.js`. 출력 예: “B형간염 단독 · 1개월: 2026-09-01”, “로타 … 2026-11-13”.
- **재현:** 출생일 `2026-08-01`·단독 경로로 계산 → 출생일을 `2026-09-01`·6가 경로로 바꾸되 재계산 버튼은 아직 누르지 않는다. 화면의 결과는 이전 결과와 바이트 단위로 같다. 새 출생일의 로타 14주 6일은 `2026-12-14`지만 화면은 `2026-11-13`을 유지하고 단독 1개월 일정도 남는다. 9장 도구는 입력이 바뀌면 이전 결과를 비우므로 동작도 서로 다르다.
- **근거 원문:** N027 로타 상한은 “생후 14주 6일”이고, 6가 분기는 “생후 1개월에 … 단독백신 2차 접종을 시행하지 않음”이다. [N027]
- **고칠 출력 제안:** 입력·선택 변경 즉시 이전 표를 비우고 “입력이 바뀌었어요. 날짜 확인하기를 다시 눌러 주세요”를 표시한다. 결과 첫 줄에 계산에 실제 사용한 출생일·경로도 함께 보여 준다. 실험실에 재사용된 같은 도구에도 적용한다.

### M08. 울음 증가 시기의 만삭·미숙아 조건을 생략했다

- **위치·인용:** `site-baby/chapters/01-map.html#overview`·`#next`, `chapters/04-crying.html#pattern`·`#story`: “생후 6~8주 무렵 많아졌다가 줄어드는 흐름”.
- **근거 원문:** N024는 “for a term baby”와 “after their due date for a premature baby”를 구분한다. SOURCES N024에도 같은 한계가 기재되어 있다. N023은 울음 증가를 설명하지만 이 6~8주·미숙아 구분을 대신 입증하지 않는다. [N024] [N023]
- **고칠 문장 제안:** “영국 안내는 만삭아는 생후 6~8주, 미숙아는 출산 예정일을 기준으로 그 무렵 울음이 많아질 수 있다고 설명합니다. 개인의 마감표는 아닙니다.” 반복되는 FAQ·지도 캡션에도 이 조건으로 읽을 수 있게 연결한다.

### M09. 지역상품권으로 지급되는 아동수당도 도구가 ‘현금’에 넣을 수 있다

- **위치·인용:** `site-baby/chapters/10-benefits.html#cash`, `#benefits-tool`, `assets/ch10.js`의 `child`, `monthly`: “아동수당 현금”, “월 현금 합계”. 입력은 지역 분류뿐이고 지급 수단을 받지 않는다.
- **근거 원문:** N095는 “현금입금 원칙”과 조례에 따른 “지역상품권으로도 지급가능”을 함께 명시한다. N105는 해당 인구감소지역에서 상품권 지급 시 추가 1만원을 설명한다. 이때 기본액까지 모두 현금이라고 보장할 수 없다. [N095] [N105]
- **재현·문제:** 첫째·가정양육·인구감소 특별지역을 선택하면 0세 행은 부모급여 100만원+아동수당 12만원=‘월 현금 112만원’이다. 해당 지역이 상품권 지급 방식인 경우에는 아동수당 기본액도 현금 통장 입금이 아니다. 추가 1만원만 합계에서 빼는 방식은 지급 수단 혼동을 해결하지 못한다. 지역을 모를 때 합계를 ‘확인 필요’로 두는 처리는 적절하다.
- **고칠 출력 제안:** 지급 방식이 확인되지 않은 지역은 “아동수당 12만원 · 현금/지역상품권 확인 필요”, “월 현금 합계 확인 필요”로 둔다. 또는 현금 지급이라고 확인한 가정이라는 조건을 명시적으로 선택하게 하고 상품권은 별도 칸으로 분리한다. 특정 지역의 실제 지급 수단을 이번 검토에서 확정한 것은 아니다.

## 권고

### R01. 성장도표의 WHO 도입 세부 근거는 대조 불가로 남는다

- **위치·인용:** `site-baby/chapters/08-growth.html#weight`: “현재 국내 도표는 2017판입니다. 0~35개월에는 WHO 성장표준을 도입했습니다.[N033][N079]”; `credits.html#n079`.
- **근거 원문 발췌:** **N079는 대조 불가**. SOURCES에 기록된 URL이 urllib와 웹 도구 모두 404다. N033의 공개 메인은 성장 평가 도표라는 성격과 공동 제정을 확인해 주지만, 해당 연령의 도입 상세를 보여 주지는 않는다. 이전 조사 기록이나 검색 스니펫을 이번 직접 원문 대조 성공으로 세지 않았다. [N079] [N033]
- **고칠 문장 제안:** 검증 가능한 공식 개발 보고서·공식 도표 설명을 확보해 인용을 교체한다. 확보 전에는 “성별·정확한 나이에 맞는 공식 성장도표로 이전 측정값과 함께 상담합니다”로 한정한다. 현 주장 자체를 거짓이라고 판정하지는 않는다.

### R02. 인쇄 주차표에서 B형간염 경로 확인을 한 달보다 앞에 배치한다

- **위치·인용:** `site-baby/print/weekly-checklist.html#main`의 “5주 35~41일 … B형간염 단독/6가 경로 확인”. 아래 별도 줄에는 단독 1개월 일정이 적혀 있다.
- **근거 원문:** N027은 “생후 0개월, 1개월, 6개월에 3회 기초접종”과 6가 경로의 분기를 명시한다. [N027]
- **문제:** 상단에 ‘해당 주까지 기다리지 말라’는 보완 문장이 있어 틀린 접종 일정으로 단정하지는 않았다. 다만 행 순서대로 체크하는 독자는 경로 결정을 뒤늦게 할 수 있다.
- **고칠 문장 제안:** 퇴원·0주 행에 “출생 접종·산모 검사와 B형간염 다음 경로 확인”, 3~4주 행에 “단독이면 1개월 접종일 확인”을 두고 5주 행은 이행 여부 재확인으로 바꾼다.

### R03. 6+6 현재 금액 각주는 과거 답변과 분리한다

- **위치·인용:** `site-baby/chapters/10-benefits.html#leave`: “월별 상한 250·250·300·350·400·450만 원.[N046][N048]”
- **근거 원문:** N048 상단의 2025-04-21 답변에는 “(1개월째)200만원”이 남아 있고, N046 현행 고용24 안내에는 “첫 1개월: 250만원”이 있다. SOURCES N048은 과거 답변 혼재를 이미 명시한다. [N048] [N046]
- **고칠 문장 제안:** 현재 금액에는 N046을 붙이고 N048은 공통 사용기간 등의 해당 설명에만 붙인다. 출처 페이지에도 “과거 금액 답변이 섞여 있어 현재 금액은 고용24 기준”이라는 구분을 유지한다. 현재 원고의 250만원이 잘못됐다는 지적은 아니다.

## 응급 문구 일관성·누락 전수 결과

BRIEFING ④에서 채택한 7문장을 `emergency-data.js`와 문자열로 대조했다. **7/7 일치**했고, JS를 켠 33쪽의 실제 렌더링 **93회 모두 원본과 일치**했다. 공통 상자와 별개로 FAQ·요약·그림에 같은 행동을 짧게 풀어쓴 곳도 읽었다. 안심 판정으로 뒤집은 FAQ는 찾지 못했으나, B02~B04의 좁은 기준이 공통 데이터에서 여러 쪽으로 전파된다.

| 관련 이론 장 | 실제 표시된 공통 신호 | 판단 |
|---|---|---|
| 1 지도 | 숨·먹기 | 소개용 일부 안내 있음 |
| 2 먹이기 | 먹기·구토 | 발열·호흡 경로까지 즉시 읽도록 보완 M02 |
| 3 잠 | 숨·먹기 | 발열 경로 보완 M02 |
| 4 울음 | 7개 전체 + 부모 위기 | 원본은 같음, 특이 울음의 긴급성은 B04 |
| 5 기저귀 | 7개 전체 + 관련 신호 | 상자 누락 없음 |
| 6 몸 | 7개 전체 + 배꼽 | 상자 누락 없음, 추가 피부 응급은 B04 |
| 7 병원 | 7개 전체 + 각 축 | 원문 조건·추가 응급 B02~B04 |
| 8 성장 | 7개 전체 + 먹기 | 상자 누락 없음 |
| 9 접종·검진 | 7개 전체 | 상자 누락 없음 |
| 10 서류·돈 | 없음 | 행정 장에 전체 응급표를 요구하지 않음 |
| 11 부모 | 부모 위기 | 영아 표와 별도로 부모 연락 카드 있음 |
| 12 안전 | 숨·발열 | 관련 안내 있음 |
| 13 백일 | 숨·먹기 | 관련 안내 있음 |

실습 2는 황달·먹기, 3은 먹기·구토, 5는 배꼽, 6은 다섯 사례별 신호, 7은 전체, 9는 먹기, E2E는 부모 위기다. **직접 돌보는 실습 4·10은 공통 신호 0개**다(M02). 실습 0·1·8은 연락처·환경·예약 중심이며 전체 응급표가 없다는 이유만으로 추가 결함을 만들지는 않았다. 인쇄 응급표는 정상 JS 환경에서 7개 모두 나타나고, 부모 위기 카드는 해당 문구와 연락 역할을 함께 제공한다.

“38℃ 미만이면 안전”, 3개월=90일, 100일=3개월, 1개월=30일이라는 **긍정형 치환·안전 판정은 찾지 못했다**. 이런 표현을 금지하거나 퀴즈 오답으로 제시한 경우는 위반으로 세지 않았다. 날짜 도구는 달력 월과 일수를 분리하며 로타 상한을 출생일+104일로 계산한다. 신고 1개월 말일·휴일, 검진 개인 종료일은 확정 기한이 아닌 기관 대조용이라고 표시한다. 개별 기관 대상조회·휴일 연장 법률 계산을 실제로 검증했다는 뜻은 아니다.

## 상충 19개·미확인 6개 처리

FACT-SHEET에서 `상충`인 **19개를 모두** 현재 사이트의 사용·미사용과 연결했다. 단순히 해외 숫자를 국내 기준으로 바꾼 경우는 찾지 못했다. 다만 M03·M08·R03처럼 인용 번호·적용 대상·과거 자료 구분을 보완해야 한다.

| 사실 항목 | 현재 처리와 판정 |
|---|---|
| FEED-04 혼합수유 | 2장에 국내/영국 차이와 개별 계획 공개. 적절 |
| FORM-02 조유수 | 국내70℃ 기본·미국 고위험군 구분·특수분유 상담. 적절 |
| FORM-08 분유 총량 | kg당 범위와 하루 상한을 원고에 사용하지 않음. 권장량 계산기도 없음 |
| MILK-02 모유 보관 | 차이 공개·미국 온도 조건 표 채택은 적절. 국내 문진표 인용은 M03 |
| MILK-03 해동·남은 모유 | 차이 공개 후 국내 남은 모유 폐기 채택. 적절 |
| SLEEP-03 속싸개 | 국내 불사용·AAP 조건부·첫 뒤집기 시도 중단. 적절 |
| SLEEP-04 공갈젖꼭지 | 국내 초기 비권장·AAP 모유수유 정착 후 고려. 적절 |
| SLEEP-08 SIDS 발생률 | 충돌하는 발생률은 쓰지 않음. 별도 사망통계의 연도·분모는 유지 |
| DIAPER-02 초기 횟수 | 국가·일령·최소/범위·재질을 분리. 적절 |
| BODY-03 목욕 시점 | 배꼽 전 부분 씻기·NHS 조건 차이 공개, WHO 첫 목욕과 구분. 적절 |
| BODY-09 목욕물 | 두 국내 안내를 나누고 37~38℃ 기본 선택. 합쳐서37~40℃로 쓰지 않음 |
| JAUND-03 태양광 | 황달 진료를 햇볕으로 대체하라는 안내 없음 |
| GROW-01 체중 회복 | 국내/AAP 수치·평가 차이 공개, 허용 감량 목표로 쓰지 않음 |
| PARENT-08 카페인 | 국내/NHS/CDC 차이·어린 신생아/미숙아 조건 공개. 잔수 계산 없음 |
| PARENT-10 음주 | 차이 공개·피하는 쪽과 개별 상담 채택. 음주 안전시간 계산 없음 |
| PARENT-11 EPDS | 점수 숫자를 원고·도구에 쓰지 않음. 점수로 진단하지 않도록 설명 |
| SAFE-06 온습도 | 국내/영국 온도 차이·과열 예방 공통 행동. 임의 범위 병합 없음 |
| INFECT-08 백일해 통계 | 1613/323 누적값 모두 사용하지 않음 |
| NEXT-02 이유식 | 국내 수유형태별/WHO·CDC 차이 공개·백일 시작 배제. 적절 |

`미확인` 6개도 확인했다. FORM-09 보충 순서·양은 상담으로, SLEEP-07 통잠·수면교육 시작일은 상담으로, VAX-08 RSV 무료 대상·비용은 기관 확인으로, CHECK-07 대사 채혈 시각은 출생병원 확인으로, INFECT-04 외출 시기는 개별 상황 상담으로 안내한다. MILK-05 철분 시작일은 원고에 숫자로 제시하지 않는다. **이 6개를 확정 숫자·보장 문장으로 사용한 사례는 발견하지 못했다.** 별도로 N035의 청각 목표는 조사표가 ‘확인’으로 분류했더라도 인용 URL의 직접 대조가 되지 않는 문제로 M05에 남겼다.

## 금지 항목과 위험한 생략

| 점검 | 결과 |
|---|---|
| 아기 약 이름·용량·해열제 계산 | 본문·실습·도구·인쇄·퀴즈에 없음. 소아과·약사 문의로 연결 |
| 상품 브랜드 추천 | 없음. 백신 성분 약어·공식 서비스명은 상품 추천으로 세지 않음 |
| EPDS 점수·계산 | 없음. 출처 페이지의 EPDS 자료명은 점수 판정이 아님 |
| 분유 권장량 자동 계산 | 없음. 실제 먹은 mL 기록은 처방 계산과 구분 |
| 자체 대변 진단 색표 | 없음. 변 흐름은 문자 중심 개념도이고 공식 카드 확인으로 연결 |
| 백일 이유식·통잠 달성 | 목표로 제시하지 않음 |
| 평균·범위를 개인 목표로 사용 | 수유·수면·체중·터미타임에 범위/권고 대상·개별 차이 설명 있음 |
| 진단·‘집에서 지켜봐도 됨’ 출력 | 도구에 없음. 관찰·준비 개수와 연락 행동만 안내. 단 B02~B04의 조건/분류 문제는 별개 |
| 미숙아·입원·특수분유 | 모유 보관·분유 조유·접종·지원 서비스에서 예외 안내 있음. 울음 시기 M08·청각 M05 보완 |
| 다태아 | 건강관리 지원 예외·출산휴가 기간 분리. 추가 진료비 인용 M06 보완 |
| 뒤보기 카시트 | 본문·그림·실습에서 뒤보기/뒷좌석/제품·차량 조건 표시. 법의 장구 의무와 권고 구분 |
| 체온 측정 부위 | 7장·실습6·기록지에 부위/시각 기록. 공통 38℃ 상자의 해석은 M01 |
| 부모 위기 | 109/1577-0199 역할 구분·임박한 위해119/112·환청/망상 즉시평가. 가해 진단·점수 판정 없음 |

39개 퀴즈는 각 장의 정답·오답·피드백을 확인했다. 위험한 행동을 정답으로 지정한 사례는 발견하지 못했다. ‘세게 흔들기’, ‘뜨거울 때 먹이기’, ‘범위 상한까지 줄어도 괜찮음’ 등은 오답으로 표시된 것이므로 금지 위반으로 집계하지 않았다. 참고값이 포함된 캡션·FAQ에서도 위의 B/M 발견과 같은 조건을 적용한다.

## 도구 개인정보·출력 검사

- 정적 코드에서 `fetch`, XHR, `sendBeacon`, WebSocket, EventSource, 외부 폼 제출 및 외부 리소스 URL을 확인했다. 돌봄 데이터를 전송하는 경로는 찾지 못했다. `postMessage` 등의 외부 전송 경로도 없고, 같은 출처 프레임의 이벤트·리사이즈·로컬 상태 공유만 있다.
- Chromium에서 **33쪽·15개 도구를 방문**, 폼 입력·제출·선택 변경·기록 추가를 실행했다. 요청 이벤트와 통신 API 호출을 함께 계측한 결과 **외부 요청 0, 비GET 요청 0, 통신 API 호출 0, 페이지 JS 오류 0**이었다. 페이지 자산을 읽는 같은 출처 GET은 별개다. 공식 출처 링크를 사용자가 눌러 외부 기관을 방문하는 행동은 데이터 자동 전송으로 세지 않았다.
- 출생일 계산은 현재 화면에서만 처리한다. 연락처·신청 상태·예약·돌봄 기록은 `babybook:` localStorage에만 저장하는 구현이다. 기록 요약은 입력 횟수이며 충분한 수유·정상 발달·안전 판정을 출력하지 않는다. 교대표의 휴식은 예정 구간이며 실제 수면 보장으로 읽지 않도록 표시한다.
- CSV 내보내기는 브라우저 Blob 다운로드이며 업로드 요청이 없다. 기록 삭제·저장 접근 실패 안내와 저장 제한 처리도 코드에서 확인했다. 이 검토는 설치된 브라우저 확장·기기 운영체제·실제 운영 서버의 별도 기능까지 검증한 것은 아니다.
- **일정 도구의 이전 결과 잔류 M07**, **현금/상품권 출력 M09**는 위의 통신 안전성과 별개인 출력 안전 결함이다.
- 인쇄 4종을 이번 브라우저에서 PDF로 만들었고 각각 **A4 1쪽**이었다. 정상 응급 인쇄표의 7개 신호와 연락처는 실제 렌더링에서도 확인했다. JS 비활성의 공백 B01은 남아 있다. 실제 프린터 출력은 하지 않았다.

## 주장 대조표

‘보완’은 원문을 열었지만 인용·대상·행동이 부족하거나 좁아 해당 발견으로 연결된 경우다. ‘대조 불가’는 원문에 접근하지 못해 진위를 확정하지 않은 경우다. 아래에는 반복을 묶은 주장과 대표 위치를 적었다. 같은 사실의 FAQ·그림·실습 재등장은 해당 단위에 포함한다. 프로그램 결함 B01·M07, 배치 문제 M02, 권고는 원문 주장 수와 별도로 센다.

| 번호 | 영역 | 대표 위치 (`site-baby/` 기준) | 대조 주장 | 직접 열람 원문 | 결과 |
|---|---|---|---|---|---|
| C001 | 먹이기 | `chapters/02-feeding.html#signals` | 초기 모유수유 하루 8~12회, 고정 간격·개인 목표로 쓰지 않음 | [N004] [N005] [N018] | 일치 |
| C002 | 먹이기 | `chapters/02-feeding.html#ways` | 입 크게 벌려 깊이 물리고 몸·머리 정렬 | [N005] [N016] | 일치 |
| C003 | 먹이기 | `chapters/02-feeding.html#signals` | 삼킴·기저귀·체중·활력을 함께 봄 | [N005] [N017] [N019] | 일치 |
| C004 | 먹이기 | `chapters/02-feeding.html#signals` | 체중 회복 전·황달·미숙아 수유 계획은 병원 확인 | [N005] [N019] | 일치 |
| C005 | 먹이기 | `chapters/02-feeding.html#ways` | 혼합수유 국내외 차이와 필요한 보충의 개별 상담 | [N004] [N089] | 일치 |
| C006 | 먹이기 | `chapters/02-feeding.html#ways` | 미국 분유 첫 주 30~60mL·첫 달 90~120mL 참고 예 | [N013] | 일치 |
| C007 | 먹이기 | `chapters/02-feeding.html#ways` | 분유 보충 순서·하루량을 자동 처방하지 않음 | [N004] [N013] [N089] | 일치 |
| C008 | 분유 | `chapters/02-feeding.html#prepare` | 국내 조유 70℃ 이상, 먹이기 전 식히기 | [N010] [N011] | 일치 |
| C009 | 분유 | `chapters/02-feeding.html#prepare` | 물 먼저·제품 전용 스푼·비율 준수 | [N012] | 일치 |
| C010 | 분유 | `chapters/02-feeding.html#prepare` | 미국 추가 가열 대상 2개월 미만·미숙아·면역저하 구분 | [N010] [N012] | 일치 |
| C011 | 분유 | `chapters/02-feeding.html#prepare` | 특수분유 의료진·제품 지시 확인 | [N010] [N012] | 일치 |
| C012 | 분유 | `chapters/02-feeding.html#storage` | 조제 후 2시간·먹이기 시작 후 1시간 중 빠른 시각 | [N010] [N012] | 일치 |
| C013 | 분유 | `chapters/02-feeding.html#storage` | 먹다 남은 분유 폐기 | [N010] [N012] | 일치 |
| C014 | 분유 | `chapters/02-feeding.html#storage` | 먹이지 않고 바로 냉장한 예외 5℃ 이하·24시간 | [N010] | 일치 |
| C015 | 분유 | `practice/03-feeding.html#panel-formula` | 전자레인지 가열 피하기·먹이기 전 온도 확인 | [N012] | 일치 |
| C016 | 위생 | `chapters/02-feeding.html#prepare` | 매 수유 후 부품 분리·전용 대야·세척·헹굼·자연 건조 | [N011] [N015] | 일치 |
| C017 | 위생 | `chapters/02-feeding.html#prepare` | 소독은 세척 다음, 2개월 미만 등 매일 추가 소독 | [N015] | 일치 |
| C018 | 모유 | `chapters/02-feeding.html#storage` | 만삭아 가정용 미국 표 실온 25℃ 이하 4시간 | [N014] | 일치 |
| C019 | 모유 | `chapters/02-feeding.html#storage` | 갓 유축 냉장 4℃ 4일 | [N014] | 일치 |
| C020 | 모유 | `chapters/02-feeding.html#storage` | 냉동 −18℃ 이하 6개월 권장·12개월 허용 | [N014] | 일치 |
| C021 | 모유 | `chapters/02-feeding.html#storage` | 미숙아·입원아 병원 지침 우선 | [N014] | 일치 |
| C022 | 모유 | `chapters/02-feeding.html#storage` | 국내 서늘한 실온 8~10시간·냉장 최대 8일/3일 권장 | [N004] | 일치 |
| C023 | 모유 | `chapters/02-feeding.html#storage` | 국내 검진 문진표 실온 4시간의 N031 인용 | [N031] [N032] | 보완 M03 |
| C024 | 모유 | `chapters/02-feeding.html#storage` | 완전 해동 후 냉장 24시간·데운 뒤 2시간 | [N014] | 일치 |
| C025 | 모유 | `chapters/02-feeding.html#storage` | 남은 모유 국내 폐기·미국 2시간 차이, 책은 폐기 채택 | [N004] [N014] | 일치 |
| C026 | 모유 | `chapters/02-feeding.html#storage` | 재냉동·전자레인지 해동 피하기 | [N004] [N014] | 일치 |
| C027 | 트림 | `chapters/02-feeding.html#burp` | 깨어 세워 안기·평평한 등 수면, 역류 때문에 경사 만들지 않기 | [N060] | 일치 |
| C028 | 트림 | `practice/03-feeding.html#burp` | 머리·목 받치고 등 문지르기의 N060 인용 | [N060] | 보완 M04 |
| C029 | 수면 | `chapters/03-sleep.html#space` | 등 대고 단단하고 평평한 빈 잠자리 | [N002] [N031] [N056] | 일치 |
| C030 | 수면 | `chapters/03-sleep.html#space` | 같은 방 별도 잠자리 최소 6개월·가능하면 1년 | [N002] [N020] | 일치 |
| C031 | 수면 | `chapters/03-sleep.html#rhythm` | 낮 빛·일상 소리, 밤 조도·자극 줄이기 | [N022] | 일치 |
| C032 | 수면 | `chapters/03-sleep.html#rhythm` | WHO 낮잠 포함 0~3개월 14~17시간·4~11개월 12~16시간 | [N092] | 일치 |
| C033 | 수면 | `chapters/03-sleep.html#items` | 국내 속싸개 불사용과 AAP 조건부 사용 차이 | [N031] [N020] [N093] | 일치 |
| C034 | 수면 | `chapters/03-sleep.html#items` | 뒤집기 첫 시도부터 속싸개 중단·무게 있는 제품 피함 | [N020] [N093] | 일치 |
| C035 | 수면 | `chapters/03-sleep.html#items` | 공갈젖꼭지 국내 초기 비권장·AAP 모유수유 정착 후 고려 | [N031] [N020] [N063] | 일치 |
| C036 | 수면 | `chapters/03-sleep.html#items` | 억지로 물리기·잠든 뒤 재삽입·끈 피함 | [N020] | 일치 |
| C037 | 수면 | `chapters/03-sleep.html#tired` | 졸리면 소파·의자에서 안고 잠들기 피함 | [N002] [N020] | 일치 |
| C038 | 수면 | `chapters/03-sleep.html#tired` | 바운서·역류방지쿠션·카시트는 일상 침대 대체 불가 | [N031] [N056] | 일치 |
| C039 | 통계 | `chapters/03-sleep.html#space` | 2025 관측 SIDS 31명/영아사망 512명 6.1%, 출생아 위험률 아님 | [N091] | 일치 |
| C040 | 울음 | `chapters/04-crying.html#pattern` | 6~8주 울음 증가의 만삭·미숙아 시간 기준 | [N023] [N024] | 보완 M08 |
| C041 | 울음 | `chapters/04-crying.html#pattern` | NHS 산통 가능성 3시간·주3일·최소1주와 다른 원인 평가 | [N026] | 일치 |
| C042 | 울음 | `chapters/04-crying.html#comfort` | 먹기·기저귀·온도·피로 점검, 부드럽게 안고 말 걸기 | [N023] | 일치 |
| C043 | 울음 | `chapters/04-crying.html#pause` | 절대로 흔들지 않기, 안전하게 내려놓고 잠시 진정·교대 | [N025] [N023] | 일치 |
| C044 | 기저귀 | `chapters/05-diapers.html#counts` | 약 1주 천기저귀 6~8·일회용 5~6·대변 3~4, 재질·수유 조건 | [N005] | 일치 |
| C045 | 기저귀 | `chapters/05-diapers.html#counts` | CDC 초기 최소 소변 1/2/5/6/6·대변 1/3/3/3/3 | [N018] | 일치 |
| C046 | 기저귀 | `chapters/05-diapers.html#counts` | NHS 생후 5일부터 젖은 기저귀 6개 이상, 미국 표와 구분 | [N017] | 일치 |
| C047 | 기저귀 | `chapters/05-diapers.html#stools` | 태변·이행변·모유/분유변 차이와 초록색만으로 진단 안 함 | [N017] [N102] | 일치 |
| C048 | 기저귀 | `chapters/05-diapers.html#stools` | 흰색·회백색 변 즉시 의료진, 사진·비교로 지체하지 않음 | [N003] [N031] | 일치 |
| C049 | 기저귀 | `chapters/05-diapers.html#stools` | 태변 이후 타르흑색·피 보이는 변 진료, 많은 피는 응급실 | [N110] | 일치 |
| C050 | 기저귀 | `chapters/05-diapers.html#stools` | 초기 검진 문진표의 변 색 질문, 모든 수첩 카드 보급으로 단정 안 함 | [N031] | 일치 |
| C051 | 기저귀 | `chapters/05-diapers.html#change` | 손 씻기·높은 교환대 혼자 두지 않기·여아 앞→뒤·포피 강제로 젖히지 않기 | [N102] | 일치 |
| C052 | 피부 | `chapters/05-diapers.html#change` | 발진 예방 자주 갈기·부드러운 세정·완전 건조 | [N051] | 일치 |
| C053 | 목욕 | `chapters/06-body.html#bath` | 국내 배꼽 탈락 전 부분 씻기, NHS 조건 차이 구분 | [N007] [N059] | 일치 |
| C054 | 목욕 | `chapters/06-body.html#bath` | 물품 먼저·아기 혼자 두지 않기·머리와 몸 지지 | [N008] [N059] | 일치 |
| C055 | 목욕 | `chapters/06-body.html#bath` | 아이사랑 안전 물 37~38℃, 호주 번역 표시 | [N008] | 일치 |
| C056 | 목욕 | `chapters/06-body.html#bath` | 같은 포털 38~40℃·방 24~26℃ 차이, 범위 합치지 않음 | [N111] [N008] | 일치 |
| C057 | 목욕 | `chapters/06-body.html#bath` | WHO 건강한 만삭아 첫 목욕 24시간 이후, 제대 후 통목욕과 구분 | [N103] | 일치 |
| C058 | 배꼽 | `chapters/06-body.html#navel` | 1~2주 탈락 참고·건조·청결·억지로 떼지 않음 | [N007] | 일치 |
| C059 | 배꼽 | `chapters/07-hospital.html#navel` | 붉고 아파야 한다는 복합 조건의 문제 | [N007] | 보완 B02 |
| C060 | 배꼽 | `chapters/07-hospital.html#navel` | 고름·악취 진료, 지속 출혈 즉시 진료 | [N007] | 일치 |
| C061 | 피부 | `chapters/06-body.html#skin` | 지루성 피부염 부드러운 세정·보습·딱지 억지로 벗기지 않음 | [N050] | 일치 |
| C062 | 피부 | `chapters/06-body.html#skin` | 신생아 여드름 자연 경과·짜기와 성인 치료제 피함 | [N088] | 일치 |
| C063 | 손톱 | `chapters/06-body.html#skin` | 움직임 안정시켜 조심스럽게 손톱 다듬기 | [N059] | 일치 |
| C064 | 응급 | `chapters/07-hospital.html#fever` | 생후 달력 3개월 미만 38℃ 이상, 좋아 보여도 즉시 응급실 | [N001] | 일치 |
| C065 | 체온 | `chapters/07-hospital.html#fever` | 4주 미만 겨드랑이 전자체온계·6개월 미만 귀 측정 오차 | [N001] | 일치 |
| C066 | 체온 | `chapters/07-hospital.html#fever` | 측정 부위와 38℃의 관계, 단일 문구로 액와 대기 기준을 만들 위험 | [N001] | 보완 M01 |
| C067 | 응급 | `chapters/07-hospital.html#breathing` | 호흡곤란·청색증·경련 즉시 119, 열이 없어도 적용 | [N001] [N085] [N090] | 일치 |
| C068 | 응급 | `chapters/07-hospital.html#breathing` | 깨우기 어려움보다 반응 거의 없음으로 좁힌 조건 | [N090] | 보완 B02 |
| C069 | 응급 | `chapters/07-hospital.html#feeding` | 수유 저하와 소변 감소를 결합한 조건 | [N001] [N090] | 보완 B02 |
| C070 | 응급 | `chapters/07-hospital.html#jaundice` | 황달 악화에 수유 저하를 추가한 조건·지속 황달 누락 | [N003] | 보완 B02 |
| C071 | 응급 | `chapters/07-hospital.html#jaundice` | 첫날 황달·흰 변·색만으로 수치/원인 확정하지 않기 | [N003] [N031] | 일치 |
| C072 | 응급 | `chapters/07-hospital.html#vomit` | 분수 구토 반복 조건·노란 구토 생략 | [N060] | 보완 B03 |
| C073 | 응급 | `print/emergency.html#main` | 목록 밖 모든 변화를 ‘오늘 문의’로 묶을 위험 | [N001] [N026] [N090] | 보완 B04 |
| C074 | 연락 | `chapters/07-hospital.html#where` | 119 상담·이송, E-gen/달빛 기관 찾기와 전화 재확인 | [N001] [N069] | 일치 |
| C075 | 연락 | `chapters/07-hospital.html#where` | 약 종류·양은 아기 나이·체중 알려 의료진/약사 문의 | [N001] | 일치 |
| C076 | 기록 | `chapters/07-hospital.html#workshop` | 나이·체온 시간/부위·수유/소변 변화 전하기, 기록 때문에 지연 안 함 | [N001] [N073] | 일치 |
| C077 | 성장 | `chapters/08-growth.html#weight` | 국내 체중 감소 5~10%·7~10일과 AAP 7~14일·10% 초과 평가 차이 | [N009] [N019] | 일치 |
| C078 | 성장 | `chapters/08-growth.html#weight` | 2017판·0~35개월 WHO 성장표준 도입 세부 | [N033] [N079] | 대조 불가 R01 |
| C079 | 성장 | `chapters/08-growth.html#weight` | 성별·나이·연속 측정 흐름, 백분위를 합격 점수로 쓰지 않음 | [N033] [N009] | 일치 |
| C080 | 발달 | `chapters/08-growth.html#development` | 문진표의 눈맞춤·소리·웃음 관찰, 백일 완료표로 쓰지 않음 | [N009] [N031] [N032] | 일치 |
| C081 | 놀이 | `chapters/08-growth.html#play` | 깨어 보호자 곁 터미타임, 졸리면 등 수면으로 옮김 | [N032] [N092] [N002] | 일치 |
| C082 | 놀이 | `chapters/08-growth.html#play` | WHO 비이동 영아 하루 총 30분 이상 여러 번, 첫날 강제 목표 아님 | [N092] | 일치 |
| C083 | 선별 | `chapters/08-growth.html#screening` | 청각·대사 검사 시행/결과/재검을 검진과 별도 확인 | [N031] [N034] [N035] | 일치 |
| C084 | 선별 | `chapters/08-growth.html#screening` | 청각 재검은 확진과 구분 | [N031] [N034] | 일치 |
| C085 | 선별 | `chapters/08-growth.html#screening` | 청각 1·3·6개월 목표의 N035 인용과 미숙아 조건 | [N035] [N031] [N032] | 보완 M05 |
| C086 | 선별 | `chapters/08-growth.html#screening` | 대사검사 채혈 시각 일률 단정 안 함, 병원·보건소 확인 | [N034] | 일치 |
| C087 | 접종 | `chapters/09-checkups.html#schedule` | B형간염 단독 출생·1·6개월 | [N027] | 일치 |
| C088 | 접종 | `chapters/09-checkups.html#schedule` | 출생 접종 뒤 6가 2·4·6개월, 1개월 생략 분기 | [N027] | 일치 |
| C089 | 접종 | `chapters/09-checkups.html#schedule` | 산모 양성·미숙아·기접종은 개인 계획 확인 | [N027] | 일치 |
| C090 | 접종 | `chapters/09-checkups.html#schedule` | BCG 피내 4주 이내 | [N027] | 일치 |
| C091 | 접종 | `chapters/09-checkups.html#schedule` | 2·4개월 DTaP·IPV·Hib·폐렴구균·로타, 성분 중복 피함 | [N027] | 일치 |
| C092 | 접종 | `chapters/09-checkups.html#schedule` | 로타 2·4 또는 2·4·6개월, 초회 14주6일·전 과정 8개월0일 | [N027] | 일치 |
| C093 | 접종 | `chapters/09-checkups.html#cost` | 지정기관·대상·지원 백신 무료, 경피 BCG와 구별 | [N027] [N028] | 일치 |
| C094 | 접종 | `chapters/09-checkups.html#cost` | 로타 다른 국가접종과 동시 가능, 개인 금기 의료진 확인 | [N027] | 일치 |
| C095 | 접종 | `chapters/09-checkups.html#cost` | RSV 항체·백신·급여/무료 구별, 전체 무료 단정 안 함 | [N027] [N076] | 일치 |
| C096 | 접종 | `practice/08-checkups.html#find` | 접종도우미 내역·기관 조회, 모든 접종 온라인 예약으로 단정 안 함 | [N028] | 일치 |
| C097 | 검진 | `chapters/09-checkups.html#booking` | 1차 생후 14~35일·2차 4~6개월 | [N007] [N030] [N031] [N032] | 일치 |
| C098 | 검진 | `chapters/09-checkups.html#booking` | 대상·지정기관·유효기간 안 무료 검진 | [N029] [N030] | 일치 |
| C099 | 검진 | `practice/08-checkups.html#find` | 건보 대상조회·기관 찾기·문진표 안내, 전화로 예약 | [N029] [N066] | 일치 |
| C100 | 서류 | `chapters/10-benefits.html#register` | 출생신고 1개월, 출생통보가 부모 신고를 대체하지 않음 | [N044] [N042] | 일치 |
| C101 | 서류 | `practice/07-apply.html#panel-before` | 2024-07-19 이후 출생아 병원 제한 없이 온라인 경로 | [N041] | 일치 |
| C102 | 서류 | `practice/07-apply.html#panel-before` | 신고인 자격·인증서·출생증명서·공개 신고 안내 | [N042] | 일치 |
| C103 | 서류 | `practice/07-apply.html#panel-before` | 출생통보정보 성별·일시·병원 전송 확인 | [N043] | 일치 |
| C104 | 서류 | `practice/07-apply.html#panel-after` | 등록·주민번호 확인 뒤 행복출산, 제출/결정/지급 구별 | [N098] [N040] [N043] | 일치 |
| C105 | 서류 | `practice/07-apply.html#panel-visit` | 행복출산 출산자/배우자, 친부모·시부모 대리 방문 경로 | [N098] | 일치 |
| C106 | 서류 | `practice/07-apply.html#items` | 행복출산 통합 항목과 자격, 별도 건강관리/휴직 신청 | [N098] [N081] [N046] | 일치 |
| C107 | 급여 | `chapters/10-benefits.html#cash` | 가정양육 0~11개월 100만원·12~23개월 50만원 | [N037] | 일치 |
| C108 | 급여 | `chapters/10-benefits.html#cash` | 0세 보육료 58.4만+현금 41.6만·1세 51.5만/현금차액0 | [N037] | 일치 |
| C109 | 급여 | `chapters/10-benefits.html#cash` | 출생일 포함 60일 소급·개별 접수일/예외 확인 | [N037] [N098] | 일치 |
| C110 | 급여 | `chapters/10-benefits.html#cash` | 2026 아동수당 9세 미만·기본 10만원, 부모급여 병행 | [N095] [N037] [N105] | 일치 |
| C111 | 급여 | `chapters/10-benefits.html#cash` | 수도권10/비수도권10.5/인구감소 우대11/특별12만원, 중복 가산 아님 | [N095] [N105] | 일치 |
| C112 | 급여 | `chapters/10-benefits.html#benefits-tool` | 상품권 지급 가능 지역의 기본액까지 현금 합계에 넣음 | [N095] [N105] | 보완 M09 |
| C113 | 급여 | `chapters/10-benefits.html#cash` | 상품권 추가 1만원 조건·미확인 지역 합계 유보 | [N095] [N105] | 일치 |
| C114 | 급여 | `chapters/10-benefits.html#voucher` | 첫만남 첫째200만/둘째이상300만 바우처·2024 이후 출생 2년 | [N036] | 일치 |
| C115 | 급여 | `chapters/10-benefits.html#voucher` | 건보 진료비 단태아100만·다태아기본140만원 | [N107] | 일치 |
| C116 | 급여 | `chapters/10-benefits.html#voucher` | 다태아 태아당100만원 추가지원의 인용 연결 | [N107] [N045] | 보완 M06 |
| C117 | 급여 | `chapters/10-benefits.html#voucher` | 진료비 발급일부터 사용·신청 전후 예정일/출산일부터2년 | [N107] | 일치 |
| C118 | 지원 | `chapters/10-benefits.html#care` | 건강관리 방문 지원·소득150% 일반 기준·지역 예외/본인부담 | [N081] [N084] | 일치 |
| C119 | 지원 | `chapters/10-benefits.html#care` | 예정일40일 전~출산후60일 신청·90일 사용, 입원/다태아 예외 확인 | [N084] | 일치 |
| C120 | 지원 | `chapters/10-benefits.html#local` | 지자체 금액 공통 추정 안 함·지역 공고·거주조건 확인 | [N098] | 일치 |
| C121 | 휴가 | `chapters/10-benefits.html#leave` | 출산전후 일반90일/법정미숙아100일/다태아120일·산후45/60일 | [N047] [N124] | 일치 |
| C122 | 휴가 | `chapters/10-benefits.html#leave` | 출산휴가 급여30일 상한220만원·회사부담/보험 분리 | [N124] | 일치 |
| C123 | 휴가 | `chapters/10-benefits.html#leave` | 보험급여 시작1개월 후~종료후12개월 신청 | [N124] | 일치 |
| C124 | 휴가 | `chapters/10-benefits.html#leave` | 배우자20일 유급·예정일50일 전~출산후120일·3회 분할·2026-09-18 현행 | [N099] [N100] | 일치 |
| C125 | 휴직 | `chapters/10-benefits.html#leave` | 일반급여100/100/80%·상한250/200/160만원, 정액 아님 | [N046] | 일치 |
| C126 | 휴직 | `chapters/10-benefits.html#leave` | 6+6 생후18개월 내 부모 모두·통상임금100%·상한250/250/300/350/400/450 | [N046] [N048] | 일치 |
| C127 | 휴직 | `chapters/10-benefits.html#leave` | 일반1년·부모각3개월 등 조건부1년6개월, 6+6과 다른 제도 | [N101] [N046] | 일치 |
| C128 | 부모 | `chapters/11-parents.html#recovery` | 산욕기 약6주 개인 회복 차이, NHS6~8주 검진은 영국 기준 | [N053] [N087] | 일치 |
| C129 | 부모 | `chapters/11-parents.html#mood` | 2주 이상 지속 또는 일상 장애 시 상담·2주 기다리라는 뜻 아님 | [N052] [N122] [N123] | 일치 |
| C130 | 부모 | `chapters/11-parents.html#mood` | 선별 설문은 진단 아님·점수로 안전 판정 안 함 | [N052] [N083] | 일치 |
| C131 | 부모 | `chapters/11-parents.html#mood` | 환청·망상·심한 혼란 즉시 전문평가, 임박한 위해 응급 도움 | [N122] [N123] | 일치 |
| C132 | 부모 | `chapters/11-parents.html#mood` | 아빠·파트너도 우울/불안 경험 가능, 국외 안내 표시 | [N121] | 일치 |
| C133 | 부모 | `chapters/11-parents.html#parent-crisis` | 109 자살예방·1577-0199 정신건강위기 역할 구분 | [N054] [N055] | 일치 |
| C134 | 부모 | `chapters/11-parents.html#parent-crisis` | 아이사랑1644-7373 평일09~18시 비응급 | [N073] | 일치 |
| C135 | 부모 | `chapters/11-parents.html#parent-crisis` | 상담센터02-2276-2276 평일9~12/14~17 예약 상담 | [N082] | 일치 |
| C136 | 부모 | `chapters/11-parents.html#feeding-parent` | 수유 중 약·미숙아 여부 알리고 상담·처방약 임의 중단 피함 | [N004] [N061] [N073] | 일치 |
| C137 | 부모 | `chapters/11-parents.html#feeding-parent` | 카페인 국내 잔수/NHS200mg/CDC300mg 차이·미숙아/어린 신생아 감량 | [N004] [N108] [N109] | 일치 |
| C138 | 부모 | `chapters/11-parents.html#feeding-parent` | 국내 음주 표현·NHS 피함이 가장 안전 차이, 같은 침대 피함 | [N004] [N062] | 일치 |
| C139 | 안전 | `chapters/12-safety.html#car` | 6세 미만 장구 의무·차종/법정 예외와 뒤보기 권고 구별 | [N058] [N094] | 일치 |
| C140 | 안전 | `chapters/12-safety.html#car` | 신생아 뒤보기·뒷좌석·제품/차량 설명서·키와 체중 조건 | [N094] | 일치 |
| C141 | 안전 | `chapters/12-safety.html#room` | 과열·담배 연기 피하기, 국내22~24℃/NHS16~20℃ 차이 | [N002] [N125] | 일치 |
| C142 | 안전 | `chapters/12-safety.html#room` | 질환별 습도 수치를 모든 건강한 아기 목표로 전용 안 함 | [N085] | 일치 |
| C143 | 감염 | `chapters/12-safety.html#visits` | 증상 있는 방문객 접촉 피하기·손 씻기·기침 예절·환기 | [N085] [N086] | 일치 |
| C144 | 감염 | `chapters/12-safety.html#visits` | 입술포진 현재/최근 사람의 신생아 입맞춤 피함 | [N112] | 일치 |
| C145 | 감염 | `chapters/12-safety.html#visits` | 밀접 접촉 가족 백일해 접종력·필요 접종 상담 | [N086] [N096] | 일치 |
| C146 | 안전 | `chapters/12-safety.html#visits` | 백일 이전 외출 일괄 금지 단정 안 함, 개별 상태 상담 | [N008] [N085] | 일치 |
| C147 | 안전 | `chapters/12-safety.html#family` | CDC 5세미만 동물 접촉 감독·접촉후 손 씻기, 형제 감독은 편집 제안 | [N104] | 일치 |
| C148 | 안전 | `chapters/12-safety.html#products` | 아기띠 신생아 허용·머리/목·끈·사용한도 확인 | [N057] [N125] | 일치 |
| C149 | 안전 | `chapters/12-safety.html#products` | 아기띠 얼굴 보임·턱이 가슴에 붙지 않음·띠 안 수유 피함 | [N125] | 일치 |
| C150 | 안전 | `chapters/12-safety.html#products` | 수면 제품 용도 구분·보행기 손상 위험 | [N031] [N032] [N056] | 일치 |
| C151 | 안전 | `chapters/12-safety.html#products` | 정확한 모델명으로 KC/리콜 조회, 인증이 수면 보장 아님 | [N077] [N056] | 일치 |
| C152 | 백일 | `chapters/13-hundred-days.html#next-visit` | 4개월 접종·4~6개월 검진, 누락 접종 지금 기관 문의 | [N027] [N032] | 일치 |
| C153 | 백일 | `chapters/13-hundred-days.html#rolling` | 뒤집기 움직임에 맞춰 속싸개·낙상·작은 물건 점검 | [N020] [N032] [N093] | 일치 |
| C154 | 백일 | `chapters/13-hundred-days.html#food` | 국내 모유6개월이후/분유4~6개월, WHO·CDC약6개월 차이 | [N119] [N063] [N120] | 일치 |
| C155 | 백일 | `chapters/13-hundred-days.html#food` | CDC4개월 전 비권장, 백일 이유식 날짜표로 쓰지 않음 | [N120] | 일치 |
| C156 | 기록·AI | `practice/09-records.html#record` | 모유mL 추정 안 함·수유 관찰/시각/기저귀를 진료 자료로 사용 | [N005] [N001] [N073] | 일치 |
| C157 | 기록·AI | `practice/09-records.html#talk` | WHO 의료 AI 부정확·자동화 편향·개인정보 위험, 소아전용 연구로 과장 안 함 | [N065] | 일치 |

## 출판 재검토 조건

B01~B04의 정적 응급 안내·원문 조건·누락 응급 경로를 먼저 고치고, M01~M09의 조건·인용·도구 출력을 반영한 뒤 재검토한다. 특히 공통 문구 변경은 7장만 고치지 말고 관련 본문·실습·인쇄·도구와 조사표를 함께 맞춘다. N079는 확인 가능한 원문으로 교체하거나 해당 상세 주장을 보류한다. 이 조건이 충족되기 전에는 출판 가능으로 표시하지 않는다.

검토 결과는 위험 항목의 수정 방향을 제안한 것이며, 이번 검토에서 실제 원고를 수정하거나 수정 완료를 검증한 것은 아니다.

## 원문 링크

아래 N번호는 기존 SOURCES의 URL이다. N079를 제외한 원고 인용 100개와 추가 확인 N045는 실제 본문/PDF/브라우저로 열었다. N079는 대조 불가다.

[N001]: https://health.kdca.go.kr/healthinfo/biz/health/gnrlzHealthInfo/gnrlzHealthInfo/gnrlzHealthInfoView.do?cntnts_sn=6951 "소아 발열 대처법"
[N002]: https://health.kdca.go.kr/healthinfo/biz/health/gnrlzHealthInfo/gnrlzHealthInfo/gnrlzHealthInfoView.do?cntnts_sn=5467 "영아돌연사증후군"
[N003]: https://health.kdca.go.kr/healthinfo/biz/health/gnrlzHealthInfo/gnrlzHealthInfo/gnrlzHealthInfoView.do?cntnts_sn=5723 "신생아 황달"
[N004]: https://health.kdca.go.kr/healthinfo/biz/health/gnrlzHealthInfo/gnrlzHealthInfo/gnrlzHealthInfoView.do?cntnts_sn=6586 "성공적인 모유 수유"
[N005]: https://www.childcare.go.kr/?menuno=422 "신생아 > 수유"
[N007]: https://www.childcare.go.kr/?menuno=424 "신생아 > 건강과 일상"
[N008]: https://www.childcare.go.kr/?menuno=421 "신생아 > 안전"
[N009]: https://www.childcare.go.kr/?menuno=420 "신생아 > 성장발달"
[N010]: https://www.korea.kr/news/healthView.do?newsId=148891700 "분유는 타는 즉시 바로 수유해야…크로노박터 이렇게 예방해요!"
[N011]: https://www.mfds.go.kr/brd/m_218/view.do?seq=875 "영·유아용식품의 올바른 사용을 위한 소비자가이드"
[N012]: https://www.cdc.gov/infant-toddler-nutrition/formula-feeding/preparation-and-storage.html "Infant Formula Preparation and Storage"
[N013]: https://www.healthychildren.org/English/ages-stages/baby/formula-feeding/Pages/Amount-and-Schedule-of-Formula-Feedings.aspx "Amount and Schedule of Baby Formula Feedings"
[N014]: https://www.cdc.gov/breastfeeding/breast-milk-preparation-and-storage/handling-breastmilk.html "Breast Milk Storage and Preparation"
[N015]: https://www.cdc.gov/hygiene/about/clean-sanitize-store-infant-feeding-items.html "How to Clean, Sanitize, and Store Infant Feeding Items"
[N016]: https://www.nhs.uk/baby/breastfeeding-and-bottle-feeding/breastfeeding/positioning-and-attachment/ "Breastfeeding: positioning and attachment"
[N017]: https://www.nhs.uk/baby/breastfeeding-and-bottle-feeding/breastfeeding-problems/enough-milk/ "Breastfeeding: is my baby getting enough milk?"
[N018]: https://www.cdc.gov/infant-toddler-nutrition/breastfeeding/newborn-basics.html "Newborn Breastfeeding Basics"
[N019]: https://www.aap.org/en/patient-care/newborn-infant-and-early-childhood-nutrition/newborn-and-infant-health-assessment-and-promotion/first-office-visit-3-5-days/ "First Office Visit, 3-5 Days"
[N020]: https://www.healthychildren.org/English/ages-stages/baby/sleep/Pages/A-Parents-Guide-to-Safe-Sleep.aspx "How to Keep Your Sleeping Baby Safe: AAP Policy Explained"
[N022]: https://www.nhs.uk/baby/caring-for-a-newborn/helping-your-baby-to-sleep/ "Helping your baby to sleep"
[N023]: https://www.nhs.uk/baby/caring-for-a-newborn/soothing-a-crying-baby/ "Soothing a crying baby"
[N024]: https://www.southtees.nhs.uk/services/children-and-young-people/specialty/neonatal/family-guide/babies-cry/ "Babies cry"
[N025]: https://www.kdca.go.kr/sites/kdca/download/safeSociety/2020/%EC%86%90%EC%83%81%EC%98%88%EB%B0%A9%EA%B3%BC%2B%EA%B1%B4%EA%B0%95%ED%95%9C%2B%EC%95%88%EC%A0%84%EC%82%AC%ED%9A%8C%2B2%ED%98%B8%2B%EC%B5%9C%EC%A2%85%EB%B3%B8.pdf "손상예방과 건강한 안전사회 2020 제2호"
[N026]: https://www.nhs.uk/conditions/colic/ "Colic"
[N027]: https://www.kdca.go.kr/bbs/kdca/55/310147/download.do "2026년 국가예방접종 지침(의료기관용, 10.2 수정)"
[N028]: https://nip.kdca.go.kr/irhp/index.jsp "예방접종도우미 누리집"
[N029]: https://www.nhis.or.kr/static/alim/paper/oldpaper/202202/sub/11.html "건강한 동화: 영유아 건강검진"
[N030]: https://parents.seocho.go.kr/seochobogun/seochobogun/03/10301010000002017112404.jsp "검진/예방접종: 영유아 건강검진"
[N031]: https://www.law.go.kr/flDownload.do?bylClsCd=200203&flSeq=148392197 "영유아건강검진 문진표(14~35일용), 별지 제4호"
[N032]: https://www.law.go.kr/flDownload.do?bylClsCd=200203&flSeq=148392203 "영유아건강검진 문진표(4~6개월용), 별지 제4호의2"
[N033]: https://knhanes.kdca.go.kr/knhanes/grtcht/main.do "소아청소년 성장도표"
[N034]: https://yangsan.go.kr/health/contents.do?mid=0301050000 "영유아 지원사업: 대사이상·신생아 청각검사"
[N035]: https://www.jangsu.go.kr/health/index.jangsu?menuCd=DOM_000000603014019000 "청각 선별검사 지원"
[N036]: https://www.mohw.go.kr/menu.es?mid=a10711020100 "임신·출산 지원 > 첫만남이용권"
[N037]: https://www.korea.kr/news/policyNewsView.do?newsId=148957936 "2026년 부모급여, 이렇게 지원합니다!"
[N040]: https://m.gov.kr/mw/AA020InfoCappView.do?CappBizCD=17410000001 "출산 관련 서비스 통합처리 신청(행복출산)"
[N041]: https://efamily.scourt.go.kr/ar/ArChkPrcd.do "출생일자 입력 > 출생 신고"
[N042]: https://efamily.scourt.go.kr/cs/CsBltnWrtGuide.do?bltnbordId=0000008&guideCd=0000008001&guideYn=Y "출생 신고 > 인터넷신고 안내"
[N043]: https://efamily.scourt.go.kr/cs/CsBltnWrtList.do?bltnbordId=0000003&bltnId=000000320250320000021&forwardFg=M&pageIndex=1 "인터넷 출생신고: 출생통보정보가 아직 전송되지 않았다는 메시지 FAQ"
[N044]: https://www.easylaw.go.kr/CSP/CnpClsMain.laf?ccfNo=2&cciNo=1&cnpClsNo=1&csmSeq=1830&popMenu=ov "출생신고 및 출생통보제"
[N045]: https://www.easylaw.go.kr/CSP/CnpClsMain.laf?ccfNo=1&cciNo=3&cnpClsNo=1&csmSeq=1830&popMenu=ov "임산부 의료비용 지원"
[N046]: https://www.work24.go.kr/cm/c/f/1100/selecSystInfo.do?systId=SI00000402 "육아휴직급여 제도안내"
[N047]: https://1350.moel.go.kr/rtmview.do?id=1000306429 "출산전후휴가·배우자출산휴가 모바일 상담"
[N048]: https://1350.moel.go.kr/rtmview.do?id=1000296162 "6+6 부모 함께 육아휴직제 모바일 상담"
[N050]: https://health.kdca.go.kr/healthinfo/biz/health/gnrlzHealthInfo/gnrlzHealthInfo/gnrlzHealthInfoView.do?cntnts_sn=6880 "지루 피부염"
[N051]: https://health.kdca.go.kr/healthinfo/biz/health/gnrlzHealthInfo/gnrlzHealthInfo/gnrlzHealthInfoView.do?cntnts_sn=6480 "기저귀피부염"
[N052]: https://www.childcare.go.kr/?menuno=417 "산후 우울증"
[N053]: https://www.childcare.go.kr/index.html?menuno=276 "산욕기"
[N054]: https://www.129.go.kr/faq/faq06.do?searchConsultingKeyword=F01&ssn=15224 "자살예방상담전화 FAQ: 기존 정신건강상담전화는?"
[N055]: https://www.mohw.go.kr/menu.es?mid=a10716040000 "자살예방 정책 추진"
[N056]: https://www.isafe.go.kr/DATA/bbs/94/20240827011002719.pdf "경사진 영아 수면용품 주의, 영아돌연사증후군 우려!"
[N057]: https://www.isafe.go.kr/DATA/bbs/94/20250519012710955.pdf "아기띠 사용 시 추락사고에 주의하세요!"
[N058]: https://www.law.go.kr/LSW/lsInfoR.do?efYd=20260701&lsiSeq=281875 "도로교통법"
[N059]: https://www.nhs.uk/baby/caring-for-a-newborn/washing-and-bathing-your-baby/ "Washing and bathing your baby"
[N060]: https://www.nhs.uk/conditions/reflux-in-babies/ "Reflux in babies"
[N061]: https://www.nhs.uk/baby/breastfeeding-and-bottle-feeding/breastfeeding-and-lifestyle/medicines/ "Breastfeeding and medicines"
[N062]: https://www.nhs.uk/baby/breastfeeding-and-bottle-feeding/breastfeeding-and-lifestyle/alcohol/ "Breastfeeding and drinking alcohol"
[N063]: https://www.who.int/health-topics/breastfeeding "Breastfeeding"
[N065]: https://www.who.int/news/item/18-01-2024-who-releases-ai-ethics-and-governance-guidance-for-large-multi-modal-models "WHO releases AI ethics and governance guidance for large multi-modal models"
[N066]: https://www.nhis.or.kr/nhis/index.do "국민건강보험공단 현재 누리집·검진기관 찾기"
[N069]: https://www.e-gen.or.kr/moonlight/main.do "달빛어린이병원·응급의료포털"
[N073]: https://www.childcare.go.kr/?menuno=300 "상담 안내"
[N076]: https://www.kdca.go.kr/bbs/kdca/55/306134/download.do "2026년도 호흡기감염병 관리지침"
[N077]: https://www.safetykorea.kr/ "제품안전정보센터 Safety Korea"
[N079]: https://www.kdca.go.kr/board/board.es?act=view&bid=0034&list_no=121891&mid=a20607020000 "2017 소아청소년 성장도표 개발"
[N081]: https://www.easylaw.go.kr/CSP/CnpClsMain.laf?ccfNo=2&cciNo=3&cnpClsNo=1&csmSeq=1830&popMenu=ov "전문 인력 지원: 산모·신생아 건강관리 지원사업"
[N082]: https://www.nmc.or.kr/nmc/contents/nmc22762276_roles "중앙난임·임산부심리상담센터 기능과 역할"
[N083]: https://www.ncmh.go.kr/static/jsp/viewHtmlDownload.jsp?filePath=%2F2020%2F05%2F20200528155108812168_1.pdf&filename=mental.pdf "근거기반 정신건강 평가도구: 기분장애 및 자살"
[N084]: https://www.yp21.go.kr/www/contents.do?key=2149 "산모·신생아 건강관리 지원"
[N085]: https://health.kdca.go.kr/healthinfo/biz/health/gnrlzHealthInfo/gnrlzHealthInfo/gnrlzHealthInfoView.do?cntnts_sn=6736 "세기관지염"
[N086]: https://health.kdca.go.kr/healthinfo/biz/health/gnrlzHealthInfo/gnrlzHealthInfo/gnrlzHealthInfoView.do?cntnts_sn=6676 "백일해"
[N087]: https://www.nhs.uk/baby/support-and-services/your-6-week-postnatal-check/ "Your 6-week postnatal check"
[N088]: https://www.nhs.uk/symptoms/rashes-babies-and-children/ "Rashes in babies and children"
[N089]: https://www.nhs.uk/baby/breastfeeding-and-bottle-feeding/bottle-feeding/combine-breast-and-bottle/ "How to combine breast and bottle feeding"
[N090]: https://www.nhs.uk/baby/health/when-to-get-urgent-medical-help-for-babies-and-children-under-5/ "When to get urgent medical help for babies and children under 5"
[N091]: https://mods.go.kr/boardDownload.es?bid=218&list_no=447102&seq=1 "2025년 사망원인통계 결과"
[N092]: https://www.who.int/news-room/detail/24-04-2019-to-grow-up-healthy-children-need-to-sit-less-and-play-more "To grow up healthy, children need to sit less and play more"
[N093]: https://www.healthychildren.org/English/ages-stages/baby/diapers-clothing/Pages/Swaddling-Is-it-Safe.aspx "Swaddling: Is it Safe for Your Baby?"
[N094]: https://www.healthychildren.org/English/safety-prevention/on-the-go/Pages/Car-Safety-Seats-Information-for-Families.aspx "Car Seats: Information for Families"
[N095]: https://www.mohw.go.kr/menu.es?mid=a10711030100 "아동수당 지급"
[N096]: https://health.kdca.go.kr/healthinfo/biz/health/gnrlzHealthInfo/gnrlzHealthInfo/gnrlzHealthInfoView.do?cntnts_sn=6953 "임신 중 예방접종"
[N098]: https://www.gov.kr/portal/rcvfvrSvc/dtlEx/174000000029 "출산 관련 서비스 통합처리 신청(행복출산): 2026 현행 상세"
[N099]: https://www.law.go.kr/lsLawLinkInfo.do?chrClsCd=010202&lsJoLnkSeq=1000446318 "남녀고용평등법 제18조의2: 배우자 출산전후휴가"
[N100]: https://www.moel.go.kr/news/enews/report/enewsView.do?news_seq=19964 "임신부터 출산까지, 남편이 함께한다: 배우자 지원 3종 세트"
[N101]: https://law.go.kr/lsLawLinkInfo.do?chrClsCd=010202&lsJoLnkSeq=1000446231 "남녀고용평등법 제19조: 육아휴직"
[N102]: https://www.nhs.uk/baby/caring-for-a-newborn/how-to-change-your-babys-nappy/ "How to change your baby's nappy"
[N103]: https://www.ncbi.nlm.nih.gov/sites/books/NBK579650/?report=reader "WHO recommendations on maternal and newborn care for a positive postnatal experience"
[N104]: https://www.cdc.gov/healthy-pets/about/index.html "Ways to Stay Healthy Around Animals"
[N105]: https://www.129.go.kr/faq/faq03.do?searchConsultingKeyword=B12 "아동수당 자주하는 질문"
[N107]: https://www.nhis.or.kr/static/html/wbdf/e/03/wbdfe0103_pop_15longdesc.html "임신출산 진료비 지원제도: 보험급여 설명"
[N108]: https://www.nhs.uk/baby/breastfeeding-and-bottle-feeding/breastfeeding-and-lifestyle/diet/ "Breastfeeding and diet"
[N109]: https://www.cdc.gov/breastfeeding-special-circumstances/hcp/diet-micronutrients/maternal-diet.html "Maternal Diet and Breastfeeding"
[N110]: https://www.healthychildren.org/English/tips-tools/symptom-checker/Pages/symptomviewer.aspx?symptom=Stools+-+Blood+In "Stools - Blood In"
[N111]: https://www.childcare.go.kr/web/board/BD_board.view.do?bbsCd=1023&seq=20200827141700483&showSummaryYn=N "신생아 목욕법"
[N112]: https://www.nhs.uk/conditions/neonatal-herpes/ "Neonatal herpes (herpes in a baby)"
[N119]: https://health.kdca.go.kr/healthinfo/biz/health/gnrlzHealthInfo/gnrlzHealthInfo/gnrlzHealthInfoView.do?cntnts_sn=5470 "이유기보충식(이유식)"
[N120]: https://www.cdc.gov/infant-toddler-nutrition/foods-and-drinks/when-what-and-how-to-introduce-solid-foods.html "When, What, and How to Introduce Solid Foods"
[N121]: https://www.guysandstthomas.nhs.uk/our-services/maternity-after-your-baby-born/looking-after-yourself "Maternity: after your baby is born — Looking after yourself"
[N122]: https://www.nhis.or.kr/static/alim/paper/oldpaper/202201/sub/12.html "산후우울증 — 마음 챙김"
[N123]: https://www.nhs.uk/mental-health/conditions/post-partum-psychosis/ "Postpartum psychosis"
[N124]: https://m.work24.go.kr/cm/c/f/1100/selecSystInfo.do?systId=SI00000406&systClId=SC00000246 "출산전후휴가와 출산전후휴가급여"
[N125]: https://www.nhs.uk/baby/caring-for-a-newborn/sudden-infant-death-syndrome-sids/ "Sudden infant death syndrome (SIDS)"
