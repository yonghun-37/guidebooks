# AIa · AI 도구 지도와 부록 제작 결과

완료: 2026-10-26. 기준: `docs/STYLE-GUIDE.md`, `docs/DESIGN.md` 12절, 사용자 AIa 지시, `research/ai-production.md`·`ai-models-pricing.md`·FACT-SHEET·SOURCES.

## 구현

- [x] [AI 도구 지도](../../site/chapters/05b-ai-tools.html): 5장 뒤·6장 앞, 번호 미지정. 9블록·3축·FAQ 5개·퀴즈 3문항. 리서치/글/이미지/디자인/편집·자막/영상 생성/음성/음악의 8작업 서비스·메뉴·입력/출력·무료량·가격·한국어/한국·상업 이용·AI 표시를 비교한다.
- [x] 첫 AI는 ChatGPT Free, 무료 완성은 Canva Free·Clipchamp Free·본인 소재/녹음. 유료 카드 14,900원/월, 디자인+음성 24,800원/월, 생성 영상 집중 29,000원/월 교체안을 제공한다. 콘텐츠·예산·한국어 선택 도우미와 극단값(0원 생성 영상)을 구현했다.
- [x] [프롬프트 모음](../../site/prompts.html): 뉴스 요약·카드 문안·이미지·릴스 대본·영상 생성·캡션/해시태그 6종. 넣을 메뉴·입출력·복사·좋은/나쁜 요청과 예상 결과·시간/비용·이론/실습 링크를 제공한다. 클립보드가 차단되면 전체 선택과 수동 복사를 안내한다.
- [x] [AI 모델·사용처·비용 총정리](../../site/ai-models.html): 조사 표의 274개 모델/버전을 텍스트 70·이미지 75·영상 63·음성/전사 35·음악 25·편집 앱 6개로 옮겼다. 버전 미공개 기능·종료/이전 모델도 구별한다. 24개 서비스 구독표, 범주/검색/초기화/빈 결과, 모바일 카드, 각주를 제공한다.
- [x] 비용 계산기: 뉴스카드 6장·30초 해설·8초×4클립 × 무료/낮은 비용/높은 비용 설정, 생성 시도 1~3회. 모델·사용처·분량·단가·계산식과 예산 환율 1,350원을 공개했다. API 사용분·구독 배분액·신규 구독료·최소 충전/세금을 구별한다. 결과가 비싸다는 이유로 품질 우위라고 하지 않는다.
- [x] 신규 전용 [CSS](../../site/assets/ai-guide.css)·[JS](../../site/assets/ai-guide.js)만 연결했다. 의존성·브라우저 저장·서버 전송 없음. 도식은 직접 작성한 HTML 흐름이며 서비스 화면 캡처·로고·새 AI 이미지 자산을 사용하지 않았다.
- [x] [통합 diff](phase-AIa-requests.md)와 [용어 후보](phase-AIa-glossary.md)를 남겼다. 공통 파일·PROJECT_STATE·진행 페이지는 통합 담당의 소유로 유지했다.

## 학습자 질문과 답

| 질문 | 직답·예·행동 위치 |
|---|---|
| 처음 가입할 서비스는? | 먼저 답부터·글 도구: ChatGPT Free → 원문 URL 준비 |
| 무료로 끝까지 되나? | 무료/유료 축·도우미: 추가 구독료 0원 → 본인 사진/녹음 선택 |
| 월 1~3만 원이면 무엇을 사나? | 14,900 + 9,900 = 24,800원 → 카드만이면 음성 구독 제외 |
| 한국어·상업 이용·AI 표시는? | 고르는 기준: 날짜/금액 발음 시험 → 권리·출처 신호·업로드 공개를 각각 확인 |
| 같은 모델이면 같은 요금인가? | 비용 부록: Flow 개당 크레딧/Runway 초당 달러 → 같은 경로·설정끼리 계산 |

신규 장은 이전 원고가 없어 70% 축약 기준을 적용할 비교 대상이 없다. 기존 기준선 파일은 변경하지 않았으며 세 파일에 금지어·내부어·단서 검사를 적용했다.

## 검증

