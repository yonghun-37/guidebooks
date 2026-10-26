# Phase 1b 결과 — 확장 자료조사와 종합 브리핑

작성: 2026-10-26, Codex. **2026년 10월 조사 기준**, 컷오프2026-10-26.

## 범위·진행·완료 판정

요구 범위는 PLAN의 Phase1b만이다. Phase1의12개 노트·출처·사실표·결과와 DESIGN/PLAN의 Hermes 호출법을 먼저 검토했다. 이 작업은 기존 조사 기록을 확장하는 Level2 문서 작업이며, 별도 specs/ADR 대신 이 결과·기존 사실표·주제 노트를 지속 기록으로 사용했다.

- [x] 미확인·약한 근거·한국 가용성 공백을8개 묶음으로 정리해 초기 gap-fill 질의에 포함.
- [x] 주제13~26의14개 원질의 작성·실행, 원응답 보존·runs.jsonl 계속 기록.
- [x] 초기 응답 품질 확인 후14개 주제를 정확 URL·단일 쟁점 중심의 보충 질의로 재조사.
- [x] Codex 직접 열람으로 공식 문서·연구·사례 보완, 출처/사실표·14개 노트·8부 브리핑 작성.
- [x] 최종 정합성 검사40개 통과·결과 반영.
- [ ] Git 커밋 — 실행 환경의 .git 읽기 전용으로 불가.
- [x] Discord 브리핑 첨부 보고(HTTP200).

**조사 산출물 작성과 모든 정책·한국 계정·법률 적용의 확인 완료는 다른 상태다.** Hermes 실행28회는 모두 exit0이지만, 실질적으로 공식 근거를 일부 얻은 실행은 가격 주제1회뿐이다. 나머지27회는 중계 프록시403으로 본문·검색 근거를 얻지 못했다. URL만 존재하는 실패 보고를 성공 조사로 계산하지 않았다. 정확 URL을 제공한 보충에서도 같은 장애가 반복됐고, 제공한 숫자를 되풀이한 부분은 독립 검증으로 채택하지 않았다.

## 수행 전략과 실제 결과

처음에는14개 주제를 최대4개씩 실행했다. 초기에 나온 실패 보고를 읽고 공식 원문·날짜·한국 적용 공백을 평가했다. 넓은 gap-fill은 마지막까지 진행 중이었으므로, 보충 묶음은3개 병렬로 제한해 전체 동시 실행을4개 이하로 유지했다. 각 질의는 timeout900, provider openai-codex, web 도구, --max-turns40을 사용했다. Hermes 코드·config·runtime·DB·컨테이너·네트워크 설정은 변경하지 않았다.

웹 중계 장애를 해결했다는 주장 없이 Codex의 별도 웹 열람과 curl로 원문을 보완했다. HTTP200이라도 빈본문·로그인·메뉴만 있으면 본문 확인으로 세지 않았다. web에서 읽었지만 보조 curl이403인 사례도 두 요청의 결과를 구분해 기록했다. 약관의 상업 이용 범위와 한국 계정에서의 실제 동작·결제·품질 실증도 구분했다.

## 산출물과 수량

- [BRIEFING.md](../../research/BRIEFING.md): 한 쪽 요약→주제별 발견→초보자10가지→수익/시간→위험→도구 조합→미확인→목차 제안의8부.
- 주제별 노트14개: 기존 형식의 핵심 사실·수치표·한국 가용성·불확실/상충·장별 반영, 원응답 경로·SHA256·각주.
- [SOURCES.md](../../research/SOURCES.md): 신규56개를 S118~S173으로 추가, 전체173개 출처·후보. 기존 출처7개는 ID를 유지하고 Phase1b 재확인 범위를 덧붙였다.
- [FACT-SHEET.md](../../research/FACT-SHEET.md): 신규73개 사실/검증 공백, 기존100개를 보존해 총173개. 해결 여부는 GAP-01~10과 [gap-fill.md](../../research/gap-fill.md)에 연결했다.
- 신규 출처 중 공식 A등급 관련 본문 직접 확인45개. 신규 B등급 포함 직접 확인52개이며, 검색/접근 실패 후보4개는 제외했다. 전체 Phase1b 재확인 레코드63개 중 관련 본문을 읽은 것은59개다. 출처 수는 문서 단위이며 모든 주장·기능의 검증 완료 수가 아니다.
- [provenance-phase-1b.json](../../research/provenance-phase-1b.json):28회 질의/원응답 경로·해시·시간·exit·품질 평가. [verification-phase-1b.json](../../research/verification-phase-1b.json): 직접 읽은 절·범위와 보조HTTP응답 해시. [validation-phase-1b.json](../../research/validation-phase-1b.json): 정합성 검사 결과.

