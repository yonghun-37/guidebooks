# Phase BX7 — 두 독립 검토 수정과 최종 게이트

검증 기준: 2026-10-28. **수정 및 로컬 게이트 완료**, Claude Code 최종 검수·배포 대기. BX6-policy의 차단 6·수정 7, BX6-repro의 발견 10·부분 질문 8을 반영했다. 실행은 가상 자료·로컬 mock HTTP로 수행했다. 실제 계정·유료 API·실발행·commit/push는 수행하지 않았다.

## 안전 구조와 구현 결정

- 발행 함수는 실제 관문 결과와 `gates/risk.py::may_auto_publish`로 승인 필요 여부를 정한다. 설정에서 허용한 info/play 유형, **전부 pass**, 제목·설명·본문·경험·이미지의 위험 신호 없음, 서버 신규 확인을 모두 요구한다. 직접 제작한 삽화로 명시하지 않은 미디어도 자동 대상에서 제외한다. 빈 검사 결과·미확인 신규 여부는 자동 허용하지 않는다. 자료 보류·금지 내용은 승인으로 풀지 않는다.
- 서버에서 post_id/안정적인 slug/상태를 조회한다. 기존 글의 `is_update`·신규 아님·서버 상태 이력은 재준비·재조회·재시도에도 남긴다. 수정하면 기존 승인을 지우고 같은 post_id의 새 최종본을 승인받는다. 발행 직전 서버에 이미 공개된 사실을 발견해도 신규 자동 예약으로 취급하지 않는다.
- 문서·계약·연결 등록부의 경제관계를 표시·제품 관문이 함께 읽는다. 관계별 수령 문구와 최종 HTML을 검사한다. 원고의 raw HTML은 거절하고 마크다운 렌더러와 등록 링크의 `sponsored` 처리로 만든 HTML만 허용한다.
- JPEG/PNG의 실제 형식과 컨테이너 구조를 확인한다. JPEG APP1, PNG eXIf·텍스트 청크를 검사·제거하며, 재검사한 `private/public-media/` 사본만 올린다. 원본 바이트·서버 사본 바이트를 별도로 보존/검증한다. 미지원·구조 불량은 자료 보류다. Pillow 12.3.0은 개발 테스트용이며 런타임 의존성은 추가하지 않았다.
- 비용 읽기 명령, 기한 지난 가상 갱신 예제, 우회 시도 묶음을 추가하고 예상 출력·체크포인트 ZIP을 재생성했다. 이 기록은 기존 단계 결과 문서 구조를 재사용하며 별도 중복 명세·ADR을 만들지 않았다.

## 차단 B01~B06 처리표

테스트 경로는 모두 `blog-auto-kit/tests/` 기준이다. 실제 준비·승인·발행 함수와 로컬 HTTP 서버를 사용한다.