| 검사 | 실제 결과·기록 |
|---|---|
| `style_lint.py` 신규 3파일 | 3/3 통과. 금지어·내부어·상자 밖 단서 0. [JSON](phase-AIa/style-lint.json) |
| `check_site.py` 전체 ReelsBook/책장 | HTML 40개, 내부 참조 2,967개, 퀴즈 57문항, 오류 0. [JSON](phase-AIa/check-site.json) |
| 1280/375/360px × 라이트/다크 | 3페이지·도우미 전 조합·계산기 3×3/재시도·복사·검색/필터·키보드·퀴즈·JS 없는 읽기·복사 거부 대안 **414검사 통과**. [코드](phase-AIa/verify-browser.mjs)·[기록](phase-AIa/browser-check.json) |
| 실제 CDN 글꼴 환경 | 동일 **414검사 통과**, 가로 넘침·콘솔/페이지·로컬 자원 오류 0. [기록](phase-AIa/browser-font-check.json)·[글꼴 로드](phase-AIa/font-check.json) |
| 통합 diff 임시 적용 | `/tmp` 복사본에서 patch 적용·크레딧만 재생성: 출처 329개, 정적 오류 0. 실제 작업 파일은 변경하지 않음. [정적](phase-AIa/integration-check.json) |
| 통합 후 경로·목차 | 3 slug·부록 루트 경로·상단 목차·하단 링크·5장/6장 이동·9블록 목차 **19검사 통과**. [코드](phase-AIa/verify-integration.mjs)·[기록](phase-AIa/integration-browser.json) |
| 공통 파일 보호 | book.js/book.css/common.js/practice.js/glossary/credits/index/PROJECT_STATE/책장 진행의 시작/종료 SHA256 9개 일치. [범위 검사](phase-AIa/scope-check.json) |
| 구문·공백 | `node --check site/assets/ai-guide.js`, `git diff --check` exit 0 |

재현: 저장소 루트에서 `python3 -m http.server 18643 --bind 127.0.0.1` 후 `node docs/results/phase-AIa/verify-browser.mjs`; 실제 글꼴 검사는 앞에 `FONT_NETWORK=1`. 검증 환경은 Linux·Chromium이며 기존 Playwright 설치를 재사용했다.

### 검토 중 수정

별도 읽기/코드 검토에서 중요한 문제 1건·작은 문제 2건을 발견해 모두 수정했다. 모델 사용처 고유명 Codex를 보존했고, 카드만 고르면 14,900원으로 표시하며, 무료 영상 한도 초과를 대표 결과에 명시했다. 비용 산술과 274행 범위는 연구와 대조했다. 직접 화면 검토에서는 모바일 표 제목이 세로로 늘어지는 문제를 찾아 CSS를 수정하고 폭 검사를 추가했다. 문체 검사에서 “로봇 한 대가”를 금지어로 오인해 “로봇 하나가”로 바꿨다. 달러 계산식의 중간값도 충분한 소수 자리로 표시했다.

최초 브라우저 검사는 미구현 페이지의 404로 실패한 뒤 구현 후 통과했다. 처음 기준선 실행은 신규 파일 부재로 적용되지 않았으며 신규 파일 검사로 전환했다. 임시 통합 검사의 첫 실패는 복사본에 쇼츠/샘플 배포 파일을 빠뜨린 것이어서 해당 원본을 복사한 뒤 통과했다.

## 화면

| 화면 | 1280px | 375px | 360px |
|---|---|---|---|
| 도구 선택 | [화면](phase-AIa/tools-1280.png) | [화면](phase-AIa/tools-375.png) | [화면](phase-AIa/tools-360.png) |
| 프롬프트 | [화면](phase-AIa/prompts-1280.png) | [화면](phase-AIa/prompts-375.png) | [화면](phase-AIa/prompts-360.png) |
| 비용 계산 | [화면](phase-AIa/models-1280.png) | [화면](phase-AIa/models-375.png) | [화면](phase-AIa/models-360.png) |
| 검색 표·모바일 카드 | [화면](phase-AIa/models-table-1280.png) | [화면](phase-AIa/models-table-375.png) | [화면](phase-AIa/models-table-360.png) |

[대표 · 장 첫 화면](phase-AIa/overview-1280.png) · [서비스 비교 표](phase-AIa/services-1280.png)

## 남은 일·한계

- 통합 담당자의 장 번호 확정·book.js diff 적용·크레딧 재생성·용어 후보 채택·PROJECT_STATE/진행 페이지 갱신·최종 검수. 기존 전체 목차에는 아직 새 3페이지가 등록되지 않았다. 각 페이지와 앞뒤 장의 직접 링크는 작동한다.
- 실제 서비스 가입·한국 계정 결제·생성·다운로드·게시, 음질/한국어 비교 실험은 수행하지 않았다. 출처가 엇갈리는 무료 접근·상업 이용·계정별 한도는 본문 확인 위치를 제공한다. 유료 API를 호출하지 않았다.
- 기존 다른 작업자의 이론·실습/쇼츠 변경을 보존했다. commit·push를 시도하지 않았다.
- 완료 알림: `scripts/notify.py`로 대표 스크린샷을 첨부해 발송, HTTP 200 확인.