원응답 전문은 Git에 넣지 않고 `/home/yonghun/project/hermes-research/output/ai-insta-research-20261026/raw/`에 그대로 보존했다. 질의는 같은 RUN의queries/, 실행 기록은runs.jsonl이다. Phase1의16개 기록을 지우지 않고 이번28개를 추가했다(누적44개). 직접 읽은 HTML/PDF는 /tmp의 조사 캐시이며 영구 산출물로 주장하지 않는다.

## 실행 기록

Phase1b 28/28회, 보충14회 포함. 실패 명령의 재시도는 없으며, 근거가 부족한 원응답의 내용 보충은 각 주제1회씩이다. 시각은 UTC, 한국은+09:00이다. 구간을 계산한 최대 동시 실행은4개다.

| 질의 | 시작 UTC | 종료 UTC | exit | 바이트 | 품질 |
| --- | --- | --- | --- | --- | --- |
| korea-cases | 00:26:23 | 00:27:23 | 0 | 5,990 | 근거 확보 실패 |
| global-faceless-ai | 00:26:23 | 00:27:27 | 0 | 5,606 | 근거 확보 실패 |
| cross-platform | 00:26:23 | 00:27:55 | 0 | 10,771 | 근거 확보 실패 |
| korea-creator-economy | 00:26:23 | 00:27:50 | 0 | 9,333 | 근거 확보 실패 |
| content-craft | 00:27:23 | 00:28:51 | 0 | 9,442 | 근거 확보 실패 |
| music-assets-licensing | 00:27:27 | 00:29:02 | 0 | 11,625 | 근거 확보 실패 |
| news-sources | 00:27:50 | 00:29:35 | 0 | 12,998 | 근거 확보 실패 |
| ai-tools-pricing | 00:27:55 | 00:30:17 | 0 | 18,810 | 일부 공식본문 |
| nocode-pipelines | 00:28:51 | 00:30:11 | 0 | 10,364 | 근거 확보 실패 |
| account-setup-security | 00:29:02 | 00:30:08 | 0 | 9,395 | 근거 확보 실패 |
| analytics-metrics | 00:29:35 | 00:31:06 | 0 | 11,444 | 근거 확보 실패 |
| misinformation-ethics | 00:30:08 | 00:32:32 | 0 | 15,669 | 근거 확보 실패 |
| learning-resources | 00:30:11 | 00:31:19 | 0 | 7,094 | 근거 확보 실패 |
| gap-fill | 00:30:17 | 00:39:25 | 0 | 12,803 | 근거 확보 실패 |
| korea-cases-supplement | 00:36:19 | 00:37:12 | 0 | 6,117 | 근거 확보 실패 |
| global-faceless-ai-supplement | 00:36:19 | 00:37:22 | 0 | 8,206 | 근거 확보 실패 |
| cross-platform-supplement | 00:36:19 | 00:37:14 | 0 | 6,486 | 근거 확보 실패 |
| korea-creator-economy-supplement | 00:37:12 | 00:38:05 | 0 | 5,442 | 근거 확보 실패 |
| content-craft-supplement | 00:37:14 | 00:38:11 | 0 | 6,534 | 근거 확보 실패 |
| music-assets-licensing-supplement | 00:37:22 | 00:38:13 | 0 | 5,028 | 근거 확보 실패 |
| news-sources-supplement | 00:38:05 | 00:39:03 | 0 | 7,365 | 근거 확보 실패 |
| ai-tools-pricing-supplement | 00:38:11 | 00:38:58 | 0 | 5,895 | 근거 확보 실패 |
| nocode-pipelines-supplement | 00:38:13 | 00:39:10 | 0 | 6,677 | 근거 확보 실패 |
| account-setup-security-supplement | 00:38:58 | 00:39:49 | 0 | 5,650 | 근거 확보 실패 |
| analytics-metrics-supplement | 00:39:03 | 00:39:45 | 0 | 6,305 | 근거 확보 실패 |
| misinformation-ethics-supplement | 00:39:10 | 00:40:21 | 0 | 8,183 | 근거 확보 실패 |
| learning-resources-supplement | 00:39:45 | 00:40:46 | 0 | 8,432 | 근거 확보 실패 |
| gap-fill-supplement | 00:39:49 | 00:41:00 | 0 | 8,269 | 근거 확보 실패 |