| 발견 | 수정 | 증명 |
|---|---|---|
| B01 건강 review·아이 정보 무승인 예약 | 별도 발행 위험 분기를 제거하고 모든 관문 pass를 필수화. 본문·설명·경험·미디어까지 동일 범위로 분류. 고정 양식 밖 이름·병원·어린이집 의심은 사람 검토 | `test_bx7_default_deny.py::test_bx6_body_and_identification_never_auto`: 본문 해열제/아스피린/발열·가상 이름/병원·설명·경험 × approval/auto/after. `test_allowlist_requires_every_pass_and_verified_new_server_record`는 review/hold/block/빈 결과·미확인 신규·유형 미허용을 거절. 허용 신규의 양성 대조도 예약 성공 |
| B02 공개 글 갱신 재예약 | JSON 자가 선언 대신 서버 조회·이력 사용. 재준비 시 승인 무효화, 서버 글 재발견도 갱신 처리 | `test_public_update_stays_update_across_prepare_retry_and_query`, `test_server_existing_post_is_update_without_local_post_record`(slug/post_id), `test_publish_reads_server_status_before_auto_reschedule`. 공개 후 수정·반복 prepare에서 무승인 예약 거부, 새 승인 후 같은 post_id 예약 |
| B03 의료기기 체험·질병 광고 | comparison_only 예외 제거. 실제 사용 문장 검사. 규제 품목의 질병 예방·치료·완화 차단, 분류 불명은 자료 보류. 명시적 비사용·건조 완화는 금지로 단정하지 않음 | `test_bx7_products.py`의 질병 문안·체험·비체험·분류/리콜 양성·음성 대조. `test_counterexamples_never_reach_future_or_publish`는 재준비·사람 승인 시도도 거부. `test_bx7_contracts.py`는 계약에만 있는 관계로 제품 검사 우회도 차단 |
| B04 불충분·숨긴 표시 | 수수료/제공품/광고비/대여 각각 첫 문단의 실제 수령 표현 요구. 상업 관계 자료 없음은 보류. 프로그램과 관계에 맞춰 문구 생성. HTML 정확 비교·raw HTML 거절 | `test_bx7_products.py`: ‘제휴 활동 안내입니다.’, display:none, hidden/class/raw HTML, 복합 관계·대여 누락·빈 관계, 쿠팡의 비수수료 관계. `test_bx7_contracts.py::test_denied_or_ambiguous_relationship_is_not_receipt_disclosure`는 수수료 부인·단순 언급도 거절 |
| B05 미디어 검사 누락 | 매직바이트 JPEG/PNG 검사. JPEG EXIF/XMP·PNG eXIf/tEXt/iTXt/zTXt 검사/제거. 사본 재검사 뒤 실제 형식 MIME으로 업로드 | `test_bx7_media.py` 36건: 메타데이터 6종 × approval/auto의 prepare→publish 차단, 이름 바꾼 JPEG, 공개 사본/원격 바이트·MIME 확인, 업로드 경계에서 제거 및 원본 보존. 미지원/손상 형식도 거절 |
| B06 본문 건강·응급·약 표현 누락 | 전체 내용 건강 분류, 건강 글에 응급 문구 적용 검토 항목. 본문 발열 등은 해당 공통 문구 누락 차단. 약 접미어·mg/ml/정/포·한국어 조사 형태 보조 검사. 본문에 탐지 한계와 건강 글 필수 사람 승인 명시 | 기본 거부 반례·`test_body_fever_requires_common_text_and_all_ten_templates_stay_equal`·`test_bx7_contracts.py`의 H3 용량 3종. 숫자 출처 관문의 차단을 H3 성공으로 세지 않음. 공통 응급 10문구는 BabyBook·조사와 직접 대조 후 고정 지문으로 회귀 |

`bypass_attempts`는 위 우회 유형의 묶음 24회를 두 모드로 실행해 무승인 future/publish 0건과 금지 문안 승인 거부를 확인한다. 갱신·응급·PNG/XMP 각 변형의 상세 보장은 별도 pytest가 담당한다. 함수의 after 경로도 기본 거부로 검사하지만 CLI의 사후 확인 설정은 기존처럼 비활성이다.

## 수정 R01~R07 처리표