## 주제별 출처 품질과 남은 공백

수는 노트에 인용한 고유 출처 ID다. 직접 확인 수는 이번 단계의 확인 레코드와 Phase1의 직접 확인 표시를 함께 읽었다. 주제 간 중복은 합산하지 않는다.

| 주제 | 출처/후보 수 | 이번 단계 본문 직접 확인 수 | 판정·남은 공백 |
| --- | --- | --- | --- |
| [korea-cases](../../research/korea-cases.md) | 7 | 7 | 당사자+인터뷰3사례,Instagram단독 손익 미확인 |
| [global-faceless-ai](../../research/global-faceless-ai.md) | 8 | 7 | 스튜디오·가상인물·교육,수익은 자기진술·순익 미검증 |
| [cross-platform](../../research/cross-platform.md) | 10 | 8 | YouTube한국, TikTok1만/5만 상충;클립은검색·Threads현행미확인 |
| [korea-creator-economy](../../research/korea-creator-economy.md) | 4 | 2 | 정부 원조사 확보;국내뉴스계정 단가/플랫폼약관 미확인 |
| [content-craft](../../research/content-craft.md) | 6 | 4 | W3C·Buffer방법론;한국 고정시간/훅 임계값 미확인 |
| [music-assets-licensing](../../research/music-assets-licensing.md) | 8 | 7 | 공공누리·소재·음원반출범위;Meta한국음원표 미확인 |
| [news-sources](../../research/news-sources.md) | 7 | 5 | NAVER신규/기존·NewsAPI약관;공지전문/RSS개별계약 미확인 |
| [ai-tools-pricing](../../research/ai-tools-pricing.md) | 17 | 10 | 한국어TTS플랜·무료/상업권·API종량;실측품질/일부가격 미확인 |
| [nocode-pipelines](../../research/nocode-pipelines.md) | 13 | 7 | 공개템플릿3개·커넥터요건;실행/라벨/결제 미검증 |
| [account-setup-security](../../research/account-setup-security.md) | 8 | 4 | 공식보안/한국Verified출시;현행메뉴/복구/요금 미검증 |
| [analytics-metrics](../../research/analytics-metrics.md) | 5 | 3 | APIviews이력·합산범위;앱발언/단위 일부 미확인 |
| [misinformation-ethics](../../research/misinformation-ethics.md) | 9 | 4 | 미국전환범위·연구·최신가이드소개;한국집행/개별법률 미확인 |
| [learning-resources](../../research/learning-resources.md) | 11 | 7 | 공개자료10개 학습경로;Blueprint/유료강의 검증 보류 |
| [gap-fill](../../research/gap-fill.md) | 44 | 21 | 도구/사례/커넥터 부분 해결;수익화/한도/국외세무 등 남음 |

## 새 핵심 공식 출처의 직접 확인 예

아래는 최소5개 요구를 넘는 대표 대조다. 상세 출처·방법·확인 범위는 verification에 있다.

| 출처 | 직접 확인한 범위 | 한계 |
| --- | --- | --- |
| S118 YouTube YPP | 초기 후원/광고 조건·기간·한국 국가목록 | 실제 신청·지급 미검증 |
| S120 NAVER 뉴스검색 | 반환필드·한도·기존 인증 | 기사 재사용 허락 아님 |
| S125 ElevenLabs FAQ | 무료 상업불가·유료 생성기간·베타 제외 | 개별 화자/한국 결제 별도 |
| S126 타입캐스트 | 최초 무료량·Basic 가격/다운로드·상업표시·기업 조건 | VAT·실측 품질 별도 |
| S128 경기도교육청 | 공공누리1~4유형·표식·출처 조건 | 개별 사진 권리 확인 필요 |
| S140·S141 TikTok | 일한약관5만과2026한국공지1만 직접 대조 | 현재 계정 적용·개정 동기 미확인 |
| S143 정부 실태조사 | PDF1~3쪽:2024실적·2025발표·표본·산업 범위 | 개인 수입/Instagram 단가 아님 |
| S155·S156 커넥터 | Zapier/Make 로그인·페이지·계정 요건 | 한국 실연결 미검증 |
| S171 정부 AI 가이드 점검 | 2026-10-08 출력/학습/등록 안내 구분 | 개별 뉴스요약 소송 판결 아님 |

## 상충·공백 처리와 목차 제안

- **상충:** TikTok S140의5만명과 S141의1만명, 기존 Meta API S001/S003의100/50을 양쪽 출처와 남겼다. 변경시점/대상·실효값을 임의 선택하지 않았다.
- **과거/현재:** Gifts S005/S006의500/5000, Verified출시 가격,2022인터뷰는 시기·범위를 밝혔고 현행 확정값으로 승격하지 않았다.
- **연구 범위:** 시장 매출·다채널 구독자·최고월 매출·관찰연구를 한국 초보자 예상수입으로 환산하지 않았다. Socialinsider의 컷오프 초과 기간 문제는 유지했다.
- **근거 부족:** 클립·NAVER이관 공지는 검색 발췌, Vrew가격은 가격표가 없는 반환으로 구분했다. 한국수익화·법령첨부/계도·국외세무·개별권리·복구 등의 남은 항목은 GAP표와 BRIEFING⑦을 따른다.
- **목차 제안:** 사례 수입원 분리, 뉴스 검색/권리 분리, TTS/음원 분기, 사람 승인, 측정 범위·정정·보안을 해당 장에 추가하도록 BRIEFING⑧에서 제안했다. DESIGN/PLAN·사이트·키트는 변경하지 않았다.

## 검증

최종 문서 정합성 검사40개를 실행해 모두 통과했다.28개 query/raw 해시·바이트수, 공통 질의 요구,28회 예산·동시최대4개,14개 노트 구조/각주,173개 출처/사실 ID, 로컬 링크·앵커, 보호 파일 해시와 Git diff 공백 검사가 통과했다. 최초 실행에서는 검사 결과 파일 자체가 아직 생성되기 전의 링크2개를 누락으로 잡았고, 결과 파일 생성 후 재실행에서 모두 통과했다. Phase1의16개 질의/원응답 해시도 별도 대조해 그대로임을 확인했다. 웹 사실·한국 계정·법률 적용·한국어 품질 자체를 자동 판정한 검사는 아니다. 사이트/스타터 키트 테스트·한국 계정 로그인/게시·유료 API는 이번 Phase1b 검증 범위가 아니어서 실행하지 않는다.

## Git·동시 작업

`findmnt -T .git -n -o TARGET,OPTIONS`에서 저장소의 .git 마운트가 ro임을 확인했다. 환경 권한 지침도 .git 쓰기를 허용하지 않는다. 따라서 `git add`·`git commit`은 시도하지 않았으며, 요청한 `Phase 1b: extended research and briefing` 커밋은 **미완료**다. 권한 우회·외부 Git 경로·원격 쓰기는 하지 않았다. Claude Code 검수 후 쓰기가 가능한 환경에서 이번 소유22개 파일만 커밋하는 후속 조치가 남는다.

작업 도중 다른 작업자의 starter-kit/ 및 Phase4b 산출물 변경이 나타났다. 이를 변경·검증·되돌리지 않았다. docs/reference-analysis.md·docs/results/phase-2.md의 시작 전 해시를 보존해 최종 대조한다. 다른 작업자가 Phase4(3005fa0)·Phase4b(b6e0155)를 커밋한 것도 read-only git log에서 확인했다. 기존 Phase1 결과의 커밋대기 문구는 역사 기록으로 두며, 이번 read-only git log에서 e22bd23(Phase1 커밋)이 이미 존재함을 확인해 PROJECT_STATE의 현황을 교정한다.

## Discord 보고

`python3 scripts/notify.py "✅ [Phase 1b 완료] ..." research/BRIEFING.md`를 실행했다.5줄 한국어 요약과 BRIEFING 첨부를 전송했고 HTTP200을 받았다. 보고 내용에 웹중계 실패·미확인 공백·커밋 불가를 포함했다. 토큰은 출력하거나 문서에 넣지 않았다.