| 발견 | 본문·조사·키트 수정 | 증명·확인 범위 |
|---|---|---|
| R01 AdSense 연령 | A7·ads 점검표를 한국어 두 안내의 만19세로 통일. BXF-018·광고 조사·BRIEFING 갱신 | 공식 자격/연령 도움말 10-28 직접 대조, `test_korean_ads_age_has_no_18_year_old_exception` |
| R02 처리방침 항목 | A2·pages에 법30조/시행령31조, 안전조치·책임자 성명/부서/연락처·권리행사/법정대리인·해당 시 민감/가명/이전 항목 추가. 양식은 완성본 아님을 명시 | BX133/BXF-101, `test_generated_policy_has_required_completion_checklist`. 실제 처리 흐름·작성 내용의 적법성은 사람 확인 |
| R03 리콜·분류·근거 | `recall_check`와 `recall_status=none_found/recalled/unchecked` 분리, `classification_basis`·분류 값 도입. 조제식 문자열만으로 확정하지 않음. 체험 BXF-048/심의 BXF-047/리콜 BXF-044로 사유 연결 | 제품 회귀의 리콜 3상태, 분류 자료 전/후, 비체험 의료기기, 비해당 분류 대조. A5·A8·A9 설명도 일치 |
| R04 손상 JPEG | 정상 합성 JPEG 고정 바이트에 FAKE·GPS·XMP만 삽입, 재생성 스크립트 갱신 | Pillow strict verify/load로 원본·제거본 정상 열림, 제거본 Make/GPS/XMP 없음. 미디어 회귀에 포함 |
| R05 실패 각주 | 광고 BX026→현재 answer/164131, 안전수면은 BX086·신규 BX136(CPSC), 접종 BX091 실제 자료실 경로, 레뷰 약관을 제공하는 공식 JS 본문까지 확인 | SOURCES/FACT-SHEET/SOURCE-CHECKS·관련 노트·각주/공통 출처색인 갱신. 접종 첨부의 최신 연도·이용권은 확정하지 않고 실행 보류 유지. URL 수신과 내용 검증은 구별 |
| R06 호스팅 단정 | A0/A2의 미지원·현행 상충 단정 제거. 구매 전 코드 삽입·광고·플러그인·REST·복구 지원 확인으로 변경 | 호스팅 노트·사실표·출처 재대조와 로컬 링크 검사. 실제 구매/호스팅 지원 실험은 미수행 |
| R07 세금 기한 각주 | A12의 일반 기한 근거를 법70조 BX134 + 해당 신고연도 국세청 안내 BX135로 교체 | BXF-066·09-tax·BRIEFING 갱신, 기존 BX053의 해당 기한 인용 제거. 개별 소득·세무 신고는 미수행 |

원문 확인 기록은 [조사 후속 대조](../../research-blog-advanced/SOURCE-CHECKS.md)와 [사실표](../../research-blog-advanced/FACT-SHEET.md)를 따른다. 기존 독립 정책 검토 144개 주장 전부를 새로 심사했다고 주장하지 않는다.

## 재현 F01~F10 처리표

| 발견 | 처리 | 증명 |
|---|---|---|
| F01 비용 기록 열기 | A4에 `python blog.py status --costs`·세 실행의 settled/0.000000 USD 출력·예약과 확정의 뜻 추가 | CLI 비용 읽기 회귀(네트워크 호출·비용 상태 변경 없음), A4 명령/expected/체크포인트와 클린룸 |
| F02 A6 마지막 상태 | 기존 future 재사용→승인→예약 유지→mock publish 재조회로 체크포인트 설명 수정 | A6 expected/status.json·클린룸, 실제 블로그 공개 성공과 구별 |
| F03 A7 실제 오류 | 새 복사본에서 위치 0 오류를 실행해 `설정 25줄 ad_after_h2: 양의 정수가 필요함 → ad_after_h2=2로 고치세요` 삽입 | [실제 오류 기록](phase-BX7/f03-observed.json), exit1. 최종 감사의 빈 예시 1건도 복구하고 checker에 빈 코드 거절 회귀 추가 |
| F04 A11 생성 파일 | cron/launchd/Windows 예시는 이미 report임을 설명, 바꿀 run 인수가 없음을 분명히 함 | 예약 파일 회귀 및 A11 클린룸·실제 파일 대조. OS 등록은 미수행 |
| F05 폴더 오류 | A1 오류 표에 can't open file·작업 폴더 확인/이동 추가 | 해당 앵커 직답/복구 명령 확인·정적/브라우저 검사 |
| F06 협찬 대장 칸 | 생성 CSV의 3칸과 내부 이력을 구별하고, 비공개 개인 거래 메모 3행 예시·수정 요청/기한/증빙 기록법 추가 | A9 본문·출력 CSV 대조. CSV 편집이 내부 이력으로 역수입된다고 쓰지 않음 |
| F07 용어 풀이 | LLM/토큰·시드·HTTP/REST/포트·WAF/SSH/FTP/Authorization·TFAT/TFCD/TFUA·scope 등 첫 등장 근처 풀이, 기본/선택 학습 구별 | 해당 장 본문 감사·문체14장·브라우저 읽기/무JS 검사 |
| F08 조건식 이해 | A5 발췌를 may_auto_publish의 단계별 조건·줄 설명·자동 허용/사람 승인 예로 교체 | 발췌 실제 줄 비교 + 허용 목록 양성/음성 회귀, 모바일 도식 확인 |
| F09 A8 오류 표 | 실제 관계/자료/초안 오류와 다음 행동을 연결 | A8 앵커 감사·기본 명령/오류 경로 대조·브라우저 |
| F10 갱신할 글 예 | weekly.html에 별도 ‘가상 갱신 예제’와 review_due=2026-10-01·원문 확인→수정→새 승인 표시 | `test_weekly_report_includes_separate_fixed_overdue_example`, A10 출력/클린룸. 실제 서버 글을 가짜로 추가하지 않음 |

## 부분 판정 8개 질문의 직답

새 초보자 사용성 시험을 했다는 뜻은 아니다. 작성자가 해당 절 첫 문장·구체 예·다음 행동을 다시 확인했다.

| 질문 | 수정한 첫 직답·연결 위치 |
|---|---|
| A1-Q5 | [A1 오류](../../site-blog/advanced/01-environment.html#errors): mock는 비어 있는 임시 포트를 고르므로 고정 포트 충돌은 보통 Docker 선택 경로에서 해결. 포트 변경 예와 연결 오류 진단 제시 |
| A2-Q2 | [A2 서버](../../site-blog/advanced/02-wordpress.html#server): WordPress.com 유료 플랜의 플러그인/WordAds와 설치형의 직접 관리 차이를 먼저 설명. 선택 플랜 구매 전 기능 확인 |
| A2-Q5 | [A2 비밀번호/이전](../../site-blog/advanced/02-wordpress.html#password): 고정 WordPress/MariaDB 이미지, DB+업로드 폴더 함께 복구. 새 서버 이전 4단계 제시 |
| A4-Q6 | [A4 비용](../../site-blog/advanced/04-drafts.html#experience): 키트 monthly_cap_usd와 공급자 Project settings→Limits→Spend 위치 직답. 비용 명령/출력과 재시도 포함 예산 예약 설명 |
| A6-Q6 | [A6 오류](../../site-blog/advanced/06-publish.html#errors): API 키만으로 글쓰기 불가, OAuth와 본인 프로젝트 요청 할당량 확인. 콘솔의 항목/단위와 광고 연결 구별 |
| A9-Q2 | [A9 미디어킷](../../site-blog/advanced/09-sponsorship.html#media-kit): 실제 기간·방문·검색 클릭과 내 설명이 잘 드러나는 대표글. 대표글 2개 선택 예 |
| A9-Q3 | [A9 흐름](../../site-blog/advanced/09-sponsorship.html#overview): 내 문의의 날짜·상태·받은 답·수정 요청·기한·증빙을 개인 메모 한 행씩 기록. 별도 비공개 예제 표와 키트 대장 구별 |
| A9-Q6 | [A9 세금/권리](../../site-blog/advanced/09-sponsorship.html#report): 현물도 기록, 2차 사용의 매체·기간·편집·별도 비용을 계약에 명시. 구체 범위 예 |

## 최종 게이트와 증거

| 게이트 | 결과 | 증거 |
|---|---|---|
| expected 재생성·--check | 13개 장 시작 상태/expected 생성·비교 성공 | [생성](phase-BX7/build-expected.txt), [비교](phase-BX7/build-check.txt), 최종 클린룸에서도 --check 실행 |
| 본문↔키트 | 14장·기본 명령31·출력31·발췌14, 불일치0 | [대조](phase-BX7/alignment.txt). 빈 코드 예시·누락 비용 명령·누락 우회 시나리오도 거절 |
| 전체 pytest | 키트245개 통과 | [전체 출력](phase-BX7/pytest.txt), 추가 독립 재검토에서 BX7 회귀120개 통과 |
| 검사기 pytest | 63개 통과 | [검사기 출력](phase-BX7/scripts-tests.txt) |
| 클린룸 재현 | Python3.11.15 새 venv·키트만 복사, A1→E2E·7시나리오·expected 비교·245 tests 통과 | [전체 로그](phase-BX7/repro.txt), 사용 가능한 3.12 인터프리터는 없어 실행하지 않음 |
| 문체 | 심화14장 통과, 금지/내부 용어·단서 위반0 | [문체](phase-BX7/style-lint.json) |
| 네 책 정적 검사 | Reels51·Shorts49·Blog50·Baby35 HTML, 오류 각0 | [Reels](phase-BX7/check-site.json), [Shorts](phase-BX7/check-site-shorts.json), [Blog](phase-BX7/check-site-blog.json), [Baby](phase-BX7/check-site-baby.json) |
| 브라우저 | 심화14장+목차2경로+출처: 102화면(1280/375/360×라이트/다크), 무JS34·도구/저장42, 가로넘침/콘솔/페이지/로컬HTTP 오류0 | [결과·입력 지문](phase-BX7/browser.json), [실행](phase-BX7/browser-stdout.txt), [재현 스크립트](phase-BX7/verify-browser.cjs), 같은 폴더 PNG. 마지막 문구 수정 후 다시 실행 |
| 변경 경계 | 다른 책/키트 수정 없음, commit/push 없음 | 최종 git diff --check와 변경 경로 감사 |

최종 입력에서 브라우저 source hash가 모두 일치함을 확인했다. 중간 원고 동기화 중의 해시 변경은 실패로 검출하고 최종 입력에서 재실행했다. 최종 게이트가 반례 발견·수정 이전의 통과 기록을 대신하지 않게 했다.

## 여전히 사람이 해야 하는 것

- 약 이름·질병·체험·식별·관계 문구 검사는 유한한 어휘/패턴의 **보조 장치**다. 모든 자연어·사진 내용을 잡는다고 보장하지 않는다. 건강 분류 글은 사람이 읽고 승인한다. 게시 전 원문 주장·적용 월령·공통 응급 문구·제품 허용 문안·실제 경험을 확인한다.
- official/claims/experience_by/제품 분류 근거/직접 제작 표시는 입력한 메모다. 코드가 외부 원문의 진실·실제 사용·권리·동의를 증명하지 않는다. 사진의 얼굴·명찰·배경·파일명과 본문이 결합해 아이를 식별하는지도 사람이 본다. 샘플의 그림책 활동 구성은 편집 제안과 건강 수칙을 구별한다.
- 관계별 문구가 생성돼도 실제 받은 물품·현금·수수료·대여와 계약, 게시 화면의 글자 크기/노출을 확인한다. 금지 문안을 승인만 눌러 해결하지 않는다. 개인정보처리방침은 실제 처리 전 흐름·수탁/이전·연락처·권리행사 절차를 완성해야 한다.
- 최신 접종 첨부의 연도/이용권, 재열람이 필요한 리뷰타임 안내, 쿠팡 live API 자격/서명/쿼터 등 확인 공백은 실행 보류를 유지한다. 호스팅 구매·복구 지원과 실제 광고/제휴 심사·국세청 신고연도 안내·세금/휴직급여의 개인 적용은 운영자가 확인한다.
- 생성한 미디어킷/보고서는 가상·집계 자료다. 실제 연락처·상담·아이 정보·세금 증빙·개인 협찬 메모는 공개 저장소에 넣지 않는다. 출력/상태/실제 데이터의 공개 여부를 직접 결정한다.
- Windows/macOS 실기기, Docker/실호스팅·인증·유료 모델·실수집·실발행·OS 예약 등록/다음 날 실행은 이번에 시험하지 않았다. Chromium 로컬 검사와 mock 성공은 실제 서비스 성공이나 독립 의료/법률 검토를 뜻하지 않는다. 다음 단계는 Claude Code 검수·커밋·배포다.

단계 완료 알림: 요청한 `scripts/notify.py`로 디스코드 전송 성공(HTTP 200). commit/push는 하지 않았다.
